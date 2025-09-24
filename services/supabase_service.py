import os
from supabase import create_client, Client
from dotenv import load_dotenv
from core.models import Disk
from typing import List, Optional

load_dotenv()  # Carga las variables de entorno desde .env

# --- Supabase Configuration ---
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
# --- End Supabase Configuration ---

class SupabaseService:
    def __init__(self):
        self.client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    def add_disk(self, name: str, total_capacity_gb: int, used_space_gb: int, contents: list[str]) -> Optional[Disk]:
        disk_data = {
            "name": name,
            "total_capacity_gb": total_capacity_gb,
            "used_space_gb": used_space_gb,
            "contents": contents,
        }
        response = self.client.table('disks').insert(disk_data).execute()
        if response.data:
            # Assuming the returned data matches the Disk model structure
            # You might need to adjust this based on your actual table columns
            return Disk(
                id=response.data[0]['id'],
                name=response.data[0]['name'],
                total_capacity_gb=response.data[0]['total_capacity_gb'],
                used_space_gb=response.data[0]['used_space_gb'],
                contents=response.data[0]['contents']
            )
        return None

    def get_all_disks(self) -> List[Disk]:
        response = self.client.table('disks').select("*").execute()
        if response.data:
            return [
                Disk(
                    id=disk_data['id'],
                    name=disk_data['name'],
                    total_capacity_gb=disk_data['total_capacity_gb'],
                    used_space_gb=disk_data['used_space_gb'],
                    contents=disk_data['contents']
                )
                for disk_data in response.data
            ]
        return []

    def get_disk_by_id(self, disk_id: str) -> Optional[Disk]:
        response = self.client.table('disks').select("*").eq('id', disk_id).execute()
        if response.data:
            disk_data = response.data[0]
            return Disk(
                id=disk_data['id'],
                name=disk_data['name'],
                total_capacity_gb=disk_data['total_capacity_gb'],
                used_space_gb=disk_data['used_space_gb'],
                contents=disk_data['contents']
            )
        return None

    def update_disk(self, disk_id: str, name: str, total_capacity_gb: int, used_space_gb: int, contents: list[str]) -> Optional[Disk]:
        update_data = {
            "name": name,
            "total_capacity_gb": total_capacity_gb,
            "used_space_gb": used_space_gb,
            "contents": contents,
        }
        response = self.client.table('disks').update(update_data).eq('id', disk_id).execute()
        if response.data:
            disk_data = response.data[0]
            return Disk(
                id=disk_data['id'],
                name=disk_data['name'],
                total_capacity_gb=disk_data['total_capacity_gb'],
                used_space_gb=disk_data['used_space_gb'],
                contents=disk_data['contents']
            )
        return None

    def delete_disk(self, disk_id: str) -> bool:
        response = self.client.table('disks').delete().eq('id', disk_id).execute()
        return bool(response.data)

    def filter_disks(self, name_query: str = "", content_query: str = "", min_free_gb: Optional[int] = None) -> List[Disk]:
        # This is a basic implementation. Advanced filtering might require database functions or views.
        disks = self.get_all_disks()

        if name_query:
            disks = [d for d in disks if name_query.lower() in d.name.lower()]

        if content_query:
            disks = [d for d in disks if any(content_query.lower() in c.lower() for c in d.contents)]

        if min_free_gb is not None:
            disks = [d for d in disks if d.free_space_gb >= min_free_gb]

        return disks
