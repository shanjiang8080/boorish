function vh(percent) {
    var h = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);
    return (percent * h) / 100;
}
  
  function vw(percent) {
    var w = Math.max(document.documentElement.clientWidth, window.innerWidth || 0);
    return (percent * w) / 100;
}

window.addEventListener('scroll', () => {
    document.body.style.setProperty('--scroll', window.pageYOffset / (document.body.offsetHeight - window.innerHeight));
  }, false);  

function css_transition(pre, elem) {
    
    // gotta calculate post based on the ratio of the thumbnail
    // height is 85vh
    // width is 70vw
    // based on the ratio...
    let real_left;
    let real_width;
    let real_top;
    const em_size = parseFloat(getComputedStyle(document.getElementById("focus_info")).fontSize);
    if (window.matchMedia('only screen and (max-width: 479px)').matches) {
        // idk yet
        // well it'll be simpler because of stuff
        real_left = 0;
        real_width = vw(100);
        real_top = window.scrollY;
    } else {
        let max_height = vh(85);
        let max_width = vw(70);
        
        // okay i think how it works is we calculate max aspect ratio by doing max_width / max_height
        // then calculate the actual aspect ratio by doing pre.width / pre.height
        // and so if actual aspect > max aspect we know it's either top fit or wide fit
        // and if it's < then we know it's the other.
        
        let max_ratio = max_width / max_height;
        let real_ratio = pre.width / pre.height;
        
        let con_length = window.innerWidth - 15*em_size;
        real_top = window.scrollY;

        if (max_ratio > real_ratio) {
            // that means it is at max_height
            // and so real_height == max_height
            // now calculate based on real_ratio the width
            real_width = max_height * real_ratio;
            real_left = (con_length - real_width) / 2;
            
        } else {
            // that means it touches the sides
            // and so real_width == max_width
            real_width = max_width;
            real_left = (con_length - max_width) / 2;
                        
            real_top += (max_height - (real_width / real_ratio)) / 2;

        }

    }
    
    if (window.matchMedia('only screen and (min-width: 480px) and (max-width: 767px)').matches) real_left += 36

    document.getElementById('image_transition').innerHTML = 
    `
    @keyframes transition {
        from {
            top: ${pre.top + window.scrollY}px;
            left: ${pre.left}px;
            width: ${pre.right - pre.left}px;
        }
        to {
            top: ${real_top + 8}px;
            left: ${real_left - 8}px;
            width: ${real_width}px;
        }
    }
    
    .transition {
        position: fixed !important;
        animation-name: transition;
        animation-duration: 0.125s;
        animation-timing-function: ease-out;
        animation-fill-mode: forwards;
    }
    
    .transition_parent {
        height: ${elem.height}px !important;
    }
    `;
    elem.className = "thumb transition";
    if (elem.parentElement.className == 'image') {
        elem.parentElement.className = 'image transition_parent';
    } else if (elem.parentElement.className == 'image video') {
        elem.parentElement.className = 'image video transition_parent';
    }
    // overthinking it. just add another preview with the same src it'll get cached...

}

let selected_image = -1;

function stopVideo() {
    const video = document.getElementById("focus_file");
    if (video.nodeName == "VIDEO") {
        video.pause();
        video.currentTime = 0;
    }
}

function hide_add_tag_suggestions() {
    const delay = (delayInms) => {
        return new Promise(resolve => setTimeout(resolve, delayInms));
      };      
      const sample = async () => {
        let delayres = await delay(100);
        document.getElementById('add_tag_box_popup').style.display = "none";
    };
      sample();
      
}

function unblur_overlay() {
    document.getElementById("container").className = "container unblur";
}
function blur_overlay() {
    document.getElementById("container").className = "container blur";
    
}

function remove_overlay() {
    document.getElementById("overlay").style.display = "none";

    
    document.getElementById('image_transition').innerHTML = ``;
    document.getElementsByClassName('transition')[0].className = 'thumb';
    if (document.getElementsByClassName('transition_parent')[0].className == 'image video transition_parent') {
        document.getElementsByClassName('transition_parent')[0].className = 'image video';
    } else {
        document.getElementsByClassName('transition_parent')[0].className = 'image';
    }
    

    selected_image = -1;
    stopVideo();
    unlock_scrolling();
    unblur_overlay();
}
function lock_scrolling() {
    document.getElementById("body").className = "hide_scrollbar remove_scrolling";
}
function unlock_scrolling() {
    document.getElementById("body").className = "hide_scrollbar";
}

let delete_tag_bool = false;
function delete_tag_toggle() {
    delete_tag_bool = !delete_tag_bool;
    if (delete_tag_bool) {
        document.getElementById("focus_delete_tag").className = "delete toggled";
        // give all the things X buttons
        let something = document.getElementsByClassName("delete_tag");

        for (let i = 0; i < something.length; i++) {
            something[i].className = "delete delete_tag";
        }
          
          
    } else {
        document.getElementById("focus_delete_tag").className = "delete";
        let something = document.getElementsByClassName("delete_tag");
        for (let i = 0; i < something.length; i++) {
            something[i].className = "delete delete_tag hidden";
        }

    }
}

function delete_tag(elem) {
    const str = elem.nextSibling.firstChild.innerHTML;

    tag_name = elem.nextSibling;
    tag_link = tag_name.children[0];
    const headers = {
        "Access-Control-Origin": "*",
    }

    let formData = new FormData();
    formData.append('name', tag_link.innerHTML);
    formData.append('file', selected_image);
    formData.append('csrfmiddlewaretoken', document.querySelector("#focus_info > input[type=hidden]").getAttribute("value"));
    


    const url = `a/remove_tag`;
    fetch(url, {
        method: "POST",
        body: formData,
        credentials: 'same-origin',
    })
    .then((response) => {
        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
        }
        return response.json();
    })
    .then((json) => {
        remove_tag_from_list(str)
    })
    .catch((error) => {
        console.log(`Something broke when attempting to remove a tag. This, to be precise: ${error}`);
    })
}
function remove_tag_from_list(str) {
    console.log(`Remove tag from list... str=${str}`)
    // get num of children
    let tags = document.getElementById("focus_tags").children;
    for (let i = 0; i < tags.length; i++) {
        let tag = tags[i];
        if (tag.children[1].firstChild.innerHTML == str) {
            // it's the same, so remove tag
            document.getElementById("focus_tags").removeChild(tag);
            return;    
        }
    }
}

function add_tag_to_list(str, color) {
    const tag_spot = document.getElementById("focus_tags");
    // all that needs to happen client-side is that the new tag appears.
    
    const delete_button = document.createElement("button");
    delete_button.className = "delete delete_tag hidden";
    //delete_button.onclick = "delete_tag(this)"; // this isn't working for some reason.
    // but, 
    delete_button.setAttribute('onclick', `delete_tag(this)`)


    const delete_icon = document.createElement("i");
    delete_icon.className = "gg-close";

    
    const tagPaper = document.createElement("div");
    tagPaper.className = 'tag_paper';
    // no left part because it's right aligned and such
    const tagText = document.createElement("div");
    tagText.className = "tag_text";

    const newTag = document.createElement("a");
    newTag.innerHTML = `${str}`;
    newTag.href = `/?tag_list=${str}`;
    newTag.classList.add("link", "tag", color);

    const tagHook = document.createElement('div')
    tagHook.className = 'hook_con';
    tagHook.innerHTML = "<img class='hook' src='/static/gallery/images/hook.svg'>";

    tag_spot.appendChild(tagPaper);
    tagPaper.appendChild(delete_button);
    delete_button.append(delete_icon);
    tagPaper.appendChild(tagText);
    tagText.appendChild(newTag);
    tagPaper.appendChild(tagHook);
}

function send_add_tag() {
    const str = document.querySelector('#add_tag_input').value;


    const headers = {
        "Access-Control-Origin": "*",
    }

    let formData = new FormData();
    formData.append('name', str);
    formData.append('file', selected_image);
    formData.append('csrfmiddlewaretoken', document.querySelector("#focus_info > input[type=hidden]").getAttribute("value"));
    


    const url = `a/add_tag`;
    fetch(url, {
        method: "POST",
        body: formData,
        credentials: 'same-origin',
    })
    .then((response) => {
        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
        }
        return response.json();
    })
    .then((json) => {
        add_tag_to_list(str, json.color)
    })
    .catch((error) => {
        console.log(`Something broke when attempting to add a tag. This, to be precise: ${error}`);
    })

}

function autocomplete_add_tag_search(tag_text) {
    // on click, it replaces the text with tag_text
    console.log('tapped')
    document.getElementById('add_tag_input').value = tag_text;
}
// for the tag box, specifically. different from search box TODO
let TagBoxInput = document.querySelector('#add_tag_input')
if (TagBoxInput != null) {
    TagBoxInput.addEventListener('input', () => {
        // when this is input... do... something.
        const str = TagBoxInput.value;
        const box = document.getElementById('add_tag_box_popup');
    
        // if input is two characters, return
        if (str.length < 3) { return; }
    
        // it's not! then make an ajax request
        
    
        const url = `a/search_tag?text=${str}`;
        fetch(url)
        .then((response) => {
            if (!response.ok) {
                throw new Error(`HTTP error: ${response.status}`);
            }
            return response.json();
        })
        .then((json) => {
            // make it visible
            box.style.display = "flex";
            
            // delete the things already there...
            box.innerHTML = "";
    
            // populate it
            for (tag of json['tags']) {
                const container = document.createElement("div");
                container.className = `box_container`;
    
                // making elements...
                const left = document.createElement('div');
                left.className = `box_left ${tag.color}`;
                left.innerHTML = tag.name;

                const right = document.createElement('div');
                right.className = "box_right";
                right.innerHTML = tag.tag_count;

                const note_con = document.createElement('div');
                note_con.innerHTML = "<img class='note' src='/static/gallery/images/note.svg'>";
                note_con.className = 'note_con';

                // adding them
                container.appendChild(left);
                container.appendChild(right);
                container.appendChild(note_con);
                
                // adding an onclick element to the container
                container.setAttribute('onclick', `autocomplete_add_tag_search("${tag.name}")`)
    
                // finally, adding the container to the box
                box.appendChild(container);
            }
            
        })
        .catch((error) => {
            console.log(`Something broke when suggesting tags to add. This, to be precise: ${error}`);
        })
    
    
    })
    
}




let images = document.getElementsByClassName("thumb");
let a = 0;
for (let i = 0; i < images.length; i++) {
    images[i].onclick = function(e) {
        const image_id = images[i].src.match(/[^\/]\d*(?=\.jpg)/)[0];
        selected_image = image_id;
        // console.log(image_id);
        const url = `a/view_image?id=${image_id}`
        // make an ajax request.

        fetch(url)
        .then((response) => {
            if (!response.ok) {
                throw new Error(`HTTP error: ${response.status}`);
            }
            // console.log(response.json())

            return response.json();
        })
        // i think it's json because the view returns json
        .then((json) => {
            // need to create divs and such in the view to make it show properly...
            
            // making the overlay div visible
            document.getElementById("overlay").style.display = "block";

            // blurring the content
            blur_overlay();

            // adding the image/video to the overlay
            document.getElementById('focus_image').innerHTML = ""

            var newElem;
            var prevElem;
            const image_spot = document.getElementById("focus_image");
            if (json['is_video']) {
                newElem = document.createElement('video');
                newElem.setAttribute('controls', true);
                newElem.id = "focus_file";

                // add element to image
                newElem.src = `/media/${json['file_name']}`;
                image_spot.appendChild(newElem)

                newElem.addEventListener('loadedmetadata', function(e){
                    // give the clicked element a transition from its current position to its full position...
                    // both scale it and move it.
                    // scale goes from center btw
                    
                    css_transition(images[i].getBoundingClientRect(), images[i]);


                });
                

            }
            else {
                newElem = document.createElement('img');
                newElem.id = "focus_file";

                // add element to image
                newElem.src = `/media/${json['file_name']}`;
                newElem.style.backgroundImage = `url("/media/thumbnails/${image_id}.jpg")`;
                newElem.style.backgroundPosition = 'center';
                newElem.style.backgroundRepeat = 'no-repeat';
                newElem.style.backgroundSize = 'contain';
                image_spot.appendChild(newElem)

                css_transition(images[i].getBoundingClientRect(), images[i]);

            }

            

            // adding the tags to the overlay

            const tag_spot = document.getElementById("focus_tags")
            tag_spot.innerHTML = "";
            for (const tag of json['tags']) {

                add_tag_to_list(tag.name, tag.color);

            }

            // adding votes and publish-date
            // document.getElementById("focus_votes").innerHTML = `votes: ${json['votes']}`;
            // document.getElementById("focus_date").innerHTML = `posted: ${json['date']}`;
            
            // lock scrolling
            lock_scrolling();

            // that's it! I think...
        })
        .catch((error) => {
            console.log(`Something broke when focusing an image. This, to be precise: ${error}`)
        });
    };
};
