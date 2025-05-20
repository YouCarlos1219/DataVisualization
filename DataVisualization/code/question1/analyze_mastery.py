import pandas as pd
import os
import glob
from pathlib import Path

def load_submit_data(data_dir):
    all_files = glob.glob(os.path.join(data_dir, "SubmitRecord-Class*.csv"))
    df_list = [pd.read_csv(f, encoding='utf-8') for f in all_files]
    data = pd.concat(df_list, ignore_index=True)
    return data

def merge_knowledge_points(data, mapping_file):
    kp_map = pd.read_csv(mapping_file)
    return data.merge(kp_map, on="title_ID", how="left")

def calculate_mastery(data):
    data['is_pass'] = data['state'].str.lower() == 'pass'

    # 平均得分
    avg_score = data.groupby(['student_ID', 'knowledge_point'])['score'].mean().reset_index()
    # 通过率
    pass_rate = data.groupby(['student_ID', 'knowledge_point'])['is_pass'].mean().reset_index()

    # 合并结果
    result = avg_score.merge(pass_rate, on=['student_ID', 'knowledge_point'])
    result['mastery_index'] = 0.6 * result['score'] + 40 * result['is_pass']  # 加权计算

    return result

def identify_weakness(result, threshold=60):
    # 方法1：掌握指数低于阈值
    weak_points = result[result['mastery_index'] < threshold]

    # 方法2：与平均水平比较
    avg_by_kp = result.groupby('knowledge_point')['mastery_index'].mean().reset_index()
    merged = result.merge(avg_by_kp, on='knowledge_point', suffixes=('', '_avg'))
    merged['gap'] = merged['mastery_index_avg'] - merged['mastery_index']
    gap_weak = merged[merged['gap'] > 15]

    return weak_points, gap_weak

def main():
    data_dir = '../../src/Data_SubmitRecord'

    mapping_file = '../../src/title_to_knowledge.csv'

    print("🔄 加载数据中...")
    data = load_submit_data(data_dir)

    print("🔄 合并知识点映射...")
    data = merge_knowledge_points(data, mapping_file)

    print("📊 计算知识点掌握指数...")
    result = calculate_mastery(data)

    print("⚠️ 识别薄弱知识点...")
    weak_by_threshold, weak_by_gap = identify_weakness(result)

    # 保存结果
    output_dir = '../../src'

    result.to_csv(os.path.join(output_dir, "mastery_result.csv"), index=False)
    weak_by_threshold.to_csv(os.path.join(output_dir, "weak_points_threshold.csv"), index=False)
    weak_by_gap.to_csv(os.path.join(output_dir, "weak_points_gap.csv"), index=False)

    print("✅ 分析完成，结果已保存至 ./src/")

if __name__ == "__main__":
    main()
