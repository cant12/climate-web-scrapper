import os
import sys
from tqdm import tqdm
import pandas as pd
from custom_driver import download_pdf

'''
use as python download.py ./data/agu -1 > download_agu.log & 
'''

root_dir = sys.argv[1]
df = pd.read_csv(root_dir.split('/')[-1] + '.csv')
checkpoint = -1

if len(sys.argv) > 2:
    checkpoint = int(sys.argv[2])

def get_dir(df, i):
    dir = root_dir
    for column in df.columns[1:-2]:
        dir = os.path.join(dir, df[column][i])
    return dir

arg_list = []
for i in range(len(df)):
    dir = get_dir(df, i)
    if not os.path.exists(dir):
        os.makedirs(dir)
    arg_list.append((df['PDF Link'][i], dir))

count = 0
for url, dir in tqdm(arg_list, file=sys.stdout):
    if count > checkpoint:
        download_pdf(url, dir)
    count += 1