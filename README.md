# Multi-threaded Web Server

## Description

This project implements a simple multi-threaded web server using Python's socket programming. The server supports HTTP GET and HEAD requests, serves files from the current directory, and logs requests to `server.log`. It is designed to handle multiple client connections concurrently, making it suitable for processing simultaneous HTTP requests from browsers or other clients. The server also handles various HTTP response statuses (e.g., 200 OK, 404 Not Found) and supports persistent and non-persistent connections.

## Requirements

- [Python 3.6 or later](https://www.python.org/downloads/)

The program relies on standard Python libraries, including `socket`, `threading`, `os`, `datetime`, `mimetypes`, `email.utils`, and `logging`. No external dependencies are required.

## Usage

**Note:** This is a Python program and does not require compilation. It can be run directly using the Python interpreter.

1. **Prepare the server script:**

   - Save the provided code as `web_server.py`.

2. **Set up files to serve:**

   - Place the files you wish to serve (e.g., HTML, images) in the same directory as `web_server.py`.
   - For testing, you can create a simple `index.html` file with content like `<h1>Hello, World!</h1>`.

3. **Run the server:**

   - Open a terminal and navigate to the directory containing `web_server.py`.

   - Execute the following command:

     ```bash
     python web_server.py
     ```

   - The server will start and listen on [http://127.0.0.1:8080](http://127.0.0.1:8080).

4. **Access the server:**

   - Open a web browser and navigate to [http://127.0.0.1:8080/<filename>](http://127.0.0.1:8080/), replacing `<filename>` with the name of the file you want to access.
   - For example, [http://127.0.0.1:8080/index.html](http://127.0.0.1:8080/index.html) to access `index.html`.

5. **Stop the server:**

   - Press `Ctrl+C` in the terminal where the server is running.

## Testing

You can test the server using a web browser or command-line tools like `curl`. Below are example commands to verify different functionalities:

- **Retrieve a file (GET request):**

  ```bash
  curl http://127.0.0.1:8080/index.html
  ```

  This should return the content of `index.html` if it exists.

- **Get headers only (HEAD request):**

  ```bash
  curl -I http://127.0.0.1:8080/index.html
  ```

  This returns the HTTP headers without the file content.

- **Test 404 error:**

  ```bash
  curl http://127.0.0.1:8080/nonexistent.html
  ```

  This should return an HTML error page indicating "404 Not Found".

- **Check logs:**

  - View the `server.log` file in the same directory to see recorded requests. Each log entry includes the client IP, access time, requested file, and response status.

- **Test concurrency:**

  - Open multiple browser tabs or execute multiple `curl` commands simultaneously to verify that the server handles concurrent requests effectively.

## Configuration

- **Host and Port:**
  - By default, the server listens on `127.0.0.1:8080` (localhost), which restricts access to the local machine.
  - To make the server accessible from other machines, edit `web_server.py` and set `HOST = '0.0.0.0'`. Then, use the server's IP address instead of `127.0.0.1` (e.g., [http://<server-ip>:8080](http://<server-ip>:8080)).
  - If port 8080 is in use, change the `PORT` variable in `web_server.py` to an available port (e.g., 8081).

- **Log File:**
  - Logs are written to `server.log`. To change the log file name or configuration, modify the `logging.basicConfig` call in `web_server.py`.

## Additional Notes

- **File Types:** The server uses Python's `mimetypes` module to automatically detect and serve various file types, including text files (e.g., HTML, CSS) and images (e.g., JPEG, PNG).
- **Error Handling:** The server supports multiple HTTP response statuses, such as:
  - 200 OK: Successful request.
  - 304 Not Modified: File unchanged since last request.
  - 400 Bad Request: Invalid request format.
  - 403 Forbidden: File access denied.
  - 404 Not Found: File does not exist.
  - 501 Not Implemented: Unsupported HTTP method.
- **Persistent Connections:** The server respects the `Connection` header, supporting both `keep-alive` (persistent) and `close` (non-persistent) connections.
- **Security:** The server is intended for educational purposes and local testing. For production use, additional security measures (e.g., preventing path traversal attacks) would be needed.

## Troubleshooting

- **Port Conflict:** If you receive an error indicating that port 8080 is in use, try a different port by editing the `PORT` variable in `web_server.py`.
- **File Not Found:** Ensure the requested files are in the same directory as `web_server.py`. The server serves files relative to its working directory.
- **Access Denied:** If you encounter a 403 Forbidden error, check the file permissions to ensure they are readable.
- **Testing from Other Machines:** If the server is not accessible from another machine, verify that `HOST` is set to `'0.0.0.0'` and that any firewalls allow traffic on the specified port.