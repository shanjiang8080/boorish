const typeSet = new Set([
    '.png', 
    '.avif',
    '.jpg',
    '.jpeg',
    '.jfif',
    '.pjpeg',
    '.pjp',
    '.gif',
    '.webp',
    '.apng',
    '.svg',
    '.mp4',
    '.webm',
]);

var loadFile = function(event) {
    var gallery = document.getElementById('upload_gallery');
    gallery.innerHTML = "";

    // for each image uploaded, create an element.
    for (const file of event.target.files) {
        const ext = file.name.match(/\.\w+$/)[0];
        console.log(ext);
        if (!typeSet.has(ext)) {
            continue;
        }
        if (ext == ".mp4" || ext == ".webm") {
            const img = document.createElement('video');
            img.style = "width: 100%;";
            img.onload = function() {
                URL.revokeObjectURL(img.src) // free memory
            }
            img.src = URL.createObjectURL(file);
            // attach it to a div container
            const div = document.createElement('div');
            div.className = 'image video';
            const hr1 = document.createElement('hr');
            hr1.style = "border: none; position: absolute; border-bottom: 4px dashed #fff8f1; width: 100%; border-top: 4px dashed #fff8f1; top: -1.25em;";
            const hr2 = document.createElement('hr');
            hr2.style = "border: none; position: absolute; border-bottom: 4px dashed #fff8f1; width: 100%; border-top: 4px dashed #fff8f1; bottom: -1.25em;";
            div.appendChild(hr1);
            div.appendChild(img);
            div.appendChild(hr2);            
    
            // attach div container to gallery.
            gallery.appendChild(div);
        } else {
            // create a new img tag
            const img = document.createElement('img');
            img.onload = function() {
                URL.revokeObjectURL(img.src) // free memory
            }
            img.src = URL.createObjectURL(file);
            // attach it to a div container
            const div = document.createElement('div');
            div.className = 'image';
            div.appendChild(img);

            // attach div container to gallery.
            gallery.appendChild(div);
        }

    };
    
};
