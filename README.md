<div align="center">
<img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white">
</div>

# Python 서버호스트
## CCTV AIoT 프로젝트(부속)

### 08-28(수)


# server.py
```py
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
```


# openAi.py
```py
from openai import OpenAI

client=OpenAI(api_key='')

def get_machine_script(command):
   system_message=read_system_prompt()
   response=client.chat.completions.create(
      model='gpt-4o',
      messages=[
         system_message,
         {'role':'user','content': command}
      ]
   )
   return response.choices[0].message.content

def read_system_prompt():
   content=''
   with open('file1.txt','r', encoding="UTF-8") as file:
      content+=file.read()+'\n'*2
   with open('file2.txt','r', encoding="UTF-8") as file:
      content+=file.read()
   return {'role':'system','content':content}

import json # 추가하기

def execute_machine_script(script):
   actions=json.loads(script)['Machina_Actions']
   for action_key, action in actions.items(): # 수정
      #print(action_key, action)
      if 'movements' in action and action['movements']: # 추가
         execute_movements(action['movements']) # 추가

motor_mapping={
   'motor_neck_vertical':19,
   'motor_neck_horizontal':18,
   # 이와 같은 방식으로 모터와 핀을 추가할 수 있다.
}
import time
def execute_movements(movements):
   print(movements)
   for movement_key, movement in movements.items():
      print(movement_key, movement)
      angle_v=movement.get('motor_neck_vertical',None)
      angle_h=movement.get('motor_neck_horizontal',None)
      speed=movement.get('speed','medium')
      print(angle_v, angle_h, speed)
      
      pin_v=motor_mapping.get('motor_neck_vertical',None)
      pin_h=motor_mapping.get('motor_neck_horizontal',None)
      print(pin_v, pin_h)
      if angle_v!=None:
         command=f'{pin_v},{angle_v},{speed}'
         print(command)
         if angle_v==90: command='A'
         elif angle_v<90: command='B'
         elif angle_v>90: command='C'
         send_to_arduino(command)
         time.sleep(1)
      if angle_h!=None:
         command=f'{pin_h},{angle_h},{speed}'
         print(command)
         if angle_h==90: command='a'
         elif angle_h<90: command='b'
         elif angle_h>90: command='c'
         send_to_arduino(command)
         time.sleep(1)

import socket

host,port='127.0.0.1',7777
addr=host,port

client=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

def send_to_arduino(command):
   print(command)
   # arduino_serial.write(command.encode()) # SerialClientUDPServer
   data=command.encode('utf-8')
   client.sendto(data,addr) 
   
   time.sleep(0.1)


```
