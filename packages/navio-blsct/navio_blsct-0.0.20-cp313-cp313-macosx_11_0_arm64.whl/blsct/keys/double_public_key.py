import blsct
from ..managed_obj import ManagedObj
from .public_key import PublicKey
from ..scalar import Scalar
from typing import Self, override

class DoublePublicKey(ManagedObj):
  @staticmethod
  def from_public_keys(pk1: PublicKey, pk2: PublicKey) -> Self:
    rv = blsct.gen_double_pub_key(pk1.value(), pk2.value())
    dpk = DoublePublicKey(rv.value)
    blsct.free_obj(rv)
    return dpk

  @staticmethod
  def from_view_key_spending_pub_key_acct_addr(
    view_key: Scalar,
    spending_pub_key: PublicKey,
    account: int,
    address: int
  ) -> Self:
    obj = blsct.gen_dpk_with_keys_and_sub_addr_id(
      view_key.value(),
      spending_pub_key.value(),
      account,
      address
    )
    return DoublePublicKey(obj) 

  @override
  def value(self):
    return blsct.cast_to_dpk(self.obj)

  @override
  def default(self) -> Self:
    pk1 = PublicKey()
    pk2 = PublicKey()
    return DoublePublicKey.from_public_keys(pk1, pk2)
