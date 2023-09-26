# FRED assembly and installation instructions
A simple RPi retrofit device which mitigates emissions from fumehoods in research labs.

For a more detailed motivation and description, see [my project post on FRED](https://nrmkirkwood.github.io/projects/fumehoodfred/).

This Readme details how to assemble and install a 'basic' FRED with buzzers only (no Teams posting). For details on installing the 'advanced' FRED code onto a RPi running Python with WiFi and Teams posts enabled, contact me.

# Assembling a 'basic' FRED

## Required equipment

You will need (AUD price in brackets links to suggested supplier):

- Raspberry Pi Pico ([$5.75](https://core-electronics.com.au/raspberry-pi-pico.html))
- Power supply + cable ([supply $1.95](https://www.ebay.com.au/itm/284385278195), [cable $2.63](https://www.ebay.com.au/itm/384493783379))
- Reward piezo buzzer 3V ([$2.90](https://core-electronics.com.au/piezo-buzzer-ps1240.html))
- Alarm buzzer 3-5V ([$0.74](https://core-electronics.com.au/piezo-buzzer.html))
- Door Switch Sensor ([$3.85](https://www.ebay.com.au/itm/154538574997))
- Code (Python) (from this repo)
- 3D printed case and lid (from this repo: [fhf-case](https://github.com/nrmkirkwood/FumeHoodFred/blob/images/fhf-case.stl) & [fhf-lid](https://github.com/nrmkirkwood/FumeHoodFred/blob/images/fhf-lid.stl))

You will also need:

- 3D printer (or make own case)
- Soldering iron & solder (or, buy Pico with soldered headers, and use M-F jumper cables)
- Velcro strips (M+F) or double sided tape/strips
- A fume hood to put it in!

## Building FRED
Solder the alarm buzzer, reward buzzer, and Reed switch onto the Pico pins as indicated. The case provided assumes you solder the buzzers directly onto the Pico with no wires:

![Alt text](https://github.com/nrmkirkwood/FumeHoodFred/blob/main/images/fhf-1.jpg?raw=true "Title")

The finished Pico should look like this:

![Alt text](https://github.com/nrmkirkwood/FumeHoodFred/blob/main/images/fhf-2.jpg?raw=true "Title")

3D print the [case](https://github.com/nrmkirkwood/FumeHoodFred/blob/images/fhf-case.stl) & [lid](https://github.com/nrmkirkwood/FumeHoodFred/blob/images/fhf-lid.stl). The Pico should fit snugly into the case. Use doubled sided tape to secure the wired Reed switch onto the top of case as pictured:

![Alt text](https://github.com/nrmkirkwood/FumeHoodFred/blob/main/images/fhf-3.jpg?raw=true "Title")

Snap the lid on (it's a snap-fit so may require a little force). If desired draw a smiley face:

![Alt text](https://github.com/nrmkirkwood/FumeHoodFred/blob/main/images/fhf-4.jpg?raw=true "Title")

At this stage, plug the RPi Pico into your computer and follow instructions to [install ThonnyIDE](https://projects.raspberrypi.org/en/projects/getting-started-with-the-pico/2), [setup MicroPython firmware](https://projects.raspberrypi.org/en/projects/getting-started-with-the-pico/3) and [use the shell to run code off the Pico](https://projects.raspberrypi.org/en/projects/getting-started-with-the-pico/4).

Load the [fhf-basic.py](https://github.com/nrmkirkwood/FumeHoodFred/blob/images/fhf-basic.py) file in Thonny and [save to your Pico as main.py](https://projects.raspberrypi.org/en/projects/getting-started-with-the-pico/9). 

Now when you plug your Pico (now a FRED) into power, the onboard green LED should turn on. Move the Reed switches together and the LED should turn off and the reward buzzer should play a chromatic riff. If you leave the FRED on for 1 hour with the Reed switches apart, the alarm buzzer will sound. (You can test this for shorter time intervals by editing the main.py code and setting the alarm time to a few seconds).

If all works well the FRED is ready to install.

# Installing FRED into a fume hood

First attach Velcro or doubled-sided tape to the backside of the FRED case:

![Alt text](https://github.com/nrmkirkwood/FumeHoodFred/blob/main/images/fhf-5.jpg?raw=true "Title")

To attached the FRED into the fume hood, pick a spot where the FRED can be close enough to the fume hood sash that there a < 1 cm gap between the Reed switches with the non-wired Reed switch on the sash *when the fume hood is fully closed*. Check this before sticking anything! Using Velcro stickers is handy as the FRED can be moved a bit after installation to optimise position. Some photos below show installation methods that work in our lab:

Inside the fumehood, with unwired Reed switch on the inside of the sash near bottom:

![Alt text](https://github.com/nrmkirkwood/FumeHoodFred/blob/main/images/fhf-8.jpg?raw=true "Title")

Outside the fumehood (recommended if possible), with unwired Reed switch on the hand-grip of the sash:

![Alt text](https://github.com/nrmkirkwood/FumeHoodFred/blob/main/images/fhf-9.jpg?raw=true "Title")