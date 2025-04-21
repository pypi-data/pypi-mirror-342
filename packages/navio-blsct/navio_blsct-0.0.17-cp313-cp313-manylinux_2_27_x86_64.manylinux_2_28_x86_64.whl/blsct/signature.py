import blsct
from .managed_obj import ManagedObj
from .keys.public_key import PublicKey
from .scalar import Scalar
from typing import Any, Self, override

class Signature(ManagedObj):
  @staticmethod
  def generate(priv_key: Scalar, msg: str) -> Self:
    sig = blsct.sign_message(priv_key.value(), msg)
    return Signature(sig)

  def verify(self, msg: str, pub_key: PublicKey) -> bool:
    return blsct.verify_msg_sig(pub_key.value(), msg, self.value())

  @override
  def value(self) -> Any:
    return blsct.cast_to_signature(self.obj)

  @override
  def default_obj(self) -> Self:
    name = self.__class__.__name__
    raise NotImplementedError(f"{name}.default_obj()")

