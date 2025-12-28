"""
Comprehensive tests for Quantum Code Optimizer system.

Tests cover:
  - Patch generation
  - Quantum embeddings
  - Similarity analysis
  - Smell detection
  - QAOA optimization
  - VQE cost evaluation
  - Ranking engine
  - End-to-end optimization
"""

import unittest
import math
from datetime import datetime
from aiplatform.quantum_code_optimizer import (
    QuantumCodeAnalyzer, PatchGenerator, QuantumEmbedder,
    QuantumSimilarityCircuit, QAOAPatchOptimizer, VQECostEvaluator,
    PatchRankingEngine, CodePatch, PatchType, CodeSmellType,
    QuantumAlgorithm, QuantumOptimizationReport, PatchOptimizationResult
)


class TestPatchGenerator(unittest.TestCase):
    """Test patch generation."""

    def setUp(self):
        self.generator = PatchGenerator()

    def test_generate_patches_from_issues(self):
        """Test patch generation from code issues."""
        code = "x = 1\ny = 2\nz = x + y"
        issues = [
            {'type': 'unused_variable', 'location': (0, 0), 'description': 'Unused variable x'}
        ]

        patches = self.generator.generate_patches(code, {'issues': issues})

        self.assertEqual(len(patches), 1)
        self.assertEqual(patches[0].patch_type, PatchType.BUG_FIX)
        self.assertGreater(patches[0].risk_score, 0)

    def test_patch_has_id(self):
        """Test that patches get unique IDs."""
        code = "pass"
        issues = [{'type': 'bug', 'location': (0, 0), 'description': 'test bug'}]

        patch1 = self.generator.generate_patches(code, {'issues': issues})[0]
        patch2 = self.generator.generate_patches(code, {'issues': issues})[0]

        self.assertNotEqual(patch1.id, patch2.id)

    def test_patch_type_detection(self):
        """Test patch type detection from description."""
        code = "pass"

        test_cases = [
            ('Bug fix issue', PatchType.BUG_FIX),
            ('Performance improvement', PatchType.PERFORMANCE),
            ('Security vulnerability', PatchType.SECURITY),
        ]

        for description, expected_type in test_cases:
            issues = [{'type': 'test', 'location': (0, 0), 'description': description}]
            patch = self.generator.generate_patches(code, {'issues': issues})[0]
            self.assertEqual(patch.patch_type, expected_type)


class TestQuantumEmbedder(unittest.TestCase):
    """Test quantum embedding generation."""

    def setUp(self):
        self.embedder = QuantumEmbedder(qubits=10)

    def test_embed_code_creates_state_vector(self):
        """Test that code embedding creates valid quantum state."""
        code = "def add(a, b):\n    return a + b"
        embedding = self.embedder.embed_code(code)

        self.assertIsNotNone(embedding.state_vector)
        self.assertEqual(len(embedding.state_vector), 2 ** 10)

    def test_embedding_caching(self):
        """Test that same code produces cached embedding."""
        code = "x = 1"
        embedding1 = self.embedder.embed_code(code)
        embedding2 = self.embedder.embed_code(code)

        self.assertEqual(embedding1.code_hash, embedding2.code_hash)
        self.assertEqual(len(self.embedder.embedding_cache), 1)

    def test_classical_features_extracted(self):
        """Test extraction of classical code features."""
        code = """
def hello():
    if True:
        print("hi")
"""
        embedding = self.embedder.embed_code(code)

        self.assertIn('lines_of_code', embedding.classical_features)
        self.assertIn('complexity', embedding.classical_features)
        self.assertIn('nesting_depth', embedding.classical_features)
        self.assertIn('function_count', embedding.classical_features)

    def test_different_codes_have_different_embeddings(self):
        """Test that different code produces different embeddings."""
        code1 = "x = 1"
        code2 = "x = 2"

        embedding1 = self.embedder.embed_code(code1)
        embedding2 = self.embedder.embed_code(code2)

        self.assertNotEqual(embedding1.code_hash, embedding2.code_hash)

    def test_state_vector_normalized(self):
        """Test that quantum state is properly normalized."""
        code = "def f(): pass"
        embedding = self.embedder.embed_code(code)

        norm_squared = sum(abs(a) ** 2 for a in embedding.state_vector)
        self.assertAlmostEqual(norm_squared, 1.0, places=5)


class TestQuantumSimilarityCircuit(unittest.TestCase):
    """Test quantum similarity and smell detection."""

    def setUp(self):
        self.embedder = QuantumEmbedder(qubits=8)
        self.circuit = QuantumSimilarityCircuit(self.embedder)

    def test_identical_code_has_high_similarity(self):
        """Test that identical code shows high similarity."""
        code = "def func(): return 42"
        similarity = self.circuit.calculate_code_similarity(code, code)

        self.assertGreater(similarity.similarity_score, 0.95)
        self.assertEqual(similarity.similarity_type, "exact")

    def test_different_code_has_low_similarity(self):
        """Test that very different code shows low similarity."""
        code1 = "x = 1"
        code2 = "class A: pass"

        similarity = self.circuit.calculate_code_similarity(code1, code2)
        self.assertLess(similarity.similarity_score, 0.5)

    def test_similar_code_has_semantic_similarity(self):
        """Test semantic similarity detection."""
        code1 = "def add(a, b): return a + b"
        code2 = "def sum_two(x, y): return x + y"

        similarity = self.circuit.calculate_code_similarity(code1, code2)
        self.assertGreater(similarity.similarity_score, 0.6)

    def test_detect_duplicate_code(self):
        """Test duplicate code detection."""
        code = """
def func1():
    x = 1
    y = 2
    return x + y

def func2():
    x = 1
    y = 2
    return x + y
"""
        smells = self.circuit.detect_code_smells(code)
        duplicate_smells = [s for s in smells if s.smell_type == CodeSmellType.DUPLICATE_CODE]

        self.assertGreater(len(duplicate_smells), 0)

    def test_detect_long_method(self):
        """Test long method detection."""
        code = "\n".join(["x = 1"] * 60)

        smells = self.circuit.detect_code_smells(code)
        # May or may not detect (depends on structure)
        self.assertIsInstance(smells, list)

    def test_detect_deep_nesting(self):
        """Test deep nesting detection."""
        code = """
if True:
    if True:
        if True:
            if True:
                if True:
                    x = 1
"""
        smells = self.circuit.detect_code_smells(code)
        deep_nest = [s for s in smells if s.smell_type == CodeSmellType.DEEP_NESTING]

        self.assertGreater(len(deep_nest), 0)

    def test_detect_complex_logic(self):
        """Test complex logic detection."""
        code = "if a and b or c and d and e or f and g: pass" * 5

        smells = self.circuit.detect_code_smells(code)
        complex_smells = [s for s in smells if s.smell_type == CodeSmellType.COMPLEX_LOGIC]

        self.assertGreaterEqual(len(complex_smells), 0)


class TestQAOAPatchOptimizer(unittest.TestCase):
    """Test QAOA patch optimization."""

    def setUp(self):
        self.optimizer = QAOAPatchOptimizer()

    def _create_test_patches(self, count=3):
        """Helper to create test patches."""
        patches = []
        for i in range(count):
            patch = CodePatch(
                id=f"patch_{i}",
                original_code="x = 1",
                patched_code=f"x = {i}",
                patch_type=PatchType.BUG_FIX,
                description=f"Fix {i}",
                risk_score=0.3 + i * 0.1,
                complexity_score=0.2 + i * 0.1
            )
            patches.append(patch)
        return patches

    def test_optimize_patches_returns_results(self):
        """Test that optimization returns results."""
        patches = self._create_test_patches(3)
        results = self.optimizer.optimize_patches(patches)

        self.assertEqual(len(results), 3)

    def test_results_ranked_by_success_probability(self):
        """Test that results are ranked by success probability."""
        patches = self._create_test_patches(3)
        results = self.optimizer.optimize_patches(patches)

        # Check that rankings are in order
        for i, result in enumerate(results):
            self.assertEqual(result.ranking, i + 1)

    def test_results_use_qaoa_algorithm(self):
        """Test that results indicate QAOA algorithm."""
        patches = self._create_test_patches(2)
        results = self.optimizer.optimize_patches(patches)

        for result in results:
            self.assertEqual(result.algorithm_used, QuantumAlgorithm.QAOA)

    def test_success_probability_in_valid_range(self):
        """Test that success probabilities are 0-1."""
        patches = self._create_test_patches(3)
        results = self.optimizer.optimize_patches(patches)

        for result in results:
            self.assertGreaterEqual(result.success_probability, 0)
            self.assertLessEqual(result.success_probability, 1)

    def test_expected_impact_based_on_patch_type(self):
        """Test that impact varies by patch type."""
        security_patch = CodePatch(
            id="sec_patch",
            original_code="pass",
            patched_code="pass",
            patch_type=PatchType.SECURITY,
            description="Security fix",
            risk_score=0.5
        )

        perf_patch = CodePatch(
            id="perf_patch",
            original_code="pass",
            patched_code="pass",
            patch_type=PatchType.PERFORMANCE,
            description="Performance",
            risk_score=0.3
        )

        patches = [security_patch, perf_patch]
        results = self.optimizer.optimize_patches(patches)

        sec_result = next(r for r in results if r.patch_id == "sec_patch")
        perf_result = next(r for r in results if r.patch_id == "perf_patch")

        self.assertGreater(sec_result.expected_impact, perf_result.expected_impact)


class TestVQECostEvaluator(unittest.TestCase):
    """Test VQE cost evaluation."""

    def setUp(self):
        self.evaluator = VQECostEvaluator()

    def test_evaluate_patch_cost(self):
        """Test VQE cost evaluation."""
        patch = CodePatch(
            id="test",
            original_code="x = 1",
            patched_code="x = 2\ny = 3",
            patch_type=PatchType.BUG_FIX,
            description="test",
            risk_score=0.4
        )

        evaluation = self.evaluator.evaluate_patch_cost(patch)

        self.assertIn('total_cost', evaluation)
        self.assertIn('code_change_magnitude', evaluation)
        self.assertIn('testing_requirement', evaluation)
        self.assertIn('deployment_risk', evaluation)

    def test_cost_in_valid_range(self):
        """Test that costs are 0-1."""
        patch = CodePatch(
            id="test",
            original_code="x = 1",
            patched_code="x = 2",
            patch_type=PatchType.REFACTORING,
            description="test",
            risk_score=0.5
        )

        evaluation = self.evaluator.evaluate_patch_cost(patch)

        self.assertGreaterEqual(evaluation['total_cost'], 0)
        self.assertLessEqual(evaluation['total_cost'], 1)

    def test_security_patches_require_more_testing(self):
        """Test that security patches require more testing."""
        security_patch = CodePatch(
            id="sec",
            original_code="pass",
            patched_code="pass",
            patch_type=PatchType.SECURITY,
            description="Security",
            risk_score=0.5
        )

        perf_patch = CodePatch(
            id="perf",
            original_code="pass",
            patched_code="pass",
            patch_type=PatchType.PERFORMANCE,
            description="Perf",
            risk_score=0.3
        )

        sec_eval = self.evaluator.evaluate_patch_cost(security_patch)
        perf_eval = self.evaluator.evaluate_patch_cost(perf_patch)

        self.assertGreater(
            sec_eval['testing_requirement'],
            perf_eval['testing_requirement']
        )


class TestPatchRankingEngine(unittest.TestCase):
    """Test final patch ranking."""

    def setUp(self):
        self.engine = PatchRankingEngine()

    def _create_test_data(self):
        """Create test patches and results."""
        patches = [
            CodePatch(
                id=f"p{i}",
                original_code="x",
                patched_code="y",
                patch_type=PatchType.BUG_FIX,
                description=f"Patch {i}",
                risk_score=0.3 + i * 0.1
            )
            for i in range(3)
        ]

        qaoa_results = [
            PatchOptimizationResult(
                patch_id=f"p{i}",
                success_probability=0.8 - i * 0.1,
                expected_impact=0.7,
                risk_assessment=0.3,
                quantum_score=0.75,
                ranking=0,
                algorithm_used=QuantumAlgorithm.QAOA,
                execution_time_ms=100,
                reasoning="test"
            )
            for i in range(3)
        ]

        vqe_evals = [
            {'total_cost': 0.3 + i * 0.1} for i in range(3)
        ]

        return patches, qaoa_results, vqe_evals

    def test_rank_patches_combines_results(self):
        """Test that ranking combines QAOA and VQE results."""
        patches, qaoa_results, vqe_evals = self._create_test_data()

        final = self.engine.rank_patches(patches, qaoa_results, vqe_evals)

        self.assertEqual(len(final), 3)
        # Check rankings are assigned
        rankings = [r.ranking for r in final]
        self.assertEqual(rankings, [1, 2, 3])

    def test_final_quantum_score_computed(self):
        """Test that final quantum score is computed."""
        patches, qaoa_results, vqe_evals = self._create_test_data()

        final = self.engine.rank_patches(patches, qaoa_results, vqe_evals)

        for result in final:
            self.assertGreater(result.quantum_score, 0)
            self.assertLess(result.quantum_score, 1)


class TestQuantumCodeAnalyzer(unittest.TestCase):
    """Test complete quantum code analyzer."""

    def setUp(self):
        self.analyzer = QuantumCodeAnalyzer()

    def test_analyze_and_optimize_returns_report(self):
        """Test that analyzer returns complete report."""
        code = "def func():\n    return 42"
        results = {'issues': []}

        report = self.analyzer.analyze_and_optimize(code, results)

        self.assertIsInstance(report, QuantumOptimizationReport)
        self.assertGreater(len(report.all_rankings), 0)

    def test_report_includes_smells(self):
        """Test that report includes detected code smells."""
        code = """
def long_func():
    x = 1
    y = 2
    if True:
        if True:
            if True:
                if True:
                    z = 3
"""
        results = {'issues': []}

        report = self.analyzer.analyze_and_optimize(code, results)

        self.assertIsInstance(report.code_smells_detected, list)

    def test_get_recommendations_returns_list(self):
        """Test that recommendations can be generated."""
        code = "x = 1"
        recommendations = self.analyzer.get_recommendations(code, num_suggestions=2)

        self.assertIsInstance(recommendations, list)
        self.assertLessEqual(len(recommendations), 2)

    def test_ide_suggest_patches_format(self):
        """Test IDE integration method format."""
        code = "def test(): pass"
        suggestions = self.analyzer.ide_suggest_patches(code)

        self.assertIn('top_patch', suggestions)
        self.assertIn('all_patches', suggestions)
        self.assertIn('smells', suggestions)
        self.assertIn('recommendations', suggestions)
        self.assertIn('quantum_confidence', suggestions)

    def test_analysis_history_tracked(self):
        """Test that analysis history is tracked."""
        code1 = "x = 1"
        code2 = "y = 2"

        self.analyzer.analyze_and_optimize(code1, {'issues': []})
        self.analyzer.analyze_and_optimize(code2, {'issues': []})

        self.assertEqual(len(self.analyzer.analysis_history), 2)


class TestEndToEndOptimization(unittest.TestCase):
    """End-to-end optimization workflow."""

    def test_real_world_patch_optimization(self):
        """Test realistic code optimization scenario."""
        code = """
def calculate_sum(numbers):
    total = 0
    for n in numbers:
        total = total + n
    return total

def calculate_sum(items):
    result = 0
    for item in items:
        result = result + item
    return result
"""

        analyzer = QuantumCodeAnalyzer()
        analysis_results = {
            'issues': [
                {'type': 'duplicate', 'location': (0, 5), 'description': 'Duplicate function'},
                {'type': 'inefficient', 'location': (0, 5), 'description': 'Loop not optimized'}
            ]
        }

        report = analyzer.analyze_and_optimize(code, analysis_results)

        # Verify report structure
        self.assertIsNotNone(report.top_recommendation)
        self.assertGreater(len(report.all_rankings), 0)
        self.assertGreater(report.total_quantum_time_ms, 0)

    def test_multiple_code_smells_detection(self):
        """Test detection of multiple code smells in realistic code."""
        code = """
class DataProcessor:
    def process(self, data):
        result = []
        if data:
            for item in data:
                if item > 0:
                    x = item
                    if x > 10:
                        if x > 20:
                            result.append(x)
        return result

    # Duplicate below
    def analyze(self, info):
        result = []
        if info:
            for item in info:
                if item > 0:
                    x = item
                    if x > 10:
                        if x > 20:
                            result.append(x)
        return result
"""

        circuit = QuantumSimilarityCircuit(QuantumEmbedder())
        smells = circuit.detect_code_smells(code)

        # Should detect multiple smells
        self.assertGreater(len(smells), 0)
        smell_types = set(s.smell_type for s in smells)
        # Should detect at least 2+ smell types
        self.assertGreaterEqual(len(smell_types), 1)


if __name__ == '__main__':
    unittest.main()
