import flet as ft

class Disk:
   def __init__(self, id: str, name: str, total_capacity_gb: int, used_space_gb: int, contents: list[str]):
      self.id = id # Usar un UUID o timestamp para IDs únicos
      self.name = name
      self.total_capacity_gb = total_capacity_gb
      self.used_space_gb = used_space_gb
      self.contents = contents # Lista de strings, ej: ["Proyectos", "Backups"]

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
         "used_space_gb": self.used_space_gb,
         "contents": self.contents,
      }

   @staticmethod
   def from_dict(data: dict):
      return Disk(
         id=data["id"],
         name=data["name"],
         total_capacity_gb=data["total_capacity_gb"],
         used_space_gb=data["used_space_gb"],
         contents=data["contents"],
      )

# Variables importantes:
# - id: Identificador único del disco.
# - name, total_capacity_gb, used_space_gb, contents: Atributos del disco.
# - free_space_gb (property): Calcula el espacio libre.
# - usage_percentage (property): Calcula el porcentaje de uso.
# - to_dict(), from_dict(): Métodos para serialización/deserialización (útil para JSON/SQLite).