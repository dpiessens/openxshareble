import unittest
from messages import TxMessages
from messages import batteryMsg
from messages import authRxMsg
from messages import authChallengeRxMsg
from messages import transRxMsg
from messages import sensorRxMsg

class TestTxMessages(unittest.TestCase):

    def test_auth_request_tx_message(self):
        result = TxMessages().auth_request_tx_message()
        self.assertEqual(len(result), 10)
        self.assertEqual(result[0], 0x1)
        self.assertEqual(result[9], 0x2)

    def test_auth_challenge_tx_message(self):
        result = TxMessages().auth_challenge_tx_message("ABCD1234", "408S29")
        self.assertEqual(len(result), 9)
        self.assertEqual(result[0], 0x4)
    
    def test_bond_request_tx_message(self):
        result = TxMessages().bond_request_tx_message()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], 0x7)
        
    def test_sensor_tx_message(self):
        result = TxMessages().sensor_tx_message()
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], 0x2e)

    def test_keep_alive_tx_message(self):
        result = TxMessages().keep_alive_tx_message(25)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], 0x6)
        self.assertEqual(result[1], 25)
    
    def test_match_ids(self):
        result = TxMessages().match_ids("68:94:23:EB:F6:2D", "401F2D")
        self.assertTrue(result)
        
        resultNoMatch = TxMessages().match_ids("68:94:23:EB:F6:2D", "401F1F")
        self.assertFalse(resultNoMatch)
        
    def test_time_tx_message(self):
        result = TxMessages().time_tx_message()
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], 0x24)
        
    def test_unbond_tx_message(self):
        result = TxMessages().unbond_tx_message()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], 0x6)
        
    def test_batteryMsg_modes(self):
        btryMsg = batteryMsg()
        
        resultOK = btryMsg.getBatteryLevel(0x00)
        self.assertEqual(resultOK, btryMsg.OK)
               
        resultBricked = btryMsg.getBatteryLevel(0x82)
        self.assertEqual(resultBricked, btryMsg.BRICKED)
        
        resultLow = btryMsg.getBatteryLevel(0x81)
        self.assertEqual(resultLow, btryMsg.LOW)
        
        resultUnknown = btryMsg.getBatteryLevel(0x5)
        self.assertEqual(resultUnknown, btryMsg.UNKNOWN)
        
    def test_authRxMsg(self):
        authMsg = authRxMsg(bytearray([0x5, 0x1, 0x1]))
                
        self.assertEqual(1, authMsg.authenticated)
        self.assertEqual(1, authMsg.bonded)
    
    def test_authChallengeRxMsg(self):
        authMsg = authChallengeRxMsg(bytearray([0x3, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x5, 0x5, 0x5, 0x5, 0x5, 0x5, 0x5, 0x5]))
                
        self.assertEqual(bytearray(b'\x01\x01\x01\x01\x01\x01\x01\x01'), authMsg.tokenHash)
        self.assertEqual(bytearray(b'\x05\x05\x05\x05\x05\x05\x05\x05'), authMsg.challenge)
        
    def test_transRxMsg(self):
        transMsg = transRxMsg(bytearray([0x25, 0x00, 0x25, 0x1, 0x0, 0x0, 0x29, 0x1, 0x1, 0x1]))
                
        self.assertEqual(transMsg.OK, transMsg.status)
        self.assertEqual(0x25, transMsg.currentTime)
        self.assertEqual(0x29, transMsg.sessionStartTime)

    def test_sensorRxMsg(self):
        sensorMsg = sensorRxMsg(bytearray([0x2f, 0x81, 0x25, 0x1, 0x0, 0x0, 0x29, 0x1, 0x1, 0x1, 0x2, 0x1, 0x1, 0x1]))
                
        self.assertEqual(sensorMsg.LOW, sensorMsg.status)
        self.assertEqual(0x25, sensorMsg.timestamp)
        self.assertEqual(0x2, sensorMsg.filtered)
        self.assertEqual(0x29, sensorMsg.unfiltered)
        