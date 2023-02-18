# tile_placer
Welcome to our untiled repo. Here you will find all of our code for the "Untiled" tile_placer PIE project. 

## What our application does:

Our project consists of a gantry and suction tool head system that can pick up tiles, flip them with a passive flipper, and place them back in their initial position. This allows us to create cool 2D animations with the tiles. 

The software we have here generates g code text files from scripts that correspond to flipping tiles to create different images. 

## Firmware

We used klipper as our 3D printing firmware to generate g-code. Klipper has a front end called Fluidd that we used to run the g code files we generated in python.

## To run: 

1.	Acquire a tile placing gantry 
2.	Acquire a Pi 4b + Ethernet cable + micro-usb
3.	Install klipper and fluidd onto pi using their tutorials
4.	Install Python 10
5.	Install an IDE like Pycharm or VSCode 
6.	Install numpy and PIL (Python Image Library) for Python 10
7.	Clone this repo 
8.	Change the image file paths in our generate_g_code.py to your local paths
9.	Run the Python scripts 
10.	Upload the text file to fluidd 
11.	Run it with the print command

## Additional information 
The FSM digram contains useful information about Pi setup, which is copied here: 

Starts as soon as script is run on Fluid (Klipper's front end that you access via http://{Pi IP Address} - Find IP address with IP scanner like Angry IP or by remoting into Pi and using default username and pw pi and raspberry, respectively. 

If you haven't booted into the Pi yet, you'll have to power it and hook it up to a monitor (if 4B using micro HDMI to HDMI and keyboard (USB A) and login that way - it should give you the IP in the summary info at the top of the terminal output once you log in. If not, run the command hostname -I
and see if there's output. 

If there's no output, then you're ethernet port isn't providing an IP address. Try a port from the cieling and not the walls (at least if in the ISIM room)

If there is output, that's your IP (10.xx.xx.xx)

Remote into the Pi using Putty which you can download from the Internet to your PC. All that's required is the IP and a connection to the same network as your Pi for you to remote in. (Make sure you're on the Olin wifi network or Ethernet connected)

First command that runs is INITIALIZE at the start of the gcode file we generate. It's a custom G Code command that automatically homes the toolhead.

