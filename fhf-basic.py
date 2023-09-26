from machine import Pin, PWM
import utime
import time

#fhf_basic_v1.2 - micropython code to run a FRED device using a RPi Pico 
#changes:
#v1.0 - created for use with Rpi Pico (no wifi)
#v1.1 - added melodies
#v1.2 - added data logs

### USER INPUTS REQUIRED IN THIS SECTION ###

# setup pins - these will need to change depending on where the buzzers and Reed switch are connected to the RPi Pico
led = Pin(25, Pin.OUT)
annoy_buzzer = Pin(12, Pin.OUT)     #PIN for the loudest buzzer you can get that works at ~3 V pinout of RPi (about 50% of cheap 5V buzzers seem to work OK)
reward_buzzer = PWM(Pin(16))        #PIN for a 3V piezo buzzer which allows different frequencies 
reed = Pin(15, Pin.IN, Pin.PULL_UP) #PIN for Reed switch sensor

#set silent = 1 for silent data logging; silent = 0 for normal operation with alarms etc.
silent = 0 

#set the time (in seconds) that fume hood is allowed to be left up before alarm (buzzer) activates
#recommend ~1 hr = 3600 seconds; too short and users will be annoyed if the alarm goes off during an experiment.
alarm_time = 3600

### FOLLOWING IS CODE TO BE LEFT ALONE UNLESS YOU WANT TO CHANGE STUFF ###

#initialise
#onboard LED off
led.low()

#buzzer off
annoy_buzzer.low()
reward_buzzer.duty_u16(0)

#wait before starting
utime.sleep(1) 

#set last closed time and status of fumehood as CLOSED to begin with
closed_last = time.ticks_ms()
fh_current = "CLOSED" 

#set some frequencies
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

# set melody and timing. If you want you can change this to alter the reward melody
melody_reward = 'cdefgabC'
rhythm_reward = [8, 8, 8, 8, 8, 8, 8, 8]
tempo = 0.5

try:
    while True:
        #if the magnet is not detected (fh open) Reed sensor returns 1 (high):
        if reed.value() == 1: 
            if fh_current == "CLOSED":
                fh_current = "OPEN"           #change status to open
                #print ("Fume Hood OPEN")     #print status of fume hood (uncomment for debug) 
                start_time = time.time()      #record time when fumehood opened
            led.high()                         #turn on indicator LED
            now = time.time() - start_time     #now is in seconds
            if (now > alarm_time and silent == 0):
                annoy_buzzer.high()            #activate buzzer if the time exceeds alarm time set above                
        else:                                   #if the fume hood closes, reed.value will not be 1
            if (fh_current == "OPEN" and time.ticks_diff(time.ticks_ms(), closed_last) > 1000):   #set a 1000 ms buffer to avoid issues with sensors triggering false open events
                # print("Fumehood CLOSED. Time open (sec): " + str(now))   #print status of fume hood (uncomment for debug)
                #open log and input data
                file=open("fredlog.csv", "a")
                file.write("\n" + "Silent Mode:" + "\t" + str(silent) + "\t" + "Time open (sec):" + "\t" + str(now))
                file.close()
                #turn off LED and buzzer:
                led.low()
                annoy_buzzer.low()
                #record last close time in ms (see loop above - this is to stop sensor errors giving false open events):
                closed_last = time.ticks_ms()
                time.sleep(0.1)

                if silent == 0:
                    reward_buzzer.duty_u16(30000) #activate reward noise on closing
                    for tone, length in zip(melody_reward, rhythm_reward):
                        reward_buzzer.freq(tones[tone])
                        time.sleep(tempo/length)
                    reward_buzzer.duty_u16(0)
                fh_current = "CLOSED"  #set status as closed

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