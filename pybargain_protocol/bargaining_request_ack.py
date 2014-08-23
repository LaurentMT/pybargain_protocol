#!/usr/bin/env python
'''
Version: 0.0.1
Python library for the bargaining protocol
'''
from pybargain_protocol import bargaining_pb2
from pybargain_protocol.constants import MAINNET
from pybargain_protocol.exceptions import SerializationError, DeserializationError
from pybargain_protocol.protocol_rules import check_time, check_expires, check_network, check_outputs, check_memo


class BargainingRequestACKDetails(object):
    '''
    Details of a BargainingRequestACK message
    '''  
    
    '''
    ATTRIBUTES
    
    amount         = amount expected by seller (sum of outputs['amount']) 
    bargaining_url = secure (usually https) location where a BargainingMessage may be sent to negotiate    
    buyer_data     = arbitrary data that may be used by the buyer
    expires        = unix timestamp (UTC) after which the negotiation will be stopped 
    memo           = utf-8 encoded, plain-text (no formatting) note that should be displayed to the receiver (part of the negotiation)
    network        = bitcoin network (@see NETWORKS constant)
    outputs        = list of outputs ([{'amount': ..., 'script': ...}])
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
                 bargaining_url = '',
                 outputs = [],
                 memo = ''):
        '''
        Constructor
        
        Parameters:
            time           = unix timestamp associated to the message
            buyer_data     = arbitrary data that may be used by the buyer
            seller_data    = arbitrary data that may be used by the seller
            network        = bitcoin network (@see NETWORKS constant)
            expires        = unix timestamp (UTC) after which the negotiation will be stopped 
            bargaining_url = secure (usually https) location where a BargainingMessage may be sent to negotiate    
            outputs        = list of outputs ([{'amount': ..., 'script': ...}])
            memo           = utf-8 encoded, plain-text (no formatting) note that should be displayed to the receiver (part of the negotiation)
        ''' 
        self.time           = time
        self.buyer_data     = buyer_data
        self.seller_data    = seller_data
        self.network        = network
        self.expires        = expires
        self.bargaining_url = bargaining_url
        self.outputs        = outputs
        self.memo           = memo
        self.amount         = sum([o['amount'] for o in outputs])
        
        
    '''
    SERIALIZATION
    '''
    def serialize(self):
        '''
        Serializes the message (protobuff)
        '''
        try:
            pbbrad = bargaining_pb2.BargainingRequestACKDetails()
            pbbrad.time = self.time
            if self.buyer_data      : pbbrad.buyer_data = self.buyer_data
            if self.seller_data     : pbbrad.seller_data = self.seller_data
            if self.network         : pbbrad.network = self.network
            if self.expires != 0    : pbbrad.expires = self.expires
            if self.bargaining_url  : pbbrad.bargaining_url = self.bargaining_url
            if self.memo            : pbbrad.memo = self.memo
            for o in self.outputs:
                outp        = pbbrad.outputs.add()
                outp.amount = o['amount']
                outp.script = o['script']    
            return pbbrad.SerializeToString()
        except:
            raise SerializationError('A problem occurred while serializing the BargainingRequestACKDetails with Protocol Buffers')
        
                
    def deserialize(pbuff): 
        '''
        Deserializes a protobuff message as a BargainingRequestACKDetails
        
        Parameters:
            pbuff = protobuff message             
        '''
        if not pbuff: raise DeserializationError('Protocol Buffer message is empty')
        
        try:
            pbbrad = bargaining_pb2.BargainingRequestACKDetails()
            pbbrad.ParseFromString(pbuff)
        except:
            raise DeserializationError('A problem occurred while deserializing the Protocol Buffers message associated to a BargainingRequestACKDetails')         
        
        time    = pbbrad.time
        network = pbbrad.network
        bdata   = pbbrad.buyer_data
        sdata   = pbbrad.seller_data
        expires = pbbrad.expires
        burl    = pbbrad.bargaining_url 
        memo    = pbbrad.memo
        outputs = []
        for o in pbbrad.outputs: outputs.append({'amount': o.amount, 'script': o.script})
        return BargainingRequestACKDetails(time, bdata, sdata, network, expires, burl, outputs, memo)
        
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
               check_network(self) and\
               check_outputs(self) and\
               check_memo(self)
    
        