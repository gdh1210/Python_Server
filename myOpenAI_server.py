import socket
from machine_script import get_machine_script, execute_machine_script

host='0.0.0.0'#임의의 네트워크 주소
port=9999

server=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#바인딩, 자바에서는 없던 개념
server.bind((host,port))

while True:
    data,addr=server.recvfrom(1024)
    data=data.decode('utf-8')
    
    print(f'Client:{data}')
    
    command=data
    
    script=get_machine_script(command)
    execute_machine_script(script)