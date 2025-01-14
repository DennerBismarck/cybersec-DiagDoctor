#!/usr/bin/python

import sys
import socket

USAGE = """\
Verify the state of a TCP port of a Host.

{} <host> <port>
  <host> - the URL or IP address of the Host.
  <port> - the TCP port of the Host.\
"""

def is_http(host, port):
    """
    Check if the specified port serves HTTP content.
    """
    try:
        # Create a new socket for the HTTP test
        http_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        http_socket.settimeout(1)
        http_socket.connect((host, port))
        # Send a simple HTTP request
        http_socket.sendall(b"GET / HTTP/1.1\r\nHost: {}\r\n\r\n".format(host.encode()))
        response = http_socket.recv(1024).decode()
        http_socket.close()
        # Check if the response contains an HTTP status line
        return response.startswith("HTTP/")
    except Exception:
        return False

if __name__ == "__main__":
    """
    Main function to check port state and detect HTTP service.
    """
    if len(sys.argv) == 3:
        host = sys.argv[1]
        port = int(sys.argv[2])
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        try:
            s.connect((host, port))
            print(f"{host} {port} open")
            if is_http(host, port):
                print(f"{host} {port} serves HTTP content")
            else:
                print(f"{host} {port} does not serve HTTP content")
        except ConnectionRefusedError:
            print(f"{host} {port} closed")
        except (TimeoutError, socket.timeout):
            print(f"{host} {port} filtered")
        except Exception as e:
            print(f"{host} {port} ? {e}")
    else:
        print(USAGE.format(sys.argv[0]))


#Original Script: https://github.com/labepi/class-security/blob/main/network/portscan.py
#Modified to scan http.