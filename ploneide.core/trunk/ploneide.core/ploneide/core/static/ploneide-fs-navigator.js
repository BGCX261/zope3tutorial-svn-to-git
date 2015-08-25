
"use strict";

(function($) {
  var ploneide_base = document.getElementById("ploneide_base").href;
  ploneide_base = ploneide_base.substring(ploneide_base.length - 1) !== "/" ? ploneide_base + "/" : ploneide_base;

  var process_click = function(title, href) {
      // href could have trailing data e.g. line number
      var type_name = href.split(':')[0];
      var unique_id = href.split(':')[1];
      var path = href.substr(href.length + 1 + unique_id.length + 1);
      /* Ask the global ploneide object to open this object */
      $.ploneide.edit_file(type_name, unique_id, null);
  };

  /* register a controller for mapping navigator-filesystem objects between view and model */
  var ControllerFS = function(type_name, unique_id, initial_data, model_data) {
        this.init_super(type_name, unique_id, initial_data, model_data);
  };
  ControllerFS.prototype = new $.ploneide.Controller();
  $.ploneide.register_controller('navigator-filesystem', ControllerFS, 100);


  /* Initialise the navigator */
  $(document).ready(function(){

    $("#tree").jstree({
          "json_data" : {

              "ajax" : {
                  "url": ploneide_base + '@@handler',
                  "data" : function (n) {
                      return {
                          'id' : n.attr ? n.attr("id") : 0,
                          'type_name': 'navigator-filesystem',
                          'method_name': 'getNavigation'
                       };
                  }
              },
          },
          "plugins" : [ "themes", "json_data" ]
      });

      $("#tree a").live("click", function(e) {
          var href = $(this).parent()[0].id;
          var title = $(this).text();
          process_click(title, href);
          return false;
      });

  });
})(jQuery);
