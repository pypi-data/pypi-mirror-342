#!/usr/bin/env python3
"""
Test script to verify that the modular imports are working correctly.
"""

import os
import sys

# Add the parent directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_module_imports():
    """Test that all modules can be imported successfully."""
    
    print("Testing modular imports...")
    
    # Test the main package
    try:
        import qcmd_cli
        print(f"✓ Main package: qcmd_cli (version {qcmd_cli.__version__})")
    except ImportError as e:
        print(f"❌ Failed to import qcmd_cli: {e}")
        assert False, f"Failed to import qcmd_cli: {e}"
    
    # Test core modules
    try:
        from qcmd_cli.core import command_generator, interactive_shell
        print("✓ Core modules")
    except ImportError as e:
        print(f"❌ Failed to import core modules: {e}")
        assert False, f"Failed to import core modules: {e}"
    
    # Test utility modules
    try:
        from qcmd_cli.utils import history, session, system
        print("✓ Utility modules")
    except ImportError as e:
        print(f"❌ Failed to import utility modules: {e}")
        assert False, f"Failed to import utility modules: {e}"
    
    # Test log analysis modules
    try:
        from qcmd_cli.log_analysis import analyzer, log_files, monitor
        print("✓ Log analysis modules")
    except ImportError as e:
        print(f"❌ Failed to import log analysis modules: {e}")
        assert False, f"Failed to import log analysis modules: {e}"
    
    # Test UI modules
    try:
        from qcmd_cli.ui import display
        print("✓ UI modules")
    except ImportError as e:
        print(f"❌ Failed to import UI modules: {e}")
        assert False, f"Failed to import UI modules: {e}"
    
    # Test config modules
    try:
        from qcmd_cli.config import settings
        print("✓ Configuration modules")
    except ImportError as e:
        print(f"❌ Failed to import configuration modules: {e}")
        assert False, f"Failed to import configuration modules: {e}"
    
    # Test command modules
    try:
        from qcmd_cli.commands import handler
        print("✓ Command modules")
    except ImportError as e:
        print(f"❌ Failed to import command modules: {e}")
        assert False, f"Failed to import command modules: {e}"
    
    # Import main entry point
    try:
        from qcmd_cli.commands.handler import main
        print("✓ Main entry point")
    except ImportError as e:
        print(f"❌ Failed to import main entry point: {e}")
        assert False, f"Failed to import main entry point: {e}"
    
    print("\nAll imports successful! The modular structure is working correctly.")
    assert True  # Use assert instead of return

if __name__ == "__main__":
    success = test_module_imports()
    sys.exit(0 if success else 1) 