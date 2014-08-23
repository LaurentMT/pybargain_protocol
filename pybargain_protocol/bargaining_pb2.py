# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: bargaining.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)




DESCRIPTOR = _descriptor.FileDescriptor(
  name='bargaining.proto',
  package='bargaining',
  serialized_pb='\n\x10\x62\x61rgaining.proto\x12\nbargaining\"+\n\x06Output\x12\x11\n\x06\x61mount\x18\x01 \x01(\x04:\x01\x30\x12\x0e\n\x06script\x18\x02 \x02(\x0c\"\x9c\x01\n\x11\x42\x61rgainingMessage\x12\x10\n\x08msg_type\x18\x01 \x02(\t\x12\x1a\n\x0f\x64\x65tails_version\x18\x02 \x01(\r:\x01\x31\x12\x1a\n\x12serialized_details\x18\x03 \x02(\x0c\x12\x17\n\tsign_type\x18\x04 \x01(\t:\x04none\x12\x11\n\tsign_data\x18\x05 \x01(\x0c\x12\x11\n\tsignature\x18\x06 \x01(\x0c\"\x91\x01\n\x18\x42\x61rgainingRequestDetails\x12\x15\n\x07network\x18\x01 \x01(\t:\x04main\x12\x12\n\nbuyer_data\x18\x02 \x01(\x0c\x12\x13\n\x0bseller_data\x18\x03 \x01(\x0c\x12\x0c\n\x04time\x18\x04 \x02(\x04\x12\x0f\n\x07\x65xpires\x18\x05 \x01(\x04\x12\x16\n\x0e\x62\x61rgaining_url\x18\x06 \x01(\t\"\xc7\x01\n\x1b\x42\x61rgainingRequestACKDetails\x12\x15\n\x07network\x18\x01 \x01(\t:\x04main\x12\x12\n\nbuyer_data\x18\x02 \x01(\x0c\x12\x13\n\x0bseller_data\x18\x03 \x01(\x0c\x12\x0c\n\x04time\x18\x04 \x02(\x04\x12\x0f\n\x07\x65xpires\x18\x05 \x01(\x04\x12\x16\n\x0e\x62\x61rgaining_url\x18\x06 \x01(\t\x12#\n\x07outputs\x18\x07 \x03(\x0b\x32\x12.bargaining.Output\x12\x0c\n\x04memo\x18\x08 \x01(\t\"\x9d\x01\n\x19\x42\x61rgainingProposalDetails\x12\x12\n\nbuyer_data\x18\x01 \x01(\x0c\x12\x13\n\x0bseller_data\x18\x02 \x01(\x0c\x12\x0c\n\x04time\x18\x03 \x02(\x04\x12\x14\n\x0ctransactions\x18\x04 \x03(\x0c\x12%\n\trefund_to\x18\x05 \x03(\x0b\x32\x12.bargaining.Output\x12\x0c\n\x04memo\x18\x06 \x01(\t\"\x88\x01\n\x1c\x42\x61rgainingProposalACKDetails\x12\x12\n\nbuyer_data\x18\x01 \x01(\x0c\x12\x13\n\x0bseller_data\x18\x02 \x01(\x0c\x12\x0c\n\x04time\x18\x03 \x02(\x04\x12#\n\x07outputs\x18\x04 \x03(\x0b\x32\x12.bargaining.Output\x12\x0c\n\x04memo\x18\x05 \x01(\t\"x\n\x1b\x42\x61rgainingCompletionDetails\x12\x12\n\nbuyer_data\x18\x01 \x01(\x0c\x12\x13\n\x0bseller_data\x18\x02 \x01(\x0c\x12\x0c\n\x04time\x18\x03 \x02(\x04\x12\x14\n\x0ctransactions\x18\x04 \x03(\x0c\x12\x0c\n\x04memo\x18\x05 \x01(\t\"d\n\x1d\x42\x61rgainingCancellationDetails\x12\x12\n\nbuyer_data\x18\x01 \x01(\x0c\x12\x13\n\x0bseller_data\x18\x02 \x01(\x0c\x12\x0c\n\x04time\x18\x03 \x02(\x04\x12\x0c\n\x04memo\x18\x04 \x01(\tB*\n org.bitcoin.protocols.bargainingB\x06Protos')




_OUTPUT = _descriptor.Descriptor(
  name='Output',
  full_name='bargaining.Output',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='amount', full_name='bargaining.Output.amount', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='script', full_name='bargaining.Output.script', index=1,
      number=2, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=32,
  serialized_end=75,
)


_BARGAININGMESSAGE = _descriptor.Descriptor(
  name='BargainingMessage',
  full_name='bargaining.BargainingMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='msg_type', full_name='bargaining.BargainingMessage.msg_type', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='details_version', full_name='bargaining.BargainingMessage.details_version', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=True, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='serialized_details', full_name='bargaining.BargainingMessage.serialized_details', index=2,
      number=3, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sign_type', full_name='bargaining.BargainingMessage.sign_type', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=True, default_value=unicode("none", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sign_data', full_name='bargaining.BargainingMessage.sign_data', index=4,
      number=5, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='signature', full_name='bargaining.BargainingMessage.signature', index=5,
      number=6, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=78,
  serialized_end=234,
)


_BARGAININGREQUESTDETAILS = _descriptor.Descriptor(
  name='BargainingRequestDetails',
  full_name='bargaining.BargainingRequestDetails',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='network', full_name='bargaining.BargainingRequestDetails.network', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=True, default_value=unicode("main", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='buyer_data', full_name='bargaining.BargainingRequestDetails.buyer_data', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='seller_data', full_name='bargaining.BargainingRequestDetails.seller_data', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='time', full_name='bargaining.BargainingRequestDetails.time', index=3,
      number=4, type=4, cpp_type=4, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='expires', full_name='bargaining.BargainingRequestDetails.expires', index=4,
      number=5, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bargaining_url', full_name='bargaining.BargainingRequestDetails.bargaining_url', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=237,
  serialized_end=382,
)


_BARGAININGREQUESTACKDETAILS = _descriptor.Descriptor(
  name='BargainingRequestACKDetails',
  full_name='bargaining.BargainingRequestACKDetails',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='network', full_name='bargaining.BargainingRequestACKDetails.network', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=True, default_value=unicode("main", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='buyer_data', full_name='bargaining.BargainingRequestACKDetails.buyer_data', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='seller_data', full_name='bargaining.BargainingRequestACKDetails.seller_data', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='time', full_name='bargaining.BargainingRequestACKDetails.time', index=3,
      number=4, type=4, cpp_type=4, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='expires', full_name='bargaining.BargainingRequestACKDetails.expires', index=4,
      number=5, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bargaining_url', full_name='bargaining.BargainingRequestACKDetails.bargaining_url', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='outputs', full_name='bargaining.BargainingRequestACKDetails.outputs', index=6,
      number=7, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='memo', full_name='bargaining.BargainingRequestACKDetails.memo', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=385,
  serialized_end=584,
)


_BARGAININGPROPOSALDETAILS = _descriptor.Descriptor(
  name='BargainingProposalDetails',
  full_name='bargaining.BargainingProposalDetails',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='buyer_data', full_name='bargaining.BargainingProposalDetails.buyer_data', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='seller_data', full_name='bargaining.BargainingProposalDetails.seller_data', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='time', full_name='bargaining.BargainingProposalDetails.time', index=2,
      number=3, type=4, cpp_type=4, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='transactions', full_name='bargaining.BargainingProposalDetails.transactions', index=3,
      number=4, type=12, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='refund_to', full_name='bargaining.BargainingProposalDetails.refund_to', index=4,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='memo', full_name='bargaining.BargainingProposalDetails.memo', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=587,
  serialized_end=744,
)


_BARGAININGPROPOSALACKDETAILS = _descriptor.Descriptor(
  name='BargainingProposalACKDetails',
  full_name='bargaining.BargainingProposalACKDetails',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='buyer_data', full_name='bargaining.BargainingProposalACKDetails.buyer_data', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='seller_data', full_name='bargaining.BargainingProposalACKDetails.seller_data', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='time', full_name='bargaining.BargainingProposalACKDetails.time', index=2,
      number=3, type=4, cpp_type=4, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='outputs', full_name='bargaining.BargainingProposalACKDetails.outputs', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='memo', full_name='bargaining.BargainingProposalACKDetails.memo', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=747,
  serialized_end=883,
)


_BARGAININGCOMPLETIONDETAILS = _descriptor.Descriptor(
  name='BargainingCompletionDetails',
  full_name='bargaining.BargainingCompletionDetails',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='buyer_data', full_name='bargaining.BargainingCompletionDetails.buyer_data', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='seller_data', full_name='bargaining.BargainingCompletionDetails.seller_data', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='time', full_name='bargaining.BargainingCompletionDetails.time', index=2,
      number=3, type=4, cpp_type=4, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='transactions', full_name='bargaining.BargainingCompletionDetails.transactions', index=3,
      number=4, type=12, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='memo', full_name='bargaining.BargainingCompletionDetails.memo', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=885,
  serialized_end=1005,
)


_BARGAININGCANCELLATIONDETAILS = _descriptor.Descriptor(
  name='BargainingCancellationDetails',
  full_name='bargaining.BargainingCancellationDetails',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='buyer_data', full_name='bargaining.BargainingCancellationDetails.buyer_data', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='seller_data', full_name='bargaining.BargainingCancellationDetails.seller_data', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='time', full_name='bargaining.BargainingCancellationDetails.time', index=2,
      number=3, type=4, cpp_type=4, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='memo', full_name='bargaining.BargainingCancellationDetails.memo', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=1007,
  serialized_end=1107,
)

_BARGAININGREQUESTACKDETAILS.fields_by_name['outputs'].message_type = _OUTPUT
_BARGAININGPROPOSALDETAILS.fields_by_name['refund_to'].message_type = _OUTPUT
_BARGAININGPROPOSALACKDETAILS.fields_by_name['outputs'].message_type = _OUTPUT
DESCRIPTOR.message_types_by_name['Output'] = _OUTPUT
DESCRIPTOR.message_types_by_name['BargainingMessage'] = _BARGAININGMESSAGE
DESCRIPTOR.message_types_by_name['BargainingRequestDetails'] = _BARGAININGREQUESTDETAILS
DESCRIPTOR.message_types_by_name['BargainingRequestACKDetails'] = _BARGAININGREQUESTACKDETAILS
DESCRIPTOR.message_types_by_name['BargainingProposalDetails'] = _BARGAININGPROPOSALDETAILS
DESCRIPTOR.message_types_by_name['BargainingProposalACKDetails'] = _BARGAININGPROPOSALACKDETAILS
DESCRIPTOR.message_types_by_name['BargainingCompletionDetails'] = _BARGAININGCOMPLETIONDETAILS
DESCRIPTOR.message_types_by_name['BargainingCancellationDetails'] = _BARGAININGCANCELLATIONDETAILS

class Output(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _OUTPUT

  # @@protoc_insertion_point(class_scope:bargaining.Output)

class BargainingMessage(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _BARGAININGMESSAGE

  # @@protoc_insertion_point(class_scope:bargaining.BargainingMessage)

class BargainingRequestDetails(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _BARGAININGREQUESTDETAILS

  # @@protoc_insertion_point(class_scope:bargaining.BargainingRequestDetails)

class BargainingRequestACKDetails(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _BARGAININGREQUESTACKDETAILS

  # @@protoc_insertion_point(class_scope:bargaining.BargainingRequestACKDetails)

class BargainingProposalDetails(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _BARGAININGPROPOSALDETAILS

  # @@protoc_insertion_point(class_scope:bargaining.BargainingProposalDetails)

class BargainingProposalACKDetails(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _BARGAININGPROPOSALACKDETAILS

  # @@protoc_insertion_point(class_scope:bargaining.BargainingProposalACKDetails)

class BargainingCompletionDetails(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _BARGAININGCOMPLETIONDETAILS

  # @@protoc_insertion_point(class_scope:bargaining.BargainingCompletionDetails)

class BargainingCancellationDetails(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _BARGAININGCANCELLATIONDETAILS

  # @@protoc_insertion_point(class_scope:bargaining.BargainingCancellationDetails)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), '\n org.bitcoin.protocols.bargainingB\006Protos')
# @@protoc_insertion_point(module_scope)