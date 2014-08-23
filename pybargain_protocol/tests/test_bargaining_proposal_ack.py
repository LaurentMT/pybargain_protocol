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
from pybargain_protocol.tests.helpers import build_proposal_ack_message, build_valid_single_tx, build_proposal_message
from pybargain_protocol.tests.values import *


'''
SPECIFIC TEST VALUES
'''
VALID_MIN_SIG  = 'HIP3OB66458QSeMUyRGSiGfNLcDFGlafncIBOG2inwy2xofsWv33aSjgxELeul/byD+VHF9SaaXd5IzpxF2gG+o='
VALID_FULL_SIG = 'GwALqnKHUxQ3sGutO8AwAHA7ATRFss2QIKNSrcqajbJNp3N04sFhDenYO8X9RobiUF6icvMVcPUqwJuOlKlG2M8='


class TestBargainingProposalAck(unittest.TestCase):

    def test_valid_min_unsigned(self):
        '''
        Tests validity of a minimal BargainingProposalACK message (unsigned)
        '''
        # Builds a minimal message
        msg = build_proposal_ack_message(time=VALID_TIME4, outputs=VALID_OUTPUTS2)
        # Gets the serialized message
        msg_ser = msg.pbuff        
        # Deserializes the message
        msg_deser = BargainingMessage.deserialize(msg_ser)
                
        # Checks
        self.assertTrue(msg.check_msg_fmt(TESTNET))
        self.assertTrue(msg_deser.check_msg_fmt(TESTNET))        

        self.assertEqual(msg_deser.msg_type, TYPE_BARGAIN_PROPOSAL_ACK)
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
        self.assertEqual(msg_deser.details.outputs, VALID_OUTPUTS2)
        
    def test_valid_min_signed(self):
        '''
        Tests validity of a minimal BargainingProposalACK message (signed)
        '''
        # Build a previous Proposal message 
        txs = build_valid_single_tx(VALID_BUYER_AMOUNT, 0, VALID_OUTPUTS1)
        prev_msg = build_proposal_message(time=VALID_TIME3, transactions=txs)
        # Builds a minimal message
        msg = build_proposal_ack_message(time=VALID_TIME4, outputs=VALID_OUTPUTS2, 
                                         sign_type=SIGN_ECDSA_SHA256, prev_msg=prev_msg)
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
        Tests validity of a full BargainingProposalACK message (unsigned)
        '''
        # Builds a full message
        msg = build_proposal_ack_message(VALID_TIME4, VALID_BUYER_DATA, VALID_SELLER_DATA, VALID_OUTPUTS2, VALID_MEMO)
        # Gets the serialized message
        msg_ser = msg.pbuff     
        # Deserializes the message
        msg_deser = BargainingMessage.deserialize(msg_ser)
        
        # Checks
        self.assertTrue(msg.check_msg_fmt(TESTNET))
        self.assertTrue(msg_deser.check_msg_fmt(TESTNET))       
        
        self.assertEqual(msg_deser.msg_type, TYPE_BARGAIN_PROPOSAL_ACK)
        self.assertEqual(msg_deser.details_version, PROTOCOL_VERSION)
        self.assertEqual(msg_deser.sign_type, SIGN_NONE)
        self.assertEqual(msg_deser.sign_data, '')
        self.assertEqual(msg_deser.signature, '')
        self.assertEqual(msg_deser.pbuff, msg_ser)
        self.assertEqual(msg_deser.status, MSG_STATUS_OK)
        
        self.assertEqual(msg_deser.details.time, VALID_TIME4)
        self.assertEqual(msg_deser.details.buyer_data, VALID_BUYER_DATA)
        self.assertEqual(msg_deser.details.seller_data, VALID_SELLER_DATA)
        self.assertEqual(msg_deser.details.outputs, VALID_OUTPUTS2)
        self.assertEqual(msg_deser.details.memo, VALID_MEMO)    
       
    
    def test_valid_full_signed(self):
        '''
        Tests validity of a full BargainingRequestACK message (signed)
        '''
        # Build a previous Proposal message 
        txs = build_valid_single_tx(VALID_BUYER_AMOUNT, 0, VALID_OUTPUTS1)
        prev_msg = build_proposal_message(time=VALID_TIME3, transactions=txs)
        # Builds a minimal message
        msg = build_proposal_ack_message(VALID_TIME4, VALID_BUYER_DATA, 
                                         VALID_SELLER_DATA, VALID_OUTPUTS2, 
                                         VALID_MEMO, SIGN_ECDSA_SHA256,
                                         prev_msg)
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
        msg = build_proposal_ack_message(outputs=VALID_OUTPUTS2)
        self.assertIsNone(msg)
        
    
    def test_invalid_memo(self):
        '''
        Tests invalidity of a message with an invalid memo
        '''
        msg = build_proposal_ack_message(time=VALID_TIME4, outputs=VALID_OUTPUTS2, memo=INVALID_MEMO)
        self.assertIsNone(msg)
        
    
    def test_invalid_outputs(self):
        '''
        Tests invalidity of a message with invalid outputs
        '''
        msg = build_proposal_ack_message(time=VALID_TIME4, outputs=INVALID_OUTPUTS)
        self.assertIsNone(msg)
             
             
    def test_invalid_sign(self):
        '''
        Tests invalidity of a message with an invalid signature
        '''
        # Build a previous Proposal message 
        txs = build_valid_single_tx(VALID_BUYER_AMOUNT, 0, VALID_OUTPUTS1)
        prev_msg = build_proposal_message(time=VALID_TIME3, transactions=txs)
        msg = build_proposal_ack_message(time=VALID_TIME4, outputs=VALID_OUTPUTS2, 
                                         sign_type=SIGN_ECDSA_SHA256, prev_msg=prev_msg)
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