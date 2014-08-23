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
from pybargain_protocol.tests.helpers import build_cancellation_message, build_valid_single_tx, build_proposal_message
from pybargain_protocol.tests.values import *


'''
SPECIFIC TEST VALUES
'''
VALID_MIN_SIG  = 'HFZ5NWF2w21jevd2xAdgqlBo0mcwk3PTMJ6D8fYY17F1VcQRknbcsy4AwatTvyWlkyFcLrO99hi+T4J4pjyuwc4='
VALID_FULL_SIG = 'G/eiIoEX9V8Wx5kyAJ5M6seRCur4neMm3bi/NXNOCKnqdvyT9t3NNTfVlRXR2qLHcDqiaTHjw5sxMu2d+Ik8NcE='


class TestBargainingCancellation(unittest.TestCase):

    def test_valid_min_unsigned(self):
        '''
        Tests validity of a minimal BargainingCancellation message (unsigned)
        '''
        # Builds a minimal message
        msg = build_cancellation_message(VALID_TIME4)
        # Gets the serialized message
        msg_ser = msg.pbuff        
        # Deserializes the message
        msg_deser = BargainingMessage.deserialize(msg_ser)
                
        # Checks
        self.assertTrue(msg.check_msg_fmt(TESTNET))
        self.assertTrue(msg_deser.check_msg_fmt(TESTNET))        

        self.assertEqual(msg_deser.msg_type, TYPE_BARGAIN_CANCELLATION)
        self.assertEqual(msg_deser.details_version, PROTOCOL_VERSION)
        self.assertEqual(msg_deser.sign_type, SIGN_NONE)
        self.assertEqual(msg_deser.sign_data, '')
        self.assertEqual(msg_deser.signature, '')
        self.assertEqual(msg_deser.pbuff, msg_ser)
        self.assertEqual(msg_deser.status, MSG_STATUS_OK)
        
        self.assertEqual(msg_deser.details.time, VALID_TIME4)
        self.assertEqual(msg_deser.details.buyer_data, '')
        self.assertEqual(msg_deser.details.seller_data, '')
        self.assertEqual(msg_deser.details.memo, '') 
        
        
    def test_valid_min_signed(self):
        '''
        Tests validity of a minimal BargainingCancellation message (signed)
        '''
        # Build a previous Proposal message 
        txs = build_valid_single_tx(VALID_AMOUNT2, VALID_FEES, VALID_OUTPUTS2)
        prev_msg = build_proposal_message(time=VALID_TIME3, transactions=txs, refund_to=VALID_REFUND_TO)
        # Builds a minimal message
        msg = build_cancellation_message(time=VALID_TIME4, sign_type=SIGN_ECDSA_SHA256, prev_msg=prev_msg)
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
        Tests validity of a full BargainingCancellation message (unsigned)
        '''
        # Builds a full message
        msg = build_cancellation_message(VALID_TIME4, VALID_BUYER_DATA, VALID_SELLER_DATA, VALID_MEMO)
        # Gets the serialized message
        msg_ser = msg.pbuff     
        # Deserializes the message
        msg_deser = BargainingMessage.deserialize(msg_ser)
        
        # Checks
        self.assertTrue(msg.check_msg_fmt(TESTNET))
        self.assertTrue(msg_deser.check_msg_fmt(TESTNET))       
        
        self.assertEqual(msg_deser.msg_type, TYPE_BARGAIN_CANCELLATION)
        self.assertEqual(msg_deser.details_version, PROTOCOL_VERSION)
        self.assertEqual(msg_deser.sign_type, SIGN_NONE)
        self.assertEqual(msg_deser.sign_data, '')
        self.assertEqual(msg_deser.signature, '')
        self.assertEqual(msg_deser.pbuff, msg_ser)
        self.assertEqual(msg_deser.status, MSG_STATUS_OK)
        
        self.assertEqual(msg_deser.details.time, VALID_TIME4)
        self.assertEqual(msg_deser.details.buyer_data, VALID_BUYER_DATA)
        self.assertEqual(msg_deser.details.seller_data, VALID_SELLER_DATA)
        self.assertEqual(msg_deser.details.memo, VALID_MEMO)    
       
    
    def test_valid_full_signed(self):
        '''
        Tests validity of a full BargainingCancellation message (signed)
        '''
        # Build a previous Proposal message 
        txs = build_valid_single_tx(VALID_AMOUNT2, VALID_FEES, VALID_OUTPUTS2)
        prev_msg = build_proposal_message(time=VALID_TIME3, transactions=txs, refund_to=VALID_REFUND_TO)
        # Builds a minimal message
        msg = build_cancellation_message(VALID_TIME4, VALID_BUYER_DATA, VALID_SELLER_DATA, 
                                         VALID_MEMO, SIGN_ECDSA_SHA256, prev_msg)
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
        msg = build_cancellation_message()
        self.assertIsNone(msg)
        
    
    def test_invalid_memo(self):
        '''
        Tests invalidity of a message with an invalid memo
        '''
        msg = build_cancellation_message(time=VALID_TIME4, memo=INVALID_MEMO)
        self.assertIsNone(msg)
        
    
    def test_invalid_sign(self):
        '''
        Tests invalidity of a message with an invalid signature
        '''
        # Build a previous Proposal message 
        txs = build_valid_single_tx(VALID_AMOUNT2, VALID_FEES, VALID_OUTPUTS2)
        prev_msg = build_proposal_message(time=VALID_TIME3, transactions=txs, refund_to=VALID_REFUND_TO)
        # Builds a minimal message
        msg = build_cancellation_message(time=VALID_TIME4, sign_type=SIGN_ECDSA_SHA256, prev_msg=prev_msg)
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