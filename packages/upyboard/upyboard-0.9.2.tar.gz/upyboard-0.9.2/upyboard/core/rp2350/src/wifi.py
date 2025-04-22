import utime
import network

class Wifi:
    """
    A class to manage WiFi connections on the Pico 2 w.
    """

    _if = network.WLAN(network.STA_IF)
    _if.active(True)

    @staticmethod
    def show_ap() -> tuple:      
        """
        Show available WiFi networks.
        
        :return: tuple of available SSIDs
        """  
        
        if Wifi._if.isconnected():
            Wifi._if.disconnect()
            
        networks = Wifi._if.scan()
        return tuple(set([network[0].decode() for network in networks if network[0] != b'']))
    
    @staticmethod
    def connect_ap(ssid:str, password:str) -> str:
        """
        Connect to a WiFi network.
        
        :param ssid: SSID of the WiFi network
        :param password: Password of the WiFi network
        :return: IP address if connected, None otherwise
        """        
        
        if Wifi._if.isconnected():
            return Wifi._if.ipconfig('addr4')[0]
        
        Wifi._if.connect(ssid, password)
        for _ in range(100):
            if Wifi._if.isconnected():
                break
            utime.sleep_ms(100)

        return Wifi._if.ipconfig('addr4')[0] if Wifi._if.isconnected() else None

    @staticmethod
    def disconnect_ap():       
        """
        Disconnect from the current WiFi network.
        """
        
        if Wifi._if.isconnected():
            Wifi._if.disconnect()
    
    @staticmethod
    def ip() -> str:      
        """
        Get the IP address of the connected WiFi network.
        
        :return: IP address if connected, None otherwise
        """  
        if Wifi._if.isconnected():
            ip = Wifi._if.ifconfig()[0]
            return ip