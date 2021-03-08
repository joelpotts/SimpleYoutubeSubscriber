# Simple YouTube Subscriper

This is a simple Django API for managing YouTube subsciptions

## Project Goals
- Re-familiarize myself with Django
- Some simple practice for django-rest-framework
- Create a simple API that can be used as a backend to practice React

## Included in the Project

- An API to manage YouTube subscriptions and fetch video data of the subscriptions
- A sample frontend using jQuery (WIP).


# The API
The primary purpose of the API is to provide a way to maintain a list of YouTube channels (subscriptions) and to provide information about the recent videos from those channels.

## Register a New User

### Request

`POST /api/register/`

    url = "http://127.0.0.1:8000/api/register/"
    data = {
        "username": "newUser",
        "password": "newPassword",
    }
    response = requests.post(url, data=data)

### Response

    HTTP/1.1 201 Created
    Date: Mon, 08 Mar 2021 10:11:44 GMT
    Server: WSGIServer/0.2 CPython/3.8.5
    Content-Type: application/json
    Vary: Accept
    Allow: POST, OPTIONS
    X-Frame-Options: DENY
    Content-Length: 18
    X-Content-Type-Options: nosniff
    Referrer-Policy: same-origin

    {"username":"newUser"}

## Authenticate

### Request

`POST /api/authenticate/`

    url = "http://127.0.0.1:8000/api/authenticate/"
    data = {
        "username": "existingUser",
        "password": "existingPassword",
    }
    response = requests.post(url, data=data)

### Response

    HTTP/1.1 200 OK
    Date: Mon, 08 Mar 2021 10:17:42 GMT
    Server: WSGIServer/0.2 CPython/3.8.5
    Content-Type: application/json
    Allow: POST, OPTIONS
    X-Frame-Options: DENY
    Content-Length: 52
    X-Content-Type-Options: nosniff
    Referrer-Policy: same-origin

    {"token":"YOUR_AUTHENTICATION_TOKEN"}

## Get Your Subscriptions

### Request

`GET /api/subscriptions/`

    url = "http://127.0.0.1:8000/api/subscriptions/"
    headers = {
        "Authorization": "Token YOUR_AUTHENTICATION_TOKEN",
    }
    response = requests.get(url, headers=headers)

### Response
    [
        {
            "id": 15,
            "channel": "AngularFirebase"
        },{
            "id": 14,
            "channel": "bingingwithbabish"
        }
    ]

## Create a New Subscription

### Request

`POST /api/subscriptions/`

    url = "http://127.0.0.1:8000/api/subscriptions/"
    # https://www.youtube.com/c/YOUTUBE_CHANNEL_NAME/videos
    data = {
        "channel": "YOUTUBE_CHANNEL_NAME",
    }
    headers = {
        "Authorization": "Token YOUR_AUTHENTICATION_TOKEN",
    }
    response = requests.post(url, data=data, headers=headers)

## Response

    HTTP/1.1 201 Created
    Date: Mon, 08 Mar 2021 10:31:42 GMT
    Server: WSGIServer/0.2 CPython/3.8.5
    Content-Type: application/json
    Vary: Accept
    Allow: GET, POST, HEAD, OPTIONS
    X-Frame-Options: DENY
    Content-Length: 30
    X-Content-Type-Options: nosniff
    Referrer-Policy: same-origin

    {"id":32,"channel":"YOUTUBE_CHANNEL_NAME"}

## Get Video Data for Your Subscriptions

### Request

`GET /api/videos/`

    url = "http://127.0.0.1:8000/api/videos/"
    headers = {
        "Authorization": "Token YOUR_AUTHENTICATION_TOKEN",
    }
    response = requests.get(url, headers=headers)

### Response
    {
        "results": [{
            "url": "qF7dkrce-mQ",
            "title": "Bitcoin \u20bf in 100 Seconds // Build your Own Blockchain",
            "image_url": "https://i.ytimg.com/vi/qF7dkrce-mQ/hqdefault.jpg?sqp=-oaymwEiCKgBEF5IWvKriqkDFQgBFQAAAAAYASUAAMhCPQCAokN4AQ==&rs=AOn4CLC6j9_HbJPu8XdKvC5w2BD4so-f9w",
            "timestamp": "2021-03-02T10:32:56.823514"
        }]
    }