#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Version: 0.0.1
Python library for the bargaining protocol
'''

import json
import unittest
from bitcoin import *
from pybargain_protocol.constants import *
from pybargain_protocol.bargaining_message import BargainingMessage
from pybargain_protocol.tests.helpers import build_request_ack_message, build_request_message
from pybargain_protocol.tests.values import *


'''
SPECIFIC TEST VALUES
'''
VALID_MIN_SIG  = 'G8ydQ6wZluax1TIACG4RMpB6/ZXPkEEbvTZcnbCQ22V1eELOt40+1u+H/+K2ueLflnG+a/Qtaqn8FwBI8ZVXilU='
VALID_FULL_SIG = 'G3Bvd3WdCMYHtNDdmMlsmcGwA2BoP6JJVTHet3TWsDa7VQzY/lPfdVwP/6XQBARnvXZYo23N3WPyBM3C7YtVYxw='



class TestBargainingRequestAck(unittest.TestCase):

    def test_valid_min_unsigned(self):
        '''
        Tests validity of a minimal BargainingRequestACK message (unsigned)
        '''
        # Builds a minimal message
        msg = build_request_ack_message(time=VALID_TIME2, outputs=VALID_OUTPUTS1)
        # Gets the serialized message
        msg_ser = msg.pbuff        
        # Deserializes the message
        msg_deser = BargainingMessage.deserialize(msg_ser)
                
        # Checks
        self.assertTrue(msg.check_msg_fmt(TESTNET))
        self.assertTrue(msg_deser.check_msg_fmt(TESTNET))        

        self.assertEqual(msg_deser.msg_type, TYPE_BARGAIN_REQUEST_ACK)
        self.assertEqual(msg_deser.details_version, PROTOCOL_VERSION)
        self.assertEqual(msg_deser.sign_type, SIGN_NONE)
        self.assertEqual(msg_deser.sign_data, '')
        self.assertEqual(msg_deser.signature, '')
        self.assertEqual(msg_deser.pbuff, msg_ser)
        self.assertEqual(msg_deser.status, MSG_STATUS_OK)
        
        self.assertEqual(msg_deser.details.time, VALID_TIME2)
        self.assertEqual(msg_deser.details.network, TESTNET)
        self.assertEqual(msg_deser.details.buyer_data, '')
        self.assertEqual(msg_deser.details.seller_data, '')
        self.assertEqual(msg_deser.details.expires, 0)
        self.assertEqual(msg_deser.details.bargaining_url, '') 
        self.assertEqual(msg_deser.details.memo, '') 
        self.assertEqual(msg_deser.details.outputs, VALID_OUTPUTS1)
        
        
    def test_valid_min_signed(self):
        '''
        Tests validity of a minimal BargainingRequestACK message (signed)
        '''
        # Builds the previous msg
        prev_msg = build_request_message(time=VALID_TIME1)
        # Builds a minimal message
        msg = build_request_ack_message(time=VALID_TIME2, outputs=VALID_OUTPUTS1, sign_type=SIGN_ECDSA_SHA256, prev_msg=prev_msg)
        # Gets the serialized message
        msg_ser = msg.pbuff
        # Deserializes the message
        msg_deser = BargainingMessage.deserialize(msg_ser)
        
        # Checks
        self.assertTrue(msg.check_signature(prev_msg))
        self.assertTrue(msg_deser.check_signature(prev_msg))   
        self.assertEquals(msg.signature, VALID_MIN_SIG)   
        self.assertEquals(msg_deser.signature, VALID_MIN_SIG)     
        
    
    def test_valid_full_unsigned(self):
        '''
        Tests validity of a full BargainingRequest message (unsigned)
        '''
        # Builds a full message
        msg = build_request_ack_message(VALID_TIME2, VALID_BUYER_DATA, VALID_SELLER_DATA, 
                                        TESTNET, VALID_EXPIRES2, VALID_BARGAIN_URI2,
                                        VALID_OUTPUTS1, VALID_MEMO)
        # Gets the serialized message
        msg_ser = msg.pbuff     
        # Deserializes the message
        msg_deser = BargainingMessage.deserialize(msg_ser)
        
        # Checks
        self.assertTrue(msg.check_msg_fmt(TESTNET))
        self.assertTrue(msg_deser.check_msg_fmt(TESTNET))       
        
        self.assertEqual(msg_deser.msg_type, TYPE_BARGAIN_REQUEST_ACK)
        self.assertEqual(msg_deser.details_version, PROTOCOL_VERSION)
        self.assertEqual(msg_deser.sign_type, SIGN_NONE)
        self.assertEqual(msg_deser.sign_data, '')
        self.assertEqual(msg_deser.signature, '')
        self.assertEqual(msg_deser.pbuff, msg_ser)
        self.assertEqual(msg_deser.status, MSG_STATUS_OK)
        
        self.assertEqual(msg_deser.details.time, VALID_TIME2)
        self.assertEqual(msg_deser.details.network, TESTNET)
        self.assertEqual(msg_deser.details.buyer_data, VALID_BUYER_DATA)
        self.assertEqual(msg_deser.details.seller_data, VALID_SELLER_DATA)
        self.assertEqual(msg_deser.details.expires, VALID_EXPIRES2)
        self.assertEqual(msg_deser.details.bargaining_url, VALID_BARGAIN_URI2)   
        self.assertEqual(msg_deser.details.outputs, VALID_OUTPUTS1)
        self.assertEqual(msg_deser.details.memo, VALID_MEMO)    
       
    
    def test_valid_full_signed(self):
        '''
        Tests validity of a full BargainingRequestACK message (signed)
        '''
        # Builds the previous msg
        prev_msg = build_request_message(time=VALID_TIME1)
        # Builds a minimal message
        msg = build_request_ack_message(VALID_TIME2, VALID_BUYER_DATA, VALID_SELLER_DATA, 
                                        TESTNET, VALID_EXPIRES2, VALID_BARGAIN_URI2, 
                                        VALID_OUTPUTS1, VALID_MEMO, SIGN_ECDSA_SHA256, prev_msg)
        # Gets the serialized message
        msg_ser = msg.pbuff
        # Deserializes the message
        msg_deser = BargainingMessage.deserialize(msg_ser)
        
        # Checks
        self.assertTrue(msg.check_signature(prev_msg))
        self.assertTrue(msg_deser.check_signature(prev_msg))  
        self.assertEquals(msg.signature, VALID_FULL_SIG)   
        self.assertEquals(msg_deser.signature, VALID_FULL_SIG)      
    
    
    def test_invalid_time(self):
        '''
        Tests invalidity of a message with erroneous time
        '''
        msg = build_request_ack_message()
        self.assertIsNone(msg)
        
    
    def test_invalid_expires(self):
        '''
        Tests invalidity of a message with an invalid expires (before time)
        '''
        msg = build_request_ack_message(time=VALID_TIME2, outputs=VALID_OUTPUTS1, expires=INVALID_EXPIRES)
        self.assertIsNone(msg)
        
        
    def test_invalid_network(self):
        '''
        Tests invalidity of a message with an invalid network
        '''
        msg = build_request_ack_message(time=VALID_TIME2, outputs=VALID_OUTPUTS1, network=INVALID_NETWORK)
        self.assertIsNone(msg)
        
    
    def test_invalid_memo(self):
        '''
        Tests invalidity of a message with an invalid memo
        '''
        msg = build_request_ack_message(time=VALID_TIME2, outputs=VALID_OUTPUTS1, memo=INVALID_MEMO)
        self.assertIsNone(msg)
        
    
    def test_invalid_outputs(self):
        '''
        Tests invalidity of a message with invalid outputs
        '''
        msg = build_request_ack_message(time=VALID_TIME2, outputs=INVALID_OUTPUTS)
        self.assertIsNone(msg)
             
        
    def test_invalid_sign(self):
        '''
        Tests invalidity of a message with an invalid signature
        '''
        prev_msg = build_request_message(time=VALID_TIME1)
        msg = build_request_ack_message(time=VALID_TIME2, outputs=VALID_OUTPUTS1, sign_type=SIGN_ECDSA_SHA256, prev_msg=prev_msg)
        # Overrides the signature with an invalid one
        msg.signature = INVALID_SIG
        msg.pbuff = msg.serialize()
        # Gets the serialized message
        msg_ser = msg.pbuff
        # Deserializes the message
        msg_deser = BargainingMessage.deserialize(msg_ser)
        # Checks
        self.assertFalse(msg.check_signature(prev_msg))
        self.assertFalse(msg_deser.check_signature(prev_msg)) 
    
    
if __name__ == '__main__':
    unittest.main()