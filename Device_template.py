import argparse
import random
import re
import subprocess

class Device():
    def __init__(self, hostname, ip_address, username, password,gateway):
        self.ten_host = hostname  # attribute
        self.dia_chi_ip = ip_address
        self.ten_tai_khoan = username
        self.mat_khau = password
        self.gateway = gateway

    # Method
    def generate_config(self):
        print(f"This is router {self.ten_host} with ip_address {self.dia_chi_ip}, username is {self.ten_tai_khoan}, password is {self.mat_khau}")
    def generate_preconfigure(self):
        if self.ten_host:
            if re.search("^SBD-\d{8}$", self.ten_host):
                hostname_config = self.ten_host
            else:
                return "Hostname is invalid, pls check again"
        else:
            hostname_config = "SBD-" + str(random.randint(10000000, 99999999))
        config_template = f"""
        version 16.12
        service timestamps debug datetime msec
        service timestamps log datetime msec
        !
        hostname {hostname_config}
        spanning-tree extend system-id
        !
        username {self.ten_tai_khoan} privilege 15 password {self.mat_khau}
        !
        redundancy
        !
        !
        interface GigabitEthernet1
         ip address {self.dia_chi_ip} 255.255.255.0
         no shut
         negotiation auto
         no mop enabled
         no mop sysid
        !
        interface GigabitEthernet2
         no ip address
         shutdown
         negotiation auto
         no mop enabled
         no mop sysid
         !
        ip forward-protocol nd
        ip http server
        ip http authentication local
        ip http secure-server
        !
        ip route 0.0.0.0 0.0.0.0 GigabitEthernet1 dhcp
        ip ssh rsa keypair-name ssh-key
        ip ssh version 2
        ip scp server enable
        !
        control-plane
        !
        !
        line con 0
         stopbits 1
        line vty 0 4
         login local
         transport input ssh
        !
        !
        end
            """
        return config_template

    def export_config(self):
        if self.ten_host:
            if re.search("^SBD-\d{8}", self.ten_host):
                hostname_config = self.ten_host
            else:
                return "Hostname is invalid, pls check again"
        else:
            hostname_config = "SBD-" + str(random.randint(10000000, 99999999))
        config_template = f"""
        version 16.12
        service timestamps debug datetime msec
        service timestamps log datetime msec
        !
        hostname {self.ten_host}
        spanning-tree extend system-id
        !
        username {self.ten_tai_khoan} privilege 15 password {self.mat_khau}
        !
        redundancy
        !
        !
        interface GigabitEthernet1
         ip address {self.dia_chi_ip} 255.255.255.0
         no shut
         negotiation auto
         no mop enabled
         no mop sysid
        !
        interface GigabitEthernet2
         no ip address
         shutdown
         negotiation auto
         no mop enabled
         no mop sysid
         !
        ip forward-protocol nd
        ip http server
        ip http authentication local
        ip http secure-server
        !
        ip route 0.0.0.0 0.0.0.0 GigabitEthernet1 dhcp
        ip ssh rsa keypair-name ssh-key
        ip ssh version 2
        ip scp server enable
        !
        control-plane
        !
        !
        line con 0
         stopbits 1
        line vty 0 4
         login local
         transport input ssh
        !
        !
        end
            """
        with open(hostname_config + ".cfg", "w") as f:
            f.write(config_template)
        return "Exported successfully"

    def check_ping(self):
        execute = subprocess.run(f"ping -c 3 {self.dia_chi_ip}", shell=True, stdin=None, capture_output=True, text=True)
        run_status = execute.stdout
        if "0.0% packet loss" in run_status:
            print("Connected")
        elif "100.0% packet loss" in run_status:
            print("Request timed out")

    def generate_route(self,routes):
        for route in routes:
            print("ip route <{}>/<{}> <{}>".format(list(route.values())[0],list(route.values())[1],self.gateway))

def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description="A single script for device management")
    parser.add_argument("-i", dest="ip_address", type=str, required=True)
    parser.add_argument("-n", dest="hostname", type=str, required=False)
    parser.add_argument("-u", dest="username", type=str, required=True)
    parser.add_argument("-p", dest="password", type=str, required=True)
    parser.add_argument("-g", dest="gateway", type=str, required=True)
    parser.add_argument("-f", dest="feature", type=str, required=True)
    args = parser.parse_args()
    ip_address = args.ip_address
    hostname = args.hostname
    username = args.username
    password = args.password
    gateway = args.gateway
    feature = args.feature
    #hostname, ip_address, username, password,gateway
    template = Device(hostname,ip_address,username,password,gateway)

    if feature == "generate_preconfig":
        template.generate_preconfigure()
    elif feature == "export_config":
        template.export_config()
        print("Exported successfully")
    elif feature == "check_availability":
        template.check_ping()
    else:
        print("Feature not supported")
    template.generate_route([{"target": "210.245.1.0","net_mask": "24"},{"target": "212.245.1.0","net_mask": "24"}])


if __name__ == "__main__":
    main()




