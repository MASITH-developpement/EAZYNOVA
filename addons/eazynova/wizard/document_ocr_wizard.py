# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import base64
import logging
import json

_logger = logging.getLogger(__name__)


class DocumentOcrWizard(models.TransientModel):
    """
    Wizard pour le traitement OCR de documents
    Permet d'extraire du texte et des données structurées depuis des images/PDFs
    """
    _name = 'eazynova.document.ocr.wizard'
    _description = 'Assistant OCR Document'
    
    document = fields.Binary(
        string="Document",
        required=True,
        help="Image ou PDF à traiter"
    )
    
    document_filename = fields.Char(
        string="Nom du fichier"
    )
    
    document_type = fields.Selection([
        ('generic', 'Document générique'),
        ('invoice', 'Facture'),
        ('quote', 'Devis'),
        ('delivery', 'Bon de livraison'),
        ('contract', 'Contrat'),
        ('expense', 'Note de frais'),
    ], string="Type de document",
       default='generic',
       required=True,
       help="Type de document pour extraction intelligente"
    )
    
    language = fields.Selection([
        ('fra', 'Français'),
        ('eng', 'Anglais'),
        ('spa', 'Espagnol'),
        ('deu', 'Allemand'),
        ('ita', 'Italien'),
    ], string="Langue",
       default='fra',
       required=True
    )
    
    state = fields.Selection([
        ('upload', 'Upload'),
        ('processing', 'Traitement'),
        ('done', 'Terminé'),
    ], default='upload',
       string="État"
    )
    
    # Résultats
    extracted_text = fields.Text(
        string="Texte extrait",
        readonly=True
    )
    
    extracted_data = fields.Text(
        string="Données structurées (JSON)",
        readonly=True,
        help="Données extraites au format JSON"
    )
    
    confidence_score = fields.Float(
        string="Score de confiance (%)",
        readonly=True,
        help="Niveau de confiance de l'extraction"
    )
    
    error_message = fields.Text(
        string="Message d'erreur",
        readonly=True
    )
    
    # Options avancées
    auto_create_record = fields.Boolean(
        string="Créer automatiquement l'enregistrement",
        default=True,
        help="Crée automatiquement un enregistrement (facture, devis, etc.) avec les données extraites"
    )
    
    def action_process(self):
        """
        Lance le traitement OCR du document
        """
        self.ensure_one()
        
        # Vérification que l'OCR est activé
        ocr_enabled = self.env['ir.config_parameter'].sudo().get_param(
            'eazynova.ocr_enabled', 'False'
        )
        
        if ocr_enabled != 'True':
            raise UserError(_("L'OCR n'est pas activé dans les paramètres."))
        
        if not self.document:
            raise UserError(_("Veuillez uploader un document."))
        
        self.write({'state': 'processing'})
        
        try:
            # Traitement OCR
            result = self._process_ocr()
            
            # Mise à jour des résultats
            self.write({
                'state': 'done',
                'extracted_text': result.get('text', ''),
                'extracted_data': json.dumps(result.get('data', {}), indent=2, ensure_ascii=False),
                'confidence_score': result.get('confidence', 0.0) * 100,
                'error_message': False
            })
            
            # Création automatique de l'enregistrement si demandé
            if self.auto_create_record and result.get('data'):
                self._create_record_from_data(result['data'])
            
        except Exception as e:
            _logger.error(f"Erreur OCR: {str(e)}")
            self.write({
                'state': 'upload',
                'error_message': str(e)
            })
        
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }
    
    def _process_ocr(self):
        """
        Traite le document avec OCR
        
        Returns:
            dict: {
                'text': str,
                'data': dict,
                'confidence': float
            }
        """
        # Décodage du document
        document_data = base64.b64decode(self.document)
        
        # Détection du type de fichier
        file_type = self._detect_file_type(document_data)
        
        if file_type == 'pdf':
            return self._process_pdf(document_data)
        elif file_type in ['image/jpeg', 'image/png', 'image/tiff']:
            return self._process_image(document_data)
        else:
            raise UserError(_("Type de fichier non supporté."))
    
    def _detect_file_type(self, data):
        """
        Détecte le type de fichier
        """
        if data.startswith(b'%PDF'):
            return 'pdf'
        elif data.startswith(b'\xff\xd8\xff'):
            return 'image/jpeg'
        elif data.startswith(b'\x89PNG'):
            return 'image/png'
        elif data.startswith(b'II*\x00') or data.startswith(b'MM\x00*'):
            return 'image/tiff'
        else:
            return 'unknown'
    
    def _process_pdf(self, pdf_data):
        """
        Traite un PDF avec OCR
        """
        try:
            import PyPDF2
            import io
            from PIL import Image
            import pdf2image
            
            # Extraction du texte PDF natif
            pdf_file = io.BytesIO(pdf_data)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            
            # Si pas de texte natif, utiliser OCR sur les images
            if not text.strip():
                images = pdf2image.convert_from_bytes(pdf_data)
                text = ""
                for image in images:
                    text += self._ocr_image(image)
            
            # Extraction de données structurées selon le type
            data = self._extract_structured_data(text)
            
            return {
                'text': text,
                'data': data,
                'confidence': 0.85
            }
            
        except ImportError as e:
            raise UserError(_("Bibliothèques manquantes: %s\n\nContactez votre administrateur.") % str(e))
        except Exception as e:
            raise UserError(_("Erreur lors du traitement PDF: %s") % str(e))
    
    def _process_image(self, image_data):
        """
        Traite une image avec OCR
        """
        try:
            from PIL import Image
            import io
            
            image = Image.open(io.BytesIO(image_data))
            text = self._ocr_image(image)
            
            # Extraction de données structurées selon le type
            data = self._extract_structured_data(text)
            
            return {
                'text': text,
                'data': data,
                'confidence': 0.90
            }
            
        except Exception as e:
            raise UserError(_("Erreur lors du traitement de l'image: %s") % str(e))
    
    def _ocr_image(self, image):
        """
        Applique l'OCR sur une image PIL
        """
        try:
            import pytesseract
            
            # Configuration Tesseract
            config = f'--oem 3 --psm 6 -l {self.language}'
            
            # OCR
            text = pytesseract.image_to_string(image, config=config)
            
            return text
            
        except ImportError:
            raise UserError(_("Tesseract n'est pas installé.\n\nContactez votre administrateur."))
        except Exception as e:
            raise UserError(_("Erreur OCR: %s") % str(e))
    
    def _extract_structured_data(self, text):
        """
        Extrait des données structurées selon le type de document
        """
        import re
        
        data = {}
        
        if self.document_type == 'invoice':
            # Extraction facture
            
            # Numéro de facture
            invoice_pattern = r'(?:facture|invoice|n°|#)\s*:?\s*([A-Z0-9\-/]+)'
            match = re.search(invoice_pattern, text, re.IGNORECASE)
            if match:
                data['invoice_number'] = match.group(1)
            
            # Date
            date_pattern = r'(\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4})'
            match = re.search(date_pattern, text)
            if match:
                data['date'] = match.group(1)
            
            # Montant total
            amount_pattern = r'(?:total|montant)\s*:?\s*(\d+[,.]?\d*)\s*€'
            match = re.search(amount_pattern, text, re.IGNORECASE)
            if match:
                amount_str = match.group(1).replace(',', '.')
                data['amount'] = float(amount_str)
            
            # TVA
            vat_pattern = r'(?:tva|vat)\s*:?\s*(\d+[,.]?\d*)\s*[%€]'
            match = re.search(vat_pattern, text, re.IGNORECASE)
            if match:
                data['vat'] = match.group(1).replace(',', '.')
        
        elif self.document_type == 'expense':
            # Extraction note de frais
            
            # Montant
            amount_pattern = r'(\d+[,.]?\d*)\s*€'
            match = re.search(amount_pattern, text)
            if match:
                amount_str = match.group(1).replace(',', '.')
                data['amount'] = float(amount_str)
            
            # Date
            date_pattern = r'(\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4})'
            match = re.search(date_pattern, text)
            if match:
                data['date'] = match.group(1)
        
        return data
    
    def _create_record_from_data(self, data):
        """
        Crée un enregistrement depuis les données extraites
        """
        if self.document_type == 'invoice' and data:
            # TODO: Créer une facture avec les données extraites
            _logger.info(f"Création facture depuis OCR: {data}")
        
        elif self.document_type == 'expense' and data:
            # TODO: Créer une note de frais avec les données extraites
            _logger.info(f"Création note de frais depuis OCR: {data}")
    
    def action_create_manual(self):
        """
        Permet de créer manuellement l'enregistrement avec les données extraites
        """
        self.ensure_one()
        
        if not self.extracted_data:
            raise UserError(_("Aucune donnée extraite."))
        
        # Redirection vers le formulaire approprié selon le type
        if self.document_type == 'invoice':
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'eazynova.facture',
                'view_mode': 'form',
                'context': {
                    'default_ocr_data': self.extracted_data
                }
            }
        
        return {'type': 'ir.actions.act_window_close'}