$(document).ready(function () {
    // CSRF code
    function getCookie(name) {
        let cookieValue = null;
        let i = 0;
        if (document.cookie && document.cookie !== '') {
            let cookies = document.cookie.split(';');
            for (i; i < cookies.length; i++) {
                let cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    let csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $('.img_post').click(function (e) {
        e.preventDefault();
        let data = $(this).attr("data-pk");

        $.ajax({
            url: 'like/',
            method: 'POST',

            data: {
                'image_id': data
            },
            success: function (d) {
                let new_like = d['likes'];
                let like_id = '#likes_count_' + data;
                let old = $(like_id).text();
                if (old > new_like) {
                    // $(img).attr('src', '{% static 'core/img/feed/liked.png' %}');
                }

                $(like_id).text(new_like);
            },
            error: function (d) {
                console.log(d);
            }
        });
    });

});