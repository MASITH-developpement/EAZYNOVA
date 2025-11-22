# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
import logging

_logger = logging.getLogger(__name__)


class PlanningAssignment(models.Model):
    _name = 'eazynova.planning.assignment'
    _description = 'Assignation de ressource EAZYNOVA'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_start desc, id desc'

    name = fields.Char(string="Nom", compute='_compute_name', store=True)
    reference = fields.Char(
        string="Référence",
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('New')
    )

    # Tâche et ressource
    task_id = fields.Many2one(
        'eazynova.planning.task',
        string="Tâche",
        required=True,
        ondelete='cascade',
        tracking=True
    )
    resource_id = fields.Many2one(
        'eazynova.planning.resource',
        string="Ressource",
        required=True,
        ondelete='cascade',
        tracking=True
    )

    # Dates (héritées de la tâche par défaut)
    date_start = fields.Datetime(string="Date de début", required=True, tracking=True)
    date_end = fields.Datetime(string="Date de fin", required=True, tracking=True)
    duration = fields.Float(
        string="Durée (heures)",
        compute='_compute_duration',
        store=True
    )

    # Allocation
    allocation_percentage = fields.Float(
        string="Allocation (%)",
        default=100.0,
        help="Pourcentage d'allocation de la ressource (0-100)"
    )

    # État
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('confirmed', 'Confirmé'),
        ('in_progress', 'En cours'),
        ('done', 'Terminé'),
        ('cancelled', 'Annulé'),
    ], string="État", default='draft', required=True, tracking=True)

    # Informations de la tâche (fields related pour faciliter les recherches)
    task_name = fields.Char(related='task_id.name', string="Nom de la tâche", store=True)
    task_priority = fields.Selection(related='task_id.priority', store=True)
    task_state = fields.Selection(related='task_id.state', store=True)

    # Informations de la ressource
    resource_name = fields.Char(related='resource_id.name', string="Nom de la ressource", store=True)
    resource_type = fields.Selection(related='resource_id.resource_type', store=True)

    # Temps et coûts
    planned_hours = fields.Float(string="Heures planifiées")
    actual_hours = fields.Float(string="Heures réelles")
    cost = fields.Float(string="Coût", compute='_compute_cost', store=True)

    # Responsable
    user_id = fields.Many2one(
        'res.users',
        string="Responsable",
        default=lambda self: self.env.user,
        tracking=True
    )

    # Notes
    notes = fields.Text(string="Notes")

    # Conflit
    has_conflict = fields.Boolean(
        string="Conflit détecté",
        compute='_compute_has_conflict',
        store=False
    )
    conflict_details = fields.Text(
        string="Détails du conflit",
        compute='_compute_has_conflict',
        store=False
    )

    # Société
    company_id = fields.Many2one(
        'res.company',
        string="Société",
        default=lambda self: self.env.company
    )

    # Couleur
    color = fields.Integer(string="Couleur", default=0)

    @api.model
    def create(self, vals):
        """Génère la référence à la création"""
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('eazynova.planning.assignment') or _('New')

        # Si les dates ne sont pas fournies, prendre celles de la tâche
        if 'task_id' in vals and not ('date_start' in vals and 'date_end' in vals):
            task = self.env['eazynova.planning.task'].browse(vals['task_id'])
            if task:
                vals.setdefault('date_start', task.date_start)
                vals.setdefault('date_end', task.date_end)

        return super(PlanningAssignment, self).create(vals)

    @api.depends('task_id', 'resource_id')
    def _compute_name(self):
        """Génère le nom de l'assignation"""
        for assignment in self:
            if assignment.task_id and assignment.resource_id:
                assignment.name = f"{assignment.task_id.name} - {assignment.resource_id.name}"
            else:
                assignment.name = _("Nouvelle assignation")

    @api.depends('date_start', 'date_end')
    def _compute_duration(self):
        """Calcule la durée de l'assignation"""
        for assignment in self:
            if assignment.date_start and assignment.date_end:
                delta = assignment.date_end - assignment.date_start
                assignment.duration = delta.total_seconds() / 3600.0
            else:
                assignment.duration = 0.0

    @api.depends('duration', 'resource_id.cost_per_hour', 'allocation_percentage')
    def _compute_cost(self):
        """Calcule le coût de l'assignation"""
        for assignment in self:
            if assignment.resource_id and assignment.resource_id.cost_per_hour:
                hours = assignment.duration * (assignment.allocation_percentage / 100.0)
                assignment.cost = hours * assignment.resource_id.cost_per_hour
            else:
                assignment.cost = 0.0

    @api.depends('resource_id', 'date_start', 'date_end', 'state')
    def _compute_has_conflict(self):
        """Détecte les conflits d'assignation"""
        for assignment in self:
            if not assignment.resource_id or not assignment.date_start or not assignment.date_end:
                assignment.has_conflict = False
                assignment.conflict_details = ""
                continue

            # Rechercher les assignations qui se chevauchent
            overlapping = self.search([
                ('resource_id', '=', assignment.resource_id.id),
                ('id', '!=', assignment.id),
                ('state', 'not in', ('cancelled', 'done')),
                '|',
                '&', ('date_start', '<=', assignment.date_start), ('date_end', '>=', assignment.date_start),
                '&', ('date_start', '<=', assignment.date_end), ('date_end', '>=', assignment.date_end),
            ])

            # Rechercher les absences qui se chevauchent
            absences = self.env['eazynova.planning.absence'].search([
                ('resource_id', '=', assignment.resource_id.id),
                ('state', '=', 'approved'),
                '|',
                '&', ('date_start', '<=', assignment.date_start), ('date_end', '>=', assignment.date_start),
                '&', ('date_start', '<=', assignment.date_end), ('date_end', '>=', assignment.date_end),
            ])

            conflicts = []
            if overlapping:
                conflicts.append(f"Chevauche {len(overlapping)} autre(s) assignation(s)")
            if absences:
                conflicts.append(f"La ressource est absente ({', '.join(absences.mapped('name'))})")

            assignment.has_conflict = bool(conflicts)
            assignment.conflict_details = "\n".join(conflicts) if conflicts else ""

    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        """Vérifie la cohérence des dates"""
        for assignment in self:
            if assignment.date_start and assignment.date_end:
                if assignment.date_end <= assignment.date_start:
                    raise ValidationError(_("La date de fin doit être postérieure à la date de début."))

    @api.constrains('allocation_percentage')
    def _check_allocation(self):
        """Vérifie que l'allocation est valide"""
        for assignment in self:
            if assignment.allocation_percentage < 0 or assignment.allocation_percentage > 100:
                raise ValidationError(_("L'allocation doit être entre 0 et 100%."))

    def action_confirm(self):
        """Confirme l'assignation"""
        # Vérifier les conflits
        for assignment in self:
            if assignment.has_conflict:
                raise UserError(_(
                    "Impossible de confirmer l'assignation : conflit détecté.\n\n%s"
                ) % assignment.conflict_details)

        self.write({'state': 'confirmed'})

    def action_start(self):
        """Démarre l'assignation"""
        self.write({'state': 'in_progress'})

    def action_done(self):
        """Termine l'assignation"""
        self.write({'state': 'done'})

    def action_cancel(self):
        """Annule l'assignation"""
        self.write({'state': 'cancelled'})

    def action_reset_draft(self):
        """Remet en brouillon"""
        self.write({'state': 'draft'})

    def action_view_task(self):
        """Ouvre la tâche liée"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Tâche'),
            'res_model': 'eazynova.planning.task',
            'res_id': self.task_id.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_view_resource(self):
        """Ouvre la ressource liée"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Ressource'),
            'res_model': 'eazynova.planning.resource',
            'res_id': self.resource_id.id,
            'view_mode': 'form',
            'target': 'current',
        }
