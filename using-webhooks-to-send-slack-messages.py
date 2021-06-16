import pandas as pd
from time import sleep
import requests
import json




def send_mass_slack(text, username, where):
    """This function will send a slack message with markup {text} to a group of channels {where}, 
    from a certain person or group {username}.  We use slack as a primary communication device and it is useful
    to send the same message to 200+ retail locations (slack channels) at once.   FYI:  Not all markup code works for mobile slack"""

    webhook_url = """you will need to administrator access to generate find the webhook URL"""
    
    # I use this input to make sure I don't accidentally send communication
    question = input("Are you sure you want to send?")
    
    if question == 'yes':
    
        for i in where:

            payload = {'channel': f'{i}',
                   'username': f'{username}',
                    'text': f"{text}",
                    'icon_emoji': 'alamo_fireworks_logo',
                    'mrkdwn': True,
                    'link_names':True,
                    'parse':None
                   
               }

            response = requests.post(
                webhook_url, data=json.dumps(payload),
                headers={'Content-Type': 'application/json'}
                )

            if response.status_code != 200:
                raise ValueError(
                    'Request to slack returned an error %s, the response is:\n%s'
                    % (response.status_code, response.text)
                )

            # sleep is not necessary, but its fun to hear the slack message alerts every second.
            sleep(1)
            
            # optional debugging
            print(i)