#!/usr/bin/env python
'''
Version: 0.0.1
Python library for the bargaining protocol
'''
from pybargain_protocol.constants import *
from pybargain_protocol.protocol_rules import *
from pybargain_protocol.exceptions import InvalidTxHashError, ThirdPartyServiceUnreachableError, UtxoError
from pybargain_protocol.helpers.bc_api import blockr_sum_inputs


class Negotiation(object):
    '''
    A negotiation (chain of messages)
    '''
    
     
    '''
    ATTRIBUTES
    
    # Negotiation id
    nid = ''
    
    # Network used for the negotiation
    network = MAINNET
    
    # User role
    role = ROLE_BUYER
    
    # Current state of the negotiation
    status = NEGO_STATUS_INITIALIZATION
    
    # Chain of messages
    _msgchain = []
    '''    
    
    
    '''
    CONSTRUCTOR
    '''
    def __init__(self, nid = '', role = ROLE_BUYER, network = MAINNET):
        '''
        Constructor
        
        Parameters:
            nid     = negotiation id
            role    = user role
            network = network used for the negotiation            
        '''
        self.nid        = nid
        self.role       = role
        self.network    = network
        self.status     = NEGO_STATUS_INITIALIZATION
        self._msgchain  = []
        
        
    '''
    CHAIN OF MESSAGES - GETTERS
    '''
    def length(self):
        '''
        Returns the length of the chain
        '''    
        return len(self._msgchain)
    
    
    def get_msg_at_idx(self, idx):
        '''
        Returns the message stored at given index
        
        Parameters:
            idx = index of the message in the chain
        '''
        invalid_idx = (idx < 0) or (idx > self.length() - 1)
        return None if invalid_idx else self._msgchain[idx]
         
    
    def get_last_msg(self):
        '''
        Returns the last message from the chain
        '''
        return None if self.length() == 0 else self._msgchain[-1]
    
    
    def get_rqst_msg(self):
        '''
        Returns the BargainingRequest message initializing the negotiation        
        '''    
        return None if self.length() == 0 else self._msgchain[0]
    
    
    def get_rqst_ack_msg(self):
        '''
        Returns the BargainingRequestACK message initializing the negotiation        
        '''    
        return None if self.length() < 2 else self._msgchain[1]
    
    
    def get_next_active_role(self):
        '''
        Returns the role (ROLE_BUYER, ROLE_SELLER) which should append the next message
        '''
        return ROLE_BUYER if self.length()%2 == 0 else ROLE_SELLER
    
    
    def get_expiry_for_role(self, role):
        '''
        Returns the timestamp after which messages sent by a given role are rejected
        Parameters:
            role = role to be checked
        '''
        if role == ROLE_BUYER:
            req_ack = self.get_rqst_ack_msg()
            if not (req_ack is None): return req_ack.details.expires
        elif role == ROLE_SELLER:
            req = self.get_rqst_msg()
            if not (req is None): return req.details.expires
        return 0
    
    
    def get_bargain_uri_for_role(self, role):
        '''
        Returns the url which should be used by a given role to send messages
        Parameters:
            role = role to be checked
        '''
        if role == ROLE_BUYER:
            req_ack = self.get_rqst_ack_msg()
            if not (req_ack is None): return req_ack.details.bargaining_url
        elif role == ROLE_SELLER:
            req = self.get_rqst_msg()
            if not (req is None): return req.details.bargaining_url
        return ''
    
    
    def get_negotiated_amount(self):
        '''
        Returns the negotiated amount if negotiation has completed, returns None otherwise
        '''
        if self.status == NEGO_STATUS_COMPLETED:
            last_prpsl = self._msgchain[-2]
            if last_prpsl.msg_type == TYPE_BARGAIN_PROPOSAL: 
                return last_prpsl.details.amount
        return None
    
    
    def get_next_msg_types(self):
        '''
        Returns a list of next message types expected by role according to current status
        '''
        INITIALIZATION_BUYER_MSG_TYPES  = [TYPE_BARGAIN_REQUEST, TYPE_BARGAIN_CANCELLATION]
        INITIALIZATION_SELLER_MSG_TYPES = [TYPE_BARGAIN_REQUEST_ACK, TYPE_BARGAIN_CANCELLATION]
        NEGOTIATION_BUYER_MSG_TYPES     = [TYPE_BARGAIN_PROPOSAL, TYPE_BARGAIN_CANCELLATION]
        NEGOTIATION_SELLER_MSG_TYPES    = [TYPE_BARGAIN_PROPOSAL_ACK, TYPE_BARGAIN_CANCELLATION]
        COMPLETION__SELLER_MSG_TYPES    = [TYPE_BARGAIN_COMPLETION, TYPE_BARGAIN_CANCELLATION]
        
        if self.status == NEGO_STATUS_INITIALIZATION:
            return INITIALIZATION_BUYER_MSG_TYPES if self.role == ROLE_SELLER else INITIALIZATION_SELLER_MSG_TYPES
        elif self.status == NEGO_STATUS_NEGOTIATION:
            return NEGOTIATION_BUYER_MSG_TYPES if self.role == ROLE_SELLER else NEGOTIATION_SELLER_MSG_TYPES
        elif self.status == NEGO_STATUS_COMPLETION:
            return [] if self.role == ROLE_SELLER else COMPLETION__SELLER_MSG_TYPES
        else:
            return []
    
    
    '''
    CHAIN OF MESSAGES - SETTERS
    '''
    def append(self, msg):
        '''
        Appends a given BargainingMessage to the chain
        
        Parameters:
            msg = BargainingMessage to be appended
        '''
        self._msgchain.append(msg)
        self._refresh_status()
        
    
    '''
    CHAIN OF MESSAGES - CHECKS
    '''
    def already_received(self, msg):
        '''
        Checks if given message has already been inserted in the chain
        
        Parameters:
            msg = BargainingMessage to be checked
        '''
        for curr_msg in self._msgchain:
            if msg.pbuff == curr_msg.pbuff: return True
        return False
        
   
    def precheck_txs(self, msg, prev_msg, fctn = blockr_sum_inputs):
        '''
        Pre-checks transactions sent within a BargainingProposal message
          * Checks if all inputs are found into the blockchain
          * Computes the amount and fees proposed by the buyer
          * Checks if all transactions are redeemable
          * Stores the results in object attributes
        
        Parameters:
            msg      = BargainingMessage to be checked
            prev_msg = last message sent by the seller (BargainingRequestACK or BargainingProposalACK)
            network  = network used for the negotiation
            fctn     = function used to compute the sum of the inputs for a given transaction
                       by querying the blockchain
                       see bc.api.blockr_sum_inputs() for signature and returned value
        '''
        prev_types = {TYPE_BARGAIN_REQUEST_ACK, TYPE_BARGAIN_PROPOSAL_ACK}
        if (msg.msg_type == TYPE_BARGAIN_PROPOSAL) and (prev_msg.msg_type in prev_types):
            try:
                msg.details.check_amount_fees_redeemable(prev_msg.details.amount, self.network, fctn)
                return True
            except UtxoError:
                msg.log_error('One or several inputs reference spent txos or are duplicate')
                return False
            except InvalidTxHashError:
                msg.log_error('One or several inputs reference invalid utxos')
                return False
            except ThirdPartyServiceUnreachableError:
                msg.log_error('Third-party service unreachable. Unable to check transactions.')
                msg.status = MSG_STATUS_UND
                return False
        else:
            return False
    
   
    def check_consistency(self, msg):
        '''
        Checks if a BargainingMessage is consistent with the current state of the negotiation, as a last message in the chain
        Returns True if message is consistent with the chain, False otherwise
        
        Parameters:
            msg = BargainingMessage to be checked
        '''
        is_consistent = True
        
        # Gets next expected role, last message and last message sent by the same role
        next_role = self.get_next_active_role()
        prev_msg = self.get_last_msg()
        prev_msg_for_role = self.get_msg_at_idx(self.length() - 2)
        
        # Checks signature
        if not check_signature(msg, prev_msg):
            is_consistent = False
            msg.log_error('Invalid signature')
        
        if not check_signature_consistency(msg, prev_msg_for_role):
            is_consistent = False
            msg.log_error('Signature is not consistent with previous signature')
        
        # Checks message type / next expected role
        if not check_msgtype_role_consistency(msg, next_role):
            is_consistent = False
            msg.log_error('Message type is unexpected at this step of the negotiation')
        
        # Checks message type / negotiation status
        if not check_msgtype_status_consistency(msg, self.status):
            is_consistent = False
            msg.log_error('Message type is not consistent with current status of the negotiation')
            
        # Checks time / expiry date
        expires = self.get_expiry_for_role(next_role)
        if not check_expires_consistency(msg, expires):
            is_consistent = False
            msg.log_error('Negotiation has expired')
        
        # Checks time / previous time
        if not check_date_consistency(msg, prev_msg_for_role):
            is_consistent = False
            msg.log_error('Invalid time (cannot be before time appearing in last sent message)')
            
        # Checks network
        if msg.msg_type in {TYPE_BARGAIN_REQUEST, TYPE_BARGAIN_REQUEST_ACK}:
            if not check_network_consistency(msg, self.network):
                is_consistent = False
                msg.log_error('Invalid network')
        
        # Checks previous message status
        # If previous message is invalid, current message should be a BargainingCancellation
        # If previous message has not been checked, it should be before sending a new message
        if not check_prev_msg_status_consistency(msg, prev_msg):
            is_consistent = False
            msg.log_error('Previous message is invalid or has not been checked.')
                
        # Checks amount / previous amount
        if msg.msg_type in {TYPE_BARGAIN_PROPOSAL, TYPE_BARGAIN_PROPOSAL_ACK}:
            if not check_amount_consistency(msg, prev_msg_for_role):
                is_consistent = False
                msg.log_error('Invalid amount (must be a better offer than last proposed amount)')
        
        # Checks tx outputs
        if msg.msg_type == TYPE_BARGAIN_PROPOSAL:
            if not check_outputs_consistency(msg, prev_msg):
                is_consistent = False
                msg.log_error('Transactions must embed all outputs sent by the seller')
                
        # Checks redeemable status is consistent with amount proposed
        if (msg.msg_type == TYPE_BARGAIN_PROPOSAL) and (self.role == ROLE_SELLER):
            if not check_redeemable_consistency(msg, prev_msg):
                is_consistent = False
                msg.log_error('Attempt to complete the negotiation with some non redeemable transactions')
        
        # Checks transactions consistency
        if msg.msg_type == TYPE_BARGAIN_COMPLETION:
            if not check_transactions_consistency(msg, prev_msg):
                is_consistent = False
                msg.log_error('Transactions in completion message don\'t match transactions from last proposal')
        
        # Returns result
        return is_consistent
                
    
    '''
    STATUS
    '''
    def _refresh_status(self):
        '''
        Refreshes the status of the negotiation
        '''
        last_msg = self.get_last_msg()
        
        if last_msg is None: 
            self.status = NEGO_STATUS_INITIALIZATION

        elif self.status == NEGO_STATUS_INITIALIZATION:
            if last_msg.msg_type == TYPE_BARGAIN_REQUEST_ACK:
                self.status = NEGO_STATUS_NEGOTIATION
            elif last_msg.msg_type == TYPE_BARGAIN_CANCELLATION:
                self.status = NEGO_STATUS_CANCELLED
        
        elif self.status == NEGO_STATUS_NEGOTIATION:
            if last_msg.msg_type == TYPE_BARGAIN_PROPOSAL:
                if last_msg.details.is_redeemable:
                    self.status = NEGO_STATUS_COMPLETION
            elif last_msg.msg_type == TYPE_BARGAIN_CANCELLATION:
                self.status = NEGO_STATUS_CANCELLED
            
        elif self.status == NEGO_STATUS_COMPLETION:
            if last_msg.msg_type == TYPE_BARGAIN_COMPLETION:
                self.status = NEGO_STATUS_COMPLETED
            elif last_msg.msg_type == TYPE_BARGAIN_CANCELLATION:
                self.status = NEGO_STATUS_CANCELLED
        
        
