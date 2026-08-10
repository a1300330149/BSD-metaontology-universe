"""
A2推荐任务深度优化脚本
- Item2Vec嵌入学习
- 序列建模推荐
- 多策略融合
- 目标: 超越0.76845
"""
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from collections import Counter, defaultdict
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')

SEED = 42
torch.manual_seed(SEED)
np.random.seed(SEED)

# ====================== 加载数据 ======================
print("加载数据...")
train = pd.read_csv('data/A推荐/train.csv')
test = pd.read_csv('data/A推荐/test.csv')
item_df = pd.read_csv('data/A推荐/item.csv')
user_df = pd.read_csv('data/A推荐/user.csv')

print(f"训练集: {len(train)} 用户")
print(f"测试集: {len(test)} 用户")
print(f"商品池: {len(item_df)} 个商品")

# ====================== 数据预处理 ======================
all_items = set(item_df['iid'].tolist())
item_list = list(all_items)
item_to_idx = {item: idx for idx, item in enumerate(item_list)}
idx_to_item = {idx: item for item, idx in item_to_idx.items()}
num_items = len(item_list)

# 构建用户-商品交互字典
user_history = {}
for _, row in train.iterrows():
    uid = row['uid']
    history_str = row['item_seq_dedup'] if pd.notna(row['item_seq_dedup']) else ''
    history = [item for item in history_str.split(',') if item in all_items]
    user_history[uid] = history

for _, row in test.iterrows():
    uid = row['uid']
    history_str = row['item_seq_dedup'] if pd.notna(row['item_seq_dedup']) else ''
    history = [item for item in history_str.split(',') if item in all_items]
    user_history[uid] = history

# ====================== Item2Vec模型 ======================
class Item2Vec(nn.Module):
    def __init__(self, num_items, embedding_dim=128, window_size=3):
        super().__init__()
        self.target_embeddings = nn.Embedding(num_items, embedding_dim)
        self.context_embeddings = nn.Embedding(num_items, embedding_dim)
        self.window_size = window_size
        nn.init.xavier_uniform_(self.target_embeddings.weight)
        nn.init.xavier_uniform_(self.context_embeddings.weight)
        
    def forward(self, target_idx, context_idx):
        target_emb = self.target_embeddings(target_idx)
        context_emb = self.context_embeddings(context_idx)
        score = torch.sum(target_emb * context_emb, dim=1)
        return score

# 构建训练样本
print("\n构建Item2Vec训练样本...")
sequences = []
for _, row in train.iterrows():
    history_str = row['item_seq_dedup'] if pd.notna(row['item_seq_dedup']) else ''
    history = [item for item in history_str.split(',') if item in all_items]
    if len(history) >= 2:
        sequences.append(history)
    # 添加目标商品
    if row['target_iid'] in all_items:
        sequences.append([row['target_iid']])

print(f"有效序列数: {len(sequences)}")

# 生成训练样本
train_samples = []
window_size = 3
for seq in sequences:
    seq_len = len(seq)
    for i in range(seq_len):
        target = seq[i]
        if target not in item_to_idx:
            continue
        start = max(0, i - window_size)
        end = min(seq_len, i + window_size + 1)
        for j in range(start, end):
            if i != j and seq[j] in item_to_idx:
                train_samples.append((item_to_idx[target], item_to_idx[seq[j]]))

print(f"训练样本数: {len(train_samples)}")

# 训练Item2Vec
print("\n训练Item2Vec...")
embedding_dim = 128
item2vec = Item2Vec(num_items, embedding_dim=embedding_dim)
optimizer = optim.Adam(item2vec.parameters(), lr=0.001)
criterion = nn.BCEWithLogitsLoss()

batch_size = 1024
num_epochs = 20

for epoch in range(num_epochs):
    np.random.shuffle(train_samples)
    total_loss = 0
    for i in range(0, len(train_samples), batch_size):
        batch = train_samples[i:i+batch_size]
        targets = torch.LongTensor([b[0] for b in batch])
        contexts = torch.LongTensor([b[1] for b in batch])
        
        # 负采样
        neg_contexts = torch.LongTensor(np.random.randint(0, num_items, len(batch)))
        
        optimizer.zero_grad()
        
        pos_score = item2vec(targets, contexts)
        neg_score = item2vec(targets, neg_contexts)
        
        pos_labels = torch.ones(len(batch))
        neg_labels = torch.zeros(len(batch))
        
        loss = criterion(pos_score, pos_labels) + criterion(neg_score, neg_labels)
        loss.backward()
        optimizer.step()
        
        total_loss += loss.item()
    
    if (epoch + 1) % 5 == 0:
        print(f"Epoch {epoch+1}/{num_epochs}: Loss = {total_loss / (len(train_samples) // batch_size):.4f}")

# 获取商品嵌入
item_embeddings = item2vec.target_embeddings.weight.detach().numpy()

# ====================== 序列推荐模型 ======================
class SeqRecommender(nn.Module):
    def __init__(self, num_items, embedding_dim=128, hidden_dim=256):
        super().__init__()
        self.item_embeddings = nn.Embedding(num_items, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, num_layers=2, batch_first=True, dropout=0.3)
        self.classifier = nn.Linear(hidden_dim, num_items)
        
    def forward(self, seq):
        emb = self.item_embeddings(seq)
        _, (hidden, _) = self.lstm(emb)
        out = self.classifier(hidden[-1])
        return out

# 准备序列推荐训练数据
print("\n准备序列推荐训练数据...")
seq_train_data = []
for _, row in train.iterrows():
    uid = row['uid']
    history_str = row['item_seq_dedup'] if pd.notna(row['item_seq_dedup']) else ''
    history = [item for item in history_str.split(',') if item in item_to_idx]
    target = row['target_iid']
    if len(history) >= 1 and target in item_to_idx:
        seq_train_data.append((history, target))

print(f"序列训练样本: {len(seq_train_data)}")

# 训练序列推荐模型
seq_model = SeqRecommender(num_items, embedding_dim=embedding_dim)
optimizer = optim.Adam(seq_model.parameters(), lr=0.001)
criterion = nn.CrossEntropyLoss()

num_epochs = 10
batch_size = 64

for epoch in range(num_epochs):
    np.random.shuffle(seq_train_data)
    total_loss = 0
    for i in range(0, len(seq_train_data), batch_size):
        batch = seq_train_data[i:i+batch_size]
        max_len = max(len(h) for h, _ in batch)
        seqs = []
        targets = []
        for history, target in batch:
            padded = [item_to_idx[h] for h in history] + [0] * (max_len - len(history))
            seqs.append(padded)
            targets.append(item_to_idx[target])
        
        seqs = torch.LongTensor(seqs)
        targets = torch.LongTensor(targets)
        
        optimizer.zero_grad()
        out = seq_model(seqs)
        loss = criterion(out, targets)
        loss.backward()
        optimizer.step()
        
        total_loss += loss.item()
    
    if (epoch + 1) % 5 == 0:
        print(f"SeqRec Epoch {epoch+1}/{num_epochs}: Loss = {total_loss / (len(seq_train_data) // batch_size):.4f}")

# ====================== 热门商品统计 ======================
print("\n分析热门商品...")
train_items = train['target_iid'].tolist()
item_counts = Counter(train_items)
popular_items = [item for item, _ in item_counts.most_common(500)]

# ====================== 多策略融合推荐 ======================
print("\n生成多策略融合推荐...")

def recommend(uid, history, top_k=10):
    history_set = set(history)
    
    scores = np.zeros(num_items)
    
    # 策略1: Item2Vec相似度推荐 (权重0.35)
    if len(history) > 0:
        hist_embs = item_embeddings[[item_to_idx[item] for item in history if item in item_to_idx]]
        mean_hist_emb = hist_embs.mean(axis=0, keepdims=True)
        sim_scores = cosine_similarity(mean_hist_emb, item_embeddings)[0]
        for i, sim in enumerate(sim_scores):
            scores[i] += sim * 0.35
    
    # 策略2: 序列推荐 (权重0.35)
    if len(history) > 0:
        try:
            seq_indices = torch.LongTensor([[item_to_idx[item] for item in history if item in item_to_idx]])
            seq_out = seq_model(seq_indices).detach().numpy()[0]
            seq_scores = torch.sigmoid(torch.FloatTensor(seq_out)).numpy()
            scores += seq_scores * 0.35
        except:
            pass
    
    # 策略3: 热门商品 (权重0.2)
    for item in popular_items[:200]:
        if item in item_to_idx:
            scores[item_to_idx[item]] += (1 / (popular_items.index(item) + 1)) * 0.2
    
    # 策略4: 训练数据协同过滤 (权重0.1)
    if len(history) > 0:
        related_items = []
        for hist_item in history[:3]:
            similar_users = train[train['target_iid'] == hist_item]['uid'].tolist()[:100]
            related = train[train['uid'].isin(similar_users)]['target_iid'].tolist()
            related_items.extend(related)
        
        rel_counts = Counter(related_items)
        for item, count in rel_counts.items():
            if item in item_to_idx:
                scores[item_to_idx[item]] += count * 0.01
    
    # 过滤历史商品
    for item in history:
        if item in item_to_idx:
            scores[item_to_idx[item]] = -1
    
    # 获取Top-K
    top_indices = np.argsort(scores)[::-1][:top_k]
    recommendations = [idx_to_item[idx] for idx in top_indices]
    
    return recommendations

# 生成测试集推荐
predictions = []
for _, row in test.iterrows():
    uid = row['uid']
    history_str = row['item_seq_dedup'] if pd.notna(row['item_seq_dedup']) else ''
    history = [item for item in history_str.split(',') if item in all_items]
    recs = recommend(uid, history, top_k=10)
    predictions.append(','.join(recs))

# 保存结果
a2_result = pd.DataFrame({
    'uid': test['uid'],
    'prediction': predictions
})

# 格式修正：确保prediction字段加引号
output_lines = ['uid,prediction']
for _, row in a2_result.iterrows():
    output_lines.append(f'{row["uid"]},"{row["prediction"]}"')

output_path = 'output/submission/A2_deep.csv'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines) + '\n')

print(f"\n✓ 已保存 A2_deep.csv")
print(f"  - 推荐策略: Item2Vec(35%) + SeqRec(35%) + 热门(20%) + 协同过滤(10%)")
print(f"  - 目标: 超越0.76845")

# 分析推荐结果
all_rec_items = []
for pred in predictions:
    all_rec_items.extend(pred.split(','))
unique_items = len(set(all_rec_items))
print(f"\n推荐多样性分析:")
print(f"  推荐不同商品数: {unique_items}")
print(f"  商品覆盖率: {unique_items / len(item_df) * 100:.1f}%")