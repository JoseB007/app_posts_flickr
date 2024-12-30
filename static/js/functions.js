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
const csrftoken = getCookie('csrftoken');

function send_data(url, data, callback) {
    $.ajax({
        url: url,
        data: data,
        headers: {'X-CSRFToken': csrftoken},
        type: "POST",
        success: function (response) {
            if (!response.error) {
                if (typeof callback === "function") {
                    callback(response);
                } else {
                    location.href = callback;
                }
            }
        },
        error: function (xhr, status) {
            alert("Disculpe, existió un problema.", status + ": " + xhr);
        },
    });
}
