#!/usr/bin/env python
'''
Version: 0.0.1
Python library for the bargaining protocol
'''
from pybargain_protocol import bargaining_pb2
from pybargain_protocol.constants import MAINNET
from pybargain_protocol.exceptions import DeserializationError, SerializationError
from pybargain_protocol.protocol_rules import check_time, check_expires, check_network


class BargainingRequestDetails(object):
    '''
    Details of a BargainingRequest message
    '''  
    
    
    '''
    ATTRIBUTES
    
    bargaining_url = secure (usually https) location where a BargainingMessage may be sent to negotiate    
    buyer_data     = arbitrary data that may be used by the buyer
    expires        = unix timestamp (UTC) after which the negotiation will be stopped 
    network        = bitcoin network (@see NETWORKS constant)
    seller_data    = arbitrary data that may be used by the seller
    time           = unix timestamp associated to the message
    '''     
    
    '''
    CONSTRUCTOR
    '''
    def __init__(self, 
                 time = 0,
                 buyer_data = '', 
                 seller_data = '',
                 network = MAINNET,
                 expires = 0,
                 bargaining_url = ''):
        '''
        Constructor
        
        Parameters:
            time           = unix timestamp associated to the message
            buyer_data     = arbitrary data that may be used by the buyer
            seller_data    = arbitrary data that may be used by the seller
            network        = bitcoin network (@see NETWORKS constant)
            expires        = unix timestamp (UTC) after which the negotiation will be stopped 
            bargaining_url = secure (usually https) location where a BargainingMessage may be sent to negotiate             
        '''
        self.time           = time
        self.buyer_data     = buyer_data
        self.seller_data    = seller_data
        self.network        = network
        self.expires        = expires
        self.bargaining_url = bargaining_url
        
        
    '''
    SERIALIZATION
    '''
    def serialize(self):
        '''
        Serializes the message (protobuff)
        '''
        try:
            pbbrd = bargaining_pb2.BargainingRequestDetails()
            pbbrd.time = self.time
            if self.buyer_data      : pbbrd.buyer_data = self.buyer_data
            if self.seller_data     : pbbrd.seller_data = self.seller_data
            if self.network         : pbbrd.network = self.network
            if self.expires != 0    : pbbrd.expires = self.expires
            if self.bargaining_url  : pbbrd.bargaining_url = self.bargaining_url
            return pbbrd.SerializeToString()
        except:
            raise SerializationError('A problem occurred while serializing the BargainingRequestDetails with Protocol Buffers')
        
        
    def deserialize(pbuff): 
        '''
        Deserializes a protobuff message as a BargainingRequestDetails
        
        Parameters:
            msg_ser = protobuff message             
        '''
        if not pbuff: raise DeserializationError('Protocol Buffers message is empty')
        
        try:
            pbbrd = bargaining_pb2.BargainingRequestDetails()
            pbbrd.ParseFromString(pbuff)
        except:
            raise DeserializationError('A problem occurred while deserializing the Protocol Buffers message associated to a BargainingRequestDetails')         
        
        time    = pbbrd.time
        network = pbbrd.network
        bdata   = pbbrd.buyer_data
        sdata   = pbbrd.seller_data
        expires = pbbrd.expires
        burl    = pbbrd.bargaining_url 
        return BargainingRequestDetails(time, bdata, sdata, network, expires, burl)
       
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
               check_expires(self) and\
               check_network(self)
        