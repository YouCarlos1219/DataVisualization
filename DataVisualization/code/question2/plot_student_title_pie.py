import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# ---------- 配置区 ----------
data_folder = '../../src/Data_SubmitRecord'
title_info_file = "../../src/Data_TitleInfo.csv"
student_id_to_plot = "8b6d1125760bd3939b6e"
class_count = 15
font_path = r"C:\Windows\Fonts\msyh.ttc"
font_prop = FontProperties(fname=font_path, size=12)
# -----------------------------

# 加载题目信息表
if not os.path.exists(title_info_file):
    print(f"未找到题目信息文件: {title_info_file}")
    exit()

title_df = pd.read_csv(title_info_file)

# 创建 title_ID -> knowledge 的映射
title_id_to_knowledge = dict(zip(title_df["title_ID"], title_df["knowledge"]))

# 收集该学生的所有提交记录
all_records = []

for i in range(1, class_count + 1):
    file_path = os.path.join(data_folder, f"SubmitRecord-Class{i}.csv")
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        student_records = df[df["student_ID"] == student_id_to_plot]
        all_records.append(student_records)

if not all_records:
    print(f"未找到任何关于学生 {student_id_to_plot} 的记录。")
    exit()

all_data = pd.concat(all_records)

# 获取该学生所有提交的 title_ID 列表
submitted_titles = all_data["title_ID"]

# 映射到知识点，并统计出现次数
knowledge_list = [title_id_to_knowledge.get(tid, "未知知识点") for tid in submitted_titles]
knowledge_series = pd.Series(knowledge_list)
knowledge_counts = knowledge_series.value_counts()

if knowledge_counts.empty:
    print(f"学生 {student_id_to_plot} 没有与知识点对应的题目提交记录。")
    exit()

# 绘图
plt.figure(figsize=(8, 8))
plt.pie(knowledge_counts, labels=knowledge_counts.index, autopct='%1.1f%%', startangle=140,
        textprops={'fontproperties': font_prop})
plt.title(f"学生 {student_id_to_plot} 提交的题目分布（按知识点）", fontproperties=font_prop)
plt.axis('equal')
plt.tight_layout()
plt.show()
