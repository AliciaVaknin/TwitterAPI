from flask import Flask, request, json, jsonify
import twitter_posts
from logging import FileHandler, WARNING, Formatter


app = Flask(__name__)

# Add log file
file_handler = FileHandler('logs/twitter_api.log')
file_handler.setLevel(WARNING)
formatter = Formatter('%(asctime)s %(levelname)s %(name)s %(message)s')
file_handler.setFormatter(formatter)
app.logger.addHandler(file_handler)


@app.route('/api/get_public_post', methods=['GET'])
def get_public_post():
    """
    returns data on the given postID
    """
    if 'postID' in request.get_json():
        post_id = request.get_json()["postID"]

    else:
        return jsonify({'error_msg': "Invalid parameter, the request's JSON should contain 'postID'"}), 400

    try:
        post_data = twitter_posts.get_post_data(post_id)
    except Exception as e:
        app.logger.error(str(e))
        return jsonify({"error_message": str(e)})

    return json.dumps(post_data, ensure_ascii=False)


if __name__ == '__main__':
    app.run()

