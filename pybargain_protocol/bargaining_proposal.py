#!/usr/bin/env python
'''
Version: 0.0.1
Python library for the bargaining protocol
'''
from bitcoin.transaction import deserialize
from pybargain_protocol import bargaining_pb2
from pybargain_protocol.constants import MAINNET
from pybargain_protocol.exceptions import SerializationError, DeserializationError, UtxoError
from pybargain_protocol.protocol_rules import check_time, check_refund_to, check_memo, check_transactions
from pybargain_protocol.helpers.bc_api import blockr_sum_inputs
from pybargain_protocol.helpers.build_check_tx import check_inputs_unicity


class BargainingProposalDetails(object):
    '''
    Details of a BargainingProposal message
    '''  
    
    '''
    ATTRIBUTES
    
    amount       = amount proposed by buyer
    buyer_data   = arbitrary data that may be used by the buyer
    fees         = fees proposed by the buyer
    is_redeemable= flag indicating if this proposal is considered as redeemable
                   No checking done on buyer side.
                   A strong checking against the blockchain is done for the seller
    memo         = utf-8 encoded, plain-text (no formatting) note that should be displayed to the receiver (part of the negotiation)
    seller_data  = arbitrary data that may be used by the seller
    refund_to    = one or more outputs ([{'script': ...}]) where the seller may return funds, if necessary
    time         = unix timestamp associated to the message
    transactions = list of serialized transactions        
    '''     
    
    
    '''
    CONSTRUCTOR
    '''
    def __init__(self,
                 time = 0,
                 buyer_data = '',
                 seller_data = '', 
                 transactions = [], 
                 memo = '',
                 refund_to = [], 
                 amount = 0,
                 fees = 0,
                 is_redeemable = False):
        '''
        Constructor
        
        Parameters:
            time         = unix timestamp associated to the message
            buyer_data   = arbitrary data that may be used by the buyer
            seller_data  = arbitrary data that may be used by the seller
            transactions = list of serialized transactions
            memo         = utf-8 encoded, plain-text (no formatting) note that should be displayed to the receiver (part of the negotiation)
            refund_to    = one or more outputs ([{'script': ...}]) where the seller may return funds, if necessary
            amount       = amount proposed by buyer (set when buyer builds the message)
            fees         = fees proposed by the buyer (set when buyer builds the message)
            is_redeemable= flag indicating if this proposal is considered as redeemable
        ''' 
        self.time         = time
        self.buyer_data   = buyer_data
        self.seller_data  = seller_data
        self.transactions = transactions
        self.memo         = memo
        self.refund_to    = refund_to
        self.amount       = amount
        self.fees         = fees
        self.is_redeemable= is_redeemable
        
        
        
    '''
    SERIALIZATION
    '''
    def serialize(self):
        '''
        Serializes the message (protobuff)
        '''
        try:
            pbbpd = bargaining_pb2.BargainingProposalDetails()
            pbbpd.time = self.time
            if self.buyer_data  : pbbpd.buyer_data = self.buyer_data
            if self.seller_data : pbbpd.seller_data = self.seller_data
            if self.memo        : pbbpd.memo = self.memo
            for r in self.refund_to:
                rt = pbbpd.refund_to.add()
                rt.script = r['script']  
            for tx in self.transactions:
                pbbpd.transactions.append(tx)
            return pbbpd.SerializeToString()
        except:
            raise SerializationError('A problem occurred while serializing the BargainingProposalDetails with Protocol Buffers')
        
                
    def deserialize(pbuff): 
        '''
        Deserializes a protobuff message as a BargainingProposalDetails
        
        Parameters:
            pbuff = protobuff message             
        '''
        if not pbuff: raise DeserializationError('Protocol Buffer message is empty')
        
        try:
            pbbpd = bargaining_pb2.BargainingProposalDetails()
            pbbpd.ParseFromString(pbuff)
        except:
            raise DeserializationError('A problem occurred while deserializing the Protocol Buffers message associated to a BargainingProposalDetails')         
        
        time  = pbbpd.time
        bdata = pbbpd.buyer_data
        sdata = pbbpd.seller_data
        memo  = pbbpd.memo
        rt    = [{'script': r.script} for r in pbbpd.refund_to]
        txs   = [tx for tx in pbbpd.transactions]
        return BargainingProposalDetails(time, bdata, sdata, txs, memo, rt)
        
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
               check_refund_to(self, self.is_redeemable) and\
               check_transactions(self, network) and\
               check_memo(self)
    


    '''
    UTILITY METHODS
    '''
    def check_amount_fees_redeemable(self, seller_amount, network = MAINNET, fctn = blockr_sum_inputs):
        '''
        Extracts amount and fees proposed by the buyer
        from a list of transactions and from the previous amount proposed by the seller
        It also checks if all transactions are redeemable
                
        Parameters:
            seller_amount = amount proposed by the seller
            network       = network used
            fctn          = function used to compute the sum of the inputs for a given transaction
                            by querying the blockchain
                            see bc.api.blockr_sum_inputs() for signature and returned value
        '''
        is_redeemable = True
        sum_inp = 0
        sum_out = 0
        # Checks inputs unicity over all txs
        if not check_inputs_unicity(self.transactions):
            is_redeemable = False
            raise UtxoError('Duplicated TXOs')        
        for tx in self.transactions:
            # Deserializes the transaction
            txjson = tx if (type(tx) == dict) else deserialize(tx)
            sum_inp_tx =  fctn(tx, network)
            sum_out_tx = sum([o['value'] for o in txjson['outs']])
            sum_inp += sum_inp_tx
            sum_out += sum_out_tx
            if sum_inp_tx < sum_out_tx: is_redeemable = False
        # Computes amount and fees proposed by the buyer
        sum_fee = max(0, sum_inp - sum_out)
        buyer_amount = sum_inp - (sum_fee + sum_out - seller_amount)
        # Stores results
        self.amount = buyer_amount
        self.fees = sum_fee
        self.is_redeemable = is_redeemable
   
    
        