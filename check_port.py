import socket

def get_open_ports(host, ports, timeout=1):
    """
    Check for open ports on a host from a specified list of ports.

    Args:
        host (str): Hostname or IP address.
        ports (list): List of ports to scan.
        timeout (float): Timeout in seconds for each connection attempt (default: 1).

    Returns:
        list: A list of open ports.
    """
    open_ports = []
    for port in ports:
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