# Prompt: Debugging Work

Use this prompt when asking Codex to debug failures.

```text
Debug the Semantix prototype systematically.

First identify the failure layer:
1. Python environment
2. Camera source
3. Model loading
4. Inference tensor shape
5. Output writer
6. Dashboard reader

Use the smallest command that reproduces the problem.
Preserve generated evidence in the explanation, but do not commit generated runs.
```

