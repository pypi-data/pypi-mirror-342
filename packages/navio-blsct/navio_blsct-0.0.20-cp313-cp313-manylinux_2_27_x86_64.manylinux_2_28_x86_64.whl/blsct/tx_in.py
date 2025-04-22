import blsct
from .keys.child_key_desc.tx_key_desc.spending_key import SpendingKey
from .managed_obj import ManagedObj
from .out_point import OutPoint
from .script import Script
from .token_id import TokenId
from .tx_id import TxId
from typing import Any, Self, override

class TxIn(ManagedObj):
  @staticmethod
  def generate(
    amount: int,
    gamma: int,
    spending_key: SpendingKey,
    token_id: TokenId,
    out_point: OutPoint,
    rbf: bool = False,
  ) -> Self:
    rv = blsct.build_tx_in(
      amount,
      gamma,
      spending_key.value(),
      token_id.value(),
      out_point.value(),
      rbf
    )
    if rv.result != 0:
      blsct.free_obj(rv)
      raise ValueError(f"Failed to build TxIn")

    obj = TxIn(rv.value)
    blsct.free_obj(rv)
    return obj

  @override
  def value(self) -> Any:
    return blsct.cast_to_tx_in(self.obj)

  def get_prev_out_hash(self) -> TxId:
    tx_id = blsct.get_tx_in_prev_out_hash(self.value())
    return TxId(tx_id)

  def get_prev_out_n(self) -> int:
    return blsct.get_tx_in_prev_out_n(self.value())

  def get_script_sig(self) -> Script:
    script_sig = blsct.get_tx_in_script_sig(self.value())
    return Script(script_sig)

  def get_sequence(self) -> int:
    return blsct.get_tx_in_sequence(self.value())

  def get_script_witness(self) -> Script:
    script_witness = blsct.get_tx_in_script_witness(self.value())
    return Script(script_witness)

