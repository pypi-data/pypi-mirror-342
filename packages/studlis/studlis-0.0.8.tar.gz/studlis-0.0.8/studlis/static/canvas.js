function retrieveImageFromClipboardAsBlob(pasteEvent, callback){
	if(pasteEvent.clipboardData == false){
        if(typeof(callback) == "function"){
            callback(undefined);
        }
    };

    var items = pasteEvent.clipboardData.items;

    if(items == undefined){
        if(typeof(callback) == "function"){
            callback(undefined);
        }
    };

    for (var i = 0; i < items.length; i++) {
        // Skip content if not image
        if (items[i].type.indexOf("image") == -1) continue;
        // Retrieve image on clipboard as blob
        var blob = items[i].getAsFile();

        if(typeof(callback) == "function"){
            callback(blob);
        }
    }
}

window.addEventListener("paste", function(e){

    // Handle the event
    retrieveImageFromClipboardAsBlob(e, function(imageBlob){
        // If there's an image, display it in the canvas
        if(imageBlob){
            var canvas = document.getElementById("mycanvas");
            var ctx = canvas.getContext('2d');
            
            // Create an image to render the blob on the canvas
            var img = new Image();

            // Once the image loads, render the img on the canvas
            img.onload = function(){
                // Update dimensions of the canvas with the dimensions of the image
                canvas.width = 128;
                canvas.height = 128;

                // Draw the image
                ctx.drawImage(img, 0, 0,128,128);
            };

            // Crossbrowser support for URL
            var URLObj = window.URL || window.webkitURL;

            // Creates a DOMString containing a URL representing the object given in the parameter
            // namely the original Blob
            img.src = URLObj.createObjectURL(imageBlob);
        }
    });
}, false);

function downloadCanvasAsPNG() {
    // Use toDataURL() to convert the canvas to a data URL
    var canvas = document.getElementById("mycanvas");
    var imageURL = canvas.toDataURL("image/png");

    // Create a temporary link to initiate the download
    var downloadLink = document.createElement('a');
    downloadLink.href = imageURL;
    downloadLink.download = 'canvas_image.png'; // Name the download file

    // Append the link to the document and trigger the download
    document.body.appendChild(downloadLink);
    downloadLink.click();

    // Clean up by removing the temporary link
    document.body.removeChild(downloadLink);
}