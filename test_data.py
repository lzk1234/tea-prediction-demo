import pandas as pd
import numpy as np

data = {
    'date': pd.date_range(start='2025-02-10', periods=90, freq='D'),
    'sales': np.random.uniform(50, 120, 90) + np.sin(np.arange(90) / 7) * 20
}
df = pd.DataFrame(data)
df['sales'] = df['sales'].round(2)

print('数据加载测试:')
print(f'数据条数: {len(df)}')
print(f'平均日销量: {df["sales"].mean():.2f}')
print(f'前5行数据:')
print(df.head())
