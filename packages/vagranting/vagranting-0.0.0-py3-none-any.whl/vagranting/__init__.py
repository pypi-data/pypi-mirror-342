#!/usr/bin/env python3
#region Imports
import os
import sys
import subprocess
import paramiko
import typing
#endregion
#region Basics
class vagranthost:
    def __load_connection(self) -> paramiko.SSHClient:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(
            hostname=self.config['HostName'],
            port=self.config['Port'],
            username=self.config['User'],
            pkey=paramiko.RSAKey.from_path(
                self.config['IdentityFile']
            )
        )
        return client

    def __init__(self, config:typing.Dict[str,str]):
        self.__client:typing.Optional[paramiko.SSHClient] = None
        self.config:typing.Dict[str,str] = config

    @property
    def client(self) -> paramiko.SSHClient:
        if self.__client is None:
            self.__client = self.__load_connection()
        return self.__client

    def exec_command(self, command:str) -> typing.Dict[str,str]:
        stdin, stdout, stderr = self.client.exec_command(command)
        return {
            'stdout':stdout.read().decode(),
            'stderr':stderr.read().decode()
        }

    def __enter__(self):
        return self

    def __exit__(self, exc_type=None, exc_value=None, traceback=None):
        self.client.close()
        return False

class vagrantfile:
    def __load_config(self, path:str) -> typing.List[typing.Dict[str,str]]:
        output: typing.List[typing.Dict[str,str]] = []
        try:
            process = subprocess.run(
                ["vagrant", "ssh-config"],
                check=True,
                capture_output=True,
                text=True,
                cwd=path,
            )

            ssh_config = {}
            for line in process.stdout.strip().split("\n"):

                if line:
                    key,value = line.strip().split(' ', 1)
                    key = key.strip()
                    value = value.strip()
                    if key in ssh_config:
                        output += [ssh_config]
                        ssh_config = {}

                    if key == "Port":
                        ssh_config[key] = int(value)
                    elif key == "IdentityFile":
                        ssh_config[key] = value.strip('"')
                    else:
                        ssh_config[key] = value

            if ssh_config != {}:
                output += [ssh_config]

        except Exception as e:
            print(e)

        return output

    def __init__(self, cwd:str=os.getcwd()):
        self.config = self.__load_config(cwd)

    @property
    def vms(self):
        vm_list = []
        for config in self.config:
            if "Host" in config:
                vm_list.append(config["Host"])
        return vm_list

    def load_vm(self, vm_name:str):
        for config in self.config:
            if "Host" in config and config["Host"] == vm_name:
                return vagranthost(config)
        return None
#endregion
