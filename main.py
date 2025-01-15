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
        ports = get_open_ports(host=host)

        print(f"Checking ports on {host}...")
        results = check_ports_http_https(host, ports)

        for port, service in results.items():
            print(f"Port {port}: {service}")
    else:
        print(USAGE.format(sys.argv[0]))