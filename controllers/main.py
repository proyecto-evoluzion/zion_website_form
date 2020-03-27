# -*- coding: utf-8 -*-

# Se importan todas las utilidades requeridas.
from odoo import http, tools, _
from odoo.http import request
from odoo.addons.website.controllers.main import QueryURL


class PatientController(http.Controller):

	@http.route(['/post/data'], auth='public', website=True,methods=['POST', 'GET'], csrf=True, type="http")
	def save(self, **kwargs):
		if kwargs:
			name = kwargs.get('firstname')
			lastname = kwargs.get('lastname')
			middlename = kwargs.get('middlename')
			surname = kwargs.get('surname')
			blood_type = kwargs.get('typeBlood')
			blood_rh = kwargs.get('typeRh')
			user_type = kwargs.get('user_type')
			age = kwargs.get('age')
			sex = kwargs.get('sex')
			res_id = kwargs.get('id')
			insurer_id = kwargs.get('insurer_id')
			phone = kwargs.get('phone')
			email = kwargs.get('email')
			residence_address = kwargs.get('residence_address')

			# Para pasar los datos de genero en el formato correcto
			if sex == 'Masculino':
				sex = 'male'
			else:
				sex = 'female'

			# Para pasar los datos tipo sangre en el formato correcto
			if blood_type == 'A':
				blood_type = 'a'
			elif blood_type == 'B':
				blood_type = 'b'
			elif blood_type == 'AB':
				blood_type = 'ab'
			else:
				blood_type = 'o'

			# Para pasar los datos tipo sangre +- en el formato correcto
			if blood_rh == '+':
				blood_rh = 'positive'
			else:
				blood_rh = 'negative'

			# Para pasar los datos tipo usuario en el formato correcto
			if user_type == 'Contributivo':
				user_type = 'contributory'
			elif user_type == 'Subsidiado':
				user_type = 'subsidized'
			elif user_type == 'Vinculado':
				user_type = 'linked'
			elif user_type == 'Particular':
				user_type = 'particular'
			elif user_type == 'Otro':
				user_type = 'other'
			elif user_type == 'Victima Contributivo':
				user_type = 'victim_contributive'
			elif user_type == 'Victima Subsidiado':
				user_type = 'victim_subsidized'
			else:
				user_type = 'victim_linked'

			post = http.request.env['doctor.patient'].search([('id','=',res_id)])
			data = {
				'lastname': lastname,
				'surname': surname,
				'firstname': name,
				'middlename': middlename,
				'blood_type': blood_type,
				'blood_rh': blood_rh,
				'age': age,
				'sex': sex,
				'user_type': user_type,
				'residence_address': residence_address,
				'phone': phone,
				'email': email,
			}
			if insurer_id:
				data['insurer_id'] = insurer_id.id

			post.write(data)
			return http.local_redirect('/')

	@http.route('/get/data', auth='public', website=True)
	def analytics(self, **kw):
		name = kw.get('name')
		patient_search_name = http.request.env['doctor.patient'].search([('name','=',name)], limit=1)
		patient_search_ref = http.request.env['doctor.patient'].search([('ref','=',name)], limit=1)
		# Aseguradora
		insurer_id = http.request.env['res.partner'].search([('is_assurance','=',True)])		

		if patient_search_name:
			#Validacion para Genero del paciente
			if patient_search_name.sex == 'male':
				sex = 'Masculino'
			else:
				sex = 'Femenino'

			patient_data = {
				'id': patient_search_name.id,
				'firstname': patient_search_name.firstname,
				'middlename': patient_search_name.middlename,
				'lastname': patient_search_name.lastname,
				'surname': patient_search_name.surname,
				'blood_rh': ['+','-'],
				'blood_type': ['A','B','AB','O'],
				'age': patient_search_name.age,
				'residence_address': patient_search_name.residence_address,
				'email': patient_search_name.email,
				'phone': patient_search_name.phone,
				'sex': ['Femenino','Masculino'],
				'insurer_id': insurer_id,
				'user_type': ['Contributivo',
								'Subsidiado',
								'Vinculado',
								'Particular',
								'Otro',
								'Victima Contributivo',
								'Victima Subsidiado',
								'Victima Vinculado'],
			}
		elif patient_search_ref:
			if patient_search_ref.sex == 'male':
				sex = 'Masculino'
			else:
				sex = 'Femenino'

			patient_data = {
				'id': patient_search_ref.id,
				'firstname': patient_search_ref.firstname,
				'middlename': patient_search_ref.middlename,
				'lastname': patient_search_ref.lastname,
				'surname': patient_search_ref.surname,
				'blood_rh': ['+','-'],
				'blood_type': ['A','B','AB','O'],
				'age': patient_search_ref.age,
				'residence_address': patient_search_ref.residence_address,
				'email': patient_search_ref.email,
				'phone': patient_search_ref.phone,				
				'sex': ['Femenino','Masculino'],
				'insurer_id': insurer_id,
				'user_type': ['Contributivo',
								'Subsidiado',
								'Vinculado',
								'Particular',
								'Otro',
								'Victima Contributivo',
								'Victima Subsidiado',
								'Victima Vinculado'],
			}
		else:
			'El paciente no existe'
			return http.local_redirect('/')

		return http.request.render('zion_website_form.atencion_page_template', {
			'data': patient_data})