import blsct
from .managed_obj import ManagedObj
from .scalar import Scalar
from .keys.double_public_key import DoublePublicKey
from .keys.public_key import PublicKey
from .sub_addr_id import SubAddrId
from typing import Any, Self, override

class SubAddr(ManagedObj):
  @staticmethod
  def generate(
    view_key: Scalar,
    spending_pub_key: PublicKey,
    sub_addr_id: SubAddrId,
  ) -> Self:
    obj = blsct.derive_sub_address(
      view_key.value(),
      spending_pub_key.value(),
      sub_addr_id.value(),
    )
    return SubAddr(obj)

  @staticmethod
  def from_double_public_key(dpk: DoublePublicKey) -> Self:
    rv = blsct.dpk_to_sub_addr(dpk.value())
    inst = SubAddr(rv.value)
    blsct.free_obj(rv)
    return inst

  @override
  def value(self) -> Any:
    return blsct.cast_to_sub_addr(self.obj)

