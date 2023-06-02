from machine import I2C, Pin, PWM ,UART,RTC,WDT,reset
from ds3231_i2c import DS3231_I2C #RTC讀的是16進制
import utime
from GET_TIME import get_time #取得時間的函數
from servo import servo #馬達旋轉的函數 橘 紅 棕

ds_i2c = I2C(0,sda=Pin(12), scl=Pin(13))

ds = DS3231_I2C(ds_i2c)
btn = Pin(17, Pin.IN, Pin.PULL_UP)
speaker = PWM(Pin(18))

pin = Pin(28, Pin.OUT, Pin.PULL_UP)

x=0
wifi_ready=0
uart = machine.UART(1,tx=Pin(8),rx=Pin(9),baudrate=115200)
led = Pin(25,Pin.OUT)

led_onboard = machine.Pin(14, machine.Pin.OUT)
pwm=PWM(Pin(15))

MusicNotes = {"B0": 31, "C1": 33,"CS1": 35,"D1": 37,"DS1": 39,"E1": 41,"F1": 44,"FS1": 46,"G1": 49,"GS1": 52,"A1": 55,"AS1": 58,"B1": 62,
"C2": 65,"CS2": 69,"D2": 73,"DS2": 78,"E2": 82,"F2": 87,"FS2": 93,"G2": 98,"GS2": 104,"A2": 110,"AS2": 117,"B2": 123,"C3": 131,"CS3": 139,
"D3": 147,"DS3": 156,"E3": 165,"F3": 175,"FS3": 185,"G3": 196,"GS3": 208,"A3": 220,"AS3": 233,"B3": 247,"C4": 262,"CS4": 277,"D4": 294,
"DS4": 311,"E4": 330,"F4": 349,"FS4": 370,"G4": 392,"GS4": 415,"A4": 440,"AS4": 466,"B4": 494,"C5": 523,"CS5": 554,"D5": 587,"DS5": 622,
"E5": 659,"F5": 698,"FS5": 740,"G5": 784,"GS5": 831,"A5": 880,"AS5": 932,"B5": 988,"C6": 1047,"CS6": 1109,"D6": 1175,"DS6": 1245,"E6": 1324,
"F6": 1397,"FS6": 1480,"G6": 1568,"GS6": 1661,"A6": 1760,"AS6": 1865,"B6": 1976,"C7": 2093,"CS7": 2217,"D7": 2349,"DS7": 2489,"E7": 2637,
"F7": 2794,"FS7": 2960,"G7": 3136,"GS7": 3322,"A7": 3520,"AS7": 3729,"B7": 3951,"C8": 4186,"CS8": 4435,"D8": 4699,"DS8": 4978}

harry=["B5","0","E6","0","0","G6","FS6","0","E6","0","0","0","B6","0","A6","0","0","0","FS6","0","0","0","E6","0","0",
"G6","FS6","0","DS6","0","0","0","E6","0","B5","0","0","0","G5","0","B5","0","0","S","B5","0","0","E6","0","0","G6","FS6","0","0","E6","0","0","0","B6","0","D7","0","0","CS7","0",
"C7","0","0","GS6","0","C7","0","0","B6","AS6","0","AS5","0","0","G6","0","E6","0","0","0","G5","0","B5","0"]

block=[40,80,120,160,0]#放入每一個的角度
D=[0,0,0,0]
servo(block[4])
#=======MQTT/Line notify========
reset='RESET'
ssid = 'SSID,blacktea890329'   #
password = 'PSWD,20000329'   #
mqtt_server = 'BROKER,mqttgo.io'
linetoken="TOKEN,DD5kW806kKEEH8BMQERiouCxyjwNChRNGWcM3T2swOW"
topic_sub = 'TOPIC,black'     
ready='ready'

def sendCMD_waitResp(cmd, uart=uart, timeout=1000):
    print(cmd)
    uart.write(cmd+'\r\n')
    waitResp()
   
def waitResp(uart=uart, timeout=1000):
    global data,wifi_ready
    prvMills = utime.ticks_ms()
    resp = b""
    while (utime.ticks_ms()-prvMills)<timeout:
        if uart.any():
            resp = b"".join([resp, uart.read(1)])
    if resp != b'' :
        data=resp
        resp = str(resp)
        print(resp)
        if (resp.find('connect'))>=0:
            wifi_ready=1
            
sendCMD_waitResp(reset)
utime.sleep(0.5)
sendCMD_waitResp(ssid)
utime.sleep(0.1)
sendCMD_waitResp(password)
utime.sleep(0.1)
sendCMD_waitResp(linetoken)
utime.sleep(0.1)
sendCMD_waitResp(topic_sub)
utime.sleep(0.1)
sendCMD_waitResp(mqtt_server)
utime.sleep(0.1)
sendCMD_waitResp(topic_sub)
utime.sleep(0.1)
sendCMD_waitResp(ready)

while (not wifi_ready) :
    utime.sleep(0.3)
    led.value(1)
    print('.')
    utime.sleep(0.3)
    led.value(0)
    print('.')
    waitResp()    
print('start')
utime.sleep(1)
for i in range(0,3):
    speaker.duty_u16(100)
    speaker.freq(2093)
    utime.sleep(0.5)
    speaker.duty_u16(65535)
    utime.sleep(0.5)
    
#設定時間
# current_time = b'\x00\x14\x08\x03\x17\x05\x23' # sec min hour week day mon year 
# ds.set_time(current_time)

def take(pin):
    global flag1
    btn.irq(handler=None)
    speaker.duty_u16(65535)
    flag1=1
    utime.sleep(1)
    btn.irq(handler=take)

btn.irq(trigger=Pin.IRQ_FALLING, handler=take)
btn.irq(handler=None) #關閉中斷功能 避免提前拿藥

# def delay():#設定延遲30分鐘
#     global goal_h
#     global goal_m
#     global goal_s
#     t = ds.read_time()
#     
#     #確定小時 把16進位的數轉為10進位
#     d=str(hex(t[2]))
#     d=d.split("x")
#     d=int(d[1])
#     goal_h=d#延遲多久 後面+數字
#     
#     #確定分鐘 把16進位的數轉為10進位
#     d=str(hex(t[1]))
#     d=d.split("x")
#     d=int(d[1])
#     goal_m=d#延遲多久 後面+數字
#     
#     #確定秒 把16進位的數轉為10進位
#     d=str(hex(t[0]))
#     d=d.split("x")
#     d=int(d[1])
#     goal_s=d#延遲多久 後面+數字

def playnote(Note, Duration):
    if Note == "0":
        utime.sleep(Duration)
    if Note == "S":
        speaker.duty_u16(65535)
        utime.sleep(Duration)
    elif Note != "0":
        speaker.duty_u16(65535)
        speaker.duty_u16(100)        
        speaker.freq(MusicNotes[Note])
        print (MusicNotes[Note])
        utime.sleep(Duration)  

def nowtime():
    global hour
    global minu
    global secs
    t = ds.read_time()#紀錄現實時間
    #小時
    hour=str(hex(t[2]))
    hour=hour.split("x")
    hour=int(hour[1])#取得現在時間
    
    #分鐘
    minu=str(hex(t[1]))
    minu=minu.split("x")
    minu=int(minu[1])#取得現在時間
    #秒
    secs=str(hex(t[0]))
    secs=secs.split("x")
    secs=str(secs[1])#取得現在時間
# delay()

while True :
    waitResp()
    data=str(data)
    if (data.find('set'))>=0:
        break
    utime.sleep(1)
T=data
Time=get_time(T)
goal_h=[Time[1],Time[3],Time[5],Time[7]]
goal_m=[Time[2],Time[4],Time[6],Time[8]]
t = ds.read_time()#紀錄現實時間
d=str(hex(t[0]))
d=d.split("x")
d=str(d[1])
goal_s=d
for k in range(0,4):
    flag1=0
    while True:#提醒迴圈
        nowtime()
        print(hour,minu,secs)
        print(int(goal_h[k]),int(goal_m[k]),goal_s)
        b=0
        if(hour==int(goal_h[k]) and minu==int(goal_m[k]) and secs==goal_s and D[k]==0):
            btn.irq(handler=take) #開啟中斷功能可以拿藥
            while (D[k]==0):#把16進位的數轉為10進位 設定30秒後跳出#音響
                for i in range(0,3):
                    for c in harry:
                        playnote(c, 0.15)
                        if flag1!=0:
                            b=2
                            break
                    speaker.duty_u16(65535)
                    utime.sleep(3)
                    if flag1!=0:
                        b=2
                        break
                speaker.duty_u16(65535)
                D[k]=1
        if(b!=0 and D[k]!=0):
            print("拿藥了")
            servo(block[k])
            btn.irq(handler=None)
            sendCMD_waitResp('MESSAGE,'+"病患已完成服藥")
            break
        if(b==0 and D[k]!=0):
            print("沒有拿藥")
            btn.irq(handler=None)
            sendCMD_waitResp('MESSAGE,'+"注意！病患尚未服藥")
            sendCMD_waitResp('MESSAGE,'+"建議主動聯絡")
            break
        utime.sleep(1)