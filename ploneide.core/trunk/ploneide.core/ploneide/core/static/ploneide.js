/* 
 * Core functions for the editor
 * http://www.learningjquery.com/2007/10/a-plugin-development-pattern
 */

(function($) {  // create closure

    $.ploneide = {};
    $.ploneide.controllers = {};
    $.ploneide.views = {};
    $.ploneide._controllers = [];

    var href = document.getElementById("ploneide_base").href;
    $.ploneide.base_url = href.substring(href.length - 1) !== "/" ? href + "/" : href;

    $.ploneide.handle = function(type_name, method_name, data, success) {
       var params = {'type_name': type_name, 'method_name': method_name};
       $.extend(params, data);
       return $.ajax({
          url: $.ploneide.base_url + 'handler',
          type: 'GET',
          dataType: 'json',
          data: params,
          success: function(xml){
            success(xml);
          }
      });
    };

    $.ploneide.register_controller = function(controller_name, controller) {
        $.ploneide.controllers[controller_name] = controller;
    };

    $.ploneide.register_view = function(type_name, view, priority) {
        var reg = $.ploneide.views[type_name];
        if (!reg) {
            reg = []
        }
        reg[reg.length] = [priority, view];       // todo sort
        $.ploneide.views[type_name] = reg;
    };

    // This is the controller base class
    $.ploneide.Controller = function() {

        this.init_super = function(type_name, unique_id, initial_data, model_data) {
            this.type_name = type_name;
            this.unique_id = unique_id;
            this.inital_data = initial_data;
            this.model_data = model_data;
            this._editors = [];

        };
        this.draw_editors = function() {
                var i;
                var model = this.model_data.model;
                var views = $.ploneide.views[model];
                if (views == 'undefined') {
                    alert('No editors configured for model type ' + this.model_data.model);
                    return;
                }
                for (i = 0; i < views.length; i++) {
                    var editor = new views[i][1](this);
                    editor.draw();
                    this._editors[this._editors.length] = editor;
                }
            };
        this.destroy_editors = function() {
            };
    };

    // This is the baseclass for editors
    $.ploneide.Editor = function() {
        this.init_super = function(controller) {
            this.controller = controller;
        };
    };


    $.ploneide.edit_file = function(type_name, unique_id, initial_data) {
      return $.ploneide.handle(type_name, 'getFile', {'filename': unique_id}, 
        success = function(xml) {

        // Got an object back - create a controller to handle it
        var controller_class = $.ploneide.controllers[type_name];
        var controller = new controller_class(type_name, unique_id, initial_data, xml);
        controller.draw_editors();
        $.ploneide._controllers[unique_id] = controller;
        return;

      });
    };


})(jQuery);

$(document).ready(function() {

    /* Initialise the Page Layout */
    $("#simple-editor-layout").splitter({
        splitVertical: true,
        outline: true,
        sizeLeft: true,
        resizeToWidth: true
    });
    $("#simple-editor-layout #main").splitter({
        splitHorizontal: true,
        outline: true,
        sizeTop: true  
        });

    $('#simple-editor-layout #main #top').bind('resize', function(e, size) {
        $('div.bespin').each(function(i, el) {var env = el.bespin; env.dimensionsChanged();});
        return true;
    });

    $("#navigation-pane").tabs("#navigation-pane div.pane", {tabs: 'h2', effect: 'slide', initialIndex: null});

    // setup ul.tabs to work as tabs for each div directly under div.panes
    $("ul.tabs").tabs("div.panes > div");
});

