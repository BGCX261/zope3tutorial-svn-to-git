GENERAL = {
    'namespace': 'castingzone',
    'sql_dialect': 'postgresql',
    'target_folder': 'tables',
    #'form_library': 'formlib',  # formlib or z3c
    'form_library': 'z3c',  # formlib or z3c
    'z3c_layer': 'boston_pagelet_skin.IPageletLayer',
}

TABLES=[
	{
		'name': 'basic_types_test',
		# Options should be : traversal-standard, traversal-group, standard, group, grid
		'stereotype': 'traversal-standard',
		'primary_key': ['id'], 
		'primary_key_has_sequence': True,
		'primary_key_sequence_name': 'basic_types_test_id_seq',
		'columns':  [
			{
				'colname': 'id',
				'dbtype': 'integer',
				'dbextra': "not null default nextval('basic_types_test_id_seq'::regclass)",
				'schema_type': 'schema.Int',
				'schema_fields': {
					'title': 'id',
					'description': 'id',
					'readonly': True,
				},
			},
			{
				'colname': 'name',
				'dbtype': 'character varying(20)',
                'mapping_type': 'MappingList',
				'schema_type': 'schema.List',
				'schema_fields': {
					'title': 'name',
					'description': 'name',
					'max_length': 20,
					'required': False,
				},
                'value_type': 'schema.Choice',
                'value_type_fields': {
					'title': 'name_part',
                    'values': ['a', 'b', 'c'],
                }
			},
			{
				'colname': 'salary',
				'dbtype': 'double precision',
				'schema_type': 'schema.Float',
				'schema_fields': {
					'title': 'salary',
					'description': 'salary',
					'required': False,
				},
			},
			{
				'colname': 'startdate',
				'dbtype': 'date',
				'schema_type': 'schema.Date',
				'schema_fields': {
					'title': 'startdate',
					'description': 'startdate',
					'required': False,
				},
			},
			{
				'colname': 'lastloging',
				'dbtype': 'timestamp without time zone',
				'schema_type': 'schema.Datetime',
				'schema_fields': {
					'title': 'lastloging',
					'description': 'lastloging',
					'required': False,
				},
			},
			{
				'colname': 'initial',
				'dbtype': 'character(1)',
				'schema_type': 'schema.TextLine',
				'schema_fields': {
					'title': 'initial',
					'description': 'initial',
					'max_length': 1,
					'required': False,
				},
			},
			{
				'colname': 'initials',
				'dbtype': 'character(3)',
				'schema_type': 'schema.TextLine',
				'schema_fields': {
					'title': 'initials',
					'description': 'initials',
					'max_length': 3,
					'required': False,
				},
			},
			{
				'colname': 'biography',
				'dbtype': 'text',
				'schema_type': 'schema.Text',
				'schema_fields': {
					'title': 'biography',
					'description': 'biography',
					'required': False,
				},
			},
			{
				'colname': 'lunchtime',
				'dbtype': 'time without time zone',
				'schema_type': 'schema.TextLine',
				'schema_fields': {
					'title': 'lunchtime',
					'description': 'lunchtime',
					'required': False,
				},
			},
			{
				'colname': 'likeswork',
				'dbtype': 'boolean',
                'mapping_type': 'MappingBool',
				'schema_type': 'schema.Bool',
				'schema_fields': {
					'title': 'likeswork',
					'description': 'likeswork',
					'required': False,
				},
			},
		],
	},
]
