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