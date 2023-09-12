from machine import Pin, PWM
import utime
import time

#fhf_basic_v1.2
#changes 
#v1.0 - created for use with Rpi Pico (no wifi)
#v1.1 - added melodies
#v1.2 - added data logs

# setup pins
led = Pin(25, Pin.OUT)
annoy_buzzer = Pin(12, Pin.OUT)     #PIN for the loudest buzzer you can get that works at ~3 V pinout of RPi (many 5V buzzers seem to work OK)
reward_buzzer = PWM(Pin(16))        #PIN for a 3V piezo buzzer which allows different frequencies
reed = Pin(15, Pin.IN, Pin.PULL_UP) #PIN for Reed switch sensor

alarm_time = 3600

led.low()
annoy_buzzer.low()
reward_buzzer.duty_u16(0)
utime.sleep(1) #wait before starting
closed_last = time.ticks_ms()
fh_current = "CLOSED" #set fumehood closed to begin with

#set silent = 1 for silent data logging; silent = 0 for normal operation with alarms etc.
silent = 0 

tempo = 0.5
tones = {
     'c': 262,
     'd': 294,
     'e': 330,
     'f': 349,
     'g': 392,
     'a': 440,
     'b': 494,
     'C': 523,
     ' ': 110,
     'H': 207,
     'X': 233,
     'F': 174,
     'E': 659
}
melody_reward = 'cdefgabC'
rhythm_reward = [8, 8, 8, 8, 8, 8, 8, 8]

try:
    while True:
        #if the magnet is not detected (fh open) Hall sensor returns 1 (high):
        if reed.value() == 1: 
            if fh_current == "CLOSED":
                fh_current = "OPEN" 
                print ("Fume Hood OPEN") #print status of fume hood and turn on indicator LED
                start_time = time.time() #record time when fumehood opened
            led.high()
            now = time.time() - start_time     #now is in seconds
            if (now > alarm_time and silent == 0):
                annoy_buzzer.high() #activate buzzer                
        else:
            if (fh_current == "OPEN" and time.ticks_diff(time.ticks_ms(), closed_last) > 1000):
                print("Fumehood CLOSED. Time open (sec): " + str(now))
                file=open("fredlog.csv", "a")
                file.write("\n" + "Silent Mode:" + "\t" + str(silent) + "\t" + "Time open (sec):" + "\t" + str(now))
                file.close()
                led.low()
                annoy_buzzer.low()
                closed_last = time.ticks_ms()
                time.sleep(0.1)
                if silent == 0:
                    reward_buzzer.duty_u16(30000) #activate reward noise
                    for tone, length in zip(melody_reward, rhythm_reward):
                        reward_buzzer.freq(tones[tone])
                        time.sleep(tempo/length)
                    reward_buzzer.duty_u16(0)
                fh_current = "CLOSED"

#exit cleanly via ctrl+c
except KeyboardInterrupt:
    print ("Quit")
    led.low()
    annoy_buzzer.low()
    reward_buzzer.duty_u16(0)
    
finally:
    led.low()
    annoy_buzzer.low()
    reward_buzzer.duty_u16(0)