from pydantic import BaseModel
from typing import Optional
# Si més endevant s'implementa un usuari per fer logins, ens caldrà un model per ell
class Recipie(BaseModel):
    id: Optional[int] = None
    name: str
    ingredients: str
    instructions: str
