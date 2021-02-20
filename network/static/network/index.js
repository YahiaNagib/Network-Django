
// Select edit post buttons 
const editBtns = document.querySelectorAll(".edit-btn");
// when clicking an edit button, hide and display some contents of the post
editBtns.forEach(btn => btn.addEventListener("click", () => {

    const postContent = btn.parentElement.parentElement.querySelector(".post-content");
    const editForm = btn.parentElement.parentElement.querySelector(".edit-form");
    btn.parentElement.parentElement.querySelector(".edit-menu").classList.toggle("visible");
    // btn.style.display = "none";
    editForm.style.display = "block";
    postContent.style.display = "none";

}));

// Make a post request to the server when the post is submitted
// to edit the post
document.querySelectorAll(".edit-form").forEach(editForm => {

    editForm.onsubmit = function () {
        const csrftoken = getCookie('csrftoken');
        const postContent = this.parentElement.parentElement.querySelector(".post-content");
        fetch('edit-post', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                "X-CSRFToken": csrftoken
            },
            body:
                JSON.stringify({
                    postId: this.elements.id.value,
                    content: this.elements.content.value
                }),
        })
            .then(response => response.json())
            .then(result => {
                editForm.style.display = "none";
                postContent.style.display = "block";
                postContent.innerHTML = result["message"];
            });

        return false;

    };
});

// make post request to the server on like or dislike a post
document.querySelectorAll(".like-icon").forEach(likeBtn => {

    likeBtn.addEventListener("click", () => {
        const csrftoken = getCookie('csrftoken');
        // To change the like icon
        likeBtn.classList.toggle("far");
        likeBtn.classList.toggle("fas");
        likeBtn.classList.toggle("liked");
        fetch('/like', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                "X-CSRFToken": csrftoken
            },
            body:
                JSON.stringify({
                    postId: likeBtn.parentElement.querySelector(".post-id").value
                }),
        })
            .then(response => response.json())
            .then(result => {
                likeBtn.parentElement.querySelector(".post-likes-number").innerHTML = result["message"];
            });
    });

});

// To show the edit menu when clicking on the menu button
document.querySelectorAll(".edit-menu-btn").forEach(btn => {
    btn.addEventListener('click', function(){
        btn.parentElement.querySelector(".edit-menu").classList.toggle("visible");
    });
});


// To show comments when clicking on the comment button
document.querySelectorAll(".post-comment").forEach(btn => {
    btn.addEventListener('click', function() {
        btn.parentElement.parentElement.querySelector(".comments").style.display = "block";
    });
});

// Comment form
// To copy the content of the div to the hidden input field
document.querySelectorAll(".add-comment-form").forEach(form => {
    form.onsubmit = function() {
        this.querySelector(".comment-content").value = this.querySelector(".add-comment-input").innerHTML;
    };
});

// Copied from Django documentaion
// used to return the csrf token for the forms
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}