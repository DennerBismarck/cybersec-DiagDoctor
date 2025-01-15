import socket

def get_open_ports(host, start_port=1, end_port=65535, timeout=1):
    """
    Check for all open ports on a host within a specified range.

    Args:
        host (str): Hostname or IP address.
        start_port (int): Starting port number (default: 1).
        end_port (int): Ending port number (default: 65535).
        timeout (float): Timeout in seconds for each connection attempt (default: 1).

    Returns:
        list: A list of open ports.
    """
    open_ports = []
    for port in range(start_port, end_port + 1):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(timeout)
            s.connect((host, port))
            s.close()
            open_ports.append(port)
        except (ConnectionRefusedError, socket.timeout):
            pass  # Port is closed or filtered
        except Exception as e:
            print(f"Error checking port {port}: {e}")
            pass
    return open_ports
