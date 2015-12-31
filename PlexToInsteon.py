import urllib.request
import urllib.parse
import urllib.error
import xml.etree.ElementTree as etree
import time
import configparser
import logging

config = configparser.ConfigParser()
config.sections()
config.read('c:\Scripts\PlexToInsteon\PlexToInsteon.ini')

# Set up logging
LogLevel = int(config['GENERAL']['LogLevel'])
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filemode='w', filename='c:\Scripts\PlexToInsteon\PlexToInsteon.log', level=LogLevel)

# General Variables
DelayTime = int(config['GENERAL']['DelayTime'])
LightingMode = "BRIGHT"

# Plex Variables            
PlexServerIP = config['PLEX']['PlexServerIP']
PlexServerPort = config['PLEX']['PlexServerPort']
PlexServerToken = config['PLEX']['PlexServerToken']
PlexServerURL = 'http://' + PlexServerIP + ':' + PlexServerPort + '/status/sessions?X-Plex-Token=' + PlexServerToken
PlexClient = config['PLEX']['PlexClient']

#ISY Variables
ISYServerIP = config['ISY']['ISYServerIP']
ISYServerPort = config['ISY']['ISYServerPort']
ISYMovieLightingSceneID = config['ISY']['MovieLightingSceneID']
ISYBrightLightingSceneID = config['ISY']['BrightLightingSceneID']
ISYUsername = config['ISY']['ISYUsername']
ISYPassword = config['ISY']['ISYPassword']
TurnOnMovieLightingModeURL = 'http://' + ISYServerIP + ':' + ISYServerPort + '/rest/nodes/' + ISYMovieLightingSceneID + '/cmd/DON'
TurnOnBrightLightingModeURL = 'http://' + ISYServerIP + ':' + ISYServerPort + '/rest/nodes/' + ISYBrightLightingSceneID + '/cmd/DON'

def SendRestCommand(RestURL):
    """ Take the established REST command and send to the ISY. Status of 200=Success. Will try 5 times and abort. """
    password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, RestURL, ISYUsername, ISYPassword)
    handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
    opener = urllib.request.build_opener(handler)
    for x in range(0,5):
        u = opener.open(RestURL)
        tree = etree.parse(u)
        root = tree.getroot()
        ISYStatus = tree.find('status')
        if ISYStatus.text == "200":
            logging.info('Command successfully sent')
            break
        else:
            logging.info('Command Failed: Try %s of 5 : %s', x+1, RestURL)
            time.sleep(1)

#---------------------------
# Open the Status_sessions.xml from the Plex Server
# Read the xml file looking for our desired Plex Client
# Print Status

logging.info('============================================')
logging.info('--------------------------------------------')
logging.info('Starting PlexToInsteon Script')
logging.info('--------------------------------------------')
logging.info('Plex Server : %s', PlexServerURL)
logging.info('Plex Client : %s', PlexClient)
logging.info('ISY Server : http://%s:%s', ISYServerIP, ISYServerPort)
logging.info('--------------------------------------------')

print('--------------------------------------------')
print('Starting PlexToInsteon Script')
print('No further output here. See logfile for more details.')
print('Press Ctrl-C to Stop Program')
print('--------------------------------------------')

while True:
    logging.debug('-----------------------------------------')
    try:
        u = urllib.request.urlopen(PlexServerURL)
        tree = etree.parse(u)
        root = tree.getroot()
        try:
            value = root.find(".//*[@title='" + PlexClient + "']")
            MovieStatus = value.attrib["state"]
        except AttributeError:
            MovieStatus = "stopped"
        logging.debug('Movie is %s', MovieStatus)
        if MovieStatus == "playing":
            if LightingMode == "BRIGHT":
                logging.info('Turning LIGHTS DOWN')
                SendRestCommand(TurnOnMovieLightingModeURL)
                LightingMode = "MOVIE"
            else:
                logging.debug('Lights Already DOWN')
        else:
            if LightingMode == "MOVIE":
                logging.info('Turning Lights UP')
                SendRestCommand(TurnOnBrightLightingModeURL)
                LightingMode = "BRIGHT"
            else:
                logging.debug('Lights Already UP')
        logging.debug('Waiting for next polling interval.')
        time.sleep(DelayTime)
    except urllib.error.URLError as e:
            print(e.reason)
            print ('Plex Server Not Responding... waiting 1 minute.')
            time.sleep(60)
