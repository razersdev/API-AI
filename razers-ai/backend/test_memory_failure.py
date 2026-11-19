import main

# ==========================================
# SIMULATE MEMORY RETRIEVAL FAILURE
# ==========================================

original_retrieve = main.retrieve_memories


def simulate_failure(*args, **kwargs):
    raise Exception("Simulated memory database failure")


main.retrieve_memories = simulate_failure

print("Simulating memory retrieval failure...")


# ==========================================
# TEST FAILURE HANDLING
# ==========================================

context = main.build_memory_context(
    "Test failure handling"
)

assert context == ""

print("MEMORY FAILURE HANDLING: PASS")
print("Application survived retrieval failure.")
print("Memory context fallback: EMPTY")


# ==========================================
# RESTORE ORIGINAL FUNCTION
# ==========================================

main.retrieve_memories = original_retrieve

print("TEST CLEANUP: SUCCESS")