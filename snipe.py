import requests
import time
from colorama import Fore
from colorama import Style


class Snipe:
    def __init__(self, snipetoken, url,manufacturer_id,macos_category_id,ios_category_id,tvos_category_id,rate_limit,macos_fieldset_id,ios_fieldset_id,tvos_fieldset_id):
        self.url = url
        self._snipetoken = snipetoken
        self.manufacturer_id = manufacturer_id
        self.macos_category_id = macos_category_id
        self.ios_category_id = ios_category_id
        self.tvos_category_id = tvos_category_id
        self.rate_limit = rate_limit
        self.request_count = 0
        self.macos_fieldset_id = macos_fieldset_id
        self.ios_fieldset_id = ios_fieldset_id
        self.tvos_fieldset_id = tvos_fieldset_id

    @property
    def headers(self):
        return {
            "authorization": "Bearer " + self._snipetoken,
            "accept": "application/json",
            "content-type": "application/json",
        }    

    #@property
    def listHardware(self, serial):
        print('Requesting Snipe Harware list at url '+ self.url + "/hardware/byserial/")
        return self.snipeItRequest("GET", "/hardware/byserial/" + serial)

    def searchModel(self, model):
        print('Requesting Snipe Model list')
        result = self.snipeItRequest("GET", "/models", params = {"limit": "50", "offset": "0", "search": model, "sort": "created_at", "order": "asc"})
        #print(result)
        return result
    
    def createModel(self, model):

        payload = {
			"name": model,
            "category_id": self.macos_category_id,
            "manufacturer_id": self.manufacturer_id,
            "model_number": model,
            "fieldset_id": self.mac_os_fieldset_id
        }
        print('Creating Snipe Model with payload:', payload)
        results = self.snipeItRequest("POST", "/models", json = payload)
        #print('the server returned ', results);
        return results

    def createAsset(self, model, payload):
        print('Creating Snipe Hardware')
        print(payload);
        payload['status_id'] = 2
        payload['model_id'] = model
        
        asset = self.snipeItRequest("POST", "/hardware", json = payload).json()
        #print(asset)
        payload = {
            "serial": payload['serial']
        }
        return self.snipeItRequest("PATCH", "/hardware/" + str(asset['payload']['id']), json = payload)


    def assignAsset(self, user, asset_id):
        print('Assigning asset '+str(asset_id)+' to user '+user)
        
        payload = {
            "search": user,
            "limit": 2
        }
        response = self.snipeItRequest("GET", "/users", params = payload).json()

        if response['total'] == 0:
            return

        payload = {
            "assigned_user": response['rows'][0]['id'],
            "checkout_to_type": "user"
        }
        return self.snipeItRequest("POST", "/hardware/" + str(asset_id) + "/checkout", json = payload)

    def unasigneAsset(self, asset_id):
        print('Unassigning asset '+str(asset_id))
        return self.snipeItRequest("POST", "/hardware/" + str(asset_id) + "/checkin")

    def updateAsset(self, asset_id, payload):
        print('Updating asset '+str(asset_id))
        #print(payload)
        return self.snipeItRequest("PATCH", "/hardware/" + str(asset_id), json = payload)

    def createMobileModel(self, model):
        print('creating new mobile Model')
        payload = {
			"name": model,
            "category_id": self.ios_category_id,
            "manufacturer_id": self.manufacturer_id,
            "model_number": model,
            "fieldset_id": self.ios_fieldset_id
        }
        return self.snipeItRequest("POST", "/models", json = payload)
    def createAppleTvModel(self, model):
        print('creating new Apple Tv Model')
        payload = {
			"name": model,
            "category_id": self.tvos_category_id,
            "manufacturer_id": self.manufacturer_id,
            "model_number": model,
            "fieldset_id": self.tvos_fieldset_id
        }
        return self.snipeItRequest("POST", "/models", json = payload)

    def buildPayloadFromMosyle(self, payload):
        finalPayload = {
            #"asset_tag": asset,
            "name": payload['device_name'],
            "serial": payload['serial_number'],
            "_snipeit_bluetooth_mac_address_8": payload['bluetooth_mac_address']
        }
        
        #lets get the proper os name
        if(payload['os'] == "mac"):
            os = "MacOS"
            #cpu stuff is only supplied by MacOS
            finalPayload["_snipeit_cpu_family_7"]: payload['cpu_model']

            finalPayload["_snipeit_percent_disk_5"]: payload['percent_disk'] + " GB"
            finalPayload["_snipeit_available_disk_5"]: payload['available_disk'] + " GB"
        elif(payload['os'] == "ios"):
            os = "iOS"
            finalPayload["_snipeit_percent_disk_5"]: payload['percent_disk'] + " GB"
            finalPayload["_snipeit_available_disk_5"]: payload['available_disk'] + " GB"
        elif(payload['os'] == "tvos"):
            os = "tvos"
        else:
            os = "Not Known"
        
                
        finalPayload['_snipeit_operating_system_3'] = os
        
        #set os version
        finalPayload['_snipeit_operating_system_version_4'] = payload['osversion']
        
        #macaddress stuff
        wifiMac = payload['wifi_mac_address']
        eithernetMac = payload['ethernet_mac_address']
        
        #default to eithernet mac, if not, fall back to wifi mac. If neither, leave blank
        if(wifiMac != None and eithernetMac == None):
            finalPayload['_snipeit_mac_address_1'] = wifiMac
        elif(eithernetMac != None):
            finalPayload['_snipeit_mac_address_1'] = eithernetMac
        

        
        return finalPayload

    def snipeItRequest(self, type, url, params = None, json = None):
        self.request_count += 1
        if(self.request_count >= self.rate_limit):
            print(Fore.YELLOW + "Max requests per minute reached. Sleeping for 60 seconds")
            time.sleep(60) 
            self.request_count = 0
            print(Fore.GREEN + "Request count has been reset", "Continuing", Style.RESET_ALL)


        if(type == "GET"):
            print('Sending GET request to snipeit', url)
            return requests.get(self.url + url, headers = self.headers, params = params)
        elif(type == "POST"):
            print('Sending POST request to snipeit', url)
            return requests.post(self.url + url, headers = self.headers, json = json)
        elif(type == "PATCH"):
            print('Sending PATCH request to snipeit', url)
            return requests.patch(self.url + url, headers = self.headers, json = json)
        elif(type == "DELETE"):
            print('Sending DELETE request to snipeit', url)
            return requests.delete(self.url + url, headers = self.headers)
        else:
            print(Fore.RED+'Unknown request type'+Style.RESET_ALL)
            return None


#if __name__ == "__main__":
    #token_snipe = Snipe("Bearer = ".self.token)
    #test2 = token_snipe.list
    #print(test2.text)