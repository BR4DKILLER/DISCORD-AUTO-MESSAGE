# required imported libaries (built-in) with the exception of requests, script made in python 3.7

import subprocess
import json
import time
import sys
import os 

try:
    import requests
except:
    print('Could not find requests module, installing - Please wait 5 Seconds.')
    time.sleep(5)
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'requests'])
    print('Successfully installed the requests module! - Please wait 5 Seconds.')
    time.sleep(5)

os.system('cls')

from datetime import datetime
from threading import Thread

# default settings for config file.

DefaultSettings = {'DiscordToken': '', 'Delay': 30, 'Message': '', 'Channels': []}
ConfigFinal = {'FinalConfig': {}}
DebugMode = False 

# functions, looks cleaner and makes life easier.

def ToggleDebug(Boolean):
    global DebugMode
    DebugMode = Boolean

def CVT(Token): # Check Valid Token
    response = requests.post('https://discord.com/api/v6/invite/538099980179865611', headers = {'authorization': Token})
    if response.status_code == 401:
        return 'Invalid'
    elif 'You need to verify your account in order to perform this action.' in str(response.content):
        return 'Phone Lock'
    else:
        return 'Valid'

def GetConfig(): # Returns old or new settings file
    DFS = False # "Default Set"

    try:
        Config = open('config.json', 'r')
        Config.close()
    except:
        Config = open('config.json', 'w')
        json.dump(DefaultSettings, Config, ensure_ascii=False, indent=4)
        DFS = True
        Config.close()

    try:
        ConfigFile = open('config.json', 'r')
        Config = ConfigFile.read()
        Config = Config.replace('\'','"')
        Config = json.loads(Config)
        ConfigFile.close()
    except Exception as e:
        print('A fatal error has occured loading the config, please reload the program or delete your config file.')
        print('Error: ' + str(e))

    return Config, DFS

def ChangeConfig(): # Changes the config
    CurrentConfig, DefaultSet = GetConfig()
    NewConfig = {'DiscordToken': '', 'Delay': 30, 'Message': '', 'Channels': []}
    Token = CurrentConfig['DiscordToken']

    # Token validation & checking
    if (Token != ''):
        CTI = input('Would you like to change your token (y/n): ')
        CT = False
        while (CTI != 'y' and CTI != 'n'):
            print('Invalid option.')
            CTI = input('Would you like to change your token (y/n): ')
    
        if (CTI == 'y'):
            Token = ''
            CT = True
        else:
            NewConfig['DiscordToken'] = Token

    if (CVT(Token) != 'Valid' or CT):
        ValidToken = False
        while (ValidToken != 'Valid'):
            Token = input('Please enter your discord Token: ')
            ValidToken = CVT(Token)
            if (ValidToken != 'Valid'):
                print('This discord Token is invalid.')
        NewConfig['DiscordToken'] = Token

    # Message file check

    NewMessage = input('Provide the name of the text file which your message is located in (e.g message.txt): ')
    ValidFile = False
    while (not ValidFile):
        try:
            MessageFile = open(NewMessage, 'r')
            MessageFile.close()
            ValidFile = True
        except:
            print('Invalid file, is it located in the same directory?')
            NewMessage = input('Provide the name of the text file which your message is located in (e.g message.txt): ')
    NewConfig['Message'] = NewMessage

    # Delay & Validation

    Delay = input('Please enter the auto message delay between messages (Seconds - 30 is recommended): ')
    while (Delay.isnumeric() == False):
        print('invalid delay')
        Delay = input('Please enter the auto message delay between messages (Seconds - 30 is recommended): ')
    NewConfig['Delay'] = int(Delay)

    # Channel IDs & Validation

    CIC = False
    while (not CIC):
        channel = input('Please enter a channel ID: ')
        while (channel.isnumeric() == False):
            print('Invalid channel ID')
            channel = input('Please enter a channel ID: ')
        NewConfig['Channels'].append(channel)

        continu = input('would you like to add another? (y/n): ')
        while (continu != 'y' and continu != 'n'):
            continu = input('would you like to add another? (y/n): ')
        if (continu == 'y'):
            CIC = False
        else:
            CIC = True

    # Making sure the config was updated correctly

    SuccessUPD = False

    try:
        Config = open('config.json', 'w')
        json.dump(NewConfig, Config, ensure_ascii=False, indent=4)
        Config.close()
        print('Successfully updated the config!')
        SuccessUPD = True
    except:
        print('an error occured while updating the config.')
    print('what')
    return SuccessUPD, NewConfig

def Clear():
    os.system('cls')

def ProvideOptions():
    print('Options:')
    print(' ')
    print('1. - Change/Setup Config')
    print('2. - Start the auto message with current config')
    print('3. - Toggle Debug Mode, only use this for debugging any errors that may occur. [WARNING: THIS TOGGLE IS NOT SAVED!]')
    print(' ')
    if(DebugMode):
        print('[DEBUG MODE ACTIVE]')
    elif(not DebugMode):
        print('[DEBUG MODE INACTIVE]')
    print(' ')
    option = input('Welcome to discord auto message! Please enter your chosen option to continue (1/2/3): ')
    while (option != '1' and option != '2' and option != '3'):
        print('Invalid option.')
        option = input('Welcome to discord auto message! Please enter your chosen option to continue (1/2/3): ')

    return option

def PrintAsciiART(Seconds):
    DebugText = ''
    if(DebugMode):
        DebugText = '[DEBUG MODE ACTIVE]'
    elif(not DebugMode):
        DebugText = ''
    print(r'''

               _    _ _______ ____    __  __ ______  _____ _____         _____ ______ 
          /\  | |  | |__   __/ __ \  |  \/  |  ____|/ ____/ ____|  /\   / ____|  ____|
         /  \ | |  | |  | | | |  | | | \  / | |__  | (___| (___   /  \ | |  __| |__   
        / /\ \| |  | |  | | | |  | | | |\/| |  __|  \___ \\___ \ / /\ \| | |_ |  __|  
       / ____ \ |__| |  | | | |__| | | |  | | |____ ____) |___) / ____ \ |__| | |____ 
      /_/    \_\____/   |_|  \____/  |_|  |_|______|_____/_____/_/    \_\_____|______|
                                                                                 
                                                                                       

     Close the program to stop the auto message, created by BR4DKILLER.     
     [Output Cleanup every {SCNDS} Seconds]
     {DEBUG_MODE}
    '''.format(SCNDS = str(Seconds), DEBUG_MODE = DebugText))

def RegularCleanup():
    TimeBetweenCleanup = ((ConfigFinal['FinalConfig']['Delay'] / 2) + 2)
    while True:
        time.sleep(TimeBetweenCleanup)
        Clear()
        PrintAsciiART(TimeBetweenCleanup)

def StartAutoMessage(ConfigDict):
    Clear()
    PrintAsciiART((ConfigFinal['FinalConfig']['Delay'] / 2) + 2)
    Thread(target=RegularCleanup).start()

    header = {'authorization': ConfigDict['DiscordToken']}
    payload = {'content': ConfigDict['Message']}
    while True:
        try:
            if(DebugMode):
                print('=========== Debug Mode ===========')
                print(' ')
            for Channel in ConfigDict['Channels']:
                if(DebugMode):
                    print('=========== Channel: ' + str(Channel) + ' ===========')
                    print(' ')
                    print('Headers: ' + json.dumps(header))
                    print('Message: ' + ConfigDict['Message'])
                    print(' ')
                    print(' ')
                elif(not DebugMode):               
                    request = requests.post(('https://discord.com/api/v9/channels/' + str(Channel) + '/messages'), data = payload, headers = header)
                    if request.status_code == 200:
                        print('succesfully sent message to channel ' + str(Channel) + ' at ' + str(datetime.now().strftime('%H:%M:%S')))
                    elif(DebugMode):
                        print('failed to send message to channel ' + str(Channel) + ' at ' + str(datetime.now().strftime('%H:%M:%S')) + ' - status code ' + str(request.status_code))
                        print('error message: ' + str(request.json()['message']))
                        print(' ')
            time.sleep(ConfigDict['Delay'])
        except KeyboardInterrupt:
            print('Program has been exited via KeyboardInterrupt.')
            sys.exit()
        except Exception as Error:
            print('An error occured while attempting to send message(s): ' + str(Error))

def StartSetup():
    Config, DefaultSet = GetConfig()
    InvalidFile = False
    global DebugMode

    if (not DefaultSet):
        Option = ProvideOptions()
        while (Option != '2'):
            if (Option == '1'):
                Success, NewConfig = ChangeConfig()
                Config = NewConfig
                Clear()
                Option = ProvideOptions()
            if (Option == '3'):
                ToggleDebug(not DebugMode)
                Clear()
                Option = ProvideOptions()        
        try:
            File = open(Config['Message'], 'r')
            Config['Message'] = File.read()
            File.close()
        except:
            Clear()
            print('Invalid message file! Please choose option 1. on relaunch or create a txt file under the name: ' + str(Config['Message']))
            InvalidFile = True
            os.system('pause')
        
        if (Option == '2' and not InvalidFile):
            ConfigFinal['FinalConfig'] = Config.copy()
            StartAutoMessage(Config)
    else:
        print('You appear to have no config file, to setup auto message you will need your discord token, channel ids and your message.')
        print(' ')
        ChangeConfig()
        Clear()

        Option = ProvideOptions()
        while (Option != '2'):
            if (Option == '1'):
                Success, NewConfig = ChangeConfig()
                Config = NewConfig
                Clear()
                Option = ProvideOptions()
            if (Option == '3'):
                ToggleDebug(not DebugMode)
                Clear()
                Option = ProvideOptions()
        try:
            File = open(Config['Message'], 'r')
            Config['Message'] = File.read()
            File.close()
        except:
            Clear()
            print('Invalid message file! Please choose option 1. on relaunch or create a txt file under the name: ' + str(Config['Message']))
            InvalidFile = True
            os.system('pause')

        if (Option == '2' and not InvalidFile):
            ConfigFinal['FinalConfig'] = Config.copy()
            StartAutoMessage(Config)

StartSetup()
