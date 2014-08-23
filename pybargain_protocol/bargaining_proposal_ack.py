#!/usr/bin/env python
'''
Version: 0.0.1
Python library for the bargaining protocol
'''
from bitcoin.transaction import deserialize
from pybargain_protocol import bargaining_pb2
from pybargain_protocol.constants import MAINNET
from pybargain_protocol.exceptions import SerializationError, DeserializationError
from pybargain_protocol.protocol_rules import check_time, check_outputs, check_memo


class BargainingProposalACKDetails(object):
    '''
    Details of a BargainingProposalACK message
    '''  
    
    '''
    ATTRIBUTES
    
    amount      = amount expected by seller (sum of outputs['amount']) 
    buyer_data  = arbitrary data that may be used by the buyer
    memo        = utf-8 encoded, plain-text (no formatting) note that should be displayed to the receiver (part of the negotiation)
    outputs     = list of outputs ([{'amount': ..., 'script': ...}])
    seller_data = arbitrary data that may be used by the seller
    time        = unix timestamp associated to the message
    '''     
    
    '''
    CONSTRUCTOR
    '''
    def __init__(self, 
                 time = 0,
                 buyer_data = '', 
                 seller_data = '',
                 outputs = [],
                 memo = ''):
        '''
        Constructor
        
        Parameters:
            time           = unix timestamp associated to the message
            buyer_data     = arbitrary data that may be used by the buyer
            seller_data    = arbitrary data that may be used by the seller
            outputs        = list of outputs ([{'amount': ..., 'script': ...}])
            memo           = utf-8 encoded, plain-text (no formatting) note that should be displayed to the receiver (part of the negotiation)
        ''' 
        self.time        = time
        self.buyer_data  = buyer_data
        self.seller_data = seller_data
        self.outputs     = outputs
        self.memo        = memo
        self.amount      = sum([o['amount'] for o in outputs])
        
        
    '''
    SERIALIZATION
    '''
    def serialize(self):
        '''
        Serializes the message (protobuff)
        '''
        try:
            pbbpad = bargaining_pb2.BargainingProposalACKDetails()
            pbbpad.time = self.time
            if self.buyer_data  : pbbpad.buyer_data = self.buyer_data
            if self.seller_data : pbbpad.seller_data = self.seller_data
            if self.memo        : pbbpad.memo = self.memo
            for o in self.outputs:
                outp        = pbbpad.outputs.add()
                outp.amount = o['amount']
                outp.script = o['script']    
            return pbbpad.SerializeToString()
        except:
            raise SerializationError('A problem occurred while serializing the BargainingProposalACKDetails with Protocol Buffers')
        
        
        
    def deserialize(pbuff): 
        '''
        Deserializes a protobuff message as a BargainingProposalACKDetails
        
        Parameters:
            pbuff = protobuff message             
        '''
        if not pbuff: raise DeserializationError('Protocol Buffers message is empty')
        
        try:
            pbbpad = bargaining_pb2.BargainingProposalACKDetails()
            pbbpad.ParseFromString(pbuff)
        except:
            raise DeserializationError('A problem occurred while deserializing the Protocol Buffers message associated to a BargainingProposalACKDetails')         
        
        time    = pbbpad.time
        bdata   = pbbpad.buyer_data
        sdata   = pbbpad.seller_data
        memo    = pbbpad.memo
        outputs = []
        for o in pbbpad.outputs: outputs.append({'amount': o.amount, 'script': o.script})
        return BargainingProposalACKDetails(time, bdata, sdata, outputs, memo)
                
    deserialize = staticmethod(deserialize)
          
    
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
        return check_time(self) and\
               check_outputs(self) and\
               check_memo(self)
    
    
        