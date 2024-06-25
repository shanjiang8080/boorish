function hide_search_suggestions() {
    const delay = (delayInms) => {
        return new Promise(resolve => setTimeout(resolve, delayInms));
      };      
      const sample = async () => {
        let delayres = await delay(100);
        document.getElementById('search_box_popup').style.display = "none";
    };
      sample();
      
}

function autocomplete_search(tag_text) {
    // on click, it replaces the text with tag_text
    console.log('tapped')
    const search_text = document.getElementById('tag_list').value
    let old_text = search_text.split(', ')[(search_text.match(/, /g) || []).length];
    document.getElementById('tag_list').value = search_text.slice(0, search_text.length - old_text.length) + tag_text;
}
// for the search box, specifically. different from tag_add box TODO
let SearchBoxInput = document.querySelector('#tag_list')
SearchBoxInput.addEventListener('input', () => {
    // when this is input... do... something.
    const str = SearchBoxInput.value;
    const input = str.split(', ')[(str.match(/, /g) || []).length]; // input is the last tag
    const box = document.getElementById('search_box_popup');

    // if input is two characters, return
    if (input.length < 3) { return; }

    // it's not! then make an ajax request
    const url = `a/search_tag?text=${input}`;
    fetch(url)
    .then((response) => {
        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
        }
        return response.json();
    })
    .then((json) => {
        // make it visible
        if (json.status == "Error") {
            throw new Error(`Validation Error: ${json.err_code}`)
        }


        box.style.display = "block";
        
        // delete the things already there...
        box.innerHTML = "";

        // populate it
        for (tag of json['tags']) {
            const container = document.createElement("div");
            container.className = `box_container`;

            // making separators...
            const left = document.createElement('div');
            left.className = `box_left ${tag.color}`;
            left.innerHTML = tag.name;

            const separator = document.createElement('div');
            separator.className = "box_separator";

            const right = document.createElement('div');
            right.className = "box_right";
            right.innerHTML = tag.tag_count;

            // adding them
            container.appendChild(left);
            container.appendChild(separator);
            container.appendChild(right);
            
            // adding an onclick element to the container
            container.setAttribute('onclick', `autocomplete_search("${tag.name}")`)

            // finally, adding the container to the box
            box.appendChild(container);
        }
        
    })
    .catch((error) => {
        console.log(`Something broke. This, to be precise: ${error}`);
    })


})
