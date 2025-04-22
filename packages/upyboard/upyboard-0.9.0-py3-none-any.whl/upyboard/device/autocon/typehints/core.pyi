import utime
import ustruct
import _thread

import machine
import micropython
import neopixel

        
class Led():
    """
    A class to control the built-in LED on the AutoCON.
    """
    
    def __init__(self):
        """
        Initialize the LED object.
        """
    
    def on(self):
        """
        Turn on the LED.
        """
                
    def off(self):
        """
        Turn off the LED.
        """
        
    def toggle(self):
        """
        Toggle the LED state.
        """
            
    def state(self):
        """
        Get the current state of the LED.
        
        :return: True if LED is on, False if off.
        """


class Illuminance:
    """
    A class to read illuminance data from the BH1750 sensor.
    """
    
    BH1750_ADDR = micropython.const(0x23)
    
    POWER_ON = micropython.const(b'\x01')
    POWER_OFF = micropython.const(b'\x00')
    RESET = micropython.const(b'\x07')
    
    CONTINUOUS_HIGH_RES = micropython.const(0x10)
    ONE_TIME_HIGH_RES = micropython.const(0x20)
    
    def __init__(self, adjusted_lux=0.75):
        """
        Initialize the BH1750 sensor.
        
        :param adjusted_lux: Adjusted lux value (default is 0.75).
        """
        
    def read(self, continuous=True):
        """
        Read illuminance data from the BH1750 sensor.
        
        :param continuous: If True, read in continuous mode; otherwise, read in one-time mode.
        :return: Illuminance value in lux. 
        """

        
class Tphg:
    """
    A class to read temperature, pressure, humidity, and gas data from the BME688 sensor.
    """
    
    BME688_ADDR = micropython.const(0x77)
    
    FORCED_MODE = micropython.const(0x01)
    SLEEP_MODE = micropython.const(0x00)
        

    def __init__(self, temp_weighting=0.10,  pressure_weighting=0.05, humi_weighting=0.20, gas_weighting=0.65, gas_ema_alpha=0.1, temp_baseline=23.0,  pressure_baseline=1013.25, humi_baseline=45.0, gas_baseline=450_000):
        """
        Initialize the BME688 sensor.
        
        :param temp_weighting: Weighting for temperature (default is 0.10).
        :param pressure_weighting: Weighting for pressure (default is 0.05).
        :param humi_weighting: Weighting for humidity (default is 0.20).
        :param gas_weighting: Weighting for gas (default is 0.65).
        :param gas_ema_alpha: Exponential moving average alpha for gas (default is 0.1).
        :param temp_baseline: Baseline temperature (default is 23.0).
        :param pressure_baseline: Baseline pressure (default is 1013.25).
        :param humi_baseline: Baseline humidity (default is 45.0).
        :param gas_baseline: Baseline gas resistance (default is 450_000).
        """
                    
    def set_temperature_correction(self, value):
        """
        Set the temperature correction value.
        
        :param value: Temperature correction value in Celsius.
        """
        
    def read(self, gas=False):
        """
        Read temperature, pressure, humidity, and gas data from the BME688 sensor.
        
        :param gas: If True, read gas data; otherwise, do not read gas data.
        :return: Tuple of (temperature, pressure, humidity, gas) values.
        """
        
    def sealevel(self, altitude):
        """
        Calculate sea level pressure based on altitude.
        
        :param altitude: Altitude in meters.
        :return: Sea level pressure in hPa.
        """
        
    def altitude(self, sealevel): 
        """
        Calculate altitude based on sea level pressure.
        
        :param sealevel: Sea level pressure in hPa.
        :return: Altitude in meters.
        """

    def iaq(self):
        """
        Calculate Indoor Air Quality (IAQ) score based on temperature, pressure, humidity, and gas data.
        
        :return: IAQ score, temperature, pressure, humidity, gas values.
        """
        
    def burnIn(self, threshold=0.01, count=10, timeout_sec=180): 
        """
        Perform a burn-in test for the BME688 sensor.
        
        :param threshold: Threshold for gas change (default is 0.01).
        :param count: Number of consecutive readings above threshold (default is 10).
        :param timeout_sec: Timeout in seconds (default is 180).
        :return: Generator yielding (status, gas, gas_change) tuples.
        """
        

class IMU:
    """
    A class to read data from the BNO055 IMU sensor.
    """
    
    BNO055_ADDR = micropython.const(0x28)

    ACCELERATION = micropython.const(0x08)
    MAGNETIC = micropython.const(0x0E)
    GYROSCOPE = micropython.const(0x14)
    EULER = micropython.const(0x1A)
    QUATERNION = micropython.const(0x20)
    ACCEL_LINEAR = micropython.const(0x28)
    ACCEL_GRAVITY = micropython.const(0x2E)
    TEMPERATURE = micropython.const(0x34)
    
    def __init__(self):
        """
        Initialize the BNO055 IMU sensor.
        """
        
    def calibration(self):
        """
        Read calibration data from the BNO055 sensor.
        
        :return: Tuple of calibration status for system, gyro, accelerometer, and magnetometer.
        """
        
    def read(self, addr):
        """
        Read data from the BNO055 sensor.
        
        :param addr: Address of the register to read.
        :return: Tuple of values read from the register.
        """


class PixelLed:
    """
    A class to control a WS2812 RGB LED strip using a AutoCON's PIO.
    Inherits from NeoPixel.
    """
    
    def __init__(self, pin:int=0, brightness:float=1.0):
        """
        Initialize the RGBLed object.
        :param pin: GPIO pin number for the LED strip.
        :param num_leds: Number of LEDs in the strip.
        :param brightness: Brightness level (0.1 to 1.0).
        """
          
    def set_color(self, r:int, g:int, b:int):
        """
        Set the color of a specific pixel in the LED strip.
        
        :param r: Red component (0-255).
        :param g: Green component (0-255).
        :param b: Blue component (0-255).
        """
        
    def clear(self):
        """
        Clear the LED strip by turning off all LEDs.
        """


class Buzzer:
    """
    Buzzer class for generating tones using PWM on RP2040.
    Accepts notes like 'C5', 'DS4', etc., and note lengths (1, 2, 4, 8, 16, 32).
    Core1 is used for sound playback, so it cannot be used for other tasks while playback is in progress.
    """
    
    NOTE_FREQ = {
        'C':  0, 'CS': 1, 'D': 2, 'DS': 3, 'E': 4, 'F': 5,
        'FS': 6, 'G': 7, 'GS': 8, 'A': 9, 'AS': 10, 'B': 11
    }

    BASE_FREQ = 16.35  # Frequency of note C0 in Hz

    def __init__(self, pin: int = 1, tempo: int = 120):
        """
        Initialize the buzzer.
        :param pin: GPIO pin number connected to the buzzer.
        :param tempo: Tempo in beats per minute (BPM).
        """
        
    def __note_to_freq(self, note_octave: str) -> float:
        """
        Convert a note string like 'C5' or 'DS4' to frequency in Hz.
        :param note_octave: Combined note and octave string.
        :return: Frequency in Hz.
        """

    def __raw_play(self, sequence, effect:str=None):
        """
        Internal thread function for playing a note sequence.
        :param sequence: List of alternating [note_octave, length, ...]
        """

    def tone(self, note_octave: str, length: int=4, echo:bool=False):
        """ 
        Play a single tone or rest.
        :param note_octave: Note + octave string (e.g., 'E5', 'CS4', or 'R' for rest).
        :param length: Note length (1, 2, 4, 8, 16, or 32).
        :param echo: If True, apply echo effect.
        """

    def play(self, melody, background:bool=False, echo:bool=False):
        """
        Play a melody, accepting either a formatted string or a list.
        :param melody: Melody in string format or list format.
        :param background: If True, play in the background.
        :param echo: If True, apply echo effect.
        """
            
    def stop(self):
        """
        Stop the currently playing melody.
        """

    def set_tempo(self, bpm: int):
        """
        Set the playback tempo.
        :param bpm: Tempo in beats per minute.
        """


class Din:
    """
    A class to read digital input pins.
    """
    
    LOW = micropython.const(0)
    HIGH = micropython.const(1)


    def __init__(self, pins=('GPIO21', 'GPIO22')):
        """
        Initialize the digital input pins.
        """
    
    def __getitem__(self, index:int) -> int:
        """
        Get the value of a specific pin.
        :param index: Index of the pin (0 to len(pins)-1).
        :return: Pin value (0 or 1).
        """

    def __len__(self) -> int:
        """
        Get the number of digital input pins.
        
        :return: Number of pins.
        """


class Relay:
    """
    A class to control relay pins.
    """
    
    _p = lambda pin: machine.Pin(pin, machine.Pin.OUT)
    
    def __init__(self, pins=('GPIO17', 'GPIO20', 'GPIO28')):
        """
        Initialize the relay pins.
        
        :param pins: List of GPIO pin numbers or names (e.g., 17, 'GPIO17').
        """
                    
    def __getitem__(self, index:int) -> machine.Pin:
        """
        Get the relay pin at the specified index.
        
        :param index: Index of the relay pin (0 to len(pins)-1).
        :return: Relay pin object.
        """

    def __len__(self) -> int:
        """
        Get the number of relay pins.
        
        :return: Number of relay pins.
        """


class Adc(machine.ADC):
    """
    A class to read analog values from ADC pins.
    """
        
    def __init__(self, channel:int):
        """
        Initialize the ADC pin.
        :param channel: ADC channel number (0, 1, or 2).
        """
    
    def read(self) -> float:
        """
        Read the analog value from the ADC pin.
        resolution = 3.3V/4096 = 0.0008056640625V/bit. (0.806mV/bit)
        Therefore, the voltage can be accurately represented up to three decimal places.
        
        :return: Analog value in volts.
        """

class Pwm(machine.PWM):
    """
    A class to control PWM on a pin.
    """
        
    def __init__(self, pin, freq, duty_u16=_MAX_DUTY_U16):
        """
        Initialize PWM on the specified pin.
        
        :param pin: GPIO pin number or Pin object
        :param freq: PWM frequency in Hz
        :param duty_u16: initial raw duty (0.._MAX_DUTY_U16)
        """
        
    def _update_periods(self):
        """Recalculate period in µs when frequency changes."""

    @property
    def freq(self):
        """Get current PWM frequency in Hz."""

    @freq.setter
    def freq(self, hz):
        """
        Set PWM frequency.
        
        :param hz: Frequency in Hz (_MIN_FREQ.._MAX_FREQ)
        """

    @property
    def period(self):
        """Get PWM period in microseconds."""

    @period.setter
    def period(self, us):
        """
        Set PWM period by specifying microseconds.

        :param us: Period in microseconds (must be >0)
        """

    @property
    def duty(self):
        """Get current duty cycle in percent (0–100)."""

    @duty.setter
    def duty(self, pct):
        """
        Set duty cycle by percentage.
        
        :param pct: Duty cycle percent (0..100)
        """

    @property
    def duty_raw(self):
        """Get current raw duty (0..65535)."""

    @duty_raw.setter
    def duty_raw(self, raw):
        """
        Set raw duty cycle.
        
        :param raw: Raw duty (0..65535)
        """

    @property
    def duty_us(self):
        """
        Get high-time pulse width in microseconds.
        """

    @duty_us.setter
    def duty_us(self, us):
        """
        Set high-time pulse width in microseconds.
        
        :param us: High-time in microseconds (0..period_us)
        """

    def deinit(self):
        """Deinitialize PWM and release the pin."""


class ServoMotor(Pwm):
    """
    Servo driver that maps 0–180° to pulse widths.
    """
    
    def __init__(self, pin:int, freq:int, min_us:int=500, max_us:int=2500):
        """
        :param pin: GPIO pin connected to servo signal line
        :param freq: PWM frequency for servo (default 50Hz)
        :param min_us: pulse width for 0° (µs)
        :param max_us: pulse width for 180° (µs)
        """

    def angle(self, deg:int):
        """
        Rotate servo to specified angle.

        :param deg: target angle in degrees (0..180)
        :return: pulse width in microseconds
         """
    
    def deinit(self):
        """Stop servo PWM and release resources."""
