from abc import ABC, abstractmethod
from dataclasses import dataclass

from typing import List, Type, Dict, Any, Optional, Union

from negmas import Mechanism, NamedObject, Agent, SAOMechanism
from negmas.helpers import get_full_type_name, instantiate, get_class
import uuid
import pandas as pd

__all__ = [
    "Visualizer", "MechanismVisualizer", "register_visualizer", "visualizer", "visualizer_type", "visualizer_type_name", "Widget"
]


@dataclass
class Widget:
    kind: str
    content: Any
    params: Dict[str, Any]


class Visualizer(ABC):
    """Base class for all visualizers in NegMAS"""
    def __init__(self, x: NamedObject = None):
        self.object: NamedObject = x

    @classmethod
    @abstractmethod
    def widget_names(cls) -> List[str]:
        """Returns the names of all widgets available"""
        return ["basic_info", "children"]

    @classmethod
    @abstractmethod
    def widget_kind(cls, widget_name: str) -> str:
        """Returns the widget type for some widget"""
        if widget_name == "basic_info":
            return "dict"
        if widget_name == "children":
            return "dict_list_dict"

    @classmethod
    @abstractmethod
    def widget_params(cls, widget_name: str) -> Dict[str, Type]:
        """Returns the names and types of all parameters of the given widget"""
        return dict()

    @abstractmethod
    def render_widget(self, name: str, params: Dict[str, Any] = None) -> Optional[Widget]:
        """Returns the content of a widget given its name and parameters as a dict"""
        if self.object is None:
            return None
        if name == "basic_info":
            return Widget(self.widget_kind(name), 
                            content=dict(
                                name=self.object.name, 
                                id=self.object.id, 
                                type=get_full_type_name(type(self.object)),
                            )
                          , params=params)
        if name == "children":
            # format {k: [Widget, Widget, Widget]} just contain the basic info, when 
            return Widget(
                kind=self.widget_kind(name),
                content={k: [visualizer(_).render_widget("basic_info").content for _ in v] for k, v in self.children.items()},
                params=params
            )

        return dict()

    @property
    @abstractmethod
    def children(self) -> Dict[str, List[NamedObject]]:
        """Returns all children of all categories"""

    @classmethod
    @abstractmethod
    def children_categories(cls) -> List[str]:
        """Returns the names of all children categories"""

    def children_of(self, category: str) -> List[NamedObject]:
        """Returns all children of a given category"""
        return self.children.get(category, [])

    @classmethod
    def default_widget_name(cls) -> Optional[str]:
        """Name of the default widget to display when showing this type of object. By default, it is the first widget
        returned by `widget_names`"""
        names = cls.widget_names()
        if len(names) < 1:
            return None
        return names[0]

    def default_widget(self) -> Dict[str, Any]:
        """Renders the default widget"""
        return self.render_widget(self.default_widget_name())


VISUALIZERS: Dict[str, str] = dict()


def register_visualizer(type_name: Union[str, Type[NamedObject]], visualizer_name: Union[str, Type[Visualizer]]):
    """
    Registers a visualizer type

    Args:
        type_name: The type for which the visualizer is registered
        visualizer_name: The visualizer type
    """
    VISUALIZERS[get_full_type_name(type_name)] = get_full_type_name(visualizer_name)


def visualizer(x: Union[str, Type[NamedObject], NamedObject]) -> Optional[Visualizer]:
    """Finds the visualizer of a given type or object.

    Remarks:

        - If no visualizer is already registered through `register_visualizer` for this type of object, the system will
          try the following in order:
          1. Try to read a class member called "visualizer_type" from the given object/type
          2. Try to add "Visualizer" to the type name and return an object of that type
          3. Return a vase Visualizer object
    """
    obj = None
    if isinstance(x, NamedObject):
        obj, x = x,  x.__class__
    return instantiate(visualizer_type(x), x=obj)


def visualizer_type(x: Union[str, Type[NamedObject], NamedObject]) -> Optional[Type[Visualizer]]:
    """Finds the type of the visualizer of a given type or object.

    Remarks:

        - If no visualizer is already registered through `register_visualizer` for this type of object, the system will
          try the following in order:
          1. Try to read a class member called "visualizer_type" from the given object/type
          2. Try to add "Visualizer" to the type name and return an object of that type
          3. Return a vase Visualizer object
    """
    if isinstance(x, NamedObject):
        x = x.__class__
    try:
        return get_class(x).visualizer_type()
    except (TypeError, AttributeError):
        pass
    type_name = get_full_type_name(x)
    v = VISUALIZERS.get(type_name, type_name + "Visualizer")
    try:
        return get_class(v)
    except TypeError:
        pass
    try:
        return get_class(v.split(".")[-1])
    except TypeError:
        pass
    return Visualizer


def visualizer_type_name(x: Union[str, Type[NamedObject], NamedObject]) -> Optional[Type[Visualizer]]:
    """Finds the type name of the visualizer of a given type or object.

    Remarks:

        - If no visualizer is already registered through `register_visualizer` for this type of object, the system will
          try the following in order:
          1. Try to read a class member called "visualizer_type" from the given object/type
          2. Try to add "Visualizer" to the type name and return an object of that type
          3. Return a vase Visualizer object
    """
    return get_full_type_name(visualizer_type(x))


class MechanismVisualizer(Visualizer):
    """
        Visualizer for Mechanism
        
        Info can be showed in MechanismVisalizer
        1. basic_info (dict)
        2. negotiator (children)
        3. offer_utils (graph_data)
    """

    @classmethod
    def widget_kind(cls, widget_name: str) -> str:
        if widget_name == "offer_utils":
            return "graph_data"
        return super().widget_kind(widget_name)

    @classmethod
    def widget_names(cls) -> List[str]:
        return ["offer_utils"] + super().widget_names()

    @classmethod
    def widget_params(cls, name: str) -> Dict[str, Type]:
        if name == "offer_utils":
            return {"first": str, "second": str}
        return super().widget_params(name)

    def render_widget(self, name: str, params: Dict[str, Any] = None) -> Optional[Widget]:
        """
            Render widget info contained in MechanismVisualizer
            return: class Widget, content: prepare for using dash to render
        """
        if name == 'offer_utils':
            # how to calculate offer_utils
            # faker member of self.object, offer_utils
            # offer_utils = self.object.offer_utils
            # realistic data come from self.object, need to analyse this object
            # self.object also running in the class CheckpointRunner
            history = pd.DataFrame(data=[_.__dict__ for _ in self.object.history])
            has_history = len(history) > 0
            if has_history:
                history = history.loc[~history.current_offer.isnull(), :]
            ufuns = self.object._get_ufuns()

            # format as following, utils value of current_offer
            # (1, 0.5, 1) 0 step 1.agent, 2.agent, 3.agent 
            # (1, 0.5, 1) 1 step
            # (1, 0.5, 1) 2 step
            offer_utils = [tuple(f(o) for f in ufuns) for o in history.current_offer]

            return Widget(
                kind=self.widget_kind(name), 
                content=dict(
                        id=(f'{get_full_type_name(type(self.object))}_{name}'), 
                        name=name, 
                        data=offer_utils
                    ), 
                params=params)
        else:
            return super().render_widget(name, params)

    @property
    def children(self) -> Dict[str, List[NamedObject]]:
        mech: Mechanism = self.object
        return {
            "negotiators": mech.negotiators
        }

    @classmethod
    def children_categories(cls) -> List[str]:
        return [
            "negotiators"]


class AgentVisualizer(Visualizer):
    """Visualizes an agent"""

    @classmethod
    def widget_kind(cls, widget_name: str) -> str:
        return super().widget_kind(widget_name)

    @classmethod
    def widget_names(cls) -> List[str]:
        return super().widget_names()

    @classmethod
    def widget_params(cls, widget_name: str) -> Dict[str, Type]:
        return super().widget_params(widget_name)

    def render_widget(self, name: str, params: Dict[str, Any] = None) -> Optional[Widget]:
        return super().render_widget(name, params)

    @property
    def children(self) -> Dict[str, List[NamedObject]]:
        agent: Agent = self.object
        return ["negotiators", [_.negotiator for _ in agent.running_negotiations]]

    @classmethod
    def children_categories(cls) -> List[str]:
        return ["negotiators"]


class WorldVisualizer(Visualizer):
    """Visualizes a world"""

    @classmethod
    def widget_kind(cls, widget_name: str) -> str:
        return super().widget_kind(widget_name)

    @classmethod
    def widget_names(cls) -> List[str]:
        return super().widget_names()

    @classmethod
    def widget_params(cls, widget_name: str) -> Dict[str, Type]:
        return super().widget_params(widget_name)

    def render_widget(self, name: str, params: Dict[str, Any] = None) -> Optional[Widget]:
        return super().render_widget(name, params)

    @classmethod
    def default_widget_name(cls) -> str:
        return super().default_widget_name()

    @property
    def children(self) -> Dict[str, List[NamedObject]]:
        # TODO:
        world = self.object
        return {
            "factories": world.factories
        }

    @classmethod
    def children_categories(cls) -> List[str]:
        pass


class SAOMechanismVisualizer(MechanismVisualizer):
    """ Visualizes a SAOMechanism"""


    @classmethod
    def widget_kind(cls, widget_name: str) -> str:
        return super().widget_kind(widget_name)

    @classmethod
    def widget_names(cls) -> List[str]:
        return super().widget_names()

    @classmethod
    def widget_params(cls, widget_name: str) -> Dict[str, Type]:
        return super().widget_params(widget_name)

    def render_widget(self, name: str, params: Dict[str, Any] = None) -> Optional[Widget]:
        return super().render_widget(name, params)

    @classmethod
    def default_widget_name(cls) -> str:
        return super().default_widget_name()

    @property
    def children(self) -> Dict[str, List[NamedObject]]:
        pass

    @classmethod
    def children_categories(cls) -> List[str]:
        pass
    




# register builtin visualizers
register_visualizer(Mechanism, MechanismVisualizer)
register_visualizer(SAOMechanism, SAOMechanismVisualizer)
