import socket
import threading
import os
import time
import mimetypes

HOST = '0.0.0.0'  # 监听所有接口
PORT = 8080  # 端口号
LOG_FILE = 'webserver.log'  # 日志文件名

log_lock = threading.Lock()  # 日志锁，确保线程安全

def handle_client(client_socket, client_address):
    try:
        request = client_socket.recv(1024).decode('utf-8')
        if not request:
            return
        # 解析请求
        request_lines = request.split('\n')
        request_line = request_lines[0].strip()
        method, path, _ = request_line.split()
        if method != 'GET':
            response = 'HTTP/1.0 405 Method Not Allowed\r\n\r\n'
            client_socket.sendall(response.encode('utf-8'))
            return
        # 处理路径
        if path == '/':
            path = '/index.html'
        file_path = '.' + path
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
            content_type, _ = mimetypes.guess_type(file_path)
            if content_type is None:
                content_type = 'application/octet-stream'
            response = f'HTTP/1.0 200 OK\r\nContent-Type: {content_type}\r\nContent-Length: {len(content)}\r\n\r\n'
            response = response.encode('utf-8') + content
            status = '200'
        except FileNotFoundError:
            response = 'HTTP/1.0 404 Not Found\r\nContent-Type: text/html\r\n\r\n<h1>404 Not Found</h1><p>Requesting file is not exist.</p>'
            response = response.encode('utf-8')
            status = '404'
        client_socket.sendall(response)
        # 记录日志
        with log_lock:
            with open(LOG_FILE, 'a') as log:
                log_time = time.strftime('%d/%b/%Y:%H:%M:%S %z', time.localtime())
                log_entry = f'{client_address[0]} - [{log_time}] "{request_line}" {status}\n'
                log.write(log_entry)
    except Exception as e:
        print(f'处理客户端 {client_address} 时出错: {e}')
    finally:
        client_socket.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f'服务器正在监听 {HOST}:{PORT}')
    while True:
        client_socket, client_address = server_socket.accept()
        print(f'接受来自 {client_address} 的连接')
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

if __name__ == '__main__':
    main()