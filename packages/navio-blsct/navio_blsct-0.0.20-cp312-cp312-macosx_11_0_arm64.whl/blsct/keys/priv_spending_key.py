import blsct
from ..scalar import Scalar
from .scalar_based_key import ScalarBasedKey
from .child_key_desc.blinding_key import BlindingKey
from .child_key_desc.token_key import TokenKey
from .child_key_desc.tx_key import TxKey
from .child_key_desc.tx_key_desc.view_key import ViewKey
from .child_key_desc.tx_key_desc.spending_key import SpendingKey
from .public_key import PublicKey
from typing import Any, Self

class PrivSpendingKey(ScalarBasedKey):
  @staticmethod
  def generate(
    blinding_pub_key: PublicKey,
    view_key: ViewKey,
    spending_key: SpendingKey,
    account: int,
    address: int
  ) -> Self:
    blsct_psk = blsct.calc_priv_spending_key(
      blinding_pub_key.value(),
      view_key.value(),
      spending_key.value(),
      account,
      address
    )
    return PrivSpendingKey(blsct_psk)

