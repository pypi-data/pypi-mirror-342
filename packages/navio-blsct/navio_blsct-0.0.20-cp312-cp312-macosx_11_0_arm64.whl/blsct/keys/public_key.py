import blsct
from ..managed_obj import ManagedObj
from ..scalar import Scalar
from .child_key_desc.tx_key_desc.view_key import ViewKey
from typing import Any, Self, override

class PublicKey(ManagedObj):
  @staticmethod
  def random() -> Self:
    rv = blsct.gen_random_public_key()
    pk = PublicKey(rv.value)
    blsct.free_obj(rv)
    return pk

  @staticmethod
  def from_scalar(scalar: Scalar) -> Self:
    blsct_pub_key = blsct.scalar_to_pub_key(scalar.value())
    return PublicKey(blsct_pub_key)

  @staticmethod
  def generate_nonce(
    blinding_pub_key: Self,
    view_key: ViewKey
  ) -> Self:
   blsct_nonce = blsct.calc_nonce(
     blinding_pub_key.value(),
     view_key.value()
   )
   return PublicKey(blsct_nonce)

  @override
  def value(self):
    return blsct.cast_to_pub_key(self.obj)

  @classmethod
  def default_obj(cls) -> Any:
    rv = blsct.gen_random_public_key()
    return rv.value

