from dotenv import load_dotenv
from typing import List
import paramiko
import os

class Paramiko:
    def __init__(self) -> None:
        # Set SSHClient Instance
        self.ssh : paramiko.SSHClient = paramiko.SSHClient()        
    
    def get_environment(self,env_file:str)-> None:
        """ Set Environment """
        load_dotenv(dotenv_path=env_file) # Load env_file
        self._IP : str = os.getenv('IP')
        self._USER : str = os.getenv('USERNAME')
        self._PASS : str = os.getenv('PASS')
        self._PORT : str = os.getenv('PORT')

    def connect_server(self)-> None:
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=self._IP,port=self._PORT,username=self._USER,password=self._PASS)
        
    def log_name_change(self)-> None:
        # 로그 파일명만 출력하는 커맨드 살향
        stdin,stdout,stderr = self.ssh.exec_command(command="ls -lh /home/%s/log | awk '{print $9}'" % (self._USER))
        
        # 파일들 리스트로 분리
        log_files : List[str] = ''.join(stdout.readlines()).strip().split('\n')
        
        # 확장자명 지정
        ext : str = '.json'
        
        # http count
        http_count : int = 1
        
        # netapps count
        netapps_count : int = 1
        
        for log_file in log_files:
            if 'http' in log_file:
                try:
                    
                    # 특정 문자열 추출 위해 '_' 스트링 기준으로 분리
                    words = log_file.split('_')
                    
                    # 특정 문자열 합치기
                    new_log_file = words[0] + '-' + words[-2] + '-' + '{:03d}'.format(http_count) + ext
                    
                    # 파일명 변경
                    stdin,stdout,stderr = self.ssh.exec_command(command=f'mv /home/{self._USER}/log/{log_file} /home/{self._USER}/log/{new_log_file}')
                                    
                    # http_count 증감
                    http_count += 1
                except:
                    pass
            elif 'netapps' in log_file:
                try:
                    
                    # 특정 문자열 추출 위해 '_' 스트링 기준으로 분리
                    words = log_file.split('_')
                    
                    # 특정 문자열 합치기
                    new_log_file = words[0] + '-' + words[-2] + '-' + '{:03d}'.format(netapps_count) + ext
                    
                    # 파일명 변경
                    self.ssh.exec_command(command=f'mv /home/{self._USER}/log/{log_file} /home/{self._USER}/log/{new_log_file}')                
                                    
                    # netapps_count 증감
                    netapps_count += 1                
                except:
                    pass
        
def main()-> None:
    # Set Environment File
    __env_file : str = '.secret.env'
    
    # Create Paramiko Instance
    paramiko : Paramiko = Paramiko()
    
    # Set environment
    paramiko.get_environment(env_file=__env_file)
    
    # Connect Server
    paramiko.connect_server()
    
    # Get Log
    paramiko.log_name_change()
        
if __name__ == '__main__':
    main()