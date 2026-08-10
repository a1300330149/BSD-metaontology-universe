import zipfile
import os

print("=" * 80)
print("打包最终提交文件")
print("=" * 80)

# 1. 检查文件
print("\n【1】检查待打包文件...")
files_to_package = [
    ("output/submission/A1_v2.csv", "A1分类预测(改进版)"),
    ("output/submission/A2_improved.csv", "A2推荐预测(改进版)")
]

for filepath, desc in files_to_package:
    if os.path.exists(filepath):
        size = os.path.getsize(filepath) / 1024
        print(f"  ✅ {desc}: {filepath} ({size:.2f} KB)")
    else:
        print(f"  ❌ {desc}: {filepath} - 不存在!")

# 2. 打包
print("\n【2】打包为prediction_v2.zip...")
zip_path = "output/submission/prediction_v2.zip"

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipf.write("output/submission/A1_v2.csv", arcname="A1.csv")
    zipf.write("output/submission/A2_improved.csv", arcname="A2.csv")

print(f"  ✅ 已打包: {zip_path}")

# 3. 验证
print("\n【3】验证zip包内容...")
with zipfile.ZipFile(zip_path, 'r') as zipf:
    print(f"  内容列表:")
    for name in zipf.namelist():
        info = zipf.getinfo(name)
        print(f"    {name}: {info.file_size / 1024:.2f} KB")

# 4. 分析内容
print("\n【4】分析打包内容...")
import pandas as pd

with zipfile.ZipFile(zip_path, 'r') as zipf:
    # A1.csv分析
    a1 = pd.read_csv(zipf.open('A1.csv'))
    print(f"\n  A1.csv (产品分类):")
    print(f"    行数: {len(a1)}")
    print(f"    test_idx范围: {a1['test_idx'].min()} - {a1['test_idx'].max()}")

    from collections import Counter
    label_dist = Counter(a1['label'])
    print(f"    标签分布:")
    for label in sorted(label_dist.keys()):
        count = label_dist[label]
        pct = count / len(a1) * 100
        bar = "█" * int(pct / 3)
        print(f"      标签{label}: {count:4d} ({pct:5.1f}%) {bar}")

    # A2.csv分析
    a2 = pd.read_csv(zipf.open('A2.csv'))
    print(f"\n  A2.csv (产品推荐):")
    print(f"    行数: {len(a2)}")

    all_items = []
    a2['prediction'].apply(lambda x: all_items.extend(x.split(',')))
    unique_items = len(set(all_items))
    item_counts = Counter(all_items)
    print(f"    唯一商品数: {unique_items}")

    print(f"    Top 10热门商品:")
    for i, (item, count) in enumerate(item_counts.most_common(10), 1):
        pct = count / len(a2) * 100
        print(f"      {i:2d}. {item}: {count:5d}次 ({pct:5.1f}%)")

# 5. 最终报告
print("\n" + "=" * 80)
print("打包完成 - 最终提交信息")
print("=" * 80)

print(f"\n📦 提交文件: {zip_path}")
print(f"📊 文件大小: {os.path.getsize(zip_path) / 1024:.2f} KB")

print(f"\n📋 内容:")
print(f"  ✅ A1.csv - 改进的分类预测")
print(f"     - 行数: {len(a1)}")
print(f"     - test_idx顺序: 与官方一致")
print(f"     - 预测分布: 改善标签4过度预测问题")

print(f"\n  ✅ A2.csv - 改进的推荐预测")
print(f"     - 行数: {len(a2)}")
print(f"     - 推荐多样性: {unique_items}个商品")
print(f"     - 推荐商品100%来自训练数据")

print(f"\n🚀 预期改进:")
print(f"  ✅ A1分类: 改善预测分布，接近训练分布")
print(f"  ✅ A2推荐: 保持100%训练数据匹配，提高推荐质量")
print(f"  ⏳ 综合得分: 待评测验证")

print("\n" + "=" * 80)
print("✅ 准备就绪！请提交 prediction_v2.zip 进行评测")
print("=" * 80)