#!/usr/bin/env python
'''
Version: 0.0.1
Python library for the bargaining protocol
'''
from pybargain_protocol.constants import *
from pybargain_protocol.helpers.build_check_tx import check_tx_signatures, check_tx, check_outputs_exist


'''
FUNCTIONS USED TO VALIDATE FORMAT OF BARGAINING_MESSAGES 
'''
def check_msg_type(msg):
    '''
    Checks if message type is valid
    Returns True if type is valid, False otherwise
    
    Parameters:
        msg = a BargainingMessage
    '''
    return msg.msg_type in MESSAGE_TYPES


def check_sig_type(msg):
    '''
    Checks if signature type is valid
    Returns True if type is valid, False otherwise
    
    Parameters:
        msg = a BargainingMessage
    '''
    return msg.sign_type in SIGN_TYPES
    

'''
FUNCTIONS USED TO VALIDATE FORMAT OF BARGAINING_[...]_DETAILS 
'''

def check_time(dtls):
    '''
    Checks if time is valid
    Returns True if valid, False otherwise
    
    Parameters:
        dtls = a Bargaining[...]Details message embedding the time attribute
    '''
    is_unset = dtls.time <= 0
    is_lng   = type(dtls.time) == long
    return is_lng and (not is_unset)


def check_expires(dtls):
    '''
    Checks if expires is valid
    Returns True if valid, False otherwise
    
    Parameters:
        dtls = a Bargaining[...]Details message embedding the expires attribute
    '''
    is_unset     = dtls.expires <= 0
    is_lng       = type(dtls.expires) == long
    is_in_future = dtls.expires > dtls.time
    return is_unset or (is_lng and is_in_future)

    
def check_network(dtls):
    '''
    Checks if network is valid
    Returns True if valid, False otherwise
    
    Parameters:
        dtls    = a Bargaining[...]Details message embedding the network attribute
    '''
    return dtls.network in NETWORKS


def check_outputs(dtls):
    '''
    Checks outputs
    Returns True if valid, False otherwise
    
    Parameters:
        dtls = a Bargaining[...]Details message embedding the outputs attribute
    '''
    is_valid_outp = False
    is_empty = (dtls.outputs is None) or (len(dtls.outputs) == 0)
    if not is_empty:
        is_valid_dict = lambda x: (type(x) == dict) and (x.has_key('amount')) and (x.has_key('script')) 
        # TODO Check that script is a valid script ?
        is_valid_outp = all([is_valid_dict(outp) for outp in dtls.outputs])
    return is_valid_outp


def check_memo(dtls):
    '''
    Checks if memo is valid
    Returns True if valid, False otherwise
    
    Parameters:
        dtls = a Bargaining[...]Details message embedding the memo attribute
    '''
    is_utf8 = True
    try: dtls.memo.decode('utf-8') 
    except UnicodeDecodeError: is_utf8 = False
    return is_utf8


def check_refund_to(dtls, mandatory = False):
    '''
    Checks if refund_to list is valid
    Returns True if valid, False otherwise
    
    Parameters:
        dtls      = a Bargaining[...]Details message embedding the time attribute
        mandatory = flag indicating if at least one input is mandatory
    '''
    is_valid_rt = True
    is_empty = (dtls.refund_to is None) or (len(dtls.refund_to) == 0)
    if not is_empty:
        is_valid_dict = lambda x: (type(x) == dict) and (x.has_key('script')) 
        is_valid_rt = all([is_valid_dict(r) for r in dtls.refund_to])
    elif mandatory:
        is_valid_rt = False
    return is_valid_rt


def check_transactions(dtls, network = MAINNET):
    '''
    Checks if transactions list is valid
    Returns True if valid, False otherwise
    
    Parameters:
        dtls    = a Bargaining[...]Details message embedding the transactions attribute
        network = network used for the negotiation    
    '''
    is_empty = (dtls.transactions is None) or (len(dtls.transactions) == 0)
    if is_empty: 
        return False
    else:
        for tx in dtls.transactions:
            # Checks transaction and signatures
            if not (check_tx(tx) and check_tx_signatures(tx, network)): return False
    return True          


'''
FUNCTIONS USED TO VALIDATE THE CONSISTENCY OF A BARGAINING MESSAGE WITH THE CURRENT STATE OF A NEGOTIATION 
'''
def check_msgtype_role_consistency(msg, role):
    '''
    Checks if message type is consistent with the next expected active role
    
    Parameters:
        msg  = BargainingMessage to be checked
        role = next expected active role 
    '''
    BUYER_MSG_TYPES  = {TYPE_BARGAIN_REQUEST, TYPE_BARGAIN_PROPOSAL, TYPE_BARGAIN_CANCELLATION}
    SELLER_MSG_TYPES = {TYPE_BARGAIN_REQUEST_ACK, TYPE_BARGAIN_PROPOSAL_ACK, TYPE_BARGAIN_COMPLETION, TYPE_BARGAIN_CANCELLATION}

    if role == ROLE_BUYER:
        return True if msg.msg_type in BUYER_MSG_TYPES else False
    elif role == ROLE_SELLER:
        return True if msg.msg_type in SELLER_MSG_TYPES else False
    
    
def check_msgtype_status_consistency(msg, status):
    '''
    Checks if message type is consistent with the current status of the negotiation
    
    Parameters:
        msg    = BargainingMessage to be checked
        status = current status of the negotiation 
    '''
    INITIALIZATION_MSG_TYPES = {TYPE_BARGAIN_REQUEST, TYPE_BARGAIN_REQUEST_ACK, TYPE_BARGAIN_CANCELLATION}
    NEGOTIATION_MSG_TYPES    = {TYPE_BARGAIN_PROPOSAL, TYPE_BARGAIN_PROPOSAL_ACK, TYPE_BARGAIN_CANCELLATION}
    COMPLETION_MSG_TYPES     = {TYPE_BARGAIN_COMPLETION, TYPE_BARGAIN_CANCELLATION}
    
    if status == NEGO_STATUS_INITIALIZATION:
        return True if msg.msg_type in INITIALIZATION_MSG_TYPES else False
    elif status == NEGO_STATUS_NEGOTIATION:
        return True if msg.msg_type in NEGOTIATION_MSG_TYPES else False
    elif status == NEGO_STATUS_COMPLETION:
        return True if msg.msg_type in COMPLETION_MSG_TYPES else False
    else:
        return False
    

def check_network_consistency(msg, network):
    '''
    Checks if network defined in message is consistent with network used for the negotiation
    
    Parameters:
        msg     = BargainingMessage to be checked
        network = network used for the negotiation 
    '''
    return msg.details.network == network


def check_date_consistency(msg, prev_msg):
    '''
    Checks if the date of message is consistent with the date of the last message sent by the same role
        
    Parameters:
        msg      = BargainingMessage to be checked
        prev_msg = previous message sent by the same role
    '''
    return True if (prev_msg is None) or (msg.details.time > prev_msg.details.time) else False


def check_expires_consistency(msg, expires):
    '''
    Checks if the date of message is consistent with the expiry date defined by the other role
        
    Parameters:
        msg     = BargainingMessage to be checked
        expires = expiry date defined by the other role
    '''
    return True if (expires == 0) or (msg.details.time <= expires) else False


def check_prev_msg_status_consistency(msg, prev_msg):
    '''
    Checks if the previous message has been validated.
    Negotiation shouldn't continue if previous message has not been validated or doesn't follow protocol rules.
        
    Parameters:
        msg      = BargainingMessage to be checked
        prev_msg = previous message
    '''
    return (prev_msg is None) or (prev_msg.status == MSG_STATUS_OK) or (msg.msg_type == TYPE_BARGAIN_CANCELLATION) 


def check_amount_consistency(msg, prev_msg):
    '''
    Checks if the proposed amount is consistent with the previous proposed amount 
        
    Parameters:
        msg      = BargainingMessage to be checked
        prev_msg = previous message sent by the same role
    '''
    if prev_msg == None:
        return False
    elif (msg.msg_type == TYPE_BARGAIN_PROPOSAL) and (prev_msg.msg_type == TYPE_BARGAIN_PROPOSAL):
        #return True if (msg.details.amount + msg.details.fees >= prev_msg.details.amount + prev_msg.details.fees) else False
        return True if (msg.details.amount >= prev_msg.details.amount) else False
    elif msg.msg_type == TYPE_BARGAIN_PROPOSAL_ACK:
        return True if (msg.details.amount <= prev_msg.details.amount) else False
    else:
        return True
    
    
def check_outputs_consistency(msg, prev_msg):
    '''
    Checks if all outputs proposed by Seller in her last message are found in txs proposed by the Buyer
    
    Parameters:
        msg      = BargainingMessage to be checked
        prev_msg = previous message
    '''
    PREV_MSG_TYPE = {TYPE_BARGAIN_REQUEST_ACK, TYPE_BARGAIN_PROPOSAL_ACK}
    if prev_msg is None:
        return False
    elif (msg.msg_type == TYPE_BARGAIN_PROPOSAL) and (prev_msg.msg_type in PREV_MSG_TYPE):
        return check_outputs_exist(msg.details.transactions, prev_msg.details.outputs)
    else:
        return False
 
 
def check_redeemable_consistency(msg, prev_msg):
    '''
    Checks if redeemable status is consistent with the amount and fees proposed
    Tries to detect a fraud with amount + fee proposed by buyer greater than amount proposed by seller
    but with some non redeemable txs (=> redeemable == False)
    
    Parameters:
        msg      = BargainingMessage to be checked
        prev_msg = previous message
    '''
    PREV_MSG_TYPE = {TYPE_BARGAIN_REQUEST_ACK, TYPE_BARGAIN_PROPOSAL_ACK}
    if prev_msg is None:
        return False
    elif (msg.msg_type == TYPE_BARGAIN_PROPOSAL) and (prev_msg.msg_type in PREV_MSG_TYPE):
        seems_redeemable = msg.details.amount + msg.details.fees >= prev_msg.details.amount
        is_redeemable = not msg.details.is_redeemable
        return not (seems_redeemable and is_redeemable)
    else:
        return False
    
    
def check_transactions_consistency(msg, prev_msg):
    '''
    Checks if transactions appearing in BargainingCompletion message are consistent 
    with transactions sent in last BargainingProposal message
        
    Parameters:
        msg      = BargainingMessage to be checked
        prev_msg = previous message
    '''
    if prev_msg is None:
        return False
    elif (msg.msg_type == TYPE_BARGAIN_COMPLETION) and (prev_msg.msg_type == TYPE_BARGAIN_PROPOSAL):
        prev_txs = prev_msg.details.transactions
        for tx in msg.details.transactions:
            if not tx in prev_txs: return False
        return True
    else:
        return False
    

def check_signature(msg, prev_msg):
    '''
    Checks if signature is valid
    
    Parameters:
        msg      = BargainingMessage to be checked
        prev_msg = previous message 
    '''
    return msg.check_signature(prev_msg)
    

def check_signature_consistency(msg, prev_msg):
    '''
    Checks if signature is consistent with last signature sent by the user (sign type, public key/cert)
    
    Parameters:
        msg      = BargainingMessage to be checked
        prev_msg = previous message sent by the same role
    '''
    return (prev_msg is None) or\
           (msg.sign_type == prev_msg.sign_type and msg.sign_data == prev_msg.sign_data)

    
    