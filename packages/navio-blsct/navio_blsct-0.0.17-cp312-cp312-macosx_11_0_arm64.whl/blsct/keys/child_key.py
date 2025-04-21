import blsct
from ..scalar import Scalar
from .scalar_based_key import ScalarBasedKey
from .child_key_desc.blinding_key import BlindingKey
from .child_key_desc.token_key import TokenKey
from .child_key_desc.tx_key import TxKey
from typing import Any, Self, override

class ChildKey(ScalarBasedKey):
  @staticmethod
  def from_scalar(seed: Scalar) -> Self:
    obj = blsct.from_seed_to_child_key(seed.value())
    return ChildKey(obj)

  def to_blinding_key(self) -> BlindingKey:
    obj = blsct.from_child_key_to_blinding_key(self.value())
    return BlindingKey(obj)

  def to_token_key(self) -> TokenKey:
    obj = blsct.from_child_key_to_token_key(self.value())
    return TokenKey(obj)

  def to_tx_key(self) -> TxKey:
    obj = blsct.from_child_key_to_tx_key(self.value())
    return TxKey(obj)

