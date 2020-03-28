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
			link_type = kwargs.get('link_type')
			birth_country_id = kwargs.get('birth_country_id')
			provenance_country_id = kwargs.get('provenance_country_id')
			residence_country_id = kwargs.get('residence_country_id')
			residence_city_id = kwargs.get('residence_city_id')
			residence_department_id = kwargs.get('residence_department_id')
			civil_state = kwargs.get('civil_state')
			occupation = kwargs.get('occupation')
			accompany_name = kwargs.get('accompany_name')
			accompany_relationship = kwargs.get('accompany_relationship')
			accompany_phone = kwargs.get('accompany_phone')
			consultation_reason = kwargs.get('consultation_reason')

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

			# Para pasar los datos estado civil en el formato correcto
			if civil_state == 'Separada/o':
				civil_state = 'separated'
			elif civil_state == 'Soltera/o':
				civil_state = 'single'
			elif civil_state == 'Casada/o':
				civil_state = 'married'
			elif civil_state == 'Unión Libre':
				civil_state = 'free_union'
			else:
				civil_state = 'widow'

			# Para pasar los datos acompanante en el formato correcto
			if accompany_relationship == 'Madre':
				accompany_relationship = 'mother'
			elif accompany_relationship == 'Padre':
				accompany_relationship = 'father'
			elif accompany_relationship == 'Abuelo':
				accompany_relationship = 'grand_father'
			elif accompany_relationship == 'Abuela':
				accompany_relationship = 'grand_mother'
			elif accompany_relationship == 'Tío':
				accompany_relationship = 'uncle'
			elif accompany_relationship == 'Tía':
				accompany_relationship = 'aunt'
			elif accompany_relationship == 'Amigo/a':
				accompany_relationship = 'friend'
			else:
				accompany_relationship = 'other'

			# Para pasar los datos de tipo vinculacion en el formato correcto
			if link_type == 'Contribuyente':
				link_type = 'contributor'
			else:
				link_type = 'beneficiary'

			post = http.request.env['doctor.patient'].sudo().search([('id','=',res_id)])
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
				'residence_department_id': residence_department_id,
				'phone': phone,
				'copy_responsible_info': True,
				'email': email,
				'link_type': link_type,
				'civil_state': civil_state,
				'occupation': occupation,
				'accompany_name': accompany_name,
				'accompany_relationship': accompany_relationship,
				'accompany_phone': accompany_phone,
				'consultation_reason': consultation_reason,
				'birth_country_id': int(birth_country_id),
				'provenance_country_id': int(provenance_country_id),
				'residence_country_id': int(residence_country_id),
				'residence_city_id': int(residence_city_id),
				'residence_department_id': int(residence_department_id),
			}
			if insurer_id:
				data['insurer_id'] = int(insurer_id)

			post.sudo().write(data)
			return http.local_redirect('/')

	@http.route('/get/data', auth='public', website=True,methods=['POST', 'GET'], csrf=True, type="http")
	def analytics(self, **kw):
		name = kw.get('name')
		patient_search_name = http.request.env['doctor.patient'].sudo().search([('name','=',name)], limit=1)
		patient_search_ref = http.request.env['doctor.patient'].sudo().search([('ref','=',name)], limit=1)
		# Aseguradora
		insurer_id = http.request.env['res.partner'].sudo().search([('is_assurance','=',True)])		
		country_id = http.request.env['res.country'].sudo().search([])
		residence_country_id = http.request.env['res.country'].sudo().search([('code','=','CO')])
		residence_department_id = http.request.env['res.country.state'].sudo().search([('country_id','=',http.request.env.ref('base.co').id)])
		residence_city_id = http.request.env['res.country.state.city'].sudo().search([('country_id','=',http.request.env.ref('base.co').id)])

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
				'link_type': ['Contribuyente','Beneficiario'],
				'age': patient_search_name.age,
				'residence_address': patient_search_name.residence_address,
				'accompany_phone': patient_search_name.accompany_phone,
				'email': patient_search_name.email,
				'phone': patient_search_name.phone,
				'accompany_name': patient_search_name.accompany_name,
				'accompany_phone': patient_search_name.accompany_phone,
				'sex': ['Femenino','Masculino'],
				'insurer_id': insurer_id,
				'country_id': country_id,
				'residence_country_id': residence_country_id,
				'residence_department_id': residence_department_id,
				'residence_city_id': residence_city_id,
				'occupation': patient_search_name.occupation,
				'consultation_reason': patient_search_name.consultation_reason,
				'civil_state': ['Separada/o','Soltera/o','Casada/o','Unión Libre','Viuda/o'],
				'accompany_relationship': ['Madre','Padre','Abuelo','Abuela','Tío','Tía','Amigo/a','Otro'],
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
				'link_type': ['Contribuyente','Beneficiario'],
				'age': patient_search_ref.age,
				'residence_address': patient_search_ref.residence_address,
				'email': patient_search_ref.email,
				'phone': patient_search_ref.phone,
				'accompany_name': patient_search_ref.accompany_name,
				'accompany_phone': patient_search_ref.accompany_phone,
				'sex': ['Femenino','Masculino'],
				'insurer_id': insurer_id,
				'country_id': country_id,
				'residence_country_id': residence_country_id,
				'residence_department_id': residence_department_id,
				'residence_city_id': residence_city_id,
				'occupation': patient_search_ref.occupation,
				'consultation_reason': patient_search_ref.consultation_reason,
				'civil_state': ['Separada/o','Soltera/o','Casada/o','Unión Libre','Viuda/o'],
				'accompany_relationship': ['Madre','Padre','Abuelo','Abuela','Tío','Tía','Amigo/a','Otro'],
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
			return http.local_redirect('/page/notfound')

		return http.request.render('zion_website_form.atencion_page_template', {
			'data': patient_data})