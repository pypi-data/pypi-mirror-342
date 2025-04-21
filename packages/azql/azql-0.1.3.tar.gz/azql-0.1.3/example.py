from pathlib import Path

import azql

fp = Path("data")
azql.convert(fp, output_dir="tmp", schema="stage", export=True)
# print(script)
