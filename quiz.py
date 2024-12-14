import http.server
import socketserver
import json
import os

PORT = 8005

class QuizHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/get-student-data":
            if os.path.exists("student_data.json"):
                with open("student_data.json", "r") as file:
                    data = file.read()
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(data.encode())
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"{}")
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == "/save-student-data":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            student_data = json.loads(post_data.decode())
            
            # Save data to a file
            if os.path.exists("student_data.json"):
                with open("student_data.json", "r") as file:
                    data = json.load(file)
            else:
                data = {}

            student_id = student_data['student_id']
            if student_id not in data:
                data[student_id] = []

            data[student_id].append(student_data['quiz_data'])

            with open("student_data.json", "w") as file:
                json.dump(data, file)

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Data saved successfully!")

Handler = QuizHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()
