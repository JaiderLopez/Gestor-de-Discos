import os
from supabase import create_client, Client
from dotenv import load_dotenv
from core.models import Disk, ContentItem
from typing import List, Optional

load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

class SupabaseService:
    def __init__(self):
        self.client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    def add_disk(self, name: str, total_capacity_gb: int, contents: List[ContentItem]) -> Optional[Disk]:
        # Convert ContentItem objects to dictionaries for JSONB storage
        contents_as_dicts = [item.to_dict() for item in contents]
        
        disk_data = {
            "name": name,
            "total_capacity_gb": total_capacity_gb,
            "contents": contents_as_dicts,
        }
        
        response = self.client.table('disks').insert(disk_data).execute()
        
        if response.data:
            return Disk.from_dict(response.data[0])
        return None

    def get_all_disks(self) -> List[Disk]:
        response = self.client.table('disks').select("*").execute()
        if response.data:
            return [Disk.from_dict(disk_data) for disk_data in response.data]
        return []

    def get_disk_by_id(self, disk_id: str) -> Optional[Disk]:
        response = self.client.table('disks').select("*").eq('id', disk_id).execute()
        if response.data:
            return Disk.from_dict(response.data[0])
        return None

    def update_disk(self, disk_id: str, name: str, total_capacity_gb: int, contents: List[ContentItem]) -> Optional[Disk]:
        contents_as_dicts = [item.to_dict() for item in contents]
        
        update_data = {
            "name": name,
            "total_capacity_gb": total_capacity_gb,
            "contents": contents_as_dicts,
        }
        
        response = self.client.table('disks').update(update_data).eq('id', disk_id).execute()
        
        if response.data:
            return Disk.from_dict(response.data[0])
        return None

    def delete_disk(self, disk_id: str) -> bool:
        response = self.client.table('disks').delete().eq('id', disk_id).execute()
        return bool(response.data)

    def filter_disks(self, name_query: str = "", content_query: str = "", min_free_gb: Optional[int] = None) -> List[Disk]:
        disks = self.get_all_disks()

        if name_query:
            disks = [d for d in disks if name_query.lower() in d.name.lower()]

        if content_query:
            # Search query in the description of each content item
            disks = [d for d in disks if any(content_query.lower() in item.description.lower() for item in d.contents)]

        if min_free_gb is not None:
            disks = [d for d in disks if d.free_space_gb >= min_free_gb]

        return disks
