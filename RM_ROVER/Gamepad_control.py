import pygame
import time
import bluetooth as bt
import socket
import sys
'''def send(dir2):
    s.send(bytes(dir2,'UTF-8'))'''




def dir(axis_val):
    dir1=""
    if(0 in axis_val.keys() and 1 in axis_val.keys()):
        x=round(axis_val[0],1)
        y=round(axis_val[1],1)
        if(x==0.0 and y==0.0):
            dir1="S"
            return dir1
    else:
        dir1="S"
        return dir1
    
    
    if ((y<=-0.8 and y>=-1.0) and (x<0.3 and x>-0.3)):
        dir1="F"
    elif (y<=1.0 and y>0.85) and (x<0.3 and x>-0.3):
        dir1="B"
    elif (x>0.85 and x<=1.0) and (y<0.3 and y>-0.3):
        dir1="R"
    elif (x<-0.85 and x>=-1.0) and (y<0.3 and y>-0.3):
        dir1="L"
    elif (x>=0.3 and x<=1.0):
        if(y>=0.3 and y<=1.0):
            dir1="J"
        elif(y>=-1.0 and y<=-0.3):
            dir1="I"
    elif (x<=-0.3 and x>=-1.0):
        if(y>=0.3 and y<=1.0):
            dir1="H"
        elif(y>=-1.0 and y<=-0.3):
            dir1="G"
    return dir1
    
speed=[10]
flag1=[0]
flag2=[0]

def speedsend(button_val,speed):
    l1=button_val[1]
    r1=button_val[2]
    flag1.append(l1)
    flag2.append(r1)
    if l1==1:
        if speed[0]==100 or (flag1[-2]==l1):
            pass
        else:
            speed[0]=speed[0]+10
    
    if r1==1:
        if speed[0]==10 or (flag2[-2]==r1):
            pass
        else:
            speed[0]=speed[0]-10
        
           
      
    




pygame.init()
axis_data = None
button_data = None
hat_data = None
j = pygame.joystick
j.init()
control=j.Joystick(0)
control.init()


'''addres="84:CC:A8:7A:38:C2"
channel = 1
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, 
socket.BTPROTO_RFCOMM)
s.connect((addres,channel))'''


'''if(j.get_count()==0):
    print("No Controller")
else:
    print("Controller present")'''
#print(control.get_name())
#print(control.get_numaxes())    
#print(control.get_numbuttons())
if not axis_data:
            axis_data = {}

if not button_data:
            button_data = {}
            for i in range(control.get_numbuttons()):
                button_data[i] = False
if not hat_data:
            hat_data = {}
            for i in range(control.get_numhats()):
                  hat_data[i] = (0, 0)


try:
 while True:
        for event in pygame.event.get():
             if event.type == pygame.JOYAXISMOTION:
                axis_data[event.axis] = round(event.value,2)
             if event.type == pygame.JOYBUTTONDOWN:
                button_data[event.button] = True
             if event.type == pygame.JOYBUTTONUP:
                button_data[event.button] = False
             if event.type == pygame.JOYHATMOTION:
                hat_data[event.hat] = event.value
             
             #print(axis_data)
            
             dir1=dir(axis_data)
             if dir1:
                print(dir1,end=' ')
             speedsend(button_data,speed)
             inch=speed[0]//10
             #print(speed[0])
             if(inch==10):
                 inch='q'
             else:
                 inch=str(inch)
             print(inch)
             #send(dir1)
             #print(axis_data.keys())   
             #time.sleep(0.1)
             if(button_data[0]==1):
                 sys.exit(0)
except KeyboardInterrupt:
    print("Interrupted")
    s.close()
