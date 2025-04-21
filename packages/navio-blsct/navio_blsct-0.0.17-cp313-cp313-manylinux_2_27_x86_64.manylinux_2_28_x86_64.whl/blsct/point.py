import blsct
from .managed_obj import ManagedObj
from typing import Any, Self, override

class Point(ManagedObj):
  @staticmethod
  def random() -> Self:
    rv = blsct.gen_random_point()
    point = Point.from_obj(rv.value)
    blsct.free_obj(rv)
    return point

  @staticmethod
  def base_point() -> Self:
    rv = blsct.gen_base_point()
    point = Point.from_obj(rv.value)
    blsct.free_obj(rv)
    return point

  def is_valid() -> bool:
    return blsct.is_valid_point(self.obj)

  def to_hex(self) -> str:
    return blsct.point_to_hex(self.value())

  @override
  def value(self) -> Any:
    return blsct.cast_to_point(self.obj)

  @classmethod
  def default_obj(cls) -> Any:
    rv = blsct.gen_base_point()
    return rv.value 
 
