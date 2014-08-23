# Python Bargaining Protocol

This is a python library providing usefull classes to implement the Bargaining Protocol (https://github.com/LaurentMT/bargaining_protocol)

A demo application using this library can be found at : 
- https://github.com/LaurentMT/pybargain_demo_server (automated seller) 
- https://github.com/LaurentMT/pybargain_demo_client (simulation of an online wallet allowing to bargain with the seller)

Online demo : http://vps90685.ovh.net:8083/


## Python versions

Python 2.7.6


## Dependencies

PyBitcoinTools (https://github.com/vbuterin/pybitcointools) - A python library for Bitcoin
```
python setup.py install
```


## Installation

```
Gets the library from Github : https://github.com/LaurentMT/pybargain_protocol/archive/master.zip
Unzips the archive in a temp directory
python setup.py install
```


## Usage

The library provides
- a set of message wrapper classes. Basically, these classes manage the serialization/deserialization of the messages (protobuff) and their validation.
- a Negotiation class which manages the chain of messages (validation of protocol rules (format and consistency), storage of the chain) and the status of the negotiation. It's the central class of the library.
- a set of helpers classes to query the blockchain and manages transactions (creation, validation, ...)


## Links
 - Bargaining protocol : https://github.com/LaurentMT/bargaining_protocol
 - Demo server : https://github.com/LaurentMT/pybargain_demo_server
 - Demo client : https://github.com/LaurentMT/pybargain_demo_client


## Author
Twitter: @LaurentMT


## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request
