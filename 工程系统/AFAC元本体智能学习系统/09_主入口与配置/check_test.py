import pandas as pd
test = pd.read_csv('./data/A推荐/test.csv')
print('test.csv信息:')
print(f'总行数: {len(test)}')
print(f'非空uid数: {test["uid"].notna().sum()}')
print(f'唯一uid数: {test["uid"].nunique()}')
print('前10行uid:')
print(test['uid'].head(10).tolist())