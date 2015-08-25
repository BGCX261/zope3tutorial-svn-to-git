
/*
 * This is an editor using the bespin editor
 */
"use strict";

(function($) {

    var EditorBespin = function(controller) {
        this.init_super(controller);

        this.draw = function() {
            var tabs = $("ul.css-tabs");
            var fn_parts = this.controller.model_data.filename.split('/');

            var li = $('<li><a href="#" title="' + this.controller.model_data.filename +'">' + fn_parts[fn_parts.length-1] + '<span class="closer">x</span></a></li>');
            tabs.append(li);

            /* TODO: need to style tooltip. position is all wrong */
            li.find('a').tooltip({'position': "bottom center", 'relative': true, 'z-index': 100});
            var panes = $("div.panes");
            var pane = $('<div class="pane"><div class="toolbar">TOOLBAR</div></div>');
            var el = $('<div class="editarea"/>');
            pane.append(el);
            panes.append(pane);

            li.find('.closer').bind('click', function(e) {
                /* remove tab and pane */
                /* TODO: data changed and cleanups */
                li.remove();
                pane.remove();

                var api = tabs.data("tabs");
                tabs.tabs("div.panes > div", {
                    'onClick': function(e, ti){
                        try {
                            $("div.panes  .bespin")[ti].bespin.dimensionsChanged();
                        } catch (e) {
                            // no event on first pass 
                        }
                        return true;
                    }});
                return false;
            });

            var controller = this.controller;


            // Setup bespin and load the data
            // TODO: I would like to set the theme to white here. I don't know how to do it
            // warning - do not use stealfocus here - messes up window positioning
            bespin.useBespin(el[0]).then(function(env) {

                var editor = env.editor;
                editor.value = controller.model_data.payload;
                editor.syntax = controller.model_data.syntax;
                editor.setLineNumber(1);
                // Only convert to tabs after it is drawn - otherwise bespin screws up.
                tabs.tabs("div.panes > div", {'initialIndex': null, 
                    'onClick': function(e, ti){
                        try {
                            $("div.panes  .bespin")[ti].bespin.dimensionsChanged();
                        } catch (e) {
                            // no event on first pass 
                        }
                        return true;
                        }});

                // Select the current tab - this way of getting the api is not comfortable
                // why not env.api?
                var api = tabs.data("tabs");
                var tab_count = tabs.children().length;
                api.click(tab_count -1);

                // Save env for later use - seems from docs that should already be set
                el[0].bespin = env;
            }, function(error) {alert(error);});
        };
    };
    EditorBespin.prototype = new $.ploneide.Editor();

    /* register the editor for each of the model types (defined in navigator.py) */
    $.ploneide.register_view('js', EditorBespin, 100);
    $.ploneide.register_view('pt', EditorBespin, 100);
    $.ploneide.register_view('py', EditorBespin, 100);
    $.ploneide.register_view('css', EditorBespin, 100);
    $.ploneide.register_view('txt', EditorBespin, 100);
    $.ploneide.register_view('cfg', EditorBespin, 100);
    $.ploneide.register_view('zcml', EditorBespin, 100);

})(jQuery);
