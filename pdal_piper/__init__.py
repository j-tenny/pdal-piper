from pdal_piper.pdal_piper import *

def _check_for_stub():
    from pathlib import Path
    from pdal import pipeline
    py_path = Path(pipeline.__file__)
    pyi_path = py_path.parent / (py_path.stem + '.pyi')

    if not pyi_path.exists():
        print("Generating PDAL skeletons (first-time setup)...")
        from pdal_piper.skeletons import generate_skeletons
        generate_skeletons()
        print("Done.")

# Auto-generate on first import
_check_for_stub()