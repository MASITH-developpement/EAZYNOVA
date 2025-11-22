# setup_chantier.ps1
# Script de creation automatique du module EAZYNOVA Chantier

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "EAZYNOVA Chantier - Installation automatique" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Chemin du module
$modulePath = "eazynova_chantier"

# Creer la structure de dossiers
Write-Host "Creation de la structure..." -ForegroundColor Yellow
New-Item -Path $modulePath -ItemType Directory -Force | Out-Null
New-Item -Path "$modulePath/models" -ItemType Directory -Force | Out-Null
New-Item -Path "$modulePath/views" -ItemType Directory -Force | Out-Null
New-Item -Path "$modulePath/security" -ItemType Directory -Force | Out-Null
New-Item -Path "$modulePath/data" -ItemType Directory -Force | Out-Null
New-Item -Path "$modulePath/static/description" -ItemType Directory -Force | Out-Null

# __init__.py (racine)
Write-Host "Creation de __init__.py..." -ForegroundColor Yellow
@"
# -*- coding: utf-8 -*-

from . import models
"@ | Out-File -FilePath "$modulePath/__init__.py" -Encoding UTF8

# models/__init__.py
Write-Host "Creation de models/__init__.py..." -ForegroundColor Yellow
@"
# -*- coding: utf-8 -*-

from . import chantier
from . import chantier_task
from . import chantier_document
"@ | Out-File -FilePath "$modulePath/models/__init__.py" -Encoding UTF8

# models/chantier_task.py
Write-Host "Creation de models/chantier_task.py..." -ForegroundColor Yellow
@"
# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class EazynovaChantierTask(models.Model):
    """Taches d'un chantier"""
    _name = 'eazynova.chantier.task'
    _description = 'Tache Chantier'
    _order = 'sequence, name'
    
    name = fields.Char(string="Tache", required=True)
    chantier_id = fields.Many2one('eazynova.chantier', string="Chantier", required=True, ondelete='cascade')
    sequence = fields.Integer(string="Sequence", default=10)
    state = fields.Selection([
        ('todo', 'A faire'),
        ('in_progress', 'En cours'),
        ('done', 'Termine'),
    ], string="Etat", default='todo', required=True)
    progress = fields.Float(string="Progression (%)", default=0.0)
    cost = fields.Monetary(string="Cout", currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', related='chantier_id.currency_id', store=True)
"@ | Out-File -FilePath "$modulePath/models/chantier_task.py" -Encoding UTF8

# models/chantier_document.py
Write-Host "Creation de models/chantier_document.py..." -ForegroundColor Yellow
@"
# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class EazynovaChantierDocument(models.Model):
    """Documents d'un chantier"""
    _name = 'eazynova.chantier.document'
    _description = 'Document Chantier'
    
    name = fields.Char(string="Nom", required=True)
    chantier_id = fields.Many2one('eazynova.chantier', string="Chantier", required=True, ondelete='cascade')
    document = fields.Binary(string="Fichier", attachment=True)
    document_filename = fields.Char(string="Nom du fichier")
    document_type = fields.Selection([
        ('plan', 'Plan'),
        ('photo', 'Photo'),
        ('facture', 'Facture'),
        ('contrat', 'Contrat'),
        ('autre', 'Autre'),
    ], string="Type", default='autre')
"@ | Out-File -FilePath "$modulePath/models/chantier_document.py" -Encoding UTF8

# data/chantier_sequence.xml
Write-Host "Creation de data/chantier_sequence.xml..." -ForegroundColor Yellow
@"
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="1">
        <record id="sequence_eazynova_chantier" model="ir.sequence">
            <field name="name">Chantier EAZYNOVA</field>
            <field name="code">eazynova.chantier</field>
            <field name="prefix">CHANT/%(year)s/</field>
            <field name="padding">5</field>
            <field name="company_id" eval="False"/>
        </record>
    </data>
</odoo>
"@ | Out-File -FilePath "$modulePath/data/chantier_sequence.xml" -Encoding UTF8

# security/ir.model.access.csv
Write-Host "Creation de security/ir.model.access.csv..." -ForegroundColor Yellow
@"
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_chantier_user,eazynova.chantier.user,model_eazynova_chantier,eazynova.group_eazynova_user,1,0,0,0
access_chantier_manager,eazynova.chantier.manager,model_eazynova_chantier,eazynova.group_eazynova_manager,1,1,1,0
access_chantier_admin,eazynova.chantier.admin,model_eazynova_chantier,eazynova.group_eazynova_admin,1,1,1,1
access_chantier_task_user,eazynova.chantier.task.user,model_eazynova_chantier_task,eazynova.group_eazynova_user,1,1,1,0
access_chantier_task_manager,eazynova.chantier.task.manager,model_eazynova_chantier_task,eazynova.group_eazynova_manager,1,1,1,1
access_chantier_document_user,eazynova.chantier.document.user,model_eazynova_chantier_document,eazynova.group_eazynova_user,1,1,1,1
access_chantier_tag,eazynova.chantier.tag,model_eazynova_chantier_tag,eazynova.group_eazynova_user,1,0,0,0
"@ | Out-File -FilePath "$modulePath/security/ir.model.access.csv" -Encoding UTF8

# views/chantier_menu.xml
Write-Host "Creation de views/chantier_menu.xml..." -ForegroundColor Yellow
@"
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>
        <menuitem id="menu_chantier"
                  name="Chantiers"
                  parent="eazynova.menu_eazynova_root"
                  sequence="10"/>
    </data>
</odoo>
"@ | Out-File -FilePath "$modulePath/views/chantier_menu.xml" -Encoding UTF8

# __manifest__.py
Write-Host "Creation de __manifest__.py..." -ForegroundColor Yellow
@"
# -*- coding: utf-8 -*-
{
    'name': 'EAZYNOVA Chantier',
    'version': '19.0.1.0.0',
    'category': 'Project',
    'summary': 'Gestion de chantiers avec IA et gestion documentaire',
    'author': 'EAZYNOVA',
    'website': 'https://eazynova-production.up.railway.app/',
    'license': 'LGPL-3',
    'depends': ['eazynova'],
    'data': [
        'security/ir.model.access.csv',
        'data/chantier_sequence.xml',
        'views/chantier_menu.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
"@ | Out-File -FilePath "$modulePath/__manifest__.py" -Encoding UTF8

# Copier chantier.py depuis EZYNOVA_chantier si existe
if (Test-Path "EZYNOVA_chantier/models/chantier.py") {
    Write-Host "Copie de chantier.py existant..." -ForegroundColor Yellow
    Copy-Item "EZYNOVA_chantier/models/chantier.py" "$modulePath/models/chantier.py"
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host "Module cree avec succes !" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Structure creee:" -ForegroundColor Cyan
Get-ChildItem -Path $modulePath -Recurse | Select-Object FullName

Write-Host ""
Write-Host "Prochaines etapes:" -ForegroundColor Yellow
Write-Host "1. Verifiez les fichiers crees" -ForegroundColor White
Write-Host "2. Supprimez ancien dossier: Remove-Item EZYNOVA_chantier -Recurse -Force" -ForegroundColor White
Write-Host "3. Git add: git add eazynova_chantier/" -ForegroundColor White
Write-Host "4. Git commit: git commit -m 'Add: Module EAZYNOVA Chantier complet'" -ForegroundColor White
Write-Host "5. Git push: git push" -ForegroundColor White
Write-Host ""