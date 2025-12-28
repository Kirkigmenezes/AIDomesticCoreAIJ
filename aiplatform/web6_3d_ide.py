"""
Web-6 3D IDE: Three-Dimensional Code Universe

Transforms code into interactive 3D space where:
  - Folders → Planets
  - Files → Continents
  - Classes → Buildings
  - Functions → Nodes
  - Dependencies → Gravitational bonds

Enables:
  • 3D code review and exploration
  • 3D change history visualization
  • 3D architecture maps for AI agents
  • AI agents walking through projects
  • Real-time spatial interaction

First IDE in the world with true 3D codebase visualization.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Tuple, Set, Optional, Any
import math
import hashlib
from datetime import datetime
import json


class EntityType(Enum):
    """Types of entities in 3D space."""
    UNIVERSE = "universe"      # Root container
    PLANET = "planet"          # Folder/directory
    CONTINENT = "continent"    # File/module
    BUILDING = "building"      # Class/interface
    NODE = "node"              # Function/method
    LINK = "link"              # Dependency/import


class VisualizationStyle(Enum):
    """3D visualization styles."""
    REALISTIC = "realistic"    # Real-world metaphor (planets, buildings)
    ABSTRACT = "abstract"      # Mathematical representation
    NETWORK = "network"        # Graph-like topology
    TOPOLOGICAL = "topological"  # Heat-map based


@dataclass
class Vector3:
    """3D coordinate."""
    x: float
    y: float
    z: float

    def __add__(self, other: 'Vector3') -> 'Vector3':
        """Add vectors."""
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: 'Vector3') -> 'Vector3':
        """Subtract vectors."""
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def distance_to(self, other: 'Vector3') -> float:
        """Calculate distance to another point."""
        dx = self.x - other.x
        dy = self.y - other.y
        dz = self.z - other.z
        return math.sqrt(dx*dx + dy*dy + dz*dz)

    def normalize(self) -> 'Vector3':
        """Normalize to unit vector."""
        dist = math.sqrt(self.x**2 + self.y**2 + self.z**2)
        if dist == 0:
            return Vector3(0, 0, 0)
        return Vector3(self.x/dist, self.y/dist, self.z/dist)

    def to_tuple(self) -> Tuple[float, float, float]:
        """Convert to tuple."""
        return (self.x, self.y, self.z)


@dataclass
class Color:
    """RGBA color."""
    r: int  # 0-255
    g: int
    b: int
    a: float = 1.0  # 0-1 alpha

    def to_hex(self) -> str:
        """Convert to hex color."""
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}"

    def to_rgba(self) -> str:
        """Convert to rgba string."""
        return f"rgba({self.r},{self.g},{self.b},{self.a})"


@dataclass
class Entity3D:
    """3D entity in code universe."""
    id: str
    name: str
    entity_type: EntityType
    position: Vector3
    size: float  # Radius/scale
    color: Color
    code_lines: int = 0
    complexity: float = 0.0  # 0-1
    parent_id: Optional[str] = None
    children_ids: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)

    def get_bounds(self) -> Dict[str, float]:
        """Get entity bounding box."""
        return {
            'min_x': self.position.x - self.size,
            'max_x': self.position.x + self.size,
            'min_y': self.position.y - self.size,
            'max_y': self.position.y + self.size,
            'min_z': self.position.z - self.size,
            'max_z': self.position.z + self.size,
        }

    def distance_to(self, other: 'Entity3D') -> float:
        """Distance to another entity."""
        return self.position.distance_to(other.position)


@dataclass
class GravitationalLink:
    """Dependency link with gravitational properties."""
    source_id: str
    target_id: str
    strength: float  # 0-1, coupling strength
    type: str  # 'import', 'inherit', 'call', 'reference'
    bidirectional: bool = False
    weight: float = 1.0  # For force calculations


@dataclass
class Viewport:
    """Camera/viewing position in 3D space."""
    position: Vector3
    look_at: Vector3
    up_vector: Vector3
    fov: float  # Field of view in degrees
    zoom: float = 1.0

    def get_direction(self) -> Vector3:
        """Get viewing direction."""
        return (self.look_at - self.position).normalize()


@dataclass
class CodeChange3D:
    """A code change represented in 3D."""
    entity_id: str
    timestamp: datetime
    change_type: str  # 'add', 'modify', 'delete', 'refactor'
    position_before: Optional[Vector3]
    position_after: Optional[Vector3]
    lines_changed: int
    complexity_delta: float
    description: str


@dataclass
class AIAgentState:
    """State of an AI agent navigating the 3D codebase."""
    agent_id: str
    position: Vector3
    velocity: Vector3 = field(default_factory=lambda: Vector3(0, 0, 0))
    target_position: Optional[Vector3] = None
    current_entity_id: Optional[str] = None
    visited_entities: List[str] = field(default_factory=list)
    interaction_history: List[Dict[str, Any]] = field(default_factory=list)
    knowledge_graph: Dict[str, Any] = field(default_factory=dict)


class SpatialIndexing:
    """Octree-like spatial indexing for 3D entities."""

    def __init__(self, bounds_min: Vector3, bounds_max: Vector3, max_depth: int = 8):
        self.bounds_min = bounds_min
        self.bounds_max = bounds_max
        self.max_depth = max_depth
        self.entities: Dict[str, Entity3D] = {}
        self.octree: Dict[str, List[str]] = {}  # cell_key -> entity_ids

    def add_entity(self, entity: Entity3D):
        """Add entity to spatial index."""
        self.entities[entity.id] = entity
        cell_key = self._get_cell_key(entity.position)
        if cell_key not in self.octree:
            self.octree[cell_key] = []
        self.octree[cell_key].append(entity.id)

    def query_sphere(self, center: Vector3, radius: float) -> List[Entity3D]:
        """Query all entities within sphere."""
        result = []
        for entity in self.entities.values():
            if entity.position.distance_to(center) <= radius:
                result.append(entity)
        return result

    def query_aabb(self, min_pos: Vector3, max_pos: Vector3) -> List[Entity3D]:
        """Query all entities in axis-aligned bounding box."""
        result = []
        for entity in self.entities.values():
            bounds = entity.get_bounds()
            if (bounds['max_x'] >= min_pos.x and bounds['min_x'] <= max_pos.x and
                bounds['max_y'] >= min_pos.y and bounds['min_y'] <= max_pos.y and
                bounds['max_z'] >= min_pos.z and bounds['min_z'] <= max_pos.z):
                result.append(entity)
        return result

    def _get_cell_key(self, pos: Vector3) -> str:
        """Get octree cell key for position."""
        cell_x = int((pos.x - self.bounds_min.x) / (self.bounds_max.x - self.bounds_min.x) * 4)
        cell_y = int((pos.y - self.bounds_min.y) / (self.bounds_max.y - self.bounds_min.y) * 4)
        cell_z = int((pos.z - self.bounds_min.z) / (self.bounds_max.z - self.bounds_min.z) * 4)
        return f"{cell_x}_{cell_y}_{cell_z}"


class CodeTo3DMapper:
    """Maps code structure to 3D spatial representation."""

    def __init__(self, style: VisualizationStyle = VisualizationStyle.REALISTIC):
        self.style = style
        self.entities: Dict[str, Entity3D] = {}
        self.links: List[GravitationalLink] = []
        self.entity_counter = 0

    def map_project(self, project_structure: Dict[str, Any]) -> Dict[str, Entity3D]:
        """Map entire project structure to 3D."""
        self.entities = {}
        self.links = []

        # Create root universe entity
        universe = self._create_entity(
            "universe_0",
            project_structure.get('name', 'Project'),
            EntityType.UNIVERSE,
            Vector3(0, 0, 0),
            100.0,
            Color(50, 50, 100)
        )
        self.entities["universe_0"] = universe

        # Map folders (planets) around universe
        folders = project_structure.get('folders', {})
        planet_positions = self._distribute_around_point(Vector3(0, 0, 0), len(folders), 150)

        for idx, (folder_name, folder_content) in enumerate(folders.items()):
            planet = self._map_folder_to_planet(
                folder_name,
                folder_content,
                planet_positions[idx],
                "universe_0"
            )
            self.entities[planet.id] = planet

        return self.entities

    def _map_folder_to_planet(self, folder_name: str, content: Dict[str, Any],
                             position: Vector3, parent_id: str) -> Entity3D:
        """Map folder to planet."""
        planet_id = f"planet_{self.entity_counter}"
        self.entity_counter += 1

        files_count = len(content.get('files', {}))
        planet_size = 20 + files_count * 2

        planet = self._create_entity(
            planet_id,
            folder_name,
            EntityType.PLANET,
            position,
            planet_size,
            Color(100, 150, 200),
            parent_id=parent_id
        )

        # Map files (continents) on planet surface
        files = content.get('files', {})
        continent_positions = self._distribute_on_sphere(position, len(files), planet_size)

        for idx, (file_name, file_content) in enumerate(files.items()):
            continent = self._map_file_to_continent(
                file_name,
                file_content,
                continent_positions[idx],
                planet_id
            )
            self.entities[continent.id] = continent

        return planet

    def _map_file_to_continent(self, file_name: str, content: Dict[str, Any],
                              position: Vector3, parent_id: str) -> Entity3D:
        """Map file to continent."""
        continent_id = f"continent_{self.entity_counter}"
        self.entity_counter += 1

        classes_count = len(content.get('classes', {}))
        continent_size = 8 + classes_count * 1.5

        continent = self._create_entity(
            continent_id,
            file_name,
            EntityType.CONTINENT,
            position,
            continent_size,
            Color(150, 200, 100),
            code_lines=content.get('lines', 0),
            parent_id=parent_id
        )

        # Map classes (buildings) on continent
        classes = content.get('classes', {})
        building_positions = self._distribute_on_sphere(position, len(classes), continent_size)

        for idx, (class_name, class_content) in enumerate(classes.items()):
            building = self._map_class_to_building(
                class_name,
                class_content,
                building_positions[idx],
                continent_id
            )
            self.entities[building.id] = building

        return continent

    def _map_class_to_building(self, class_name: str, content: Dict[str, Any],
                              position: Vector3, parent_id: str) -> Entity3D:
        """Map class to building."""
        building_id = f"building_{self.entity_counter}"
        self.entity_counter += 1

        methods_count = len(content.get('methods', {}))
        building_size = 3 + methods_count * 0.5

        building = self._create_entity(
            building_id,
            class_name,
            EntityType.BUILDING,
            position,
            building_size,
            Color(200, 150, 100),
            code_lines=content.get('lines', 0),
            complexity=content.get('complexity', 0.5),
            parent_id=parent_id
        )

        # Map methods (nodes) in building
        methods = content.get('methods', {})
        node_positions = self._distribute_in_radius(position, len(methods), building_size * 2)

        for idx, (method_name, method_content) in enumerate(methods.items()):
            node = self._map_method_to_node(
                method_name,
                method_content,
                node_positions[idx],
                building_id
            )
            self.entities[node.id] = node

        return building

    def _map_method_to_node(self, method_name: str, content: Dict[str, Any],
                           position: Vector3, parent_id: str) -> Entity3D:
        """Map method to node."""
        node_id = f"node_{self.entity_counter}"
        self.entity_counter += 1

        node = self._create_entity(
            node_id,
            method_name,
            EntityType.NODE,
            position,
            1.0,
            Color(255, 150, 150),
            code_lines=content.get('lines', 0),
            complexity=content.get('complexity', 0.3),
            parent_id=parent_id
        )

        return node

    def add_dependency_link(self, source_id: str, target_id: str,
                           dep_type: str, strength: float = 1.0):
        """Add gravitational dependency link."""
        link = GravitationalLink(
            source_id=source_id,
            target_id=target_id,
            strength=strength,
            type=dep_type,
            weight=strength
        )
        self.links.append(link)

    def _create_entity(self, entity_id: str, name: str, entity_type: EntityType,
                      position: Vector3, size: float, color: Color, **kwargs) -> Entity3D:
        """Create entity with defaults."""
        return Entity3D(
            id=entity_id,
            name=name,
            entity_type=entity_type,
            position=position,
            size=size,
            color=color,
            **kwargs
        )

    def _distribute_around_point(self, center: Vector3, count: int, radius: float) -> List[Vector3]:
        """Distribute points around center (hemisphere)."""
        positions = []
        for i in range(count):
            angle = (i / count) * 2 * math.pi
            x = center.x + radius * math.cos(angle)
            y = center.y + 50 + i * 5  # Slight vertical spread
            z = center.z + radius * math.sin(angle)
            positions.append(Vector3(x, y, z))
        return positions

    def _distribute_on_sphere(self, center: Vector3, count: int, radius: float) -> List[Vector3]:
        """Distribute points on sphere surface (golden ratio)."""
        positions = []
        golden_angle = math.pi * (3 - math.sqrt(5))

        for i in range(count):
            y = center.y + radius * (1 - (i / (count - 1) if count > 1 else 0.5) * 2)
            rad = math.sqrt(radius**2 - (y - center.y)**2)

            theta = golden_angle * i
            x = center.x + rad * math.cos(theta)
            z = center.z + rad * math.sin(theta)
            positions.append(Vector3(x, y, z))

        return positions

    def _distribute_in_radius(self, center: Vector3, count: int, max_radius: float) -> List[Vector3]:
        """Distribute points within radius."""
        positions = []
        for i in range(count):
            angle = (i / count) * 2 * math.pi
            r = max_radius * math.sqrt(i / count)  # Uniform distribution
            x = center.x + r * math.cos(angle)
            z = center.z + r * math.sin(angle)
            y = center.y + (i - count/2) * 0.5
            positions.append(Vector3(x, y, z))
        return positions


class GravitationalPhysics:
    """Physics engine for gravitational interactions between entities."""

    def __init__(self, entities: Dict[str, Entity3D], links: List[GravitationalLink]):
        self.entities = entities
        self.links = links
        self.forces: Dict[str, Vector3] = {eid: Vector3(0, 0, 0) for eid in entities.keys()}

    def calculate_forces(self):
        """Calculate gravitational forces on all entities."""
        self.forces = {eid: Vector3(0, 0, 0) for eid in self.entities.keys()}

        # Gravitational attraction along dependency links
        for link in self.links:
            if link.source_id not in self.entities or link.target_id not in self.entities:
                continue

            source = self.entities[link.source_id]
            target = self.entities[link.target_id]

            direction = (target.position - source.position).normalize()
            distance = source.position.distance_to(target.position)
            distance = max(distance, 1.0)  # Avoid division by zero

            # Gravitational force: F = G * m1 * m2 / r^2
            # Here: m = complexity * code_lines
            m1 = max(source.complexity, 0.1) * max(source.code_lines, 1)
            m2 = max(target.complexity, 0.1) * max(target.code_lines, 1)

            # Scale by link strength
            force_magnitude = (link.strength * m1 * m2) / (distance ** 2 + 1)

            force = direction * force_magnitude

            # Apply to both entities (if bidirectional)
            self.forces[source.id] = self.forces[source.id] + force
            if link.bidirectional:
                neg_force = direction * (-force_magnitude)
                self.forces[target.id] = self.forces[target.id] + neg_force

    def get_force(self, entity_id: str) -> Vector3:
        """Get calculated force on entity."""
        return self.forces.get(entity_id, Vector3(0, 0, 0))


class AIAgentNavigator:
    """Navigation system for AI agents in 3D codebase."""

    def __init__(self, entities: Dict[str, Entity3D], spatial_index: SpatialIndexing):
        self.entities = entities
        self.spatial_index = spatial_index
        self.agents: Dict[str, AIAgentState] = {}

    def create_agent(self, agent_id: str, start_position: Vector3) -> AIAgentState:
        """Create new AI agent."""
        agent = AIAgentState(
            agent_id=agent_id,
            position=start_position,
            visited_entities=[]
        )
        self.agents[agent_id] = agent
        return agent

    def navigate_to_entity(self, agent_id: str, target_entity_id: str) -> List[Vector3]:
        """Generate path to target entity."""
        if agent_id not in self.agents or target_entity_id not in self.entities:
            return []

        agent = self.agents[agent_id]
        target_entity = self.entities[target_entity_id]
        target_position = target_entity.position

        # Simple A* like pathfinding (simplified)
        path = [agent.position]
        current_pos = agent.position

        while current_pos.distance_to(target_position) > 5:
            # Move toward target
            direction = (target_position - current_pos).normalize()
            next_pos = current_pos + direction * 10
            path.append(next_pos)
            current_pos = next_pos

        path.append(target_position)
        agent.target_position = target_position
        return path

    def move_agent(self, agent_id: str, velocity: Vector3, dt: float = 0.016):
        """Move agent by velocity."""
        if agent_id not in self.agents:
            return

        agent = self.agents[agent_id]
        agent.position = agent.position + velocity * dt
        agent.velocity = velocity

        # Check for entity interaction
        nearby = self.spatial_index.query_sphere(agent.position, 5)
        if nearby:
            closest = min(nearby, key=lambda e: agent.position.distance_to(e.position))
            agent.current_entity_id = closest.id
            if closest.id not in agent.visited_entities:
                agent.visited_entities.append(closest.id)

    def get_agent_view(self, agent_id: str) -> Dict[str, Any]:
        """Get what agent can see from current position."""
        if agent_id not in self.agents:
            return {}

        agent = self.agents[agent_id]
        visible = self.spatial_index.query_sphere(agent.position, 50)

        return {
            'position': agent.position.to_tuple(),
            'visible_entities': [e.id for e in visible],
            'current_entity': agent.current_entity_id,
            'visited_count': len(agent.visited_entities),
        }


class InteractionSystem:
    """System for interacting with entities in 3D space."""

    def __init__(self, entities: Dict[str, Entity3D]):
        self.entities = entities
        self.modification_history: List[CodeChange3D] = []

    def select_entity(self, entity_id: str) -> Optional[Entity3D]:
        """Select entity for interaction."""
        return self.entities.get(entity_id)

    def move_entity(self, entity_id: str, new_position: Vector3) -> bool:
        """Move entity to new position."""
        if entity_id not in self.entities:
            return False

        entity = self.entities[entity_id]
        old_position = entity.position

        entity.position = new_position

        change = CodeChange3D(
            entity_id=entity_id,
            timestamp=datetime.now(),
            change_type='refactor',
            position_before=old_position,
            position_after=new_position,
            lines_changed=0,
            complexity_delta=0.0,
            description=f"Moved {entity.name} in 3D space"
        )
        self.modification_history.append(change)
        return True

    def modify_entity_properties(self, entity_id: str, properties: Dict[str, Any]) -> bool:
        """Modify entity properties."""
        if entity_id not in self.entities:
            return False

        entity = self.entities[entity_id]

        for key, value in properties.items():
            if hasattr(entity, key):
                setattr(entity, key, value)

        change = CodeChange3D(
            entity_id=entity_id,
            timestamp=datetime.now(),
            change_type='modify',
            position_before=entity.position,
            position_after=entity.position,
            lines_changed=0,
            complexity_delta=0.0,
            description=f"Modified properties of {entity.name}"
        )
        self.modification_history.append(change)
        return True

    def reorganize_hierarchy(self, entity_id: str, new_parent_id: str) -> bool:
        """Reorganize hierarchy (move to different parent)."""
        if entity_id not in self.entities or new_parent_id not in self.entities:
            return False

        entity = self.entities[entity_id]
        old_parent = entity.parent_id

        # Remove from old parent
        if old_parent and old_parent in self.entities:
            parent_entity = self.entities[old_parent]
            if entity_id in parent_entity.children_ids:
                parent_entity.children_ids.remove(entity_id)

        # Add to new parent
        entity.parent_id = new_parent_id
        new_parent = self.entities[new_parent_id]
        new_parent.children_ids.append(entity_id)

        change = CodeChange3D(
            entity_id=entity_id,
            timestamp=datetime.now(),
            change_type='refactor',
            position_before=None,
            position_after=None,
            lines_changed=0,
            complexity_delta=0.0,
            description=f"Reorganized {entity.name} hierarchy"
        )
        self.modification_history.append(change)
        return True

    def get_modification_history(self) -> List[CodeChange3D]:
        """Get history of modifications."""
        return self.modification_history


class Web6IDE:
    """Main Web-6 3D IDE orchestrator."""

    def __init__(self, visualization_style: VisualizationStyle = VisualizationStyle.REALISTIC):
        self.style = visualization_style
        self.mapper = CodeTo3DMapper(visualization_style)
        self.entities: Dict[str, Entity3D] = {}
        self.links: List[GravitationalLink] = []
        self.spatial_index = SpatialIndexing(
            Vector3(-500, -500, -500),
            Vector3(500, 500, 500)
        )
        self.physics = None
        self.navigator = None
        self.interaction = None
        self.viewport = None
        self.analysis_cache = {}

    def initialize_from_project(self, project_structure: Dict[str, Any]):
        """Initialize 3D universe from project structure."""
        # Map code to 3D
        self.entities = self.mapper.map_project(project_structure)

        # Setup spatial indexing
        for entity in self.entities.values():
            self.spatial_index.add_entity(entity)

        # Get links from mapper
        self.links = self.mapper.links

        # Initialize physics
        self.physics = GravitationalPhysics(self.entities, self.links)

        # Initialize navigation
        self.navigator = AIAgentNavigator(self.entities, self.spatial_index)

        # Initialize interaction
        self.interaction = InteractionSystem(self.entities)

        # Setup default viewport
        root_entity = self.entities.get('universe_0')
        if root_entity:
            self.viewport = Viewport(
                position=Vector3(0, 100, 200),
                look_at=Vector3(0, 0, 0),
                up_vector=Vector3(0, 1, 0),
                fov=45.0
            )

    def add_dependency(self, source_id: str, target_id: str, dep_type: str):
        """Add dependency link."""
        self.mapper.add_dependency_link(source_id, target_id, dep_type)
        self.links = self.mapper.links

        if self.physics:
            self.physics.links = self.links

    def simulate_physics(self, iterations: int = 10, dt: float = 0.016):
        """Simulate gravitational physics."""
        if not self.physics:
            return

        for _ in range(iterations):
            self.physics.calculate_forces()

            # Apply forces to entities (simplified integration)
            for entity_id, force in self.physics.forces.items():
                if entity_id in self.entities:
                    entity = self.entities[entity_id]
                    # Only move non-root entities
                    if entity.entity_type != EntityType.UNIVERSE:
                        accel = force * 0.01  # Scale down acceleration
                        entity.position = entity.position + accel * (dt ** 2)

    def create_ai_agent(self, agent_id: str) -> AIAgentState:
        """Create new AI agent."""
        if not self.navigator:
            return None

        start_pos = Vector3(0, 100, 0)  # Start near center
        return self.navigator.create_agent(agent_id, start_pos)

    def get_3d_scene_json(self) -> Dict[str, Any]:
        """Export 3D scene as JSON (Three.js format)."""
        scene_data = {
            'metadata': {
                'version': '1.0',
                'style': self.style.value,
                'timestamp': datetime.now().isoformat(),
            },
            'objects': [],
            'lights': [
                {
                    'type': 'DirectionalLight',
                    'position': [200, 300, 200],
                    'color': 0xffffff,
                    'intensity': 1.0
                },
                {
                    'type': 'AmbientLight',
                    'color': 0x404040,
                    'intensity': 0.5
                }
            ],
            'links': []
        }

        # Add entities as Three.js objects
        for entity in self.entities.values():
            obj = {
                'id': entity.id,
                'name': entity.name,
                'type': entity.entity_type.value,
                'geometry': 'sphere',  # Simplified
                'position': entity.position.to_tuple(),
                'scale': [entity.size, entity.size, entity.size],
                'material': {
                    'color': entity.color.to_hex(),
                    'opacity': entity.color.a,
                    'emissive': entity.color.to_hex() if entity.entity_type == EntityType.NODE else '#000000'
                },
                'metadata': {
                    'code_lines': entity.code_lines,
                    'complexity': entity.complexity,
                    'children': entity.children_ids,
                }
            }
            scene_data['objects'].append(obj)

        # Add dependency links
        for link in self.links:
            link_data = {
                'source': link.source_id,
                'target': link.target_id,
                'type': link.type,
                'strength': link.strength,
                'geometry': 'line'
            }
            scene_data['links'].append(link_data)

        return scene_data

    def generate_3d_code_review(self, reviewer_id: str) -> Dict[str, Any]:
        """Generate 3D code review report."""
        review = {
            'reviewer_id': reviewer_id,
            'timestamp': datetime.now().isoformat(),
            'entities_analyzed': len(self.entities),
            'observations': [],
            'recommendations': []
        }

        # Analyze entities
        for entity in self.entities.values():
            if entity.entity_type == EntityType.NODE:
                # Check code complexity
                if entity.complexity > 0.8:
                    review['observations'].append({
                        'entity_id': entity.id,
                        'issue': 'High complexity',
                        'severity': 'warning',
                        'suggestion': f"Refactor {entity.name} - complexity score {entity.complexity:.2f}"
                    })

                # Check code length
                if entity.code_lines > 100:
                    review['observations'].append({
                        'entity_id': entity.id,
                        'issue': 'Long function',
                        'severity': 'info',
                        'suggestion': f"Consider breaking down {entity.name} ({entity.code_lines} lines)"
                    })

        # Analyze dependencies
        for link in self.links:
            if link.strength > 0.8:
                review['observations'].append({
                    'link': f"{link.source_id} -> {link.target_id}",
                    'issue': 'Strong coupling',
                    'severity': 'warning',
                    'suggestion': 'Consider decoupling these modules'
                })

        return review

    def get_3d_change_history(self) -> List[Dict[str, Any]]:
        """Get 3D visualization of change history."""
        if not self.interaction:
            return []

        history = []
        for change in self.interaction.modification_history:
            change_data = {
                'timestamp': change.timestamp.isoformat(),
                'entity_id': change.entity_id,
                'type': change.change_type,
                'description': change.description,
                'position_before': change.position_before.to_tuple() if change.position_before else None,
                'position_after': change.position_after.to_tuple() if change.position_after else None,
            }
            history.append(change_data)

        return history
