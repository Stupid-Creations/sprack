
# Sprack
Send and read messages on slack - Using a [Sprig](https://sprig.hackclub.com/)!

 ## Setup:
 - Sprack uses a version of MicroPython which is compiled with a graphics library for the st7789. You can find an installation of the library [here](https://github.com/russhughes/st7789_mpy/blob/master/firmware/RP2W/firmware.uf2).
 - Currently, Sprack needs a server running at all times for it to function. `recieve.py `needs to be running at all times for the micropython code to function. The code will most probably be altered in the future to run solely on a sprig using requests.
 - Sprack uses a user token to send and recieve messages. For this, you need to create a slack bot with a user token. [The Slack Bolt Guide](https://tools.slack.dev/bolt-python/getting-started/) has pretty good instructions for this. The bot needs `channels:read`, `chat:write`, `groups:history`, `groups:read` and `users:read` user token scopes
 
 ![enter image description here](https://hc-cdn.hel1.your-objectstorage.com/s/v3/11e41bc0504da50a50d9862fd13df3da79f4820e_image.png)
 - Install the bot and copy paste the user token into `recieve.py`, as well as adding your wifi ssid and password, and server IP and port into `sprig.py`
 - Run the server, flash the micropython installation on your sprig, and then run `sprig.py` on it!

---
 ## Limitations 
- Currently, Sprack only supports DMing and reading in private channels
- Sprack also needs the server running at all times, and the wifi ssid must be hard coded in 
## Using Sprack
- **Buttons**:
	- WASD for navigation
	- I for selection
	- J as backspace
	- L for shift when typing
	- K for exiting current menu
- **Menus**:
	- Channel Selection: ![h](https://hc-cdn.hel1.your-objectstorage.com/s/v3/aae845de11ea064936d7dea3a1cb3b52584bdd28_img-20250316-wa0038.jpg)
Sprack boots into the channel selection menu, which is exactly what it sounds like.
- **Messages:**![enter image description here](https://hc-cdn.hel1.your-objectstorage.com/s/v3/d8ce402dd58e8db72da06d6062b3e5e6623e70ec_img-20250316-wa0036.jpg)On selecting to read messages in a channel, Sprack switches to the message view, where you can view older messages by clicking A, and those newer by clicking D. In case messages are too long to be viewed on the screen, you can scroll up and down with W and S. You can also reveal threads by pressing I. 
- **Writing:**![enter image description here](https://hc-cdn.hel1.your-objectstorage.com/s/v3/34dc7dadb361b7adc01effa85ee1f375efae33f1_img-20250316-wa0034.jpg)navigate with WASD, Select with I, use L as the shift key and J for deleting characters.
## Stuff to be added
- Getting sprack to run fully on the sprig (Current version of this needs a lot of optimization because it eats a lot of RAM)
- Writing in threads: As much as i hate threads on slack, support for it will probably be added later :p
- Pings - might mess around with event subscriptions and see what I can do 
