import random
from Crypto.Cipher import AES

class TxMessages():

    def auth_challenge_tx_message(self, challenge, transmitterId):
        hash = self.calculate_hash(challenge, transmitterId)
        return self.append_opcode(0x4, challenge)
    
    def auth_request_tx_message(self):
        token = bytearray(random.getrandbits(8) for i in range(8))
        data = self.append_opcode(0x1, token)
        data.append(0x2)
        return data
    
    def bond_request_tx_message(self):
        return bytearray([0x7])
        
    def disconnect_request_tx_message(self):
        return bytearray([0x9])
    
    def keep_alive_tx_message(self, time):
        return bytearray([0x6, time])
    
    def sensor_tx_message(self):
        return self.calc_crc_array(0x2e)
    
    def time_tx_message(self):
        return self.calc_crc_array(0x24)
    
    def unbond_tx_message(self):
        return bytearray([0x6])
    
    def append_opcode(self, opcode, value):
        arr = bytearray(value)
        # Assign opcode.
        arr.insert(0, opcode)
        return arr
       
    def match_ids(self, deviceId, serial):
        lastId = deviceId[-2:].upper()
        lastSerial = serial[-2:].upper()
        return lastId == lastSerial
        
    def calc_crc_array(self, b):
        crcShort = 0
        crcShort ^= (b & 0xff)
        crcShort ^= ((crcShort & 0xff) >> 4)
        crcShort ^= (crcShort << 12) & 0xffff
        crcShort ^= ((crcShort & 0xFF) << 5) & 0xffff
        crcShort &= 0xffff
        return bytearray([b, (crcShort & 0xff), (crcShort >> 8)])
        
    def calculate_hash(self, data, serial):
      secret_text = bytearray(data + data)
      key = b"00{0}00{0}".format(serial)
      
      e = AES.new(key, AES.MODE_ECB)
      return e.encrypt(buffer(secret_text))

class batteryMsg():
    UNKNOWN = 0
    BRICKED = 1
    LOW = 2
    OK = 3
    
    def getBatteryLevel(self, code):
        if code > 0x81:
            return self.BRICKED
        else:
            if code == 0x81:
                return self.LOW
            if code == 0x00:
                return self.OK
            else:
                return self.UNKNOWN

class authRxMsg():
    def __init__(self, packet):
        if (packet.count >= 3) and (packet[0] == 0x5):
            self.authenticated = packet[1]
            self.bonded = packet[2]
            
    @property
    def authenticated(self):
        return self.authenticated

    @property
    def bonded(self):
        return self.bonded

class authChallengeRxMsg():
    def __init__(self, packet):
        if (packet.count >= 17) and (packet[0] == 0x3):
            self.tokenHash = packet[1:9]
            self.challenge = packet[9:17]
            
    @property
    def challenge(self):
        return self.challenge

    @property
    def tokenHash(self):
        return self.tokenHash
   
class transRxMsg(batteryMsg):
    def __init__(self, packet):
        if (packet.count >= 10) and (packet[0] == 0x25):
            self.status = self.getBatteryLevel(packet[1])
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
    
class sensorRxMsg(batteryMsg):
    def __init__(self, packet):
        if (packet.count >= 14) and (packet[0] == 0x2f):
            self.status = self.getBatteryLevel(packet[1])
            self.timestamp = packet[2]
            self.unfiltered = packet[6]
            self.filtered = packet[10]
            
    @property
    def status(self):
        return self.status

    @property
    def timestamp(self):
        return self.timestamp

    @property
    def filtered(self):
        return self.filtered
        
    @property
    def unfiltered(self):
        return self.unfiltered