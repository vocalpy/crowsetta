"""module for formats."""
import sys
import pkg_resources

current_module = sys.modules[__name__]
for entry_point in pkg_resources.iter_entry_points('crowsetta.format'):
    setattr(current_module, entry_point.name, entry_point.load())
