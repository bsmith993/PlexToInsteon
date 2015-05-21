# PlexToInsteon
Small Python script that monitors a Plex Server to determine if a specific Plex Client is playing a movie, and will turn Insteon lights up or down based on playback status. 

GOAL: When you start watching a movie, dim your Insteon lights to a movie scene you have created. When you pause or stop the movie, return the movie lighting to a normal lighting mode.

REQUIREMENTS: 
-Obiviously a Plex Media Server and Plex Client
-Insteon contolled lighting, with a movie mode scene and a NON  movie mode scene. Movie mode intended to be dim, non movie mode intended to be bright.
-ISY-994i controller, using the REST commands to trigger scenes.
-Python 3.4

Here's the plan... read the xml file from the Plex Server to see if a user defined Plex Home Theater Client is playing a movie. If it is, set the lights to movie mode. When it pauses or stops, bring em up.

NOTES: 
### For error checking on sending commands via the ISY. If the REST command does not return a success code, will try only 5 times. 
### I chose NOT to do any current lighting state checks and continuous monitoring and setting of lighting mode. I only want it to send when the movie state changes. This way if you are watching a movie and want to manually override the lighting mode you aren't fighting with the script. You turn it up, it turns it back down. 

The PlexToInsteon.ini file contains your variables. You must use your Plex Client ID as shown in the XML file. Make sure you open your particular Plex installation's xml file in a browser by accessing the URL of:

  http://YOUR_SERVER/status/sessions
  
Start playing a movie on the client you want to monitor. Look near the bottom of the file for your "Player" xml data. The xml attribute of "title" is what you will want to use here.

Same thing for your Insteon scene commands. YOu will need to locate your scene ID's inside your ISY admin console. It is the 5 digit string usually.


INSTALLATION:

This script will run with the python launcher. Configure the INI file with your prefs. Then you can run it manually and just leave it be. Or run it as a scheduled task. Doing so as a scheduled task might have problems with where the log files and INI file comes from. I still have work to do on that.