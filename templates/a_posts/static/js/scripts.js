// {% for comment in post.comments.all %}
// {% include 'a_posts/comment.html' %}
// {% endfor %}

$(function () {
    function loadComments() {
        $.ajax({
            url: window.location.pathname,
            type: "GET",
            data: {
                action: "get_comments",
            },
            success: function (response) {
                if (!response.error) {
                    const commentsSection = $("#tab-contents");
                    commentsSection.empty();
                    const comments = response.comments;
                    comments.forEach((comment) => {
                        commentsSection.append(
                            `<comment class="card p-4 !mb-4">
                                <div class="flex justify-between items-center"> 
                                    <a class="flex items-center gap-1 mb-2" href="${comment.author_profile_url}">
                                        <img class="w-8 h-8 object-cover rounded-full" src="${comment.avatar}"> 
                                        <span class="font-bold hover:underline">${comment.author}</span>
                                        <span class="text-sm font-normal text-gray-400">@${comment.user}</span>
                                    </a>
                                </div>
                                <p class="text-xl px-2">
                                    ${comment.body}
                                </p>
                                {% include 'a_posts/reply.html' %}
                            </comment>`
                        );
                    });
                }
            },
            error: function (xhr, status, error) {
                console.error("Error al cargar comentarios:", error);
            },
        });
    }

    loadComments();
});
