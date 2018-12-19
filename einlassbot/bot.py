def run():
    import gc
    import network
    from urequests import get, post
    from machine import DAC, Pin
    # Enable garbage collector
    gc.enable()
    # Connect to WiFi
    nic = network.WLAN()
    if not nic.isconnected(): 
        nic.active(True)
        while not nic.active():
            pass
        nic.config(dhcp_hostname="Einlassbot")
        print("Connecting to WiFi")
        nic.connect('<YOUR_SSID>', '<YOUR_PASSWORD>')
        while not nic.isconnected():
            pass
    del nic
    del network
    gc.collect()
    
    last_update = 0
    print("Starting Bot")
    while True:
        try:
            req=get("https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates?timeout=60&offset="+str(last_update)+"&allowed_updates[]=message")
            if req.status_code != 200:
                continue
            result = req.json().get("result")
            req.close()
            del req
            if not result:
                del result
                continue
            try:
                # Only take the latest result, this will automatically debounce spam a little bit
                res = result.pop()
                del result
            except e:
                print(res)
            gc.collect()
            #####
            last_update = res["update_id"]+1
            if res["message"].get("text") == "Tür":
                cid = res["message"]["chat"]["id"]
                name = res["message"]["from"]["first_name"]
                #####
                req = get("https://api.telegram.org/bot<YOUR_BOT_TOKEN>/sendMessage?chat_id="+str(cid)+"&text=Kein+Problem+"+name)
                if req.status_code != 200:
                    continue
                req.close()
                del req
                del res
                del cid
                gc.collect()
                #####
                req = post("https://<YOUR_PYTHON_BACKEND>", data=bytes("Tür, "+name,'utf-8'))

                if req.status_code != 200:
                    continue
                tmp = req.content
                req.close()
                del req
                gc.collect()
                mDAC = DAC(Pin(25))
                mDAC.beep(1500, 600)
                with open("tmp.wav", "wb") as f:
                    f.write(tmp)
                    del f
                del tmp
                del name
                gc.collect()
                #####            
                mDAC.wavplay("tmp.wav")
                e = False
                while not e:
                    try:
                        mDAC.write(0)
                        mDAC.deinit()
                        e = True
                    except ValueError:
                        pass
                    gc.collect()
                del e
                del mDAC
                gc.collect()
        except Exception as e:
            with open("error.log", "a") as f:
                f.write(str(e))
                del f
