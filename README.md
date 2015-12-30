# PlexToInsteon
Small Python script that monitors a Plex Server to determine if a specific Plex Client is playing a movie, and will turn Insteon lights up or down based on playback status. 

****** This is very early development. *******

GOAL: When you start watching a movie, dim your Insteon lights to a movie scene you have created. When you pause or stop the movie, return the movie lighting to a normal lighting mode.

-------------------------------------------------
REQUIREMENTS: 
-Obiviously a Plex Media Server and Plex Client
-Insteon ISY-994i contolled lighting, with a movie mode scene and a NON  movie mode scene. Movie mode intended to be dim, non movie mode intended to be bright.

-------------------------------------------------
INSTALLATION:
-You must have Python installed. (Google it if you need help) This is written for Python 3.4
-There is no installation for the script itself. Simply place the files in a folder (example: c:\scripts\PlexToInsteon) and then schedule a job using the windows task scheduler (or however else you'd like to trigger it). 
-Modify the ini file to your variables and fire up the script. 
-The script will continuously run. It is low memory and CPU usage so I just let it be.
-The script will fail right now if the Plex Server is stopped. So I have to restart it sometimes.

Scheduled Job example for a task to run at every startup:

Program: c:\Python34\pyw
Arguments: c:\Scripts\PlexToInsteon\PlexToInsteon.py
Start In: c:\Scripts\PlexToInsteon

-------------------------------------------------
USAGE
Here's the plan... read the xml file from the Plex Server to see if a user defined Plex Home Theater Client is playing a movie. If it is, set the lights to movie mode. When it pauses or stops, bring em up.

-------------------------------------------------
NOTES: 
### For error checking on sending commands via the ISY. If the REST command does not return a success code, will try only 5 times. 
### I chose NOT to do any current lighting state checks and continuous monitoring and setting of lighting mode. I only want it to send when the movie state changes. This way if you are watching a movie and want to manually override the lighting mode you aren't fighting with the script. You turn it up, it turns it back down. 

-------------------------------------------------
UPDATES:
5/18/2015:
Script is now functioning to read the /status/sessions xml file from a locally hosted Plex Server. Changes in movie playing state is functioning properly.

The PlexToInsteon.ini file contains your variables. You must use your Plex Client ID as shown in the devices list on your server.

12/30/2015:
Updated Plex authentication to use PlexToken. This is needed because the standard connections didn't work once turning your plex server into a plex family/home setup.

-------------------------------------------------
COMING SOON:

Need some error checking on the Plex status url.

Convert to service- something that can show it is running in the systray or the like.

Convert from triggering scenes in the ISY to setting a state variable instead. Reason being. There are times when you do NOT want the lights to be modified while watching a movie. For instance... having a dinner/movie night with the kids, hit play, room goes dark, can't see food. So the intent is to have a state variable, then use a program to watch for the state changes. It might be a lot simpler that way actually. Let the ISY do the work instead of the script.
