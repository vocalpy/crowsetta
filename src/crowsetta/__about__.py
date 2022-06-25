import os.path

__all__ = [
    "__title__",
    "__summary__",
    "__uri__",
    "__version__",
    "__commit__",
    "__author__",
    "__email__",
    "__license__",
    "__copyright__",
]


try:
    base_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    base_dir = None


__title__ = "crowsetta"
__summary__ = "A Python tool to work with any format for annotating animal vocalizations and bioacoustics data"
__uri__ = "https://github.com/vocalpy/crowsetta"

__version__ = "4.0.0.post1"

if base_dir is not None and os.path.exists(os.path.join(base_dir, ".commit")):
    with open(os.path.join(base_dir, ".commit")) as fp:
        __commit__ = fp.read().strip()
else:
    __commit__ = None

__author__ = "David Nicholson"
__email__ = "nicholdav@gmail.com"

__license__ = "BSD"
__copyright__ = "2019-present %s" % __author__
