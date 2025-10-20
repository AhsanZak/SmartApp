"""
Database Initialization Script
Automatically creates all database tables based on SQLAlchemy models
Reads configuration from config/app.toml and environment variables
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import OperationalError
import time

from config.database import Base, engine
from config.settings import get_settings, get_toml_config
from models import User, Document, Chat, Message
from models.document import DocumentChunk


def check_database_exists():
    """Check if database exists and is accessible"""
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True
    except OperationalError as e:
        print(f"❌ Cannot connect to database: {e}")
        return False


def enable_extensions():
    """No-op for SQLite; keep for compatibility"""
    print("\nUsing SQLite - no database extensions required")


def create_tables():
    """Create all tables defined in models"""
    print("\nCreating database tables...")
    
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("All tables created successfully.")
        
        # List created tables
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"\nCreated tables ({len(tables)}):")
        for table in sorted(tables):
            print(f"   - {table}")
            
    except Exception as e:
        print(f"Error creating tables: {e}")
        raise


def verify_tables():
    """Verify that all expected tables exist"""
    print("\nVerifying tables...")
    
    expected_tables = ['users', 'documents', 'document_chunks', 'chats', 'messages']
    
    try:
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()
        
        missing_tables = set(expected_tables) - set(existing_tables)
        
        if missing_tables:
            print(f"Missing tables: {', '.join(missing_tables)}")
            return False
        else:
            print("All expected tables exist.")
            
            # Show table details
            for table in expected_tables:
                columns = inspector.get_columns(table)
                print(f"\n   Table {table} ({len(columns)} columns):")
                for col in columns:
                    col_type = str(col['type'])
                    nullable = "NULL" if col['nullable'] else "NOT NULL"
                    print(f"      - {col['name']}: {col_type} {nullable}")
            
            return True
            
    except Exception as e:
        print(f"Error verifying tables: {e}")
        return False


def reset_database(force=False):
    """Drop all tables and recreate them (USE WITH CAUTION!)"""
    if not force:
        print("\nWARNING: This will delete ALL data in the database!")
        response = input("Are you sure you want to continue? (yes/no): ")
        if response.lower() != 'yes':
            print("Aborted")
            return False
    
    print("\nDropping all tables...")
    try:
        Base.metadata.drop_all(bind=engine)
        print("All tables dropped")
        
        # Recreate tables
        create_tables()
        return True
        
    except Exception as e:
        print(f"Error resetting database: {e}")
        return False


def show_database_info():
    """Display database connection information"""
    settings = get_settings()
    db_config = get_toml_config("database")
    
    print("\n" + "="*60)
    print("DATABASE CONFIGURATION")
    print("="*60)
    
    # Parse database URL to hide password
    db_url = settings.database_url
    if "@" in db_url:
        protocol_part = db_url.split("://")[0]
        rest = db_url.split("://")[1]
        if "@" in rest:
            credentials = rest.split("@")[0]
            location = rest.split("@")[1]
            username = credentials.split(":")[0]
            display_url = f"{protocol_part}://{username}:****@{location}"
        else:
            display_url = db_url
    else:
        display_url = db_url
    
    print(f"URL: {display_url}")
    
    if db_config:
        print(f"Host: {db_config.get('host', 'N/A')}")
        print(f"Port: {db_config.get('port', 'N/A')}")
        print(f"Database: {db_config.get('database', 'N/A')}")
        print(f"Username: {db_config.get('username', 'N/A')}")
    
    print("="*60 + "\n")


def main():
    """Main initialization function"""
    print("\n" + "="*60)
    print("SMART APP - DATABASE INITIALIZATION")
    print("="*60)
    
    # Show database info
    show_database_info()
    
    # Check database connection
    print("Checking database connection...")
    if not check_database_exists():
        print("\nFailed to connect to database!")
        print("\nPlease check:")
        print("1. Database server is running (docker-compose up -d postgres)")
        print("2. Database credentials in config/app.toml or .env are correct")
        print("3. Database exists (or will be created automatically)")
        sys.exit(1)
    
    print("Database connection successful.")
    
    # Wait a moment for database to be fully ready
    print("\nWaiting for database to be ready...")
    time.sleep(2)
    
    # Enable extensions
    enable_extensions()
    
    # Create tables
    create_tables()
    
    # Verify tables
    if verify_tables():
        print("\n" + "="*60)
        print("DATABASE INITIALIZATION COMPLETE")
        print("="*60)
        print("\nYour database is ready to use.")
        print("\nNext steps:")
        print("1. Start the backend: cd smtapp_core && uvicorn main:app --reload")
        print("2. Or use Docker: docker-compose up -d")
        print("3. Access API docs: http://localhost:8000/docs")
        print("\n" + "="*60 + "\n")
    else:
        print("\nInitialization completed with warnings")
        sys.exit(1)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Initialize Smart App Database")
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Drop all tables and recreate them (WARNING: deletes all data!)"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Skip confirmation prompts (use with --reset)"
    )
    parser.add_argument(
        "--verify-only",
        action="store_true",
        help="Only verify existing tables without creating new ones"
    )
    
    args = parser.parse_args()
    
    try:
        if args.verify_only:
            print("\nVerification Mode")
            show_database_info()
            if check_database_exists():
                verify_tables()
        elif args.reset:
            show_database_info()
            if check_database_exists():
                reset_database(force=args.force)
        else:
            main()
            
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nFatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

