import socket
import ssl

def check_ports_http_https(host, ports):
    """
    Check if the specified ports on a host serve HTTP or HTTPS content.

    Args:
        host (str): Hostname or IP address.
        ports (list): List of port numbers to check.

    Returns:
        dict: A dictionary with port numbers as keys and their service type as values.
              Example:
              {
                  80: "http",
                  443: "https",
                  8080: "none"
              }
    """
    results = {}

    for port in ports:
        results[port] = "none"  # Default to none
        try:
            # Check if the port is open
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((host, port))
            s.close()

            # Check for HTTP
            try:
                http_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                http_socket.settimeout(1)
                http_socket.connect((host, port))
                http_socket.sendall(b"GET / HTTP/1.1\r\nHost: {}\r\n\r\n".format(host.encode()))
                response = http_socket.recv(1024).decode()
                http_socket.close()
                if response.startswith("HTTP/"):
                    results[port] = "http"
                    continue  # Skip HTTPS check if HTTP is confirmed
            except Exception:
                pass

            # Check for HTTPS
            try:
                context = ssl.create_default_context()
                with socket.create_connection((host, port), timeout=1) as sock:
                    with context.wrap_socket(sock, server_hostname=host) as ssock:
                        ssock.sendall(b"GET / HTTP/1.1\r\nHost: {}\r\n\r\n".format(host.encode()))
                        response = ssock.recv(1024).decode()
                        if response.startswith("HTTP/"):
                            results[port] = "https"
            except Exception:
                pass

        except (ConnectionRefusedError, socket.timeout):
            results[port] = "closed"
        except Exception as e:
            results[port] = f"error ({e})"

    return results
