import socket
import os

def create_response_header(status_code, content_type, content_length):
    header = "HTTP/1.1 " + status_code + "\n"
    header += "Content-Type: " + content_type + "\n"
    header += "Content-Length: " + str(content_length) + "\n\n"
    return header.encode()

def handle_request(client_socket, request):
    try:
        method, path, version = request.split("\n")[0].split(" ")
        if method == "GET":
            if path == "/":
                path = "/index.html"

            file_path = "." + path
            if os.path.isfile(file_path):
                with open(file_path, "rb") as file:
                    content = file.read()
                    content_length = len(content)
                    response_header = create_response_header("200 OK", "text/html", content_length)
                    client_socket.sendall(response_header + content)
            else:
                content = b"404 Not Found"
                content_length = len(content)
                response_header = create_response_header("404 Not Found", "text/plain", content_length)
                client_socket.sendall(response_header + content)
    except:
        pass
    finally:
        client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8080))
    server_socket.listen()
    print("Server berjalan di localhost:8080")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Menerima koneksi dari {client_address[0]}:{client_address[1]}")
        request = client_socket.recv(1024).decode()
        print(f"Mendapatkan request: {request.split()[1]}")
        handle_request(client_socket, request)

if __name__ == "__main__":
    start_server()
