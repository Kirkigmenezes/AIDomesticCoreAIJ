"""
Cross-AI Developer Mesh
IDE-integrated multi-model orchestration with intelligent routing, consensus, and merging

Manages multiple AI models as a coordinated swarm:
- Gemini 3, Grok 4.1, GPT-5.1, Local REChain LLM
- Automatic model routing based on task type
- Multi-LLM merge (Git-like conflict resolution)
- Consensus mechanisms
- Diff generation and integration
"""

from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
import asyncio
import json
from datetime import datetime
from difflib import unified_diff
import hashlib


class ModelProvider(Enum):
    """Supported model providers"""
    GEMINI_3 = "gemini_3"
    GROK_4_1 = "grok_4_1"
    GPT_5_1 = "gpt_5_1"
    RECHAIN_LOCAL = "rechain_local"


class TaskType(Enum):
    """Types of development tasks"""
    CODE_GENERATION = "code_generation"
    BUG_FIX = "bug_fix"
    CODE_REVIEW = "code_review"
    OPTIMIZATION = "optimization"
    DOCUMENTATION = "documentation"
    TESTING = "testing"
    ARCHITECTURE = "architecture"
    DEBUGGING = "debugging"
    REFACTORING = "refactoring"


class MergeStrategy(Enum):
    """Strategies for merging model outputs"""
    CONSENSUS = "consensus"  # Majority wins
    WEIGHTED = "weighted"  # Based on model confidence
    PRIORITY = "priority"  # Based on provider priority
    BLENDED = "blended"  # Combine best parts
    VOTE_MAJORITY = "vote_majority"  # Exact match majority


@dataclass
class ModelConfig:
    """Configuration for each AI model"""
    provider: ModelProvider
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    model_name: str = ""
    max_tokens: int = 8000
    temperature: float = 0.7
    timeout_seconds: int = 60
    enabled: bool = True
    priority: int = 1  # For routing decisions
    
    # Specializations
    strengths: Set[TaskType] = field(default_factory=set)
    weaknesses: Set[TaskType] = field(default_factory=set)


@dataclass
class ModelResponse:
    """Response from a single model"""
    provider: ModelProvider
    content: str
    confidence: float  # 0-1, how confident in this response
    reasoning: str  # Why the model chose this approach
    tokens_used: int = 0
    latency_ms: float = 0.0
    error: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class MergeConflict:
    """Conflict in merged model responses"""
    location: str  # Line number or code section
    provider1: ModelProvider
    response1: str
    provider2: ModelProvider
    response2: str
    confidence_diff: float  # Difference in confidence


@dataclass
class MergedResponse:
    """Result of merging multiple model responses"""
    merged_content: str
    consensus_score: float  # 0-1, how much agreement
    conflicts: List[MergeConflict] = field(default_factory=list)
    used_providers: List[ModelProvider] = field(default_factory=list)
    merge_strategy: MergeStrategy = MergeStrategy.CONSENSUS
    reasoning: str = ""
    diffs: List[str] = field(default_factory=list)  # Unified diffs from each model


class ModelRouter:
    """
    Intelligent router that decides which models to use for each task
    """
    
    def __init__(self, model_configs: Dict[ModelProvider, ModelConfig]):
        self.model_configs = model_configs
        self.task_history: List[Dict] = []
        self.routing_weights: Dict[Tuple[TaskType, ModelProvider], float] = {}
        
    def select_models(self, 
                     task: str,
                     task_type: TaskType,
                     parallel: bool = True) -> List[ModelProvider]:
        """Select best models for task"""
        
        suitable_models = []
        
        for provider, config in self.model_configs.items():
            if not config.enabled:
                continue
            
            # Check if task type is in strengths
            score = 0
            if task_type in config.strengths:
                score += 2.0
            elif task_type in config.weaknesses:
                score -= 1.0
            else:
                score += 1.0
            
            # Provider priority
            score *= config.priority
            
            # Task-provider routing history
            routing_key = (task_type, provider)
            if routing_key in self.routing_weights:
                score *= (1 + self.routing_weights[routing_key])
            
            suitable_models.append((provider, score))
        
        # Sort by score
        suitable_models.sort(key=lambda x: x[1], reverse=True)
        
        # Return top models (3-5 for parallel execution)
        if parallel:
            return [p for p, _ in suitable_models[:5]]
        else:
            return [suitable_models[0][0]]
    
    def route_task(self, 
                  task: str,
                  task_type: TaskType,
                  context: Optional[str] = None) -> Dict[str, Any]:
        """Route task and return routing plan"""
        
        models = self.select_models(task, task_type, parallel=True)
        
        plan = {
            "task": task,
            "task_type": task_type.value,
            "selected_models": [m.value for m in models],
            "parallel": len(models) > 1,
            "merge_strategy": MergeStrategy.CONSENSUS.value,
            "routing_timestamp": datetime.now().isoformat()
        }
        
        self.task_history.append(plan)
        return plan


class ModelAggregator:
    """
    Aggregates responses from multiple models using various strategies
    """
    
    def __init__(self):
        self.response_cache: Dict[str, ModelResponse] = {}
        self.merge_history: List[Dict] = []
        
    def aggregate(self,
                 responses: List[ModelResponse],
                 strategy: MergeStrategy = MergeStrategy.CONSENSUS,
                 task_type: Optional[TaskType] = None) -> MergedResponse:
        """Aggregate multiple model responses into single result"""
        
        if not responses:
            return MergedResponse(
                merged_content="",
                consensus_score=0.0,
                merge_strategy=strategy
            )
        
        # Route to appropriate aggregation strategy
        if strategy == MergeStrategy.CONSENSUS:
            return self._aggregate_consensus(responses)
        elif strategy == MergeStrategy.WEIGHTED:
            return self._aggregate_weighted(responses)
        elif strategy == MergeStrategy.BLENDED:
            return self._aggregate_blended(responses)
        elif strategy == MergeStrategy.PRIORITY:
            return self._aggregate_priority(responses)
        else:
            return self._aggregate_consensus(responses)
    
    def _aggregate_consensus(self, responses: List[ModelResponse]) -> MergedResponse:
        """Use majority voting for consensus"""
        
        if len(responses) == 1:
            return MergedResponse(
                merged_content=responses[0].content,
                consensus_score=responses[0].confidence,
                used_providers=[responses[0].provider],
                merge_strategy=MergeStrategy.CONSENSUS
            )
        
        # Check if responses are similar
        response_groups = self._group_similar_responses(responses)
        
        # Find largest group (majority)
        largest_group = max(response_groups.values(), key=len)
        consensus_score = len(largest_group) / len(responses)
        
        # Use first from majority as base
        merged_content = largest_group[0].content
        
        # Generate conflicts for non-consensus responses
        conflicts = []
        for provider, response in [(r.provider, r) for r in responses if r not in largest_group]:
            conflicts.append(MergeConflict(
                location="entire_response",
                provider1=largest_group[0].provider,
                response1=merged_content[:100],
                provider2=provider,
                response2=response.content[:100],
                confidence_diff=abs(largest_group[0].confidence - response.confidence)
            ))
        
        return MergedResponse(
            merged_content=merged_content,
            consensus_score=consensus_score,
            conflicts=conflicts,
            used_providers=[r.provider for r in responses],
            merge_strategy=MergeStrategy.CONSENSUS,
            reasoning=f"Consensus from {len(largest_group)}/{len(responses)} models"
        )
    
    def _aggregate_weighted(self, responses: List[ModelResponse]) -> MergedResponse:
        """Weight responses by confidence score"""
        
        if len(responses) == 1:
            return MergedResponse(
                merged_content=responses[0].content,
                consensus_score=responses[0].confidence,
                used_providers=[responses[0].provider],
                merge_strategy=MergeStrategy.WEIGHTED
            )
        
        # Sort by confidence
        sorted_responses = sorted(responses, key=lambda r: r.confidence, reverse=True)
        
        # Use highest confidence response as base
        merged_content = sorted_responses[0].content
        avg_confidence = sum(r.confidence for r in responses) / len(responses)
        
        # Generate conflicts
        conflicts = []
        for i, response in enumerate(sorted_responses[1:], 1):
            conflicts.append(MergeConflict(
                location=f"weighted_position_{i}",
                provider1=sorted_responses[0].provider,
                response1=merged_content[:100],
                provider2=response.provider,
                response2=response.content[:100],
                confidence_diff=sorted_responses[0].confidence - response.confidence
            ))
        
        return MergedResponse(
            merged_content=merged_content,
            consensus_score=avg_confidence,
            conflicts=conflicts,
            used_providers=[r.provider for r in responses],
            merge_strategy=MergeStrategy.WEIGHTED,
            reasoning=f"Weighted by confidence: {[f'{r.provider.value}({r.confidence:.2f})' for r in sorted_responses]}"
        )
    
    def _aggregate_blended(self, responses: List[ModelResponse]) -> MergedResponse:
        """Blend the best parts of each response"""
        
        # Split each response into lines
        response_lines = [r.content.split('\n') for r in responses]
        max_lines = max(len(lines) for lines in response_lines)
        
        # Create merged content by selecting best line from each position
        merged_lines = []
        for line_idx in range(max_lines):
            candidates = []
            for resp_idx, lines in enumerate(response_lines):
                if line_idx < len(lines):
                    candidates.append((line_idx, resp_idx, lines[line_idx]))
            
            if candidates:
                # Choose longest/best candidate for this line
                best = max(candidates, key=lambda x: len(x[2]))
                merged_lines.append(best[2])
        
        merged_content = '\n'.join(merged_lines)
        avg_confidence = sum(r.confidence for r in responses) / len(responses)
        
        return MergedResponse(
            merged_content=merged_content,
            consensus_score=avg_confidence,
            used_providers=[r.provider for r in responses],
            merge_strategy=MergeStrategy.BLENDED,
            reasoning="Blended best parts from all models"
        )
    
    def _aggregate_priority(self, responses: List[ModelResponse]) -> MergedResponse:
        """Use priority-based selection (highest priority first)"""
        
        # Sort by provider priority (assume GPT > Gemini > Grok > Local)
        priority_order = {
            ModelProvider.GPT_5_1: 4,
            ModelProvider.GEMINI_3: 3,
            ModelProvider.GROK_4_1: 2,
            ModelProvider.RECHAIN_LOCAL: 1
        }
        
        sorted_responses = sorted(
            responses,
            key=lambda r: priority_order.get(r.provider, 0),
            reverse=True
        )
        
        merged_content = sorted_responses[0].content
        avg_confidence = sum(r.confidence for r in responses) / len(responses)
        
        return MergedResponse(
            merged_content=merged_content,
            consensus_score=avg_confidence,
            used_providers=[r.provider for r in responses],
            merge_strategy=MergeStrategy.PRIORITY,
            reasoning=f"Selected by priority: {sorted_responses[0].provider.value}"
        )
    
    def _group_similar_responses(self, responses: List[ModelResponse]) -> Dict[str, List[ModelResponse]]:
        """Group similar responses together"""
        
        groups = {}
        for response in responses:
            # Use content hash as grouping key
            content_hash = hashlib.md5(response.content.encode()).hexdigest()
            if content_hash not in groups:
                groups[content_hash] = []
            groups[content_hash].append(response)
        
        return groups


class ModelConsensus:
    """
    Consensus mechanisms for multi-model decision making
    """
    
    @staticmethod
    def generate_diffs(responses: List[ModelResponse]) -> List[str]:
        """Generate unified diffs between responses"""
        
        diffs = []
        if len(responses) < 2:
            return diffs
        
        base_content = responses[0].content.split('\n')
        
        for response in responses[1:]:
            other_content = response.content.split('\n')
            diff = list(unified_diff(
                base_content,
                other_content,
                fromfile=responses[0].provider.value,
                tofile=response.provider.value,
                lineterm=''
            ))
            diffs.append('\n'.join(diff))
        
        return diffs
    
    @staticmethod
    def resolve_conflicts(conflicts: List[MergeConflict],
                         strategy: str = "confidence") -> str:
        """Resolve merge conflicts"""
        
        if not conflicts:
            return "No conflicts to resolve"
        
        if strategy == "confidence":
            # Use response with higher confidence
            result = []
            for conflict in conflicts:
                if conflict.confidence_diff > 0:
                    result.append(f"✓ Keeping {conflict.provider1.value}")
                else:
                    result.append(f"✓ Switching to {conflict.provider2.value}")
            return '\n'.join(result)
        
        return f"Resolved {len(conflicts)} conflicts using {strategy} strategy"


class MultiModelManager:
    """
    Central manager for multi-model orchestration and IDE integration
    """
    
    def __init__(self):
        # Initialize model configs
        self.model_configs = {
            ModelProvider.GEMINI_3: ModelConfig(
                provider=ModelProvider.GEMINI_3,
                model_name="gemini-3",
                priority=3,
                strengths={TaskType.CODE_GENERATION, TaskType.DOCUMENTATION},
                weaknesses={TaskType.DEBUGGING}
            ),
            ModelProvider.GROK_4_1: ModelConfig(
                provider=ModelProvider.GROK_4_1,
                model_name="grok-4.1",
                priority=2,
                strengths={TaskType.OPTIMIZATION, TaskType.ARCHITECTURE},
                weaknesses={TaskType.TESTING}
            ),
            ModelProvider.GPT_5_1: ModelConfig(
                provider=ModelProvider.GPT_5_1,
                model_name="gpt-5.1",
                priority=4,
                strengths={TaskType.CODE_REVIEW, TaskType.BUG_FIX, TaskType.DEBUGGING},
                weaknesses=set()
            ),
            ModelProvider.RECHAIN_LOCAL: ModelConfig(
                provider=ModelProvider.RECHAIN_LOCAL,
                model_name="rechain-local",
                priority=1,
                strengths={TaskType.OPTIMIZATION},
                weaknesses={TaskType.CODE_GENERATION, TaskType.ARCHITECTURE}
            )
        }
        
        self.router = ModelRouter(self.model_configs)
        self.aggregator = ModelAggregator()
        self.request_history: List[Dict] = []
        
    async def process_request(self,
                            prompt: str,
                            task_type: TaskType,
                            merge_strategy: MergeStrategy = MergeStrategy.CONSENSUS,
                            num_models: Optional[int] = None) -> MergedResponse:
        """
        Process request through multiple models and merge results
        """
        
        # Route to appropriate models
        routing_plan = self.router.route_task(prompt, task_type)
        models_to_use = [ModelProvider[m.split('_')[0].upper()] for m in routing_plan['selected_models']][:num_models or 5]
        
        # Simulate parallel requests to multiple models
        responses = await self._call_models_parallel(prompt, models_to_use)
        
        # Aggregate responses
        merged = self.aggregator.aggregate(responses, merge_strategy)
        
        # Generate diffs
        merged.diffs = ModelConsensus.generate_diffs(responses)
        
        # Log request
        self.request_history.append({
            "timestamp": datetime.now().isoformat(),
            "prompt": prompt[:100],
            "task_type": task_type.value,
            "models_used": [m.value for m in models_to_use],
            "consensus_score": merged.consensus_score,
            "conflicts": len(merged.conflicts)
        })
        
        return merged
    
    async def _call_models_parallel(self, 
                                   prompt: str,
                                   providers: List[ModelProvider]) -> List[ModelResponse]:
        """Call multiple models in parallel"""
        
        tasks = [
            self._call_single_model(prompt, provider)
            for provider in providers
        ]
        
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out errors
        valid_responses = [r for r in responses if isinstance(r, ModelResponse) and not r.error]
        return valid_responses
    
    async def _call_single_model(self, 
                                prompt: str,
                                provider: ModelProvider) -> ModelResponse:
        """Call single model (simulated)"""
        
        # Simulate API call with some delay
        await asyncio.sleep(0.1)
        
        # Generate model-specific response based on provider characteristics
        responses = {
            ModelProvider.GEMINI_3: f"[GEMINI-3] Implementation:\n{prompt}\n\n# Clean, documented solution",
            ModelProvider.GROK_4_1: f"[GROK-4.1] Optimized approach:\n{prompt}\n\n# Performance-optimized",
            ModelProvider.GPT_5_1: f"[GPT-5.1] Best practice:\n{prompt}\n\n# Industry-standard approach",
            ModelProvider.RECHAIN_LOCAL: f"[RECHAIN-LOCAL] Quick fix:\n{prompt}\n\n# Efficient local solution"
        }
        
        config = self.model_configs[provider]
        
        return ModelResponse(
            provider=provider,
            content=responses.get(provider, f"Response from {provider.value}"),
            confidence=0.75 + (0.05 * config.priority),
            reasoning=f"Generated by {provider.value} specialized in selected task",
            tokens_used=len(prompt.split()) * 2,
            latency_ms=100 + (50 * config.priority)
        )
    
    def get_mesh_status(self) -> Dict[str, Any]:
        """Get current mesh status"""
        
        return {
            "timestamp": datetime.now().isoformat(),
            "models": {
                provider.value: {
                    "enabled": config.enabled,
                    "priority": config.priority,
                    "strengths": [t.value for t in config.strengths],
                    "weaknesses": [t.value for t in config.weaknesses]
                }
                for provider, config in self.model_configs.items()
            },
            "total_requests": len(self.request_history),
            "average_consensus": sum(r["consensus_score"] for r in self.request_history) / max(1, len(self.request_history)) if self.request_history else 0
        }


class IDEMeshIntegration:
    """
    IDE integration for cross-AI mesh
    Handles multi-LLM merge, diff generation, and conflict resolution
    """
    
    def __init__(self):
        self.manager = MultiModelManager()
        self.open_merges: Dict[str, MergedResponse] = {}
        self.merge_history: List[Dict] = []
        
    async def get_multi_llm_suggestions(self,
                                       code: str,
                                       cursor_position: int,
                                       task_type: TaskType) -> Dict[str, Any]:
        """Get suggestions from multiple LLMs"""
        
        prompt = f"Code context:\n{code}\n\nPosition: {cursor_position}\n\nSuggestion needed:"
        
        merged = await self.manager.process_request(
            prompt,
            task_type,
            merge_strategy=MergeStrategy.BLENDED
        )
        
        return {
            "suggestions": merged.merged_content,
            "consensus_score": merged.consensus_score,
            "diffs": merged.diffs,
            "providers_used": [p.value for p in merged.used_providers],
            "conflicts": len(merged.conflicts)
        }
    
    async def multi_llm_merge(self,
                            code_versions: Dict[str, str],
                            merge_strategy: str = "consensus") -> Dict[str, Any]:
        """
        Git-like merge for multiple LLM outputs
        """
        
        merge_id = hashlib.md5(
            json.dumps(code_versions, sort_keys=True).encode()
        ).hexdigest()[:8]
        
        # Prepare versions as model responses
        responses = [
            ModelResponse(
                provider=ModelProvider[name.upper().split('_')[0]],
                content=code,
                confidence=0.8,
                reasoning=f"Version from {name}"
            )
            for name, code in code_versions.items()
        ]
        
        # Determine merge strategy
        strat = MergeStrategy.CONSENSUS
        if merge_strategy == "weighted":
            strat = MergeStrategy.WEIGHTED
        elif merge_strategy == "blended":
            strat = MergeStrategy.BLENDED
        
        merged = self.manager.aggregator.aggregate(responses, strat)
        merged.diffs = ModelConsensus.generate_diffs(responses)
        
        # Store merge for reference
        self.open_merges[merge_id] = merged
        
        return {
            "merge_id": merge_id,
            "merged_code": merged.merged_content,
            "consensus_score": merged.consensus_score,
            "strategy": merge_strategy,
            "conflicts": [
                {
                    "location": c.location,
                    "option1": c.response1[:50],
                    "option2": c.response2[:50],
                    "confidence_diff": c.confidence_diff
                }
                for c in merged.conflicts
            ],
            "diffs": merged.diffs[:2]  # Limit diffs in response
        }
    
    async def resolve_merge_conflict(self,
                                    merge_id: str,
                                    conflict_index: int,
                                    chosen_option: int) -> bool:
        """Resolve specific merge conflict"""
        
        if merge_id not in self.open_merges:
            return False
        
        merged = self.open_merges[merge_id]
        if conflict_index >= len(merged.conflicts):
            return False
        
        conflict = merged.conflicts[conflict_index]
        
        # Record resolution
        self.merge_history.append({
            "timestamp": datetime.now().isoformat(),
            "merge_id": merge_id,
            "conflict_index": conflict_index,
            "chosen": "option1" if chosen_option == 1 else "option2",
            "provider_chosen": conflict.provider1.value if chosen_option == 1 else conflict.provider2.value
        })
        
        return True
    
    async def auto_resolve_merge(self, merge_id: str) -> Dict[str, Any]:
        """Automatically resolve merge using consensus"""
        
        if merge_id not in self.open_merges:
            return {"success": False, "message": "Merge not found"}
        
        merged = self.open_merges[merge_id]
        
        # Resolve conflicts using confidence
        resolutions = ModelConsensus.resolve_conflicts(
            merged.conflicts,
            strategy="confidence"
        )
        
        del self.open_merges[merge_id]
        
        return {
            "success": True,
            "merge_id": merge_id,
            "final_code": merged.merged_content,
            "resolutions": resolutions,
            "conflicts_resolved": len(merged.conflicts)
        }
    
    def get_mesh_status(self) -> Dict[str, Any]:
        """Get IDE mesh status"""
        
        status = self.manager.get_mesh_status()
        status["open_merges"] = len(self.open_merges)
        status["total_merge_operations"] = len(self.merge_history)
        status["average_consensus_score"] = status.get("average_consensus", 0)
        
        return status
