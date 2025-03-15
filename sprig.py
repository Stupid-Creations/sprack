import network
import socket
import time
from machine import Pin, SPI
import st7789
import vga1_8x8 as font
import json
from things import Pwd, IP, ssid
SSID = ssid
PASSWORD = Pwd
SERVER_IP = IP
PORT = 5000 
# Connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)
down = Pin(7, Pin.IN, Pin.PULL_UP)
up = Pin(5, Pin.IN, Pin.PULL_UP)
left = Pin(6, Pin.IN, Pin.PULL_UP)
right = Pin(8, Pin.IN, Pin.PULL_UP)
select = Pin(12, Pin.IN, Pin.PULL_UP)
exit = Pin(14, Pin.IN, Pin.PULL_UP)
backspace = Pin(13, Pin.IN, Pin.PULL_UP)
shift = Pin(15, Pin.IN, Pin.PULL_UP)

spi = SPI(0, baudrate=20000000, polarity=0, phase=0,
          sck=Pin(18), mosi=Pin(19), miso=None)
tft=st7789.ST7789(spi,160,128,dc=Pin(22,Pin.OUT),reset=Pin(26,Pin.OUT),cs=Pin(20,Pin.OUT),rotations=[(0x00, 128, 160, 0, 0), (0x60, 160, 128, 0, 0), (0xc0, 128, 160, 0, 0), (0xa0, 160, 128, 0, 0)])
tft.init()
tft.rotation(1)
tft.fill(100)

while not wlan.isconnected():
    pass  # Wait for connection

print("Connected to Wi-Fi!")
channelencoder = "oshawottsarecute42"
print("making initial connection to recieve channel list")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, PORT))
print("sending proof of new connection")
client_socket.send('youreallyshouldnotbewritingthis'.encode())
rd = ""
last = None
while True:
    received_data = client_socket.recv(1024)
    if last == received_data:
        break
    rd+=received_data.decode('utf-8')
    last =received_data
channels = json.loads(rd)
client_socket.close()
keys = [i for i  in channels]

for i in keys:
    if keys.index(i) < 5:
        tft.fill_rect(0,keys.index(i)*23,160,20,0)
        tft.text(font,i,0,keys.index(i)*23)

def split_string(s, max_length=20):
    words = s.split() 
    chunks = []
    current_chunk = ""

    for word in words:
        if len(current_chunk) + len(word) + 1 > max_length or "Unfurl" in word:
            chunks.append(current_chunk.strip()) 
            current_chunk = word
        else:
            current_chunk += " " + word

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

def split_everything(s, max_length=20):
    words = [i for i in s]
    print(words)
    chunks = []
    current_chunk = ""

    for word in words:
        if len(current_chunk) + len(word) + 1 > max_length or "Unfurl" in word:
            chunks.append(current_chunk.strip()) 
            current_chunk = word
        else:
            current_chunk += " " + word

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

selector = 0
offset = 0
change = True
mode = 0
index = 0
texttime = False
offtwo = 0
oldselector = 0
oldoffset = 0
keeb = ["0123456789","qwertyuiop","asdfghjkl:","zxcvbnm,./","SEND SPACE_BAR"]
cursor = [0,0]
kt = ""

while True:
    if mode == 0:
        if change:
            tft.fill(100)
            for i in keys:
                if keys.index(i) - offset >= 0 and keys.index(i)-offset<5:
                    tft.fill_rect(0,(keys.index(i)-offset)*23,160,20,0)
                    tft.text(font,channels[i],0,(keys.index(i)-offset)*23)
            tft.fill_rect(0,(selector-offset)*23,160,20,125)
            tft.text(font,channels[keys[selector]],0,(selector-offset)*23)
            change = False
        if not down.value() and selector < len(keys) - 1:
            change = True
            selector+=1
            offset = max(0,selector-4)
            time.sleep(0.2)
        if not up.value() and selector > 0:
            change = True
            selector-=1
            offset = max(0,selector-4)
            time.sleep(0.2)
        if not select.value():
            try:
                    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client_socket.settimeout(5)  
                    client_socket.connect((SERVER_IP, PORT)) 

                    message = channelencoder+keys[selector]
                    client_socket.send(message.encode()) 
                    print("Channel sent!")

                    client_socket.close()
            except Exception as e:
                print("Connection failed:", e)
            mode = 1
            change = True
            oldselector = selector
            oldoffset = offset
            selector = 0
            time.sleep(0.2)
    if mode == 1:
        if change:
            if not texttime:
                tft.fill(100)
                tft.fill_rect(0,0,160,20,0)
                tft.fill_rect(0,23,160,20,0)
                tft.fill_rect(0,selector*23,160,20,255)
                tft.text(font,"Read",0,0)
                tft.text(font,"Write",0,23)
            else:
                print(chat)
                tft.fill(0)
                string = split_string(chat)
                for i in range(len(string)):
                    if i*8 - offtwo >= 0 and i*8 - offtwo < 128:
                        tft.text(font, string[i],0,(i*8-offtwo))
            change = False
        if not down.value():
            if not texttime and selector < 1:
                selector+=1
                change = True
            else:
                    offtwo+=8
                    change = True
                    time.sleep(0.2)
        if not exit.value():
            selector = oldselector
            offset = oldoffset
            mode = 0
            offtwo = 0
            change = True
            texttime = False
            index = 0
            chat = ""
        if not up.value():
            if not texttime and selector > 0:
                selector-=1
                change = True
            else:
                if offtwo > 0:
                    offtwo -= 8
                    change = True
                    time.sleep(0.2)
        if not select.value() and not texttime:
            if selector == 0:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.settimeout(50)  
                client_socket.connect((SERVER_IP, PORT))
                client_socket.send(f"lemmereadpls{index}".encode())  
                received_data = client_socket.recv(1024)
                chat = received_data.decode('utf-8')
                if texttime == False:
                    texttime = True
                change = True
                client_socket.close()
            else:
                mode = 2
                change = True
                print("write")
                time.sleep(0.2)
        if not left.value() and texttime and index > 0:
            index -= 1
            offtwo = 0
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(50)  
            client_socket.connect((SERVER_IP, PORT)) 
            client_socket.send(f"lemmereadpls{index}".encode())  
            received_data = client_socket.recv(1024)
            chat = received_data.decode('utf-8')
            texttime = True
            change = True
            client_socket.close()
        if not right.value() and texttime:
            index += 1
            offtwo = 0
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(50)  
            client_socket.connect((SERVER_IP, PORT)) 
            client_socket.send(f"lemmereadpls{index}".encode()) 
            received_data = client_socket.recv(1024)
            chat = received_data.decode('utf-8')
            texttime = True
            change = True
            client_socket.close()
        if not select.value() and texttime:
            change = True
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(50)  
            client_socket.connect((SERVER_IP, PORT)) 
            client_socket.send(f"threadpls{index}".encode()) 
            received_data = client_socket.recv(1024)
            client_socket.close()
            if received_data.decode('utf-8') != "":
                chat = received_data.decode('utf-8')
    if mode == 2:
        if change:
            tft.fill(0)
            tft.text(font,"0 1 2 3 4 5 6 7 8 9",0,0)
            tft.text(font,"q w e r t y u i o p",0,10)
            tft.text(font,"a s d f g h j k l :",0,20)
            tft.text(font,"z x c v b n m , . /",0,30)
            tft.text(font,"SEND SPACE_BAR",0,40)
            string = split_string(kt)
            for i in range(len(string)):
                if i*8 >= 0 and i*8 < 128:
                    tft.text(font, string[i],0,(i*8)+50)
            tft.fill_rect(cursor[0]*16,cursor[1]*10,10,10,255)
            change = False
        if not right.value() and cursor[0]<(len(keeb[cursor[1]])-1):
            cursor[0]+=1
            change = True
            time.sleep(0.2)
        if not left.value()and cursor[0]>0:
            cursor[0]-=1
            change = True
            time.sleep(0.2)
        if not up.value() and cursor[1]>0:
            cursor[1]-=1
            change = True
            time.sleep(0.2)
        if not down.value() and cursor[1] < 4:
            cursor[1]+=1
            change = True
            time.sleep(0.2)
        if not select.value():
            if cursor[1] < 4:
                if not shift.value():
                    kt += keeb[cursor[1]][cursor[0]].upper()
                    change = True
                    time.sleep(0.2)
                else:
                    kt+=keeb[cursor[1]][cursor[0]]
                    change = True
                    time.sleep(0.2)
            else:
                if cursor[0] > 2:
                    kt += " "
                    time.sleep(0.2)
                else:
                    print('sending :3')
                    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client_socket.settimeout(50)  
                    client_socket.connect((SERVER_IP, PORT)) 
                    client_socket.send(kt.encode()) 
                    client_socket.close()
                    kt = ""
                    time.sleep(0.2)
        if not exit.value():
            kt = ""
            cursor = [0,0]
            mode = 0
            change = True
            time.sleep(0.2)
                
        if not backspace.value():
            kt = kt[:-1]
            change = True
            time.sleep(0.2)
    






            
            
        
        
    




