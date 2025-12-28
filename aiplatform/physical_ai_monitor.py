"""
Physical AI - Prometheus-Style Infrastructure Monitoring
Monitor and manage physical AI infrastructure with intelligent analytics
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import json

class MetricType(Enum):
    """Types of metrics to monitor"""
    CPU_USAGE = "cpu_usage"
    MEMORY_USAGE = "memory_usage"
    NETWORK_IO = "network_io"
    DISK_IO = "disk_io"
    TEMPERATURE = "temperature"
    POWER_CONSUMPTION = "power_consumption"
    QUANTUM_FIDELITY = "quantum_fidelity"
    ERROR_RATE = "error_rate"
    LATENCY = "latency"
    THROUGHPUT = "throughput"

class AlertLevel(Enum):
    """Alert severity levels"""
    INFO = 0
    WARNING = 1
    CRITICAL = 2
    FATAL = 3

@dataclass
class Metric:
    """Physical metric measurement"""
    name: str
    type: MetricType
    value: float
    unit: str
    timestamp: str
    device_id: str
    labels: Dict[str, str] = field(default_factory=dict)

@dataclass
class Alert:
    """System alert"""
    id: str
    level: AlertLevel
    title: str
    description: str
    metric_name: str
    threshold: float
    current_value: float
    timestamp: str
    resolved: bool = False

@dataclass
class HealthReport:
    """System health report"""
    timestamp: str
    overall_health: float  # 0-1
    component_health: Dict[str, float]
    critical_issues: List[str]
    recommendations: List[str]

class PhysicalAIMonitor:
    """
    Physical AI Infrastructure Monitor
    Prometheus-style monitoring for quantum and AI infrastructure
    
    Features:
    - Real-time metric collection
    - Physical constraint monitoring
    - Quantum hardware health tracking
    - Power and thermal management
    - Predictive failure detection
    - Infrastructure optimization recommendations
    - Multi-site federation monitoring
    """
    
    def __init__(self):
        self.metrics: Dict[str, List[Metric]] = {}
        self.alerts: Dict[str, Alert] = {}
        self.alert_rules: List[Dict[str, Any]] = self._init_alert_rules()
        self.historical_data: List[Dict] = []
        self.health_history: List[HealthReport] = []
        
    def _init_alert_rules(self) -> List[Dict[str, Any]]:
        """Initialize default alert rules"""
        return [
            {
                "metric": MetricType.CPU_USAGE,
                "warning_threshold": 70,
                "critical_threshold": 90,
                "duration_seconds": 60
            },
            {
                "metric": MetricType.MEMORY_USAGE,
                "warning_threshold": 80,
                "critical_threshold": 95,
                "duration_seconds": 30
            },
            {
                "metric": MetricType.TEMPERATURE,
                "warning_threshold": 70,
                "critical_threshold": 90,
                "duration_seconds": 10
            },
            {
                "metric": MetricType.QUANTUM_FIDELITY,
                "warning_threshold": 0.95,
                "critical_threshold": 0.90,
                "comparison": "less_than"
            },
            {
                "metric": MetricType.ERROR_RATE,
                "warning_threshold": 0.005,
                "critical_threshold": 0.01,
                "duration_seconds": 60
            }
        ]
    
    def record_metric(self, metric: Metric) -> str:
        """Record physical metric"""
        
        if metric.name not in self.metrics:
            self.metrics[metric.name] = []
        
        self.metrics[metric.name].append(metric)
        
        # Keep only last 1000 measurements per metric
        if len(self.metrics[metric.name]) > 1000:
            self.metrics[metric.name] = self.metrics[metric.name][-1000:]
        
        # Check alert rules
        self._check_alert_rules(metric)
        
        return metric.name
    
    def record_quantum_metrics(self, device_id: str, metrics: Dict[str, float]):
        """Record quantum hardware metrics"""
        
        timestamp = datetime.now().isoformat()
        
        for metric_name, value in metrics.items():
            if metric_name == "fidelity":
                metric = Metric(
                    name="quantum_fidelity",
                    type=MetricType.QUANTUM_FIDELITY,
                    value=value,
                    unit="percentage",
                    timestamp=timestamp,
                    device_id=device_id
                )
            elif metric_name == "error_rate":
                metric = Metric(
                    name="quantum_error_rate",
                    type=MetricType.ERROR_RATE,
                    value=value,
                    unit="errors_per_1000_operations",
                    timestamp=timestamp,
                    device_id=device_id
                )
            elif metric_name == "gate_time":
                metric = Metric(
                    name="gate_execution_time",
                    type=MetricType.LATENCY,
                    value=value,
                    unit="nanoseconds",
                    timestamp=timestamp,
                    device_id=device_id
                )
            else:
                continue
            
            self.record_metric(metric)
    
    def record_system_metrics(self, device_id: str, system_stats: Dict[str, float]):
        """Record system resource metrics"""
        
        timestamp = datetime.now().isoformat()
        
        metric_mapping = {
            "cpu_usage": MetricType.CPU_USAGE,
            "memory_usage": MetricType.MEMORY_USAGE,
            "temperature": MetricType.TEMPERATURE,
            "power_consumption": MetricType.POWER_CONSUMPTION,
            "network_io": MetricType.NETWORK_IO,
            "disk_io": MetricType.DISK_IO
        }
        
        units = {
            "cpu_usage": "%",
            "memory_usage": "%",
            "temperature": "celsius",
            "power_consumption": "watts",
            "network_io": "mbps",
            "disk_io": "iops"
        }
        
        for stat_name, stat_value in system_stats.items():
            if stat_name not in metric_mapping:
                continue
            
            metric = Metric(
                name=stat_name,
                type=metric_mapping[stat_name],
                value=stat_value,
                unit=units.get(stat_name, ""),
                timestamp=timestamp,
                device_id=device_id
            )
            
            self.record_metric(metric)
    
    def _check_alert_rules(self, metric: Metric):
        """Check metric against alert rules"""
        
        for rule in self.alert_rules:
            if rule["metric"] != metric.type:
                continue
            
            threshold = rule.get("critical_threshold", float('inf'))
            comparison = rule.get("comparison", "greater_than")
            
            should_alert = False
            if comparison == "greater_than":
                should_alert = metric.value > threshold
            elif comparison == "less_than":
                should_alert = metric.value < threshold
            
            if should_alert:
                self._create_alert(metric, rule, AlertLevel.CRITICAL)
    
    def _create_alert(self, metric: Metric, rule: Dict, level: AlertLevel):
        """Create alert for metric"""
        
        alert = Alert(
            id=f"alert_{len(self.alerts)}",
            level=level,
            title=f"{metric.type.value} threshold exceeded on {metric.device_id}",
            description=f"{metric.name} reached {metric.value}{metric.unit}",
            metric_name=metric.name,
            threshold=rule.get("critical_threshold", 0),
            current_value=metric.value,
            timestamp=datetime.now().isoformat()
        )
        
        self.alerts[alert.id] = alert
    
    def resolve_alert(self, alert_id: str):
        """Resolve alert"""
        if alert_id in self.alerts:
            self.alerts[alert_id].resolved = True
    
    def get_current_health(self) -> HealthReport:
        """Get current system health assessment"""
        
        # Calculate component health
        component_health = {}
        
        # CPU health
        cpu_metrics = self.metrics.get("cpu_usage", [])
        if cpu_metrics:
            latest_cpu = cpu_metrics[-1].value
            component_health["cpu"] = max(0, 1 - latest_cpu / 100)
        
        # Memory health
        mem_metrics = self.metrics.get("memory_usage", [])
        if mem_metrics:
            latest_mem = mem_metrics[-1].value
            component_health["memory"] = max(0, 1 - latest_mem / 100)
        
        # Temperature health
        temp_metrics = self.metrics.get("temperature", [])
        if temp_metrics:
            latest_temp = temp_metrics[-1].value
            component_health["temperature"] = max(0, 1 - latest_temp / 100)
        
        # Quantum fidelity
        quantum_metrics = self.metrics.get("quantum_fidelity", [])
        if quantum_metrics:
            latest_fidelity = quantum_metrics[-1].value / 100
            component_health["quantum"] = latest_fidelity
        
        # Overall health
        overall_health = sum(component_health.values()) / len(component_health) if component_health else 0.5
        
        # Get critical issues
        critical_issues = [
            f"{alert.title}" 
            for alert in self.alerts.values() 
            if alert.level == AlertLevel.CRITICAL and not alert.resolved
        ]
        
        # Get recommendations
        recommendations = self._generate_recommendations(component_health)
        
        report = HealthReport(
            timestamp=datetime.now().isoformat(),
            overall_health=overall_health,
            component_health=component_health,
            critical_issues=critical_issues,
            recommendations=recommendations
        )
        
        self.health_history.append(report)
        return report
    
    def _generate_recommendations(self, component_health: Dict[str, float]) -> List[str]:
        """Generate optimization recommendations"""
        
        recommendations = []
        
        if component_health.get("cpu", 1) < 0.3:
            recommendations.append("High CPU usage detected. Consider load balancing or optimization.")
        
        if component_health.get("memory", 1) < 0.2:
            recommendations.append("Critical memory usage. Increase RAM or optimize memory usage.")
        
        if component_health.get("temperature", 1) < 0.2:
            recommendations.append("High temperature detected. Check cooling system and ventilation.")
        
        if component_health.get("quantum", 0) < 0.95:
            recommendations.append("Quantum fidelity degradation. Recalibrate quantum hardware.")
        
        if not recommendations:
            recommendations.append("System operating normally. No immediate optimization needed.")
        
        return recommendations
    
    def predict_failure(self, device_id: str, metric_type: MetricType) -> Dict[str, Any]:
        """Predict potential hardware failure"""
        
        metric_name = metric_type.value
        if metric_name not in self.metrics:
            return {"prediction": None, "confidence": 0}
        
        metrics = self.metrics[metric_name]
        if len(metrics) < 10:
            return {"prediction": None, "confidence": 0, "reason": "Insufficient data"}
        
        # Simple trend analysis
        recent_metrics = metrics[-10:]
        values = [m.value for m in recent_metrics]
        
        # Calculate trend
        trend = (values[-1] - values[0]) / max(values[0], 0.01) if values[0] != 0 else 0
        
        failure_risk = "low"
        if trend > 0.1:  # >10% increase
            failure_risk = "high"
        elif trend > 0.05:
            failure_risk = "medium"
        
        return {
            "device_id": device_id,
            "metric": metric_type.value,
            "current_value": values[-1],
            "trend": f"{trend*100:.2f}%",
            "failure_risk": failure_risk,
            "prediction_confidence": 0.7,
            "recommended_action": f"Inspect {metric_type.value} if risk is high"
        }
    
    def get_performance_report(self, time_period_hours: int = 24) -> Dict[str, Any]:
        """Generate performance report"""
        
        cutoff_time = datetime.now() - timedelta(hours=time_period_hours)
        
        report = {
            "period_hours": time_period_hours,
            "start_time": cutoff_time.isoformat(),
            "metrics_collected": len(self.metrics),
            "alerts_generated": len([a for a in self.alerts.values() if not a.resolved]),
            "average_health": None,
            "metric_summaries": {}
        }
        
        # Calculate average health from history
        recent_reports = [h for h in self.health_history 
                         if datetime.fromisoformat(h.timestamp) > cutoff_time]
        if recent_reports:
            avg_health = sum(h.overall_health for h in recent_reports) / len(recent_reports)
            report["average_health"] = avg_health
        
        # Metric summaries
        for metric_name, metric_list in self.metrics.items():
            if metric_list:
                values = [m.value for m in metric_list]
                report["metric_summaries"][metric_name] = {
                    "current": values[-1],
                    "average": sum(values) / len(values),
                    "min": min(values),
                    "max": max(values),
                    "sample_count": len(values)
                }
        
        return report
    
    def export_metrics_prometheus(self) -> str:
        """Export metrics in Prometheus format"""
        
        lines = []
        
        for metric_name, metric_list in self.metrics.items():
            if metric_list:
                latest = metric_list[-1]
                # Prometheus format: metric_name{labels} value timestamp
                labels = " ".join([f'{k}="{v}"' for k, v in latest.labels.items()])
                labels += f' device_id="{latest.device_id}"'
                timestamp = int(datetime.fromisoformat(latest.timestamp).timestamp() * 1000)
                line = f"{metric_name}{{{labels}}} {latest.value} {timestamp}"
                lines.append(line)
        
        return "\n".join(lines)
    
    def get_infrastructure_summary(self) -> Dict[str, Any]:
        """Get infrastructure monitoring summary"""
        
        health = self.get_current_health()
        
        return {
            "timestamp": datetime.now().isoformat(),
            "overall_health": f"{health.overall_health*100:.1f}%",
            "components": health.component_health,
            "active_alerts": sum(1 for a in self.alerts.values() if not a.resolved),
            "resolved_alerts": sum(1 for a in self.alerts.values() if a.resolved),
            "total_metrics_tracked": len(self.metrics),
            "recent_health_trend": self._calculate_trend(),
            "critical_issues": health.critical_issues,
            "recommendations": health.recommendations
        }
    
    def _calculate_trend(self) -> str:
        """Calculate health trend"""
        if len(self.health_history) < 2:
            return "insufficient_data"
        
        recent = self.health_history[-1].overall_health
        previous = self.health_history[-2].overall_health
        
        if recent > previous:
            return "improving"
        elif recent < previous:
            return "degrading"
        else:
            return "stable"
