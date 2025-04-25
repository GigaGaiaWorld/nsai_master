import sqlite3
import json
import hashlib
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings
from config import paths

class DBConfig(BaseSettings):
    """
    Database configurations, supports environment variable overrides.
    """
    db_path: Path = Field(
        default=paths.get_abscase_path("history/langda.db"),
        description="SQLite path to the dictionary storage database"
    )

    class Config:
        env_prefix = "DICTDB_"
        env_file = ".env"


class DictEntry(BaseModel):
    """
    Dictionary entry model.
    """
    hash: str = Field(..., description="Primary key, hash value of the dictionary")
    content: Dict[str, Any] = Field(..., description="Dictionary content")
    force_update: bool = Field(False, description="Flag indicating if this entry should be updated with new hash on each update")


class DictDB:
    """
    A manager for dictionary storage using SQLite and Pydantic for data validation.
    """
    def __init__(self, config: DBConfig = DBConfig()):
        self.config = config
        self.conn = sqlite3.connect(str(self.config.db_path))
        self._create_table()

    def _create_table(self) -> None:
        """
        Create dictionary_storage table if it doesn't exist.
        """
        cursor = self.conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS dictionary_storage (
                hash TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                force_update BOOLEAN NOT NULL DEFAULT 0
            )
            """
        )
        self.conn.commit()

    def _generate_hash(self, content: Dict[str, Any]) -> str:
        """
        Generate a hash for the content. This can be used for generating new hashes
        for force_update items.
        
        Args:
            content: Dictionary content to hash
            
        Returns:
            str: MD5 hash of the content (first 8 characters)
        """
        content_str = json.dumps(content, sort_keys=True)
        return hashlib.md5(content_str.encode('utf-8')).hexdigest()[:8]

    def add_or_update(self, hash_value: str, content: Dict[str, Any], force_update: bool = False) -> str:
        """
        Add a new dictionary entry or update if already exists.
        
        Args:
            hash_value: Hash value serving as the primary key
            content: Dictionary content to store
            force_update: Flag indicating if this entry should always generate a new hash on update
            
        Returns:
            str: The hash value (possibly new if force_update is True)
        """
        cursor = self.conn.cursor()
        
        # Check if this is an update of a force_update entry
        if force_update:
            cursor.execute("SELECT force_update FROM dictionary_storage WHERE hash = ?", (hash_value,))
            result = cursor.fetchone()
            
            # If entry exists and is marked for force_update, generate a new hash
            if result and result[0]:
                # First delete the old entry
                cursor.execute("DELETE FROM dictionary_storage WHERE hash = ?", (hash_value,))
                # Generate a new hash value
                hash_value = self._generate_hash(content)
        
        # Convert dictionary to JSON string for storage
        content_json = json.dumps(content)
        
        # Validate with Pydantic model
        entry = DictEntry(hash=hash_value, content=content, force_update=force_update)
        
        # Insert or replace the entry
        cursor.execute(
            "INSERT OR REPLACE INTO dictionary_storage (hash, content, force_update) VALUES (?, ?, ?)",
            (entry.hash, content_json, int(force_update))
        )
        self.conn.commit()
        return hash_value

    def get_item(self, hash_value: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a dictionary by its hash value.
        
        Args:
            hash_value: The hash value of the dictionary to retrieve
            
        Returns:
            Optional[Dict[str, Any]]: The dictionary content or None if not found
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT content FROM dictionary_storage WHERE hash = ?", (hash_value,))
        row = cursor.fetchone()
        if not row:
            return None
        # Convert JSON string back to dictionary
        return json.loads(row[0])

    def get_item_with_update_flag(self, hash_value: str) -> Optional[Tuple[Dict[str, Any], bool]]:
        """
        Retrieve a dictionary by its hash value along with its force_update flag.
        
        Args:
            hash_value: The hash value of the dictionary to retrieve
            
        Returns:
            Optional[Tuple[Dict[str, Any], bool]]: Tuple of (content, force_update) or None if not found
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT content, force_update FROM dictionary_storage WHERE hash = ?", (hash_value,))
        row = cursor.fetchone()
        if not row:
            return None
        # Convert JSON string back to dictionary and boolean flag
        return json.loads(row[0]), bool(row[1])

    def get_all_items(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all dictionaries stored in the database.
        
        Returns:
            Dict[str, Dict[str, Any]]: Dictionary mapping hash values to their content
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT hash, content FROM dictionary_storage")
        rows = cursor.fetchall()
        
        result = {}
        for hash_value, content_json in rows:
            result[hash_value] = json.loads(content_json)
        
        return result

    def get_all_items_with_flags(self) -> Dict[str, Tuple[Dict[str, Any], bool]]:
        """
        Get all dictionaries stored in the database with their force_update flags.
        
        Returns:
            Dict[str, Tuple[Dict[str, Any], bool]]: Dictionary mapping hash values to (content, force_update) tuples
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT hash, content, force_update FROM dictionary_storage")
        rows = cursor.fetchall()
        
        result = {}
        for hash_value, content_json, force_update in rows:
            result[hash_value] = (json.loads(content_json), bool(force_update))
        
        return result

    def list_all_hashes(self) -> List[str]:
        """
        List all hash values in the database.
        
        Returns:
            List[str]: List of hash values
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT hash FROM dictionary_storage")
        rows = cursor.fetchall()
        return [row[0] for row in rows]

    def set_force_update_flag(self, hash_value: str, force_update: bool) -> bool:
        """
        Set the force_update flag for an entry.
        
        Args:
            hash_value: The hash value of the dictionary
            force_update: New flag value
            
        Returns:
            bool: True if successful, False if entry not found
        """
        cursor = self.conn.cursor()
        cursor.execute("UPDATE dictionary_storage SET force_update = ? WHERE hash = ?", 
                      (int(force_update), hash_value))
        self.conn.commit()
        return cursor.rowcount > 0

    def remove(self, hash_value: str) -> bool:
        """
        Remove a dictionary entry by hash value.
        
        Args:
            hash_value: The hash value of the dictionary to remove
            
        Returns:
            bool: True if deleted, False if not found
        """
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM dictionary_storage WHERE hash = ?", (hash_value,))
        self.conn.commit()
        return cursor.rowcount > 0

    def sync_with_dict(self, dict_data: Dict[str, Dict[str, Any]], 
                       force_update_flags: Optional[Dict[str, bool]] = None) -> Dict[str, int]:
        """
        Synchronize the database with the provided dictionary.
        - Add or update items that are in dict_data
        - Remove items that are in database but not in dict_data
        
        Args:
            dict_data: Dictionary of {hash: content} to sync with
            force_update_flags: Optional dictionary of {hash: force_update_flag}
            
        Returns:
            Dict[str, int]: Statistics of sync operation
        """
        stats = {
            "added": 0,
            "updated": 0,
            "deleted": 0,
            "retained": 0,
            "regenerated": 0  # For items that got new hash values
        }
        
        if force_update_flags is None:
            force_update_flags = {}
        
        # Get existing items with their flags
        cursor = self.conn.cursor()
        cursor.execute("SELECT hash, force_update FROM dictionary_storage")
        existing_items = {row[0]: bool(row[1]) for row in cursor.fetchall()}
        
        # Track new hash values for items that had force_update=True
        old_to_new_hash = {}
        processed_hashes = set()
        
        # Process updates with potential hash regeneration
        for hash_value, content in dict_data.items():
            force_update = force_update_flags.get(hash_value, False)
            
            if hash_value in existing_items:
                # Item exists - check if we need to regenerate hash
                if existing_items[hash_value] or force_update:
                    # This item needs a new hash
                    old_hash = hash_value
                    new_hash = self._generate_hash(content)
                    
                    # Remove old entry
                    cursor.execute("DELETE FROM dictionary_storage WHERE hash = ?", (old_hash,))
                    
                    # Insert with new hash
                    content_json = json.dumps(content)
                    cursor.execute(
                        "INSERT INTO dictionary_storage (hash, content, force_update) VALUES (?, ?, ?)",
                        (new_hash, content_json, int(force_update))
                    )
                    
                    old_to_new_hash[old_hash] = new_hash
                    processed_hashes.add(new_hash)
                    stats["regenerated"] += 1
                else:
                    # Regular update
                    existing_content = self.get_item(hash_value)
                    if existing_content != content:
                        content_json = json.dumps(content)
                        cursor.execute(
                            "UPDATE dictionary_storage SET content = ? WHERE hash = ?",
                            (content_json, hash_value)
                        )
                        stats["updated"] += 1
                    else:
                        stats["retained"] += 1
                    
                    # Update force_update flag if needed
                    if existing_items[hash_value] != force_update:
                        cursor.execute(
                            "UPDATE dictionary_storage SET force_update = ? WHERE hash = ?",
                            (int(force_update), hash_value)
                        )
                    
                    processed_hashes.add(hash_value)
            else:
                # New item
                content_json = json.dumps(content)
                cursor.execute(
                    "INSERT INTO dictionary_storage (hash, content, force_update) VALUES (?, ?, ?)",
                    (hash_value, content_json, int(force_update))
                )
                processed_hashes.add(hash_value)
                stats["added"] += 1
        
        # Process deletions (items in DB but not in input dict)
        existing_hashes = set(existing_items.keys())
        input_hashes = set(dict_data.keys())
        
        # We need to consider potential hash changes for force_update items
        effective_input_hashes = (input_hashes - set(old_to_new_hash.keys())) | set(old_to_new_hash.values())
        
        to_delete = existing_hashes - effective_input_hashes
        for hash_value in to_delete:
            cursor.execute("DELETE FROM dictionary_storage WHERE hash = ?", (hash_value,))
            stats["deleted"] += 1
        
        self.conn.commit()
        
        # Return mapping of old hashes to new hashes along with stats
        stats["hash_changes"] = old_to_new_hash
        
        return stats

    def cleanup(self, valid_hashes: List[str]) -> int:
        """
        Delete all entries whose hash values are not in the provided valid_hashes list.
        
        Args:
            valid_hashes: List of hash values to keep
            
        Returns:
            int: Number of entries removed
        """
        if not valid_hashes:
            # Remove all if no valid hashes provided
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM dictionary_storage")
            removed = cursor.rowcount
            self.conn.commit()
            return removed
            
        placeholders = ",".join("?" for _ in valid_hashes)
        query = f"DELETE FROM dictionary_storage WHERE hash NOT IN ({placeholders})"
        cursor = self.conn.cursor()
        cursor.execute(query, valid_hashes)
        removed = cursor.rowcount
        self.conn.commit()
        return removed

    def close(self) -> None:
        """
        Close the database connection.
        """
        self.conn.close()


if __name__ == "__main__":
    # Demo usage
    db = DictDB()
    
    # Sample dictionaries with force_update flags
    sample_dicts = {
        "hash1": {"name": "张三", "age": 25, "skills": ["Python", "SQL"]},
        "hash2": {"name": "李四", "age": 30, "skills": ["Java", "C++"]},
        "hash3": {"name": "王五", "age": 22, "skills": ["JavaScript", "HTML"]}
    }
    
    force_update_flags = {
        "hash1": True,  # This one will get a new hash on each update
        "hash2": False,
        "hash3": True   # This one will also get a new hash on each update
    }
    
    # Sync with database
    stats = db.sync_with_dict(sample_dicts, force_update_flags)
    print(f"Initial sync stats: {stats}")
    
    if "hash_changes" in stats:
        print("Hash changes:")
        for old_hash, new_hash in stats["hash_changes"].items():
            print(f"  {old_hash} -> {new_hash}")
    
    # Get all items with flags
    all_items = db.get_all_items_with_flags()
    print("\nAll items:")
    for hash_val, (content, force_update) in all_items.items():
        flag_str = "will update with new hash" if force_update else "static hash"
        print(f"  {hash_val} ({flag_str}): {content}")
    
    # Let's update some content and sync again
    # We need to use the potentially new hash values from the first sync
    new_dicts = {}
    new_flags = {}
    
    # Copy items with their potentially new hashes
    for hash_val, (content, force_update) in all_items.items():
        # Make a small modification to each item
        content["updated"] = True
        new_dicts[hash_val] = content
        new_flags[hash_val] = force_update
    
    # Sync again
    stats = db.sync_with_dict(new_dicts, new_flags)
    print(f"\nSecond sync stats: {stats}")
    
    if "hash_changes" in stats:
        print("Hash changes:")
        for old_hash, new_hash in stats["hash_changes"].items():
            print(f"  {old_hash} -> {new_hash}")
    
    # Final check - should see new hashes for force_update items
    all_items = db.get_all_items_with_flags()
    print("\nFinal items:")
    for hash_val, (content, force_update) in all_items.items():
        flag_str = "will update with new hash" if force_update else "static hash"
        print(f"  {hash_val} ({flag_str}): {content}")
    
    db.close()