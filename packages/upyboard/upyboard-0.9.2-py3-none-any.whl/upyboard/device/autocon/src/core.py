import math
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
        
        self.__led = machine.Pin("WL_GPIO0", machine.Pin.OUT)
    
    def on(self):
        """
        Turn on the LED.
        """
        
        self.__led.value(1)
        
    def off(self):
        """
        Turn off the LED.
        """
        
        self.__led.value(0)

    def toggle(self):
        """
        Toggle the LED state.
        """
        
        self.__led.toggle()
    
    def state(self):
        """
        Get the current state of the LED.
        
        :return: True if LED is on, False if off.
        """
        
        return not self.__led.value()


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
        
        self.adjusted_lux  = adjusted_lux 
                 
        self.__i2c = machine.I2C(0)
        
        self.__i2c.writeto(Illuminance.BH1750_ADDR, Illuminance.POWER_ON) 
        self.__i2c.writeto(Illuminance.BH1750_ADDR, Illuminance.RESET)
        
    def __del__(self):
        self.__i2c.writeto(Illuminance.BH1750_ADDR, Illuminance.POWER_OFF)

    def read(self, continuous=True):
        """
        Read illuminance data from the BH1750 sensor.
        
        :param continuous: If True, read in continuous mode; otherwise, read in one-time mode.
        :return: Illuminance value in lux. 
        """
              
        mode = Illuminance.CONTINUOUS_HIGH_RES if continuous else Illuminance.ONE_TIME_HIGH_RES      
        self.__i2c.writeto(Illuminance.BH1750_ADDR, bytes([mode]))
        utime.sleep_ms(120 if continuous else 180)            
        
        data = self.__i2c.readfrom(Illuminance.BH1750_ADDR, 2)
        lux = int.from_bytes(data, 'big') * self.adjusted_lux
                  
        return round(lux)


class Tphg:
    """
    A class to read temperature, pressure, humidity, and gas data from the BME688 sensor.
    """
    
    BME688_ADDR = micropython.const(0x77)
    
    FORCED_MODE = micropython.const(0x01)
    SLEEP_MODE = micropython.const(0x00)
        
    def __set_power_mode(self, value):
        tmp = self.__i2c.readfrom_mem(Tphg.BME688_ADDR, 0x74, 1)[0] 
        tmp &= ~0x03
        tmp |= value
        self.__i2c.writeto_mem(Tphg.BME688_ADDR, 0x74, bytes([tmp]))
        utime.sleep_ms(1)
        
    def __reset_sensor(self):
        """
        Soft reset the BME688 sensor and wait for it to become ready again.
        """
        try:
            # Soft reset
            self.__i2c.writeto_mem(Tphg.BME688_ADDR, 0xE0, bytes([0xB6]))
            utime.sleep_ms(10)
            
            # Wait for the reset to complete (check if the chip ID is readable)
            start_time = utime.ticks_ms()
            while utime.ticks_diff(utime.ticks_ms(), start_time) < 500:
                try:
                    chip_id = self.__i2c.readfrom_mem(Tphg.BME688_ADDR, 0xD0, 1)[0]
                    if chip_id == 0x61:  # BME680/688 chip ID is 0x61
                        # Re-initialize important settings
                        self.__i2c.writeto_mem(Tphg.BME688_ADDR, 0x72, bytes([0b001]))                        # Humidity oversampling x1
                        self.__i2c.writeto_mem(Tphg.BME688_ADDR, 0x74, bytes([(0b010 << 5) | (0b011 << 2)]))  # Temperature oversampling x2, Pressure oversampling x4
                        self.__i2c.writeto_mem(Tphg.BME688_ADDR, 0x75, bytes([0b001 << 2]))                   # Filter coefficient 3
                        
                        self.__i2c.writeto_mem(Tphg.BME688_ADDR, 0x50, bytes([0x1F]))                         # idac_heat_0
                        self.__i2c.writeto_mem(Tphg.BME688_ADDR, 0x5A, bytes([0x73]))                         # res_heat_0
                        self.__i2c.writeto_mem(Tphg.BME688_ADDR, 0x64, bytes([0x64]))                         # gas_wait_0 is 100ms
                        
                        self.__i2c.writeto_mem(Tphg.BME688_ADDR, 0x71, bytes([(0b1 << 4) | (0b0000)]))        # run_gas, nv_conv
                        utime.sleep_ms(50)
                        return True
                except:
                    utime.sleep_ms(10)
            return False
        except:
            return False
  
    def __perform_reading(self, max_retries=5):
        """
        Perform a reading from the BME688 sensor with improved error handling.
        
        :param max_retries: Maximum number of retry attempts (default is 5)
        :raises OSError: If the sensor data is not ready after all retries
        """
        total_attempts = 0
        reset_performed = False
        
        while total_attempts < max_retries:
            try:
                total_attempts += 1
                
                # Enter forced mode to trigger one measurement cycle
                self.__i2c.writeto_mem(self.BME688_ADDR, 0x71, bytes([(0b1 << 4) | 0x00]))
                self.__set_power_mode(Tphg.FORCED_MODE)
                
                # Give the sensor some initial time to start the conversion
                utime.sleep_ms(50)
                
                # Maximum wait time for measurement (500ms should be enough for all oversampling settings)
                max_wait_time = 500
                start_time = utime.ticks_ms()
                
                # Keep checking until data is ready or timeout occurs
                while utime.ticks_diff(utime.ticks_ms(), start_time) < max_wait_time:
                    # Read status register
                    status = self.__i2c.readfrom_mem(self.BME688_ADDR, 0x1D, 1)[0]
                    
                    # Check if measuring (bit 5) is 0 and new_data (bit 7) is 1
                    gas_measuring = status & 0x20
                    new_data_ready = status & 0x80
                    
                    if not gas_measuring and new_data_ready:
                        # Data is ready, read all values at once
                        data = self.__i2c.readfrom_mem(Tphg.BME688_ADDR, 0x1D, 17)
                        
                        # Process the raw data
                        self._adc_pres = ((data[2] * 4096) + (data[3] * 16) + (data[4] / 16))
                        self._adc_temp = ((data[5] * 4096) + (data[6] * 16) + (data[7] / 16))
                        self._adc_hum = ustruct.unpack(">H", bytes(data[8:10]))[0]
                        self._adc_gas = int(ustruct.unpack(">H", bytes(data[13:15]))[0] / 64)
                        self._gas_range = data[14] & 0x0F
                            
                        # Calculate t_fine (needed for other calculations)
                        var1 = (self._adc_temp / 8) - (self._temp_calibration[0] * 2)
                        var2 = (var1 * self._temp_calibration[1]) / 2048
                        var3 = ((var1 / 2) * (var1 / 2)) / 4096
                        var3 = (var3 * self._temp_calibration[2] * 16) / 16384
                        self._t_fine = int(var2 + var3)
                        
                        # If we got here, the read was successful
                        return
                    
                    # Wait a bit before checking again, but not too long
                    utime.sleep_ms(10)
                
                # If we get here, the sensor didn't provide data within the timeout
                if not reset_performed and total_attempts >= max_retries // 2:
                    # Try a sensor reset as a last resort
                    if self.__reset_sensor():
                        reset_performed = True
                        # Give it one more try after reset
                        continue
                
                # Wait a bit longer between retries
                utime.sleep_ms(100 * total_attempts)
                
            except Exception as e:
                # For any unexpected error, wait and try again
                utime.sleep_ms(100 * total_attempts)
                
        # If we reach this point, all attempts failed
        raise OSError("BME688 sensor failed to provide data after multiple attempts. Consider power cycling the device.")

    def __temperature(self):
        """
        Calculate temperature in Celsius.
        """

        return ((((self._t_fine * 5) + 128) / 256) / 100) + self._temperature_correction
            
    def __pressure(self):
        """
        Calculate pressure in hPa.
        """
        
        var1 = (self._t_fine / 2) - 64000
        var2 = ((var1 / 4) * (var1 / 4)) / 2048
        var2 = (var2 * self._pressure_calibration[5]) / 4
        var2 = var2 + (var1 * self._pressure_calibration[4] * 2)
        var2 = (var2 / 4) + (self._pressure_calibration[3] * 65536)
        var1 = ((((var1 / 4) * (var1 / 4)) / 8192) * (self._pressure_calibration[2] * 32) / 8) + ((self._pressure_calibration[1] * var1) / 2)
        var1 = var1 / 262144
        var1 = ((32768 + var1) * self._pressure_calibration[0]) / 32768
        calc_pres = 1048576 - self._adc_pres
        calc_pres = (calc_pres - (var2 / 4096)) * 3125
        calc_pres = (calc_pres / var1) * 2
        var1 = (self._pressure_calibration[8] * (((calc_pres / 8) * (calc_pres / 8)) / 8192)) / 4096
        var2 = ((calc_pres / 4) * self._pressure_calibration[7]) / 8192
        var3 = (((calc_pres / 256) ** 3) * self._pressure_calibration[9]) / 131072
        calc_pres += (var1 + var2 + var3 + (self._pressure_calibration[6] * 128)) / 16
        return calc_pres / 100

    def __humidity(self):
        """
        Calculate humidity in %.
        """
        
        temp_scaled = ((self._t_fine * 5) + 128) / 256
        var1 = (self._adc_hum - (self._humidity_calibration[0] * 16)) - ((temp_scaled * self._humidity_calibration[2]) / 200)
        var2 = (self._humidity_calibration[1] * (((temp_scaled * self._humidity_calibration[3]) / 100) + 
                (((temp_scaled * ((temp_scaled * self._humidity_calibration[4]) / 100)) / 64) / 100) + 16384)) / 1024
        var3 = var1 * var2
        var4 = self._humidity_calibration[5] * 128
        var4 = (var4 + ((temp_scaled * self._humidity_calibration[6]) / 100)) / 16
        var5 = ((var3 / 16384) * (var3 / 16384)) / 1024
        var6 = (var4 * var5) / 2
        calc_hum = ((((var3 + var6) / 1024) * 1000) / 4096) / 1000
        return 100 if calc_hum > 100 else 0 if calc_hum < 0 else calc_hum
    
    def __gas(self):
        """
        Calculate gas resistance in ohms.
        """
        
        lookup_table_1 = {
            0: 2147483647.0, 1: 2126008810.0, 2: 2130303777.0, 3: 2147483647.0,
            4: 2143188679.0, 5: 2136746228.0, 6: 2126008810.0, 7: 2147483647.0
        }

        lookup_table_2 = {
            0: 4096000000.0, 1: 2048000000.0, 2: 1024000000.0, 3: 512000000.0,
            4: 255744255.0, 5: 127110228.0, 6: 64000000.0, 7: 32258064.0,
            8: 16016016.0, 9: 8000000.0, 10: 4000000.0, 11: 2000000.0,
            12: 1000000.0, 13: 500000.0, 14: 250000.0, 15: 125000.0
        }

        var1 = ((1340 + (5 * self._sw_err)) * lookup_table_1.get(self._gas_range, 2147483647.0)) / 65536 
        var2 = ((self._adc_gas * 32768) - 16777216) + var1
        var3 = (lookup_table_2.get(self._gas_range, 125000.0) * var1) / 512 
        return ((var3 + (var2 / 2)) / var2)

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
        
        self.__i2c = machine.I2C(0)
        
        self.__i2c.writeto_mem(Tphg.BME688_ADDR, 0xE0, bytes([0xB6]))                         # Soft reset
        utime.sleep_ms(5)        
          
        self.__set_power_mode(Tphg.SLEEP_MODE)
        
        t_calibration = self.__i2c.readfrom_mem(Tphg.BME688_ADDR, 0x89, 25)
        t_calibration += self.__i2c.readfrom_mem(Tphg.BME688_ADDR, 0xE1, 16)
        
        self._sw_err = (self.__i2c.readfrom_mem(Tphg.BME688_ADDR, 0x04, 1)[0] & 0xF0) / 16

        calibration = [float(i) for i in list(ustruct.unpack("<hbBHhbBhhbbHhhBBBHbbbBbHhbb", bytes(t_calibration[1:39])))]
        self._temp_calibration = [calibration[x] for x in [23, 0, 1]]
        self._pressure_calibration = [calibration[x] for x in [3, 4, 5, 7, 8, 10, 9, 12, 13, 14]]
        self._humidity_calibration = [calibration[x] for x in [17, 16, 18, 19, 20, 21, 22]]
        #self._gas_calibration = [calibration[x] for x in [25, 24, 26]]                        # res_heat_0, idac_heat_0, gas_wait_0
        
        self._humidity_calibration[1] *= 16
        self._humidity_calibration[1] += self._humidity_calibration[0] % 16
        self._humidity_calibration[0] /= 16

        self.__i2c.writeto_mem(Tphg.BME688_ADDR, 0x72, bytes([0b001]))                        # Humidity oversampling x1
        self.__i2c.writeto_mem(Tphg.BME688_ADDR, 0x74, bytes([(0b010 << 5) | (0b011 << 2)]))  # Temperature oversampling x2, Pressure oversampling x4
        self.__i2c.writeto_mem(Tphg.BME688_ADDR, 0x75, bytes([0b001 << 2]))                   # Filter coefficient 3 (only to temperature and pressure data)
        
        self.__i2c.writeto_mem(Tphg.BME688_ADDR, 0x50, bytes([0x1F]))                         # idac_heat_0
        self.__i2c.writeto_mem(Tphg.BME688_ADDR, 0x5A, bytes([0x73]))                         # res_heat_0
        self.__i2c.writeto_mem(Tphg.BME688_ADDR, 0x64, bytes([0x64]))                         # gas_wait_0 is 100ms (1ms ~ 4032ms, 20ms ~ 30ms are neccessary)
                
        self.__i2c.writeto_mem(Tphg.BME688_ADDR, 0x71, bytes([(0b1 << 4) | (0b0000)]))        # run_gas(enable gas measurements), nv_conv (index of heater set-point 0)
        utime.sleep_ms(50)
        
        self._temperature_correction = -10
        self._t_fine = None
        self._adc_pres = None
        self._adc_temp = None
        self._adc_hum = None
        self._adc_gas = None
        self._gas_range = None
        
        self.temp_weighting = temp_weighting
        self.pressure_weighting = pressure_weighting
        self.humi_weighting = humi_weighting
        self.gas_weighting = gas_weighting
        self.gas_ema_alpha = gas_ema_alpha
        self.temp_baseline = temp_baseline
        self.pressure_baseline = pressure_baseline
        self.humi_baseline = humi_baseline
        self.gas_baseline = gas_baseline
        
        total_weighting = temp_weighting + pressure_weighting + humi_weighting + gas_weighting
        if abs(total_weighting - 1.0) > 0.001:
             raise ValueError("The sum of weightings is not equal to 1.  This may lead to unexpected IAQ results.")
            
    def set_temperature_correction(self, value):
        """
        Set the temperature correction value.
        
        :param value: Temperature correction value in Celsius.
        """
        
        self._temperature_correction += value

    def read(self, gas=False):
        """
        Read temperature, pressure, humidity, and gas data from the BME688 sensor.
        
        :param gas: If True, read gas data; otherwise, do not read gas data.
        :return: Tuple of (temperature, pressure, humidity, gas) values.
        """
        
        self.__perform_reading()
        if not gas:
            return self.__temperature(), self.__pressure(), self.__humidity(), None
        else:
            return self.__temperature(), self.__pressure(), self.__humidity(), self.__gas()
        
    def sealevel(self, altitude):
        """
        Calculate sea level pressure based on altitude.
        
        :param altitude: Altitude in meters.
        :return: Sea level pressure in hPa.
        """
        
        self.__perform_reading()
        press = self.__pressure()  
        return press / pow((1-altitude/44330), 5.255), press
        
    def altitude(self, sealevel): 
        """
        Calculate altitude based on sea level pressure.
        
        :param sealevel: Sea level pressure in hPa.
        :return: Altitude in meters.
        """
        
        self.__perform_reading()
        press = self.__pressure()
        return 44330 * (1.0-pow(press/sealevel,1/5.255)), press

    def iaq(self):
        """
        Calculate Indoor Air Quality (IAQ) score based on temperature, pressure, humidity, and gas data.
        
        :return: IAQ score, temperature, pressure, humidity, gas values.
        """
        
        self.__perform_reading()
        temp = self.__temperature()
        pres = self.__pressure()
        humi = self.__humidity()
        gas = self.__gas()

        hum_offset = humi - self.humi_baseline
        hum_score = (1 - min(max(abs(hum_offset) / (self.humi_baseline * 2), 0), 1)) * (self.humi_weighting * 100)

        temp_offset = temp - self.temp_baseline
        temp_score = (1- min(max(abs(temp_offset) / 10, 0), 1)) * (self.temp_weighting * 100)

        self.gas_baseline = (self.gas_ema_alpha * gas) + ((1 - self.gas_ema_alpha) * self.gas_baseline) # EMA for gas_baseline
        gas_offset = self.gas_baseline - gas
        gas_score = (gas_offset / self.gas_baseline) * (self.gas_weighting * 100)
        gas_score = max(0, min(gas_score, self.gas_weighting * 100))
        
        pressure_offset = pres - self.pressure_baseline
        pressure_score =  (1 - min(max(abs(pressure_offset) / 50, 0), 1)) * (self.pressure_weighting * 100)

        iaq_score = round((hum_score + temp_score + gas_score + pressure_score) * 5)

        return iaq_score, temp, pres, humi, gas
        
    def burnIn(self, threshold=0.01, count=10, timeout_sec=180): 
        """
        Perform a burn-in test for the BME688 sensor.
        
        :param threshold: Threshold for gas change (default is 0.01).
        :param count: Number of consecutive readings above threshold (default is 10).
        :param timeout_sec: Timeout in seconds (default is 180).
        :return: Generator yielding (status, gas, gas_change) tuples.
        """
        
        self.__perform_reading()
        prev_gas = self.__gas()
        
        counter  = 0
        timeout_time = utime.ticks_us()  
        interval_time = utime.ticks_us()
                 
        while True:
            if utime.ticks_diff(utime.ticks_us(), interval_time) > 1_000_000:
                self.__perform_reading()
                curr_gas = self.__gas()
                gas_change = abs((curr_gas - prev_gas) / prev_gas)
                yield False, curr_gas, gas_change

                counter  = counter + 1 if gas_change <= threshold else 0

                if counter > count:
                    yield True, curr_gas, 0.0
                    break
                else:
                    yield False, curr_gas, gas_change
                    
                prev_gas = curr_gas
                interval_time = utime.ticks_us()
            
            if utime.ticks_diff(utime.ticks_us(), timeout_time) > timeout_sec * 1_000_000:
                yield False, 0.0, 0.0
                break


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
        
        self.__i2c = machine.I2C(0)
        
        self.__scale = {self.ACCELERATION:1/100, self.MAGNETIC:1/16, self.GYROSCOPE:0.001090830782496456, self.EULER:1/16,  self.QUATERNION:1/(1<<14), self.ACCEL_LINEAR:1/100, self.ACCEL_GRAVITY:1/100}
        self.__call = {self.ACCELERATION:self.__read_other, self.MAGNETIC:self.__read_other, self.GYROSCOPE:self.__read_other, self.EULER:self.__read_other,  self.QUATERNION:self.__read_quaternion, self.ACCEL_LINEAR:self.__read_other, self.ACCEL_GRAVITY:self.__read_other, self.TEMPERATURE:self.__read_temperature}

        self.__i2c.writeto_mem(IMU.BNO055_ADDR, 0X3D, bytes([0x00])) #Mode Register, Enter configuration.
        utime.sleep_ms(20)
        self.__i2c.writeto_mem(IMU.BNO055_ADDR, 0x3F, bytes([0x20])) #Trigger Register, Reset
        utime.sleep_ms(650)
        self.__i2c.writeto_mem(IMU.BNO055_ADDR, 0X3E, bytes([0x00])) #Power Register, Set to normal power. cf) low power is 0x01
        self.__i2c.writeto_mem(IMU.BNO055_ADDR, 0X07, bytes([0x00])) #Page Register, Make sure we're in config mode and on page0(param, data), page1(conf)
        self.__i2c.writeto_mem(IMU.BNO055_ADDR, 0X3F, bytes([0x80])) #Trigger Register, External oscillator
        self.__i2c.writeto_mem(IMU.BNO055_ADDR, 0X3F, bytes([0x00])) #Trigger Register,
        utime.sleep_ms(10)
        self.__i2c.writeto_mem(IMU.BNO055_ADDR, 0X3D, bytes([0x0C])) #Mode Register, Enter normal operation (NDOF)
        utime.sleep_ms(200)

    def __read_temperature(self, addr):
        """
        Read temperature data from the BNO055 sensor.
        
        :param addr: Address of the temperature register.
        :return: Temperature value in Celsius.
        """
        
        t = self.__i2c.readfrom_mem(IMU.BNO055_ADDR, addr, 1)[0]
        return t - 256 if t > 127 else t

    def __read_quaternion(self, addr):
        """
        Read quaternion data from the BNO055 sensor.
        
        :param addr: Address of the quaternion register.
        :return: Quaternion values as a tuple.
        """
        
        t = self.__i2c.readfrom_mem(IMU.BNO055_ADDR, addr, 8)  
        return tuple(v * self.__scale[self.QUATERNION] for v in ustruct.unpack('hhhh', t))

    def __read_other(self, addr):
        """
        Read other data from the BNO055 sensor.
        
        :param addr: Address of the register to read.
        :return: Tuple of values read from the register.
        """
        
        if addr not in self.__scale:
            raise ValueError(f"Address {addr} not in scale mapping")
        t = self.__i2c.readfrom_mem(IMU.BNO055_ADDR, addr, 6)
        return tuple(v * self.__scale[addr] for v in ustruct.unpack('hhh', t))

    def calibration(self):
        """
        Read calibration data from the BNO055 sensor.
        
        :return: Tuple of calibration status for system, gyro, accelerometer, and magnetometer.
        """
        
        data = self.__i2c.readfrom_mem(IMU.BNO055_ADDR, 0x35, 1)[0] #Calibration Resiger, Read        
        return (data >> 6) & 0x03, (data >> 4) & 0x03, (data >> 2) & 0x03, data & 0x03  #Sys, Gyro, Accel, Mag

    def read(self, addr):
        """
        Read data from the BNO055 sensor.
        
        :param addr: Address of the register to read.
        :return: Tuple of values read from the register.
        """
        
        return self.__call[addr](addr)


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
        
        self.brightness = brightness
        self.__np = neopixel.NeoPixel(machine.Pin(0, machine.Pin.OUT), 1)

    def set_color(self, r:int, g:int, b:int):
        """
        Set the color of a specific pixel in the LED strip.
        
        :param r: Red component (0-255).
        :param g: Green component (0-255).
        :param b: Blue component (0-255).
        """
        
        r = int(r * self.brightness)
        g = int(g * self.brightness)
        b = int(b * self.brightness)
                
        self.__np[0] = (r, g, b)
        self.__np.write()

    def clear(self):
        """
        Clear the LED strip by turning off all LEDs.
        """
        
        self.__np[0] = (0, 0, 0)
        self.__np.write()


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
        
        self.__buzzer= machine.PWM(machine.Pin(pin))
        self.__buzzer.duty_u16(0)
        self.__tempo = tempo
        self.__is_playing = False

    def __note_to_freq(self, note_octave: str) -> float:
        """
        Convert a note string like 'C5' or 'DS4' to frequency in Hz.
        :param note_octave: Combined note and octave string.
        :return: Frequency in Hz.
        """

        note = note_octave[:-1].upper()
        octave = int(note_octave[-1])
        if note not in self.NOTE_FREQ:
            raise ValueError(f"Unknown note: {note}")
        n = (octave * 12) + self.NOTE_FREQ[note]
        return self.BASE_FREQ * (2 ** (n / 12))

    def __raw_play(self, sequence, effect:str=None):
        """
        Internal thread function for playing a note sequence.
        :param sequence: List of alternating [note_octave, length, ...]
        """

        self.__is_playing = True
        for i in range(0, len(sequence), 2):
            if not self.__is_playing:
                break
            note = sequence[i]
            length = sequence[i + 1]
            self.tone(note, length, effect)
        self.__is_playing = False


    def tone(self, note_octave: str, length: int=4, echo:bool=False):
        """ 
        Play a single tone or rest.
        :param note_octave: Note + octave string (e.g., 'E5', 'CS4', or 'R' for rest).
        :param length: Note length (1, 2, 4, 8, 16, or 32).
        :param echo: If True, apply echo effect.
        """

        duration = (60 / self.__tempo) * (4 / length)

        if note_octave.upper() in ['R', 'REST']:
            self.__buzzer.duty_u16(0)
            utime.sleep(duration)
            return

        freq = self.__note_to_freq(note_octave)
        self.__buzzer.freq(int(freq))
        self.__buzzer.duty_u16(32768)

        if echo:
            echo_delay = duration * 0.1  # Echo delay time as a fraction of the original duration
            echo_decay = 0.5  # Echo decay ratio
            num_echoes = 2    # Number of echoes

            # Play the original tone
            utime.sleep(duration * 0.5)
            self.__buzzer.duty_u16(0)
            utime.sleep(duration * 0.1)

            # Play echoes
            for i in range(num_echoes):
                utime.sleep(echo_delay)
                self.__buzzer.duty_u16(int(32768 * (echo_decay ** (i + 1))))
                utime.sleep(duration * 0.2)
                self.__buzzer.duty_u16(0)
                utime.sleep(duration * 0.1)
        else:        
            utime.sleep(duration * 0.9)
            self.__buzzer.duty_u16(0)
            utime.sleep(duration * 0.1)

    def play(self, melody, background:bool=False, echo:bool=False):
        """
        Play a melody, accepting either a formatted string or a list.
        :param melody: Melody in string format or list format.
        :param background: If True, play in the background.
        :param echo: If True, apply echo effect.
        """
        
        if self.__is_playing:
            print("Playback already in progress.")
            return

        if background:
            _thread.start_new_thread(self.__raw_play, (melody, echo))
        else:
            self.__raw_play(melody, echo)
            
    def stop(self):
        """
        Stop the currently playing melody.
        """
        
        self.__is_playing = False
        self.__buzzer.duty_u16(0)

    def set_tempo(self, bpm: int):
        """
        Set the playback tempo.
        :param bpm: Tempo in beats per minute.
        """
        
        self.__tempo = bpm


class Din:
    """
    A class to read digital input pins.
    """
    
    LOW = micropython.const(0)
    HIGH = micropython.const(1)

    class __ReadOnly:
        """
        A class to read a digital input pin.
        """
        
        def __init__(self, pin:int|str):
            """
            Initialize the digital input pin.
            
            :param pin: GPIO pin number or name (e.g., 21, 'GPIO21').
            """
            
            self.__pin = machine.Pin(pin, machine.Pin.IN)

        def value(self) -> int:
            """
            Get the value of the pin.
            
            :return: Pin value (0 or 1).
            """
            return self.__pin.value()

        def __repr__(self):
            return f"<ReadOnlyPin value={self.value()}>"

    def __init__(self, pins=('GPIO21', 'GPIO22')):
        """
        Initialize the digital input pins.
        """
        self.__din =[Din.__ReadOnly(pin) for pin in pins]
    
    def __getitem__(self, index:int) -> int:
        """
        Get the value of a specific pin.
        :param index: Index of the pin (0 to len(pins)-1).
        :return: Pin value (0 or 1).
        """
        
        return self.__din[index]

    def __len__(self) -> int:
        """
        Get the number of digital input pins.
        
        :return: Number of pins.
        """
        
        return len(self.__din)


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
        
        self.__relays = [Relay._p(pin) for pin in pins]
            
    def __getitem__(self, index:int) -> machine.Pin:
        """
        Get the relay pin at the specified index.
        
        :param index: Index of the relay pin (0 to len(pins)-1).
        :return: Relay pin object.
        """
        return self.__relays[index]

    def __len__(self) -> int:
        """
        Get the number of relay pins.
        
        :return: Number of relay pins.
        """
        
        return len(self.__relays)


class Adc(machine.ADC):
    """
    A class to read analog values from ADC pins.
    """
    
    ADC_CHANNELS = {0:26, 1:27, 2:28}
    
    def __init__(self, channel:int):
        """
        Initialize the ADC pin.
        :param channel: ADC channel number (0, 1, or 2).
        """
        adc_gpio_num = Adc.ADC_CHANNELS.get(channel)
        if adc_gpio_num is None:
            raise ValueError("Invalid ADC channel. Choose from 0, 1, or 2.")    
                
        super().__init__(machine.Pin(adc_gpio_num))
    
    def read(self):
        """
        Read the analog value from the ADC pin.
        resolution = 3.3V/4096 = 0.0008056640625V/bit. (0.806mV/bit)
        Therefore, the voltage can be accurately represented up to three decimal places.
        
        :return: Analog value in volts.
        """
        
        return math.floor(self.read_u16() * (3.3 / 65535) * 1000) / 1000 


def _clamp(val, lo, hi):
    """Clamp val into the inclusive range [lo, hi]."""
    return lo if val < lo else hi if val > hi else val
    
class Pwm(machine.PWM):
    _MIN_FREQ      = 8
    _MAX_FREQ      = 62_500_000
    _MIN_DUTY_PCT  = 0
    _MAX_DUTY_PCT  = 100
    _MIN_DUTY_U16  = 0
    _MAX_DUTY_U16  = (1 << 16) - 1 # 16-bit resolution, 0..65535
    _MICROSECONDS_PER_SECOND = 1_000_000
    
    def __init__(self, pin, freq, duty_u16=_MAX_DUTY_U16):
        """
        Initialize PWM on the specified pin.
        
        :param pin: GPIO pin number or Pin object
        :param freq: PWM frequency in Hz
        :param duty_u16: initial raw duty (0.._MAX_DUTY_U16)
        """
        super().__init__(machine.Pin(pin))
        self.freq = freq
        self.duty_raw = duty_u16  
        
    def _update_periods(self):
        """Recalculate period in µs when frequency changes."""
        self._period = self._MICROSECONDS_PER_SECOND // self._freq

    @property
    def freq(self):
        """Get current PWM frequency in Hz."""
        return self._freq

    @freq.setter
    def freq(self, hz):
        """
        Set PWM frequency.
        
        :param hz: Frequency in Hz (_MIN_FREQ.._MAX_FREQ)
        """
        if not (self._MIN_FREQ <= hz <= self._MAX_FREQ):
            raise ValueError(f"Frequency must be between {self._MIN_FREQ}Hz and {self._MAX_FREQ}Hz")
        super().freq(hz)
        self._freq = hz
        self._update_periods()

    @property
    def period(self):
        """Get PWM period in microseconds."""
        return self._period

    @period.setter
    def period(self, us):
        """
        Set PWM period by specifying microseconds.

        :param us: Period in microseconds (must be >0)
        """
        if us <= 0:
            raise ValueError("period must be > 0")
        new_freq = self._MICROSECONDS_PER_SECOND // us
        self.freq = new_freq

    @property
    def duty(self):
        """Get current duty cycle in percent (0–100)."""
        raw = self.duty_u16()
        return raw * 100 // self._MAX_DUTY_U16

    @duty.setter
    def duty(self, pct):
        """
        Set duty cycle by percentage.
        
        :param pct: Duty cycle percent (0..100)
        """
        pct = _clamp(pct, self._MIN_DUTY_PCT, self._MAX_DUTY_PCT)
        raw = int(pct * self._MAX_DUTY_U16 / 100)
        self.duty_u16(raw)

    @property
    def duty_raw(self):
        """Get current raw duty (0..65535)."""
        return self.duty_u16()

    @duty_raw.setter
    def duty_raw(self, raw):
        """
        Set raw duty cycle.
        
        :param raw: Raw duty (0..65535)
        """
        raw = _clamp(raw, self._MIN_DUTY_U16, self._MAX_DUTY_U16)
        self.duty_u16(raw)

    @property
    def duty_us(self):
        """
        Get high-time pulse width in microseconds.
        """
        raw = super().duty_u16()
        return raw * self._period // self._MAX_DUTY_U16

    @duty_us.setter
    def duty_us(self, us):
        """
        Set high-time pulse width in microseconds.
        
        :param us: High-time in microseconds (0..period_us)
        """
        us = _clamp(us, 0, self._period)
        raw = int(us * self._MAX_DUTY_U16 // self._period)
        super().duty_u16(raw)

    def deinit(self):
        """Deinitialize PWM and release the pin."""
        super().deinit()


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
        if not (0 < min_us < max_us):
            raise ValueError("min_us and max_us must satisfy 0 < min_us < max_us")

        super().__init__(pin, freq)
        self._min_us = min_us
        self._max_us = max_us

    def angle(self, deg:int):
        """
        Rotate servo to specified angle.

        :param deg: target angle in degrees (0..180)
        :return: pulse width in microseconds
         """
        deg = _clamp(deg, 0, 180)
        span_us = self._max_us - self._min_us
        us      = self._min_us + (span_us * deg) // 180

        self.duty_us = us
        return self.duty_us
    
    def deinit(self):
        """Stop servo PWM and release resources."""
        super().deinit()
