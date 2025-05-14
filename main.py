import time
import serial
from backend.Packet import PacketProcessor

_port_name = "COM3"
_default_bauld_rate = 115200

s = serial.Serial(port=_port_name, baudrate=_default_bauld_rate)

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

  processing_header = False
  processing_content = False

  new_packet = False

  packet_p = PacketProcessor(s)

  while(1):

    if on_interval(1000):
      # pipe incoming bytes into buffer
      PacketProcessor.process()
      pass
        
    pass

  s.close() 