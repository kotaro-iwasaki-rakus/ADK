import gzip
import shutil
from pathlib import Path

source = Path("{hoge}")
output = Path("{hoge}")
output.mkdir(parents=True, exist_ok=True)

for csv_file in source.glob("*.csv"):
    gz_file = output / csv_file.with_suffix(csv_file.suffix + ".gz").name

    with open(csv_file, "rb") as f_in:
        with gzip.open(gz_file, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
    print(f"Compressed: {csv_file.name} → {gz_file.name}")
