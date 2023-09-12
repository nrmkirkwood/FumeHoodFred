import RPi.GPIO as GPIO
import utime
import time
import datetime
import random
import pymsteams

#This version of FHF code is for a RPi with wi-fi and can post to Microsoft Teams.

#v2.03
#changes 
#v2.01 or lower - development
#v2.02 - tweaked buzzer time to 1 hr, first post to 1 hr 10 min
#v2.03 - added a 0.5 second wait before looping to slow down program a bit

# setup Teams WebHook connection
myTeamsMessage = pymsteams.connectorcard("INSERT WEBHOOK HERE")

# setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17 , GPIO.IN, pull_up_down=GPIO.PUD_UP) #hall effect sensor
GPIO.setup(18, GPIO.OUT) #indicator LED
GPIO.setup(21, GPIO.OUT) #buzzer

#Turn off posting to Teams by setting ChattyFred to 0
ChattyFred = 1

#Turn off buzzer by setting NoisyFred to 0
NoisyFred = 1

#some constants for a fumehood
CO2perhr = 4.5
kWhperhr = 4.2

#messages - {0} = time in hrs, {1} = massCO2 used, {2} = CO2perhr, {3} = kWh used, {4} = time for tree to remove CO2 @ 15 kg/yr 
#alert messages
s1 = ("Knock, knock, who's there? ... Nobody, apparently, because I've been left up for {0} hours! Apparently you all hate the planet, because during this time I've emitted {1} kg of CO2.")
s2 = ("Can I remind you all that I am saving your lives by preventing you from breathing in toxic vapours, and all I get in thanks is being left up for {0} hours and counting? I'm fuming.'")
s3 = ("Fumehood, fumehood burning bright, burning fossil fuels all through the night. That's right, I've been left up again. Already burned {3} kWh of energy... and counting.")
s4 = ("I didn't realise this was an open relationship... I've been left open for the past {0} hours, during which I've emitted {1} kg of CO2.")
s5 = ("Once again I'm left open - if I had a dollar for every time I was left up, it would't even pay for my energy bill - since I was opened {0} hours ago, I have wasted {3} kWh.")
s6 = ("I'm glad you are all doing your part to increase global temperatures. I've been left up and have already emitted {1} kg of CO2. Maybe once the world is 2 C warmer you will remember to close me.")
s7 = ("Are all human lab users this forgetful? I've been left up for {0} hours and emitted {1} kg of CO2. You know that when the world heats up us robots will handle it a lot better than you will, right?")
s8 = ("You've left me up again. {0} hours and counting, {1} kg of CO2 emitted, world continuing to heat up. To quote a great fellow robot: I could calculate your chance of survival, but you won’t like it.")
s9 = ("I've been left up for {0} hours already. FYI, I consume as much energy as four houses in Melbourne. You humans are paying the bills so you might want to close me at some point.")
s10 = ("I've been left open for {0} hours. I hope that you are all enjoying the unnecessary {1} kg of CO2 that I've emitted over this time...")
s11 = ("Dear Human Fumehood Users. You are terrible humans. I've been left up. Again. For {0} hours. Pick up your game and close me before I get mad and dob you all in to Greta Thunberg.")
#Make list of strings
alert_options = [s1,s2,s3,s4,s5,s6,s7,s8,s9,s10, s11] 

#stop messages
stop1 = "Finally, after {0} hours, I've been closed. Thank you, human."
stop2 = "I'm closed, at least somebody likes the planet. I still emitted {1} kg of CO2, mind you."
stop3 = "Better turn your heater back on, because I've been closed so we are now a tiny bit closer to averting catastrophic global warming. I 'only' emitted {1} kg of CO2 this time."
stop4 = "Somebody has shut me... While I was up, I used as much power as four houses. Not that I care, I'm just a fume hood, I don't pay the bills."
stop5 = "Once again I'm closed, after another {0} hours up - I wonder if a lab human really ran an experiment in me that whole time...?"
stop6 = "I've been closed after {0} hours up. It is going to take a eucalyptus tree about {4} years to remove the extra CO2 from the atmosphere. Better get planting..."
#Make list of strings
stop_options = [stop1, stop2, stop3, stop4, stop5, stop6]

utime.sleep(3) #wait 3 seconds before starting

try:
  run = 0
  alert = 0
  first_announce = 0
  second_announce = 0
  third_announce = 0
  fourth_announce = 0

  while True :
    # check for start
    if GPIO.input(17)== 1 or run == 1:

      #if the fume hood was previously closed, "run" will be 0
      if run == 0:
        #print status of fume hood and turn on indicator LED
        start_time = time.time()
        today = datetime.datetime.strftime(datetime.datetime.today() , '%d/%m/%Y\t%H:%M')
        print (str(today) + "\tFume Hood OPEN")            
        GPIO.output(18, GPIO.HIGH)

      now = time.time() - start_time     #now is in seconds
      
      # calculate h,m,s
      m,s = divmod(now,60)
      h,m = divmod(m,60)
      
      #calculate some other things
      massCO2 = int(round(CO2perhr*h))
      kWh = int(round(kWhperhr*h))
      treetime = massCO2/15 #based on 15 kgCO2/year removal rate https://ecotree.green/en/how-much-co2-does-a-tree-absorb

      # set to run continuously while fume hood is "OPEN"
      run = 1

      #the following if statement starts buzzing after set times
      if NoisyFred == 1:
        
        #buzzing after 1 hour
        if now > 3600 and alert == 0:
          #start buzzing
          GPIO.output(21, GPIO.HIGH)

      #the following "if" statements trigger alerts if the fume hood is left OPEN for set times
      if ChattyFred == 1:

        #first alert at 1 hour 10 min
        if now > 4200 and first_announce == 0:

          #Generate random number chosen from length of list, to be used to randomly pick an item from the list. 
          r = random.randint(0,len(alert_options)-1) #"-1" accounts for indexing of lists starting at 0 not 1

          #now pick the random item from options list, add in data, and print it
          first_announce_text = alert_options[r].format(h, massCO2, CO2perhr, kWh, treetime)
          print (first_announce_text)

          #post on Teams
          myTeamsMessage.text(first_announce_text)
          myTeamsMessage.send()
          first_announce = 1              
          
          #set "alert mode" variable to 1 to indicate the fume hood is complaining    
          alert = 1

        #second alert at 12 hours
        if now > 43200 and second_announce == 0:

          #Generate random number chosen from length of list, to be used to randomly pick an item from the list. 
          r = random.randint(0,len(alert_options)-1) #"-1" accounts for indexing of lists starting at 0 not 1

          #now pick the random item from options list, add in data, and print it
          second_announce_text = alert_options[r].format(h, massCO2, CO2perhr, kWh, treetime)              
          print (second_announce_text)    

          #post on Teams
          myTeamsMessage.text(second_announce_text)
          myTeamsMessage.send()
          second_announce = 1
          alert = 1

        #third alert at 48 hours
        if now > 172800 and third_announce == 0:

          #Generate random number chosen from length of list, to be used to randomly pick an item from the list. 
          r = random.randint(0,len(alert_options)-1) #"-1" accounts for indexing of lists starting at 0 not 1

          #now pick the random item from options list, add in data, and print it
          third_announce_text = alert_options[r].format(h, massCO2, CO2perhr, kWh, treetime)                 
          print (third_announce_text)    

          #post on Teams
          myTeamsMessage.text(third_announce_text)
          myTeamsMessage.send()
          third_announce = 1
          alert = 1
                   
        #fourth alert at 1 week
        if now > 604800 and fourth_announce == 0:

          #Generate random number chosen from length of list, to be used to randomly pick an item from the list. 
          r = random.randint(0,len(alert_options)-1) #"-1" accounts for indexing of lists starting at 0 not 1

          #now pick the random item from options list, add in data, and print it
          fourth_announce_text = alert_options[r].format(h, massCO2, CO2perhr, kWh, treetime)                 
          print (fourth_announce_text)

          #post on Teams
          myTeamsMessage.text(fourth_announce_text)
          myTeamsMessage.send()
          fourth_announce = 1
          alert = 1
          
          
      utime.sleep(0.5) #wait a bit before looping
      
    # check for stop
    if GPIO.input(17)==0:

      #if fume hood was previously OPEN
      if run == 1:
        #print fume hood status and turn off LED indicator
        today = datetime.datetime.strftime(datetime.datetime.today() , '%d/%m/%Y\t%H:%M')
        print (str(today) + "\tFume Hood CLOSED")
        GPIO.output(18, GPIO.LOW)

        #stop buzzing
        GPIO.output(21, GPIO.LOW)
        
        #add record of how long fume hood was open for to file fredlog.txt
        with open('fredlog.txt', 'a') as f:
          f.write('\n'+ str(today) + '\t' + str(int(round(now))) + '\t' + str(ChattyFred) + '\t' + str(NoisyFred))

      #set status of fume hood to CLOSED
      run = 0
      first_announce = 0
      second_announce = 0
      third_announce = 0
      fourth_announce = 0
            
      #if any Teams posts were made, let people know Fred has been closed       
      if alert == 1 and ChattyFred == 1:        
         
        #Generate random number chosen from length of list, to be used to randomly pick an item from the list. 
        r = random.randint(0,len(stop_options)-1) #"-1" accounts for indexing of lists starting at 0 not 1

        #now pick the random item from options list, add in data, and print it
        stop_msg = stop_options[r].format(h, massCO2, CO2perhr, kWh, treetime)
        print (stop_msg)

        #post to Teams
        myTeamsMessage.text(stop_msg)
        myTeamsMessage.send()         

      #reset alert mode to zero
      alert = 0
      #wait a bit before looping
      utime.sleep(0.5) 
    
#exit via ctrl+c
except KeyboardInterrupt:
  print ("  Quit")
  GPIO.cleanup()

finally:
  GPIO.cleanup()
