#!/usr/bin/env python
'''
Version: 0.0.1
Python library for the bargaining protocol
'''
import copy
from bitcoin.main import sha256, ecdsa_sign, ecdsa_verify
from pybargain_protocol.constants import *
from pybargain_protocol import bargaining_pb2
from pybargain_protocol.exceptions import InvalidSignatureTypeError, SignatureError, DeserializationError, SerializationError, InvalidMessageTypeError
from pybargain_protocol.bargaining_request import BargainingRequestDetails
from pybargain_protocol.bargaining_request_ack import BargainingRequestACKDetails
from pybargain_protocol.bargaining_proposal import BargainingProposalDetails
from pybargain_protocol.bargaining_proposal_ack import BargainingProposalACKDetails
from pybargain_protocol.bargaining_completion import BargainingCompletionDetails
from pybargain_protocol.bargaining_cancellation import BargainingCancellationDetails
from pybargain_protocol.protocol_rules import check_msg_type, check_sig_type



class BargainingMessage(object):
    '''
    Message wrapper class
    '''    
    
    
    '''
    ATTRIBUTES
    
    msg_type        = message type
    details_version = protocol version
    sign_type       = type of signature used
    sign_data       = public key/cert used to sign the message
    details         = message details
    signature       = signature of the message
    pbuff           = protocol buffers serialized string
    status          = message status
    errors          = list of errors         
    '''    

    
    '''
    CONSTRUCTOR
    '''
    def __init__(self, msg_type = '', details = ''):
        '''
        Constructor
        
        Parameters:
            msg_type = message type
            details  = message details            
        '''
        self.msg_type        = msg_type
        self.details         = details
        self.details_version = PROTOCOL_VERSION
        self.pbuff           = ''
        self.sign_type       = SIGN_NONE
        self.sign_data       = ''       
        self.signature       = ''
        self._reset_status()
        
    
    '''
    SERIALIZATION
    '''
    def serialize(self):
        '''
        Serializes the BargainingMessage in protobuff format
        Returns the serialized message
        '''
        try:
            pbbm = bargaining_pb2.BargainingMessage()
            pbbm.msg_type           = self.msg_type
            pbbm.serialized_details = self.details.serialize()
            pbbm.details_version    = self.details_version
            pbbm.sign_type          = self.sign_type
            if self.sign_type != SIGN_NONE:
                pbbm.sign_data = self.sign_data
                pbbm.signature = self.signature
            return pbbm.SerializeToString()
        except:
            raise SerializationError('A problem occurred while serializing the BargainingMessage with Protocol Buffers')
                
        
    def deserialize(pbuff): 
        '''
        Deserializes a protobuff message as a BargainingMessage
        
        Parameters:
            pbuff = protobuff message             
        '''
        if not pbuff: raise DeserializationError('Protocol Buffers message is empty')
        
        try:
            pbbm = bargaining_pb2.BargainingMessage()
            pbbm.ParseFromString(pbuff)   
        except:
            raise DeserializationError('A problem occurred while deserializing the Protocol Buffers message associated to a BargainingMessage')         
        
        bm = BargainingMessage()
        bm.msg_type        = pbbm.msg_type
        bm.details_version = pbbm.details_version
        bm.pbuff           = pbuff
        bm.sign_type       = pbbm.sign_type
        bm.details         = BargainingMessage._deserialize_details(pbbm.msg_type, pbbm.serialized_details)
        if pbbm.sign_data: bm.sign_data = pbbm.sign_data
        if pbbm.signature: bm.signature = pbbm.signature
        return bm
                
    deserialize = staticmethod(deserialize)
     
     
    def _deserialize_details(msg_type, pbuff):
        '''
        Deserializes a protobuff message as a Bargaining[...]Details
        
        Parameters:
            msg_type = message type
            pbuff    = protobuff message for details
        ''' 
        if msg_type == TYPE_BARGAIN_REQUEST:
            return BargainingRequestDetails.deserialize(pbuff)
        elif msg_type == TYPE_BARGAIN_REQUEST_ACK:
            return BargainingRequestACKDetails.deserialize(pbuff)
        elif msg_type == TYPE_BARGAIN_PROPOSAL:
            return BargainingProposalDetails.deserialize(pbuff)
        elif msg_type == TYPE_BARGAIN_PROPOSAL_ACK:
            return BargainingProposalACKDetails.deserialize(pbuff)
        elif msg_type == TYPE_BARGAIN_COMPLETION:
            return BargainingCompletionDetails.deserialize(pbuff)
        elif msg_type == TYPE_BARGAIN_CANCELLATION:
            return BargainingCancellationDetails.deserialize(pbuff)
        else:
            raise InvalidMessageTypeError(msg_type)
                
    _deserialize_details = staticmethod(_deserialize_details)
    
           
    '''
    SIGNATURES
    '''
    def sign(self, prev_msg = None, sign_type = SIGN_NONE, sign_data = '', sign_priv = None):
        '''
        Signs the message
        Returns the signature
        
        Parameters:
            prev_msg  = previous message received
            sign_type = type of signature used
            sign_data = ecdsa public key, X509 certificates, ...
            sign_priv = private key           
        '''
        if sign_type == SIGN_NONE: return        
        # Gets the serialized content to be signed
        prev_pbuff = '' if prev_msg is None else prev_msg.pbuff
        curr_pbuff = self._get_pbuff_for_sign(sign_type, sign_data)
        pbuff      = (prev_pbuff + '|' if prev_pbuff else '') + curr_pbuff
        # Signs the content
        if sign_type == SIGN_ECDSA_SHA256:
            self.signature = self._sign_ecdsa_sha256(pbuff, sign_priv)
            self.sign_type = SIGN_ECDSA_SHA256
            self.sign_data = sign_data 
            #print(self.signature) # TODO Delete this line
        # NOTE : Adds new signature schemes here
        else:
            raise InvalidSignatureTypeError(sign_type)
        
        
    def check_signature(self, prev_msg = None):
        '''
        Checks the signature of the message
        Returns True if signature is valid, False otherwise
        
        Parameters:
            prev_msg = previous message in the negotiation chain            
        '''  
        if self.sign_type == SIGN_NONE: return True        
        # Gets the serialized content which should have been signed
        prev_pbuff = '' if prev_msg is None else prev_msg.pbuff
        curr_pbuff = self._get_pbuff_for_check_sign()
        pbuff      = (prev_pbuff + '|' if prev_pbuff else '') + curr_pbuff
        # Checks signature
        if self.sign_type == SIGN_ECDSA_SHA256:
            return self._check_sign_ecdsa_sha256(pbuff, self.signature, self.sign_data)
        # NOTE : Adds new signature schemes here
        else:
            raise InvalidSignatureTypeError(self.sign_type)
        
    
    def _get_pbuff_for_sign(self, sign_type = SIGN_NONE, sign_data = ''):
        '''
        Prepares the serialized content to be signed
        
        Parameters:
            sign_type = type of signature used
            sign_data = ecdsa public key, X509 certificates, ...            
        '''
        bm = copy.deepcopy(self)
        bm.signature = ''
        bm.sign_type = sign_type
        bm.sign_data = sign_data    
        return bm.serialize()
        
        
    def _get_pbuff_for_check_sign(self):
        '''
        Gets the serialized content which should have been signed
        '''
        pbuff = self.pbuff if self.pbuff else self.serialize()
        pbbm = bargaining_pb2.BargainingMessage()
        pbbm.ParseFromString(pbuff)
        pbbm.signature = '' 
        return pbbm.SerializeToString()
                    
    
    '''
    ECDSA + SHA256
    '''
    def _sign_ecdsa_sha256(self, msg, privkey):
        '''
        Signs a msg with SHA256 + ECDSA
        
        Parameters:
            msg     = message to be signed
            privkey = private key            
        '''
        if privkey is None: raise SignatureError()
        try: return ecdsa_sign(sha256(msg), privkey)
        except: raise SignatureError()
        
    
    def _check_sign_ecdsa_sha256(self, msg, sig, pubkey):
        '''
        Checks a SHA256 + ECDSA signature
        Returns True is signature is valid, False otherwise
        
        Parameters:
            msg    = signed message
            sig    = signature
            pubkey = ecdsa public key           
        '''
        if (not sig) or (not pubkey): return False
        try: return ecdsa_verify(sha256(msg), sig, pubkey)
        except: return False
        
    
    '''
    VALIDATIONS 
    '''
    def check_msg_fmt(self, network = MAINNET):
        '''
        Checks if message format is valid
        Returns True if message is valid, False otherwise
        
        Parameters:
            network = network used for the negotiation
        '''
        self._reset_status()
        self.status = MSG_STATUS_OK
        
        is_valid_dtls     = self.details.check_msg_fmt(network)
        is_valid_msg_type = check_msg_type(self)
        is_valid_sig_type = check_sig_type(self)
        
        if not is_valid_dtls    : self.log_error('Invalid message details')
        if not is_valid_msg_type: self.log_error('Invalid message type')
        if not is_valid_sig_type: self.log_error('Invalid signature type')        
        
        return is_valid_msg_type and is_valid_sig_type and is_valid_dtls
        
    
    '''
    STATUS
    '''   
    def _reset_status(self):
        '''
        Resets the status and the list of errors
        '''
        self.status = MSG_STATUS_UND
        self.errors = []
        
    
    def log_error(self, error):
        '''
        Registers an error and set the status
        
        Parameters:
            error = error to register
        '''
        self.errors.append(error)
        self.status = MSG_STATUS_KO
        
         
        