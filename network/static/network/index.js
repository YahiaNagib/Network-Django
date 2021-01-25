
const editBtn = document.querySelectorAll(".edit-btn");

editBtn.forEach(btn => btn.addEventListener("click", () => {

    const postContent = btn.parentElement.querySelector(".post-content");
    const editForm = btn.parentElement.querySelector(".edit-form");
    btn.style.display = "none";
    editForm.style.display = "block";
    postContent.style.display = "none";

}));

document.querySelectorAll(".edit-form").forEach(editForm => {

    editForm.onsubmit = function () {
        const csrftoken = getCookie('csrftoken');
        const postContent = this.parentElement.querySelector(".post-content");
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
                this.parentElement.querySelector(".edit-btn").style.display = "block";
                postContent.innerHTML = result["message"];
            });

        return false;

    };
});

document.querySelectorAll(".like-icon").forEach(likeBtn => {

    likeBtn.addEventListener("click", () => {
        const csrftoken = getCookie('csrftoken');
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