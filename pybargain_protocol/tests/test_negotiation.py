#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Version: 0.0.1
Python library for the bargaining protocol
'''
import unittest
from pybargain_protocol.negotiation import Negotiation
from pybargain_protocol.constants import *
from pybargain_protocol.bargaining_request import BargainingRequestDetails
from pybargain_protocol.bargaining_message import BargainingMessage
from pybargain_protocol.bargaining_request_ack import BargainingRequestACKDetails
from pybargain_protocol.bargaining_proposal import BargainingProposalDetails
from pybargain_protocol.tests.helpers import build_valid_single_tx
from pybargain_protocol.helpers.bc_api import blockr_sum_unspent_inputs
from pybargain_protocol.bargaining_proposal_ack import BargainingProposalACKDetails
from pybargain_protocol.bargaining_completion import BargainingCompletionDetails
from pybargain_protocol.tests.values import *



class TestNegotiation(unittest.TestCase):
    
    def test_full_nego(self):
        wire = None
        nego_buyer = None
        nego_seller = None
        
        '''
        BUYER SENDS A REQUEST
        '''
        network = TESTNET
        nego_buyer = Negotiation(role=ROLE_BUYER, network=network)
        
        dtls = BargainingRequestDetails(VALID_TIME1, VALID_BUYER_DATA, VALID_SELLER_DATA, 
                                        network, VALID_EXPIRES1, VALID_BARGAIN_URI1)  
        msg = BargainingMessage(TYPE_BARGAIN_REQUEST, dtls)
        
        check_format = msg.check_msg_fmt(network)
        self.assertTrue(check_format)
        
        if check_format:
            msg.sign(None, SIGN_ECDSA_SHA256, TEST_PUB1, TEST_PRIV1)
            check_consistency = nego_buyer.check_consistency(msg)
            self.assertTrue(check_consistency)  
            if check_consistency:    
                msg.pbuff = msg.serialize()
                nego_buyer.append(msg)
                wire = msg.pbuff
            else:
                wire = None
        else:
            wire = None


        '''
        SELLER RECEIVES THE REQUEST
        '''
        self.assertIsNotNone(wire)
        network = msg.details.network
        
        msg = BargainingMessage.deserialize(wire)
        
        check_format = msg.check_msg_fmt(network)
        self.assertTrue(check_format)
        
        if check_format:
            nego_seller = Negotiation(role=ROLE_SELLER, network=network)  
            check_consistency = nego_seller.check_consistency(msg)
            self.assertTrue(check_consistency)  
            nego_seller.append(msg)
         
                    
        '''
        SELLER SENDS A REQUEST ACK
        '''    
        network = nego_seller.network
        last_msg = nego_seller.get_last_msg()
        
        dtls = BargainingRequestACKDetails(VALID_TIME2, VALID_BUYER_DATA, VALID_SELLER_DATA, 
                                           network, VALID_EXPIRES2, VALID_BARGAIN_URI2, 
                                           VALID_OUTPUTS1, VALID_MEMO) 
        msg = BargainingMessage(TYPE_BARGAIN_REQUEST_ACK, dtls)
        
        check_format = msg.check_msg_fmt(network)
        self.assertTrue(check_format)
        
        if check_format:        
            msg.sign(last_msg, SIGN_ECDSA_SHA256, TEST_PUB2, TEST_PRIV2)
            check_consistency = nego_seller.check_consistency(msg)
            self.assertTrue(check_consistency)  
            if check_consistency:    
                msg.pbuff = msg.serialize()
                nego_seller.append(msg)
                wire = msg.pbuff
            else:
                wire = None
        else:
            wire = None    
                
        
        '''
        BUYER RECEIVES THE REQUEST ACK
        '''  
        self.assertIsNotNone(wire)
        network = nego_buyer.network
        
        msg = BargainingMessage.deserialize(wire)
        
        already_received = nego_buyer.already_received(msg)
        self.assertFalse(already_received)
        if not already_received:
            check_format = msg.check_msg_fmt(network)
            self.assertTrue(check_format)
            if check_format:
                check_consistency = nego_buyer.check_consistency(msg)
                self.assertTrue(check_consistency)  
                nego_buyer.append(msg) 
            
        
        '''
        CHECKS CASE : BUYER RECEIVES THE SAME REQUEST ACK
        ''' 
        already_received = nego_buyer.already_received(msg)
        self.assertTrue(already_received)                  
        
        
        '''
        BUYER SENDS A PROPOSAL
        '''    
        network = nego_buyer.network
        last_msg = nego_buyer.get_last_msg()
        
        txs = build_valid_single_tx(VALID_BUYER_AMOUNT, 0, VALID_OUTPUTS1)
        #txs = ['0100000001bb208a92f55b75bd126d88e3eaa1d9b6ec3b2593d0e617370e9874bf62a6de26010000008c493046022100803ec4562ab5cfda828309e43feb5691d5fd95b6c228432b32fdd19143c4fdce022100e96dce89f4e44fe8ea25d55db08d00ac9ef9c09a0debd9d846e023003ad5e5f901410472247a199c1af501fa4384150a2db82c54d71cade7ed8b3d4e52a0a8878e2fd2eabc65efe99647c7a0f769a23a1967ef70c561bcfaa9963876f7b5ac311c8399ffffffff0300e1f505000000001976a914041b819daf6aaf12d85324320121b045faedf22c88ac80d1f008000000001976a914041b819daf6aaf12d85324320121b045faedf22c88ac00c2eb0b000000001976a9147dc5cf86aa8ea975f3715f73be9d90e1fac3efea88ac00000000']
        dtls = BargainingProposalDetails(VALID_TIME3, VALID_BUYER_DATA, VALID_SELLER_DATA, 
                                         txs, VALID_MEMO, [], VALID_BUYER_AMOUNT, 0, False)  
        msg = BargainingMessage(TYPE_BARGAIN_PROPOSAL, dtls)
        
        check_format = msg.check_msg_fmt(network)
        self.assertTrue(check_format)
        
        if check_format:
            msg.sign(last_msg, SIGN_ECDSA_SHA256, TEST_PUB1, TEST_PRIV1)
            check_consistency = nego_buyer.check_consistency(msg)
            self.assertTrue(check_consistency)  
            if check_consistency:
                msg.pbuff = msg.serialize()
                nego_buyer.append(msg)
                wire = msg.pbuff
            else:
                wire = None
        else:
            wire = None
                
    
        '''
        SELLER RECEIVES THE PROPOSAL
        '''  
        self.assertIsNotNone(wire)        
        network = nego_seller.network
        last_msg = nego_seller.get_last_msg()
        
        msg = BargainingMessage.deserialize(wire)
        
        already_received = nego_seller.already_received(msg)
        self.assertFalse(already_received)
        if not already_received:
            precheck_txs = nego_seller.precheck_txs(msg, last_msg, blockr_sum_unspent_inputs)
            self.assertTrue(precheck_txs)
            if precheck_txs:
                check_format = msg.check_msg_fmt(nego_seller.network)
                self.assertTrue(check_format)
                if check_format:
                    check_consistency = nego_seller.check_consistency(msg)
                    self.assertTrue(check_consistency)
            nego_seller.append(msg)     
                                         
        
        '''
        SELLER SENDS ANOTHER OFFER (PROPOSAL ACK)
        '''    
        network = nego_seller.network
        last_msg = nego_seller.get_last_msg()
        
        dtls = BargainingProposalACKDetails(VALID_TIME4, VALID_BUYER_DATA, VALID_SELLER_DATA, VALID_OUTPUTS2, VALID_MEMO)
        msg = BargainingMessage(TYPE_BARGAIN_PROPOSAL_ACK, dtls)
        
        check_format = msg.check_msg_fmt(network)
        self.assertTrue(check_format)
        
        if check_format:
            msg.sign(last_msg, SIGN_ECDSA_SHA256, TEST_PUB2, TEST_PRIV2)
            check_consistency = nego_seller.check_consistency(msg)
            self.assertTrue(check_consistency)  
            if check_consistency:    
                msg.pbuff = msg.serialize()
                nego_seller.append(msg)
                wire = msg.pbuff
            else:
                wire = None
        else:
            wire = None
            
            
        '''
        BUYER RECEIVES THE PROPOSAL ACK
        '''  
        self.assertIsNotNone(wire)
        network = nego_buyer.network
        
        msg = BargainingMessage.deserialize(wire)
        
        already_received = nego_buyer.already_received(msg)
        self.assertFalse(already_received)
        if not already_received:
            check_format = msg.check_msg_fmt(network)
            self.assertTrue(check_format)
            if check_format:
                check_consistency = nego_buyer.check_consistency(msg)
                self.assertTrue(check_consistency)  
            nego_buyer.append(msg) 
                    
                
        '''
        BUYER ACCEPTS SELLER PROPOSAL (SENDS A REDEEMABLE PROPOSAL)
        '''    
        network = nego_buyer.network
        last_msg = nego_buyer.get_last_msg()
        amount = last_msg.details.amount
        fees = 1000
        
        txs = build_valid_single_tx(amount, fees, last_msg.details.outputs)
        dtls = BargainingProposalDetails(VALID_TIME5, VALID_BUYER_DATA, VALID_SELLER_DATA, 
                                         txs, VALID_MEMO, VALID_REFUND_TO, amount, fees, True)  
        msg = BargainingMessage(TYPE_BARGAIN_PROPOSAL, dtls)
        
        check_format = msg.check_msg_fmt(network)
        self.assertTrue(check_format)
        
        if check_format:
            msg.sign(last_msg, SIGN_ECDSA_SHA256, TEST_PUB1, TEST_PRIV1)
            check_consistency = nego_buyer.check_consistency(msg)
            self.assertTrue(check_consistency)  
            if check_consistency:
                msg.pbuff = msg.serialize()
                nego_buyer.append(msg)
                wire = msg.pbuff
            else:
                wire = None
        else:
            wire = None    
                
        
        '''
        SELLER RECEIVES THE PROPOSAL
        '''  
        self.assertIsNotNone(wire)        
        network = nego_seller.network
        last_msg = nego_seller.get_last_msg()
        
        msg = BargainingMessage.deserialize(wire)
        
        already_received = nego_seller.already_received(msg)
        self.assertFalse(already_received)
        if not already_received:
            precheck_txs = nego_seller.precheck_txs(msg, last_msg, blockr_sum_unspent_inputs)
            self.assertTrue(precheck_txs)
            if precheck_txs:
                check_format = msg.check_msg_fmt(nego_seller.network)
                self.assertTrue(check_format)
                if check_format:
                    check_consistency = nego_seller.check_consistency(msg)
                    self.assertTrue(check_consistency)
            nego_seller.append(msg)     
        
        
        '''
        SELLER SENDS A COMPLETION 
        '''    
        network = nego_seller.network
        last_msg = nego_seller.get_last_msg()
        txs = last_msg.details.transactions
        
        dtls = BargainingCompletionDetails(VALID_TIME6, VALID_BUYER_DATA, VALID_SELLER_DATA, txs, VALID_MEMO)
        msg = BargainingMessage(TYPE_BARGAIN_COMPLETION, dtls)
        
        check_format = msg.check_msg_fmt(network)
        self.assertTrue(check_format)
        
        if check_format:
            msg.sign(last_msg, SIGN_ECDSA_SHA256, TEST_PUB2, TEST_PRIV2)
            check_consistency = nego_seller.check_consistency(msg)
            self.assertTrue(check_consistency)  
            if check_consistency:    
                msg.pbuff = msg.serialize()
                nego_seller.append(msg)
                wire = msg.pbuff
            else:
                wire = None
        else:
            wire = None
            
            
        '''
        BUYER RECEIVES THE COMPLETION
        '''  
        self.assertIsNotNone(wire)
        network = nego_buyer.network
        
        msg = BargainingMessage.deserialize(wire)
        
        already_received = nego_buyer.already_received(msg)
        self.assertFalse(already_received)
        if not already_received:
            check_format = msg.check_msg_fmt(network)
            self.assertTrue(check_format)
            if check_format:
                check_consistency = nego_buyer.check_consistency(msg)
                self.assertTrue(check_consistency)  
            nego_buyer.append(msg) 
                
                
        

if __name__ == '__main__':
    unittest.main()