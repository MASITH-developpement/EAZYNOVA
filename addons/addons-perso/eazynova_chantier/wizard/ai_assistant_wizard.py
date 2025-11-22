# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging
import json

_logger = logging.getLogger(__name__)


class AiAssistantWizard(models.TransientModel):
    """
    Wizard pour l'assistant IA EAZYNOVA
    Interface conversationnelle avec l'IA
    """
    _name = 'eazynova.ai.assistant.wizard'
    _description = 'Assistant IA EAZYNOVA'
    
    question = fields.Text(
        string="Votre question",
        required=True,
        help="Posez votre question à l'assistant IA"
    )
    
    context_model = fields.Char(
        string="Modèle contextuel",
        help="Modèle Odoo en contexte"
    )
    
    context_id = fields.Integer(
        string="ID contextuel",
        help="ID de l'enregistrement en contexte"
    )
    
    response = fields.Html(
        string="Réponse",
        readonly=True
    )
    
    conversation_history = fields.Text(
        string="Historique",
        help="Historique de la conversation (JSON)"
    )
    
    def action_ask(self):
        """
        Envoie la question à l'IA et récupère la réponse
        """
        self.ensure_one()
        
        # Vérification que l'IA est activée
        ai_enabled = self.env['ir.config_parameter'].sudo().get_param(
            'eazynova.ai_assistance_enabled', 'False'
        )
        
        if ai_enabled != 'True':
            raise UserError(_("L'assistance IA n'est pas activée dans les paramètres."))
        
        # Récupération du provider
        provider = self.env['ir.config_parameter'].sudo().get_param(
            'eazynova.ai_provider', 'anthropic'
        )
        
        # Construction du contexte
        context = self._build_context()
        
        # Appel à l'IA
        try:
            response = self._call_ai(self.question, context, provider)
            
            # Mise à jour de l'historique
            history = json.loads(self.conversation_history or '[]')
            history.append({
                'question': self.question,
                'response': response,
                'timestamp': fields.Datetime.now().isoformat()
            })
            
            self.write({
                'response': response,
                'conversation_history': json.dumps(history),
                'question': ''  # Reset pour nouvelle question
            })
            
        except Exception as e:
            _logger.error(f"Erreur assistant IA: {str(e)}")
            raise UserError(_("Erreur lors de la communication avec l'IA: %s") % str(e))
        
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }
    
    def _build_context(self):
        """
        Construit le contexte pour l'IA
        """
        context = {
            'user': {
                'name': self.env.user.name,
                'company': self.env.company.name,
                'lang': self.env.user.lang,
            },
            'timestamp': fields.Datetime.now().isoformat(),
        }
        
        # Ajout du contexte métier si disponible
        if self.context_model and self.context_id:
            try:
                record = self.env[self.context_model].browse(self.context_id)
                if record.exists():
                    context['business_context'] = {
                        'model': self.context_model,
                        'record_name': record.display_name if hasattr(record, 'display_name') else str(record),
                    }
            except Exception as e:
                _logger.warning(f"Impossible de charger le contexte métier: {str(e)}")
        
        return context
    
    def _call_ai(self, question, context, provider):
        """
        Appelle l'API IA
        """
        if provider == 'anthropic':
            return self._call_anthropic(question, context)
        elif provider == 'openai':
            return self._call_openai(question, context)
        else:
            return _("Provider IA non configuré ou non supporté.")
    
    def _call_anthropic(self, question, context):
        """
        Appel à l'API Anthropic Claude
        """
        api_key = self.env['ir.config_parameter'].sudo().get_param('eazynova.ai_api_key', '')
        
        if not api_key:
            return _("Clé API Anthropic non configurée.")
        
        try:
            import anthropic
            
            client = anthropic.Anthropic(api_key=api_key)
            
            # Construction du prompt système
            system_prompt = f"""Tu es un assistant IA pour EAZYNOVA, un système de gestion d'entreprise.
Tu aides les utilisateurs avec leurs questions sur la gestion de chantiers, factures, et autres aspects métier.
Contexte utilisateur: {json.dumps(context, ensure_ascii=False)}
Réponds en français, de manière claire et professionnelle."""
            
            # Appel API
            message = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": question}
                ]
            )
            
            return message.content[0].text
            
        except ImportError:
            return _("La bibliothèque Anthropic n'est pas installée. Contactez votre administrateur.")
        except Exception as e:
            _logger.error(f"Erreur API Anthropic: {str(e)}")
            return _("Erreur lors de l'appel à l'API Anthropic: %s") % str(e)
    
    def _call_openai(self, question, context):
        """
        Appel à l'API OpenAI
        """
        api_key = self.env['ir.config_parameter'].sudo().get_param('eazynova.ai_api_key', '')
        
        if not api_key:
            return _("Clé API OpenAI non configurée.")
        
        try:
            import openai
            
            client = openai.OpenAI(api_key=api_key)
            
            # Appel API
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": f"Tu es un assistant IA pour EAZYNOVA. Contexte: {json.dumps(context, ensure_ascii=False)}"
                    },
                    {
                        "role": "user",
                        "content": question
                    }
                ],
                max_tokens=1024
            )
            
            return response.choices[0].message.content
            
        except ImportError:
            return _("La bibliothèque OpenAI n'est pas installée. Contactez votre administrateur.")
        except Exception as e:
            _logger.error(f"Erreur API OpenAI: {str(e)}")
            return _("Erreur lors de l'appel à l'API OpenAI: %s") % str(e)
    
    def action_new_conversation(self):
        """
        Démarre une nouvelle conversation
        """
        self.write({
            'question': '',
            'response': '',
            'conversation_history': '[]'
        })
        
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }