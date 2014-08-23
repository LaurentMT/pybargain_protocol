#!/usr/bin/env python
'''
Version: 0.0.1
Python library for the bargaining protocol
'''
from pybargain_protocol import bargaining_pb2
from pybargain_protocol.constants import MAINNET
from pybargain_protocol.exceptions import SerializationError, DeserializationError
from pybargain_protocol.protocol_rules import check_time, check_memo, check_transactions


class BargainingCompletionDetails(object):
    '''
    Details of a BargainingCompletion message
    '''  
    
    '''
    ATTRIBUTES
    
    buyer_data   = arbitrary data that may be used by the buyer
    memo         = utf-8 encoded, plain-text (no formatting) note that should be displayed to the receiver (part of the negotiation)
    seller_data  = arbitrary data that may be used by the seller
    time         = unix timestamp associated to the message
    transactions = list of serialized transactions sent to the network
    '''     
    
    '''
    CONSTRUCTOR
    '''
    def __init__(self,
                 time = 0,
                 buyer_data = '',
                 seller_data = '', 
                 transactions = [], 
                 memo = ''):
        '''
        Constructor
        
        Parameters:
            time         = unix timestamp associated to the message
            buyer_data   = arbitrary data that may be used by the buyer
            seller_data  = arbitrary data that may be used by the seller
            transactions = list of serialized transactions
            memo         = utf-8 encoded, plain-text (no formatting) note that should be displayed to the receiver (part of the negotiation)
        ''' 
        self.time         = time
        self.buyer_data   = buyer_data
        self.seller_data  = seller_data
        self.transactions = transactions
        self.memo         = memo
        
        
    '''
    SERIALIZATION
    '''
    def serialize(self):
        '''
        Serializes the message (protobuff)
        '''
        try:
            pbbcd = bargaining_pb2.BargainingCompletionDetails()
            pbbcd.time = self.time
            if self.buyer_data  : pbbcd.buyer_data = self.buyer_data
            if self.seller_data : pbbcd.seller_data = self.seller_data
            if self.memo        : pbbcd.memo = self.memo
            for tx in self.transactions:
                pbbcd.transactions.append(tx)
            return pbbcd.SerializeToString()
        except:
            raise SerializationError('A problem occurred while serializing the BargainingCompletionDetails with Protocol Buffers')
        
        
        
    def deserialize(pbuff): 
        '''
        Deserializes a protobuff message as a BargainingCompletionDetails
        
        Parameters:
            pbuff = protobuff message             
        '''
        if not pbuff: raise DeserializationError('Protocol Buffer message is empty')
        
        try:
            pbbcd = bargaining_pb2.BargainingCompletionDetails()
            pbbcd.ParseFromString(pbuff)
        except:
            raise DeserializationError('A problem occurred while deserializing the Protocol Buffers message associated to a BargainingCompletionDetails')         
        
        time  = pbbcd.time
        bdata = pbbcd.buyer_data
        sdata = pbbcd.seller_data
        memo  = pbbcd.memo
        txs   = [tx for tx in pbbcd.transactions]
        return BargainingCompletionDetails(time, bdata, sdata, txs, memo)
        
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
               check_memo(self) and\
               check_transactions(self, network)
               
