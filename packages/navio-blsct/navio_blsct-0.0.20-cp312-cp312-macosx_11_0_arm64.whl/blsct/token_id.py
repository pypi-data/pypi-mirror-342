import blsct
from .managed_obj import ManagedObj
from typing import Any, Self, override

class TokenId(ManagedObj):
  @staticmethod
  def from_token(token: int) -> Self:
    rv = blsct.gen_token_id(token);
    token_id = TokenId(rv.value)
    blsct.free_obj(rv)
    return token_id
 
  @staticmethod
  def from_token_and_subid(token: int, subid: int) -> Self:
    rv = blsct.gen_token_id_with_subid(token, subid) 
    token_id = TokenId(rv.value)
    blsct.free_obj(rv)
    return token_id

  def token(self) -> int:
    return blsct.get_token_id_token(self.value())

  def subid(self) -> int:
    return blsct.get_token_id_subid(self.value())

  @override
  def value(self):
    return blsct.cast_to_token_id(self.obj)

  @classmethod
  def default_obj(cls) -> Any:
    rv = blsct.gen_default_token_id()
    return rv.value

