import uuid
from typing import List, Optional
from core.models import Disk

class DiskService:
    def __init__(self):
        self._disks: List[Disk] = [] # Almacenamiento en memoria por ahora

    def add_disk(self, name: str, total_capacity_gb: int, used_space_gb: int, contents: list[str]) -> Disk:
        new_id = str(uuid.uuid4())
        new_disk = Disk(new_id, name, total_capacity_gb, used_space_gb, contents)
        self._disks.append(new_disk)
        return new_disk

    def get_all_disks(self) -> List[Disk]:
        return list(self._disks)

    def get_disk_by_id(self, disk_id: str) -> Optional[Disk]:
        return next((d for d in self._disks if d.id == disk_id), None)

    def update_disk(self, disk_id: str, name: str, total_capacity_gb: int, used_space_gb: int, contents: list[str]) -> Optional[Disk]:
        disk_to_update = self.get_disk_by_id(disk_id)
        if disk_to_update:
            disk_to_update.name = name
            disk_to_update.total_capacity_gb = total_capacity_gb
            disk_to_update.used_space_gb = used_space_gb
            disk_to_update.contents = contents
            return disk_to_update
        return None

    def delete_disk(self, disk_id: str) -> bool:
        initial_len = len(self._disks)
        self._disks = [d for d in self._disks if d.id != disk_id]
        return len(self._disks) < initial_len

    def filter_disks(self, name_query: str = "", content_query: str = "", min_free_gb: Optional[int] = None) -> List[Disk]:
        filtered = self._disks

        if name_query:
            filtered = [d for d in filtered if name_query.lower() in d.name.lower()]

        if content_query:
            filtered = [d for d in filtered if any(content_query.lower() in c.lower() for c in d.contents)]

        if min_free_gb is not None:
            filtered = [d for d in filtered if d.free_space_gb >= min_free_gb]

        return filtered

# Variables importantes:
# - _disks: Lista privada que almacena los objetos Disk.
# Métodos importantes:
# - add_disk, get_all_disks, get_disk_by_id, update_disk, delete_disk: Implementan el CRUD.
# - filter_disks: Gestiona la lógica de filtrado según los requisitos.