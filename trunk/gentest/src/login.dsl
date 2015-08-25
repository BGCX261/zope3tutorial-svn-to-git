GENERAL = {
    'namespace': 'gentest',
    'sql_dialect': 'postgresql',
    'target_folder': 'tables',
    'form_library': 'z3c',  
    'z3c_layer': 'boston_pagelet_skin.IPageletLayer',
}

TABLES=[
	{
		'name': 'login',
		# Options should be : traversal-standard, traversal-group, standard, group, grid
		'stereotype': 'traversal-standard',
		'primary_key': ['id'], 
		'primary_key_has_sequence': True,
		'primary_key_sequence_name': 'login_id_seq',
		'columns':  [
			{
				'colname': 'id',
				'dbtype': 'integer',
				'dbextra': "not null default nextval('login_id_seq'::regclass)",
				'list_to_comma_separated': False,
				'schema_type': 'schema.Int',
				'schema_fields': {
					'title': 'id',
					'description': 'id',
					'readonly': True,
				},
			},
			{
				'colname': 'login',
				'dbtype': 'character varying(100)',
				'list_to_comma_separated': False,
				'schema_type': 'schema.TextLine',
				'schema_fields': {
					'title': 'login',
					'description': 'login',
					'max_length': 100,
					'required': False,
				},
			},
			{
				'colname': 'password',
				'dbtype': 'character varying(50)',
				'list_to_comma_separated': False,
				'schema_type': 'schema.TextLine',
				'schema_fields': {
					'title': 'password',
					'description': 'password',
					'max_length': 50,
					'required': False,
				},
			},
			{
				'colname': 'groups',
				'dbtype': 'character varying(200)',
				'list_to_comma_separated': False,
				'schema_type': 'schema.TextLine',
				'schema_fields': {
					'title': 'groups',
					'description': 'groups',
					'max_length': 200,
					'required': False,
				},
			},
			{
				'colname': 'member_id',
				'dbtype': 'integer',
				'list_to_comma_separated': False,
				'schema_type': 'schema.Int',
				'schema_fields': {
					'title': 'member_id',
					'description': 'member_id',
					'required': False,
				},
			},
		],
	},
]
