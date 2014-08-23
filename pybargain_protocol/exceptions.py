'''
Version: 0.0.1
Exceptions
'''

class BaseError(Exception):
    '''
    Base exception class for the library
    '''
    pass


class InvalidRoleError(BaseError):
    '''
    Exception raised for errors related to an invalid role
    (a user tries to build/check a message not associated to her role)        
    '''    
    def __init__(self, operation = '', role = ''): 
        self._operation = operation
        self._role = role
        
    def __str__(self): 
        return 'Operation %s can not be processed by user with role %s' % (self.operation, self._role)
        

class InvalidDetailsError(BaseError):
    '''
    Exception raised for errors related to an invalid message details        
    '''    
    def __init__(self, message_type = ''):
        self._message_type = message_type
        
    def __str__(self): 
        return 'Invalid details for type : %s' % self._message_type
    
    
class SignatureError(BaseError):
    '''
    Exception raised for errors related to a signing operation        
    '''    
    def __init__(self):
        pass
        
    def __str__(self): 
        return 'A problem occured during message signing'


class InvalidSignatureTypeError(BaseError):
    '''
    Exception raised for errors related to an invalid signature type        
    '''    
    def __init__(self, sig_type = ''):
        self._sig_type = sig_type
        
    def __str__(self): 
        return 'Invalid signature type : %s' % self._sig_type
    
    
class InvalidMessageTypeError(BaseError):
    '''
    Exception raised for errors related to an invalid message type        
    '''    
    def __init__(self, message_type = ''):
        self._message_type = message_type
        
    def __str__(self): 
        return 'Invalid message type : %s' % self._message_type
    

class SerializationError(BaseError):
    '''
    Exception raised for errors related to serialization        
    '''    
    def __init__(self, error = ''):
        self._error = error
        
    def __str__(self): 
        return 'A problem was encountered during serialization : %s' % self._error
    

class UtxoError(BaseError):
    '''
    Exception raised for errors related to an invalid utxo (txo already spent)   
    '''    
    def __init__(self, error = ''):
        self._error = error
        
    def __str__(self): 
        return 'TXO alrady spent : %s' % self._error


class InvalidTxHashError(BaseError):
    '''
    Exception raised for errors related to an invalid tx hash       
    '''    
    def __init__(self, error = ''):
        self._error = error
        
    def __str__(self): 
        return 'Invalid hash of transaction : %s' % self._error


class ThirdPartyServiceUnreachableError(BaseError):
    '''
    Exception raised for errors related to an unreachable third party service        
    '''    
    def __init__(self, error = ''):
        self._error = error
        
    def __str__(self): 
        return 'A problem was encountered during connection with a third-party service : %s' % self._error


class DeserializationError(BaseError):
    '''
    Exception raised for errors related to deserialization        
    '''    
    def __init__(self, error = ''):
        self._error = error
        
    def __str__(self): 
        return 'A problem was encountered during deserialization : %s' % self._error


class NotImplementedError(BaseError):
    '''
    Exception raised when a feature is not implemented
    '''    
    def __init__(self): 
        pass
        
    def __str__(self): 
        return "Feature not implemented"