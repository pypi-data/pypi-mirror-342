import blsct
from .managed_obj import ManagedObj
from typing import Any, Self, override

class Scalar(ManagedObj):
  """
  Wrapper for the finite field object provided by the `mcl`_ library (mclBnFr).

  .. _mcl: https://github.com/herumi/mcl

  This class provides finite field operations over the scalar field used in the BLS12-381 curve.
  """

  @staticmethod
  def random() -> Self:
    """Generate a random scalar"""
    rv = blsct.gen_random_scalar()
    scalar = Scalar(rv.value)
    blsct.free_obj(rv)
    return scalar

  @staticmethod
  def from_int(n: int) -> Self:
    """Create a scalar from an integer"""
    rv = blsct.gen_scalar(n)
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
    """Return the underlying native object"""
    return blsct.cast_to_scalar(self.obj)

  @classmethod
  def default_obj(cls) -> Any:
    """Return the underlying native object of the default Scalar object"""
    rv = blsct.gen_scalar(0)
    return rv.value

