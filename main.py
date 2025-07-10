import time
import serial
from backend.Packet import PacketProcessor

_port_name = "COM3"
_default_baud_rate = 115200

s = serial.Serial(port=_port_name, baudrate=_default_baud_rate)

_last_interval = 0

def on_interval(default_time = 1000):
  global _last_interval
  exceeds = ((time.time_ns() - _last_interval) > default_time)

  if exceeds:
    _last_interval = time.time_ns()

  return exceeds

class Packet:
  def __init__(self, id):
      self.id_ = id
  pass

if __name__ == '__main__':

  packet_p = PacketProcessor(s, b'\xff\xaa')

  while(1):

    if on_interval(1000):
      # pipe incoming bytes into buffer
      packet_p.process()
      pass
        
    pass

  s.close() 
