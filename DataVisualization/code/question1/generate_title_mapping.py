import pandas as pd

def generate_title_to_knowledge(input_path, output_path):
    # 读取题目信息
    df = pd.read_csv(input_path, encoding='utf-8')

    # 提取 title_ID 和 knowledge 列，并去重
    title_kp = df[['title_ID', 'knowledge']].drop_duplicates()

    # 重命名为标准列名
    title_kp.columns = ['title_ID', 'knowledge_point']

    # 保存为 CSV
    title_kp.to_csv(output_path, index=False, encoding='utf-8')
    print(f"✅ 成功生成知识点映射文件：{output_path}")

if __name__ == "__main__":
    input_csv = '../../src/Data_TitleInfo.csv'
    output_csv = '../../src/title_to_knowledge.csv'
    generate_title_to_knowledge(input_csv, output_csv)
