import flet as ft
from typing import List

class ContentItem:
    def __init__(self, description: str, size_gb: int):
        self.description = description
        self.size_gb = size_gb

    def to_dict(self):
        return {"description": self.description, "size_gb": self.size_gb}

    @staticmethod
    def from_dict(data: dict):
        return ContentItem(description=data.get("description", ""), size_gb=data.get("size_gb", 0))

class Disk:
    def __init__(self, id: str, name: str, total_capacity_gb: int, contents: List[ContentItem]):
        self.id = id
        self.name = name
        self.total_capacity_gb = total_capacity_gb
        self.contents = contents

    @property
    def used_space_gb(self) -> int:
        return sum(item.size_gb for item in self.contents)

    @property
    def free_space_gb(self) -> int:
        return self.total_capacity_gb - self.used_space_gb

    @property
    def usage_percentage(self) -> float:
        if self.total_capacity_gb == 0:
            return 0.0
        return (self.used_space_gb / self.total_capacity_gb) * 100

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "total_capacity_gb": self.total_capacity_gb,
            "contents": [item.to_dict() for item in self.contents],
        }

    @staticmethod
    def from_dict(data: dict):
        contents_list = [ContentItem.from_dict(item) for item in data.get("contents", [])]
        # The used_space_gb is now calculated, so it's not passed to the constructor
        return Disk(
            id=data.get("id"),
            name=data.get("name"),
            total_capacity_gb=data.get("total_capacity_gb"),
            contents=contents_list,
        )

# Variables importantes:
# - id: Identificador único del disco.
# - name, total_capacity_gb, used_space_gb, contents: Atributos del disco.
# - free_space_gb (property): Calcula el espacio libre.
# - usage_percentage (property): Calcula el porcentaje de uso.
# - to_dict(), from_dict(): Métodos para serialización/deserialización (útil para JSON/SQLite).