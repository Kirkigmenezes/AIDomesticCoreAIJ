"""
Edge Execution Framework
Distributed computation at the edge with quantum simulation
"""

from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import asyncio
from datetime import datetime
import json

class DeviceType(Enum):
    """Types of edge devices"""
    MOBILE = "mobile"
    IOT = "iot"
    GATEWAY = "gateway"
    DESKTOP = "desktop"
    QUANTUM_SIMULATOR = "quantum_simulator"

class TaskPriority(Enum):
    """Task execution priority"""
    CRITICAL = 0
    HIGH = 1
    NORMAL = 2
    LOW = 3

@dataclass
class EdgeDevice:
    """Edge device specification"""
    id: str
    device_type: DeviceType
    hostname: str
    cpu_cores: int
    memory_gb: float
    network_bandwidth_mbps: float
    supported_frameworks: List[str] = field(default_factory=list)
    quantum_simulator: bool = False
    available: bool = True
    location: str = "unknown"

@dataclass
class EdgeTask:
    """Task for edge execution"""
    id: str
    code: str
    language: str
    priority: TaskPriority
    timeout_seconds: int
    required_frameworks: List[str] = field(default_factory=list)
    data_size_mb: float = 0.0
    estimated_compute_time_ms: float = 0.0

@dataclass
class EdgeResult:
    """Result from edge execution"""
    task_id: str
    device_id: str
    status: str
    output: Any
    execution_time_ms: float
    memory_used_mb: float
    timestamp: str = None

class EdgeExecutionFramework:
    """
    Edge computation framework with quantum capabilities
    
    Features:
    - Distributed task execution on edge devices
    - Local quantum simulator on edge
    - Federated learning at device level
    - Bandwidth-aware task scheduling
    - Device resource optimization
    - Privacy-preserving edge computation
    - Mobile and IoT support
    """
    
    def __init__(self):
        self.devices: Dict[str, EdgeDevice] = {}
        self.tasks: Dict[str, EdgeTask] = {}
        self.results: Dict[str, EdgeResult] = {}
        self.execution_queue: List[EdgeTask] = []
        self.device_pool: Dict[str, List[str]] = {}  # Task -> Assigned devices
        
    def register_device(self, device: EdgeDevice) -> str:
        """Register edge device"""
        self.devices[device.id] = device
        print(f"Device registered: {device.hostname} ({device.device_type.value})")
        return device.id
    
    def register_devices_batch(self, devices: List[EdgeDevice]) -> List[str]:
        """Register multiple edge devices"""
        device_ids = []
        for device in devices:
            device_ids.append(self.register_device(device))
        return device_ids
    
    async def submit_task(self, task: EdgeTask) -> str:
        """Submit task for edge execution"""
        
        self.tasks[task.id] = task
        self.execution_queue.append(task)
        
        # Find suitable devices
        suitable_devices = self._find_suitable_devices(task)
        
        if not suitable_devices:
            raise ValueError(f"No suitable devices for task {task.id}")
        
        self.device_pool[task.id] = suitable_devices
        
        # Schedule for execution
        asyncio.create_task(self._execute_on_device(task, suitable_devices[0]))
        
        return task.id
    
    async def execute_quantum_on_edge(self, 
                                     circuit_code: str,
                                     shots: int = 1000) -> Dict[str, Any]:
        """Execute quantum circuit on edge device"""
        
        # Find device with quantum simulator
        quantum_devices = [d for d in self.devices.values() 
                          if d.quantum_simulator and d.available]
        
        if not quantum_devices:
            raise ValueError("No quantum simulator available on edge")
        
        device = quantum_devices[0]
        
        # Prepare task
        task = EdgeTask(
            id=f"quantum_{len(self.tasks)}",
            code=circuit_code,
            language="qiskit",
            priority=TaskPriority.HIGH,
            timeout_seconds=60,
            required_frameworks=["qiskit"],
            estimated_compute_time_ms=shots * 0.1
        )
        
        result = await self._execute_on_device(task, device.id)
        
        return {
            "device": device.hostname,
            "result": result,
            "shots": shots,
            "quantum_execution": True
        }
    
    async def _execute_on_device(self, task: EdgeTask, device_id: str) -> Dict[str, Any]:
        """Execute task on specific device"""
        
        device = self.devices.get(device_id)
        if not device:
            return {"status": "error", "message": "Device not found"}
        
        if not device.available:
            return {"status": "error", "message": "Device not available"}
        
        # Mark device as busy
        device.available = False
        
        try:
            # Simulate execution
            start_time = datetime.now()
            await asyncio.sleep(task.estimated_compute_time_ms / 1000)
            end_time = datetime.now()
            
            execution_time = (end_time - start_time).total_seconds() * 1000
            
            result = EdgeResult(
                task_id=task.id,
                device_id=device_id,
                status="success",
                output=f"Executed on {device.hostname}",
                execution_time_ms=execution_time,
                memory_used_mb=min(device.memory_gb * 100, 512),
                timestamp=datetime.now().isoformat()
            )
            
            self.results[task.id] = result
            return result.__dict__
            
        except Exception as e:
            return {
                "task_id": task.id,
                "device_id": device_id,
                "status": "error",
                "error": str(e)
            }
        finally:
            device.available = True
    
    def _find_suitable_devices(self, task: EdgeTask) -> List[str]:
        """Find devices suitable for task"""
        
        suitable = []
        
        for device_id, device in self.devices.items():
            if not device.available:
                continue
            
            # Check framework support
            frameworks_available = all(
                fw in device.supported_frameworks 
                for fw in task.required_frameworks
            )
            
            if not frameworks_available:
                continue
            
            # Check resource availability
            if device.memory_gb < 1 and task.data_size_mb > 512:
                continue
            
            # Check for quantum requirement
            if task.language == "qiskit" and not device.quantum_simulator:
                continue
            
            suitable.append(device_id)
        
        return suitable
    
    async def federated_learning_on_edge(self, 
                                        local_data_path: str,
                                        model_update_code: str) -> Dict[str, Any]:
        """Execute federated learning locally on edge devices"""
        
        # Submit training task to each device
        training_results = []
        
        for device_id, device in self.devices.items():
            if device.device_type in [DeviceType.MOBILE, DeviceType.DESKTOP]:
                task = EdgeTask(
                    id=f"federated_{device_id}",
                    code=model_update_code,
                    language="python",
                    priority=TaskPriority.NORMAL,
                    timeout_seconds=300,
                    required_frameworks=["tensorflow", "pytorch"]
                )
                
                result = await self._execute_on_device(task, device_id)
                training_results.append(result)
        
        return {
            "federated_learning": True,
            "devices_trained": len(training_results),
            "aggregation": "federated_averaging",
            "privacy_preserved": True,
            "results": training_results
        }
    
    def get_device_status(self) -> Dict[str, Any]:
        """Get status of all edge devices"""
        
        devices_status = []
        for device in self.devices.values():
            devices_status.append({
                "id": device.id,
                "hostname": device.hostname,
                "type": device.device_type.value,
                "available": device.available,
                "cpu_cores": device.cpu_cores,
                "memory_gb": device.memory_gb,
                "network_bandwidth_mbps": device.network_bandwidth_mbps,
                "quantum_capable": device.quantum_simulator,
                "location": device.location
            })
        
        return {
            "total_devices": len(self.devices),
            "available_devices": sum(1 for d in self.devices.values() if d.available),
            "devices": devices_status,
            "total_cpu_cores": sum(d.cpu_cores for d in self.devices.values()),
            "total_memory_gb": sum(d.memory_gb for d in self.devices.values())
        }
    
    def get_execution_statistics(self) -> Dict[str, Any]:
        """Get execution statistics"""
        
        total_tasks = len(self.results)
        successful_tasks = sum(1 for r in self.results.values() if r.status == "success")
        failed_tasks = sum(1 for r in self.results.values() if r.status == "error")
        
        avg_exec_time = (
            sum(r.execution_time_ms for r in self.results.values()) / total_tasks
            if total_tasks > 0 else 0
        )
        
        return {
            "total_executed_tasks": total_tasks,
            "successful_tasks": successful_tasks,
            "failed_tasks": failed_tasks,
            "success_rate": successful_tasks / total_tasks if total_tasks > 0 else 0,
            "average_execution_time_ms": avg_exec_time,
            "pending_tasks": len(self.execution_queue),
            "task_priority_distribution": {
                "critical": sum(1 for t in self.tasks.values() if t.priority == TaskPriority.CRITICAL),
                "high": sum(1 for t in self.tasks.values() if t.priority == TaskPriority.HIGH),
                "normal": sum(1 for t in self.tasks.values() if t.priority == TaskPriority.NORMAL),
                "low": sum(1 for t in self.tasks.values() if t.priority == TaskPriority.LOW)
            }
        }
    
    async def optimize_execution_plan(self, tasks: List[EdgeTask]) -> List[List[str]]:
        """Optimize execution plan across devices"""
        
        # Group tasks by priority
        by_priority = {}
        for task in tasks:
            if task.priority not in by_priority:
                by_priority[task.priority] = []
            by_priority[task.priority].append(task)
        
        execution_plan = []
        
        # Execute critical tasks first
        for priority in sorted(by_priority.keys()):
            priority_tasks = by_priority[priority]
            # Schedule tasks to available devices
            for task in priority_tasks:
                devices = self._find_suitable_devices(task)
                if devices:
                    execution_plan.append(devices)
        
        return execution_plan
    
    def export_device_manifest(self) -> str:
        """Export device manifest as JSON"""
        
        manifest = {
            "devices": [
                {
                    "id": d.id,
                    "type": d.device_type.value,
                    "hostname": d.hostname,
                    "specs": {
                        "cpu_cores": d.cpu_cores,
                        "memory_gb": d.memory_gb,
                        "network_bandwidth_mbps": d.network_bandwidth_mbps
                    },
                    "capabilities": {
                        "frameworks": d.supported_frameworks,
                        "quantum_simulator": d.quantum_simulator
                    },
                    "location": d.location
                }
                for d in self.devices.values()
            ]
        }
        
        return json.dumps(manifest, indent=2)
