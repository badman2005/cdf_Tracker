import sqlite3
from database import get_db_connection

def seed_projects():
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Clear the old data so we don't have duplicates
    cursor.execute("DELETE FROM applications")

    # 2. Real Zambian Projects with Inspection Photos
    # Format: (name, nrc, category, receipt_id, data_hash, title, constituency, lat, lng, image_url)
    zambia_projects = [
        (
            'Chanda Mulenga', '111/11/1', 'Infrastructure', 'CDF-A1B2C3D4', 'hash_001',
            'Munali Market Shelter', 'Munali', -15.3895, 28.3512,
            'https://images.unsplash.com/photo-1590644365607-1c5a519a7a37' # Construction site photo
        ),
        (
            'Sarah Phiri', '222/22/1', 'Health', 'CDF-E5F6G7H8', 'hash_002',
            'Kanyama Clinic Wing', 'Kanyama', -15.4285, 28.2521,
            'https://images.unsplash.com/photo-1586771107445-d3ca888129ff' # Hospital build photo
        ),
        (
            'John Banda', '333/33/1', 'Agri', 'CDF-I9J0K1L2', 'hash_003',
            'Choma Maize Silos', 'Choma', -16.8085, 26.9821,
            'https://images.unsplash.com/photo-1500382017468-9049fed747ef' # Agriculture site photo
        ),
        (
            'Grace Mutale', '444/44/1', 'Education', 'CDF-M3N4O5P6', 'hash_004',
            'Ndola Tech Hub', 'Ndola', -12.9601, 28.6322,
            'https://images.unsplash.com/photo-1541913057-955a2912df6a' # School foundation photo
        )
    ]

    # 3. Insert the new data
    cursor.executemany('''
        INSERT INTO applications (name, nrc, category, receipt_id, data_hash, title, constituency, lat, lng, image_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', zambia_projects)

    conn.commit()
    conn.close()
    print("✓ SUCCESS: Database seeded with coordinates and Inspection Photos!")

if __name__ == '__main__':
    seed_projects()