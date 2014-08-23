#!/usr/bin/env python
'''
Version: 0.0.1
Python library for the bargaining protocol
'''

import re
import json
import urllib2
import random
from bitcoin.transaction import deserialize
from pybargain_protocol.constants import MAINNET, TESTNET
from pybargain_protocol.exceptions import ThirdPartyServiceUnreachableError, InvalidTxHashError
from pybargain_protocol.helpers.build_check_tx import scriptsig_to_addr


'''
FUNCTIONS ALLOWING TO REQUEST THE BLOCKCHAIN VIA SOME APIs
'''


# Makes a request to a given URL (first argument) and optional params (second argument)
def make_request(*args):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0'+str(random.randrange(1000000)))]
    try:
        return opener.open(*args).read().strip()
    except Exception,e:
        try: p = e.read().strip()
        except: p = e
        raise Exception(p)
    
'''
GENERIC FUNCTIONS TO COMPUTES SUM OF INPUTS
'''
def _sum_inputs(tx, network = MAINNET, fetchtx = None):
    # Computes the sum of the inputs for a given transaction
    # Doesn't check if inputs are unspent
    # Checks that a txo does not appear several times as an input
    # Raises a ThirdPartyServiceUnreachableError if third-party service is unreachable
    # Raises a InvalidTxHashError if Tx Hash is not found in the blockchain
    if fetchtx is None: return 0
    txjson = tx if (type(tx) == dict) else deserialize(tx)
    txos = set()
    sum_inp = 0
    for i in range(len(txjson['ins'])):
        inp_hash = txjson['ins'][i]['outpoint']['hash']
        inp_idx = txjson['ins'][i]['outpoint']['index']
        txo = inp_hash + ':' + str(inp_idx)
        if not (txo in txos):
            txos.add(txo)        
            inp_tx = fetchtx(inp_hash, network)
            if inp_tx: 
                inp = deserialize(inp_tx)
                sum_inp += inp['outs'][inp_idx]['value']
    return sum_inp

def _sum_unspent_inputs(tx, network = MAINNET, unspent = None):
    # Computes the sum of the inputs for a given transaction
    # Checks if inputs are unspent
    # Checks that a txo does not appear several times as an input
    # Raises a ThirdPartyServiceUnreachableError if third-party service is unreachable
    # Raises a UtxoError if an input has already been spent
    if unspent is None: return 0
    txjson = tx if (type(tx) == dict) else deserialize(tx)
    txos = set()
    addr = set()  
    sum_inp = 0
    for i in range(len(txjson['ins'])):
        inp_hash = txjson['ins'][i]['outpoint']['hash']
        inp_idx = txjson['ins'][i]['outpoint']['index']
        in_addr = scriptsig_to_addr(txjson['ins'][i]['script'], network)
        txo = inp_hash + ':' + str(inp_idx)
        if not (txo in txos):
            txos.add(txo) 
            addr.add(in_addr)
    utxos = unspent(network, list(addr))
    for utxo in utxos:
        if utxo['output'] in txos:
            sum_inp += utxo['value']
            txos.remove(utxo['output'])
    return sum_inp


##################################################################################
# BLOCKR.IO API
# Initial code from pybitcoinstools.bci 
# Modified to work with bitcoin mainnet and testnet
##################################################################################
def _get_blockr_host(network):
    if network == MAINNET: return 'btc.blockr.io'
    else: return 'tbtc.blockr.io'


def blockr_pushtx(tx, network=MAINNET):
    if not re.match('^[0-9a-fA-F]*$', tx): tx = tx.encode('hex')
    url = 'https://%s/api/v1/tx/push' % _get_blockr_host(network)
    return make_request(url, '{"hex":"%s"}' % tx)


def blockr_fetchtx(txhash, network=MAINNET):
    if not re.match('^[0-9a-fA-F]*$',txhash): txhash = txhash.encode('hex')
    url = 'https://%s/api/v1/tx/raw/' % _get_blockr_host(network)
    try:
        jsondata = json.loads(make_request(url + txhash))
        return jsondata['data']['tx']['hex']
    except Exception,e:
        try:
            jsondata = json.loads(str(e))
            if jsondata['status'] == 'fail' and jsondata['code'] == 404: raise InvalidTxHashError(txhash)
            else: raise ThirdPartyServiceUnreachableError(str(e))
        except:
            raise ThirdPartyServiceUnreachableError(str(e))


def blockr_unspent(network=MAINNET, *args):
    # Valid input formats: blockr_unspent([addr1, addr2, addr3])
    #                      blockr_unspent(addr1, addr2, addr3)
    if len(args) == 0: return []
    elif isinstance(args[0],list): addrs = args[0]
    else: addrs = args
    url = 'https://%s/api/v1/address/unspent/' % _get_blockr_host(network)
    res = make_request(url+','.join(addrs))
    data = json.loads(res)['data']
    o = []
    if 'unspent' in data: data = [data]
    for dat in data:
        for u in dat['unspent']:
            o.append({
                "output": u['tx']+':'+str(u['n']),
                "value": int(u['amount'].replace('.',''))
            })
    return o


def blockr_sum_inputs(tx, network = MAINNET):
    # Computes the sum of the inputs for a given transaction
    # Doesn't check if inputs are unspent
    # Checks that a txo does not appear several times as an input
    # Raises a ThirdPartyServiceUnreachableError if blockr api is unreachable
    # Raises a InvalidTxHashError if Tx Hash is not found in the blockchain
    return _sum_inputs(tx, network, blockr_fetchtx)


def blockr_sum_unspent_inputs(tx, network = MAINNET):
    # Computes the sum of the inputs for a given transaction
    # Checks if inputs are unspent
    # Checks that a txo does not appear several times as an input
    # Raises a ThirdPartyServiceUnreachableError if blockr api is unreachable
    # Raises a UtxoError if an input has already been spent
    return _sum_unspent_inputs(tx, network, blockr_unspent)


##################################################################################
# BLOCKCHAIN.INFO API
# Initial code from pybitcoinstools.bci 
##################################################################################

def bci_pushtx(tx, network=MAINNET):
    # Pushes a transaction to the network using https://blockchain.info/pushtx
    if network == TESTNET: raise ThirdPartyServiceUnreachableError('Not implemented')
    if not re.match('^[0-9a-fA-F]*$', tx): tx = tx.encode('hex')
    return make_request('https://blockchain.info/pushtx','tx=' + tx)
        
        
def bci_fetchtx(txhash, network=MAINNET):
    print(txhash)
    if network == TESTNET: raise ThirdPartyServiceUnreachableError('Not implemented')
    if not re.match('^[0-9a-fA-F]*$', txhash): txhash = txhash.encode('hex')
    try:
        data = make_request('https://blockchain.info/rawtx/' + txhash + '?format=hex')
        return data
    except Exception,e:
        if str(e) == 'Transaction not found': raise InvalidTxHashError(txhash)
        else: raise ThirdPartyServiceUnreachableError(str(e))    


def bci_unspent(network=MAINNET, *args):
    # Valid input formats: bci_unspent([addr1, addr2,addr3])
    #                      bci_unspent(addr1, addr2, addr3)
    if network == TESTNET: raise ThirdPartyServiceUnreachableError('Not implemented')
    if len(args) == 0: return []
    elif isinstance(args[0],list): addrs = args[0]
    else: addrs = args
    u = []
    for addr in addrs:
        try: data = make_request('https://blockchain.info/unspent?address='+addr)
        except Exception,e: 
            if str(e) == 'No free outputs to spend': continue
            else: raise Exception(e)
        try:
            jsonobj = json.loads(data)
            for o in jsonobj["unspent_outputs"]:
                h = o['tx_hash'].decode('hex')[::-1].encode('hex')
                u.append({
                    "output": h+':'+str(o['tx_output_n']),
                    "value": o['value'] 
                })
        except:
            raise Exception("Failed to decode data: "+data)
    return u


def bci_sum_inputs(tx, network = MAINNET):
    # Computes the sum of the inputs for a given transaction
    # Doesn't check if inputs are unspent
    # Checks that a txo does not appear several times as an input
    # Raises a ThirdPartyServiceUnreachableError if bci api is unreachable
    # Raises a InvalidTxHashError if Tx Hash is not found in the blockchain
    return _sum_inputs(tx, network, bci_fetchtx)


def bci_sum_unspent_inputs(tx, network = MAINNET):
    # Computes the sum of the inputs for a given transaction
    # Checks if inputs are unspent
    # Checks that a txo does not appear several times as an input
    # Raises a ThirdPartyServiceUnreachableError if bci api is unreachable
    # Raises a UtxoError if an input has already been spent
    return _sum_unspent_inputs(tx, network, bci_unspent)



        