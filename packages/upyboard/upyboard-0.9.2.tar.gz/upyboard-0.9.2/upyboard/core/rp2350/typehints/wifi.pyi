import utime
import network

class Wifi:
    """
    A class to manage WiFi connections on the Pico 2 w.
    """

    @staticmethod
    def show_ap() -> tuple:      
        """
        Show available WiFi networks.
        
        :return: tuple of available SSIDs
        """  
        
    @staticmethod
    def connect_ap(ssid:str, password:str) -> str:
        """
        Connect to a WiFi network.
        
        :param ssid: SSID of the WiFi network
        :param password: Password of the WiFi network
        :return: IP address if connected, None otherwise
        """        
        
    @staticmethod
    def disconnect_ap():       
        """
        Disconnect from the current WiFi network.
        """
            
    @staticmethod
    def ip() -> str:      
        """
        Get the IP address of the connected WiFi network.
        
        :return: IP address if connected, None otherwise
        """  
