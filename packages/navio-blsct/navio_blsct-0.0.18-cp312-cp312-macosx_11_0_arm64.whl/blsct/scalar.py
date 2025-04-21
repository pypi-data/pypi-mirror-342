import blsct
from .managed_obj import ManagedObj
from typing import Any, Optional, override, Self

class Scalar(ManagedObj):
  """
  Represents a finite field element in the BLS12-381 G1 curve group.
  A wrapper of MclScalar_ in navio-core.

  .. _MclScalar: https://github.com/nav-io/navio-core/blob/master/src/blsct/arith/mcl/mcl_scalar.h

  >>> from blsct import Scalar
  >>> a = Scalar.from_int(123)
  >>> a.to_int()
  123
  >>> a.to_hex()
  '7b'
  """
  def __init__(self, value: Optional[int]):
    if isinstance(value, int):
      rv = blsct.gen_scalar(value)
      super().__init__(rv.value)
    elif value is None:
      super().__init__()
    else:
      raise ValueError(f"Scalar can only be instantiated with int, but got '{type(value).__name__}'")

  @staticmethod
  def random() -> Self:
    """Generate a random scalar"""
    rv = blsct.gen_random_scalar()
    scalar = Scalar(rv.value)
    blsct.free_obj(rv)
    return scalar

  def to_hex(self) -> str:
    """Convert the scalar to a hexadecimal string"""
    return blsct.scalar_to_hex(self.value())

  def to_int(self) -> int:
    """Convert the scalar to an integer"""
    return  blsct.scalar_to_uint64(self.value())

  @override
  def value(self) -> Any:
    return blsct.cast_to_scalar(self.obj)

  @classmethod
  def default_obj(cls) -> Any:
    rv = blsct.gen_scalar(0)
    return rv.value

