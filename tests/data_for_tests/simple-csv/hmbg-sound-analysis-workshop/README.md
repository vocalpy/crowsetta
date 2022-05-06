These files were created from the following dataset:
https://figshare.com/articles/dataset/Wav_and_label_files_used_in_the_workshop/4714387

The following snippet was used to convert the `.txt` files to 
the `simple-csv` format in `crowsetta`:
```python
from pathlib import Path
import pandas as pd

txt_files = sorted(Path('.').glob('*.txt'))
for txt_file in txt_files:
    df = pd.read_csv(txt_file, sep='\t', header=None)
    df.columns = ['onset_s', 'offset_s', 'label']
    csv_file = txt_file.parent / (txt_file.stem + '.csv')
    df.to_csv(csv_file, index=None)
```
