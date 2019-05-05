"""module for formats."""
import sys
import pkg_resources

_INSTALLED = []
current_module = sys.modules[__name__]
for entry_point in pkg_resources.iter_entry_points('crowsetta.format'):
    setattr(current_module, entry_point.name, entry_point.load())
    _INSTALLED.append(entry_point.name)


def show():
    """shows what vocal annotation formats are currently installed"""
    formats_str = ', '.join([format for format in _INSTALLED])
    print(
        f'installed vocal annotation formats:\n{formats_str}'
    )
