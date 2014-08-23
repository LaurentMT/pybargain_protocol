#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Version: 0.0.1
Python library for the bargaining protocol
'''

import json
import unittest
from pybargain_protocol.constants import *
from pybargain_protocol.bargaining_message import BargainingMessage
from pybargain_protocol.tests.helpers import build_request_message
from pybargain_protocol.tests.values import *


'''
SPECIFIC TEST VALUES
'''
VALID_MIN_SIG  = 'HCZz6iXxHYKF7QI2AjgrRvGL6diWpOo6Xt6QQC0S84c+5iWipHI2lJBFxjYvqrj0+PkhS635i5ZH6LUxGlKgGo0='
VALID_FULL_SIG = 'G+mkFz/B55pcpFJdLPPMPMlIoLmgrDERN9TFTlkNNR0sDe8AXmF/30xdp0U5ij6M5KM5S4uDzsdjwistbB+g+BE='



class TestBargainingRequest(unittest.TestCase):

    def test_valid_min_unsigned(self):
        '''
        Tests validity of a minimal BargainingRequest message (unsigned)
        '''
        # Builds a minimal message
        msg = build_request_message(VALID_TIME1)
        # Gets the serialized message
        msg_ser = msg.pbuff        
        # Deserializes the message
        msg_deser = BargainingMessage.deserialize(msg_ser)
                
        # Checks
        self.assertTrue(msg.check_msg_fmt(TESTNET))
        self.assertTrue(msg_deser.check_msg_fmt(TESTNET))        

        self.assertEqual(msg_deser.msg_type, TYPE_BARGAIN_REQUEST)
        self.assertEqual(msg_deser.details_version, PROTOCOL_VERSION)
        self.assertEqual(msg_deser.sign_type, SIGN_NONE)
        self.assertEqual(msg_deser.sign_data, '')
        self.assertEqual(msg_deser.signature, '')
        self.assertEqual(msg_deser.pbuff, msg_ser)
        self.assertEqual(msg_deser.status, MSG_STATUS_OK)
        
        self.assertEqual(msg_deser.details.time, VALID_TIME1)
        self.assertEqual(msg_deser.details.network, TESTNET)
        self.assertEqual(msg_deser.details.buyer_data, '')
        self.assertEqual(msg_deser.details.seller_data, '')
        self.assertEqual(msg_deser.details.expires, 0)
        self.assertEqual(msg_deser.details.bargaining_url, '') 
        
    
    def test_valid_min_signed(self):
        '''
        Tests validity of a minimal BargainingRequest message (signed)
        '''
        # Builds a minimal message
        msg = build_request_message(time=VALID_TIME1, sign_type=SIGN_ECDSA_SHA256)
        # Gets the serialized message
        msg_ser = msg.pbuff
        # Deserializes the message
        msg_deser = BargainingMessage.deserialize(msg_ser)
        
        # Checks
        self.assertTrue(msg.check_signature())
        self.assertTrue(msg_deser.check_signature())   
        self.assertEquals(msg.signature, VALID_MIN_SIG)   
        self.assertEquals(msg_deser.signature, VALID_MIN_SIG)     
    
    
    def test_valid_full_unsigned(self):
        '''
        Tests validity of a full BargainingRequest message (unsigned)
        '''
        # Builds a full message
        msg = build_request_message(VALID_TIME1, VALID_BUYER_DATA, VALID_SELLER_DATA, TESTNET, VALID_EXPIRES1, VALID_BARGAIN_URI1)
        # Gets the serialized message
        msg_ser = msg.pbuff     
        # Deserializes the message
        msg_deser = BargainingMessage.deserialize(msg_ser)
        
        # Checks
        self.assertTrue(msg.check_msg_fmt(TESTNET))
        self.assertTrue(msg_deser.check_msg_fmt(TESTNET))       
        
        self.assertEqual(msg_deser.msg_type, TYPE_BARGAIN_REQUEST)
        self.assertEqual(msg_deser.details_version, PROTOCOL_VERSION)
        self.assertEqual(msg_deser.sign_type, SIGN_NONE)
        self.assertEqual(msg_deser.sign_data, '')
        self.assertEqual(msg_deser.signature, '')
        self.assertEqual(msg_deser.pbuff, msg_ser)
        self.assertEqual(msg_deser.status, MSG_STATUS_OK)
        
        self.assertEqual(msg_deser.details.time, VALID_TIME1)
        self.assertEqual(msg_deser.details.network, TESTNET)
        self.assertEqual(msg_deser.details.buyer_data, VALID_BUYER_DATA)
        self.assertEqual(msg_deser.details.seller_data, VALID_SELLER_DATA)
        self.assertEqual(msg_deser.details.expires, VALID_EXPIRES1)
        self.assertEqual(msg_deser.details.bargaining_url, VALID_BARGAIN_URI1)     
        
    
    def test_valid_full_signed(self):
        '''
        Tests validity of a full BargainingRequest message (signed)
        '''
        # Builds a minimal message
        msg = build_request_message(VALID_TIME1, VALID_BUYER_DATA, VALID_SELLER_DATA, TESTNET,
                                    VALID_EXPIRES1, VALID_BARGAIN_URI1, SIGN_ECDSA_SHA256)
        # Gets the serialized message
        msg_ser = msg.pbuff
        # Deserializes the message
        msg_deser = BargainingMessage.deserialize(msg_ser)
        
        # Checks
        self.assertTrue(msg.check_signature())
        self.assertTrue(msg_deser.check_signature())  
        self.assertEquals(msg.signature, VALID_FULL_SIG)   
        self.assertEquals(msg_deser.signature, VALID_FULL_SIG)      
    
    
    def test_invalid_time(self):
        '''
        Tests invalidity of a message with erroneous time
        '''
        msg = build_request_message()
        self.assertIsNone(msg)
        
    
    def test_invalid_expires(self):
        '''
        Tests invalidity of a message with an invalid expires (before time)
        '''
        msg = build_request_message(time=VALID_TIME1, expires=INVALID_EXPIRES)
        self.assertIsNone(msg)
        
        
    def test_invalid_network(self):
        '''
        Tests invalidity of a message with an invalid network
        '''
        msg = build_request_message(time=VALID_TIME1, expires=INVALID_NETWORK)
        self.assertIsNone(msg)
        
        
    def test_invalid_sign(self):
        '''
        Tests invalidity of a message with an invalid signature
        '''
        msg = build_request_message(time=VALID_TIME1, sign_type=SIGN_ECDSA_SHA256)
        # Overrides the signature with an invalid one
        msg.signature = INVALID_SIG
        msg.pbuff = msg.serialize()
        # Gets the serialized message
        msg_ser = msg.pbuff
        # Deserializes the message
        msg_deser = BargainingMessage.deserialize(msg_ser)
        # Checks
        self.assertFalse(msg.check_signature())
        self.assertFalse(msg_deser.check_signature()) 
        
    
if __name__ == '__main__':
    unittest.main()