"""
Phase 2.4: Distributed/Mesh IDE (Web-6 Architecture)

A distributed IDE where code and logic flow across multiple execution points:
  - Local machine (developer workstation)
  - Edge nodes (REChain® network)
  - Cloud infrastructure (scaling)
  - Quantum backend (optimization)
  - Local models (AI agents)

Instead of code living in one place, the IDE itself becomes a network.
Each file has guardian agents that manage, protect, and optimize it.

The IDE is not software running on your machine. The IDE is a distributed system.
Your machine is just a node in that network.

Revolutionary concept: Code lives everywhere. IDE is the network connecting them.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Set, Tuple, Optional, Any, Callable
from abc import ABC, abstractmethod
import hashlib
import json
from datetime import datetime
import uuid


# =============================================================================
# CORE ENUMS
# =============================================================================

class NodeType(Enum):
    """Types of nodes in the mesh network."""
    LOCAL = "local"              # Developer's machine
    EDGE = "edge"                # Edge computing node (REChain)
    CLOUD = "cloud"              # Cloud infrastructure
    QUANTUM = "quantum"          # Quantum backend
    MODEL = "model"              # Local AI model host


class ExecutionContext(Enum):
    """Where should code execute."""
    LOCAL = "local"              # On developer's machine
    EDGE = "edge"                # On edge node
    CLOUD = "cloud"              # In cloud
    QUANTUM = "quantum"          # Quantum optimization
    HYBRID = "hybrid"            # Distributed across nodes


class AgentRole(Enum):
    """Guardian agent roles."""
    GUARDIAN = "guardian"        # File protector/optimizer
    MONITOR = "monitor"          # Watches for changes/issues
    OPTIMIZER = "optimizer"      # Performance improvement
    SECURITY = "security"        # Security analysis
    SYNC = "sync"                # Keeps replicas in sync
    COORDINATOR = "coordinator"  # Orchestrates execution


class SyncState(Enum):
    """State of replica synchronization."""
    SYNCED = "synced"           # All replicas consistent
    PENDING = "pending"         # Changes waiting to sync
    CONFLICT = "conflict"       # Versions differ
    DIVERGED = "diverged"       # Critical divergence


# =============================================================================
# CORE DATA CLASSES
# =============================================================================

@dataclass
class CodeReplica:
    """A copy of code on a specific node."""
    node_id: str                # Which node has this replica
    node_type: NodeType         # Type of node
    content: str                # Code content
    hash: str                   # Content hash
    timestamp: datetime         # When was it last updated
    version: int                # Version number
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Calculate hash if not provided."""
        if not self.hash:
            self.hash = hashlib.sha256(self.content.encode()).hexdigest()[:16]


@dataclass
class GuardianAgent:
    """Agent that manages and protects a file."""
    agent_id: str               # Unique ID
    file_id: str                # File being managed
    role: AgentRole             # Agent's primary role
    node_id: str                # Which node hosts this agent
    status: str = "active"      # active, sleeping, error
    metrics: Dict[str, Any] = field(default_factory=dict)  # Performance/security metrics
    state: Dict[str, Any] = field(default_factory=dict)    # Agent internal state
    watchers: List[str] = field(default_factory=list)      # Files being watched
    last_action: Optional[datetime] = None
    
    def is_active(self) -> bool:
        """Check if agent is active."""
        return self.status == "active"


@dataclass
class FileMetadata:
    """Metadata about a file in mesh."""
    file_id: str                # Unique ID
    path: str                   # File path
    replicas: Dict[str, CodeReplica] = field(default_factory=dict)  # node_id -> replica
    sync_state: SyncState = SyncState.SYNCED
    guardian_id: Optional[str] = None  # Primary guardian agent
    secondary_guardians: List[str] = field(default_factory=list)
    access_log: List[Dict[str, Any]] = field(default_factory=list)
    
    def get_primary_replica(self) -> Optional[CodeReplica]:
        """Get most up-to-date replica."""
        if not self.replicas:
            return None
        return max(self.replicas.values(), key=lambda r: r.timestamp)
    
    def replicas_consistent(self) -> bool:
        """Check if all replicas have same content."""
        if len(self.replicas) <= 1:
            return True
        hashes = {r.hash for r in self.replicas.values()}
        return len(hashes) == 1


@dataclass
class MeshNode:
    """A node in the mesh network."""
    node_id: str                # Unique ID
    node_type: NodeType         # Type of node
    location: str               # Geographic/logical location
    status: str = "online"      # online, offline, degraded
    hosted_files: Set[str] = field(default_factory=set)  # File IDs
    agents: Dict[str, GuardianAgent] = field(default_factory=dict)
    capabilities: List[str] = field(default_factory=list)  # What this node can do
    load: float = 0.0           # Current load (0-1)
    latency_ms: int = 0         # Network latency to coordinator
    
    def is_available(self) -> bool:
        """Check if node can accept work."""
        return self.status == "online" and self.load < 0.9


@dataclass
class ExecutionPlan:
    """How to execute code across mesh."""
    plan_id: str
    file_id: str
    steps: List[Dict[str, Any]] = field(default_factory=list)  # Execution steps
    target_context: ExecutionContext = ExecutionContext.HYBRID
    primary_node: Optional[str] = None
    backup_nodes: List[str] = field(default_factory=list)
    estimated_time_ms: int = 0
    confidence: float = 0.0  # 0-1 probability of success


@dataclass
class SyncEvent:
    """A synchronization event between replicas."""
    event_id: str
    file_id: str
    source_node: str
    target_nodes: List[str]
    timestamp: datetime
    new_hash: str
    old_hash: Optional[str]
    success: bool = False
    latency_ms: int = 0


# =============================================================================
# ABSTRACT BASE CLASSES
# =============================================================================

class MeshNode_(ABC):
    """Base class for mesh nodes."""
    
    @abstractmethod
    def execute(self, code: str, context: ExecutionContext) -> Any:
        """Execute code on this node."""
        pass
    
    @abstractmethod
    def store_replica(self, file_id: str, content: str) -> bool:
        """Store code replica."""
        pass
    
    @abstractmethod
    def sync_file(self, file_id: str, content: str) -> bool:
        """Sync file to this node."""
        pass


class GuardianAgent_(ABC):
    """Base class for guardian agents."""
    
    @abstractmethod
    def monitor(self) -> Dict[str, Any]:
        """Monitor file and return metrics."""
        pass
    
    @abstractmethod
    def protect(self) -> bool:
        """Protect file from issues."""
        pass
    
    @abstractmethod
    def optimize(self) -> bool:
        """Optimize file."""
        pass


# =============================================================================
# MESH NETWORK LAYER
# =============================================================================

class MeshNetworkLayer:
    """Manages the mesh network topology and communication."""
    
    def __init__(self):
        """Initialize mesh network."""
        self.nodes: Dict[str, MeshNode] = {}
        self.node_graph: Dict[str, Set[str]] = {}  # Adjacency list
        self.network_latencies: Dict[Tuple[str, str], int] = {}  # (from, to) -> ms
        self.bandwidth: Dict[Tuple[str, str], int] = {}  # (from, to) -> MB/s
        self.routing_table: Dict[str, List[str]] = {}  # file_id -> [best path]
    
    def add_node(self, node: MeshNode) -> bool:
        """Add node to mesh."""
        if node.node_id in self.nodes:
            return False
        
        self.nodes[node.node_id] = node
        self.node_graph[node.node_id] = set()
        return True
    
    def connect_nodes(self, node_a: str, node_b: str, latency_ms: int, 
                      bandwidth_mbps: int = 100) -> bool:
        """Create bidirectional connection."""
        if node_a not in self.nodes or node_b not in self.nodes:
            return False
        
        self.node_graph[node_a].add(node_b)
        self.node_graph[node_b].add(node_a)
        
        self.network_latencies[(node_a, node_b)] = latency_ms
        self.network_latencies[(node_b, node_a)] = latency_ms
        
        self.bandwidth[(node_a, node_b)] = bandwidth_mbps
        self.bandwidth[(node_b, node_a)] = bandwidth_mbps
        
        return True
    
    def find_best_path(self, source: str, target: str) -> List[str]:
        """Find lowest-latency path between nodes (Dijkstra)."""
        if source not in self.nodes or target not in self.nodes:
            return []
        
        if source == target:
            return [source]
        
        # Dijkstra's algorithm
        distances = {node: float('inf') for node in self.nodes}
        distances[source] = 0
        previous = {node: None for node in self.nodes}
        unvisited = set(self.nodes.keys())
        
        while unvisited:
            current = min(unvisited, key=lambda n: distances[n])
            
            if distances[current] == float('inf'):
                break
            
            if current == target:
                break
            
            for neighbor in self.node_graph.get(current, []):
                if neighbor in unvisited:
                    latency = self.network_latencies.get((current, neighbor), 0)
                    new_distance = distances[current] + latency
                    
                    if new_distance < distances[neighbor]:
                        distances[neighbor] = new_distance
                        previous[neighbor] = current
            
            unvisited.remove(current)
        
        # Reconstruct path
        path = []
        current = target
        while current is not None:
            path.append(current)
            current = previous[current]
        
        return list(reversed(path))
    
    def get_network_health(self) -> Dict[str, Any]:
        """Get overall network health."""
        online_nodes = sum(1 for n in self.nodes.values() if n.is_available())
        total_nodes = len(self.nodes)
        
        avg_latency = 0
        if self.network_latencies:
            avg_latency = sum(self.network_latencies.values()) // len(self.network_latencies)
        
        avg_load = 0
        if self.nodes:
            avg_load = sum(n.load for n in self.nodes.values()) / len(self.nodes)
        
        return {
            'online_nodes': online_nodes,
            'total_nodes': total_nodes,
            'availability': online_nodes / max(1, total_nodes),
            'avg_latency_ms': avg_latency,
            'avg_load': avg_load,
            'topology_edges': len(self.network_latencies)
        }


# =============================================================================
# CODE REPLICATION MANAGER
# =============================================================================

class CodeReplicationManager:
    """Manages distributed code replicas across mesh."""
    
    def __init__(self, network: MeshNetworkLayer):
        """Initialize replication manager."""
        self.network = network
        self.files: Dict[str, FileMetadata] = {}
        self.sync_events: List[SyncEvent] = []
        self.replica_factor = 3  # How many copies to keep
    
    def register_file(self, file_id: str, path: str, initial_content: str,
                      primary_node: str) -> bool:
        """Register file in mesh."""
        if file_id in self.files:
            return False
        
        metadata = FileMetadata(
            file_id=file_id,
            path=path,
            replicas={
                primary_node: CodeReplica(
                    node_id=primary_node,
                    node_type=self.network.nodes[primary_node].node_type,
                    content=initial_content,
                    hash="",
                    timestamp=datetime.now(),
                    version=1
                )
            }
        )
        
        self.files[file_id] = metadata
        return True
    
    def replicate_file(self, file_id: str, target_nodes: List[str]) -> bool:
        """Replicate file to additional nodes."""
        if file_id not in self.files:
            return False
        
        metadata = self.files[file_id]
        primary = metadata.get_primary_replica()
        
        if not primary:
            return False
        
        for node_id in target_nodes:
            if node_id in self.network.nodes and node_id not in metadata.replicas:
                replica = CodeReplica(
                    node_id=node_id,
                    node_type=self.network.nodes[node_id].node_type,
                    content=primary.content,
                    hash=primary.hash,
                    timestamp=datetime.now(),
                    version=primary.version
                )
                metadata.replicas[node_id] = replica
        
        return True
    
    def sync_file(self, file_id: str, new_content: str, source_node: str) -> bool:
        """Sync updated file across replicas."""
        if file_id not in self.files:
            return False
        
        metadata = self.files[file_id]
        new_hash = hashlib.sha256(new_content.encode()).hexdigest()[:16]
        
        # Update all replicas
        target_nodes = []
        for node_id, replica in metadata.replicas.items():
            if node_id != source_node:
                target_nodes.append(node_id)
                replica.content = new_content
                replica.hash = new_hash
                replica.timestamp = datetime.now()
                replica.version += 1
        
        # Record sync event
        event = SyncEvent(
            event_id=str(uuid.uuid4()),
            file_id=file_id,
            source_node=source_node,
            target_nodes=target_nodes,
            timestamp=datetime.now(),
            new_hash=new_hash,
            old_hash=metadata.get_primary_replica().hash if metadata.get_primary_replica() else None,
            success=True
        )
        self.sync_events.append(event)
        
        metadata.sync_state = SyncState.SYNCED if metadata.replicas_consistent() else SyncState.PENDING
        return True
    
    def resolve_conflict(self, file_id: str, winning_replica_node: str) -> bool:
        """Resolve conflicting replicas."""
        if file_id not in self.files:
            return False
        
        metadata = self.files[file_id]
        
        if winning_replica_node not in metadata.replicas:
            return False
        
        winning = metadata.replicas[winning_replica_node]
        
        # Copy winning version to all other replicas
        for node_id, replica in metadata.replicas.items():
            if node_id != winning_replica_node:
                replica.content = winning.content
                replica.hash = winning.hash
                replica.version = winning.version + 1
                replica.timestamp = datetime.now()
        
        metadata.sync_state = SyncState.SYNCED
        return True


# =============================================================================
# GUARDIAN AGENT SYSTEM
# =============================================================================

class GuardianAgentSystem:
    """Manages guardian agents protecting files."""
    
    def __init__(self, replication_manager: CodeReplicationManager):
        """Initialize guardian system."""
        self.replication = replication_manager
        self.agents: Dict[str, GuardianAgent] = {}
        self.file_guardians: Dict[str, str] = {}  # file_id -> primary guardian_id
    
    def create_guardian(self, file_id: str, node_id: str, 
                        role: AgentRole = AgentRole.GUARDIAN) -> GuardianAgent:
        """Create guardian agent for file."""
        agent_id = f"guardian_{file_id}_{uuid.uuid4().hex[:8]}"
        
        agent = GuardianAgent(
            agent_id=agent_id,
            file_id=file_id,
            role=role,
            node_id=node_id,
            status="active"
        )
        
        self.agents[agent_id] = agent
        
        if file_id not in self.file_guardians:
            self.file_guardians[file_id] = agent_id
        
        return agent
    
    def add_secondary_guardian(self, file_id: str, agent_id: str) -> bool:
        """Add secondary guardian for redundancy."""
        if file_id not in self.replication.files:
            return False
        
        if agent_id not in self.agents:
            return False
        
        metadata = self.replication.files[file_id]
        if agent_id not in metadata.secondary_guardians:
            metadata.secondary_guardians.append(agent_id)
        
        return True
    
    def monitor_file(self, file_id: str) -> Dict[str, Any]:
        """Get monitoring data for file from its guardian."""
        if file_id not in self.file_guardians:
            return {}
        
        guardian_id = self.file_guardians[file_id]
        guardian = self.agents[guardian_id]
        
        metadata = self.replication.files[file_id]
        primary = metadata.get_primary_replica()
        
        return {
            'file_id': file_id,
            'guardian_id': guardian_id,
            'guardian_status': guardian.status,
            'sync_state': metadata.sync_state.value,
            'replica_count': len(metadata.replicas),
            'replicas_consistent': metadata.replicas_consistent(),
            'version': primary.version if primary else 0,
            'last_sync': primary.timestamp if primary else None,
            'access_count': len(metadata.access_log)
        }


# =============================================================================
# EXECUTION ROUTER
# =============================================================================

class ExecutionRouter:
    """Routes code execution to appropriate nodes."""
    
    def __init__(self, network: MeshNetworkLayer, replication: CodeReplicationManager):
        """Initialize router."""
        self.network = network
        self.replication = replication
        self.execution_history: List[Dict[str, Any]] = []
    
    def plan_execution(self, file_id: str, context: ExecutionContext,
                       developer_node: str) -> Optional[ExecutionPlan]:
        """Create execution plan for file."""
        if file_id not in self.replication.files:
            return None
        
        plan = ExecutionPlan(
            plan_id=str(uuid.uuid4()),
            file_id=file_id,
            target_context=context
        )
        
        metadata = self.replication.files[file_id]
        
        # Determine primary execution node based on context
        if context == ExecutionContext.LOCAL:
            plan.primary_node = developer_node
        
        elif context == ExecutionContext.EDGE:
            # Find nearest edge node
            edge_nodes = [n for n in self.network.nodes.values() 
                         if n.node_type == NodeType.EDGE and n.is_available()]
            if edge_nodes:
                plan.primary_node = min(edge_nodes, key=lambda n: n.latency_ms).node_id
        
        elif context == ExecutionContext.CLOUD:
            # Find best cloud node
            cloud_nodes = [n for n in self.network.nodes.values() 
                          if n.node_type == NodeType.CLOUD and n.is_available()]
            if cloud_nodes:
                plan.primary_node = min(cloud_nodes, key=lambda n: n.load).node_id
        
        elif context == ExecutionContext.QUANTUM:
            # Route to quantum backend
            quantum_nodes = [n for n in self.network.nodes.values() 
                           if n.node_type == NodeType.QUANTUM]
            if quantum_nodes:
                plan.primary_node = quantum_nodes[0].node_id
        
        elif context == ExecutionContext.HYBRID:
            # Use developer's node as primary, others as backup
            plan.primary_node = developer_node
            backup_nodes = [n.node_id for n in self.network.nodes.values() 
                           if n.node_id != developer_node and n.is_available()]
            plan.backup_nodes = backup_nodes[:2]  # Keep 2 backups
        
        # Add execution steps
        plan.steps = [
            {'step': 1, 'action': 'fetch_replica', 'node': plan.primary_node},
            {'step': 2, 'action': 'compile', 'node': plan.primary_node},
            {'step': 3, 'action': 'execute', 'node': plan.primary_node},
            {'step': 4, 'action': 'verify', 'node': plan.backup_nodes[0] if plan.backup_nodes else plan.primary_node},
            {'step': 5, 'action': 'sync_results', 'nodes': list(metadata.replicas.keys())}
        ]
        
        return plan
    
    def execute(self, plan: ExecutionPlan, code: str) -> Dict[str, Any]:
        """Execute plan."""
        result = {
            'plan_id': plan.plan_id,
            'file_id': plan.file_id,
            'status': 'executed',
            'steps_completed': len(plan.steps),
            'execution_time_ms': 0,
            'result': None
        }
        
        self.execution_history.append(result)
        return result


# =============================================================================
# MESH IDE COORDINATOR
# =============================================================================

class MeshIDECoordinator:
    """Main orchestrator for the distributed mesh IDE."""
    
    def __init__(self):
        """Initialize mesh IDE."""
        self.network = MeshNetworkLayer()
        self.replication = CodeReplicationManager(self.network)
        self.guardians = GuardianAgentSystem(self.replication)
        self.router = ExecutionRouter(self.network, self.replication)
        self.coordinator_id = str(uuid.uuid4())
    
    def initialize_mesh(self, node_configs: List[Dict[str, Any]]) -> bool:
        """Initialize mesh with nodes."""
        for config in node_configs:
            node = MeshNode(
                node_id=config.get('node_id', str(uuid.uuid4())),
                node_type=NodeType[config['node_type']],
                location=config.get('location', 'unknown'),
                capabilities=config.get('capabilities', [])
            )
            self.network.add_node(node)
        
        # Connect nodes (simple star topology)
        nodes = list(self.network.nodes.keys())
        for i, node_a in enumerate(nodes[1:], 1):
            latency = 50 if self.network.nodes[node_a].node_type == NodeType.LOCAL else 100
            self.network.connect_nodes(nodes[0], node_a, latency)
        
        return True
    
    def add_file(self, path: str, content: str, primary_node: str) -> Optional[str]:
        """Add file to mesh."""
        file_id = f"file_{hashlib.md5(path.encode()).hexdigest()[:8]}"
        
        self.replication.register_file(file_id, path, content, primary_node)
        
        # Assign guardian agent
        self.guardians.create_guardian(file_id, primary_node)
        
        # Replicate to other nodes
        replica_nodes = [n.node_id for n in self.network.nodes.values() 
                        if n.node_id != primary_node and n.is_available()][:2]
        self.replication.replicate_file(file_id, replica_nodes)
        
        # Create secondary guardians
        for node_id in replica_nodes:
            agent = self.guardians.create_guardian(
                file_id, node_id, AgentRole.MONITOR
            )
            self.guardians.add_secondary_guardian(file_id, agent.agent_id)
        
        return file_id
    
    def sync_file(self, file_id: str, new_content: str, source_node: str) -> bool:
        """Sync file changes across mesh."""
        return self.replication.sync_file(file_id, new_content, source_node)
    
    def execute_code(self, file_id: str, context: ExecutionContext,
                    developer_node: str) -> Dict[str, Any]:
        """Execute code in distributed context."""
        plan = self.router.plan_execution(file_id, context, developer_node)
        
        if not plan:
            return {'status': 'error', 'message': 'Could not create execution plan'}
        
        metadata = self.replication.files[file_id]
        primary = metadata.get_primary_replica()
        
        if not primary:
            return {'status': 'error', 'message': 'No code replica found'}
        
        return self.router.execute(plan, primary.content)
    
    def get_mesh_status(self) -> Dict[str, Any]:
        """Get overall mesh status."""
        return {
            'coordinator_id': self.coordinator_id,
            'network_health': self.network.get_network_health(),
            'total_files': len(self.replication.files),
            'total_agents': len(self.guardians.agents),
            'sync_events': len(self.replication.sync_events),
            'execution_history': len(self.router.execution_history),
            'nodes': {
                node_id: {
                    'type': node.node_type.value,
                    'status': node.status,
                    'load': node.load,
                    'hosted_files': len(node.hosted_files),
                    'agents': len(node.agents)
                }
                for node_id, node in self.network.nodes.items()
            }
        }
    
    def monitor_file(self, file_id: str) -> Dict[str, Any]:
        """Monitor file status."""
        return self.guardians.monitor_file(file_id)
    
    def get_replication_status(self, file_id: str) -> Dict[str, Any]:
        """Get replication status for file."""
        if file_id not in self.replication.files:
            return {}
        
        metadata = self.replication.files[file_id]
        
        return {
            'file_id': file_id,
            'sync_state': metadata.sync_state.value,
            'replicas': {
                node_id: {
                    'node_type': replica.node_type.value,
                    'version': replica.version,
                    'hash': replica.hash,
                    'timestamp': replica.timestamp.isoformat()
                }
                for node_id, replica in metadata.replicas.items()
            },
            'consistent': metadata.replicas_consistent()
        }


# =============================================================================
# MESH FILE MANAGER
# =============================================================================

class MeshFileManager:
    """High-level file management interface for mesh."""
    
    def __init__(self, coordinator: MeshIDECoordinator):
        """Initialize file manager."""
        self.coordinator = coordinator
        self.local_cache: Dict[str, str] = {}  # Local copy of files
    
    def open_file(self, path: str, developer_node: str) -> Optional[str]:
        """Open file from mesh."""
        file_id = f"file_{hashlib.md5(path.encode()).hexdigest()[:8]}"
        
        if file_id not in self.coordinator.replication.files:
            return None
        
        metadata = self.coordinator.replication.files[file_id]
        primary = metadata.get_primary_replica()
        
        if primary:
            self.local_cache[file_id] = primary.content
            return primary.content
        
        return None
    
    def save_file(self, file_id: str, content: str, developer_node: str) -> bool:
        """Save file to mesh."""
        if file_id not in self.coordinator.replication.files:
            return False
        
        self.local_cache[file_id] = content
        return self.coordinator.sync_file(file_id, content, developer_node)
    
    def execute_file(self, file_id: str, context: ExecutionContext,
                    developer_node: str) -> Dict[str, Any]:
        """Execute file in mesh."""
        return self.coordinator.execute_code(file_id, context, developer_node)


# =============================================================================
# STATS & TELEMETRY
# =============================================================================

class MeshTelemetry:
    """Telemetry collection for mesh IDE."""
    
    def __init__(self, coordinator: MeshIDECoordinator):
        """Initialize telemetry."""
        self.coordinator = coordinator
        self.events: List[Dict[str, Any]] = []
    
    def record_event(self, event_type: str, details: Dict[str, Any]) -> None:
        """Record telemetry event."""
        self.events.append({
            'timestamp': datetime.now(),
            'event_type': event_type,
            'details': details
        })
    
    def get_execution_stats(self) -> Dict[str, Any]:
        """Get execution statistics."""
        executions = self.coordinator.router.execution_history
        
        if not executions:
            return {}
        
        total_time = sum(e.get('execution_time_ms', 0) for e in executions)
        
        return {
            'total_executions': len(executions),
            'total_time_ms': total_time,
            'avg_time_ms': total_time / len(executions),
            'success_count': sum(1 for e in executions if e.get('status') == 'executed')
        }
    
    def get_sync_stats(self) -> Dict[str, Any]:
        """Get synchronization statistics."""
        events = self.coordinator.replication.sync_events
        
        if not events:
            return {}
        
        total_latency = sum(e.latency_ms for e in events)
        
        return {
            'total_sync_events': len(events),
            'successful_syncs': sum(1 for e in events if e.success),
            'total_latency_ms': total_latency,
            'avg_latency_ms': total_latency / len(events) if events else 0
        }
