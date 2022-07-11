This is a mirror from our internal GitLab

Forked from Dem972's [Python Mosyle2snipe](https://github.com/dem972/Mosyle_2snipe). It's a great bit of work and really helped me wrap my head around both APIs. Python is not my "native" language by any means, so pull requests and suggestions are always welcome.

Major changes are:
- The "all" type in the last version of the script did not work, and the Mosyle API requires you to do one device type at a time. Created a loop to do each device type in a single run.
- Snipe-IT Generated Assets ID's are synced back to the Mosyle device Asset Tags
- Cleaned up some of the settings and made manufacturer and devices categories variables for easier set up
- Added more comments in the code to explain what each block is doing
- Added lots of print messages to help the user understand what is currently happening. Honestly, too much information. Most of this was my debugging process and I plan to clean it up some more.
- If a device in Mosyle is a user enrolled device, the script assumes it is BYOB and does not add it into Snipe-IT
- Snipe-IT has a default API rate limit of 120 calls per minute. Added logic to pause the script when rate is hit. Limit is definable in settings.ini if you have changed the default limit
- It was our intention to get as much information about the device from Mosyle into Snipe-it. Because of this there are lots of custom fields currently hardcoded into this version of the script. Before running, take a look at buildPayloadFromMosyle in snipe.py and either change all attributes starting with "_snipeit_" to the matching database field in your Snipe-IT instance, or comment out the line.
- Optionally import model images from img.appledb.dev for apple devices


Before you start, make sure the following prerequisites are taken care of:

[System]
- Python 3
- The [Colorama Libary](https://pypi.org/project/colorama/) (pip3 install colorama)

[mosyle]
- You will need to generate a new token from the Mosyle Admin console: Organization--> Api integration
- Please note, with a recent update in Mosyle, an admin's username and password is now requrired in the call. You might want to create a new user for this.
- Also, just a fair warning. Be careful palying around with the Mosyle API. You can very much remove ADMIN rights from yourself.

[snipe-it]
- Snipe url is the full url of your Snipe-IT instance's api. EG: https://snipeit.example.com/api/v1 (do not add a slash at the end!)
- Generate the api key from the Snipe-IT seetings and for use in the configuration.ini
- Manufacturer Id should be set to the Apple Manufacturer entry in Snipe-IT. If you have not done this already, add apple as a manufacturer.
- If you have not done so already, you will need to create a category of devices for MacOS (we did "Computers"), iOS ( we did "Mobile/Tablets", and TVOS (we did "Media Players").
- The script will attempt to take device user assignments from Mosyle and "check out" the devices to the same user in Snipe-It. The two services should already have idential users for this to work. We have both Mosyle and Snipe-IT bound to our active directory/ldap for this reason.




[MosyleSnipeSync]
- Copy settings-example.ini to settings.ini
- Configure seetings.ini with the needed parameters.
- Each line has a comment above explaining the setting

[Questions/Comments/Concerns?]

You can best find me on the MacAdmin's slack as [Jake Garrison (Karpadiem)](https://macadmins.slack.com/team/U76DMNHT3)
