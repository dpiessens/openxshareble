
import Adafruit_BluefruitLE
from Adafruit_BluefruitLE.services.servicebase import ServiceBase
import Queue
import uuid
import time
from attrs import Attrs
from messages import TxMessages
from messages import batteryMsg
from messages import authRxMsg
from messages import authChallengeRxMsg
from messages import transRxMsg
from messages import sensorRxMsg 

class G5UART (ServiceBase):
  ADVERTISED = []
  SERVICES = [Attrs.CGMService]
  CHARACTERISTICS = [Attrs.Authentication, Attrs.Control, Attrs.Communication ]

  UART_SERVICE_UUID = Attrs.CGMService
  AuthUUID    = Attrs.Authentication
  ControlUUID  = Attrs.Control
  CommunicationUUID = Attrs.Communication
  
  def __init__(self, device, **kwds):
      """Initialize UART from provided bluez device."""
      # Find the UART service and characteristics associated with the device.
      print 'Adversisement: ', ADVERTISED
      self._uart = device.find_service(self.UART_SERVICE_UUID)
      print self._uart
      self._queue = Queue.Queue()
      r = device.is_paired
      self.serial = kwds.pop('SERIAL', None)
      print "paired?", r
      if not r:
        print "pairing ", device.id, "..."
        device.pair( )
        print "paired"
        print device.advertised
        print "finding service"
        self._uart = device.find_service(self.UART_SERVICE_UUID)
        print "SERVICE", self._uart
      for svc in device.list_services( ):
        print svc.uuid, svc.uuid == self.UART_SERVICE_UUID, svc, svc._service
        print "CHARACTERISTICS"
        chrsts = svc.list_characteristics( )
        for chtr in chrsts:
          print chtr.uuid, chtr, chtr._characteristic
      # setup characistics
      self.setup_dexcom( )
  
  def set_serial (self, SERIAL):
    self.serial = SERIAL
  
  def _auth_received (self, data):
    print "Auth Challenge Data: {0}".format(data)
    authRxChallenge = authChallengeRxMsg(data)
    print "Auth Challenge: {0}".format(authRxChallenge.challenge)
    authTxChallenge = TxMessages().auth_challenge_tx_message(authRxChallenge.challenge, self.serial)
    print "Auth Transmit Challenge: ", authTxChallenge
    self._auth.write_value(authTxChallenge)
    
  def setup_dexcom (self):
    self.remainder = bytearray( )
    self._auth = self._uart.find_characteristic(self.AuthUUID)
    self._rx = self._uart.find_characteristic(self.CommunicationUUID)
    # Use a queue to pass data received from the RX property change back to
    # the main thread in a thread-safe way.
    if self._auth.notifying:
      self._auth.stop_notify( )
    if not self._auth.notifying:
      self._auth.start_notify(self._auth_received)
    
    if self._rx.notifying:
      self._rx.stop_notify( )
    if not self._rx.notifying:
      self._rx.start_notify(self._rx_received)
      
  def _heartbeat_tick (self, data):
    print "_heartbeat_tick", str(data).encode('hex')
  
  def _on_rcv (self, data):
    print "_on_rcv", str(data).encode('hex')

  def read (self, size=1, timeout_sec=None):
    spool = bytearray( )
    spool.extend(self.remainder)
    self.remainder = bytearray( )
    while len(spool) < size:
      spool.extend(self.pop(timeout_sec=timeout_sec))
      time.sleep(.100)
    self.remainder.extend(spool[size:])
    return str(spool[:size])
  def pop (self, timeout_sec=None):
    return super(G5UART, self).read(timeout_sec=timeout_sec)