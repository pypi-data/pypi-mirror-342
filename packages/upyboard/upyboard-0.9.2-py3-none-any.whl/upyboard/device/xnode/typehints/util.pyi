import usys
import utime
import uos
import machine

from micropython import const


class ANSIEC:
    """
    ANSI Escape Codes for terminal text formatting.
    This class provides methods for setting foreground and background colors, as well as text attributes.
    It uses ANSI escape codes to format text in the terminal.
    """
    
    class FG:
        """
        ANSI escape codes for foreground colors.
        This class provides methods for setting foreground colors using ANSI escape codes.
        It includes standard colors, bright colors, and RGB color support.
        """
        
        BLACK = "\u001b[30m"
        RED = "\u001b[31m"
        GREEN = "\u001b[32m"
        YELLOW = "\u001b[33m"
        BLUE = "\u001b[34m"
        MAGENTA = "\u001b[35m"
        CYAN = "\u001b[36m"
        WHITE = "\u001b[37m"
        BRIGHT_BLACK= "\u001b[30;1m"
        BRIGHT_RED = "\u001b[31;1m"
        BRIGHT_GREEN = "\u001b[32;1m"
        BRIGHT_YELLOW = "\u001b[33;1m"
        BRIGHT_BLUE = "\u001b[34;1m"
        BRIGHT_MAGENTA = "\u001b[35;1m"
        BRIGHT_CYAN = "\u001b[36;1m"
        BRIGHT_WHITE = "\u001b[37;1m"
                
        @classmethod
        def rgb(cls, r:int, g:int, b:int) -> str:
            """
            Returns an ANSI escape code for RGB foreground color.
            :param r: Red component (0-255).
            :param g: Green component (0-255).
            :param b: Blue component (0-255).
            :return: An ANSI escape code for RGB foreground color.
            """

    class BG:
        """
        ANSI escape codes for background colors.
        This class provides methods for setting background colors using ANSI escape codes.
        It includes standard colors, bright colors, and RGB color support.
        """
        
        BLACK = "\u001b[40m"
        RED = "\u001b[41m"
        GREEN = "\u001b[42m"
        YELLOW = "\u001b[43m"
        BLUE = "\u001b[44m"
        MAGENTA = "\u001b[45m"
        CYAN = "\u001b[46m"
        WHITE = "\u001b[47m"
        BRIGHT_BLACK= "\u001b[40;1m"
        BRIGHT_RED = "\u001b[41;1m"
        BRIGHT_GREEN = "\u001b[42;1m"
        BRIGHT_YELLOW = "\u001b[43;1m"
        BRIGHT_BLUE = "\u001b[44;1m"
        BRIGHT_MAGENTA = "\u001b[45;1m"
        BRIGHT_CYAN = "\u001b[46;1m"
        BRIGHT_WHITE = "\u001b[47;1m"
                
        @classmethod
        def rgb(cls, r:int, g:int, b:int) -> str:
            """
            Returns an ANSI escape code for RGB background color.
            
            :param r: Red component (0-255).
            :param g: Green component (0-255).
            :param b: Blue component (0-255).
            :return: An ANSI escape code for RGB background color.
            """

    class OP:
        """
        A class for managing ANSI escape codes for font attributes and cursor positioning.
        This class provides methods to control font styles and cursor movement using ANSI escape codes.
        It supports actions such as resetting attributes, applying bold, underline, and reverse effects, clearing the screen or lines, and moving the cursor.
        """
        
        RESET = "\u001b[0m"
        BOLD = "\u001b[1m"
        UNDER_LINE = "\u001b[4m"
        REVERSE = "\u001b[7m"
        CLEAR = "\u001b[2J"
        CLEAR_LINE = "\u001b[2K"
        TOP = "\u001b[0;0H"

        @classmethod
        def up(cls, n:int) -> str:
            """
            Cursor up
            
            :param n: Number of lines to move up.
            :return: An ANSI escape code to move the cursor up.
            """

        @classmethod
        def down(cls, n:int) -> str:
            """
            Cursor down
            
            :param n: Number of lines to move down.
            :return: An ANSI escape code to move the cursor down.
            """
            
        @classmethod
        def right(cls, n:int) -> str:
            """
            Cursor right
            
            :param n: Number of columns to move right.
            :return: An ANSI escape code to move the cursor right.
            """

        @classmethod
        def left(cls, n:int) -> str:
            """
            Cursor left
            
            :param n: Number of columns to move left.
            :return: An ANSI escape code to move the cursor left.
            """
           
        @classmethod
        def next_line(cls, n:int) -> str:
            """
            Cursor down to next line
            
            :param n: Number of lines to move down.
            :return: An ANSI escape code to move the cursor down.
            """

        @classmethod
        def prev_line(cls, n:int) -> str:
            """
            Cursor up to previous line
            
            :param n: Number of lines to move up.
            :return: An ANSI escape code to move the cursor up.
            """
        
        @classmethod
        def to(cls, row:int, colum:int) -> str:
            """
            Move cursor to specified row and column.
            
            :param row: Row number (1-based).
            :param colum: Column number (1-based).
            :return: An ANSI escape code to move the cursor.
            """
            
            
def rand(size:int=4) -> int:
    """
    Generates a random number of the specified size in bytes.
    
    :param size: The size of the random number in bytes. Default is 4 bytes.
    :return: A random number of the specified size.
    """

def map(x:int|float, min_i:int|float, max_i:int|float, min_o:int|float, max_o:int|float) -> int|float:
    """
    Maps a value from one range to another.

    :param x: The value to be mapped.
    :param min_i: The minimum value of the input range.
    :param min_o: The minimum value of the output range.
    :return: The mapped value.
    """

def xrange(start:float, stop:float=None, step:float=None) -> any:
    """
    A generator function to create a range of floating point numbers.
    This is a replacement for the built-in range function for floating point numbers.   
    :param start: Starting value of the range.
    :param stop: Ending value of the range.
    :param step: Step size for the range.
    :return: A range object that generates floating point numbers.
    """
    
def intervalChecker(interval:int) -> callable:
    """
    Creates a function that checks if the specified interval has passed since the last call.
    
    :param interval: The interval in milliseconds.
    :return: A function that checks if the interval has passed.
    """

def WDT(timeout:int) -> machine.WDT:
    """
    Creates a watchdog timer (WDT) object with the specified timeout.
    
    :param timeout: The timeout in seconds.
    :return: A WDT object.
    """

def i2cdetect(bus:int=1, show:bool=False) -> list | None:
    """
    Detect I2C devices on the specified bus.
    
    :param bus: The I2C bus number. Default is 1.
    :param show: If True, print the detected devices. Default is False.
    :return: A list of detected I2C devices.
    """
 
 
class Slip:
    """
    SLIP (Serial Line Internet Protocol) encoder/decoder.
    This class provides methods to encode and decode SLIP packets.
    It uses the SLIP protocol to encapsulate data for transmission over serial lines.
    """

    END = b'\xC0'
    ESC = b'\xDB'
    ESC_END = b'\xDC'
    ESC_ESC = b'\xDD'

    @staticmethod
    def decode(chunk: bytes) -> list:
        """
        SLIP decoder. Returns a list of decoded byte strings.
        :param chunk: A byte string to decode.
        :return: A list of bytes.
        """
        
    @staticmethod
    def encode(payload: bytes) -> bytes:
        """
        SLIP encoder. Returns a byte string.
        :param payload: A byte string to encode.
        :return: A byte string.
        """
 
 
class ReplSerial:
    """
    A class to handle reading and writing to the REPL (Read-Eval-Print Loop) UART.
    This class provides methods to read and write data to the REPL UART with optional timeout.
    """

    def __init__(self, timeout:int|float|None=None):
        """
        Initializes the ReplSerial object with an optional timeout.
        
        :param timeout: The timeout in seconds. Default is None (no timeout).
        """
            
    @property
    def timeout(self) -> int|float|None:
        """
        Returns the current timeout value.
        
        :return: The timeout value in seconds.
        """

    @timeout.setter
    def timeout(self, n:int|float|None):
        """
        Sets the timeout value.
        
        :param n: The timeout value in seconds.
        """
        
    def read(self, size:int=1) -> bytes: 
        """
        Reads data from the REPL UART.
        
        :param size: The number of bytes to read. Default is 1 byte.
        :return: A byte string containing the read data.
        """
        
    def read_until(self, expected:bytes=b'\n', size:int|None=None) -> bytes:
        """
        Reads data from the REPL UART until the expected byte sequence is found or the specified size is reached.
        
        :param expected: The expected byte sequence to look for. Default is b'\n'.
        :param size: The maximum number of bytes to read. Default is None (no limit).
        :return: A byte string containing the read data.
        """
        
    def write(self, data:bytes) -> int:
        """
        Writes data to the REPL UART.
        
        :param data: The data to write as a byte string.
        :return: The number of bytes written.
        """