# -*- coding: utf-8 -*-

from odoo import fields, models


class websiteMenuInherit(models.Model):

    _inherit = "website.menu"

    active = fields.Boolean(string='Activo', default=True)