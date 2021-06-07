# TwitterAPI

## Installation:

1. Clone the git repository: git clone https://github.com/AliciaVaknin/TwitterAPI.git

2. Create an environment that includes the following directories:
 'flask','requests','aiohttp','logging', 'json', 're'
 
3. Run twitter_api.py

## Usage:

To get data about a Twitter post by its id, run the following http request:

```
curl -X GET -H "Content-Type: application/json" -d "{ \"postID\": \"1383567148224708610\" }" http://127.0.0.1:5000/api/get_public_post
```

The request data is a json file with the following format:

```
{"postID": <post_id> }
```