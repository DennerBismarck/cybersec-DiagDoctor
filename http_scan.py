#!/usr/bin/python

import socket

def check_port_and_http(host, port):
    """
    Check the state of a TCP port on a host and whether it serves HTTP content.

    Args:
        host (str): Hostname or IP address.
        port (int): Port number.

    Returns:
        dict: A dictionary containing the port state and whether it serves HTTP.
              Example:
              {
                  "state": "open",
                  "is_http": True
              }
    """
    result = {"state": "unknown", "is_http": False}

    try:
        # Check if the port is open
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((host, port))
        s.close()
        result["state"] = "open"

        # Check if it serves HTTP
        try:
            http_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            http_socket.settimeout(1)
            http_socket.connect((host, port))
            http_socket.sendall(b"GET / HTTP/1.1\r\nHost: {}\r\n\r\n".format(host.encode()))
            response = http_socket.recv(1024).decode()
            http_socket.close()
            result["is_http"] = response.startswith("HTTP/")
        except Exception:
            result["is_http"] = False

    except ConnectionRefusedError:
        result["state"] = "closed"
    except (TimeoutError, socket.timeout):
        result["state"] = "filtered"
    except Exception as e:
        result["state"] = f"unknown ({e})"

    return result
