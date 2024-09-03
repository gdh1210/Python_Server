import socket
from openAi import get_machine_script, execute_machine_script

if __name__ == '__main__':
    host = '0.0.0.0'
    port = 7777

# 소켓 생성 
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 바인딩
server.bind((host, port))


while True:
    data, addr = server.recvfrom(1024)
    data = data.decode("utf-8")

    print(f"Client : {data}")

    command = data
    script = get_machine_script(command)
    execute_machine_script(script)
