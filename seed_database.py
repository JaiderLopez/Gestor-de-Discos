from services.supabase_service import SupabaseService

def seed_data():
    """
    Inserts a few sample disks into the Supabase database.
    """
    service = SupabaseService()
    
    # Check if there's already data to avoid duplicates
    if service.get_all_disks():
        print("Database already contains data. Skipping seeding.")
        return

    print("Seeding database with sample data...")
    
    service.add_disk("SSD Principal", 500, 450, ["Sistema Operativo", "Apps"])
    service.add_disk("HDD Backups", 2000, 1200, ["Fotos Familiares", "Documentos"])
    service.add_disk("NVMe Juegos", 1000, 100, ["Juegos Actuales"])
    service.add_disk("USB Trabajo", 128, 10, ["Proyectos Activos"])
    service.add_disk("Servidor Media", 4000, 3800, ["Peliculas", "Series"])
    
    print("Seeding complete.")

if __name__ == "__main__":
    seed_data()
