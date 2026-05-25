import asyncio
from config.database import db

async def test_connection():
    print("Testing MongoDB connection...")
    try:
        # Ping the admin database
        await db.command("ping")
        print("\n[SUCCESS] Successfully connected to MongoDB!")
        print(f"Connected Database Name: '{db.name}'")
    except Exception as e:
        print("\n[ERROR] Failed to connect to MongoDB.")
        print(f"Error Details: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_connection())
