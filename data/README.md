# Generated data

This folder is where Week 1 writes the synthetic freight dataset. The files
themselves are gitignored. You generate them locally:

```python
from zoro import data
data.save_all()          # writes CSV + Parquet under data/
```

Do not commit the generated tables. Anyone who clones the repo can rebuild the
same rows from `zoro/data.py` with the same seed.
