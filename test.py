from server import app
from utils import post_file

if __name__ == '__main__':
    with app.test_client() as client:
        post_file(client, 'test.epub', '/upload')