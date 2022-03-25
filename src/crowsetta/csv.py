from .generic import annot2csv, csv2annot
from .meta import Meta

meta = Meta(
    name='csv',
    ext='csv',
    from_file=csv2annot,
    to_csv=annot2csv,
)
