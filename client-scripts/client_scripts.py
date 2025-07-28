import os


def make_keys(user_id: int):
    try:
        os.system("echo User Private key")
        os.system("wg genkey | tee /etc/wireguard/user_privatekey | wg pubkey | tee /etc/wireguard/user_publickey")
    except Exception as exc:
        print(f"ERROR! {exc}")


def add_new_peer_to_server_conf(user_id: int):
    public_key = ""
    with open("user_publickey", "r") as file:
        public_key = file.read()
    peer_str = f'''[Peer]
PublicKey = {public_key.strip()}
AllowedIPs = 10.0.0.3/32'''
    with open("wg0.conf", "a") as file:
        file.write(peer_str)


def make_new_user_conf(user_id: int, user_adress: str):
    private_key = ""
    with open("user_privatekey", "r") as file:
        private_key = file.read()

    user_config_str = f'''[Interface]
PrivateKey = {private_key.strip()}
Address = {user_adress}
DNS = 8.8.8.8

[Peer]
PublicKey = foeu0p96/OKo3lbdxw7kuFS+aIsP1g7q1KNDO7+tsD8=
Endpoint = 185.58.115.184:51830
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 20'''
    with open(f"{user_id}wg.conf", "w") as file:
        file.write(user_config_str)
