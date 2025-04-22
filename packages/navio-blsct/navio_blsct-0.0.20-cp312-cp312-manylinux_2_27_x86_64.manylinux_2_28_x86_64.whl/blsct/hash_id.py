import blsct
from .keys.public_key import PublicKey
from .keys.child_key_desc.tx_key_desc.view_key import ViewKey
from .managed_obj import ManagedObj
from .scalar import Scalar
from typing import Any, Self, override

class HashId(ManagedObj):
  @staticmethod
  def generate(
    blinding_pub_key: PublicKey,
    spending_pub_key: PublicKey,
    view_key: ViewKey
  ) -> Self:
    obj = blsct.calc_hash_id(
      blinding_pub_key.value(),
      spending_pub_key.value(),
      view_key.value()
    )
    return HashId(obj)

  def to_hex(self) -> str:
    return blsct.get_key_id_hex(self.value())

  @override
  def value(self) -> Any:
    return blsct.cast_to_key_id(self.obj)
