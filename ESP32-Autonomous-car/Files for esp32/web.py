# setting up wireless connection
def connect():
    import network
    import time
    import machine
    #wifi credentials
    ssid = "Redmi 9A"
    password =  "77777777"
 
    station = network.WLAN(network.STA_IF) # create station interface
    
    if station.isconnected() == True:
        print("Already connected")
        return
    station.active(True) # activate the interface
    if machine.reset_cause() != machine.SOFT_RESET:
        # configuration below MUST match your home router settings!!
        # CHECK DHCP RANGE OF YOUR ROUTER BEFORE ASSIGNING STATIC IP!!
        # station.ifconfig(('192.168.1.30', '255.255.255.0', '192.168.1.1', '8.8.8.8')) 
        station.ifconfig(('192.168.43.30', '255.255.255.0', '192.168.43.10', '8.8.8.8')) 
        #example: station.ifconfig(('192.168.180.180', '255.255.255.0', '192.168.180.1', '8.8.8.8'))
        #if you are using laptop as access point: station.ifconfig(('static ip you want to assign', 'subnet mask', 'host ip', 'host ip'))
    station.connect(ssid, password)
 
    while station.isconnected() == False:
        pass
    print("Connection successful")
    
    #turn on onboard led for 5 sec to notify the successful connection
    from machine import Pin
    p = Pin(2, Pin.OUT)
    print(station.ifconfig())
    p.on()
    time.sleep(5)
    p.off()