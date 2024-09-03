<div align="center">
<img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white">
</div>

# Python 서버호스트
## CCTV AIoT 프로젝트(부속)

### 08-28(수)

자바에서 열어놓은 서버 포트는 7777 파이썬에서 열어 놓은 포트는 9999 이를 이용해 서버를 분리했고 <br>
파이썬 서버에 안드로이드에서 보낸 음성 텍스트를 받으면 이를 Open AI에 보내 인식하고 .txt 파일에 지정해둔 답변 양식을 읽어와서 <br>
command를 송출하면 자바 서버에서 이를 인식하고 서보모터를 제어하는 방식으로 진행된다.<br>

자바 서버 링크 - https://github.com/gdh1210/Java_Server_Host

# myOpenAI_server.py
```py
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
```


# machine_script.py
```py
from openai import OpenAI

client=OpenAI(api_key='이곳에 gpt API key 를 입력')

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
    try:
       actions=json.loads(script)['Machina_Actions']
       for action_key, action in actions.items(): # 수정
          #print(action_key, action)
          if 'movements' in action and action['movements']: # 추가
             execute_movements(action['movements']) # 추가
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")
        print(f"Received script: {script}")
    except KeyError as e:
        print(f"KeyError: {e}")
        print(f"Received script: {script}")
        
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
         if angle_v==90: command='F'
         elif angle_v<90: command='U'
         elif angle_v>90: command='D'
         send_to_arduino(command)
         print(command)
         time.sleep(1)
         
      if angle_h!=None:
         command=f'{pin_h},{angle_h},{speed}'
         if angle_h==90: command='F'
         elif angle_h<90: command='L'
         elif angle_h>90: command='R'
         print(command)
         send_to_arduino(command)
         time.sleep(1)

#자바 UDP 서버로 보내주는 클라이언트 코드
import socket

a_host,a_port='127.0.0.1',7777
a_addr=a_host,a_port

a_client=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

def send_to_arduino(command):
    print(command)
	#arduino_serial.write(command.encode()) => 아두이노에 직접 시리얼을 보내는 코드
	#자바 UDP 서버로 보내주는것으로 변경
    data=command.encode('utf-8')
    a_client.sendto(data,a_addr)
    
    time.sleep(0.1)
```
