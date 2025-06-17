"""
Mock Database cho Development Mode
In-memory storage để test mà không cần PostgreSQL thật
"""
import json
import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime


class MockDatabase:
    """Mock implementation của database cho development"""
    
    def __init__(self):
        """Khởi tạo in-memory storage"""
        self.tables = {
            "requirements": {},
            "features": {},
            "bugs": {},
            "code_changes": {},
            "tests": {},
            "test_results": {},
            "user_feedback": {},
            "documents": {},
            "code_files": {},
            "test_coverage": {},
            "relationships": {}
        }
        self.connection_count = 0
        self.query_count = 0
    
    def connect(self) -> bool:
        """Mô phỏng database connection"""
        self.connection_count += 1
        return True
    
    def disconnect(self):
        """Mô phỏng database disconnection"""
        pass
    
    def insert(self, table: str, data: Dict[str, Any]) -> str:
        """Insert data vào table"""
        self.query_count += 1
        
        if table not in self.tables:
            raise ValueError(f"Table {table} does not exist")
        
        # Generate ID nếu không có
        if "id" not in data:
            data["id"] = f"{table}_{uuid.uuid4().hex[:8]}"
        
        # Add timestamps
        data["created_at"] = datetime.now().isoformat()
        data["updated_at"] = datetime.now().isoformat()
        
        # Store data
        self.tables[table][data["id"]] = data.copy()
        
        return data["id"]
    
    def update(self, table: str, id: str, data: Dict[str, Any]) -> bool:
        """Update data trong table"""
        self.query_count += 1
        
        if table not in self.tables:
            raise ValueError(f"Table {table} does not exist")
        
        if id not in self.tables[table]:
            return False
        
        # Update data
        data["updated_at"] = datetime.now().isoformat()
        self.tables[table][id].update(data)
        
        return True
    
    def select(self, table: str, id: Optional[str] = None, 
               where: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Select data từ table"""
        self.query_count += 1
        
        if table not in self.tables:
            raise ValueError(f"Table {table} does not exist")
        
        # Get specific record by ID
        if id:
            if id in self.tables[table]:
                return [self.tables[table][id]]
            return []
        
        # Get all records
        results = list(self.tables[table].values())
        
        # Apply where conditions
        if where:
            filtered_results = []
            for record in results:
                match = True
                for key, value in where.items():
                    if key not in record or record[key] != value:
                        match = False
                        break
                if match:
                    filtered_results.append(record)
            results = filtered_results
        
        return results
    
    def delete(self, table: str, id: str) -> bool:
        """Delete record từ table"""
        self.query_count += 1
        
        if table not in self.tables:
            raise ValueError(f"Table {table} does not exist")
        
        if id in self.tables[table]:
            del self.tables[table][id]
            return True
        
        return False
    
    def search(self, table: str, query: str, fields: List[str]) -> List[Dict[str, Any]]:
        """Search records theo text query"""
        self.query_count += 1
        
        if table not in self.tables:
            return []
        
        results = []
        query_lower = query.lower()
        
        for record in self.tables[table].values():
            for field in fields:
                if field in record and isinstance(record[field], str):
                    if query_lower in record[field].lower():
                        results.append(record)
                        break
        
        return results
    
    def get_related_records(self, entity_id: str) -> List[Dict[str, Any]]:
        """Tìm records liên quan thông qua relationships"""
        self.query_count += 1
        
        related = []
        
        # Find relationships involving this entity
        for rel in self.tables["relationships"].values():
            if rel.get("source_entity_id") == entity_id:
                # Find target entity
                target_type = rel.get("target_entity_type", "").lower()
                target_id = rel.get("target_entity_id")
                
                if target_type in self.tables and target_id in self.tables[target_type]:
                    related.append({
                        "relationship": rel,
                        "entity": self.tables[target_type][target_id]
                    })
            
            elif rel.get("target_entity_id") == entity_id:
                # Find source entity
                source_type = rel.get("source_entity_type", "").lower()
                source_id = rel.get("source_entity_id")
                
                if source_type in self.tables and source_id in self.tables[source_type]:
                    related.append({
                        "relationship": rel,
                        "entity": self.tables[source_type][source_id]
                    })
        
        return related
    
    def get_stats(self) -> Dict[str, Any]:
        """Trả về database statistics"""
        stats = {
            "connection_count": self.connection_count,
            "query_count": self.query_count,
            "table_counts": {}
        }
        
        for table, records in self.tables.items():
            stats["table_counts"][table] = len(records)
        
        return stats
    
    def clear_all_data(self):
        """Xóa toàn bộ data (cho testing)"""
        for table in self.tables:
            self.tables[table].clear()
    
    def export_data(self) -> Dict[str, Any]:
        """Export toàn bộ data để backup"""
        return {
            "tables": self.tables,
            "stats": self.get_stats()
        }
    
    def import_data(self, data: Dict[str, Any]):
        """Import data từ backup"""
        if "tables" in data:
            self.tables = data["tables"]


# Factory function để tạo mock database
def create_mock_database() -> MockDatabase:
    """Tạo mock database instance"""
    return MockDatabase()


# Example usage và testing
if __name__ == "__main__":
    # Test mock database
    db = create_mock_database()
    
    print("🗄️ Testing Mock Database")
    print("=" * 40)
    
    # Test connection
    print(f"Connection: {db.connect()}")
    
    # Test insert
    req_id = db.insert("requirements", {
        "title": "Test Requirement",
        "description": "Test description",
        "priority": "high"
    })
    print(f"Inserted requirement: {req_id}")
    
    # Test insert relationship
    rel_id = db.insert("relationships", {
        "source_entity_id": req_id,
        "target_entity_id": "feat_001",
        "relationship_type": "implements",
        "source_entity_type": "requirement",
        "target_entity_type": "feature"
    })
    print(f"Inserted relationship: {rel_id}")
    
    # Test select
    requirements = db.select("requirements")
    print(f"Requirements count: {len(requirements)}")
    
    # Test search
    search_results = db.search("requirements", "test", ["title", "description"])
    print(f"Search results: {len(search_results)}")
    
    # Test update
    updated = db.update("requirements", req_id, {"priority": "critical"})
    print(f"Updated: {updated}")
    
    # Test related records
    related = db.get_related_records(req_id)
    print(f"Related records: {len(related)}")
    
    # Test stats
    stats = db.get_stats()
    print(f"Database stats: {stats}")
    
    print("\n✅ Mock Database test completed!") 