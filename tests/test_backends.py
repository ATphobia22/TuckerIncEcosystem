from tuckerinc82.backends import discover_backends, load_backend_registry


def test_backend_registry_contains_major_qml_ecosystems():
    ids = {entry["backend_id"] for entry in load_backend_registry()}
    assert {
        "pennylane",
        "qiskit-machine-learning",
        "torchquantum",
        "cuda-q",
        "cirq",
        "tensorflow-quantum",
        "mitiq",
        "amazon-braket",
        "merlin",
    }.issubset(ids)


def test_backend_discovery_is_import_safe():
    discovered = discover_backends()
    assert discovered
    assert all(isinstance(entry["available"], bool) for entry in discovered)
