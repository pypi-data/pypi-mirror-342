import blsct
from .keys.child_key_desc.tx_key_desc.spending_key import SpendingKey
from .managed_obj import ManagedObj
from .out_point import OutPoint
from .point import Point
from .scalar import Scalar
from .script import Script
from .sub_addr import SubAddr
from .token_id import TokenId
from typing import Any, Self, Optional, Literal, override

TxOutputType = Literal["Normal", "StakedCommitment"]

class TxOut(ManagedObj):
  @staticmethod
  def generate(
    sub_addr: SubAddr,
    amount: int,
    memo: str,
    token_id: Optional[TokenId] = None,
    output_type: TxOutputType = 'Normal',
    min_stake: int = 0,
  ) -> Self:
    token_id = TokenId() if token_id is None else token_id

    rv = blsct.build_tx_out(
      sub_addr.value(),
      amount,
      memo,
      token_id.value(),
      blsct.Normal if output_type == "Normal" else blsct.StakedCommitment,
      min_stake
    )
    if rv.result != 0:
      blsct.free_obj(rv)
      raise ValueError(f"Failed to build TxOut")

    obj = TxOut(rv.value)
    blsct.free_obj(rv)
    return obj

  @override
  def value(self) -> Any:
    return blsct.cast_to_tx_out(self.obj)

  def get_value(self) -> int:
    return blsct.get_tx_out_value(self.value())

  def get_script_pub_key(self) -> Script:
    obj = blsct.get_tx_out_script_pubkey(self.value())
    return Script(obj)

  def get_spending_key(self) -> Point:
    obj = blsct.get_tx_out_spending_key(self.value())
    return Point(obj)

  def get_ephemeral_key(self) -> Point:
    obj = blsct.get_tx_out_ephemeral_key(self.value())
    return Point(obj)

  def get_blinding_key(self) -> Point:
    obj = blsct.get_tx_out_blinding_key(self.value())
    return Point(obj)

  def get_view_tag(self) -> int:
    return blsct.get_tx_out_view_tag(self.value())

  def get_range_proof_A(self) -> Point:
    obj = blsct.get_tx_out_range_proof_A(self.value())
    return Point(obj)

  def get_range_proof_B(self) -> Point:
    obj = blsct.get_tx_out_range_proof_B(self.value())
    return Point(obj)

  def get_range_proof_r_prime(self) -> Point:
    obj = blsct.get_tx_out_range_proof_r_prime(self.value())
    return Point(obj)

  def get_range_proof_s_prime(self) -> Point:
    obj = blsct.get_tx_out_range_proof_s_prime(self.value())
    return Point(obj)

  def get_range_proof_delta_prime(self) -> Point:
    obj = blsct.get_tx_out_range_proof_delta_prime(self.value())
    return Point(obj)

  def get_range_proof_alpha_hat(self) -> Point:
    obj = blsct.get_tx_out_range_proof_alpha_hat(self.value())
    return Point(obj)

  def get_range_proof_tau_x(self) -> Scalar:
    obj = blsct.get_tx_out_range_proof_tau_x(self.value())
    return Scalar(obj)

  def get_token_id(self) -> TokenId:
    obj = blsct.get_tx_out_token_id(self.value())
    return TokenId(obj)

