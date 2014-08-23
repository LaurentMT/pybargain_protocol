#!/usr/bin/env python
'''
Version: 0.0.1
Python library for the bargaining protocol
'''
import math
from bitcoin.transaction import *
from pybargain_protocol.constants import MAINNET, MAGIC_BYTES_TESTNET, TESTNET, MAGIC_BYTES_MAINNET

# BITCOIN CONSTANTS
MIN_TX_SIZE = 100
MAX_BLOCK_SIZE = 1048576
MAX_MONEY_RANGE = 2100000000000000
SATOSHIS_TO_BITCOIN = 100000000


def build_tx_with_change(inputs,
                         outputs,
                         amount = 0, 
                         fees = 0,
                         change_addr = ''):
    '''
    Builds a transaction with an additional change output if necessary
    
    if amount + fees < sum(inputs['amount']) then adds an output with:
        * output['amount'] = sum(inputs['amount']) - amount - fees
        * output['script'] = script(change_addr)
                
    Parameters:
        inputs      = list of inputs ([{'output': u'txhash:vindex', 'value': ..., 'privkey': ...}])
        outputs     = list of outputs ([{'amount': ..., 'script': ...}])
        amount      = amount proposed by the buyer
        fees        = fees for this transaction
        change_addr = change address used if necessary
    '''
    outputs_cp = copy.deepcopy(outputs)
    # Computes the sum of inputs
    sum_inp = sum([i['value'] for i in inputs])
    
    # Creates a change output if necessary (and if we have a change address)
    if (amount + fees < sum_inp) and change_addr:
        change = sum_inp - amount - fees
        script = address_to_script(change_addr)
        outputs_cp.append({'amount': change, 'script': script})
    
    # Builds the tx
    tx = {'locktime': 0, 'version': 1, 'ins': [], 'outs': []}
    for i in inputs:
        i = i['output']
        tx['ins'].append({'outpoint': {'hash': i[:64], 'index': int(i[65:])}, 
                          'script': '', 
                          'sequence': 4294967295})
    for o in outputs_cp:
        tx['outs'].append({'script': o['script'], 'value': o['amount']})
    tx = serialize(tx)
    
    # Signs the tx
    for i in range(len(inputs)): 
        tx = sign(tx, i, inputs[i]['privkey'])
    return tx
    
    
def check_tx(tx):
    '''
    Checks validity of a transaction
    according to some of the rules defined in https://en.bitcoin.it/wiki/Protocol_rules#.22tx.22_messages
        
    Parameters:
        tx = transaction to be checked
    '''
    if (not tx) or (tx is None): return False
    
    # Deserializes the tx
    if type(tx) == dict:
        txjson = tx 
        txser = serialize(tx)
    else:
        txjson = deserialize(tx)
        txser = tx
    # 2. Make sure neither in or out lists are empty 
    if txjson['ins'] is None or len(txjson['ins']) == 0: return False
    if txjson['outs'] is None or len(txjson['outs']) == 0: return False
    # 3. Size in bytes < MAX_BLOCK_SIZE
    if len(txser) >= MAX_BLOCK_SIZE: return False 
    # 4. Each output value, as well as the total, must be in legal money range 
    sum_outs = 0
    for o in txjson['outs']:
        if (o['value'] < 0) or (o['value'] > MAX_MONEY_RANGE): return False
        else: sum_outs += o['value']
    if sum_outs > MAX_MONEY_RANGE: return False            
    # 5. Make sure none of the inputs have hash=0, n=-1 (coinbase transactions) 
    for i in txjson['ins']:
        if not i['outpoint']['hash'] and i['outpoint']['index'] == -1: 
            return False
    # 6. Check that nLockTime <= INT_MAX[1], size in bytes >= 100[2]
    if txjson['locktime'] >= math.pow(2,32): return False
    if len(txser) < MIN_TX_SIZE: return False
    
    return True
    
    
def check_tx_signatures(tx, network = MAINNET):
    '''
    Checks validity of tx signatures
    Supports P2PH and P2SH (n-of-m signatures)
    Returns True if valid, False otherwise
    
    Parameters:
        tx      = transaction
        network = network used
    '''
    magicbytes = MAGIC_BYTES_TESTNET if network == TESTNET else MAGIC_BYTES_MAINNET
    # Gets the tx in serialized/desrialized forms
    if type(tx) == dict:
        txjson = tx 
        txser = serialize(tx)
    else:
        txjson = deserialize(tx)
        txser = tx
    # Checks each tx input
    for i in range(len(txjson['ins'])):
        try:
            # Deserializes the input scriptsig
            scr_sig = deserialize_script(txjson['ins'][i]['script'])
            if len(scr_sig) == 2:
                # P2PH script
                # Computes script pubkey associated to input
                scr_pubkey = address_to_script(pubtoaddr(scr_sig[1], magicbytes))
                # Verifies input signature
                if not verify_tx_input(txser, i, scr_pubkey, scr_sig[0], scr_sig[1]): return False
            elif len(scr_sig) >= 3:
                # P2SH script
                # Extract signatures
                # (first item is 0; subsequent are sigs; filter out empty placeholder sigs)
                sigs = [s for s in scr_sig[1:-1] if s] 
                # Extracts scriptpubkey (last item)
                scr_pubkey_hex = scr_sig[-1] 
                scr_pubkey = deserialize_script(scr_pubkey_hex)
                # Extracts n (required number of signatures)
                n = scr_pubkey[0]
                # Extracts pubkeys
                # (first item is n, -2 is m, -1 is multisig op; we get everything else (the pubkeys))
                pubkeys = scr_pubkey[1:-2]
                # Checks signatures and number of valid signatures
                nbsig = 0
                for pubkey in pubkeys:
                    for sig in sigs:
                        if verify_tx_input(txser, i, scr_pubkey_hex, sig, pubkey): 
                            nbsig += 1
                            break
                if nbsig < n: return False
            else:
                # Not implemented or invalid scriptsig
                return False
        except:
            return False
    return True


def check_inputs_unicity(txs):
    '''
    Checks that inputs are unique among the given transactions 
    
    Parameters:
        txs = list of transactions
    '''
    txos = set()
    for tx in txs:
        txjson = tx if (type(tx) == dict) else deserialize(tx)
        for i in range(len(txjson['ins'])):
            inp_hash = txjson['ins'][i]['outpoint']['hash']
            inp_idx = txjson['ins'][i]['outpoint']['index']
            txo = inp_hash + ':' + str(inp_idx)
            if txo in txos: return False
            else: txos.add(txo)    
    return True


def check_outputs_exist(txs, outputs):
    '''
    Checks occurences of a list of outputs among a list of transactions
    Returns True if all outputs appear in a transaction of the given list, False otherwise
    
    Parameters:
        txs     = list of transactions
        outputs = list of outputs [{'amount': ..., 'script': ...}]
    '''
    outp_set = set([o['script'] + ':' + str(o['amount']) for o in outputs])
    for tx in txs:
        txjson = tx if (type(tx) == dict) else deserialize(tx)
        for o in txjson['outs']:
            outp = o['script'] + ':' + str(o['value'])
            if outp in outp_set:
                outp_set.remove(outp)
    return True if len(outp_set) == 0 else False


def scriptsig_to_addr(scr_sig, network = MAINNET):
    '''
    Returns the address corresponding to a given scriptsig
    
    Parameters:
        scr_sig = script sig
        network = network used
    '''
    magicbytes = MAGIC_BYTES_TESTNET if network == TESTNET else MAGIC_BYTES_MAINNET 
    if not (type(scr_sig) == dict): 
        scr_sig = deserialize_script(scr_sig)    
    if len(scr_sig) == 2:
        # P2PH script
        # Computes script pubkey associated to input
        return pubtoaddr(scr_sig[1], magicbytes)
    elif len(scr_sig) >= 3:
        scr_pubkey_hex = scr_sig[-1] 
        return p2sh_scriptaddr(scr_pubkey_hex, 196)
    else:
        return ''
    
    