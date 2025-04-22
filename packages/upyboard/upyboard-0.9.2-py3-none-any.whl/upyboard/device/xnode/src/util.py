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
             
            return "\u001b[38;2;{};{};{}m".format(r, g, b)

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
             
            return "\u001b[48;2;{};{};{}m".format(r, g, b)

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
            return "\u001b[{}A".format(n)

        @classmethod
        def down(cls, n:int) -> str:
            """
            Cursor down
            
            :param n: Number of lines to move down.
            :return: An ANSI escape code to move the cursor down.
            """
            
            return "\u001b[{}B".format(n)

        @classmethod
        def right(cls, n:int) -> str:
            """
            Cursor right
            
            :param n: Number of columns to move right.
            :return: An ANSI escape code to move the cursor right.
            """
            
            return "\u001b[{}C".format(n)

        @classmethod
        def left(cls, n:int) -> str:
            """
            Cursor left
            
            :param n: Number of columns to move left.
            :return: An ANSI escape code to move the cursor left.
            """
            
            return "\u001b[{}D".format(n)
        
        @classmethod
        def next_line(cls, n:int) -> str:
            """
            Cursor down to next line
            
            :param n: Number of lines to move down.
            :return: An ANSI escape code to move the cursor down.
            """
            
            return "\u001b[{}E".format(n)

        @classmethod
        def prev_line(cls, n:int) -> str:
            """
            Cursor up to previous line
            
            :param n: Number of lines to move up.
            :return: An ANSI escape code to move the cursor up.
            """
            
            return "\u001b[{}F".format(n)
                
        @classmethod
        def to(cls, row:int, colum:int) -> str:
            """
            Move cursor to specified row and column.
            
            :param row: Row number (1-based).
            :param colum: Column number (1-based).
            :return: An ANSI escape code to move the cursor.
            """
            
            return "\u001b[{};{}H".format(row, colum)

def rand(size:int=4) -> int:
    """
    Generates a random number of the specified size in bytes.
    
    :param size: The size of the random number in bytes. Default is 4 bytes.
    :return: A random number of the specified size.
    """
    
    return int.from_bytes(uos.urandom(size), "big")

def map(x:int|float, min_i:int|float, max_i:int|float, min_o:int|float, max_o:int|float) -> int|float:
    """
    Maps a value from one range to another.

    :param x: The value to be mapped.
    :param min_i: The minimum value of the input range.
    :param min_o: The minimum value of the output range.
    :return: The mapped value.
    """
    
    return (x - min_i) * (max_o - min_o) / (max_i - min_i) + min_o

def xrange(start:float, stop:float=None, step:float=None) -> any:
    """
    A generator function to create a range of floating point numbers.
    This is a replacement for the built-in range function for floating point numbers.   
    :param start: Starting value of the range.
    :param stop: Ending value of the range.
    :param step: Step size for the range.
    :return: A range object that generates floating point numbers.
    """
    
    if stop is None:
        stop = start
        start = 0.0

    if step is None:
        step = 1.0 if stop > start else -1.0

    if step == 0.0:
        raise ValueError("step must not be zero")
    if (stop - start) * step < 0.0:
        return  # empty range

    round_digits = len(f"{step}".split('.')[1])
    
    current = start
    epsilon = abs(step) / 10_000_000

    while (step > 0 and current < stop - epsilon) or (step < 0 and current > stop + epsilon):
        yield round(current, round_digits)
        current += step

def intervalChecker(interval:int) -> callable:
    """
    Creates a function that checks if the specified interval has passed since the last call.
    
    :param interval: The interval in milliseconds.
    :return: A function that checks if the interval has passed.
    """
    
    current_tick = utime.ticks_us()   
    
    def check_interval():
        nonlocal current_tick
        
        if utime.ticks_diff(utime.ticks_us(), current_tick) >= interval * 1000:
            current_tick = utime.ticks_us()
            return True
        return False
    
    return check_interval

def WDT(timeout:int) -> machine.WDT:
    """
    Creates a watchdog timer (WDT) object with the specified timeout.
    
    :param timeout: The timeout in seconds.
    :return: A WDT object.
    """
    
    return machine.WDT(0, timeout)

def i2cdetect(bus:int=1, show:bool=False) -> list | None:
    """
    Detect I2C devices on the specified bus.
    
    :param bus: The I2C bus number. Default is 1.
    :param show: If True, print the detected devices. Default is False.
    :return: A list of detected I2C devices.
    """
    
    i2c = machine.I2C(bus)
    devices = i2c.scan()

    if not show:
        return devices
    else:
        print("     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f")
        for i in range(0, 8):
            print("{:02x}:".format(i*16), end='')
            for j in range(0, 16):
                address = i * 16 + j
                if address in devices:
                    print(ANSIEC.FG.BRIGHT_YELLOW + " {:02x}".format(address) + ANSIEC.OP.RESET, end='')
                else:
                    print(" --", end='')
            print()


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
    
    __decode_state = {'started': False, 'escaped': False, 'data': bytearray(), 'pending_end': False, 'junk': bytearray()}
    
    @staticmethod
    def decode(chunk: bytes) -> list:
        """
        SLIP decoder. Returns a list of decoded byte strings.
        :param chunk: A byte string to decode.
        :return: A list of bytes.
        """
        result = []
        data = Slip.__decode_state['data']
        junk = Slip.__decode_state['junk']
        started = Slip.__decode_state['started']
        escaped = Slip.__decode_state['escaped']
        pending_end = Slip.__decode_state['pending_end']

        for char in chunk:
            if escaped:
                if char == ord(Slip.ESC_END):
                    data.append(ord(Slip.END))
                elif char == ord(Slip.ESC_ESC):
                    data.append(ord(Slip.ESC))
                else:
                    data.clear()
                    started = False
                    pending_end = False
                    return []
                escaped = False
            elif char == ord(Slip.ESC):
                escaped = True
            elif char == ord(Slip.END):
                if pending_end:
                    if started:
                        result.append(bytes(data))
                        data.clear()
                    else:
                        junk.clear()
                    started = True
                    pending_end = False
                elif started:
                    result.append(bytes(data))
                    data.clear()
                    started = False
                    pending_end = True
                else:
                    started = True
                    pending_end = True
            else:
                if pending_end:
                    started = True
                    data.append(char)
                    pending_end = False
                elif started:
                    data.append(char)
                else:
                    junk.append(char)

        Slip.__decode_state['started'] = started
        Slip.__decode_state['escaped'] = escaped
        Slip.__decode_state['pending_end'] = pending_end

        return result
    
    @staticmethod
    def encode(payload: bytes) -> bytes:
        """
        SLIP encoder. Returns a byte string.
        :param payload: A byte string to encode.
        :return: A byte string.
        """
        return Slip.END + payload.replace(Slip.ESC, Slip.ESC + Slip.ESC_ESC).replace(Slip.END, Slip.ESC + Slip.ESC_END) + Slip.END


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
        
        self.timeout = timeout
    
    @property
    def timeout(self) -> int|float|None:
        """
        Returns the current timeout value.
        
        :return: The timeout value in seconds.
        """
        
        return self.__timeout
    
    @timeout.setter
    def timeout(self, n:int|float|None):
        """
        Sets the timeout value.
        
        :param n: The timeout value in seconds.
        """
        
        self.__timeout = n
    
    def read(self, size:int=1) -> bytes: 
        """
        Reads data from the REPL UART.
        
        :param size: The number of bytes to read. Default is 1 byte.
        :return: A byte string containing the read data.
        """
        
        if self.timeout is None:
            assert size > 0, "size must be greater than 0"
            return usys.stdin.buffer.read(size)
        elif self.timeout is not None and self.timeout == 0:
            return usys.stdin.buffer.read(-1)
        elif self.timeout is not None and self.timeout > 0:
            rx_buffer = b''
            t0 = utime.ticks_ms()
            while utime.ticks_diff(utime.ticks_ms(), t0) / 1000 < self.timeout:
                b = usys.stdin.buffer.read(-1)
                if b:
                    rx_buffer += b
                    if len(rx_buffer) >= size:
                        break
            return rx_buffer
        
    def read_until(self, expected:bytes=b'\n', size:int|None=None) -> bytes:
        """
        Reads data from the REPL UART until the expected byte sequence is found or the specified size is reached.
        
        :param expected: The expected byte sequence to look for. Default is b'\n'.
        :param size: The maximum number of bytes to read. Default is None (no limit).
        :return: A byte string containing the read data.
        """
        
        rx_buffer = bytearray()
        expected_len = len(expected)

        t0 = utime.ticks_ms() if (self.timeout is not None and self.timeout > 0) else None 
        while True:
            if t0 is not None:
                ellipsis = utime.ticks_diff(utime.ticks_ms(), t0) / 1000
                if ellipsis >= self.timeout:
                    break  # Timeout

            try:
                b = usys.stdin.buffer.read(-1)
                if self.timeout is not None and self.timeout == 0:
                    return b if b else b''
            except Exception as e:
                return
                
            if not b: 
                continue

            rx_buffer.extend(b)

            if size is not None and len(rx_buffer) >= size:
                return bytes(rx_buffer[:size])

            if len(rx_buffer) >= expected_len and rx_buffer[-expected_len:] == expected:
                return bytes(rx_buffer)
        
        return bytes(rx_buffer) # Timeout occurred, return what's read so far
                    
    def write(self, data:bytes) -> int:
        """
        Writes data to the REPL UART.
        
        :param data: The data to write as a byte string.
        :return: The number of bytes written.
        """
        
        assert isinstance(data, bytes), "data must be a byte type"
        
        ret = usys.stdout.write(data)
                
        return ret
