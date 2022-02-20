import platform
import os
import requests

class SysInfo:
    def print_info():
        machine_platform = platform.machine()
        version_platform = platform.version()
        system_platform = platform.system()
        processor_platform = platform.processor()
        platform_username = os.getlogin()
        public_ip = requests.get("https://api.ipify.org").text

        text = f"""
    [SYSINFO]

    Machine
    {machine_platform} 

    Version
    {version_platform}
    
    System
    {system_platform}

    Processor
    {processor_platform}

    Windows Username
    {platform_username}

    Public IP
    {public_ip}

    """
        return text

if __name__ == "__main__":
    SysInfo.print_info()