# Overview
This is the `README.md` for the <a href="https://github.com/MPvI/Einlassbot/blob/master/assets/action.mp4">_Einlassbot_</a>. 

<img src="https://github.com/MPvI/Einlassbot/blob/master/assets/front.jpg" width=250/>

<img src="https://github.com/MPvI/Einlassbot/blob/master/assets/top.jpg" width=250/>

<img src="https://github.com/MPvI/Einlassbot/blob/master/assets/back.jpg" width=250/>

Thanks to everyone who wrote a piece of software or designed a piece of hardware used in this project.

## Purpose
The purpose of the _Einlassbot_ is to announce a users name if he writes **Tür** (German for **Door**) into a specific Telegram group. It can therefore be considered as a replacement for a doorbell. 

You may call this an overengineered solution for a doorbell. However, it was a present for Xmas, build in a couple of days and brought a lot of joy.
## Components
The system is made up of 3 components:
- A microcontroller, running the bot logic and playing audio
- A Telegram Bot, sitting in a Telegram group
- A backend providing TTS functionality
## How can I use this?
To use this you need at least your own Telegram Bot. Adapt `bot.py` to connect to your WiFi, use the correct token for your bot and query your flask endpoint. You should also make sure to adapt the `docker-compose.yml` so that the container is reachable for you.

- Create Telegram Bot and add to group
- Flash ESP32 with LoBo MicroPython
- Wire up the circuit
- Transfer the modified `bot.py` and `main.py` with `ampy` to the ESP32
- Run docker container
- Reboot ESP32 and enjoy (hopefully) ;-)

# Microcontroller - `/einlassbot`
- [ESP32 from AzDelivery](https://www.az-delivery.de/products/esp32-developmentboard) the actual hardware
- [MicroPython LoBo](https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo) is a really awesome micropython port for ESP32
- [esptool](https://github.com/espressif/esptool) to flash the ESP32
- [ampy](https://github.com/adafruit/ampy) transfer files from and to the microcontroller
- [Kemo M031N Amplifier](https://www.kemo-electronic.de/en/Light-Sound/Amplifier-Splitter/Modules/M031N-Amplifier-3-5-W-universal.php) getting some power to that speaker
- [Aukru 5V 3A Power Supply](https://www.amazon.de/dp/B01566WOAG/ref=cm_sw_r_tw_dp_U_x_41sgCb798FKM6) making it run
- 200-10k Ohm logarithmic potentiometer for controlling volume
- 4W, 105dB @ 1 kHz / 1 Volt, 4 Ohm speaker

### Circuit
Just connect everything as described for the [Kemo M031N example circuit](https://www.kemo-electronic.de/datasheets/m031n_24032om.pdf). Input to the potentiometer comes from one of the DAC pins, I use `Pin(25)`. Supply voltage comes from the 5V pin of the ESP. Make sure your power supply can take the load. I use a _probably total overkill_ 3A Raspberry Pi power supply. If you experience trouble with your power supply and are capable of reading the German language you may try [this](https://arduino-hannover.de/2018/07/25/die-tuecken-der-esp32-stromversorgung/).

### Possible Improvements
- Higher supply voltage (12V) for amp so it can actually reach 3.5W
- Use microcontroller with more than 100kB of RAM (less pain)
- First MicroPython project, probably lots of code improvements
- Stop using flask dev server (bad!)
- Audio quality?

# Telegram Bot
Make sure the bot is part of your specific group.
The bot needs to receive all messages.
Command Botfather to set privacy mode to `Disable` with `/setprivacy`.
Longpolling Telegram BotAPI `get_updates()` from microcontroller.

# Backend - `/py-web-service`
- [Docker](https://www.docker.com/) container based on `base/archlinux`
- [Docker Compose](https://docs.docker.com/compose/) to build and run the container 
- [Flask](http://flask.pocoo.org/) as framework for the endpoint
- [gTTS](https://pypi.org/project/gTTS/) performing TTS with `translate.google.com`
- [pydub](https://pypi.org/project/pydub/) converting mp3 to wav
- [SoX](http://sox.sourceforge.net/) converting audio to 8bit PCM wav file

### Backend Magic - not part of the project

- [nginx-proxy](https://github.com/jwilder/nginx-proxy) automatic reverse proxy magic for containers
- [docker-letsencrypt-nginx-proxy-companion](https://github.com/JrCs/docker-letsencrypt-nginx-proxy-companion) proxy magic + free TLS = magic²
