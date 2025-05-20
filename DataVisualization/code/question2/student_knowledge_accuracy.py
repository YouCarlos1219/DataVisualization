import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from matplotlib.font_manager import FontProperties

# ---------- 配置区 ----------
data_folder = '../../src/Data_SubmitRecord'
title_info_file = "../../src/Data_TitleInfo.csv"
student_id_to_analyze = "8b6d1125760bd3939b6e"
class_count = 15
font_path = r"C:\Windows\Fonts\msyh.ttc"
font_prop = FontProperties(fname=font_path, size=12)
# -----------------------------

# 加载题目信息
if not os.path.exists(title_info_file):
    print(f"未找到题目信息文件: {title_info_file}")
    exit()
title_df = pd.read_csv(title_info_file)

# 构建 title_ID -> (knowledge, score)
title_info_dict = {
    row["title_ID"]: {"knowledge": row["knowledge"], "score": row["score"]}
    for _, row in title_df.iterrows()
}

# 获取该学生的所有提交记录
all_records = []
for i in range(1, class_count + 1):
    file_path = os.path.join(data_folder, f"SubmitRecord-Class{i}.csv")
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        student_df = df[df["student_ID"] == student_id_to_analyze]
        all_records.append(student_df)

if not all_records:
    print(f"未找到学生 {student_id_to_analyze} 的记录。")
    exit()

all_data = pd.concat(all_records)

# 统计每个知识点的提交总次数和正确次数
correct_count = defaultdict(int)
total_count = defaultdict(int)

for _, row in all_data.iterrows():
    title_id = row["title_ID"]
    student_score = row["score"]

    if title_id not in title_info_dict:
        continue

    knowledge = title_info_dict[title_id]["knowledge"]
    full_score = title_info_dict[title_id]["score"]

    total_count[knowledge] += 1
    if student_score == full_score:
        correct_count[knowledge] += 1

# 构建结果 DataFrame
result = []
for knowledge in total_count:
    total = total_count[knowledge]
    correct = correct_count[knowledge]
    accuracy = correct / total if total > 0 else 0
    result.append({
        "知识点": knowledge,
        "提交次数": total,
        "正确次数": correct,
        "正确率": round(accuracy * 100, 2)
    })

result_df = pd.DataFrame(result).sort_values(by="正确率", ascending=False)
print(f"\n学生 {student_id_to_analyze} 在各知识点的答题正确率：\n")
print(result_df.to_string(index=False))

# ----------- 画雷达图 -----------
labels = result_df["知识点"].tolist()
scores = result_df["正确率"].tolist()

# 添加起点闭环
labels += [labels[0]]
scores += [scores[0]]

angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=True)

fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
ax.plot(angles, scores, 'b-', linewidth=2)
ax.fill(angles, scores, 'skyblue', alpha=0.4)
ax.set_thetagrids(angles * 180 / np.pi, labels, fontproperties=font_prop)
ax.set_title(f"学生 {student_id_to_analyze} 在各知识点的正确率雷达图", fontproperties=font_prop, fontsize=14)
ax.set_ylim(0, 100)  # 百分比范围
ax.grid(True)
plt.tight_layout()
plt.show()
