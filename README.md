# Multi-threaded Web Server

This project is a simple multi-threaded web server implemented in Python using socket programming. It handles multiple HTTP GET requests concurrently, serves static files from the local directory, logs requests to a file, and returns appropriate HTTP responses, including 404 errors for non-existent files.

## Features

- **Concurrent Request Handling**: Uses multi-threading to process multiple client connections simultaneously.
- **Static File Serving**: Serves files (e.g., HTML, images) from the script’s directory.
- **Request Logging**: Logs client IP, timestamp, request line, and status code to `webserver.log`.
- **Error Handling**: Returns 404 Not Found for missing files and 405 Method Not Allowed for non-GET requests.

## Requirements

- [Python 3.6 or later](https://www.python.org/downloads/)

No external libraries are required, as the server uses standard Python modules (`socket`, `threading`, `os`, `time`, `mimetypes`).

## Setup

1. **Install Python**: Ensure [Python 3.6 or later](https://www.python.org/downloads/) is installed on your system. Verify by running `python --version` in a terminal.
2. **Prepare the Server Script**: Save the server script (e.g., `server.py`) in a directory of your choice.
3. **Create HTML Files**: Place static files, such as `index.html`, in the same directory as the script. For example, create `index.html` with:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Welcome</title>
</head>
<body>
    <h1>Welcome to My Web Server</h1>
    <p>This is a simple web server built with Python.</p>
</body>
</html>
```

You can add other files, like `about.html` or images in subdirectories (e.g., `images/logo.png`), to test additional functionality.

## Running the Server

1. **Open a Terminal**: Use a terminal or command prompt on your operating system.
2. **Navigate to the Directory**: Change to the directory containing `server.py` using `cd /path/to/directory`.
3. **Start the Server**: Run the following command:

   ```bash
   python server.py
   ```

4. **Verify Server Start**: The server will start listening on `0.0.0.0:8080`. You should see a message like:

   ```
   服务器正在监听 0.0.0.0:8080
   ```

   This translates to "Server is listening on 0.0.0.0:8080".

5. **Stop the Server**: To stop the server, press `Ctrl+C` in the terminal.

## Accessing the Server

1. **Local Access**:
   - Open a web browser and navigate to `http://localhost:8080/`.
   - You should see the content of `index.html` displayed.
   - Access other files by specifying their paths, e.g., `http://localhost:8080/about.html`.

2. **Command-Line Testing**:
   - Use `curl` to test the server:

     ```bash
     curl http://localhost:8080/
     ```

     This should return the HTML content of `index.html`.

   - To test a 404 error:

     ```bash
     curl http://localhost:8080/nonexistent.html
     ```

     This should return a 404 Not Found response.

## Logging

The server logs each request to `webserver.log` in the script’s directory. Each entry includes:

- **Client IP Address**: The IP of the requesting client (e.g., `127.0.0.1`).
- **Timestamp**: Formatted as `[DD/MMM/YYYY:HH:MM:SS +ZZZZ]`, e.g., `[29/Apr/2025:18:36:00 +0800]`.
- **Request Line**: The full HTTP request, e.g., `GET / HTTP/1.1`.
- **Status Code**: The HTTP response code, e.g., `200` for OK or `404` for Not Found.

Example log entry:

```
127.0.0.1 - [29/Apr/2025:18:36:00 +0800] "GET / HTTP/1.1" 200
```

The log file is appended to with each request, so it may grow over time. You can delete or archive it if needed.

## Troubleshooting

| **Issue** | **Solution** |
|-----------|--------------|
| **Server doesn't start** | Check if port 8080 is in use by another process (`netstat -an | find "8080"` on Windows or `lsof -i :8080` on Linux). Change the port in `server.py` (e.g., to `8081`) if needed. |
| **404 Not Found** | Verify that the requested file (e.g., `index.html`) exists in the script’s directory and the path is correct. |
| **Blank page** | A blank page may indicate a 404 error with no content. Modify the server to return a custom 404 message, e.g., `<h1>404 Not Found</h1>`. |
| **Cannot access from another machine** | Ensure the firewall allows incoming connections on port 8080. On Windows, run: <br> ```bash<br>netsh advfirewall firewall add rule name="Open Port 8080" dir=in action=allow protocol=TCP localport=8080<br>``` <br> Or use Windows Firewall with Advanced Security GUI. On Linux, run: <br> ```bash<br>sudo ufw allow 8080<br>``` <br> Also, check if the router blocks port 8080 or requires port forwarding. |

## Server Messages

The server outputs messages in Chinese. Key translations include:

- `服务器正在监听 0.0.0.0:8080`: "Server is listening on 0.0.0.0:8080"
- `接受来自 ('127.0.0.1', 12345) 的连接`: "Accepting connection from ('127.0.0.1', 12345)"
- `处理客户端 ('127.0.0.1', 12345) 时出错: [error message]`: "Error processing client ('127.0.0.1', 12345): [error message]"

To use English messages, modify the `print` statements in `server.py`.

## Notes

- The server only supports GET requests; other methods return a 405 Method Not Allowed response.
- The root path (`/`) serves `index.html` by default.
- File types are determined using the `mimetypes` module. Unknown types default to `application/octet-stream`.
- The server is designed for educational purposes and may not handle production-level loads or security requirements.