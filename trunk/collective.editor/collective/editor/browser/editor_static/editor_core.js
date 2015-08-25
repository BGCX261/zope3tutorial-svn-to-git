/* 
 * Core functions for the editor
 */

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

  var url_pathname = window.location.pathname;
  var process_file = function(title, path) {
    $.ajax({
      url: url_pathname,
      type: 'GET',
      dataType: 'json',
      data: {'requestType': 'ajax', 'requestId': 'getFile', 'filename': path},
      success: function(xml){
        var tabs = $("ul.css-tabs");
        var fn_parts = xml.filename.split('/');

        var li = $('<li><a href="#" title="' + xml.filename +'">' + fn_parts[fn_parts.length-1] + '<span class="closer">x</span></a></li>');
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


        // Setup bespin and load the data
        // TODO: I would like to set the theme to white here. I don't know how to do it
        // warning - do not use stealfocus here - messes up window positioning
        bespin.useBespin(el[0]).then(function(env) {

            var editor = env.editor;
            editor.value = xml.payload;
            editor.syntax = xml.syntax;
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
      }
      });
  };
  var process_project = function(title, path) {
    alert('project' + path);
  };
  var process_folder = function(title, path) {
    alert('folder' + path);
  };

  /* Load the file system file info into a jstree */
  $("#tree").jstree({
        "json_data" : {

            "ajax" : {
                "url": url_pathname,
                "data" : function (n) {
                    return {
                        'id' : n.attr ? n.attr("id") : 0,
                        'requestType': 'ajax',
                        'requestId': 'getNavigation'
                     };
                }
            },
        },
        "plugins" : [ "themes", "json_data" ]
    });
    /* PROBLEM HERE _ HOW TO HANDLE CLICK ON A FILE */
    $("#tree a").live("click", function(e) {
        var href = $(this).parent()[0].id;
        var linktype = href.split(':')[0];
        var title = $(this).text();
        if (linktype == 'file') {
            process_file(title, href.substr(5));
        }
        else if (linktype == 'folder') {
            process_folder(title, href.substr(7));
        }
        else if (linktype == 'project') {
            process_project(title, href.substr(8));
        }
        else {
            alert ("You activated " + title + ", key=" + href);
        }
        return false;
    });

    // setup ul.tabs to work as tabs for each div directly under div.panes
    $("ul.tabs").tabs("div.panes > div");
});

