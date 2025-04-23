"""
Database module for PyPro.

This module provides a lightweight ORM and migration system.
It tries to use SQLAlchemy if available, with a fallback to
a simple database wrapper.
"""

import os
import sqlite3
import json
import logging
import sys
import importlib
import inspect
from datetime import datetime
from typing import Dict, Any, List, Type, Optional, Union, Tuple

try:
    import sqlalchemy
    from sqlalchemy import create_engine, Column, String, Integer, Boolean, DateTime, ForeignKey
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker, relationship
    SQLALCHEMY_AVAILABLE = True
except ImportError:
    SQLALCHEMY_AVAILABLE = False
    
    # Create dummy classes for type hints to work without SQLAlchemy
    class Column:
        def __init__(self, type_=None, primary_key=False, nullable=True, 
                     unique=False, default=None, *args, **kwargs):
            self.type_ = type_
            self.primary_key = primary_key
            self.nullable = nullable
            self.unique = unique
            self.default = default
            
    class String:
        def __init__(self, length=None):
            self.length = length
            
    class Integer:
        pass
        
    class Boolean:
        pass
        
    class DateTime:
        pass
        
    class ForeignKey:
        def __init__(self, reference):
            self.reference = reference
    
    def relationship(*args, **kwargs):
        return None


class SimpleModel:
    """
    Base class for models when SQLAlchemy is not available.
    
    This provides a simple ORM-like interface for SQLite databases.
    """
    __tablename__ = None
    __columns__ = {}
    __primary_key__ = None
    
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    @classmethod
    def create_table(cls, cursor):
        """Create the database table for this model."""
        if not cls.__tablename__:
            raise ValueError(f"Model {cls.__name__} has no __tablename__")
            
        columns = []
        for name, column in cls.__columns__.items():
            col_def = f"{name} {cls._get_column_type(column)}"
            
            if getattr(column, 'primary_key', False):
                if column.type_ == Integer:
                    col_def += " PRIMARY KEY AUTOINCREMENT"
                else:
                    col_def += " PRIMARY KEY"
                cls.__primary_key__ = name
                
            if not getattr(column, 'nullable', True):
                col_def += " NOT NULL"
                
            if getattr(column, 'unique', False):
                col_def += " UNIQUE"
                
            columns.append(col_def)
            
        create_stmt = f"CREATE TABLE IF NOT EXISTS {cls.__tablename__} ({', '.join(columns)})"
        cursor.execute(create_stmt)
    
    @staticmethod
    def _get_column_type(column):
        """Convert column type to SQLite type."""
        if column.type_ == String:
            length = getattr(column, 'length', None)
            return f"TEXT" if not length else f"VARCHAR({length})"
        elif column.type_ == Integer:
            return "INTEGER"
        elif column.type_ == Boolean:
            return "BOOLEAN"
        elif column.type_ == DateTime:
            return "TIMESTAMP"
        else:
            return "TEXT"
    
    def save(self, db):
        """Save this model instance to the database."""
        values = {}
        for name, column in self.__class__.__columns__.items():
            if hasattr(self, name):
                value = getattr(self, name)
                
                # Convert Python types to DB types
                if isinstance(value, datetime):
                    value = value.isoformat()
                elif isinstance(value, bool):
                    value = 1 if value else 0
                    
                values[name] = value
        
        # Handle primary key
        pk = self.__class__.__primary_key__
        if pk and hasattr(self, pk) and getattr(self, pk) is not None:
            # Update existing record
            set_clause = ", ".join([f"{k} = ?" for k in values.keys()])
            params = list(values.values())
            params.append(getattr(self, pk))
            
            query = f"UPDATE {self.__class__.__tablename__} SET {set_clause} WHERE {pk} = ?"
            db.cursor.execute(query, params)
        else:
            # Insert new record
            columns = ", ".join(values.keys())
            placeholders = ", ".join(["?"] * len(values))
            
            query = f"INSERT INTO {self.__class__.__tablename__} ({columns}) VALUES ({placeholders})"
            db.cursor.execute(query, list(values.values()))
            
            # Set the primary key if it was auto-generated
            if pk and not hasattr(self, pk):
                setattr(self, pk, db.cursor.lastrowid)
        
        db.conn.commit()
        return self
        
    @classmethod
    def get(cls, db, id):
        """Get a model instance by primary key."""
        if not cls.__primary_key__:
            raise ValueError(f"Model {cls.__name__} has no primary key")
            
        query = f"SELECT * FROM {cls.__tablename__} WHERE {cls.__primary_key__} = ?"
        db.cursor.execute(query, (id,))
        row = db.cursor.fetchone()
        
        if not row:
            return None
            
        # Convert row to dict
        result = {}
        for idx, col in enumerate(db.cursor.description):
            result[col[0]] = row[idx]
            
        return cls(**result)
    
    @classmethod
    def all(cls, db):
        """Get all instances of this model."""
        query = f"SELECT * FROM {cls.__tablename__}"
        db.cursor.execute(query)
        rows = db.cursor.fetchall()
        
        results = []
        for row in rows:
            # Convert row to dict
            result = {}
            for idx, col in enumerate(db.cursor.description):
                result[col[0]] = row[idx]
                
            results.append(cls(**result))
            
        return results
    
    @classmethod
    def filter(cls, db, **kwargs):
        """Filter instances by column values."""
        conditions = []
        params = []
        
        for key, value in kwargs.items():
            conditions.append(f"{key} = ?")
            params.append(value)
            
        where_clause = " AND ".join(conditions)
        query = f"SELECT * FROM {cls.__tablename__}"
        
        if where_clause:
            query += f" WHERE {where_clause}"
            
        db.cursor.execute(query, params)
        rows = db.cursor.fetchall()
        
        results = []
        for row in rows:
            # Convert row to dict
            result = {}
            for idx, col in enumerate(db.cursor.description):
                result[col[0]] = row[idx]
                
            results.append(cls(**result))
            
        return results
    
    def delete(self, db):
        """Delete this model instance from the database."""
        if not self.__class__.__primary_key__:
            raise ValueError(f"Model {self.__class__.__name__} has no primary key")
            
        pk = self.__class__.__primary_key__
        if not hasattr(self, pk):
            raise ValueError(f"Model instance has no primary key value")
            
        query = f"DELETE FROM {self.__class__.__tablename__} WHERE {pk} = ?"
        db.cursor.execute(query, (getattr(self, pk),))
        db.conn.commit()


class SimpleDatabase:
    """Simple database connection manager."""
    
    def __init__(self, database_url):
        self.database_url = database_url
        self.conn = None
        self.cursor = None
        self.connect()
        
    def connect(self):
        """Connect to the database."""
        if self.database_url.startswith('sqlite:///'):
            db_path = self.database_url[10:]
            self.conn = sqlite3.connect(db_path)
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
        else:
            raise ValueError(f"Unsupported database URL: {self.database_url}")
    
    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


# Model class to be used by applications
if SQLALCHEMY_AVAILABLE:
    # Use SQLAlchemy Base model
    Model = declarative_base()
else:
    # Use our simple model
    Model = SimpleModel


class Database:
    """Database connection and ORM wrapper."""
    
    def __init__(self, app=None):
        self.app = None
        self.engine = None
        self.session_factory = None
        self.simple_db = None
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize the database with an application."""
        self.app = app
        
        if SQLALCHEMY_AVAILABLE:
            # Use SQLAlchemy
            self.engine = create_engine(
                app.config.get('DATABASE_URL', 'sqlite:///pypro.db'),
                echo=app.config.get('DEBUG', False)
            )
            self.session_factory = sessionmaker(bind=self.engine)
            
            # Create tables for all models
            if app.config.get('CREATE_TABLES', True):
                self._create_sqlalchemy_tables()
        else:
            # Use simple database
            self.simple_db = SimpleDatabase(
                app.config.get('DATABASE_URL', 'sqlite:///pypro.db')
            )
            
            # Create tables for all models
            if app.config.get('CREATE_TABLES', True):
                self._create_simple_tables()
    
    def _create_sqlalchemy_tables(self):
        """Create tables for SQLAlchemy models."""
        # Find all models that inherit from Model
        models = []
        
        # Check main module
        if self.app.import_name == '__main__':
            main_module = sys.modules['__main__']
            for name, obj in inspect.getmembers(main_module):
                if inspect.isclass(obj) and issubclass(obj, Model) and obj != Model:
                    models.append(obj)
        else:
            # Check the app's module
            try:
                app_module = importlib.import_module(self.app.import_name)
                for name, obj in inspect.getmembers(app_module):
                    if inspect.isclass(obj) and issubclass(obj, Model) and obj != Model:
                        models.append(obj)
                        
                # Check submodules (models.py, etc.)
                for submodule_name in ['models', 'database']:
                    try:
                        submodule = importlib.import_module(f"{self.app.import_name}.{submodule_name}")
                        for name, obj in inspect.getmembers(submodule):
                            if inspect.isclass(obj) and issubclass(obj, Model) and obj != Model:
                                models.append(obj)
                    except ImportError:
                        pass
            except ImportError:
                pass
        
        # Create tables for found models
        if models:
            Model.metadata.create_all(self.engine)
            
    def _create_simple_tables(self):
        """Create tables for simple models."""
        # Find all models that inherit from SimpleModel
        models = []
        
        # Check main module
        if self.app.import_name == '__main__':
            main_module = sys.modules['__main__']
            for name, obj in inspect.getmembers(main_module):
                if inspect.isclass(obj) and issubclass(obj, SimpleModel) and obj != SimpleModel:
                    models.append(obj)
        else:
            # Check the app's module
            try:
                app_module = importlib.import_module(self.app.import_name)
                for name, obj in inspect.getmembers(app_module):
                    if inspect.isclass(obj) and issubclass(obj, SimpleModel) and obj != SimpleModel:
                        models.append(obj)
                        
                # Check submodules (models.py, etc.)
                for submodule_name in ['models', 'database']:
                    try:
                        submodule = importlib.import_module(f"{self.app.import_name}.{submodule_name}")
                        for name, obj in inspect.getmembers(submodule):
                            if inspect.isclass(obj) and issubclass(obj, SimpleModel) and obj != SimpleModel:
                                models.append(obj)
                    except ImportError:
                        pass
            except ImportError:
                pass
        
        # Create tables for found models
        for model_class in models:
            try:
                model_class.create_table(self.simple_db.cursor)
            except Exception as e:
                logging.error(f"Error creating table for {model_class.__name__}: {e}")
    
    def get_session(self):
        """Get a new SQLAlchemy session."""
        if not SQLALCHEMY_AVAILABLE:
            raise RuntimeError("SQLAlchemy is not available")
            
        return self.session_factory()
        
    def get_connection(self):
        """Get the database connection."""
        if SQLALCHEMY_AVAILABLE:
            return self.engine.connect()
        else:
            return self.simple_db


class Migration:
    """
    Database migration helper.
    
    This class helps manage schema changes over time.
    """
    
    def __init__(self, db, migrations_dir='migrations'):
        self.db = db
        self.migrations_dir = migrations_dir
        
        # Ensure migrations directory exists
        if not os.path.exists(migrations_dir):
            os.makedirs(migrations_dir)
            
        # Create migrations table if it doesn't exist
        self._create_migrations_table()
    
    def _create_migrations_table(self):
        """Create the migrations tracking table if it doesn't exist."""
        if SQLALCHEMY_AVAILABLE:
            with self.db.get_connection() as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS migrations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL UNIQUE,
                        applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
        else:
            self.db.simple_db.cursor.execute("""
                CREATE TABLE IF NOT EXISTS migrations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            self.db.simple_db.conn.commit()
    
    def generate(self, name):
        """Generate a new migration file."""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f"{timestamp}_{name}.py"
        filepath = os.path.join(self.migrations_dir, filename)
        
        with open(filepath, 'w') as f:
            f.write("""
# Migration file generated by PyPro

def upgrade(db):
    \"\"\"
    Upgrade database schema.
    
    Args:
        db: Database connection
    \"\"\"
    # Example:
    # db.execute("CREATE TABLE new_table (id INTEGER PRIMARY KEY, name TEXT)")
    pass
    
def downgrade(db):
    \"\"\"
    Downgrade database schema.
    
    Args:
        db: Database connection
    \"\"\"
    # Example:
    # db.execute("DROP TABLE new_table")
    pass
""")
        
        print(f"Generated migration file: {filepath}")
        return filepath
    
    def get_applied_migrations(self):
        """Get list of applied migrations."""
        if SQLALCHEMY_AVAILABLE:
            with self.db.get_connection() as conn:
                result = conn.execute("SELECT name FROM migrations ORDER BY id")
                return [row[0] for row in result]
        else:
            self.db.simple_db.cursor.execute("SELECT name FROM migrations ORDER BY id")
            rows = self.db.simple_db.cursor.fetchall()
            return [row[0] for row in rows]
    
    def get_pending_migrations(self):
        """Get list of pending migrations."""
        applied = set(self.get_applied_migrations())
        all_migrations = []
        
        for filename in os.listdir(self.migrations_dir):
            if filename.endswith('.py'):
                migration_name = filename[:-3]  # Remove .py extension
                all_migrations.append((migration_name, os.path.join(self.migrations_dir, filename)))
        
        # Sort by timestamp prefix
        all_migrations.sort(key=lambda x: x[0])
        
        return [(name, path) for name, path in all_migrations if name not in applied]
    
    def migrate(self, target=None):
        """
        Run pending migrations.
        
        Args:
            target: Target migration to migrate to (exclusive), or None for all
        """
        pending = self.get_pending_migrations()
        
        for name, path in pending:
            if target and name == target:
                break
                
            try:
                # Load the migration module
                module_name = os.path.basename(path)[:-3]  # Remove .py extension
                spec = importlib.util.spec_from_file_location(module_name, path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Run the upgrade function
                if SQLALCHEMY_AVAILABLE:
                    with self.db.get_connection() as conn:
                        module.upgrade(conn)
                        conn.execute("INSERT INTO migrations (name) VALUES (?)", (name,))
                else:
                    module.upgrade(self.db.simple_db)
                    self.db.simple_db.cursor.execute("INSERT INTO migrations (name) VALUES (?)", (name,))
                    self.db.simple_db.conn.commit()
                    
                print(f"Applied migration: {name}")
                
            except Exception as e:
                print(f"Error applying migration {name}: {e}")
                raise
    
    def rollback(self, steps=1):
        """
        Rollback the last n migrations.
        
        Args:
            steps: Number of migrations to roll back
        """
        applied = self.get_applied_migrations()
        if not applied:
            print("No migrations to roll back.")
            return
            
        # Get the migrations to roll back
        to_rollback = applied[-steps:]
        
        for name in reversed(to_rollback):
            try:
                # Find the migration file
                filename = None
                for f in os.listdir(self.migrations_dir):
                    if f.endswith('.py') and f[:-3] == name:
                        filename = f
                        break
                
                if not filename:
                    print(f"Migration file for {name} not found. Skipping.")
                    continue
                    
                path = os.path.join(self.migrations_dir, filename)
                
                # Load the migration module
                module_name = os.path.basename(path)[:-3]  # Remove .py extension
                spec = importlib.util.spec_from_file_location(module_name, path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Run the downgrade function
                if SQLALCHEMY_AVAILABLE:
                    with self.db.get_connection() as conn:
                        module.downgrade(conn)
                        conn.execute("DELETE FROM migrations WHERE name = ?", (name,))
                else:
                    module.downgrade(self.db.simple_db)
                    self.db.simple_db.cursor.execute("DELETE FROM migrations WHERE name = ?", (name,))
                    self.db.simple_db.conn.commit()
                    
                print(f"Rolled back migration: {name}")
                
            except Exception as e:
                print(f"Error rolling back migration {name}: {e}")
                raise
