import socket
import threading
import os
import datetime
import mimetypes
from email.utils import formatdate, parsedate_to_datetime

# 服务器配置
HOST = '127.0.0.1'  # 主机地址
PORT = 8080  # 端口号

# 创建服务器 socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)  # 监听连接，最大等待数 5
print(f"服务器监听在 {HOST}:{PORT}")

# 配置日志
import logging
logging.basicConfig(filename='server.log', level=logging.INFO, format='%(message)s')

def generate_error_response(status_code, message, connection):
    """
    生成带有 HTML 正文的错误响应
    """
    status_messages = {
        400: "Bad Request",
        403: "Forbidden",
        404: "Not Found",
        501: "Not Implemented",
    }
    status_line = f"HTTP/1.1 {status_code} {status_messages.get(status_code, 'Error')}"
    body = f"<html><body><h1>{status_code} {status_messages.get(status_code, 'Error')}</h1><p>{message}</p></body></html>"
    headers = f"Content-Type: text/html\r\n"
    headers += f"Content-Length: {len(body)}\r\n"
    headers += f"Date: {formatdate(timeval=None, localtime=False, usegmt=True)}\r\n"
    headers += f"Connection: {connection}\r\n"
    return f"{status_line}\r\n{headers}\r\n{body}".encode('utf-8')

def handle_client(client_socket):
    """
    处理客户端连接，解析请求并发送响应
    """
    file = client_socket.makefile('r', encoding='utf-8')
    while True:
        # 读取请求行
        request_line = file.readline().strip()
        if not request_line:
            break  # 没有更多请求

        # 读取头部
        headers = {}
        while True:
            line = file.readline().strip()
            if line == '':
                break
            key, value = line.split(': ', 1)
            headers[key] = value

        # 获取 Connection 头部
        connection = headers.get('Connection', 'keep-alive').lower()

        # 解析请求行
        try:
            method, path, protocol = request_line.split(' ')
            if path == '/':
                path = '/index.html'
        except ValueError:
            status = '400 Bad Request'
            response = generate_error_response(400, "Invalid request line", connection)
            client_socket.sendall(response)
            logging.info(f"{client_socket.getpeername()[0]} - {datetime.datetime.now()} - {path} - {status}")
            if connection == 'close':
                break
            continue

        # 只支持 GET 和 HEAD 方法
        if method not in ['GET', 'HEAD']:
            status = '501 Not Implemented'
            response = generate_error_response(501, "Method not supported", connection)
            client_socket.sendall(response)
            logging.info(f"{client_socket.getpeername()[0]} - {datetime.datetime.now()} - {path} - {status}")
            if connection == 'close':
                break
            continue

        # 构造文件路径
        file_path = '.' + path

        if not os.path.exists(file_path):
            status = '404 Not Found'
            response = generate_error_response(404, "File not found", connection)
        elif not os.access(file_path, os.R_OK):
            status = '403 Forbidden'
            response = generate_error_response(403, "Permission denied", connection)
        else:
            # 获取文件最后修改时间
            mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path), datetime.timezone.utc)
            last_modified = mod_time.strftime("%a, %d %b %Y %H:%M:%S GMT")

            # 检查 If-Modified-Since 头部
            if 'If-Modified-Since' in headers:
                try:
                    if_modified_since = parsedate_to_datetime(headers['If-Modified-Since'])
                    if mod_time <= if_modified_since:
                        status = '304 Not Modified'
                        response_headers = f"Date: {formatdate(timeval=None, localtime=False, usegmt=True)}\r\n"
                        response_headers += f"Last-Modified: {last_modified}\r\n"
                        response_headers += f"Connection: {connection}\r\n"
                        response = f"HTTP/1.1 304 Not Modified\r\n{response_headers}\r\n".encode('utf-8')
                        client_socket.sendall(response)
                        logging.info(f"{client_socket.getpeername()[0]} - {datetime.datetime.now()} - {path} - {status}")
                        if connection == 'close':
                            break
                        continue
                except:
                    pass
            try:
                # 读取文件内容
                with open(file_path, 'rb') as f:
                    content = f.read()
            except PermissionError:
                status = '403 Forbidden'
                response = generate_error_response(403, "Permission denied", connection)
                client_socket.sendall(response)
                continue

            # 猜测内容类型
            content_type, _ = mimetypes.guess_type(file_path)
            if content_type is None:
                content_type = 'application/octet-stream'

            status = '200 OK'
            # 构造响应头部
            response_headers = f"Content-Type: {content_type}\r\n"
            if method == 'GET':
                response_headers += f"Content-Length: {len(content)}\r\n"
            response_headers += f"Last-Modified: {last_modified}\r\n"
            response_headers += f"Date: {formatdate(timeval=None, localtime=False, usegmt=True)}\r\n"
            response_headers += f"Connection: {connection}\r\n"

            if method == 'GET':
                response = f"HTTP/1.1 200 OK\r\n{response_headers}\r\n".encode('utf-8') + content
            else:  # HEAD
                response = f"HTTP/1.1 200 OK\r\n{response_headers}\r\n".encode('utf-8')

        # 发送响应
        client_socket.sendall(response)

        # 记录日志
        logging.info(f"{client_socket.getpeername()[0]} - {datetime.datetime.now()} - {path} - {status}")

        # 如果 Connection 为 close，断开连接
        if connection == 'close':
            break

    client_socket.close()

# 主循环，接受连接并启动线程
while True:
    client_socket, addr = server_socket.accept()
    print(f"接受来自 {addr} 的连接")
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()