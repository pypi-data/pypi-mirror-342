import blsct
from .keys.public_key import PublicKey
from .scalar import Scalar
from typing import Self

class ViewTag():
  def __init__(
    self,
    blinding_pub_key: PublicKey,
    view_key: Scalar
  ) -> Self:
    self.value = blsct.calc_view_tag(
      blinding_pub_key.value(),
      view_key.value()
    )

  def value() -> int:
    return self.value

  def __str__(self):
    name = self.__class__.__name__
    return f"{name}({self.value})"

