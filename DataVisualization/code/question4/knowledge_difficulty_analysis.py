import pandas as pd
import numpy as np
import glob
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm

# --- 1. 读数据 ---
df_students = pd.read_csv('../../src/Data_StudentInfo.csv')
df_titles = pd.read_csv('../../src/Data_TitleInfo.csv')
file_list = glob.glob('../../src/Data_SubmitRecord/SubmitRecord-Class*.csv')
df_records = pd.concat([pd.read_csv(f) for f in file_list], ignore_index=True)

# --- 2. 数据预处理 ---
df_records['date'] = pd.to_datetime(df_records['time'], unit='s').dt.date

# --- 3. 计算每个学生提交次数（不去重，原始提交数） ---
submit_counts = df_records.groupby('student_ID').size().reset_index(name='submit_count')

# --- 4. 按提交次数排序，均分为三类学习模式 ---
submit_counts = submit_counts.sort_values('submit_count', ascending=False).reset_index(drop=True)
total_students = len(submit_counts)
group_size = total_students // 3

def assign_mode(idx):
    if idx < group_size:
        return 1  # 提交次数最多
    elif idx < 2 * group_size:
        return 2
    else:
        return 3

submit_counts['learning_mode'] = submit_counts.index.map(assign_mode)

# --- 5. 计算每个学生的题目通过率 ---
# 通过率 = 通过的题目数 / 提交过的题目数（去重）

# 标记“通过”题目（假设state中含“完全正确”为通过）
df_records['passed'] = df_records['state'].apply(lambda x: 1 if 'Absolutely_Correct' in str(x) else 0)

# 去重后的提交题目列表和对应是否通过（取每个题目最大是否通过）
df_pass = df_records.groupby(['student_ID', 'title_ID'])['passed'].max().reset_index()

# 计算通过题数和提交题目总数
pass_counts = df_pass.groupby('student_ID')['passed'].sum().reset_index(name='pass_count')
total_titles = df_pass.groupby('student_ID').size().reset_index(name='total_titles')

pass_rate = pass_counts.merge(total_titles, on='student_ID')
pass_rate['final_pass_rate'] = pass_rate['pass_count'] / pass_rate['total_titles']

# --- 6. 合并学习模式与通过率 ---
df_analysis = submit_counts.merge(pass_rate[['student_ID', 'final_pass_rate']], on='student_ID', how='left')
df_analysis['final_pass_rate'].fillna(0, inplace=True)

# --- 7. 计算各学习模式的平均通过率 ---
mode_means = df_analysis.groupby('learning_mode')['final_pass_rate'].mean().reset_index()

# --- 8. 绘制柱形图 ---
font_path = r"C:\Windows\Fonts\msyh.ttc"
my_font = fm.FontProperties(fname=font_path)

plt.figure(figsize=(8, 6))
sns.barplot(x='learning_mode', y='final_pass_rate', data=mode_means, palette='Set2')

plt.title('不同学习模式的平均题目通过率', fontproperties=my_font, fontsize=16)
plt.xlabel('学习模式', fontproperties=my_font, fontsize=12)
plt.ylabel('平均题目通过率', fontproperties=my_font, fontsize=12)
plt.xticks([0, 1, 2], ['1类（提交最多）', '2类（中等）', '3类（最少）'], fontproperties=my_font, fontsize=11)

for idx, value in enumerate(mode_means['final_pass_rate']):
    plt.text(idx, value + 0.01, f"{value:.2%}", ha='center', fontproperties=my_font, fontsize=11)

plt.ylim(0, 1.1)
plt.tight_layout()
plt.show()
