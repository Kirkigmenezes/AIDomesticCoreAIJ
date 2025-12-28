"""
Web-6 Semantic Graph Engine
Semantic knowledge graphs with 3D visualization and code mapping
"""

from typing import Dict, List, Set, Any, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum
import json
import uuid

class EntityType(Enum):
    """Types of semantic entities"""
    CODE_FUNCTION = "code_function"
    CODE_CLASS = "code_class"
    CODE_MODULE = "code_module"
    DATA_STRUCTURE = "data_structure"
    ALGORITHM = "algorithm"
    CONCEPT = "concept"
    DEPENDENCY = "dependency"

class RelationType(Enum):
    """Types of semantic relationships"""
    CALLS = "calls"
    INHERITS = "inherits"
    USES = "uses"
    IMPLEMENTS = "implements"
    DEPENDS_ON = "depends_on"
    RELATED_TO = "related_to"
    CONTAINS = "contains"

@dataclass
class SemanticEntity:
    """Semantic entity in knowledge graph"""
    id: str
    type: EntityType
    name: str
    description: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    tags: Set[str] = field(default_factory=set)
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "type": self.type.value,
            "name": self.name,
            "description": self.description,
            "tags": list(self.tags),
            "metadata": self.metadata
        }

@dataclass
class SemanticRelation:
    """Relationship between entities"""
    id: str
    source_id: str
    target_id: str
    type: RelationType
    weight: float = 1.0
    properties: Dict[str, Any] = field(default_factory=dict)

class Web6SemanticGraph:
    """
    Semantic knowledge graph for code understanding
    
    Features:
    - Entity extraction from code
    - Relationship inference
    - Semantic search
    - Graph visualization (3D embedding)
    - Code mapping and visualization
    - Context-aware recommendations
    """
    
    def __init__(self):
        self.entities: Dict[str, SemanticEntity] = {}
        self.relations: Dict[str, SemanticRelation] = {}
        self.entity_index: Dict[str, List[str]] = {}  # Index by type
        self.graph_embeddings: Dict[str, List[float]] = {}  # 3D embeddings
        
    def add_entity(self, entity: SemanticEntity) -> str:
        """Add semantic entity to graph"""
        self.entities[entity.id] = entity
        
        # Index by type
        if entity.type not in self.entity_index:
            self.entity_index[entity.type] = []
        self.entity_index[entity.type].append(entity.id)
        
        # Generate 3D embedding
        self.graph_embeddings[entity.id] = self._generate_embedding(entity)
        
        return entity.id
    
    def add_relation(self, relation: SemanticRelation) -> str:
        """Add semantic relation"""
        self.relations[relation.id] = relation
        return relation.id
    
    def extract_from_code(self, code: str, file_path: str) -> List[str]:
        """Extract semantic entities from source code"""
        entity_ids = []
        
        # Extract functions
        import re
        func_pattern = r'def\s+(\w+)\s*\((.*?)\)'
        for match in re.finditer(func_pattern, code):
            func_name = match.group(1)
            params = match.group(2)
            
            entity = SemanticEntity(
                id=str(uuid.uuid4()),
                type=EntityType.CODE_FUNCTION,
                name=func_name,
                description=f"Function {func_name} in {file_path}",
                metadata={
                    "file": file_path,
                    "line": code[:match.start()].count('\n'),
                    "parameters": [p.strip() for p in params.split(',') if p.strip()]
                }
            )
            entity_id = self.add_entity(entity)
            entity_ids.append(entity_id)
        
        # Extract classes
        class_pattern = r'class\s+(\w+)(?:\((.*?)\))?:'
        for match in re.finditer(class_pattern, code):
            class_name = match.group(1)
            bases = match.group(2) or ""
            
            entity = SemanticEntity(
                id=str(uuid.uuid4()),
                type=EntityType.CODE_CLASS,
                name=class_name,
                description=f"Class {class_name} in {file_path}",
                metadata={
                    "file": file_path,
                    "line": code[:match.start()].count('\n'),
                    "base_classes": [b.strip() for b in bases.split(',') if b.strip()]
                }
            )
            entity_id = self.add_entity(entity)
            entity_ids.append(entity_id)
        
        # Extract imports (dependencies)
        import_pattern = r'(?:from\s+(\S+)\s+)?import\s+([^\n]+)'
        for match in re.finditer(import_pattern, code):
            module = match.group(1) or "builtins"
            imports = match.group(2)
            
            entity = SemanticEntity(
                id=str(uuid.uuid4()),
                type=EntityType.DEPENDENCY,
                name=module,
                description=f"Dependency: {module}",
                metadata={"imports": imports.strip()}
            )
            entity_id = self.add_entity(entity)
            entity_ids.append(entity_id)
        
        return entity_ids
    
    def infer_relations(self) -> int:
        """Infer semantic relationships from code"""
        relation_count = 0
        
        # Infer dependency relations
        dependencies = [e for e in self.entities.values() 
                       if e.type == EntityType.DEPENDENCY]
        functions = [e for e in self.entities.values() 
                    if e.type == EntityType.CODE_FUNCTION]
        
        for func in functions:
            for dep in dependencies:
                # Create DEPENDS_ON relation
                relation = SemanticRelation(
                    id=str(uuid.uuid4()),
                    source_id=func.id,
                    target_id=dep.id,
                    type=RelationType.DEPENDS_ON,
                    weight=0.8
                )
                self.add_relation(relation)
                relation_count += 1
        
        return relation_count
    
    def search_semantic(self, query: str, entity_type: Optional[EntityType] = None) -> List[SemanticEntity]:
        """Semantic search in graph"""
        results = []
        query_lower = query.lower()
        
        for entity in self.entities.values():
            if entity_type and entity.type != entity_type:
                continue
            
            # Match name or description
            if (query_lower in entity.name.lower() or 
                query_lower in entity.description.lower() or
                any(query_lower in tag for tag in entity.tags)):
                results.append(entity)
        
        return results
    
    def get_related_entities(self, entity_id: str, relation_type: Optional[RelationType] = None) -> List[SemanticEntity]:
        """Get entities related to given entity"""
        related = []
        
        for relation in self.relations.values():
            if relation.source_id == entity_id:
                if relation_type is None or relation.type == relation_type:
                    related.append(self.entities[relation.target_id])
        
        return related
    
    def _generate_embedding(self, entity: SemanticEntity) -> List[float]:
        """Generate 3D embedding for visualization"""
        import hashlib
        
        # Simple hash-based embedding (can be replaced with proper semantic embeddings)
        hash_obj = hashlib.md5(entity.name.encode())
        hash_int = int(hash_obj.hexdigest(), 16)
        
        # Generate 3D coordinates using hash
        x = ((hash_int >> 0) % 1000) / 1000
        y = ((hash_int >> 10) % 1000) / 1000
        z = ((hash_int >> 20) % 1000) / 1000
        
        return [x, y, z]
    
    def generate_3d_visualization(self, format: str = "threejs") -> Dict[str, Any]:
        """Generate 3D visualization data"""
        
        nodes = []
        edges = []
        
        # Create nodes
        for entity in self.entities.values():
            nodes.append({
                "id": entity.id,
                "label": entity.name,
                "type": entity.type.value,
                "position": self.graph_embeddings.get(entity.id, [0, 0, 0]),
                "description": entity.description
            })
        
        # Create edges
        for relation in self.relations.values():
            edges.append({
                "source": relation.source_id,
                "target": relation.target_id,
                "type": relation.type.value,
                "weight": relation.weight
            })
        
        return {
            "format": format,
            "nodes": nodes,
            "edges": edges,
            "stats": {
                "node_count": len(nodes),
                "edge_count": len(edges),
                "types": list(set(n["type"] for n in nodes))
            }
        }
    
    def generate_code_map(self) -> Dict[str, Any]:
        """Generate interactive code map"""
        
        functions = [e for e in self.entities.values() 
                    if e.type == EntityType.CODE_FUNCTION]
        classes = [e for e in self.entities.values() 
                  if e.type == EntityType.CODE_CLASS]
        
        # Group by file
        files = {}
        for entity in self.entities.values():
            if "file" in entity.metadata:
                file_path = entity.metadata["file"]
                if file_path not in files:
                    files[file_path] = {"functions": [], "classes": []}
                
                if entity.type == EntityType.CODE_FUNCTION:
                    files[file_path]["functions"].append(entity.to_dict())
                elif entity.type == EntityType.CODE_CLASS:
                    files[file_path]["classes"].append(entity.to_dict())
        
        return {
            "type": "code_map",
            "files": files,
            "statistics": {
                "total_files": len(files),
                "total_functions": len(functions),
                "total_classes": len(classes),
                "total_entities": len(self.entities),
                "total_relations": len(self.relations)
            }
        }
    
    def export_to_json(self) -> str:
        """Export graph as JSON"""
        graph_data = {
            "entities": [e.to_dict() for e in self.entities.values()],
            "relations": [
                {
                    "id": r.id,
                    "source": r.source_id,
                    "target": r.target_id,
                    "type": r.type.value,
                    "weight": r.weight
                }
                for r in self.relations.values()
            ],
            "embeddings": self.graph_embeddings
        }
        return json.dumps(graph_data, indent=2)
