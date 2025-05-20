import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from matplotlib.font_manager import FontProperties

# 设置中文字体（微软雅黑）
font = FontProperties(fname=r"C:\Windows\Fonts\msyh.ttc", size=12)


def load_all_class_data(folder_path):
    """加载 SubmitRecord-Class1~15.csv 数据并合并"""
    all_df = []
    for i in range(1, 16):
        file_path = os.path.join(folder_path, f'SubmitRecord-Class{i}.csv')
        if os.path.exists(file_path):
            temp_df = pd.read_csv(file_path)
            temp_df['class'] = f'Class{i}'
            all_df.append(temp_df)
        else:
            print(f"警告：未找到 {file_path}")
    return pd.concat(all_df, ignore_index=True)


def process_time(df):
    """处理时间戳为 datetime 和小时"""
    df['datetime'] = pd.to_datetime(df['time'], unit='s')
    df['hour'] = df['datetime'].dt.hour
    df['dayofweek'] = df['datetime'].dt.dayofweek  # 0=Monday, ..., 6=Sunday
    df['is_weekend'] = df['dayofweek'] >= 5
    return df


def plot_hourly_for_student(df, student_id, save_dir='student_plots'):
    """生成指定学生的答题高峰时段柱状图"""
    os.makedirs(save_dir, exist_ok=True)

    student_df = df[df['student_ID'] == student_id]
    if student_df.empty:
        print(f"未找到学生ID {student_id} 的数据！")
        return

    # 统计各小时答题数量，并确保 0-23 全部显示
    hourly_counts = student_df['hour'].value_counts().reindex(range(24), fill_value=0)

    plt.figure(figsize=(10, 5))
    sns.barplot(x=hourly_counts.index, y=hourly_counts.values, palette='viridis')
    plt.xlabel('小时（Hour of Day）', fontproperties=font)
    plt.ylabel('答题次数（Submissions）', fontproperties=font)
    plt.title(f'学习者 {student_id} 的答题高峰时段', fontproperties=font)
    plt.xticks(range(0, 24), fontproperties=font)
    plt.yticks(fontproperties=font)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()

    # 显示图形
    plt.show()

def main():
    data_folder = '../../src/Data_SubmitRecord'

    print("加载数据中...")
    df_all = load_all_class_data(data_folder)

    print("转换时间戳...")
    df_all = process_time(df_all)

    # ✅ 直接指定一个学生ID
    student_id = '8b6d1125760bd3939b6e'

    plot_hourly_for_student(df_all, student_id)


if __name__ == '__main__':
    main()
