#!/usr/bin/env python3
"""Simple test script to verify safeguards package can be imported."""

try:
    import safeguards

    print(f"Successfully imported safeguards version {safeguards.__version__}")
    print("Package can be imported correctly.")
except ImportError as e:
    print(f"Error importing safeguards: {e}")
    exit(1)
