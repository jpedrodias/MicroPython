# filename: sensors/sensor_ds18b20.py
# WEMOS D1 Mini Board GPIO Map: D8 pull_down, D4 pull_down
# D0=16, D1=5, D2=4, D3=0, D4=2, D5=14, D6=12, D7=13, D8=15
import machine, time

class Sensor_DS18B20():
  def __init__(self, pin):
    if not isinstance(pin, int):
      raise TypeError('pin must be integer')
    
    from onewire import OneWire
    from ds18x20 import DS18X20
    ow = OneWire(machine.Pin(ds18b20_pin)) 
    ow.scan()
    ow.reset()
    self.ds18b20 = DS18X20(ow)
    self.roms = self.ds18b20.scan()
    self.temps = [None for rom in self.roms]
  def read(self):
    self.ds18b20.convert_temp()
    time.sleep_ms(750)
    for i, rom in enumerate(self.roms):
      t = self.ds18b20.read_temp(rom)
      self.temps[i] = round(t, 1)
    return self.temps
  @property
  def values(self):
    return self.temps
  @property
  def values_dict(self):
    temps_dict = {}
    for i, value in enumerate(self.temps):
      temps_dict['t{}'.format(i)] = value
    return temps_dict
#End of Sensor_DS18B20
