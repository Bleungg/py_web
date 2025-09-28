import sys
import os
import re
import time
import mimetypes
from http.server import *
from threading import Thread

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            root = os.path.join(os.getcwd(), "public")
            curr_path = os.path.normpath(self.path.lstrip("/"))
            full_path = os.path.join(root, curr_path)
            full_path = os.path.realpath(full_path)

            if not os.path.exists(full_path):
                raise FileNotFoundError(f"{self.path} not found")
            
            elif os.path.isdir(full_path):
                index_path = os.path.join(full_path, "index.html")

                if os.path.exists(index_path):
                    self.handle_file(index_path)

                else:
                    raise FileNotFoundError(f"No index.html in directory {self.path}")
                
            elif os.path.isfile(full_path):
                self.handle_file(full_path)

            else:
                raise FileNotFoundError(f"{self.path} is not a file")
            
        except Exception:
            self.handle_error()

    def handle_file(self, full_path):
        try:
            with open(full_path, "rb") as f:
                content = f.read()

            self.send_content(content, 200, full_path)
            
        except Exception:
            self.handle_error()

    def send_content(self, content, status, path: str=None):
        content_type = "application/octet-stream"

        if path:
            mime_type, encoding = mimetypes.guess_type(path)
            if mime_type:
                content_type = mime_type

        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))

        if path and encoding:
            self.send_header("Content-Encoding", encoding)

        self.end_headers()
        self.wfile.write(content)

    def handle_error(self):
        try:
            path = os.path.join(os.path.dirname(__file__), "../templates/error.html")
            with open(path, "rb") as f:
                content = f.read()
            self.send_content(content, 404, path)
        except Exception:
            fallback = b"<h1>404 Not Found</h1><p>The requested resource could not be found.</p>"
            self.send_content(fallback, 404)


PORT = int(sys.argv[1])

def shutdown(server: ThreadingHTTPServer, seconds):
    print(f"Server shutdown in {seconds} seconds")
    time.sleep(seconds)
    server.shutdown()
    sys.exit(0)

if __name__ == "__main__":
    serverAddress = ("localhost", PORT)
    server = ThreadingHTTPServer(serverAddress, RequestHandler)
    print(f"Server is running at http://127.0.0.1:{PORT}")
    Thread(target=server.serve_forever, daemon=True).start()

    while True:
        inp = input("")
        match = re.match(r"/exit\s*(\d*)", inp)

        if match and match.group(1) and match.group(1).strip().isdigit():
            shutdown(server, int(match.group(1)))
        elif match:
            shutdown(server, 5)
        else:
            print("Not valid exit command")
    
# http://127.0.0.1:8000/index.html