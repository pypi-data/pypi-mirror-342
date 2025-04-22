#!/usr/bin/env python3
#region Imports
import os
import sys
import subprocess
import testinfra
import paramiko
#endregion
#region Basics
def connect_to_vagrant(vm_name = "default"):
    try:
        process = subprocess.run(
            ["vagrant", "ssh-config", vm_name],
            check=True,
            capture_output=True,
            text=True
        )
        config_output = process.stdout

        ssh_config = {}
        for line in config_output.strip().split("\n"):
            if line:
                key,value = line.strip().split(' ', 1)
                ssh_config[key] = value

        hostname = ssh_config.get("HostName")
        port = int(ssh_config.get("Port",22))
        username = ssh_config.get("User")
        private_key = ssh_config.get("IdentityFile").strip('"')

        if not all([hostname, port, username, private_key]):
            raise ValueError("Missing required SSH configuration values.")
    
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            key = paramiko.RSAKey.from_path(private_key)
            print("Loaded RSA Key")
        except Exception as e:
            print(f"Failed to load RSA key: {e}")
        
        client.connect(
            hostname=hostname,
            port=port,
            username=username,
            pkey=key
        )
        return client
    except Exception as e:
        print(f"Error connecting to Vagrant VM: {e}")
        return None
#endregion

if __name__ == "__main__":
    vm = connect_to_vagrant("one")
    stdin, stdout, stderr = vm.exec_command("ls /")
    print(stdout.read().decode())
    print(stderr.read().decode())