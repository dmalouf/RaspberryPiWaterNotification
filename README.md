# RaspberryPiWaterNotification
Project that uses a Raspberry Pi and LM393 moisture sensor (plus 'blade') to notify the presence of water.

This project is under the 'unlicense' license, as given to GitHub users when creating a new project that is to be public domain from inception.

The corresponding blog post is here: https://dissectionbydavid.wordpress.com/2022/10/01/raspberry-pi-water-sensor-alert-system/

This project requires:
* Python 3 (probably at least 3.6 or 3.7 - have not tested how 'low' in the 3 line one can use)
* The rpi.gpio package
  * as most Raspberry Pis are running a Debian variant, this is satisfied by: `sudo apt install python3-rpi.gpio`
* If using the SendGrid and/or Twillio notifications, their respective libraries are needed: `pip install sendgrid twillio`
* Also if using SendGrid or Twillio, be sure to get the needed keys and values into _your_ Pi's environment
  * e.g. copy the .env.sample to .env but populate it with _your_ values :: then `source` the file either in an OS file or at least source-ing before running:
     ```
     source .env; python3 main.py
     ```
