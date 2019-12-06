# filename: sensor_manager.py
import micropython, machine, ustruct, time, math

# from https://github.com/robert-hh/BMP085_BMP180
class Sensor_BMP085():
    def __init__(self, i2c=None, address=0x77):
        if i2c is None:
            raise ValueError("The I2C bus must be specified")
        else:
            self._bmp_i2c = i2c
        self.t = None
        self.p = None
        self._bmp_addr = address 
        self.chip_id = self._bmp_i2c.readfrom_mem(self._bmp_addr, 0xD0, 2)
        self._delays = (7, 8, 14, 28)
        self._diff_sign = time.ticks_diff(1, 0)
        (self._AC1, self._AC2, self._AC3, self._AC4, self._AC5, self._AC6,
         self._B1, self._B2, self._MB, self._MC, self._MD) = \
            ustruct.unpack('>hhhHHHhhhhh',
                self._bmp_i2c.readfrom_mem(self._bmp_addr, 0xAA, 22))
        self._oversample = 3
        self._baseline = 1013.25
        self._UT_raw = bytearray(2)
        self._B5 = 0
        self._MLX = bytearray(3)
        self._COMMAND = bytearray(1)
        self.gauge = self.makegauge() 
        for _ in range(128):
            next(self.gauge)
            time.sleep_ms(1)

    def compvaldump(self):
        return [self._AC1, self._AC2, self._AC3, self._AC4, self._AC5,
                self._AC6, self._B1, self._B2, self._MB, self._MC, self._MD,
                self._oversample]
    
    def makegauge(self):
        while True:
            self._COMMAND[0] = 0x2e
            self._bmp_i2c.writeto_mem(self._bmp_addr, 0xF4, self._COMMAND)
            t_start = time.ticks_ms()
            while (time.ticks_diff(time.ticks_ms(), t_start) *
                   self._diff_sign) <= 5: 
                yield None
            try:
                self._bmp_i2c.readfrom_mem_into(self._bmp_addr, 0xf6,
                                                self._UT_raw)
            except:
                yield None

            self._COMMAND[0] = 0x34 | (self._oversample << 6)
            self._bmp_i2c.writeto_mem(self._bmp_addr, 0xF4, self._COMMAND)
            t_pressure_ready = self._delays[self._oversample]
            t_start = time.ticks_ms()
            while (time.ticks_diff(time.ticks_ms(), t_start) *
                   self._diff_sign) <= t_pressure_ready:
                yield None
            try:
                self._bmp_i2c.readfrom_mem_into(self._bmp_addr, 0xf6,
                                                self._MLX)
            except:
                yield None
            yield True

    def blocking_read(self):
        if next(self.gauge) is not None:
            pass
        while next(self.gauge) is None:
            pass

    @property
    def sealevel(self):
        return self._baseline

    @sealevel.setter
    def sealevel(self, value):
        if 300 < value < 1200:  # just ensure some reasonable value
            self._baseline = value

    @property
    def oversample(self):
        return self._oversample

    @oversample.setter
    def oversample(self, value):
        if value in range(4):
            self._oversample = value
        else:
            print('oversample can only be 0, 1, 2 or 3, using 3 instead')
            self._oversample = 3

    @property
    def temperature(self):
        next(self.gauge)
        X1 = ((ustruct.unpack(">H", self._UT_raw)[0] - self._AC6) * self._AC5) >> 15
        X2 = (self._MC << 11) // (X1 + self._MD)
        self._B5 = X1 + X2
        return ((self._B5 + 8) >> 4) / 10.0

    @property
    def pressure(self):
        self.temperature  # Get values for temperature AND pressure
        UP = (((self._MLX[0] << 16) + (self._MLX[1] << 8) + self._MLX[2]) >>
              (8 - self._oversample))
        B6 = self._B5 - 4000
        X1 = (self._B2 * ((B6 * B6) >> 12)) >> 11
        X2 = (self._AC2 * B6) >> 11
        B3 = (((self._AC1 * 4 + X1 + X2) << self._oversample) + 2) >> 2
        X1 = (self._AC3 * B6) >> 13
        X2 = (self._B1 * ((B6 * B6) >> 12)) >> 16
        X3 = ((X1 + X2) + 2) >> 2
        B4 = (self._AC4 * (X3 + 32768)) >> 15
        B7 = (UP - B3) * (50000 >> self._oversample)
        p = (B7 * 2) // B4
        X1 = (((p >> 8) * (p >> 8)) * 3038) >> 16
        X2 = (-7357 * p) // 65536
        return (p + (X1 + X2 + 3791) // 16) / 100
    def read(self):
      self.t = self.temperature
      self.p = self.pressure
      return [self.t, self.p]
    @property
    def values(self):
      return [self.t, self.p]
    @property
    def values_dict(self):
      return {'t': self.t, 'p': self.p}
#End of Sensor_BMP085

class Sensor_BMP180(Sensor_BMP085):
    def __init__(self, i2c=None, address=0x77):
        super().__init__(i2c, address)
#End of Sensor_BMP180
