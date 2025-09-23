#!/usr/bin/env python3

# Quick test to verify the LocalModelRegistry singleton behavior
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dataflow.ml_logic.registry.local_registry import LocalModelRegistry

# Test that singleton works
registry1 = LocalModelRegistry()
registry2 = LocalModelRegistry()

print(f"Registry 1 ID: {id(registry1)}")
print(f"Registry 2 ID: {id(registry2)}")
print(f"Are they the same instance? {registry1 is registry2}")

# Test that ABC methods are properly implemented
print(f"Available methods: {[method for method in dir(registry1) if not method.startswith('_')]}")
