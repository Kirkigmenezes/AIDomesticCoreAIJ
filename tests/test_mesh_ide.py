"""
Comprehensive Test Suite for Phase 2.4: Distributed Mesh IDE

Tests cover:
  - Mesh network topology and routing
  - Code replication and synchronization
  - Guardian agent system
  - Execution planning and routing
  - End-to-end mesh workflows
"""

import unittest
from datetime import datetime
from aiplatform.mesh_ide import (
    MeshIDECoordinator, MeshNetworkLayer, CodeReplicationManager,
    GuardianAgentSystem, ExecutionRouter, MeshNode, MeshFileManager,
    MeshTelemetry, CodeReplica, FileMetadata, GuardianAgent,
    NodeType, ExecutionContext, AgentRole, SyncState
)


class TestMeshNetworkLayer(unittest.TestCase):
    """Test mesh network topology and routing."""

    def setUp(self):
        """Set up test network."""
        self.network = MeshNetworkLayer()
        
        # Create nodes
        self.local_node = MeshNode(
            node_id="local_1",
            node_type=NodeType.LOCAL,
            location="developer_machine",
            capabilities=["compile", "debug", "test"]
        )
        
        self.edge_node = MeshNode(
            node_id="edge_1",
            node_type=NodeType.EDGE,
            location="rechain_network",
            capabilities=["compile", "test", "optimize"]
        )
        
        self.cloud_node = MeshNode(
            node_id="cloud_1",
            node_type=NodeType.CLOUD,
            location="aws_region",
            capabilities=["compile", "test", "scale", "monitor"]
        )
        
        # Add to network
        self.network.add_node(self.local_node)
        self.network.add_node(self.edge_node)
        self.network.add_node(self.cloud_node)

    def test_add_node(self):
        """Test adding nodes to network."""
        self.assertEqual(len(self.network.nodes), 3)
        self.assertIn("local_1", self.network.nodes)
        self.assertIn("edge_1", self.network.nodes)

    def test_connect_nodes(self):
        """Test connecting nodes."""
        success = self.network.connect_nodes("local_1", "edge_1", 50, 100)
        self.assertTrue(success)
        
        self.assertIn("edge_1", self.network.node_graph["local_1"])
        self.assertIn("local_1", self.network.node_graph["edge_1"])

    def test_latency_recording(self):
        """Test network latency recording."""
        self.network.connect_nodes("local_1", "cloud_1", 150, 50)
        
        latency = self.network.network_latencies[("local_1", "cloud_1")]
        self.assertEqual(latency, 150)

    def test_pathfinding(self):
        """Test path finding between nodes."""
        # Create path: local -> edge -> cloud
        self.network.connect_nodes("local_1", "edge_1", 50)
        self.network.connect_nodes("edge_1", "cloud_1", 100)
        
        path = self.network.find_best_path("local_1", "cloud_1")
        
        self.assertEqual(len(path), 3)
        self.assertEqual(path[0], "local_1")
        self.assertEqual(path[-1], "cloud_1")

    def test_network_health(self):
        """Test network health metrics."""
        self.network.connect_nodes("local_1", "edge_1", 50)
        self.network.connect_nodes("edge_1", "cloud_1", 100)
        
        health = self.network.get_network_health()
        
        self.assertEqual(health['online_nodes'], 3)
        self.assertEqual(health['total_nodes'], 3)
        self.assertEqual(health['availability'], 1.0)


class TestCodeReplication(unittest.TestCase):
    """Test code replication across mesh."""

    def setUp(self):
        """Set up replication test."""
        self.network = MeshNetworkLayer()
        self.replication = CodeReplicationManager(self.network)
        
        # Create nodes
        for node_id in ["local_1", "edge_1", "cloud_1"]:
            node = MeshNode(
                node_id=node_id,
                node_type=NodeType.LOCAL if "local" in node_id else NodeType.EDGE if "edge" in node_id else NodeType.CLOUD,
                location=node_id
            )
            self.network.add_node(node)

    def test_register_file(self):
        """Test registering file in mesh."""
        file_id = "file_001"
        path = "src/main.py"
        content = "print('hello')"
        
        success = self.replication.register_file(file_id, path, content, "local_1")
        
        self.assertTrue(success)
        self.assertIn(file_id, self.replication.files)
        
        metadata = self.replication.files[file_id]
        self.assertEqual(metadata.path, path)
        self.assertIn("local_1", metadata.replicas)

    def test_replicate_file(self):
        """Test replicating file to multiple nodes."""
        file_id = "file_001"
        content = "x = 1"
        
        self.replication.register_file(file_id, "test.py", content, "local_1")
        success = self.replication.replicate_file(file_id, ["edge_1", "cloud_1"])
        
        self.assertTrue(success)
        
        metadata = self.replication.files[file_id]
        self.assertEqual(len(metadata.replicas), 3)
        self.assertIn("local_1", metadata.replicas)
        self.assertIn("edge_1", metadata.replicas)
        self.assertIn("cloud_1", metadata.replicas)

    def test_sync_file(self):
        """Test synchronizing file changes."""
        file_id = "file_001"
        initial_content = "x = 1"
        new_content = "x = 2"
        
        self.replication.register_file(file_id, "test.py", initial_content, "local_1")
        self.replication.replicate_file(file_id, ["edge_1"])
        
        success = self.replication.sync_file(file_id, new_content, "local_1")
        
        self.assertTrue(success)
        
        # Check all replicas updated
        for replica in self.replication.files[file_id].replicas.values():
            self.assertEqual(replica.content, new_content)

    def test_replica_consistency(self):
        """Test checking replica consistency."""
        file_id = "file_001"
        content = "code"
        
        self.replication.register_file(file_id, "test.py", content, "local_1")
        self.replication.replicate_file(file_id, ["edge_1"])
        
        metadata = self.replication.files[file_id]
        self.assertTrue(metadata.replicas_consistent())

    def test_conflict_resolution(self):
        """Test resolving conflicting replicas."""
        file_id = "file_001"
        
        self.replication.register_file(file_id, "test.py", "v1", "local_1")
        self.replication.replicate_file(file_id, ["edge_1", "cloud_1"])
        
        # Simulate divergence
        metadata = self.replication.files[file_id]
        metadata.replicas["edge_1"].content = "v2"
        metadata.replicas["cloud_1"].content = "v3"
        metadata.sync_state = SyncState.CONFLICT
        
        # Resolve to local version
        success = self.replication.resolve_conflict(file_id, "local_1")
        
        self.assertTrue(success)
        self.assertTrue(metadata.replicas_consistent())
        self.assertEqual(metadata.sync_state, SyncState.SYNCED)


class TestGuardianAgentSystem(unittest.TestCase):
    """Test guardian agent management."""

    def setUp(self):
        """Set up guardian test."""
        self.network = MeshNetworkLayer()
        self.replication = CodeReplicationManager(self.network)
        self.guardians = GuardianAgentSystem(self.replication)
        
        # Create nodes
        for node_id in ["local_1", "edge_1"]:
            node = MeshNode(
                node_id=node_id,
                node_type=NodeType.LOCAL if "local" in node_id else NodeType.EDGE,
                location=node_id
            )
            self.network.add_node(node)

    def test_create_guardian(self):
        """Test creating guardian agent."""
        file_id = "file_001"
        
        agent = self.guardians.create_guardian(file_id, "local_1")
        
        self.assertIsNotNone(agent)
        self.assertEqual(agent.file_id, file_id)
        self.assertEqual(agent.node_id, "local_1")
        self.assertEqual(agent.role, AgentRole.GUARDIAN)
        self.assertTrue(agent.is_active())

    def test_primary_guardian(self):
        """Test primary guardian assignment."""
        file_id = "file_001"
        
        self.replication.register_file(file_id, "test.py", "code", "local_1")
        agent1 = self.guardians.create_guardian(file_id, "local_1")
        
        self.assertEqual(self.guardians.file_guardians[file_id], agent1.agent_id)

    def test_secondary_guardians(self):
        """Test secondary guardian assignment."""
        file_id = "file_001"
        
        self.replication.register_file(file_id, "test.py", "code", "local_1")
        agent1 = self.guardians.create_guardian(file_id, "local_1")
        agent2 = self.guardians.create_guardian(file_id, "edge_1", AgentRole.MONITOR)
        
        success = self.guardians.add_secondary_guardian(file_id, agent2.agent_id)
        
        self.assertTrue(success)
        
        metadata = self.replication.files[file_id]
        self.assertIn(agent2.agent_id, metadata.secondary_guardians)

    def test_monitor_file(self):
        """Test monitoring file status."""
        file_id = "file_001"
        
        self.replication.register_file(file_id, "test.py", "code", "local_1")
        self.guardians.create_guardian(file_id, "local_1")
        
        status = self.guardians.monitor_file(file_id)
        
        self.assertEqual(status['file_id'], file_id)
        self.assertEqual(status['sync_state'], 'synced')
        self.assertEqual(status['replica_count'], 1)


class TestExecutionRouter(unittest.TestCase):
    """Test execution planning and routing."""

    def setUp(self):
        """Set up execution test."""
        self.network = MeshNetworkLayer()
        self.replication = CodeReplicationManager(self.network)
        self.router = ExecutionRouter(self.network, self.replication)
        
        # Create nodes
        for node_type in [NodeType.LOCAL, NodeType.EDGE, NodeType.CLOUD]:
            node = MeshNode(
                node_id=f"{node_type.value}_1",
                node_type=node_type,
                location=f"{node_type.value}_location"
            )
            self.network.add_node(node)

    def test_local_execution_plan(self):
        """Test planning local execution."""
        file_id = "file_001"
        
        self.replication.register_file(file_id, "test.py", "x = 1", "local_1")
        
        plan = self.router.plan_execution(file_id, ExecutionContext.LOCAL, "local_1")
        
        self.assertIsNotNone(plan)
        self.assertEqual(plan.target_context, ExecutionContext.LOCAL)
        self.assertEqual(plan.primary_node, "local_1")

    def test_edge_execution_plan(self):
        """Test planning edge execution."""
        file_id = "file_001"
        
        self.replication.register_file(file_id, "test.py", "x = 1", "local_1")
        
        plan = self.router.plan_execution(file_id, ExecutionContext.EDGE, "local_1")
        
        self.assertIsNotNone(plan)
        self.assertEqual(plan.target_context, ExecutionContext.EDGE)
        self.assertIn("edge", plan.primary_node)

    def test_hybrid_execution_plan(self):
        """Test planning hybrid execution."""
        file_id = "file_001"
        
        self.replication.register_file(file_id, "test.py", "x = 1", "local_1")
        self.replication.replicate_file(file_id, ["edge_1", "cloud_1"])
        
        plan = self.router.plan_execution(file_id, ExecutionContext.HYBRID, "local_1")
        
        self.assertIsNotNone(plan)
        self.assertEqual(plan.primary_node, "local_1")
        self.assertGreater(len(plan.backup_nodes), 0)

    def test_execution(self):
        """Test executing plan."""
        file_id = "file_001"
        
        self.replication.register_file(file_id, "test.py", "x = 1", "local_1")
        
        plan = self.router.plan_execution(file_id, ExecutionContext.LOCAL, "local_1")
        result = self.router.execute(plan, "x = 1")
        
        self.assertEqual(result['status'], 'executed')
        self.assertEqual(result['plan_id'], plan.plan_id)


class TestMeshIDECoordinator(unittest.TestCase):
    """Test main mesh IDE coordinator."""

    def setUp(self):
        """Set up coordinator test."""
        self.coordinator = MeshIDECoordinator()
        
        # Initialize mesh
        nodes = [
            {'node_id': 'local_1', 'node_type': 'LOCAL', 'location': 'dev_machine'},
            {'node_id': 'edge_1', 'node_type': 'EDGE', 'location': 'rechain'},
            {'node_id': 'cloud_1', 'node_type': 'CLOUD', 'location': 'aws'},
            {'node_id': 'quantum_1', 'node_type': 'QUANTUM', 'location': 'quantum_lab'}
        ]
        
        self.coordinator.initialize_mesh(nodes)

    def test_initialization(self):
        """Test mesh initialization."""
        status = self.coordinator.get_mesh_status()
        
        self.assertEqual(status['total_files'], 0)
        self.assertEqual(status['total_agents'], 0)

    def test_add_file(self):
        """Test adding file to mesh."""
        file_id = self.coordinator.add_file("src/main.py", "print('hi')", "local_1")
        
        self.assertIsNotNone(file_id)
        self.assertIn(file_id, self.coordinator.replication.files)

    def test_file_replication(self):
        """Test file gets replicated."""
        file_id = self.coordinator.add_file("src/main.py", "code", "local_1")
        
        metadata = self.coordinator.replication.files[file_id]
        self.assertGreater(len(metadata.replicas), 1)

    def test_guardian_assignment(self):
        """Test guardian agent assigned to file."""
        file_id = self.coordinator.add_file("src/main.py", "code", "local_1")
        
        metadata = self.coordinator.replication.files[file_id]
        self.assertIsNotNone(metadata.guardian_id)
        self.assertGreater(len(metadata.secondary_guardians), 0)

    def test_sync_file(self):
        """Test syncing file changes."""
        file_id = self.coordinator.add_file("src/main.py", "v1", "local_1")
        
        success = self.coordinator.sync_file(file_id, "v2", "local_1")
        
        self.assertTrue(success)
        
        metadata = self.coordinator.replication.files[file_id]
        for replica in metadata.replicas.values():
            self.assertEqual(replica.content, "v2")

    def test_execute_code_local(self):
        """Test executing code locally."""
        file_id = self.coordinator.add_file("src/main.py", "x = 1", "local_1")
        
        result = self.coordinator.execute_code(file_id, ExecutionContext.LOCAL, "local_1")
        
        self.assertEqual(result['status'], 'executed')

    def test_execute_code_edge(self):
        """Test executing code on edge."""
        file_id = self.coordinator.add_file("src/main.py", "x = 1", "local_1")
        
        result = self.coordinator.execute_code(file_id, ExecutionContext.EDGE, "local_1")
        
        self.assertEqual(result['status'], 'executed')

    def test_execute_code_hybrid(self):
        """Test executing code in hybrid mode."""
        file_id = self.coordinator.add_file("src/main.py", "x = 1", "local_1")
        
        result = self.coordinator.execute_code(file_id, ExecutionContext.HYBRID, "local_1")
        
        self.assertEqual(result['status'], 'executed')

    def test_mesh_status(self):
        """Test getting mesh status."""
        self.coordinator.add_file("src/main.py", "code", "local_1")
        self.coordinator.add_file("src/util.py", "code", "local_1")
        
        status = self.coordinator.get_mesh_status()
        
        self.assertEqual(status['total_files'], 2)
        self.assertGreater(status['total_agents'], 0)

    def test_monitor_file(self):
        """Test monitoring file."""
        file_id = self.coordinator.add_file("src/main.py", "code", "local_1")
        
        monitor = self.coordinator.monitor_file(file_id)
        
        self.assertEqual(monitor['file_id'], file_id)
        self.assertEqual(monitor['sync_state'], 'synced')

    def test_replication_status(self):
        """Test replication status."""
        file_id = self.coordinator.add_file("src/main.py", "code", "local_1")
        
        status = self.coordinator.get_replication_status(file_id)
        
        self.assertEqual(status['file_id'], file_id)
        self.assertTrue(status['consistent'])


class TestMeshFileManager(unittest.TestCase):
    """Test high-level file management."""

    def setUp(self):
        """Set up file manager test."""
        self.coordinator = MeshIDECoordinator()
        self.coordinator.initialize_mesh([
            {'node_id': 'local_1', 'node_type': 'LOCAL'},
            {'node_id': 'edge_1', 'node_type': 'EDGE'}
        ])
        
        self.file_manager = MeshFileManager(self.coordinator)

    def test_save_and_open_file(self):
        """Test saving and opening file."""
        path = "src/main.py"
        content = "x = 1"
        
        file_id = self.coordinator.add_file(path, content, "local_1")
        
        retrieved = self.file_manager.open_file(path, "local_1")
        
        self.assertEqual(retrieved, content)

    def test_save_file(self):
        """Test saving file changes."""
        file_id = self.coordinator.add_file("src/main.py", "v1", "local_1")
        
        success = self.file_manager.save_file(file_id, "v2", "local_1")
        
        self.assertTrue(success)

    def test_execute_file(self):
        """Test executing file."""
        file_id = self.coordinator.add_file("src/main.py", "x = 1", "local_1")
        
        result = self.file_manager.execute_file(file_id, ExecutionContext.LOCAL, "local_1")
        
        self.assertEqual(result['status'], 'executed')


class TestMeshTelemetry(unittest.TestCase):
    """Test telemetry and monitoring."""

    def setUp(self):
        """Set up telemetry test."""
        self.coordinator = MeshIDECoordinator()
        self.coordinator.initialize_mesh([
            {'node_id': 'local_1', 'node_type': 'LOCAL'},
            {'node_id': 'edge_1', 'node_type': 'EDGE'}
        ])
        
        self.telemetry = MeshTelemetry(self.coordinator)

    def test_record_event(self):
        """Test recording telemetry event."""
        self.telemetry.record_event('test_event', {'key': 'value'})
        
        self.assertEqual(len(self.telemetry.events), 1)

    def test_execution_stats(self):
        """Test execution statistics."""
        file_id = self.coordinator.add_file("src/main.py", "x = 1", "local_1")
        self.coordinator.execute_code(file_id, ExecutionContext.LOCAL, "local_1")
        
        stats = self.telemetry.get_execution_stats()
        
        self.assertEqual(stats['total_executions'], 1)
        self.assertEqual(stats['success_count'], 1)


class TestEnd2EndMeshWorkflow(unittest.TestCase):
    """End-to-end mesh IDE workflow tests."""

    def test_complete_mesh_workflow(self):
        """Test complete mesh workflow."""
        # 1. Initialize mesh
        coordinator = MeshIDECoordinator()
        coordinator.initialize_mesh([
            {'node_id': 'dev_laptop', 'node_type': 'LOCAL', 'location': 'office'},
            {'node_id': 'edge_node1', 'node_type': 'EDGE', 'location': 'rechain_network'},
            {'node_id': 'cloud_us', 'node_type': 'CLOUD', 'location': 'aws_us'},
            {'node_id': 'quantum_backend', 'node_type': 'QUANTUM', 'location': 'quantum_lab'}
        ])
        
        # 2. Add file to mesh
        file_id = coordinator.add_file(
            "src/algorithm.py",
            "def optimize(x):\n    return x * 2",
            "dev_laptop"
        )
        
        self.assertIsNotNone(file_id)
        
        # 3. Verify replication
        metadata = coordinator.replication.files[file_id]
        self.assertGreater(len(metadata.replicas), 1)
        
        # 4. Execute locally
        result = coordinator.execute_code(file_id, ExecutionContext.LOCAL, "dev_laptop")
        self.assertEqual(result['status'], 'executed')
        
        # 5. Sync to edge
        coordinator.sync_file(file_id, "def optimize(x):\n    return x * 3", "dev_laptop")
        
        # 6. Execute on edge
        result = coordinator.execute_code(file_id, ExecutionContext.EDGE, "dev_laptop")
        self.assertEqual(result['status'], 'executed')
        
        # 7. Verify mesh status
        status = coordinator.get_mesh_status()
        self.assertEqual(status['total_files'], 1)
        self.assertGreater(status['total_agents'], 0)


if __name__ == '__main__':
    unittest.main()
