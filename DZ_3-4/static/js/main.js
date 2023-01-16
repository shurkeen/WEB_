const not_auth = "You are not authorized"

$(".like-question").on('click', function(ev){
    if ($("#user-is-logged").text() == 'yes')
    {
        const request = new Request(
            'http://127.0.0.1:8000/like/',
            {
                method: 'POST',
                headers: {
                    'X-CSRFToken' : csrftoken,
                    'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8'

                },
                body: 'question_id=' + $(this).data('id')
            }
        )

        fetch(request).then(
            response => response.json().then(
                (response) => {
                    const old_count_likes = $(this).text(); 
                    $(this).text(response.count_likes);
                    const new_count_likes = $(this).text();
                    if (new_count_likes > old_count_likes)
                    {
                        $(this).addClass("like-up");
                    }
                    else
                    {
                        $(this).removeClass("like-up");
                    }
                }
            )
        );
    }
    else
    {
        alert(not_auth);
    }
})


$(".like-answer").on('click', function(ev){
    if ($("#user-is-logged").text() == 'yes')
    {
        const request = new Request(
            'http://127.0.0.1:8000/like_answer/',
            {
                method: 'POST',
                headers: {
                    'X-CSRFToken' : csrftoken,
                    'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8'
    
                },
                body: 'answer_id=' + $(this).data('id')
            }
        )
    
        fetch(request).then(
            response => response.json().then(
                (response) => {
                    const old_count_likes = $(this).text(); 
                    $(this).text(response.count_likes_answer);
                    const new_count_likes = $(this).text();
                    if (new_count_likes > old_count_likes)
                    {
                        $(this).addClass("like-up");
                    }
                    else
                    {
                        $(this).removeClass("like-up");
                    }
                }
            )
        );
    }
    else
    {
        alert(not_auth);
    }
})

$(".correct-button").on('click', function(ev){
    if ($("#user-is-logged").text() == 'yes')
    {
        const request = new Request(
            'http://127.0.0.1:8000/correct/',
            {
                method: 'POST',
                headers: {
                    'X-CSRFToken' : csrftoken,
                    'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8'
    
                },
                body: 'answer_id=' + $(this).data('id')
            }
        )
    
        fetch(request).then(
            response => response.json().then(
                (response) => 
                {
                    console.log(response)
                    console.log("#" + response.old_answer_id)
                    if (response.status)
                    {
                        if (response.correct)
                        {
                            $(this).addClass("btn-success");
                        }
                        else
                        {
                            $(this).removeClass("btn-success");
                        }
                        // удаляем старый верный вопрос, если он был
                        if (response.old_answer_id)
                        {
                            $('[data-id="' + response.old_answer_id + '"]').removeClass("btn-success");
                        }
                    }
                    else
                    {
                        alert("You are not the author of the question");
                    }
                }
            )
        );
    }
    else
    {
        alert(not_auth);
    }
})