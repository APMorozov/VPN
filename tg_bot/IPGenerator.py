from file_work import read_text, write_text
import ipaddress
from database.db_work import DataBase


class IPGenerator:
    def __init__(self, subnet="10.0.0.0/24"):
        self.subnet = ipaddress.IPv4Network(subnet)

    def get_new_ip(self, db: DataBase, db_name: str):
        used_ip = db.get_used_ip(db_name)
        print(used_ip)
        for host in self.subnet.hosts():
            ip_str = f"{host}/32"
            if ip_str not in used_ip:
                return ip_str
        raise ValueError("No more free IPs in the subnet!")

