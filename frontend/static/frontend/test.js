function setAuthCookie(authToken, daysToExpire){
    expiryDate = new Date();
    expiryDate.setDate(expiryDate.getDate() + daysToExpire);
    document.cookie = "authToken=" + authToken + ";expires=" + expiryDate.toUTCString() +";samesite=strict";
}

function generateAlert(alertHeader, alertText, alertType){
    alertHtml = `
        <div class="alert alert-${alertType} alert-dismissible fade show" role="alert">
            <strong>${alertHeader}</strong> ${alertText}
            <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                <span aria-hidden="true">&times;</span>
            </button>
        </div>`;
    return $.parseHTML(alertHtml);
}

function generateVideoElement(video){
    console.log(video)
    videoHtml = `
        <div class="card" style="flex-basis: 30%;; margin: 1em;">
            <img class="card-img-top" src="${video.image_url}">
            <div class="card-body">
                <h5 class="card-title">
                    ${video.title}
                </h5>
                <p><b>Date Published: </b>${new Date(video.timestamp).toDateString()}</p>
                <a href="https://www.youtube.com/watch?v=${video.url}" class="stretched-link" target="_blank" rel="noopener noreferrer"/>
            </div>
        </div>`;
        return $.parseHTML(videoHtml);
}

function populate_video_feed(videos){
    for(const video of videos){
        $("#video-list").append(generateVideoElement(video));
    }
}

function fetch_videos(){
    $.get("/api/videos")
    .done(
        function(data, status){
            data.results.sort(function(a, b){
                return new Date(b.timestamp) - new Date(a.timestamp)
            });
            populate_video_feed(data.results)
            console.log("videos data " + JSON.stringify(data.results))
        }
    );
}

$(document).ready(function() {
    $.ajaxSetup({
        headers: { "Authorization": "Token a2b0bc3c93d36defb88e409d86a08743c80b04e8" }
    });

    $("#add-channel-form").submit(function(event) {
        // Do not refresh the page
        event.preventDefault();

        $.post(
            "/api/subscriptions/", {"channel": $("#channel-input").val()}
        ).done(
            function(data, status){
                $("#add-channel").prepend(generateAlert("Success", `You have successfully subscribed to ${$("#channel-input").val()}`, "success"));
            }
        ).fail(
            function(jqXHR){
                $("#add-channel").prepend(generateAlert("Error", `You were unable to subscribe to ${$("#channel-input").val()}`, "danger"));
            }
        );
    });

    $("#signin-form").submit(function(event) {
        event.preventDefault();

        $.post(
            "/api/authenticate/", {"username": $("#username-input").val(), "password": $("#password-input").val()}
        ).done(
            // Save auth token as cookie
            function(data, status){
                setAuthCookie(data["token"], 1);
                console.log(document.cookie);
                $("#signin-form").trigger("reset");
            }
        ).fail(
            function(jqXHR){
                $("#add-channel").prepend(generateAlert("Error", "Unable to login.", "danger"));
            }
        );
    });

    fetch_videos();
});