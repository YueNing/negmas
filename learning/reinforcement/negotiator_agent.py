from typing import List, Optional, Any, TYPE_CHECKING, Union, Dict, Tuple, Type
from negmas.negotiators import Negotiator, AspirationMixin, Controller
from common import *
if TYPE_CHECKING:
    from .mechanisms import Mechanism
    from .outcomes import Issue, Outcome

class DQNNegotiator(Negotiator):
    """
    can directly develop a DQN agent, do not need to develop a 
    """
    __type__ = "DQNNegotiator"

    def propose(self, state: MechanismState) -> Optional["Outcome"]:

        pass

    def propose_(self, state: MechanismState):
        pass

