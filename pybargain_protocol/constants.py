#!/usr/bin/env python
'''
Version: 0.0.1
Python library for the bargaining protocol
'''

# Protocol version
PROTOCOL_VERSION = 1

# Networks
MAINNET = 'main'
TESTNET = 'test'

NETWORKS = {MAINNET, TESTNET}

# Networks magic bytes
MAGIC_BYTES_MAINNET = 0
MAGIC_BYTES_TESTNET = 111
MAGIC_BYTES_MULTISIG_MAINNET = 5
MAGIC_BYTES_MULTISIG_TESTNET = 3

# Signatures types
SIGN_NONE         = 'none'
SIGN_ECDSA_SHA256 = 'ecdsa+sha256'

SIGN_TYPES = {SIGN_NONE, SIGN_ECDSA_SHA256}

# Messages types
TYPE_BARGAIN_REQUEST        = 'bargainingrequest'
TYPE_BARGAIN_REQUEST_ACK    = 'bargainingrequestack'
TYPE_BARGAIN_PROPOSAL       = 'bargainingproposal'
TYPE_BARGAIN_PROPOSAL_ACK   = 'bargainingproposalack' 
TYPE_BARGAIN_COMPLETION     = 'bargainingcompletion'
TYPE_BARGAIN_CANCELLATION   = 'bargainingcancellation'

# Sets of messages types per "thematic"
MESSAGE_TYPES = {TYPE_BARGAIN_REQUEST, TYPE_BARGAIN_REQUEST_ACK, 
                 TYPE_BARGAIN_PROPOSAL, TYPE_BARGAIN_PROPOSAL_ACK,
                 TYPE_BARGAIN_COMPLETION, TYPE_BARGAIN_CANCELLATION}

# Messages status
MSG_STATUS_KO  = 0
MSG_STATUS_OK  = 1
MSG_STATUS_UND = 2

# Negotiation status
NEGO_STATUS_INITIALIZATION = 0
NEGO_STATUS_NEGOTIATION = 1
NEGO_STATUS_COMPLETION = 2
NEGO_STATUS_COMPLETED = 3
NEGO_STATUS_CANCELLED = 4

NEGO_STATUS = {NEGO_STATUS_INITIALIZATION, NEGO_STATUS_NEGOTIATION, 
               NEGO_STATUS_COMPLETION, NEGO_STATUS_COMPLETED,
               NEGO_STATUS_CANCELLED}
    
# User roles
ROLE_BUYER  = 0
ROLE_SELLER = 1
    



