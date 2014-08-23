#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Version: 0.0.1
Python library for the bargaining protocol
'''
import json
from bitcoin import address_to_script
from bitcoin.main import sha256, privtopub, pubtoaddr
from pybargain_protocol.constants import MAGIC_BYTES_TESTNET

'''
TEST VALUES
'''
TEST_PRIV1          = sha256('This is a private key')       
TEST_PUB1           = privtopub(TEST_PRIV1)                 
TEST_ADDR1          = pubtoaddr(TEST_PUB1, MAGIC_BYTES_TESTNET) # mryyjA6YpPCJ24MsSN7YnCK6M3NZoUAwxb

TEST_PRIV2          = sha256('This is another private key')
TEST_PUB2           = privtopub(TEST_PRIV2)
TEST_ADDR2          = pubtoaddr(TEST_PUB2, MAGIC_BYTES_TESTNET) # mftfwza9ZBwQRF2VW3YLuBhe8AkR2c2vrL

VALID_TIME1         = 1400100000L
VALID_TIME2         = 1400200000L
VALID_TIME3         = 1400300000L
VALID_TIME4         = 1400400000L
VALID_TIME5         = 1400500000L
VALID_TIME6         = 1400600000L
VALID_EXPIRES1      = 1401100000L
VALID_EXPIRES2      = 1401200000L

VALID_MEMO          = 'Ceci est le contenu d\'un memo.'
VALID_SELLER_DATA   = json.dumps({'product_id': 11521, 'user_id': 1, 'nego_id': 1})
VALID_BUYER_DATA    = json.dumps({'product_id': 11521, 'user_id': 2, 'nego_id': 4})
VALID_BARGAIN_URI1  = 'http://www.myhost1.com/bargain'
VALID_BARGAIN_URI2  = 'http://www.myhost2.com/bargain'

VALID_BUYER_AMOUNT  = 50000000
VALID_FEES          = 1000
VALID_REFUND_TO     = [{'script': address_to_script(TEST_ADDR1)}]

VALID_OUTPUTS1      = [{'amount': 100000000, 'script': address_to_script(TEST_ADDR2)}, 
                       {'amount': 150000000, 'script': address_to_script(TEST_ADDR2)}]
VALID_AMOUNT1       = VALID_OUTPUTS1[0]['amount'] + VALID_OUTPUTS1[1]['amount'] 

VALID_OUTPUTS2      = [{'amount': 100000000, 'script': address_to_script(TEST_ADDR2)}, 
                       {'amount': 50000000, 'script': address_to_script(TEST_ADDR2)}]
VALID_AMOUNT2       = VALID_OUTPUTS2[0]['amount'] + VALID_OUTPUTS2[1]['amount'] 



INVALID_MEMO        = VALID_MEMO.encode("utf-16")
INVALID_OUTPUTS     = [{'amount': 100000000}]
INVALID_EXPIRES     = 1300100000L
INVALID_NETWORK     = 'myfakenet'
INVALID_SIG         = 'ThisIsAnInvalidSignaturex3vKfIPlIB8IrbjAncp/1JBgHR/VC0c3ygdmTIw3Fi4KxKpRqDb7JfhhhFLhuzk='

