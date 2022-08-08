from pythonping import ping
import os
#import paramiko
import socket

class ServicesSupervisor():
    def __init__(self, service_name, service_ip, method='ping', port=None) -> None:
        self.service_name : str = service_name
        self.service_ip : str = service_ip
        self.method : str = method
        self.service_port :int = port
        self.service_status : dict = self.ServiceStatus()

    def __check_service(self) -> float:
        result = os.popen("ping -c 1 " + self.service_ip).readlines()
        result = result[-1].split()
        try:
            return float(result[-2].split('/')[1])
        except:
            print("Error",result,self.service_name)
            return 100.0

    def __is_port_in_use(self) -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex((self.service_ip, self.service_port)) == 0

    def __check_service_status(self) -> bool:
        if self.method == 'ping':
            return True if self.__check_service() < 30.0 else False
        elif self.method == 'port':
            self.__check_service()
            return self.__is_port_in_use()

    def ServiceStatus(self) -> dict:
        self.service_status = {"status":self.__check_service_status(), "average":self.__check_service()}
        return {"status":self.__check_service_status(), "average":self.__check_service()}
