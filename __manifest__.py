# -*- coding: utf-8 -*-
{
  'name':'Formulario personalizado - Website',
  'summary': """
        EvoluZion, S.A
    """,
  'description': '''
          Modulo base para crear formularios web en Odoo.
	  ''',
  'version':'1.0',
  'author':'EvoluZion',
  'website': "",
  'application': False,
  'data': [
    'views/patient_responsive_template.xml',
    'views/search_appointment.xml',
    'views/source_files.xml',
    'views/patient_authorization.xml',
    # 'security/ir.model.access.csv',
  ],


  'category': 'website',
  'depends': ['base','website'],
}
