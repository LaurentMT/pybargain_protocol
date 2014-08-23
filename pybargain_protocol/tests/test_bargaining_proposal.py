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
from pybargain_protocol.tests.helpers import build_valid_single_tx, build_proposal_message, build_request_ack_message, build_unsigned_single_tx
from pybargain_protocol.tests.values import *



'''
SPECIFIC TEST VALUES
'''
VALID_MIN_SIG  = 'G2hoKHDmsSkxGgBGCtG5i848dhIu7KC2k0G80UdMgYTQjGYtLsnM6eQixwcUp0OTDSenqEjbxm8x/GsW8bHDkNA='
VALID_FULL_SIG = 'G4tshZ7kLc8iZvxIRSzRsbDED/Suz8j+5tdl1o650URXD8LIOBXR88KDLS4UGZIZ1wIOThNLty/fUabMBX11vVA='


class TestBargainingProposal(unittest.TestCase):
        
    def test_valid_min_unsigned(self):
        '''
        Tests validity of a minimal BargainingProposal message (unsigned)
        '''
        # Builds a minimal message
        txs = build_valid_single_tx(VALID_BUYER_AMOUNT, 0, VALID_OUTPUTS1)
        msg = build_proposal_message(time=VALID_TIME3, transactions=txs)
        # Gets the serialized message
        msg_ser = msg.pbuff        
        # Deserializes the message
        msg_deser = BargainingMessage.deserialize(msg_ser)
        
        # Checks
        self.assertTrue(msg.check_msg_fmt(TESTNET))
        self.assertTrue(msg_deser.check_msg_fmt(TESTNET))        

        self.assertEqual(msg_deser.msg_type, TYPE_BARGAIN_PROPOSAL)
        self.assertEqual(msg_deser.details_version, PROTOCOL_VERSION)
        self.assertEqual(msg_deser.sign_type, SIGN_NONE)
        self.assertEqual(msg_deser.sign_data, '')
        self.assertEqual(msg_deser.signature, '')
        self.assertEqual(msg_deser.pbuff, msg_ser)
        self.assertEqual(msg_deser.status, MSG_STATUS_OK)
        
        self.assertEqual(msg_deser.details.time, VALID_TIME3)
        self.assertEqual(msg_deser.details.buyer_data, '')
        self.assertEqual(msg_deser.details.seller_data, '')
        self.assertEqual(msg_deser.details.memo, '') 
        self.assertEqual(msg_deser.details.transactions, txs)
        
      
    def test_valid_min_signed(self):
        '''
        Tests validity of a minimal BargainingProposal message (signed)
        '''
        # Build a previous RequestACK message 
        prev_msg = build_request_ack_message(time=VALID_TIME2, outputs=VALID_OUTPUTS1)
        # Builds a minimal message
        txs = build_valid_single_tx(VALID_BUYER_AMOUNT, 0, VALID_OUTPUTS1)
        msg = build_proposal_message(time=VALID_TIME3, transactions=txs, sign_type=SIGN_ECDSA_SHA256, prev_msg=prev_msg)
        # Gets the serialized message
        msg_ser = msg.pbuff
        # Deserializes the message
        msg_deser = BargainingMessage.deserialize(msg_ser)
              
        # Checks
        self.assertEquals(msg.signature, VALID_MIN_SIG)   
        self.assertEquals(msg_deser.signature, VALID_MIN_SIG)   
        self.assertTrue(msg.check_signature(prev_msg))
        self.assertTrue(msg_deser.check_signature(prev_msg))   
        
         
    def test_valid_full_unsigned(self):
        '''
        Tests validity of a full BargainingProposal message (unsigned)
        '''
        # Builds a minimal message
        txs = build_valid_single_tx(VALID_BUYER_AMOUNT, 0, VALID_OUTPUTS1)
        msg = build_proposal_message(VALID_TIME3, VALID_BUYER_DATA, VALID_SELLER_DATA, txs,
                                     VALID_BUYER_AMOUNT, 0,VALID_MEMO, VALID_REFUND_TO, SIGN_NONE)
        # Gets the serialized message
        msg_ser = msg.pbuff        
        # Deserializes the message
        msg_deser = BargainingMessage.deserialize(msg_ser)
        
        # Checks
        self.assertTrue(msg.check_msg_fmt(TESTNET))
        self.assertTrue(msg_deser.check_msg_fmt(TESTNET))        

        self.assertEqual(msg_deser.msg_type, TYPE_BARGAIN_PROPOSAL)
        self.assertEqual(msg_deser.details_version, PROTOCOL_VERSION)
        self.assertEqual(msg_deser.sign_type, SIGN_NONE)
        self.assertEqual(msg_deser.sign_data, '')
        self.assertEqual(msg_deser.signature, '')
        self.assertEqual(msg_deser.pbuff, msg_ser)
        self.assertEqual(msg_deser.status, MSG_STATUS_OK)
        
        self.assertEqual(msg_deser.details.time, VALID_TIME3)
        self.assertEqual(msg_deser.details.buyer_data, VALID_BUYER_DATA)
        self.assertEqual(msg_deser.details.seller_data, VALID_SELLER_DATA)
        self.assertEqual(msg_deser.details.memo, VALID_MEMO) 
        self.assertEqual(msg_deser.details.transactions, txs)
      
    
    def test_valid_full_signed(self):
        '''
        Tests validity of a full BargainingProposal message (signed)
        '''
        # Build a previous RequestACK message 
        prev_msg = build_request_ack_message(time=VALID_TIME2, outputs=VALID_OUTPUTS1)
        # Builds a minimal message
        txs = build_valid_single_tx(VALID_BUYER_AMOUNT, 0, VALID_OUTPUTS1)
        msg = build_proposal_message(VALID_TIME3, VALID_BUYER_DATA, VALID_SELLER_DATA, txs,
                                     VALID_BUYER_AMOUNT, 0, VALID_MEMO, VALID_REFUND_TO,
                                     SIGN_ECDSA_SHA256, prev_msg)
        # Gets the serialized message
        msg_ser = msg.pbuff
        # Deserializes the message
        msg_deser = BargainingMessage.deserialize(msg_ser)
        
        # Checks
        self.assertTrue(msg.check_signature(prev_msg))
        self.assertTrue(msg_deser.check_signature(prev_msg))   
        self.assertEquals(msg.signature, VALID_FULL_SIG)   
        self.assertEquals(msg_deser.signature, VALID_FULL_SIG)   
    
    
    def test_invalid_memo(self):
        '''
        Tests invalidity of a message with an invalid memo
        '''
        txs = build_valid_single_tx(VALID_BUYER_AMOUNT, 0, VALID_OUTPUTS1)
        msg = build_proposal_message(time=VALID_TIME3, transactions=txs, memo=INVALID_MEMO)
        self.assertIsNone(msg)
    
     
    def test_invalid_time(self):
        '''
        Tests invalidity of a message with erroneous time
        '''
        txs = build_valid_single_tx(VALID_BUYER_AMOUNT, 0, VALID_OUTPUTS1)
        msg = build_proposal_message(transactions=txs)
        self.assertIsNone(msg)
    
    
    def test_invalid_sign(self):
        '''
        Tests invalidity of a message with an invalid signature
        '''
        # Build a previous RequestACK message 
        prev_msg = build_request_ack_message(time=VALID_TIME2, outputs=VALID_OUTPUTS1)
        # Builds a minimal message
        txs = build_valid_single_tx(VALID_BUYER_AMOUNT, 0, VALID_OUTPUTS1)
        msg = build_proposal_message(time=VALID_TIME3, transactions=txs, sign_type=SIGN_ECDSA_SHA256, prev_msg=prev_msg)
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
    
    
    def test_invalid_refund_to(self):
        '''
        Tests invalidity of a message with an invalid refund_to
        '''
        txs = build_valid_single_tx(VALID_AMOUNT1, 0, VALID_OUTPUTS1)
        msg = build_proposal_message(time=VALID_TIME3, transactions=txs, amount=VALID_AMOUNT1, fees=0, is_redeemable=True)
        self.assertIsNone(msg)
        
     
    def test_invalid_empty_txs(self):
        '''
        Tests invalidity of a message with an empty txs
        '''
        msg = build_proposal_message(time=VALID_TIME3, amount=VALID_AMOUNT1, fees=0)
        self.assertIsNone(msg)
        
    
    def test_invalid_txs(self):
        '''
        Tests invalidity of a message with an unsigned tx (unsigned tx)
        '''
        txs = build_unsigned_single_tx(VALID_AMOUNT1, 0, VALID_OUTPUTS1)
        msg = build_proposal_message(time=VALID_TIME3, transactions=txs, amount=VALID_AMOUNT1, fees=0)
        self.assertIsNone(msg)
        
   
if __name__ == '__main__':
    unittest.main()