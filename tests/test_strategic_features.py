"""
Strategic AI Features Integration Tests
Comprehensive testing for Web-6, Privacy IDE, LLM-kernel, Edge, and Physical AI
"""

import pytest
import asyncio
from datetime import datetime

# Import modules to test
from aiplatform.web6_semantic_graph import Web6SemanticGraph, SemanticEntity, EntityType
from aiplatform.privacy_first_ide import PrivacyFirstIDE, PrivacyLevel, ExecutionMode
from aiplatform.llm_kernel_ide import LLMKernel, IDEKernelIntegration, SuggestionType
from aiplatform.edge_execution import EdgeExecutionFramework, EdgeDevice, DeviceType, EdgeTask, TaskPriority
from aiplatform.physical_ai_monitor import PhysicalAIMonitor, Metric, MetricType


class TestWeb6SemanticGraph:
    """Test Web-6 semantic graph functionality"""
    
    def test_entity_creation(self):
        graph = Web6SemanticGraph()
        entity = SemanticEntity(
            id="test_1",
            type=EntityType.CODE_FUNCTION,
            name="test_function",
            description="A test function"
        )
        entity_id = graph.add_entity(entity)
        assert entity_id == "test_1"
        assert entity_id in graph.entities
    
    def test_code_extraction(self):
        graph = Web6SemanticGraph()
        code = '''
def hello_world():
    print("Hello")

class MyClass:
    def method(self):
        pass

import numpy as np
'''
        entity_ids = graph.extract_from_code(code, "test.py")
        assert len(entity_ids) > 0
        assert len(graph.entities) >= 3  # At least function, class, dependency
    
    def test_semantic_search(self):
        graph = Web6SemanticGraph()
        entity = SemanticEntity(
            id="test_1",
            type=EntityType.CODE_FUNCTION,
            name="calculate_sum",
            description="Calculates sum of numbers"
        )
        graph.add_entity(entity)
        
        results = graph.search_semantic("calculate")
        assert len(results) == 1
        assert results[0].name == "calculate_sum"
    
    def test_3d_visualization(self):
        graph = Web6SemanticGraph()
        entity = SemanticEntity(
            id="test_1",
            type=EntityType.CODE_FUNCTION,
            name="test",
            description="Test"
        )
        graph.add_entity(entity)
        
        viz = graph.generate_3d_visualization()
        assert "nodes" in viz
        assert "edges" in viz
        assert len(viz["nodes"]) == 1
        assert viz["stats"]["node_count"] == 1
    
    def test_code_map_generation(self):
        graph = Web6SemanticGraph()
        code = "def func(): pass\nclass Cls: pass"
        graph.extract_from_code(code, "test.py")
        
        code_map = graph.generate_code_map()
        assert "files" in code_map
        assert "statistics" in code_map


class TestPrivacyFirstIDE:
    """Test privacy-first IDE functionality"""
    
    @pytest.mark.asyncio
    async def test_file_creation_unencrypted(self):
        ide = PrivacyFirstIDE("user_1")
        file_id = ide.create_file(
            "test.py",
            "print('hello')",
            "python",
            PrivacyLevel.INTERNAL
        )
        assert file_id in ide.files
        assert not ide.files[file_id].encrypted
    
    @pytest.mark.asyncio
    async def test_file_creation_encrypted(self):
        ide = PrivacyFirstIDE("user_1")
        file_id = ide.create_file(
            "secret.py",
            "secret_data = 'classified'",
            "python",
            PrivacyLevel.ENCRYPTED
        )
        assert ide.files[file_id].encrypted
    
    @pytest.mark.asyncio
    async def test_code_execution_local(self):
        ide = PrivacyFirstIDE("user_1")
        file_id = ide.create_file("test.py", "x = 1 + 1", "python")
        
        result = await ide.execute_code(file_id, ExecutionMode.LOCAL)
        assert result["status"] == "success"
        assert result["execution_mode"] == "local"
    
    @pytest.mark.asyncio
    async def test_code_execution_distributed(self):
        ide = PrivacyFirstIDE("user_1")
        file_id = ide.create_file("test.py", "x = 1\ny = 2\nz = x + y", "python")
        
        result = await ide.execute_code(file_id, ExecutionMode.DISTRIBUTED)
        assert result["status"] == "success"
        assert result["execution_mode"] == "distributed"
    
    @pytest.mark.asyncio
    async def test_zero_knowledge_proof(self):
        ide = PrivacyFirstIDE("user_1")
        file_id = ide.create_file("proof.py", "secret = 42", "python")
        
        zkp = ide.enable_zero_knowledge_proof(file_id)
        assert zkp["zkp_enabled"]
        assert zkp["proof_scheme"] == "zk-SNARK"


class TestLLMKernel:
    """Test LLM kernel IDE integration"""
    
    @pytest.mark.asyncio
    async def test_code_completion(self):
        kernel = LLMKernel()
        from aiplatform.llm_kernel_ide import LLMContext
        
        context = LLMContext(
            code_snippet="def hello(",
            language="python",
            surrounding_code="def hello("
        )
        
        completions = await kernel.complete_code(context)
        assert len(completions) > 0
        assert isinstance(completions[0], str)
    
    @pytest.mark.asyncio
    async def test_bug_detection(self):
        kernel = LLMKernel()
        from aiplatform.llm_kernel_ide import LLMContext
        
        context = LLMContext(
            code_snippet="if x = 5:",
            language="python",
            surrounding_code="if x = 5:"
        )
        
        bugs = await kernel.detect_bugs(context)
        assert len(bugs) > 0
    
    @pytest.mark.asyncio
    async def test_optimization_suggestions(self):
        kernel = LLMKernel()
        from aiplatform.llm_kernel_ide import LLMContext
        
        context = LLMContext(
            code_snippet="for i in range(10):\n    for j in range(10): pass",
            language="python",
            surrounding_code="nested loops"
        )
        
        suggestions = await kernel.suggest_optimizations(context)
        assert len(suggestions) > 0
        assert suggestions[0].type == SuggestionType.OPTIMIZATION
    
    @pytest.mark.asyncio
    async def test_test_generation(self):
        kernel = LLMKernel()
        from aiplatform.llm_kernel_ide import LLMContext
        
        context = LLMContext(
            code_snippet="def add(a, b): return a + b",
            language="python",
            surrounding_code=""
        )
        
        tests = await kernel.generate_tests(context)
        assert "def test_" in tests
        assert "assert" in tests


class TestEdgeExecution:
    """Test edge execution framework"""
    
    @pytest.mark.asyncio
    async def test_device_registration(self):
        framework = EdgeExecutionFramework()
        device = EdgeDevice(
            id="device_1",
            device_type=DeviceType.GATEWAY,
            hostname="edge_gateway_1",
            cpu_cores=4,
            memory_gb=8,
            network_bandwidth_mbps=1000
        )
        
        device_id = framework.register_device(device)
        assert device_id == "device_1"
        assert device_id in framework.devices
    
    @pytest.mark.asyncio
    async def test_task_submission(self):
        framework = EdgeExecutionFramework()
        device = EdgeDevice(
            id="device_1",
            device_type=DeviceType.DESKTOP,
            hostname="desktop_1",
            cpu_cores=8,
            memory_gb=16,
            network_bandwidth_mbps=1000,
            supported_frameworks=["python"]
        )
        framework.register_device(device)
        
        task = EdgeTask(
            id="task_1",
            code="print('hello')",
            language="python",
            priority=TaskPriority.NORMAL,
            timeout_seconds=10
        )
        
        task_id = await framework.submit_task(task)
        assert task_id == "task_1"
    
    @pytest.mark.asyncio
    async def test_device_status(self):
        framework = EdgeExecutionFramework()
        device = EdgeDevice(
            id="device_1",
            device_type=DeviceType.IOT,
            hostname="iot_1",
            cpu_cores=2,
            memory_gb=1,
            network_bandwidth_mbps=100
        )
        framework.register_device(device)
        
        status = framework.get_device_status()
        assert status["total_devices"] == 1
        assert status["available_devices"] == 1
    
    @pytest.mark.asyncio
    async def test_quantum_execution_on_edge(self):
        framework = EdgeExecutionFramework()
        device = EdgeDevice(
            id="quantum_1",
            device_type=DeviceType.QUANTUM_SIMULATOR,
            hostname="quantum_edge",
            cpu_cores=16,
            memory_gb=32,
            network_bandwidth_mbps=10000,
            quantum_simulator=True,
            supported_frameworks=["qiskit"]
        )
        framework.register_device(device)
        
        result = await framework.execute_quantum_on_edge("circuit_code", shots=1000)
        assert "device" in result
        assert result["quantum_execution"]


class TestPhysicalAIMonitor:
    """Test physical AI monitoring"""
    
    def test_metric_recording(self):
        monitor = PhysicalAIMonitor()
        metric = Metric(
            name="cpu_usage",
            type=MetricType.CPU_USAGE,
            value=45.5,
            unit="%",
            timestamp=datetime.now().isoformat(),
            device_id="server_1"
        )
        
        result = monitor.record_metric(metric)
        assert result == "cpu_usage"
        assert len(monitor.metrics["cpu_usage"]) == 1
    
    def test_quantum_metrics_recording(self):
        monitor = PhysicalAIMonitor()
        metrics = {
            "fidelity": 0.98,
            "error_rate": 0.002,
            "gate_time": 50.0
        }
        
        monitor.record_quantum_metrics("quantum_1", metrics)
        assert "quantum_fidelity" in monitor.metrics
        assert "quantum_error_rate" in monitor.metrics
    
    def test_system_metrics_recording(self):
        monitor = PhysicalAIMonitor()
        stats = {
            "cpu_usage": 60,
            "memory_usage": 75,
            "temperature": 65,
            "power_consumption": 500
        }
        
        monitor.record_system_metrics("server_1", stats)
        assert len(monitor.metrics) >= 4
    
    def test_alert_creation(self):
        monitor = PhysicalAIMonitor()
        metric = Metric(
            name="cpu_usage",
            type=MetricType.CPU_USAGE,
            value=95,  # Critical
            unit="%",
            timestamp=datetime.now().isoformat(),
            device_id="server_1"
        )
        
        initial_alerts = len(monitor.alerts)
        monitor.record_metric(metric)
        # Alert should be created for critical threshold
        assert len(monitor.alerts) >= initial_alerts
    
    def test_health_assessment(self):
        monitor = PhysicalAIMonitor()
        
        # Record some metrics
        for i in range(5):
            metric = Metric(
                name="cpu_usage",
                type=MetricType.CPU_USAGE,
                value=40 + i*5,
                unit="%",
                timestamp=datetime.now().isoformat(),
                device_id="server_1"
            )
            monitor.record_metric(metric)
        
        health = monitor.get_current_health()
        assert health.overall_health >= 0
        assert health.overall_health <= 1
        assert isinstance(health.recommendations, list)
    
    def test_failure_prediction(self):
        monitor = PhysicalAIMonitor()
        
        # Record increasing temperatures
        for i in range(15):
            metric = Metric(
                name="temperature",
                type=MetricType.TEMPERATURE,
                value=50 + i*2,  # Rising trend
                unit="celsius",
                timestamp=datetime.now().isoformat(),
                device_id="server_1"
            )
            monitor.record_metric(metric)
        
        prediction = monitor.predict_failure("server_1", MetricType.TEMPERATURE)
        assert "failure_risk" in prediction
    
    def test_prometheus_export(self):
        monitor = PhysicalAIMonitor()
        metric = Metric(
            name="cpu_usage",
            type=MetricType.CPU_USAGE,
            value=50,
            unit="%",
            timestamp=datetime.now().isoformat(),
            device_id="server_1",
            labels={"environment": "production"}
        )
        monitor.record_metric(metric)
        
        prometheus_format = monitor.export_metrics_prometheus()
        assert "cpu_usage" in prometheus_format
        assert "device_id" in prometheus_format


class TestIntegration:
    """Integration tests for all strategic features"""
    
    @pytest.mark.asyncio
    async def test_end_to_end_workflow(self):
        """Test complete workflow using all strategic modules"""
        
        # 1. Create semantic graph of code
        graph = Web6SemanticGraph()
        code = """
def process_data(data):
    return sum(data)

def analyze(input_list):
    result = process_data(input_list)
    return result / len(input_list)

import numpy as np
"""
        graph.extract_from_code(code, "analysis.py")
        assert len(graph.entities) > 0
        
        # 2. Create privacy-first IDE and execute code
        ide = PrivacyFirstIDE("analyst_1")
        file_id = ide.create_file("analysis.py", code, "python", PrivacyLevel.ENCRYPTED)
        result = await ide.execute_code(file_id)
        assert result["status"] == "success"
        
        # 3. Use LLM kernel for optimization
        kernel = LLMKernel()
        from aiplatform.llm_kernel_ide import LLMContext
        context = LLMContext(
            code_snippet="for i in range(n): for j in range(m): pass",
            language="python",
            surrounding_code=""
        )
        suggestions = await kernel.suggest_optimizations(context)
        assert len(suggestions) > 0
        
        # 4. Set up edge execution
        framework = EdgeExecutionFramework()
        device = EdgeDevice(
            id="edge_1",
            device_type=DeviceType.GATEWAY,
            hostname="gateway_1",
            cpu_cores=8,
            memory_gb=16,
            network_bandwidth_mbps=1000,
            supported_frameworks=["python"]
        )
        framework.register_device(device)
        
        # 5. Monitor with physical AI
        monitor = PhysicalAIMonitor()
        metric = Metric(
            name="cpu_usage",
            type=MetricType.CPU_USAGE,
            value=65,
            unit="%",
            timestamp=datetime.now().isoformat(),
            device_id="edge_1"
        )
        monitor.record_metric(metric)
        health = monitor.get_current_health()
        
        assert health.overall_health > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
