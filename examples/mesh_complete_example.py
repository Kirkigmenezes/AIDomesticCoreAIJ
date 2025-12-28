"""
Cross-AI Developer Mesh - Complete Example
Demonstrates multi-LLM orchestration, merging, and conflict resolution
"""

import asyncio
from aiplatform.cross_ai_mesh import (
    IDEMeshIntegration, TaskType, MergeStrategy
)


async def main():
    print("\n" + "="*80)
    print("CROSS-AI DEVELOPER MESH - COMPLETE DEMONSTRATION")
    print("="*80 + "\n")
    
    ide = IDEMeshIntegration()
    
    # ========================================================================
    # SCENARIO 1: Multi-Model Code Generation with Consensus
    # ========================================================================
    
    print("[SCENARIO 1] Multi-Model Code Generation with Consensus\n")
    print("Task: Implement quicksort algorithm")
    print("-"*80)
    
    suggestions = await ide.get_multi_llm_suggestions(
        code="def quicksort(arr):",
        cursor_position=20,
        task_type=TaskType.CODE_GENERATION
    )
    
    print(f"\n✓ Received suggestions from: {', '.join(suggestions['providers_used'])}")
    print(f"✓ Consensus Score: {suggestions['consensus_score']:.1%}")
    print(f"✓ Number of Conflicts: {suggestions['conflicts']}")
    print(f"\nMerged Suggestion:\n{'-'*40}")
    print(suggestions['suggestions'][:200] + "...")
    
    # ========================================================================
    # SCENARIO 2: Multiple Approaches with Merge Conflict Resolution
    # ========================================================================
    
    print("\n\n[SCENARIO 2] Multiple Implementation Approaches\n")
    print("Task: Sort an array - different models suggest different approaches")
    print("-"*80)
    
    code_versions = {
        "gpt_approach": """def sort_array(arr):
    # Quicksort - O(n log n) average
    def quicksort(arr, low, high):
        if low < high:
            pi = partition(arr, low, high)
            quicksort(arr, low, pi - 1)
            quicksort(arr, pi + 1, high)
    return quicksort(arr, 0, len(arr) - 1)""",
        
        "gemini_approach": """def sort_array(arr):
    # Mergesort - O(n log n) guaranteed
    def mergesort(arr):
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left = mergesort(arr[:mid])
        right = mergesort(arr[mid:])
        return merge(left, right)
    return mergesort(arr)""",
        
        "grok_approach": """def sort_array(arr):
    # Heapsort - O(n log n) in-place
    def heapify(arr, n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        if left < n and arr[left] > arr[largest]:
            largest = left
        if right < n and arr[right] > arr[largest]:
            largest = right
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(arr, n, largest)
    for i in range(len(arr) // 2 - 1, -1, -1):
        heapify(arr, len(arr), i)
    return arr"""
    }
    
    # Merge using consensus strategy
    merge_consensus = await ide.multi_llm_merge(
        code_versions,
        merge_strategy="consensus"
    )
    
    print("\n[CONSENSUS MERGE]")
    print(f"Merge ID: {merge_consensus['merge_id']}")
    print(f"Consensus Score: {merge_consensus['consensus_score']:.1%}")
    print(f"Number of Conflicts: {len(merge_consensus['conflicts'])}")
    print(f"\nMerged Implementation:\n{'-'*40}")
    print(merge_consensus['merged_code'][:150] + "...")
    
    # Show conflicts
    if merge_consensus['conflicts']:
        print(f"\nConflicts Detected: {len(merge_consensus['conflicts'])}")
        for i, conflict in enumerate(merge_consensus['conflicts'][:2]):
            print(f"\n  Conflict {i+1}:")
            print(f"    Location: {conflict['location']}")
            print(f"    Option 1: {conflict['option1']}")
            print(f"    Option 2: {conflict['option2']}")
    
    # ========================================================================
    # SCENARIO 3: Blended Merging - Combine Best Parts
    # ========================================================================
    
    print("\n\n[SCENARIO 3] Blended Merging (Best of All Approaches)\n")
    print("Task: Merge all three approaches taking the best parts")
    print("-"*80)
    
    merge_blended = await ide.multi_llm_merge(
        code_versions,
        merge_strategy="blended"
    )
    
    print(f"\n✓ Blended Merge ID: {merge_blended['merge_id']}")
    print(f"✓ Consensus Score: {merge_blended['consensus_score']:.1%}")
    print(f"✓ Strategy: Takes best lines from each approach")
    print(f"\nBlended Result:\n{'-'*40}")
    print(merge_blended['merged_code'][:150] + "...")
    
    # ========================================================================
    # SCENARIO 4: Manual Conflict Resolution
    # ========================================================================
    
    print("\n\n[SCENARIO 4] Manual Conflict Resolution\n")
    print("Task: Resolve conflicts by choosing preferred implementation")
    print("-"*80)
    
    code_versions_conflict = {
        "recursive": "def fibonacci(n):\n    return fib(n-1) + fib(n-2) if n > 1 else n",
        "iterative": "def fibonacci(n):\n    a, b = 0, 1\n    for _ in range(n): a, b = b, a+b\n    return a",
        "memoized": "def fibonacci(n, memo={}):\n    if n in memo: return memo[n]\n    if n <= 1: return n\n    memo[n] = fibonacci(n-1, memo) + fibonacci(n-2, memo)\n    return memo[n]"
    }
    
    merge_resolve = await ide.multi_llm_merge(code_versions_conflict)
    merge_id = merge_resolve['merge_id']
    
    print(f"\n✓ Created merge: {merge_id}")
    print(f"✓ Conflicts found: {len(merge_resolve['conflicts'])}")
    
    # Resolve first conflict
    if merge_resolve['conflicts']:
        print(f"\nResolving first conflict...")
        resolved = await ide.resolve_merge_conflict(merge_id, 0, 1)
        print(f"✓ Conflict resolved: {resolved}")
    
    # Auto-resolve remaining
    final = await ide.auto_resolve_merge(merge_id)
    print(f"\n✓ Auto-resolved remaining conflicts")
    print(f"✓ Final implementation chosen")
    print(f"\nFinal Code:\n{'-'*40}")
    print(final['final_code'][:100] + "...")
    
    # ========================================================================
    # SCENARIO 5: Code Review from Multiple Perspectives
    # ========================================================================
    
    print("\n\n[SCENARIO 5] Code Review from Multiple Models\n")
    print("Task: Get code review from GPT, Gemini, and Grok")
    print("-"*80)
    
    reviews = {
        "gpt_review": """✓ Code Quality: A+
✓ Performance: Excellent
⚠ Issues: None critical
→ Suggestion: Consider type hints""",
        
        "gemini_review": """✓ Code Quality: A
✓ Performance: Good
⚠ Issues: Missing docstring
→ Suggestion: Add comprehensive docstring""",
        
        "grok_review": """✓ Code Quality: A
✓ Performance: Could optimize
⚠ Issues: Not using latest Python features
→ Suggestion: Use walrus operator for conditions"""
    }
    
    merge_review = await ide.multi_llm_merge(reviews, merge_strategy="blended")
    
    print(f"\n✓ Reviews from: GPT-5.1, Gemini-3, Grok-4.1")
    print(f"✓ Consensus Score: {merge_review['consensus_score']:.1%}")
    print(f"\nMerged Review:\n{'-'*40}")
    print(merge_review['merged_code'][:200] + "...")
    
    # ========================================================================
    # SCENARIO 6: Mesh Status and Metrics
    # ========================================================================
    
    print("\n\n[SCENARIO 6] Mesh Status and Performance Metrics\n")
    print("-"*80)
    
    status = ide.get_mesh_status()
    
    print(f"\n✓ Total Requests Processed: {status['total_requests']}")
    print(f"✓ Average Consensus Score: {status['average_consensus_score']:.1%}")
    print(f"✓ Open Merges: {status['open_merges']}")
    print(f"✓ Total Merge Operations: {status['total_merge_operations']}")
    
    print(f"\nActive Models in Mesh:")
    for provider, config in status['models'].items():
        print(f"\n  📦 {provider}")
        print(f"     Priority: {config['priority']}")
        print(f"     Status: {'✓ Enabled' if config['enabled'] else '✗ Disabled'}")
        print(f"     Strengths: {', '.join([s.split('_')[0] for s in config['strengths'][:3]])}")
    
    # ========================================================================
    # SUMMARY
    # ========================================================================
    
    print("\n\n" + "="*80)
    print("CROSS-AI DEVELOPER MESH - SUMMARY")
    print("="*80)
    
    print("""
✓ Scenario 1: Multi-Model Code Generation
  → All models suggest and reach consensus

✓ Scenario 2: Merge Conflict Resolution
  → Different approaches detected and shown as conflicts

✓ Scenario 3: Blended Merging
  → Combined best parts from all approaches

✓ Scenario 4: Manual Conflict Resolution
  → User resolves conflicts by selecting preferred option

✓ Scenario 5: Multi-Perspective Review
  → Each model provides unique insights, merged intelligently

✓ Scenario 6: Performance Metrics
  → Track mesh usage and model performance

KEY BENEFITS:
═════════════════════════════════════════════════════════════════════════════════
1. Never use just one model - leverage best of all four simultaneously
2. Automatic routing - optimal model selection for each task type
3. Git-like merging - resolve AI conflicts like code conflicts
4. Consensus scoring - know how much models agree (confidence metric)
5. Conflict visibility - see disagreements and choose best approach
6. Intelligent aggregation - 5 different merge strategies

REAL-WORLD APPLICATIONS:
═════════════════════════════════════════════════════════════════════════════════
• Code Generation: Consensus of 4 models vs 1 model output
• Bug Fixing: Debug from different expert perspectives simultaneously
• Code Review: Multi-expert review in single interface
• Architecture: Different models, different perspectives (GPT+Grok)
• Optimization: Grok excels, GPT validates approach
• Learning: See how different models tackle same problem
    """)
    
    print("="*80)
    print("Demo Complete! ✓")
    print("="*80 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
