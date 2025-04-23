from abc import abstractmethod

from relationalai.early_access.dsl.core.types import Type

class BindableTable:
    """
    A class representing a bindable table.
    """

    @abstractmethod
    def key_type(self) -> Type:
        pass

    @abstractmethod
    def physical_name(self) -> str:
        pass


class BindableAttribute:

    @property
    @abstractmethod
    def table(self) -> 'BindableTable':
        pass

    @abstractmethod
    def physical_name(self) -> str:
        pass

    @abstractmethod
    def type(self) -> 'Type':
        pass
