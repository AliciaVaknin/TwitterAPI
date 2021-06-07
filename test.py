from twitter_api import app
import unittest


class TwitterAPITestCase(unittest.TestCase):

    # check if response is 200
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/api/get_public_post', json={'postID': '1233441223232245760'})
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    # check if the returned data is correct
    def test_returned_data(self):
        tester = app.test_client(self)
        response = tester.get('/api/get_public_post', json={'postID': '1233441223232245760'})
        self.assertTrue(b'post_created_at' in response.data)


if __name__ == "__main__":
    unittest.main()