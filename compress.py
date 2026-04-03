import gzip
import shutil

with open('data/vector_store/simple_db.json', 'rb') as f_in:
    with gzip.open('data/vector_store/simple_db.json.gz', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
