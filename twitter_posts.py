import requests
import json
import re

BEARER_TOKEN = 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA' \
               '33AGWWjCpTnA'


def get_post_data(post_id):
    """
        Returns a json that contains the given post's data.
        The data includes: creation date, the post text, number of likes, number of retweet,
        list of the post attached media (if exists) [(media_type, media_url), ..].
    """

    try:
        guest_token = generate_guest_token()
        r = requests.get("https://twitter.com/i/api/2/timeline/conversation/{}.json?&include_reply_count=1"
                         "&tweet_mode=extended".format(post_id),
                         headers={'x-guest-token': guest_token, 'authorization': BEARER_TOKEN})
        json_data = json.loads(r.text)

        if "globalObjects" not in json_data:
            raise Exception("The given post id doesn't exist.")

        post_data = json_data["globalObjects"]["tweets"][post_id]

        post_filtered_data = filter_post_data(post_data)

    except Exception as e:
        raise type(e)(str(e) + " happened when trying to get post #{} data".format(post_id))

    return post_filtered_data


def filter_post_data(post_data):
    """
    filters the given json and returns a json with the important post data
    """

    # get basic data
    i_data = {'post_created_at': post_data['created_at'], 'post_text': post_data['full_text'],
              'number_of_likes': post_data['favorite_count'], 'number_of_retweet': post_data['retweet_count']}

    # get media types and urls
    media_data = []
    if 'media' in post_data['entities']:
        for media_obj in post_data['entities']['media']:
            media_data.append((media_obj['type'], media_obj['media_url_https']))

    if media_data:
        i_data['attached_media'] = media_data

    # Get post hashtags
    hashtags = []
    if 'hashtags' in post_data['entities']:
        for hashtag_obj in post_data['entities']['hashtags']:
            hashtags.append(hashtag_obj['text'])

    if hashtags:
        i_data['hashtags'] = hashtags

    # Get user mentions
    user_mentions = []
    if 'user_mentions' in post_data['entities']:
        for user_mentions_obj in post_data['entities']['user_mentions']:
            user_mentions.append(user_mentions_obj['name'])

    if user_mentions:
        i_data['user_mentions'] = user_mentions

    return i_data


def generate_guest_token():
    """
    Generates a fresh x-guest-token that will be used in the twitter http requests
    """
    response = requests.get("https://twitter.com/")
    twitter_xml_str = response.text
    regexp = re.compile(r'document\.cookie = decodeURIComponent\(\"gt=([0-9]+);')
    guest_token_match = regexp.search(twitter_xml_str)
    if guest_token_match:
        guest_token = guest_token_match.group().split("gt=")[1].split(';')[0]
        return guest_token
    else:
        raise Exception("Failed to generate guest token.")
