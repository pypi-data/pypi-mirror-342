var set_svg_drop = function(element, target,callback=undefined){
  element.on("dragover", function(ev) {
    let event = ev.originalEvent;
    event.stopPropagation();
    event.preventDefault();
    event.dataTransfer.dropEffect = 'copy';

  });
  element.on("drop", function(ev) {
    let event = ev.originalEvent;
    event.stopPropagation();
    event.preventDefault();
  
    var files = event.dataTransfer.files; // FileList object.
  
    // files is a FileList of File objects. List some properties.
    if (files.length > 0) {
        var file = files[0];
        if (file.type === "image/svg+xml") {
            var reader = new FileReader();
  
            reader.onload = function(e) {

                //svg=$(e.target.result).find("svg").html();
                node_1 = $(e.target.result).attr("width","256").attr("height","256");
                node_2= $(e.target.result).attr("width","256").attr("height","256");
                target.empty();
                target.append(node_1);
                target.append(node_2);

                node_2.find("[fill]").each(function(index,el){
                  el = $(el);
                  el.attr("fill","#0000FF");
                });
                node_2.find("[stroke]").each(function(index,el){
                  el = $(el);
                  el.attr("fstroke","#0000FF");
                });
                if(callback!=undefined){callback(file);}
            };
  
            reader.readAsText(file);

           



        } else {
            alert("Please drop an SVG file.");
        }
    }

  });
}

