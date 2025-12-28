"""
Cross-AI Developer Mesh Tests
Comprehensive testing of multi-model orchestration and IDE integration
"""

import pytest
import asyncio
from datetime import datetime

from aiplatform.cross_ai_mesh import (
    MultiModelManager, ModelRouter, ModelAggregator, ModelConsensus,
    IDEMeshIntegration, ModelProvider, TaskType, MergeStrategy,
    ModelConfig, ModelResponse
)


class TestModelRouter:
    """Test intelligent routing of tasks to models"""
    
    def test_model_selection_by_strength(self):
        """Test selecting models based on task type strength"""
        configs = {
            ModelProvider.GPT_5_1: ModelConfig(
                provider=ModelProvider.GPT_5_1,
                strengths={TaskType.CODE_REVIEW, TaskType.BUG_FIX},
                priority=4
            ),
            ModelProvider.GEMINI_3: ModelConfig(
                provider=ModelProvider.GEMINI_3,
                strengths={TaskType.CODE_GENERATION},
                priority=3
            )
        }
        
        router = ModelRouter(configs)
        models = router.select_models("Review this code", TaskType.CODE_REVIEW)
        
        # GPT should be selected first (strength match + highest priority)
        assert ModelProvider.GPT_5_1 in models
    
    def test_routing_plan_generation(self):
        """Test generation of complete routing plan"""
        configs = {
            ModelProvider.GPT_5_1: ModelConfig(
                provider=ModelProvider.GPT_5_1,
                priority=4
            ),
            ModelProvider.GEMINI_3: ModelConfig(
                provider=ModelProvider.GEMINI_3,
                priority=3
            )
        }
        
        router = ModelRouter(configs)
        plan = router.route_task("Write code", TaskType.CODE_GENERATION)
        
        assert plan["task_type"] == TaskType.CODE_GENERATION.value
        assert "selected_models" in plan
        assert plan["parallel"] is True


class TestModelAggregator:
    """Test aggregation of multiple model responses"""
    
    def test_consensus_aggregation_majority(self):
        """Test consensus when majority agrees"""
        responses = [
            ModelResponse(
                provider=ModelProvider.GPT_5_1,
                content="def hello():\n    return 'world'",
                confidence=0.9,
                reasoning="Most Pythonic"
            ),
            ModelResponse(
                provider=ModelProvider.GEMINI_3,
                content="def hello():\n    return 'world'",
                confidence=0.85,
                reasoning="Matches best practice"
            ),
            ModelResponse(
                provider=ModelProvider.GROK_4_1,
                content="def hello(): return 'world'",
                confidence=0.7,
                reasoning="More concise"
            )
        ]
        
        aggregator = ModelAggregator()
        merged = aggregator.aggregate(responses, MergeStrategy.CONSENSUS)
        
        assert merged.consensus_score >= 0.6  # 2/3 agree
        assert len(merged.conflicts) > 0  # One disagreement
    
    def test_weighted_aggregation(self):
        """Test aggregation by confidence weighting"""
        responses = [
            ModelResponse(
                provider=ModelProvider.GPT_5_1,
                content="High confidence response",
                confidence=0.95,
                reasoning="Expert"
            ),
            ModelResponse(
                provider=ModelProvider.RECHAIN_LOCAL,
                content="Low confidence response",
                confidence=0.5,
                reasoning="Local"
            )
        ]
        
        aggregator = ModelAggregator()
        merged = aggregator.aggregate(responses, MergeStrategy.WEIGHTED)
        
        # Higher confidence response should be preferred
        assert "High confidence" in merged.merged_content
    
    def test_blended_aggregation(self):
        """Test blending best parts from all responses"""
        responses = [
            ModelResponse(
                provider=ModelProvider.GPT_5_1,
                content="def process():\n    # Great comment\n    pass",
                confidence=0.8,
                reasoning="Good docs"
            ),
            ModelResponse(
                provider=ModelProvider.GROK_4_1,
                content="def process():\n    optimize()\n    return result",
                confidence=0.8,
                reasoning="Optimized"
            )
        ]
        
        aggregator = ModelAggregator()
        merged = aggregator.aggregate(responses, MergeStrategy.BLENDED)
        
        assert len(merged.merged_content) > 0
        assert merged.merge_strategy == MergeStrategy.BLENDED


class TestModelConsensus:
    """Test consensus mechanisms and conflict resolution"""
    
    def test_diff_generation(self):
        """Test generating diffs between responses"""
        responses = [
            ModelResponse(
                provider=ModelProvider.GPT_5_1,
                content="def hello():\n    return 'world'",
                confidence=0.8,
                reasoning="Test 1"
            ),
            ModelResponse(
                provider=ModelProvider.GEMINI_3,
                content="def hello():\n    return 'earth'",
                confidence=0.7,
                reasoning="Test 2"
            )
        ]
        
        diffs = ModelConsensus.generate_diffs(responses)
        assert len(diffs) > 0
        assert any("---" in d or "+++" in d for d in diffs)
    
    def test_conflict_resolution_by_confidence(self):
        """Test resolving conflicts using confidence scores"""
        from aiplatform.cross_ai_mesh import MergeConflict
        
        conflicts = [
            MergeConflict(
                location="line_1",
                provider1=ModelProvider.GPT_5_1,
                response1="print('hello')",
                provider2=ModelProvider.GEMINI_3,
                response2="print('hi')",
                confidence_diff=0.15  # GPT more confident
            )
        ]
        
        resolution = ModelConsensus.resolve_conflicts(conflicts, strategy="confidence")
        assert "gpt" in resolution.lower() or "keeping" in resolution.lower()


class TestMultiModelManager:
    """Test central multi-model orchestration"""
    
    @pytest.mark.asyncio
    async def test_process_request_single_task(self):
        """Test processing request through multiple models"""
        manager = MultiModelManager()
        
        merged = await manager.process_request(
            "Write hello world function",
            TaskType.CODE_GENERATION,
            merge_strategy=MergeStrategy.CONSENSUS
        )
        
        assert merged.merged_content != ""
        assert len(merged.used_providers) > 0
        assert 0 <= merged.consensus_score <= 1
    
    @pytest.mark.asyncio
    async def test_parallel_model_calls(self):
        """Test parallel execution of multiple models"""
        manager = MultiModelManager()
        
        responses = await manager._call_models_parallel(
            "test prompt",
            [ModelProvider.GPT_5_1, ModelProvider.GEMINI_3, ModelProvider.GROK_4_1]
        )
        
        assert len(responses) >= 1
        assert all(hasattr(r, 'content') for r in responses)
    
    def test_mesh_status(self):
        """Test getting mesh status"""
        manager = MultiModelManager()
        
        status = manager.get_mesh_status()
        
        assert "models" in status
        assert ModelProvider.GPT_5_1.value in status["models"]
        assert "total_requests" in status


class TestIDEMeshIntegration:
    """Test IDE integration with mesh"""
    
    @pytest.mark.asyncio
    async def test_multi_llm_suggestions(self):
        """Test getting suggestions from multiple LLMs"""
        ide = IDEMeshIntegration()
        
        suggestions = await ide.get_multi_llm_suggestions(
            "def add(a, b):",
            cursor_position=15,
            task_type=TaskType.CODE_GENERATION
        )
        
        assert "suggestions" in suggestions
        assert "consensus_score" in suggestions
        assert "providers_used" in suggestions
        assert len(suggestions["providers_used"]) > 0
    
    @pytest.mark.asyncio
    async def test_multi_llm_merge_consensus(self):
        """Test merging multiple LLM outputs with consensus"""
        ide = IDEMeshIntegration()
        
        versions = {
            "gpt": "def hello():\n    return 'world'",
            "gemini": "def hello():\n    return 'world'",
            "grok": "def hello(): return 'earth'"
        }
        
        result = await ide.multi_llm_merge(
            versions,
            merge_strategy="consensus"
        )
        
        assert "merge_id" in result
        assert "merged_code" in result
        assert result["consensus_score"] > 0
        assert "conflicts" in result
    
    @pytest.mark.asyncio
    async def test_multi_llm_merge_blended(self):
        """Test merging with blended strategy"""
        ide = IDEMeshIntegration()
        
        versions = {
            "gpt": "def process():\n    # Docstring\n    return result",
            "gemini": "def process():\n    optimize()\n    return result"
        }
        
        result = await ide.multi_llm_merge(
            versions,
            merge_strategy="blended"
        )
        
        assert "merge_id" in result
        assert len(result["merged_code"]) > 0
    
    @pytest.mark.asyncio
    async def test_merge_conflict_resolution(self):
        """Test resolving specific merge conflicts"""
        ide = IDEMeshIntegration()
        
        versions = {
            "gpt": "print('hello')",
            "gemini": "print('hi')"
        }
        
        merge_result = await ide.multi_llm_merge(versions)
        merge_id = merge_result["merge_id"]
        
        # Resolve first conflict if exists
        if merge_result["conflicts"]:
            resolved = await ide.resolve_merge_conflict(merge_id, 0, 1)
            assert resolved is True
    
    @pytest.mark.asyncio
    async def test_auto_resolve_merge(self):
        """Test automatic conflict resolution"""
        ide = IDEMeshIntegration()
        
        versions = {
            "gpt": "solution_1",
            "gemini": "solution_1",
            "grok": "solution_2"
        }
        
        merge_result = await ide.multi_llm_merge(versions)
        merge_id = merge_result["merge_id"]
        
        auto_resolved = await ide.auto_resolve_merge(merge_id)
        
        assert auto_resolved["success"] is True
        assert "final_code" in auto_resolved
    
    def test_mesh_status_from_ide(self):
        """Test IDE mesh status"""
        ide = IDEMeshIntegration()
        
        status = ide.get_mesh_status()
        
        assert "models" in status
        assert "open_merges" in status
        assert "total_merge_operations" in status


class TestEndToEndWorkflow:
    """End-to-end tests for complete workflows"""
    
    @pytest.mark.asyncio
    async def test_complete_development_workflow(self):
        """Test complete development workflow"""
        ide = IDEMeshIntegration()
        
        # Step 1: Generate code with multiple models
        suggestions = await ide.get_multi_llm_suggestions(
            "class DataProcessor:",
            cursor_position=20,
            task_type=TaskType.CODE_GENERATION
        )
        
        assert suggestions["consensus_score"] > 0
        
        # Step 2: Get code review from multiple models
        review_versions = {
            "gpt_review": "Code quality: Good\nIssues: None",
            "gemini_review": "Code quality: Good\nIssues: Add docstring"
        }
        
        merge_result = await ide.multi_llm_merge(review_versions)
        assert "merge_id" in merge_result
        
        # Step 3: Auto-resolve
        final_result = await ide.auto_resolve_merge(merge_result["merge_id"])
        assert final_result["success"] is True
    
    @pytest.mark.asyncio
    async def test_merge_conflict_resolution_workflow(self):
        """Test workflow with conflict resolution"""
        ide = IDEMeshIntegration()
        
        # Create merge with conflicts
        versions = {
            "approach_1": "def solve():\n    return solution_a()",
            "approach_2": "def solve():\n    return solution_b()"
        }
        
        merge = await ide.multi_llm_merge(versions)
        
        # Should have conflicts
        assert len(merge["conflicts"]) > 0
        
        # Resolve conflicts manually
        for i, conflict in enumerate(merge["conflicts"]):
            await ide.resolve_merge_conflict(merge["merge_id"], i, 1)
        
        # Final auto-resolve
        final = await ide.auto_resolve_merge(merge["merge_id"])
        assert final["success"] is True


class TestPerformanceAndScalability:
    """Test performance characteristics"""
    
    @pytest.mark.asyncio
    async def test_multiple_sequential_requests(self):
        """Test handling multiple sequential requests"""
        manager = MultiModelManager()
        
        for i in range(5):
            merged = await manager.process_request(
                f"Request {i}: write a function",
                TaskType.CODE_GENERATION
            )
            assert merged.merged_content != ""
        
        assert len(manager.request_history) == 5
    
    @pytest.mark.asyncio
    async def test_concurrent_requests(self):
        """Test handling concurrent requests"""
        ide = IDEMeshIntegration()
        
        tasks = [
            ide.get_multi_llm_suggestions(
                f"Task {i}",
                i * 10,
                TaskType.CODE_GENERATION
            )
            for i in range(3)
        ]
        
        results = await asyncio.gather(*tasks)
        
        assert len(results) == 3
        assert all("suggestions" in r for r in results)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
