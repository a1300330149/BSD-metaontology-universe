#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BSD 围棋引擎×基因引擎 双引擎协同突破1001
==========================================

核心思想:
  1. 围棋引擎: 像下棋一样系统化穷举所有可能的参数组合
  2. 基因引擎: 从成功/失败请求中提取基因特征，完成相似组合

突破策略:
  Phase 1: 围棋穷举 — 系统搜索正确的messages格式
  Phase 2: 基因提取 — 从请求/响应中提取关键特征
  Phase 3: 基因重组 — 基于成功特征构造新的请求
  Phase 4: 协同进化 — 两引擎协同迭代突破
"""

import os, sys, json, time, hashlib, ssl, itertools
import urllib.request, urllib.error
from datetime import datetime
from collections import defaultdict, Counter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE

sys.path.insert(0, BASE_DIR)
from BSD_AHADecryptor import decrypt_aha

# ============================================================================
# 配置
# ============================================================================
TRAE_STORAGE = r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\storage.json'
IDE_VERSION = '2.3.62837'
API_HOST = 'trae-api-cn.mchost.guru'
AUTH_HOST = 'api.trae.cn'
USER_ID = '3753060170739075'
DEVICE_ID = '136411536168449'
CLIENT_ID = 'ono9krqynydwx5'

def load_credentials():
    with open(TRAE_STORAGE, 'r', encoding='utf-8') as f:
        storage = json.load(f)
    cloudide_enc = storage.get('iCubeAuthInfo://icube.cloudide', '')
    if cloudide_enc:
        try:
            dec = decrypt_aha(cloudide_enc)
            data = json.loads(dec.decode('utf-8'))
            return {
                'jwt_token': data.get('token', ''),
                'userId': data.get('userId', ''),
                'refreshToken': data.get('refreshToken', ''),
            }
        except Exception as e:
            print(f'  ⚠️ cloudide解密失败: {e}')
    return {}

# ============================================================================
# 围棋引擎: 穷举搜索器
# ============================================================================
class GoEngineSearcher:
    """围棋引擎穷举搜索器
    
    模拟围棋对弈的搜索策略:
    1. 广度优先搜索所有可能的参数组合
    2. 评估每个组合的"胜率"(是否突破1001)
    3. 基于评估结果进行深度搜索
    """
    
    def __init__(self, jwt):
        self.jwt = jwt
        self.search_tree = {}  # 搜索树
        self.evaluated_combos = []  # 已评估的组合
        self.best_result = None  # 最佳结果
        self.gene_pool = defaultdict(list)  # 基因池
        
    def _make_request(self, body, extra_headers=None):
        """发送请求"""
        url = f'https://{API_HOST}/api/ide/v2/llm_raw_chat'
        headers = {
            'Authorization': f'Bearer {self.jwt}',
            'Cloud-IDE-JWT': self.jwt,
            'x-cloudide-token': self.jwt,
            'Content-Type': 'application/json',
            'User-Agent': f'TraeCN/{IDE_VERSION} (Windows; x64)',
            'X-Device-ID': DEVICE_ID,
            'X-Client-ID': CLIENT_ID,
            'Origin': 'https://trae.cn',
            'Referer': 'https://trae.cn/chat',
        }
        if extra_headers:
            headers.update(extra_headers)
        
        try:
            body_bytes = json.dumps(body).encode('utf-8')
            req = urllib.request.Request(url, data=body_bytes, headers=headers, method='POST')
            with urllib.request.urlopen(req, timeout=10, context=SSL_CTX) as resp:
                return {
                    'status': resp.status,
                    'body': resp.read().decode('utf-8', errors='replace'),
                    'headers': dict(resp.headers),
                }
        except urllib.error.HTTPError as e:
            return {
                'status': e.code,
                'body': e.read().decode('utf-8', errors='replace'),
                'headers': dict(e.headers) if hasattr(e, 'headers') else {},
            }
        except Exception as e:
            return {'status': 0, 'body': str(e), 'headers': {}}
    
    def evaluate_combo(self, body_combo):
        """评估一个参数组合"""
        response = self._make_request(body_combo)
        
        status = response['status']
        body = response['body']
        is_1001 = '1001' in body
        body_length = len(body)
        
        # 评分系统 (类似围棋评估)
        score = 0
        breakthrough = False
        
        if status == 200 and not is_1001:
            score = 100  # 完美突破
            breakthrough = True
        elif status == 200 and is_1001:
            score = 10   # 被1001拦截
        elif status == 400 and not is_1001:
            score = 50   # 绕过1001但参数错误
            if body_length > 0:
                score = 60  # 有响应体更接近成功
        elif status == 404:
            score = 0    # 路径不存在
        else:
            score = 5    # 其他情况
        
        result = {
            'combo': body_combo,
            'status': status,
            'score': score,
            'breakthrough': breakthrough,
            'response': body[:200],
            'response_length': body_length,
            'is_1001': is_1001,
        }
        
        self.evaluated_combos.append(result)
        
        # 更新最佳结果
        if self.best_result is None or score > self.best_result['score']:
            self.best_result = result
        
        # 提取基因特征
        self._extract_genes(body_combo, result)
        
        return result
    
    def _extract_genes(self, body_combo, result):
        """从请求/响应中提取基因特征"""
        gene_features = {
            'body_keys': sorted(body_combo.keys()),
            'status': result['status'],
            'score': result['score'],
            'breakthrough': result['breakthrough'],
            'has_messages': 'messages' in body_combo,
            'has_query': 'query' in body_combo,
            'has_conversation_id': 'conversation_id' in body_combo,
            'has_user_id': 'user_id' in body_combo or 'user_id' in str(body_combo),
            'response_length': result['response_length'],
            'is_1001': result['is_1001'],
        }
        
        # 根据评分分类存储
        score_level = 'breakthrough' if result['breakthrough'] else \
                      'high_score' if result['score'] >= 50 else \
                      'medium_score' if result['score'] >= 10 else 'low_score'
        
        self.gene_pool[score_level].append(gene_features)
    
    def systematic_search(self):
        """系统性穷举搜索 (Phase 1)"""
        print('\n' + '='*70)
        print('  Phase 1: 围棋穷举 — 系统化参数搜索')
        print('='*70)
        
        # 定义搜索空间
        # 类似围棋的"布局-中盘-官子"搜索策略
        
        search_space = {
            'message_formats': [
                # 不同的messages格式
                {'messages': [{'role': 'user', 'content': '你好'}]},
                {'messages': [{'role': 'system', 'content': 'You are helpful.'}, {'role': 'user', 'content': '你好'}]},
                {'messages': [{'role': 'user', 'content': '你好', 'content_type': 'text'}]},
                {'messages': [{'role': 'user', 'content': '你好', 'type': 'text'}]},
            ],
            'additional_fields': [
                {},  # 无额外字段
                {'stream': False},
                {'stream': False, 'conversation_id': 'test_001'},
                {'stream': False, 'conversation_id': 'test_001', 'user_id': USER_ID},
                {'stream': False, 'session_id': 'test_session_001'},
                {'stream': False, 'format': 'chat'},
                {'stream': False, 'client_type': 'trae_ide'},
                {'stream': False, 'client_type': 'trae_ide', 'version': IDE_VERSION},
                {'stream': True},
            ],
            'model_specs': [
                {'model': 'doubao-pro-32k'},
                {'model': 'doubao-pro-32k', 'temperature': 0.7},
                {'model': 'doubao-pro-32k', 'max_tokens': 100},
                {'model': 'doubao-pro-32k', 'top_p': 0.9},
                {'model': 'doubao-pro-32k', 'temperature': 0.7, 'max_tokens': 100},
            ],
        }
        
        # 生成所有组合
        print('\n  搜索空间:')
        print(f'    消息格式: {len(search_space["message_formats"])} 种')
        print(f'    额外字段: {len(search_space["additional_fields"])} 种')
        print(f'    模型参数: {len(search_space["model_specs"])} 种')
        
        all_combos = []
        for msg_fmt in search_space['message_formats']:
            for addl in search_space['additional_fields']:
                for model in search_space['model_specs']:
                    combo = {}
                    combo.update(msg_fmt)
                    combo.update(addl)
                    combo.update(model)
                    all_combos.append(combo)
        
        print(f'    总组合数: {len(all_combos)}')
        print('\n  开始搜索...\n')
        
        # 执行搜索
        for i, combo in enumerate(all_combos):
            result = self.evaluate_combo(combo)
            
            progress = (i + 1) / len(all_combos) * 100
            status_icon = '🎯' if result['breakthrough'] else '⚠️' if result['score'] >= 50 else '🔑'
            
            if i % 10 == 0 or result['score'] >= 50:
                print(f'    [{i+1}/{len(all_combos)}] {status_icon} HTTP {result["status"]} | Score={result["score"]} | 1001={result["is_1001"]}')
                if result['response'][:100]:
                    print(f'         响应: {result["response"][:100]}')
            
            # 成功突破则停止
            if result['breakthrough']:
                print(f'\n    🎉 找到突破点!')
                return result
        
        print(f'\n  Phase 1 完成')
        print(f'    评估组合: {len(self.evaluated_combos)}')
        print(f'    最佳分数: {self.best_result["score"] if self.best_result else 0}')
        
        return self.best_result
    
    def deep_search(self, base_combo):
        """深度搜索 (Phase 2) — 基于最佳结果进行局部搜索"""
        print('\n' + '='*70)
        print('  Phase 2: 围棋深度搜索 — 局部优化')
        print('='*70)
        
        if not base_combo:
            print('  无基础组合，跳过深度搜索')
            return None
        
        # 基于base_combo进行微调
        variants = []
        
        # 变体1: 修改content
        contents = ['你好', 'Hello', 'test', '测试', 'hi', '您好']
        for content in contents:
            variant = json.loads(json.dumps(base_combo))  # 深拷贝
            if 'messages' in variant:
                variant['messages'][0]['content'] = content
            variants.append(variant)
        
        # 变体2: 添加不同的system消息
        system_prompts = [
            'You are a helpful assistant.',
            '你是一个有用的助手。',
            'You are Trae AI assistant.',
            'Trae CN AI Assistant',
            'Default system prompt',
        ]
        for sys_prompt in system_prompts:
            variant = json.loads(json.dumps(base_combo))
            if 'messages' in variant and len(variant['messages']) > 0:
                variant['messages'].insert(0, {'role': 'system', 'content': sys_prompt})
            variants.append(variant)
        
        # 变体3: 修改stream参数
        for stream_val in [True, False]:
            variant = json.loads(json.dumps(base_combo))
            variant['stream'] = stream_val
            variants.append(variant)
        
        # 变体4: 添加随机ID
        for _ in range(5):
            variant = json.loads(json.dumps(base_combo))
            variant['conversation_id'] = hashlib.sha256(f'id{time.time()}{_}'.encode()).hexdigest()[:16]
            variants.append(variant)
        
        print(f'\n  生成变体: {len(variants)} 个')
        print('  开始深度搜索...\n')
        
        best = base_combo
        best_score = self.best_result['score'] if self.best_result else 0
        
        for i, variant in enumerate(variants):
            result = self.evaluate_combo(variant)
            
            if result['score'] > best_score:
                best_score = result['score']
                best = variant
                print(f'    [{i+1}] 🏆 新最佳: Score={result["score"]}')
            
            if result['breakthrough']:
                print(f'\n    🎉 深度搜索突破成功!')
                return result
        
        print(f'\n  Phase 2 完成')
        print(f'    最佳分数: {best_score}')
        return best


# ============================================================================
# 基因引擎: 特征提取器
# ============================================================================
class GeneEngineExtractor:
    """基因引擎特征提取器
    
    从请求/响应中提取"基因"特征:
    1. 结构基因: 请求体的键结构
    2. 数值基因: 参数的值特征
    3. 响应基因: 服务端响应特征
    4. 突破基因: 与突破相关的关键特征
    """
    
    def __init__(self):
        self.gene_library = {
            'structure_genes': [],  # 结构基因
            'value_genes': [],      # 数值基因
            'response_genes': [],   # 响应基因
            'breakthrough_genes': [],  # 突破基因
        }
    
    def extract_structure_genes(self, combo):
        """提取结构基因 — 请求体的键结构"""
        genes = []
        
        # 顶层键
        top_keys = sorted(combo.keys())
        genes.append(f'top_keys:{",".join(top_keys)}')
        
        # messages结构
        if 'messages' in combo:
            msgs = combo['messages']
            for i, msg in enumerate(msgs):
                if isinstance(msg, dict):
                    msg_keys = sorted(msg.keys())
                    genes.append(f'msg_{i}_keys:{",".join(msg_keys)}')
                    if 'role' in msg:
                        genes.append(f'msg_{i}_role:{msg["role"]}')
                    if 'content' in msg:
                        content_len = len(str(msg['content']))
                        genes.append(f'msg_{i}_content_len:{content_len}')
        
        return genes
    
    def extract_value_genes(self, combo):
        """提取数值基因 — 参数的值特征"""
        genes = []
        
        for key, value in combo.items():
            if isinstance(value, str):
                genes.append(f'{key}_str_len:{len(value)}')
                genes.append(f'{key}_str_type:{type(value).__name__}')
            elif isinstance(value, bool):
                genes.append(f'{key}_bool:{value}')
            elif isinstance(value, (int, float)):
                genes.append(f'{key}_num:{value}')
            elif isinstance(value, list):
                genes.append(f'{key}_list_len:{len(value)}')
            elif isinstance(value, dict):
                genes.append(f'{key}_dict_keys:{len(value)}')
        
        return genes
    
    def extract_response_genes(self, response_info):
        """提取响应基因 — 服务端响应特征"""
        genes = []
        
        status = response_info.get('status', 0)
        body = response_info.get('body', '')
        headers = response_info.get('headers', {})
        
        # 状态码基因
        genes.append(f'status:{status}')
        genes.append(f'is_1001:{"1001" in body}')
        genes.append(f'body_len:{len(body)}')
        
        # 响应头基因
        if 'server' in headers:
            genes.append(f'server:{headers["server"]}')
        if 'x-tt-logid' in headers:
            genes.append(f'has_logid:True')
        if 'eagleid' in headers:
            genes.append(f'has_eagleid:True')
        
        # 响应体类型
        if body:
            if body.startswith('event:'):
                genes.append('response_type:SSE')
            elif body.startswith('{'):
                genes.append('response_type:JSON')
            elif body.startswith('<'):
                genes.append('response_type:HTML')
            else:
                genes.append('response_type:unknown')
        
        return genes
    
    def extract_breakthrough_genes(self, results):
        """提取突破基因 — 与突破相关的关键特征组合"""
        breakthrough_genes = []
        
        # 分析所有结果，找出高分组合的共同特征
        high_score_combos = [r for r in results if r.get('score', 0) >= 50]
        low_score_combos = [r for r in results if r.get('score', 0) < 50]
        
        if high_score_combos:
            # 提取高分组合的共同结构基因
            high_structures = []
            for combo in high_score_combos:
                if isinstance(combo.get('combo'), dict):
                    structure = tuple(sorted(combo['combo'].keys()))
                    high_structures.append(structure)
            
            # 找出最常见的结构
            if high_structures:
                counter = Counter(high_structures)
                most_common = counter.most_common(3)
                for structure, count in most_common:
                    breakthrough_genes.append({
                        'type': 'common_structure',
                        'structure': list(structure),
                        'frequency': count / len(high_score_combos),
                        'score_range': 'high',
                    })
        
        # 找出高分与低分的差异
        if high_score_combos and low_score_combos:
            high_keys = set()
            low_keys = set()
            for c in high_score_combos:
                if isinstance(c.get('combo'), dict):
                    high_keys.update(c['combo'].keys())
            for c in low_score_combos:
                if isinstance(c.get('combo'), dict):
                    low_keys.update(c['combo'].keys())
            
            # 高分特有的键
            unique_high = high_keys - low_keys
            if unique_high:
                breakthrough_genes.append({
                    'type': 'unique_keys_in_high',
                    'keys': list(unique_high),
                    'description': '高分组合特有的键',
                })
            
            # 低分特有的键
            unique_low = low_keys - high_keys
            if unique_low:
                breakthrough_genes.append({
                    'type': 'unique_keys_in_low',
                    'keys': list(unique_low),
                    'description': '低分组合特有的键',
                })
        
        return breakthrough_genes


# ============================================================================
# 双引擎协同器
# ============================================================================
class DualEngineOrchestrator:
    """围棋引擎×基因引擎 双引擎协同器"""
    
    def __init__(self, jwt):
        self.jwt = jwt
        self.go_engine = GoEngineSearcher(jwt)
        self.gene_engine = GeneEngineExtractor()
        self.iteration = 0
        self.best_result = None
    
    def run_coordinated_attack(self):
        """运行协同攻击"""
        print('\n' + '#'*70)
        print('  # 双引擎协同突破1001')
        print('#'*70)
        print(f'  时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        print(f'  引擎: 围棋引擎(穷举) × 基因引擎(提取)')
        print('#'*70)
        
        # Phase 1: 围棋穷举
        best_combo = self.go_engine.systematic_search()
        
        # Phase 2: 基因提取
        print('\n' + '='*70)
        print('  Phase 3: 基因提取 — 分析成功特征')
        print('='*70)
        
        all_results = self.go_engine.evaluated_combos
        if all_results:
            # 提取结构基因
            for result in all_results:
                if isinstance(result.get('combo'), dict):
                    structure_genes = self.gene_engine.extract_structure_genes(result['combo'])
                    self.gene_engine.gene_library['structure_genes'].extend(structure_genes)
            
            # 提取突破基因
            breakthrough_genes = self.gene_engine.extract_breakthrough_genes(all_results)
            self.gene_engine.gene_library['breakthrough_genes'] = breakthrough_genes
            
            print('\n  突破基因分析:')
            for gene in breakthrough_genes:
                print(f'    类型: {gene["type"]}')
                print(f'    详情: {json.dumps(gene, ensure_ascii=False)[:200]}')
                print()
        
        # Phase 3: 基于基因的深度搜索
        if best_combo and isinstance(best_combo.get('combo'), dict):
            improved = self.go_engine.deep_search(best_combo['combo'])
            if improved:
                self.best_result = improved
        
        # 最终结果
        self._generate_final_report()
        
        return self.best_result
    
    def _generate_final_report(self):
        """生成最终报告"""
        print('\n' + '#'*70)
        print('  # 双引擎协同突破报告')
        print('#'*70)
        
        all_results = self.go_engine.evaluated_combos
        if not all_results:
            print('  无实验结果')
            return
        
        # 统计
        status_counts = Counter(r['status'] for r in all_results)
        score_counts = Counter()
        for r in all_results:
            if r['score'] >= 100:
                score_counts['突破'] += 1
            elif r['score'] >= 50:
                score_counts['绕过1001'] += 1
            elif r['score'] >= 10:
                score_counts['被1001拦截'] += 1
            else:
                score_counts['失败'] += 1
        
        print(f'\n  实验统计:')
        print(f'    总实验数: {len(all_results)}')
        print(f'    HTTP状态分布:')
        for status, count in sorted(status_counts.items()):
            print(f'      HTTP {status}: {count}次')
        print(f'    结果分布:')
        for label, count in sorted(score_counts.items(), key=lambda x: x[0], reverse=True):
            print(f'      {label}: {count}次')
        
        # 最佳结果
        best = self.go_engine.best_result
        if best:
            print(f'\n  最佳结果:')
            print(f'    分数: {best["score"]}')
            print(f'    HTTP状态: {best["status"]}')
            print(f'    绕过1001: {not best["is_1001"]}')
            print(f'    突破成功: {best["breakthrough"]}')
            print(f'    参数组合: {json.dumps(best["combo"], ensure_ascii=False)[:200]}')
            print(f'    响应: {best["response"][:200]}')
        
        # 基因库总结
        print(f'\n  基因库:')
        for gene_type, genes in self.gene_engine.gene_library.items():
            print(f'    {gene_type}: {len(genes)} 条基因')
        
        # 核心结论
        print(f'\n  核心结论:')
        if best and best['breakthrough']:
            print(f'    🎉 1001突破成功！')
            print(f'    使用的引擎: 围棋引擎×基因引擎双协同')
        elif best and best['score'] >= 50:
            print(f'    ⚠️  部分突破成功')
            print(f'    messages格式绕过了1001，但参数仍需调整')
            print(f'    建议: 继续微调messages参数')
        else:
            print(f'    ❌ 未突破1001')
            print(f'    所有请求仍被拦截')
        
        print('#'*70)


# ============================================================================
# 主执行
# ============================================================================
if __name__ == '__main__':
    cred = load_credentials()
    if not cred.get('jwt_token'):
        print('  ❌ 无有效JWT Token')
        sys.exit(1)
    
    print(f'  ✅ 凭据加载成功')
    print(f'    用户ID: {cred.get("userId", "")}')
    
    orchestrator = DualEngineOrchestrator(cred['jwt_token'])
    orchestrator.run_coordinated_attack()
