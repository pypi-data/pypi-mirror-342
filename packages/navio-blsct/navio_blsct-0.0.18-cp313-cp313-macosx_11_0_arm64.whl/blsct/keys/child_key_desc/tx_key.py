import blsct
from ..scalar_based_key import ScalarBasedKey
from .tx_key_desc.spending_key import SpendingKey
from .tx_key_desc.view_key import ViewKey
from typing import Any

class TxKey(ScalarBasedKey):
  def to_spending_key(self) -> SpendingKey:
    obj = blsct.from_tx_key_to_spending_key(self.value())
    return SpendingKey(obj)

  def to_view_key(self) -> ViewKey:
    obj = blsct.from_tx_key_to_view_key(self.value())
    return ViewKey(obj)

