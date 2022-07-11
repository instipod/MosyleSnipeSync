#this file can be run to update your Snipe-IT models without interacting with Mosyle.

import base64
from tracemalloc import stop
import requests
import json
import datetime
import configparser
import colorama
from sys import exit

from mosyle import Mosyle
from snipe import Snipe
from colorama import Fore
from colorama import Style
from operator import mod

modelNumber = "iPad11,2";

# Converts datetim/e to timestamp for Mosyle
ts = datetime.datetime.now().timestamp() - 200

# Set some Variables from the settings.conf:
config = configparser.ConfigParser()
config.read('settings.ini')

# This is the address, cname, or FQDN for your snipe-it instance.
snipe_url = config['snipe-it']['url']
apiKey = config['snipe-it']['apiKey']
defaultStatus = config['snipe-it']['defaultStatus']
apple_manufacturer_id = config['snipe-it']['manufacturer_id']
macos_category_id = config['snipe-it']['macos_category_id']
ios_category_id =  config['snipe-it']['ios_category_id']
tvos_category_id =  config['snipe-it']['tvos_category_id']
macos_fieldset_id = config['snipe-it']['macos_fieldset_id']
ios_fieldset_id = config['snipe-it']['ios_fieldset_id']
tvos_fieldset_id = config['snipe-it']['tvos_fieldset_id']
deviceTypes = config['mosyle']['deviceTypes'].split(',')

snipe_rate_limit = int(config['snipe-it']['rate_limit'])

apple_image_check = config['snipe-it'].getboolean('apple_image_check')

#setup the snipe-it api
snipe = Snipe(apiKey,snipe_url,apple_manufacturer_id,macos_category_id,ios_category_id,tvos_category_id,snipe_rate_limit, macos_fieldset_id, ios_fieldset_id, tvos_fieldset_id,apple_image_check)


#get all models
models = snipe.listAllModels().json()
print(models);
#loop through each model
for model in models['rows']:
    #is the model's manufacturer Apple?
    print('Processing model: ' + str(model['id']), model["model_number"])
    print("Is the model's manufacturer Apple?", "checking manufacture id " + str(model['manufacturer']['id']) +" against known apple manufacturer id: "+ str(apple_manufacturer_id))
    if int(model['manufacturer']['id']) == int(apple_manufacturer_id):
        #yes!
        print(Fore.GREEN, "Yes! Checking for photo!", Style.RESET_ALL);
        #Does it need a picture?
        if model['image'] == None:
            print("No photo. Dowloading photos")
            imageResponse = snipe.getImageForModel(model["model_number"]);
            if imageResponse != False:
                print("Photo Downloaded")
                snipe.setImageForModel(model["id"],imageResponse.content)
                payload = {
                    "image": imageResponse
                }
            
                snipe.updateModel(str(model['id']), payload)
            else:
                print("no photo found, moving on")
        else:
            print("picture already set. Skipping")
    else:
        print(Fore.YELLOW,'model is not apple. Skip.',Style.RESET_ALL)

