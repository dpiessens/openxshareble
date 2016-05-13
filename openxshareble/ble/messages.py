

class messages():
    def auth_challenge_tx_message(challenge):
        return self.append_opcode(0x4, challenge)
    
    def auth_request_tx_message():
        token = sys.random(8)
        data = self.append_opcode(0x2, token)
        data.append(0x2)
        return data
    
    def bond_request_tx_message():
        return bytearray([0x7])
        
    def disconnect_request_tx_message():
        return bytearray([0x9])
    
    def keep_alive_tx_message(time):
        return bytearray([0x6, byte(time)])
    
    def sensor_tx_message():
        return self.calc_crc_array(0x2e)
    
    def time_tx_message():
        return self.calc_crc_array(0x24)
    
    def unbond_tx_message(time):
        return bytearray([0x6])
    
    def append_opcode(self, opcode, value):
        arr = bytearray(value)
        # Assign opcode.
        arr.insert(0, opcode)
        return arr
        
    def calc_crc_array(self, b):
        crcShort = 0
        crcShort ^= (b & 0xff)
        crcShort ^= ((crcShort & 0xff) >> 4)
        crcShort ^= (crcShort << 12) & 0xffff
        crcShort ^= ((crcShort & 0xFF) << 5) & 0xffff
        crcShort &= 0xffff
        return bytearray([b, (crcShort & 0xff), (crcShort >> 8)])
        
class transRxMsg():
    UNKNOWN = 0
    BRICKED = 1
    LOW = 2
    OK = 3

    def __init__(self, packet):
        if (packet.count >= 10) and (packet[0] == 0x25):
            self.status = getBatteryLevel(packet[1])
            self.currentTime = packet[2]
            self.sessionStartTime = packet[6]
            
    @property
    def status(self):
        return self.status

    @property
    def currentTime(self):
        return self.currentTime

    @property
    def sessionStartTime(self):
        return self.sessionStartTime
    
    def getBatteryLevel(self, code):
        if code > 0x81:
            return self.BRICKED
        else:
            if b == 0x81:
                return self.LOW
            if b == 0x00:
                return self.OK
            else:
                return self.UNKNOWN