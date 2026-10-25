"""
Happy Dussehra Animation - Convenient CLI Launcher
Provides an easy-to-type terminal entrypoint for 'Happy Dussehra Animation.py'.

Usage:
    python happy_dasara.py          # Runs high-fidelity Pygame cinematic engine
    python happy_dasara.py --turtle # Runs vector Turtle/Tkinter fallback engine
"""

import sys
import importlib.util
from pathlib import Path

def main():
    target_script = Path(__file__).parent / "Happy Dussehra Animation.py"
    if not target_script.exists():
        print(f"Error: Could not find main animation script at '{target_script}'")
        sys.exit(1)
    
    spec = importlib.util.spec_from_file_location("__main__", str(target_script))
    module = importlib.util.module_from_spec(spec)
    sys.modules["__main__"] = module
    spec.loader.exec_module(module)

if __name__ == "__main__":
    main()
