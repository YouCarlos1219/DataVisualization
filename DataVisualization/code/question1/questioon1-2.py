import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.font_manager import FontProperties

# 设置中文字体
font = FontProperties(fname=r"C:\Windows\Fonts\msyh.ttc", size=12)

# 读取数据
df = pd.read_csv('../../src/weak_points_threshold.csv')

# 选择一个学生ID（示例）
student_id = '8b6d1125760bd3939b6e'  # 请改成你数据里的实际学生ID字符串或数字

# 筛选该学生的数据并排序
df_student = df[df['student_ID'] == student_id].sort_values('mastery_index')

plt.figure(figsize=(10,5))
sns.barplot(data=df_student, y='knowledge_point', x='mastery_index', palette='coolwarm')

plt.xlabel('掌握指数', fontsize=12, fontproperties=font)
plt.ylabel('知识点名称', fontsize=12, fontproperties=font)
plt.title(f'学生 {student_id} 薄弱知识点掌握情况', fontsize=14, fontproperties=font)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10, fontproperties=font)

plt.tight_layout()
plt.show()
