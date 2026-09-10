---
name: cf-dsa
description: CodeForge cross-cutting Data Structures and Algorithms correctness skill applied on top of all language implementations.
---

# CodeForge Skill: Cross-Cutting DSA Correctness

- **SKILL:** DSA Correctness (Cross-Cutting)
- **TRIGGERS:** Any algorithmic or data structure implementation in any supported language
- **SCOPE:** Validates algorithmic correctness, asymptotic complexity, and edge case coverage across original and translated implementations.
- **COMMON_FAULTS:**
  - `DSA-001`: Unhandled empty input collection or null pointers
  - `DSA-002`: Off-by-one boundary conditions (zero index vs 1-based, inclusive vs exclusive bounds)
  - `DSA-003`: Integer overflow/underflow on boundary values ($2^{31}-1$, $-2^{31}$)
  - `DSA-004`: Cycle detection failure in linked lists or graphs (causing infinite recursion/loop)
  - `DSA-005`: Inefficient complexity (e.g., $O(N^2)$ brute force where $O(N \log N)$ or $O(N)$ is standard)
  - `DSA-006`: Duplicates or negative key handling in hashing or sorting algorithms
- **EVALUATION_PROTOCOL:**
  1. **Asymptotic Complexity**: Explicitly state Big-O Time Complexity and Space Complexity.
  2. **Boundary Testing**:
     - Empty collection / array size 0
     - Single element ($N=1$)
     - Duplicate elements
     - Negative numbers and zero
     - Extreme integer boundaries (`INT_MAX`, `INT_MIN`)
     - Sorted vs reverse-sorted arrays
  3. **Optimization Advisory**: Flag suboptimal implementations and provide the optimal algorithm as a labeled alternative without altering user intent unless requested.
