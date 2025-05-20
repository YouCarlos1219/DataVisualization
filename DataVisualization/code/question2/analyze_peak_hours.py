import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from matplotlib.font_manager import FontProperties

# 设置中文字体（微软雅黑）
font = FontProperties(fname=r"C:\Windows\Fonts\msyh.ttc", size=12)

def find_student_class(folder_path, student_id):
    """查找学生所在班级，返回班级编号（1~15），找不到返回None"""
    for i in range(1, 16):
        file_path = os.path.join(folder_path, f'SubmitRecord-Class{i}.csv')
        if os.path.exists(file_path):
            try:
                df = pd.read_csv(file_path, usecols=['student_ID'])
            except Exception as e:
                print(f"读取文件 {file_path} 出错：{e}")
                continue
            if student_id in df['student_ID'].values:
                return i
    return None

def load_class_data_for_student(folder_path, student_id, class_id):
    """加载指定班级的数据，并筛选出对应学生的答题记录"""
    file_path = os.path.join(folder_path, f'SubmitRecord-Class{class_id}.csv')
    if not os.path.exists(file_path):
        print(f"未找到文件 {file_path}")
        return pd.DataFrame()
    df = pd.read_csv(file_path)
    student_df = df[df['student_ID'] == student_id]
    return student_df

def process_time(df):
    """处理时间戳为 datetime 和小时"""
    df['datetime'] = pd.to_datetime(df['time'], unit='s')
    df['hour'] = df['datetime'].dt.hour
    return df

def plot_hourly_for_student(df, student_id, save_dir='student_plots'):
    """生成指定学生的答题高峰时段柱状图，横轴显示0~23小时完整序列"""
    if df.empty:
        print(f"学生 {student_id} 没有答题数据，无法绘图。")
        return

    os.makedirs(save_dir, exist_ok=True)

    # 补全小时0~23，缺失时填0
    hourly_counts = df['hour'].value_counts().reindex(range(24), fill_value=0).sort_index()

    plt.figure(figsize=(10, 5))
    sns.barplot(x=hourly_counts.index, y=hourly_counts.values, palette='viridis')
    plt.xlabel('小时（Hour of Day）', fontproperties=font)
    plt.ylabel('答题次数（Submissions）', fontproperties=font)
    plt.title(f'学习者 {student_id} 的答题高峰时段', fontproperties=font)
    plt.xticks(range(24), fontproperties=font)
    plt.yticks(fontproperties=font)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()

    plt.show()

    save_path = os.path.join(save_dir, f'{student_id}_hourly_submission.png')
    plt.savefig(save_path)
    plt.close()
    print(f"答题高峰图已保存到: {save_path}")

def main():
    data_folder = '../../src/Data_SubmitRecord'  # 修改为你的数据文件夹路径
    student_id = '8b6d1125760bd3939b6e'  # 修改为你想查询的学生ID .


    print(f"正在查找学生 {student_id} 所在班级...")
    class_id = find_student_class(data_folder, student_id)
    if class_id is None:
        print(f"未找到学生 {student_id} 所在班级数据。请确认学生ID是否正确。")
        return
    print(f"学生 {student_id} 位于班级 Class{class_id}")

    print(f"加载班级 Class{class_id} 数据并筛选学生 {student_id} 的答题记录...")
    df_student = load_class_data_for_student(data_folder, student_id, class_id)
    if df_student.empty:
        print(f"学生 {student_id} 在班级 Class{class_id} 中没有答题记录。")
        return

    print("处理时间戳...")
    df_student = process_time(df_student)

    print("绘制答题高峰时段图...")
    plot_hourly_for_student(df_student, student_id)

if __name__ == '__main__':
    main()
