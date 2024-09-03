import socket
from machine_script import get_machine_script, execute_machine_script

host = '0.0.0.0'  # 임의의 네트워크 주소
port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((host, port))

while True:
    data, addr = server.recvfrom(1024)
    try:
        message = data.decode('utf-8')
        print(f'Client: {message}')
        
        command = message
        script = get_machine_script(command)
        execute_machine_script(script)
    except UnicodeDecodeError as e:
        print(f"UnicodeDecodeError: {e}")
        print(f"Received raw data: {data}")
    except Exception as e:
        print(f"Unexpected error: {e}")
