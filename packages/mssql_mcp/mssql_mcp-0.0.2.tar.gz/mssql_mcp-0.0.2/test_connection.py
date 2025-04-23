import pytds

config = {
    "server": "192.168.100.21",
    "user": "sa",
    "password": "Tech@2025",
    "database": "P12_TECH"
}

try:
    print("Attempting to connect to SQL Server...")
    conn = pytds.connect(**config)
    cursor = conn.cursor()
    print("Connection successful!")
    
    print("\nTesting query execution...")
    cursor.execute("SELECT TOP 1 * FROM INFORMATION_SCHEMA.TABLES")
    row = cursor.fetchone()
    print(f"Query result: {row}")
    
    cursor.close()
    conn.close()
    print("\nConnection test completed successfully!")
except Exception as e:
    print(f"Error: {str(e)}")
