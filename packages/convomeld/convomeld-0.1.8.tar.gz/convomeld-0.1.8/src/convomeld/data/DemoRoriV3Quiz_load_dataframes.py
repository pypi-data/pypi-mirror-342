ls /home/hobs/code/tangibleai/community/convomeld/data/
p = '/home/hobs/code/tangibleai/community/convomeld/data/DemoRoriV3Quiz.xlsx'
from pathlib import Path
p = Path(p)
import pandas as pd
dfs = pd.read_excel(p)
pip install openpyxl
dfs = pd.read_excel(p)
len(dfs)
dfs[0]
dfs
dfs = pd.read_excel?
for i in range(1000);
dfs = []
for i in range(1000):
    try:
        df = pd.read_excel(p, i)
    except:
        break
    dfs.append(df)
from tqdm import tqdm
dfs = []
for i in tqdm(range(1000)):
    try:
        df = pd.read_excel(p, i)
    except Exception as e:
        print(e)
        break
    dfs.append(df)
import joblib
dfs[0]
xl = pd.ExcelFile(p)
xl.sheet_names
tables = dict(zip(xl.sheet_names, dfs))
joblib.dump?
joblib.dump(tables, p.with_suffix('.joblib').open())
joblib.dump(tables, p.with_suffix('.joblib').open('w'))
joblib.dump(tables, p.with_suffix('.joblib').open('wb'))
ls /home/hobs/code/tangibleai/community/convomeld/data/
dfs = joblib.load(p.with_suffix('.joblib'))
dfs
dfs.keys()
hist -f p.parens / 'DemoRoriV3Quiz_load_dataframes.py'
p
