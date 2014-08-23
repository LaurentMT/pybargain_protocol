#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Version: 0.0.1
Python library for the bargaining protocol
'''
from bitcoin.transaction import select, deserialize, serialize
from pybargain_protocol.constants import *
from pybargain_protocol.bargaining_cancellation import BargainingCancellationDetails
from pybargain_protocol.bargaining_message import BargainingMessage
from pybargain_protocol.helpers.bc_api import blockr_unspent
from pybargain_protocol.helpers.build_check_tx import build_tx_with_change
from pybargain_protocol.bargaining_completion import BargainingCompletionDetails
from pybargain_protocol.bargaining_proposal_ack import BargainingProposalACKDetails
from pybargain_protocol.bargaining_request_ack import BargainingRequestACKDetails
from pybargain_protocol.bargaining_request import BargainingRequestDetails
from pybargain_protocol.bargaining_proposal import BargainingProposalDetails
from pybargain_protocol.tests.values import *



def build_valid_single_tx(amount, fees, outputs):
    '''
    Return a list with a single valid tx
    '''
    # Gets utxos for TEST_ADDR1
    utxos = blockr_unspent(TESTNET, TEST_ADDR1)
    inputs = select(utxos, amount + fees)
    for i in inputs: i['privkey'] = TEST_PRIV1
    # Builds and returns the tx (embedded in a list)
    return [build_tx_with_change(inputs, outputs, amount, fees, TEST_ADDR1)]
            

def build_valid_multi_tx(amount, fees, outputs):
    '''
    Return a list with 2 valid tx
    '''
    txs = []
    # Gets utxos for TEST_ADDR1
    utxos = blockr_unspent(TESTNET, TEST_ADDR1) 
    for output in outputs:
        inputs = select(utxos, output['amount'] + fees)
        for inp in inputs: inp['privkey'] = TEST_PRIV1
        tx = build_tx_with_change(inputs, output, output['amount'], fees, TEST_ADDR1)
        txs.append(tx)
    return txs


def build_unsigned_single_tx(amount, fees, outputs):
        '''
        Builds an unsigned tx and returns it in a list
        '''
        txs = build_valid_single_tx(amount, fees, outputs)
        txjson = deserialize(txs[0])
        for inp in txjson["ins"]: inp['script'] = ''
        return [serialize(txjson)]
    

def _build_message(dtls, msg_type, sign_type, prev_msg=None, pubkey='', privkey=None):
    msg = BargainingMessage(msg_type, dtls)
    if sign_type == SIGN_ECDSA_SHA256:
        msg.sign(prev_msg, SIGN_ECDSA_SHA256, pubkey, privkey)    
    if msg.check_msg_fmt(TESTNET) and msg.check_signature(prev_msg):    
        msg.pbuff = msg.serialize()
        return msg
    else:
        return None   


def build_request_message(time = 0,
                          buyer_data = '', 
                          seller_data = '',
                          network = TESTNET,
                          expires = 0,
                          bargaining_url = '',
                          sign_type = SIGN_NONE):
    '''
    Builds a BargainingRequest message
    Returns the BargainingMessage
    '''
    dtls = BargainingRequestDetails(time, buyer_data, seller_data, network, expires, bargaining_url)  
    return _build_message(dtls, TYPE_BARGAIN_REQUEST, sign_type, None, TEST_PUB1, TEST_PRIV1)
        
    
def build_request_ack_message(time = 0,
                              buyer_data = '', 
                              seller_data = '',
                              network = TESTNET,
                              expires = 0,
                              bargaining_url = '',
                              outputs = [],
                              memo = '',
                              sign_type = SIGN_NONE,
                              prev_msg = None):
    '''
    Builds a BargainingRequestACK message
    Returns the BargainingMessage
    '''
    dtls = BargainingRequestACKDetails(time, buyer_data, seller_data, network, expires, bargaining_url, outputs, memo) 
    return _build_message(dtls, TYPE_BARGAIN_REQUEST_ACK, sign_type, prev_msg, TEST_PUB2, TEST_PRIV2)              
 
 
def build_proposal_message(time = 0,
                           buyer_data = '', 
                           seller_data = '',
                           transactions = [],
                           amount = 0,
                           fees = 0,
                           memo = '',
                           refund_to = [],
                           sign_type = SIGN_NONE,
                           prev_msg = None,
                           is_redeemable = False):
    '''
    Builds a BargainingProposal message
    Returns the BargainingMessage
    '''
    dtls = BargainingProposalDetails(time, buyer_data, seller_data, transactions, memo, refund_to, amount, fees, is_redeemable)        
    return _build_message(dtls, TYPE_BARGAIN_PROPOSAL, sign_type, prev_msg, TEST_PUB1, TEST_PRIV1)


def build_proposal_ack_message(time = 0,
                               buyer_data = '', 
                               seller_data = '',
                               outputs = [],
                               memo = '',
                               sign_type = SIGN_NONE,
                               prev_msg = None):
    '''
    Builds a BargainingProposalACK message
    Returns the BargainingMessage
    '''
    dtls = BargainingProposalACKDetails(time, buyer_data, seller_data, outputs, memo) 
    return _build_message(dtls, TYPE_BARGAIN_PROPOSAL_ACK, sign_type, prev_msg, TEST_PUB2, TEST_PRIV2)       


def build_completion_message(time = 0,
                             buyer_data = '', 
                             seller_data = '',
                             transactions = [],
                             memo = '',
                             sign_type = SIGN_NONE,
                             prev_msg = None):
    '''
    Builds a BargainingCompletion message
    Returns the BargainingMessage
    '''
    dtls = BargainingCompletionDetails(time, buyer_data, seller_data, transactions, memo)        
    return _build_message(dtls, TYPE_BARGAIN_COMPLETION, sign_type, prev_msg, TEST_PUB2, TEST_PRIV2)
  

def build_cancellation_message(time = 0,
                               buyer_data = '', 
                               seller_data = '',
                               memo = '',
                               sign_type = SIGN_NONE,
                               prev_msg = None):
    '''
    Builds a BargainingCancellation message
    Returns the BargainingMessage
    '''
    dtls = BargainingCancellationDetails(time, buyer_data, seller_data, memo)
    return _build_message(dtls, TYPE_BARGAIN_CANCELLATION, sign_type, prev_msg, TEST_PUB2, TEST_PRIV2)

    
