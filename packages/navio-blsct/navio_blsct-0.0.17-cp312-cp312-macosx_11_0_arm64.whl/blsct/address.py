import blsct
from .keys.double_public_key import DoublePublicKey
from enum import Enum, auto

class AddressEncoding(Enum):
  Bech32 = auto()
  Bech32M = auto()

class Address():
  @staticmethod
  def encode(dpk: DoublePublicKey, encoding: AddressEncoding):
    blsct_encoding = None
    if encoding == AddressEncoding.Bech32:
      blsct_encoding = blsct.Bech32
    elif encoding == AddressEncoding.Bech32M:
      blsct_encoding = blsct.Bech32M
    else:
      raise ValueError(f"Unknown encoding: {encoding}")

    dpk = blsct.cast_to_dpk(dpk.obj)
    rv = blsct.encode_address(dpk, blsct_encoding)
    if rv.result != 0:
      blsct.free_obj(rv)
      raise ValueError(f"Failed to encode address: {rv.result}")

    enc_addr = blsct.as_string(rv.value)
    blsct.free_obj(rv)
    return enc_addr

  @staticmethod
  def decode(addr: str):
    rv = blsct.decode_address(addr)
    if rv.result != 0:
      blsct.free_obj(rv)
      raise ValueError(f"Failed to decode address: {rv.result}")

    # move rv.value (blsct_dpk) to DoublePublicKey
    dpk = DoublePublicKey.from_obj(rv.value)
    blsct.free_obj(rv)

    return dpk
