#!/usr/bin/env python
'''
Version: 0.0.1
Python library for the bargaining protocol
'''
from pybargain_protocol import bargaining_pb2
from pybargain_protocol.constants import MAINNET
from pybargain_protocol.exceptions import SerializationError, DeserializationError
from pybargain_protocol.protocol_rules import check_time, check_memo


class BargainingCancellationDetails(object):
    '''
    Details of a BargainingCancellation message
    '''  
    
    '''
    ATTRIBUTES
    
    buyer_data  = arbitrary data that may be used by the buyer
    memo        = utf-8 encoded, plain-text (no formatting) note that should be displayed to the receiver (part of the negotiation)
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
                 memo = ''):
        '''
        Constructor
        
        Parameters:
            time        = unix timestamp associated to the message
            buyer_data  = arbitrary data that may be used by the buyer
            seller_data = arbitrary data that may be used by the seller
            memo        = utf-8 encoded, plain-text (no formatting) note that should be displayed to the receiver (part of the negotiation)
        ''' 
        self.time        = time
        self.buyer_data  = buyer_data
        self.seller_data = seller_data
        self.memo        = memo
        
        
    '''
    SERIALIZATION
    '''
    def serialize(self):
        '''
        Serializes the message (protobuff)
        '''
        try:
            pbcd = bargaining_pb2.BargainingCancellationDetails()
            pbcd.time = self.time
            if self.buyer_data  : pbcd.buyer_data = self.buyer_data
            if self.seller_data : pbcd.seller_data = self.seller_data
            if self.memo        : pbcd.memo = self.memo
            return pbcd.SerializeToString()
        except:
            raise SerializationError('A problem occurred while serializing the BargainingCancellationDetails with Protocol Buffers')
        
        
        
    def deserialize(pbuff): 
        '''
        Deserializes a protobuff message as a BargainingCancellationDetails
        
        Parameters:
            pbuff = protobuff message             
        '''
        if not pbuff: raise DeserializationError('Protocol Buffer message is empty')
        
        try:
            pbcd = bargaining_pb2.BargainingCancellationDetails()
            pbcd.ParseFromString(pbuff)
        except:
            raise DeserializationError('A problem occurred while deserializing the Protocol Buffers message associated to a BargainingCancellationDetails')         
        
        time  = pbcd.time
        bdata = pbcd.buyer_data
        sdata = pbcd.seller_data
        memo  = pbcd.memo
        return BargainingCancellationDetails(time, bdata, sdata, memo)
        
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
        return check_time(self) and check_memo(self)
        
         
        