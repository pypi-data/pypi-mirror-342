from dataclasses import dataclass
from typing import Optional


@dataclass
class ORMEntityType:
    id: str
    name: str
    preferred_id: Optional[str]

@dataclass
class ORMValueType:
    id: str
    name: str
    data_type: str

@dataclass
class ORMRole:
    id: str
    name: str
    relationship_name: str
    player: str

@dataclass
class SubtypeArrow:
    start: Optional[str]
    end: Optional[str]

@dataclass
class ORMUniquenessConstraint:
    id: str
    roles: list[str]
    identifies: Optional[str]