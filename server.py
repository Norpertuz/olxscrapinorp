import http.server
import socketserver

PORT = 8000

def run():
    with socketserver.TCPServer(("", PORT), http.server.SimpleHTTPRequestHandler) as httpd:
        print(f"http://localhost:{PORT}")
        httpd.serve_forever()
