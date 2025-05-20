import pandas as pd
import numpy as np
import glob
import matplotlib.pyplot as plt
import seaborn as sns

# --- 1. 读数据 ---
df_students = pd.read_csv('../../src/Data_StudentInfo.csv')
df_titles = pd.read_csv('../../src/Data_TitleInfo.csv')

file_list = glob.glob('../../src/Data_SubmitRecord/SubmitRecord-Class*.csv')
df_records = pd.concat([pd.read_csv(f) for f in file_list], ignore_index=True)

# --- 2. 预处理 df_records ---

# 时间戳转日期（如果需要）
df_records['date'] = pd.to_datetime(df_records['time'], unit='s').dt.date

# --- 3. 计算每个学生提交次数 ---
total_submissions = df_records.groupby('student_ID').size().reset_index(name='total_submissions')

# --- 4. 学习模式划分：提交次数排序，等人数分三组 ---
total_submissions = total_submissions.sort_values('total_submissions', ascending=False).reset_index(drop=True)
n = len(total_submissions)
size = n // 3

def assign_mode(idx):
    if idx < size:
        return 1  # 提交次数最多的1类
    elif idx < 2 * size:
        return 2
    else:
        return 3

total_submissions['learning_mode'] = total_submissions.index.map(assign_mode)

# --- 5. 计算最后一次答题的通过率作为学习效果 ---

# 对每个学生每个题目，选取最新一次提交记录
df_records_sorted = df_records.sort_values(['student_ID', 'title_ID', 'time'], ascending=[True, True, False])
df_last_submit = df_records_sorted.groupby(['student_ID', 'title_ID']).first().reset_index()

# 判断是否“通过”，假设 'state' 字段包含"完全正确"即通过
df_last_submit['passed'] = df_last_submit['state'].apply(lambda x: 1 if '完全正确' in str(x) else 0)

# 计算每个学生的通过率
pass_rate = df_last_submit.groupby('student_ID')['passed'].mean().reset_index(name='final_pass_rate')

# --- 6. 合并提交次数、学习模式和学习效果 ---
df_analysis = total_submissions.merge(pass_rate, on='student_ID', how='left')

# --- 7. 可视化分析 ---

plt.figure(figsize=(10, 6))
sns.boxplot(x='learning_mode', y='final_pass_rate', data=df_analysis, palette='Set1')
plt.title('不同学习模式的学习效果（最后题目通过率）分布')
plt.xlabel('学习模式（按提交次数划分）')
plt.ylabel('最后题目通过率')
plt.xticks([0, 1, 2], ['1类（提交最多）', '2类（中等）', '3类（最少）'])
plt.show()

plt.figure(figsize=(8, 5))
mode_means = df_analysis.groupby('learning_mode')['final_pass_rate'].mean().reset_index()
sns.barplot(x='learning_mode', y='final_pass_rate', data=mode_means, palette='Set2')
plt.title('不同学习模式的平均学习效果')
plt.xlabel('学习模式（按提交次数划分）')
plt.ylabel('平均最后题目通过率')
plt.xticks([0, 1, 2], ['1类（提交最多）', '2类（中等）', '3类（最少）'])
plt.show()
