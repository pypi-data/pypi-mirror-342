$.fn.tpl = function (id) {
    this.empty();
    var t = $("[tpl_id='" + id + "']");
    if (t.length == 0){ console.log("Error: could not find template " + id);return;}
    if (t.length > 1) {console.log("Error: multiple templates of  " + id + " found");return;}
    if (t[0].tagName == "TEMPLATE") {
        t = t[0].content.cloneNode(true);
        var node = document.importNode(t.children[0], true);
        this.append(node);
        return $(node);
    }

    var t = $("[tpl_id='" + id + "']").clone().children();

    this.append(t);
    return t;
}

$.fn.appendtpl = function (id) {
    var t = $("[tpl_id='" + id + "']");
    if (t.length == 0){ console.log("Error: could not find template " + id);return;}
    if (t.length > 1) {console.log("Error: multiple templates of  " + id + " found");return;}
    if (t[0].tagName == "TEMPLATE") {
        t = t[0].content.cloneNode(true);
        var node = document.importNode(t.children[0], true);
        this.append(node);
        return $(node);
    }

    var t = $("[tpl_id='" + id + "']").clone().children();

    this.append(t);
    return t;
}