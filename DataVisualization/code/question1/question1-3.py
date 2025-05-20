import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.font_manager import FontProperties

font = FontProperties(fname=r"C:\Windows\Fonts\msyh.ttc", size=12)

df = pd.read_csv('../../src/weak_points_threshold.csv')

pivot_table = df.pivot(index='student_ID', columns='knowledge_point', values='mastery_index')

print("知识点数量:", len(pivot_table.columns))
print("学生数量:", len(pivot_table.index))

# 缺失值填0（或根据业务需求填其他值）
pivot_table = pivot_table.fillna(0)

plt.figure(figsize=(12,8))
sns.heatmap(pivot_table, cmap='YlGnBu', linewidths=0.5, linecolor='gray',
            cbar_kws={'label': '掌握指数'},
            square=False)

plt.title('学生-知识点掌握指数热力图', fontsize=16, fontproperties=font)
plt.xlabel('知识点', fontsize=14, fontproperties=font)
plt.ylabel('学生ID', fontsize=14, fontproperties=font)

plt.xticks(fontsize=10, rotation=45, ha='right', fontproperties=font)
plt.yticks(fontsize=10, fontproperties=font)

plt.tight_layout()
plt.show()
