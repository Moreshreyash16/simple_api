'''
@Author: Shreyash More

@Date: 2023-08-10 13:34:30

@Last Modified by: Shreyash More

@Last Modified time: 2023-08-10 13:34:30

@Title : Create a simple crud operation api without any framework 

'''
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import json
from dotenv import load_dotenv
import os
load_dotenv()
import requests

# creating a token with environment variable
API_KEY = os.getenv('ACCESS_TOKEN')
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    data = {}

    # get operation
    def do_GET(self):
        auth_token = self.headers.get('Authorization')
        parsed_path = urllib.parse.urlparse(self.path)
        print(auth_token)
        if auth_token != API_KEY:
            self.send_response(401)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Unauthorized')
            return
        
        if parsed_path.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            print(auth_token)
            self.wfile.write(b'Hello, this is a simple API!')
        elif parsed_path.path == '/items':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(self.data).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')
    # post operation
    def do_POST(self):
        parsed_path = urllib.parse.urlparse(self.path)

        if parsed_path.path == '/items':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            new_item = urllib.parse.parse_qs(post_data.decode('utf-8'))
            
            if 'id' not in new_item:
                self.send_response(400)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                print(new_item.get('id')[0])
                print(new_item.get('name')[0])
                self.wfile.write(b'Missing "id" in request')
                return
            
    
            item_id = new_item.get('id')[0]  # Get the ID from the new item
            item_name=new_item.get('name')[0]
            self.data[item_id] = {'id':item_id,'name':item_name}

            self.send_response(201)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(new_item).encode('utf-8'))
            
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')
    
    # put opeartion
    def do_PUT(self):
        parsed_path = urllib.parse.urlparse(self.path)

        if parsed_path.path == '/items':
            content_length = int(self.headers['Content-Length'])
            put_data = self.rfile.read(content_length)
            updated_item = urllib.parse.parse_qs(put_data.decode('utf-8'))

            item_id = updated_item.get('old_id')
            item_name = updated_item.get('name')

            if item_id is None or item_name is None:
                self.send_response(400)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'Missing "id" or "name" in request')
                return
            try:
                item_id = item_id[0]
                item_name = item_name[0]

                self.data[item_id] = {'id': item_id, 'name': item_name}
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(updated_item).encode('utf-8'))
            except Exception as e:
                print(e)
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

    # Delete operation
    def do_DELETE(self):
        parsed_path = urllib.parse.urlparse(self.path)

        if parsed_path.path == '/items':
            query_components = urllib.parse.parse_qs(parsed_path.query)
            item_id = query_components.get('id', [None])[0]

            if item_id is None:
                self.send_response(400)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'Missing "id" in query parameters')
                return
            
            if item_id in self.data:
                deleted_item = self.data.pop(item_id)
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(deleted_item).encode())
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'Item not found')
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port http://localhost:{port}...')
    httpd.serve_forever()


if __name__ == '__main__':
    run()


