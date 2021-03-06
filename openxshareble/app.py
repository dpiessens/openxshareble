
import Adafruit_BluefruitLE
from Adafruit_BluefruitLE.services import UART as OriginalUART
# from ble import uart
from ble.uart import G5UART as UART
from ble.readdata import Device
import time
import atexit

class App (object):
  """ A high level application object.

  Any application needing to talk to Dexcom G5 will need
  to perform operations to setup the ble data transport.  This class
  mixes the UART, ble code, and provides helpful prolog and epilog
  routines that run before and after main, respectively.
  """
  def __init__ (self, **kwds):
    self.disconnect_on_after = kwds.get('disconnect_on_after', False)
    pass
  def setup_ble (self):
    # create console handler and set level to debug for diagnostics

    self.remote = None
    self.ble = Adafruit_BluefruitLE.get_provider()
    # Initialize the BLE system.  MUST be called before other BLE calls!
    self.ble.initialize()
    # Get the first available BLE network adapter and make sure it's powered on.
    self.adapter = self.ble.get_default_adapter()
    self.adapter.power_on()
    print('Using adapter: {0}'.format(self.adapter.name))
    self.dexcom = None
    pass
  def setup_dexcom (self, serial=None, mac=None):
    # Once connected do everything else in a try/finally to make sure the device
    # is disconnected when done.
    try:
        # Wait for service discovery to complete for the UART service.  Will
        # time out after 60 seconds (specify timeout_sec parameter to override).
        # print device._device.GattServices
        print('Discovering services...')
        UART.discover(self.remote)

        # Once service discovery is complete create an instance of the service
        # and start interacting with it.
        self.uart = UART(self.remote, SERIAL=serial)


        self.dexcom = Device(self.uart)
        print "DEXCOM", self.dexcom
        if not self.dexcom:
          self.dexcom = Device(self.uart)
    except:
        # Make sure device is disconnected on exit.
        if self.disconnect_on_after and (self.remote is not None):
          self.remote.disconnect()
  def prolog (self, clear_cached_data=True, disconnect_devices=False, scan_devices=True, connect=True, mac=None, serial=None):
    """
    Things to do before running the main part of the application.
    """
    # Clear any cached data because both bluez and CoreBluetooth have issues with
    # caching data and it going stale.
    if clear_cached_data:
      self.ble.clear_cached_data()


    if disconnect_devices:
      # Disconnect any currently connected UART devices.  Good for cleaning up and
      # starting from a fresh state.
      print('Disconnecting any connected UART devices...')
      UART.disconnect_devices()

    if scan_devices:
      # Scan for UART devices.
      print('Searching for UART device...')
      try:
          if mac:
            print('Searching for MAC: {0}'.format(mac))
            self.remote = self.select_mac(mac=mac, serial=serial)
          else:
            print 'Starting device scan...'
            print('Using adapter: {0}'.format(self.adapter.name))
            self.adapter.start_scan()
            atexit.register(self.adapter.stop_scan)
            # Search for the first UART device found (will time out after 60 seconds
            # but you can specify an optional timeout_sec parameter to change it).
            self.remote = UART.find_device()
          if self.remote is None:
              raise RuntimeError('Failed to find UART device!')
              return
      finally:
          # Make sure scanning is stopped before exiting.
          if self.adapter.is_scanning:
            self.adapter.stop_scan()

    if connect and not self.remote.is_connected:
      print('Connecting to device...')
      self.remote.connect()  # Will time out after 60 seconds, specify timeout_sec parameter
                        # to change the timeout.
    print(self.parse_device_name(self.remote))
    # device._device.Pair( )
    print(self.ble._print_tree( ))
    for service in self.remote.list_services( ):
      print(service, service.uuid)
    print("ADVERTISED")
    print(self.remote.advertised)

    pass
  def parse_device_name(self, device):
    try:
      return device.name
    except:
      return device.id

  def select_mac (self, mac=None, serial=None, **kwds):
    for device in self.enumerate_dexcoms(mac, **kwds):
      deviceStr = str(device.id)
      if (deviceStr == mac) or (self.match_ids(deviceStr, serial)):
        print 'Device matches: ', deviceStr
        return device
        
  def match_ids(self, deviceId, serial):
        lastId = deviceId[-2:].upper()
        lastSerial = serial[-2:].upper()
        return lastId == lastSerial
        
  def enumerate_dexcoms (self, mac=None, timeout_secs=120):
    start = time.time()
    known_uarts = set()
    print('Searching for UART devices for {0} seconds...'.format(timeout_secs))
    self.adapter.start_scan()
        
    while (time.time() - start) < timeout_secs:
      
      print 'Active scanning:'      
      # Enter a loop and print out whenever a new UART device is found.
      nestStart = time.time()
      while (time.time() - nestStart) < 30:
          
          # Call UART.find_devices to get a list of any UART devices that
          # have been found.  This call will quickly return results and does
          # not wait for devices to appear.
          found = set(UART.find_devices())
          # Check for new devices that haven't been seen yet and print out
          # their name and ID (MAC address on Linux, GUID on OSX).
          new = found - known_uarts
          hasMac = False
          for device in new:
              deviceId = str(device.id)
              print('Found UART: {0} [{1}]'.format(deviceId, self.parse_device_name(device)))
              if mac == deviceId:
                print time.time()
                self.adapter.stop_scan()
                hasMac = True

          known_uarts.update(new)
          if hasMac:
            return known_uarts
          # Sleep for a second and see if new devices have appeared.
          time.sleep(1.0)
          now = time.time( )
      
      print 'Pausing for 20 sec...'
      time.sleep(20.0)

    self.adapter.stop_scan()
    return known_uarts

  def epilog (self):
    """
    Things to do after running the main part of the application.
    """
    # Make sure device is disconnected on exit.
    if self.disconnect_on_after and self.remote.is_connected:
      self.remote.disconnect()
    # self.ble._gobject_mainloop.quit( )
    pass
  def set_handler (self, handler):
    self.handler = handler
  def run (self):
    self.ble.run_mainloop_with(self.main)
    pass
  def main (self):
    """
    Subclasses should replace this method.
    """
