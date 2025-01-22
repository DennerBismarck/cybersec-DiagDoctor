import sys

from check_port import get_open_ports
from scan import check_ports_http_https

USAGE="""\
    Verify the ports of a host and return the open http or https ones.
    
    {} <host>
    <host> - the URL or IP adress of the host.
    """

if __name__ == "__main__":
    if len(sys.argv)==2:
        host = sys.argv[1]
        ports_to_scan = [80, 8080, 8000, 8888, 443, 8443, 4443, 3000, 4000, 5000, 7000, 9000]
        ports = get_open_ports(host=host, ports=ports_to_scan)

        print(f"Checking ports on {host}...")
        results = check_ports_http_https(host, ports)

        for port, service in results.items():
            print(f"Port {port}: {service}")
    else:
        print(USAGE.format(sys.argv[0]))