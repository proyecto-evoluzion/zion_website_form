# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _


class websiteMenuInherit(models.Model):

    _inherit = "website.menu"

    active = fields.Boolean(string='Activo', default=True)