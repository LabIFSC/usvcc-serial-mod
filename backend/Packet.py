from serial import Serial

DEFAULT_PROC_MANIFEST = {
    "steps": {
      "sync" : {
        "byte_len": 2,
        "type": "bytes",
        "steps" : {}
      },
      "header" : {
        "byte_len": 4,
        "type" : "int",
        "steps" : {
          "proc_id" : {
            "byte_len" : 2,
            "type" : "int"
          },
          "proc_content_len" : {
            "byte_len": 0,
            "type": "int"
          }
        }
      },
      "content" : {
        "byte_len" : 0,
        "type": "undefined",
        "steps" : {}
      },
      "eol" : {
        "byte_len" : 3,
        "type" : "bytes",
        "steps" : {}
      }
    }
  }

class PacketBuffer:
  pass

class PacketProcessor:
  manifest: object = DEFAULT_PROC_MANIFEST
  serial: Serial
  
  signt_bytes: bytes = b'\xff\xaa'
  cfg_endianess = "little"

  # internal processing state
  current_step = "sync"

  current_packet_id = 0
  current_packet_size = 0

  current_packet_content = ""

  def __init__(self, serial, signature_bytes):
    self.serial = serial
    self.signt_bytes = signature_bytes  #todo: validate for max size of 2 bytes
    pass

  def process(self):
    # interact with serial buffer
    # pipe into a buffer till the packet is complete, then assemble a new packet
    # and pipe into a usable object for the program logic

    if (self.serial.in_waiting > 0):

      data = 0

      match self.current_step:
        case "sync":
          data = self.serial.read(size=2) # 2 8bit bytes

          if (data == self.signt_bytes):
            self.current_step = "header"
          pass
        
        case "header":
          data = self.serial.read(size=2) # ID: serialize as int
          self.current_packet_id = data
          print("ID: {0}".format(int.from_bytes(data, self.cfg_endianess)))

          # todo: check if an existing packet has the same ID
          # if it does, then skip the processing and wait for a new sync_byte sequence

          data = self.serial.read(size=2) # Content-Length: serialize as int
          data_int = int.from_bytes(data, self.cfg_endianess)
          self.current_packet_size = data
          print("Content Length: {0}".format(int.from_bytes(data, self.cfg_endianess)))

          self.current_step = "content"
          pass

        case "content":
          # read 1 byte at a time, increament read counter till it reaches
          # previously parsed 'Content-Length'
          data = self.serial.read(size=1)
          self.current_packet_content.append(data)
          print("Content: {0}".format(data))

          counter += 1
          if ((counter + 1) >= self.current_packet_size):
            # expected to be content padding byte
            data = self.serial.read(size=1)
            print("Content Padding: {0}".format(data))

            if (data == '\n'):
              self.current_packet_content.append('\0')
            # todo: pad content
            self.current_step = "eol"
          pass

        case "eol":
          data = self.serial.read(1)
          if data == '\n':
            # Packet streaming process completed with sucess
            print("EOL: {0}".format(data))
          # todo: clean up state
          # assemble complete packet and push into a packet buffer
          self.current_step = "sync"
          pass

      pass

      # check for sync bytes
      data = self.serial.read(size=2) # 2 8bit bytes

      # attempt to read remaining header
      if  data == self.signt_bytes:
        print("Sync bytes: {0}".format(data))

        data = self.serial.read(size=2)
        print("ID: {0}".format(int.from_bytes(data, self.cfg_endianess)))
        # todo: Hash map already received packets
        # if a packet with same id already has been received, skip

        data = self.serial.read(size=2)
        data_int = int.from_bytes(data, self.cfg_endianess)
        print("Content Length: {0}".format(int.from_bytes(data, self.cfg_endianess)))

        data = self.serial.read(size = data_int)
        print("Content: {0}".format(data))

        data = self.serial.read(1)
        print("Content Padding: {0}".format(data))

        data = self.serial.read(1)
        print("EOL: {0}".format(data))
        # data = s.read(1) # Attempt to read the next 4 bytes in the header
        # print("Header: {0}".format(data.decode("utf-8")))

      pass
    pass
  pass