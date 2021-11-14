# https://github.com/schinckel/micropython-sht30/blob/master/sht30/sht30.py
class SHT30:
    POLYNOMIAL = 0x131  # P(x) = x^8 + x^5 + x^4 + 1 = 100110001
    ALERT_PENDING_MASK = 0x8000     # 15
    HEATER_MASK = 0x2000            # 13
    RH_ALERT_MASK = 0x0800          # 11
    T_ALERT_MASK = 0x0400           # 10
    RESET_MASK = 0x0010             # 4
    CMD_STATUS_MASK = 0x0002        # 1
    WRITE_STATUS_MASK = 0x0001      # 0
    # MSB = 0x2C LSB = 0x06 Repeatability = High, Clock stretching = enabled
    MEASURE_CMD = b'\x2C\x10'
    STATUS_CMD = b'\xF3\x2D'
    RESET_CMD = b'\x30\xA2'
    CLEAR_STATUS_CMD = b'\x30\x41'
    ENABLE_HEATER_CMD = b'\x30\x6D'
    DISABLE_HEATER_CMD = b'\x30\x66'
    def __init__(self, i2c=i2c, delta_temp=0, delta_hum=0, i2c_address=DEFAULT_I2C_ADDRESS):
        self.i2c = i2c
        self.i2c_addr = i2c_address
        self.set_delta(delta_temp, delta_hum)
        time.sleep_ms(50)
    def init(self):
        self.i2c.init()
    def is_present(self):
        return self.i2c_addr in self.i2c.scan()
    def set_delta(self, delta_temp=0, delta_hum=0):
        self.delta_temp = delta_temp
        self.delta_hum = delta_hum
    def _check_crc(self, data):
        crc = 0xFF
        for b in data[:-1]:
            crc ^= b
            for _ in range(8, 0, -1):
                if crc & 0x80:
                    crc = (crc << 1) ^ SHT30.POLYNOMIAL
                else:
                    crc <<= 1
        crc_to_check = data[-1]
        return crc_to_check == crc
    def send_cmd(self, cmd_request, response_size=6, read_delay_ms=100):
        try:
            self.i2c.start()
            self.i2c.writeto(self.i2c_addr, cmd_request)
            if not response_size:
                self.i2c.stop()
                return
            time.sleep_ms(read_delay_ms)
            data = self.i2c.readfrom(self.i2c_addr, response_size)
            self.i2c.stop()
            for i in range(response_size//3):
                if not self._check_crc(data[i*3:(i+1)*3]):  # pos 2 and 5 are CRC
                    raise SHT30Error(SHT30Error.CRC_ERROR)
            if data == bytearray(response_size):
                raise SHT30Error(SHT30Error.DATA_ERROR)
            return data
        except OSError as ex:
            if 'I2C' in ex.args[0]:
                raise SHT30Error(SHT30Error.BUS_ERROR)
            raise ex
    def clear_status(self):
        return self.send_cmd(SHT30.CLEAR_STATUS_CMD, None)
    def reset(self):
        return self.send_cmd(SHT30.RESET_CMD, None)
    def status(self, raw=False):
        data = self.send_cmd(SHT30.STATUS_CMD, 3, read_delay_ms=20)
        if raw:
            return data
        status_register = data[0] << 8 | data[1]
        return status_register
    def measure(self, raw=False):
        data = self.send_cmd(SHT30.MEASURE_CMD, 6)
        if raw:
            return data
        t_celsius = (((data[0] << 8 |  data[1]) * 175) / 0xFFFF) - 45 + self.delta_temp
        rh = (((data[3] << 8 | data[4]) * 100.0) / 0xFFFF) + self.delta_hum
        return t_celsius, rh
    def measure_int(self, raw=False):
        data = self.send_cmd(SHT30.MEASURE_CMD, 6)
        if raw:
            return data
        aux = (data[0] << 8 | data[1]) * 175
        t_int = (aux // 0xffff) - 45
        t_dec = (aux % 0xffff * 100) // 0xffff
        aux = (data[3] << 8 | data[4]) * 100
        h_int = aux // 0xffff
        h_dec = (aux % 0xffff * 100) // 0xffff
        return t_int, t_dec, h_int, h_dec

class SHT30Error(Exception):
    BUS_ERROR = 0x01
    DATA_ERROR = 0x02
    CRC_ERROR = 0x03
    def __init__(self, error_code=None):
        self.error_code = error_code
        super().__init__(self.get_message())
    def get_message(self):
        if self.error_code == SHT30Error.BUS_ERROR:
            return "Bus error"
        elif self.error_code == SHT30Error.DATA_ERROR:
            return "Data error"
        elif self.error_code == SHT30Error.CRC_ERROR:
            return "CRC error"
        else:
            return "Unknown error"
