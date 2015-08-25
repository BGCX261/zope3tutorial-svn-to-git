Boston Pagelet Skin
-------------------

This is a very simple skin for testing the generated code. It provides a pagelet 
version of the boston main template. The configurations are:

    .skin.ISkin             - the skin
    .layer.IPageletLayer    - the layer for registering z3c.pagelet and z3c.form

The resulting skin can be viewed as:

    ++skin++BostonPagelet

Add this directory to your src directory as boston_pagelet_skin.

For your pagelets based content, register them with

    layer="boston_pagelet_skin.IPageletLayer"

In the dsl file, set the GENERAL Section as follows:

    GENERAL = {
        'namespace': 'test',
        'sql_dialect': 'postgresql',
        'target_folder': 'tables',
        'form_library': 'z3c',
        'z3c_layer': 'boston_pagelet_skin.IPageletLayer',
    }


