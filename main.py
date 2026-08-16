import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

hostName = "localhost"
serverPort = 8080


class MyServer(BaseHTTPRequestHandler):
    """Специальный класс для обработки входящих запросов"""

    def do_GET(self):
        """Метод для обработки входящих GET-запросов"""

        if self.path == "/contacts" or self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            with open("contacts.html", "r", encoding="utf-8") as file:
                page_content = file.read()
            self.wfile.write(bytes(page_content, "utf-8"))

        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            with open("404.html", "r", encoding="utf-8") as file:
                page_content = file.read()
            self.wfile.write(bytes(page_content, "utf-8"))

    def do_POST(self):
        """Метод для обработки входящих POST-запросов (отправка формы)"""

        content_length = int(self.headers["Content-Length"])

        post_data = self.rfile.read(content_length)

        data_string = post_data.decode("utf-8")
        form_data = parse_qs(data_string)

        name = form_data.get("name", [""])[0]
        email = form_data.get("email", [""])[0]
        message = form_data.get("message", [""])[0]

        print("\n=== ПОЛУЧЕНЫ НОВЫЕ ДАННЫЕ ИЗ ФОРМЫ ===")
        print(f"Имя пользователя: {name}")
        print(f"Email: {email}")
        print(f"Сообщение: {message}")
        print("=======================================\n")

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        with open("contacts.html", "r", encoding="utf-8") as file:
            page_content = file.read()
        self.wfile.write(bytes(page_content, "utf-8"))


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print(f"Server started http://{hostName}:{serverPort}")

    try:
        webServer.serve_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        webServer.server_close()
        print("Server stopped.")
        sys.exit(0)
