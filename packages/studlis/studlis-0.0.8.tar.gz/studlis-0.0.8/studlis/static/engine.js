var DoRequest = function (name, data = {},onsuccess,onfail) {
    return $.post({
        url: "/request/"+name,
        contentType: "application/json",
        data: JSON.stringify({"data":JSON.stringify(data)}),
        success: function(data){
            if (data.success){onsuccess(data);return;}
            
            if (typeof (onfail) == 'undefined') {
              console.log("Request failed:", data);
              ShowGenericError(data);
              return;
              }
              if (onfail(data)===true) ShowErrorMessage(data.err);

        },
        error: function(xhr, textStatus, errorThrown) {
          console.log("Request '"+name+"' failed: " + errorThrown)
          ShowGenericError("Request '"+name+"' failed: "+errorThrown);
        }
      });
    }

var DoDownload = function (name, data = {},onsuccess,onfail) {
  // var queryString = encodeURIComponent(JSON.stringify(data)); 
   var href = "/request/" + name + "/" + encodeURIComponent(JSON.stringify(data));
   var downloadLink = document.createElement("a");
   downloadLink.href = href;
   downloadLink.download = "export.zip"; 
   document.body.appendChild(downloadLink);
   downloadLink.click();
   document.body.removeChild(downloadLink);


}


var ShowGenericError = function(err){    
    m=new bootstrap.Modal('#error_modal');
    m.show();
    if(typeof err === 'string' || err instanceof String){
        $("#error_text").text(err);
        $("#error_detail").text("");
    }else{
        $("#error_text").text(err.error);
        $("#error_detail").text(err.traceback);
       // $("#error_log").text(err.log);
    }
}





