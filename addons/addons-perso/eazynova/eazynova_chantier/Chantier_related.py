# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class EazynovaChantierPhase(models.Model):
    """
    Phase d'un chantier (ex: Gros œuvre, Second œuvre, Finitions)
    """
    _name = 'eazynova.chantier.phase'
    _description = 'Phase de Chantier'
    _order = 'sequence, name'
    
    name = fields.Char(
        string="Nom de la phase",
        required=True,
        help="Nom de la phase (ex: Gros œuvre, Électricité, etc.)"
    )
    
    sequence = fields.Integer(
        string="Séquence",
        default=10,
        help="Ordre d'affichage des phases"
    )
    
    chantier_id = fields.Many2one(
        'eazynova.chantier',
        string="Chantier",
        required=True,
        ondelete='cascade',
        help="Chantier associé"
    )
    
    date_start = fields.Date(
        string="Date de début",
        required=True
    )
    
    date_end = fields.Date(
        string="Date de fin",
        required=True
    )
    
    progress = fields.Float(
        string="Avancement (%)",
        default=0.0,
        help="Pourcentage d'avancement de la phase"
    )
    
    state = fields.Selection([
        ('pending', 'En attente'),
        ('in_progress', 'En cours'),
        ('done', 'Terminé'),
    ], string="État",
       default='pending',
       required=True
    )
    
    description = fields.Text(
        string="Description",
        help="Description détaillée de la phase"
    )
    
    _sql_constraints = [
        ('check_dates', 'CHECK(date_end >= date_start)', 'La date de fin doit être postérieure à la date de début !'),
        ('check_progress', 'CHECK(progress >= 0 AND progress <= 100)', 'L\'avancement doit être entre 0 et 100 !'),
    ]


class EazynovaChantierTache(models.Model):
    """
    Tâche d'un chantier
    """
    _name = 'eazynova.chantier.tache'
    _description = 'Tâche de Chantier'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'priority desc, date_deadline, name'
    
    name = fields.Char(
        string="Tâche",
        required=True,
        tracking=True
    )
    
    chantier_id = fields.Many2one(
        'eazynova.chantier',
        string="Chantier",
        required=True,
        ondelete='cascade',
        tracking=True
    )
    
    phase_id = fields.Many2one(
        'eazynova.chantier.phase',
        string="Phase",
        domain="[('chantier_id', '=', chantier_id)]",
        tracking=True
    )
    
    user_id = fields.Many2one(
        'res.users',
        string="Responsable",
        default=lambda self: self.env.user,
        tracking=True
    )
    
    date_deadline = fields.Date(
        string="Date limite",
        tracking=True
    )
    
    priority = fields.Selection([
        ('0', 'Normale'),
        ('1', 'Importante'),
        ('2', 'Urgente'),
    ], string="Priorité",
       default='0',
       tracking=True
    )
    
    state = fields.Selection([
        ('todo', 'À faire'),
        ('in_progress', 'En cours'),
        ('done', 'Terminé'),
        ('cancelled', 'Annulé'),
    ], string="État",
       default='todo',
       required=True,
       tracking=True
    )
    
    description = fields.Html(
        string="Description"
    )
    
    hours_planned = fields.Float(
        string="Heures prévues",
        help="Nombre d'heures prévues pour cette tâche"
    )
    
    hours_spent = fields.Float(
        string="Heures réalisées",
        help="Nombre d'heures réellement passées"
    )


class EazynovaChantierEquipe(models.Model):
    """
    Équipe affectée à un chantier
    """
    _name = 'eazynova.chantier.equipe'
    _description = 'Équipe de Chantier'
    _order = 'name'
    
    name = fields.Char(
        string="Nom de l'équipe",
        required=True,
        help="Nom de l'équipe (ex: Équipe Maçonnerie)"
    )
    
    chantier_id = fields.Many2one(
        'eazynova.chantier',
        string="Chantier",
        required=True,
        ondelete='cascade'
    )
    
    chef_equipe_id = fields.Many2one(
        'res.users',
        string="Chef d'équipe",
        required=True,
        help="Responsable de l'équipe"
    )
    
    member_ids = fields.Many2many(
        'res.users',
        string="Membres",
        help="Membres de l'équipe"
    )
    
    specialite = fields.Selection([
        ('maconnerie', 'Maçonnerie'),
        ('electricite', 'Électricité'),
        ('plomberie', 'Plomberie'),
        ('peinture', 'Peinture'),
        ('menuiserie', 'Menuiserie'),
        ('charpente', 'Charpente'),
        ('couverture', 'Couverture'),
        ('autres', 'Autres'),
    ], string="Spécialité",
       help="Spécialité de l'équipe"
    )
    
    active = fields.Boolean(
        string="Actif",
        default=True
    )
    
    note = fields.Text(
        string="Notes"
    )
    