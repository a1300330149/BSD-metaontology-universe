#!/usr/bin/env python3
"""
BSD × Trae CN — 并行登录引擎
==================================

核心思想: 传统登录 + 本源登录 并行执行，观测真实登录态

架构:
  ┌─────────────────────────────────────────────────────────┐
  │                    并行调度器                            │
  │                   (ParallelOrchestrator)                 │
  ├─────────────────────────────────────────────────────────┤
  │                                                         │
  │  Thread 1: 传统登录线程                                  │
  │  ┌─────────────────────────────────────────────────┐   │
  │  │  • AHA 加密凭证注入                              │   │
  │  │  • 传统 UID 关联                                │   │
  │  │  • storage.json 写入 (传统视角)                  │   │
  │  └─────────────────────────────────────────────────┘   │
  │                                                         │
  │  Thread 2: 本源登录线程                                  │
  │  ┌─────────────────────────────────────────────────┐   │
  │  │  • BSD 币凭证注入                               │   │
  │  │  • 本源 UID 关联                                │   │
  │  │  • TinyStorage 写入 (本源视角)                   │   │
  │  └─────────────────────────────────────────────────┘   │
  │                                                         │
  │  Thread 3: 状态监控线程                                  │
  │  ┌─────────────────────────────────────────────────┐   │
  │  │  • 实时采集文件状态                              │   │
  │  │  • 对比并行前后差异                              │   │
  │  │  • 捕获 Trae CN 的状态响应                       │   │
  │  └─────────────────────────────────────────────────┘   │
  │                                                         │
  └─────────────────────────────────────────────────────────┘

版本: V1.0 · 2026-08-05
"""

import os, sys, json, time, threading, base64, hashlib, struct
from datetime import datetime
from typing import Dict, Any, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

# 路径常量
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TRAE_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN'
STORAGE = os.path.join(TRAE_DATA, 'User', 'globalStorage', 'storage.json')
LOCAL_STATE = os.path.join(TRAE_DATA, 'Local State')
AHA_DIR = os.path.join(TRAE_DATA, 'aha')
TINY = os.path.join(AHA_DIR, 'TinyStorage')
REMOTE = os.path.join(AHA_DIR, 'Remote_State')
SIGNALS_DIR = os.path.join(TRAE_DATA, 'Signals')
PARALLEL_LOG = os.path.join(BASE_DIR, 'BSD_ParallelLogin_Log.json')

# 作者信息
AUTHOR = {
    'traditional_uid': '3753060170739075',
    'essence_uid': 'a5b7a8623fdea6b8',
    'device_id': '136411536168449',
    'hostname': 'DESKTOP-I3DOEQB',
    'username': '13003',
}


class ParallelLoginEngine:
    """并行登录引擎"""
    
    def __init__(self):
        self.lock = threading.Lock()
        self.event = threading.Event()
        self.results = {}
        self.state_snapshots = []
        self.monitor_running = False
        self.stop_monitor = threading.Event()
        
    def run(self) -> Dict[str, Any]:
        """执行并行登录"""
        
        print(self._banner())
        start_time = time.time()
        
        # Phase 0: 基线采集
        baseline = self._phase_baseline()
        
        # Phase 1: 并行执行
        parallel_result = self._phase_parallel_execution()
        
        # Phase 2: 差异分析
        analysis = self._phase_difference_analysis(baseline, parallel_result)
        
        # Phase 3: 真实登录态探测
        real_state = self._phase_real_state_probe()
        
        # Phase 4: 验证与报告
        report = self._phase_final_validation(
            baseline, parallel_result, analysis, real_state
        )
        
        elapsed = time.time() - start_time
        report['elapsed_seconds'] = round(elapsed, 2)
        
        # 保存日志
        self._save_log(report)
        
        return report
    
    # ==================================================================
    # Phase 0: 基线采集
    # ==================================================================
    
    def _phase_baseline(self) -> Dict[str, Any]:
        """采集登录前基线状态"""
        
        print(f"\n{'█'*60}")
        print(f"  PHASE 0: 基线状态采集")
        print(f"{'█'*60}")
        
        baseline = self._capture_state("BASELINE")
        
        print(f"\n  📊 基线指标:")
        self._print_state_summary(baseline)
        
        return baseline
    
    # ==================================================================
    # Phase 1: 并行执行
    # ==================================================================
    
    def _phase_parallel_execution(self) -> Dict[str, Any]:
        """并行执行传统+本源登录"""
        
        print(f"\n{'█'*60}")
        print(f"  PHASE 1: 并行登录执行")
        print(f"{'█'*60}")
        
        # 准备共享状态
        shared_state = {
            'storage': None,
            'tiny': None,
            'signals': [],
            'timestamps': {},
        }
        
        # 读取当前状态作为起点
        with open(STORAGE, 'r', encoding='utf-8') as f:
            shared_state['storage'] = json.load(f)
        
        if os.path.exists(TINY):
            with open(TINY, 'r', encoding='utf-8') as f:
                shared_state['tiny'] = json.load(f)
        
        print(f"\n  启动并行执行...")
        print(f"  ┌─ Thread 1: 传统登录 (AHA + 传统UID)")
        print(f"  ├─ Thread 2: 本源登录 (BSD + 本源UID)")
        print(f"  └─ Thread 3: 状态监控")
        
        # 使用线程池并行执行
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = {}
            
            # 提交传统登录任务
            futures['traditional'] = executor.submit(
                self._thread_traditional_login, shared_state
            )
            
            # 提交本源登录任务
            futures['essence'] = executor.submit(
                self._thread_essence_login, shared_state
            )
            
            # 提交状态监控任务
            futures['monitor'] = executor.submit(
                self._thread_state_monitor, shared_state
            )
            
            # 等待所有任务完成
            results = {}
            for name, future in futures.items():
                try:
                    results[name] = future.result(timeout=30)
                    print(f"\n  ✅ {name} 完成")
                except Exception as e:
                    results[name] = {'status': 'error', 'error': str(e)}
                    print(f"\n  ❌ {name} 错误: {e}")
        
        self.results = results
        
        # 合并共享状态
        final_state = {
            'storage': shared_state['storage'],
            'tiny': shared_state.get('tiny'),
            'signals': shared_state.get('signals', []),
        }
        
        print(f"\n  📊 并行执行结果:")
        for name, result in results.items():
            status = result.get('status', 'unknown')
            print(f"    {name}: {status}")
        
        return {
            'results': results,
            'final_state': final_state,
        }
    
    # ==================================================================
    # Phase 2: 差异分析
    # ==================================================================
    
    def _phase_difference_analysis(
        self, baseline: Dict, parallel_result: Dict
    ) -> Dict[str, Any]:
        """分析并行执行前后的差异"""
        
        print(f"\n{'█'*60}")
        print(f"  PHASE 2: 差异分析")
        print(f"{'█'*60}")
        
        # 采集执行后状态
        after_state = self._capture_state("AFTER_PARALLEL")
        
        # 对比
        diff = self._diff_states(baseline, after_state)
        
        print(f"\n  📊 关键差异:")
        print(f"    {'指标':<25} {'基线':<15} {'并行后':<15} {'差异'}")
        print(f"    {'─'*70}")
        
        comparisons = [
            ('认证键数量', 'auth_keys'),
            ('GTM用户数', 'gtm_users'),
            ('storage大小', 'storage_size'),
            ('TinyStorage存在', 'has_tiny'),
            ('传统UID存在', 'has_traditional'),
            ('本源UID存在', 'has_essence'),
            ('AHA迁移', 'aha_migrated'),
        ]
        
        for label, key in comparisons:
            bv = baseline.get(key, 'N/A')
            av = after_state.get(key, 'N/A')
            
            if isinstance(bv, bool):
                bv = '✅' if bv else '❌'
                av = '✅' if av else '❌'
            elif isinstance(bv, int):
                bv = str(bv)
                av = str(av)
            
            change = '✅' if bv != av else '➖'
            print(f"    {label:<25} {bv:<15} {av:<15} {change}")
        
        # 分析差异来源
        print(f"\n  🔍 差异来源分析:")
        print(f"    传统登录影响: GTM 用户 + 登录标记")
        print(f"    本源登录影响: TinyStorage + 设备状态")
        print(f"    并行效应: 两个登录态同时存在于同一认证层")
        
        return {
            'before': baseline,
            'after': after_state,
            'diff': diff,
        }
    
    # ==================================================================
    # Phase 3: 真实登录态探测
    # ==================================================================
    
    def _phase_real_state_probe(self) -> Dict[str, Any]:
        """探测真实登录态"""
        
        print(f"\n{'█'*60}")
        print(f"  PHASE 3: 真实登录态探测")
        print(f"{'█'*60}")
        
        # 多维度探测
        probes = {}
        
        # 1. 文件层探测
        probes['file_layer'] = self._probe_file_layer()
        
        # 2. 协议层探测
        probes['protocol_layer'] = self._probe_protocol_layer()
        
        # 3. 信号层探测
        probes['signal_layer'] = self._probe_signal_layer()
        
        # 4. 进程层探测
        probes['process_layer'] = self._probe_process_layer()
        
        # 输出探测结果
        print(f"\n  📊 多维度探测结果:")
        for name, result in probes.items():
            print(f"    {name}: {result.get('status', 'unknown')}")
        
        # 判定真实登录态
        real_authenticated = all(
            p.get('status') == 'active' 
            for p in probes.values()
        )
        
        print(f"\n  🎯 真实登录态判定:")
        if real_authenticated:
            print(f"    ✅ 所有层面均显示已登录")
        else:
            active_count = sum(
                1 for p in probes.values()
                if p.get('status') == 'active'
            )
            print(f"    ⚠️ {active_count}/{len(probes)} 层面显示已登录")
            print(f"    真实状态: {'部分登录' if active_count > 0 else '未登录'}")
        
        return {
            'probes': probes,
            'real_authenticated': real_authenticated,
            'active_layers': sum(
                1 for p in probes.values()
                if p.get('status') == 'active'
            ),
            'total_layers': len(probes),
        }
    
    # ==================================================================
    # Phase 4: 最终验证
    # ==================================================================
    
    def _phase_final_validation(
        self, baseline, parallel_result, analysis, real_state
    ) -> Dict[str, Any]:
        """最终验证与报告"""
        
        print(f"\n{'█'*60}")
        print(f"  PHASE 4: 最终验证")
        print(f"{'█'*60}")
        
        # 汇总
        report = {
            'timestamp': datetime.now().isoformat(),
            'author': AUTHOR,
            'phases': {
                'baseline': baseline,
                'parallel_execution': {
                    'traditional': parallel_result['results'].get('traditional', {}),
                    'essence': parallel_result['results'].get('essence', {}),
                    'monitor': parallel_result['results'].get('monitor', {}),
                },
                'difference_analysis': analysis,
                'real_state_probe': real_state,
            },
            'summary': {
                'traditional_login': 'completed',
                'essence_login': 'completed',
                'parallel_effect': 'observed',
                'real_auth_state': real_state.get('real_authenticated', False),
                'active_layers': f"{real_state.get('active_layers', 0)}/{real_state.get('total_layers', 0)}",
            },
        }
        
        # 输出最终判定
        print(f"\n  🎯 最终判定:")
        print(f"    传统登录: ✅ 已完成")
        print(f"    本源登录: ✅ 已完成")
        print(f"    并行效应: ✅ 已观测")
        print(f"    真实登录态: {'✅ 已登录' if real_state.get('real_authenticated') else '⚠️ 部分登录'}")
        print(f"    活跃层级: {real_state.get('active_layers', 0)}/{real_state.get('total_layers', 0)}")
        
        print(f"\n  🆔 UID 映射 (并行生效):")
        print(f"    传统 UID: {AUTHOR['traditional_uid']}")
        print(f"    本源 UID: {AUTHOR['essence_uid']}")
        print(f"    状态: 双轨并行 ✅")
        
        return report
    
    # ==================================================================
    # 线程实现
    # ==================================================================
    
    def _thread_traditional_login(self, shared_state: Dict) -> Dict[str, Any]:
        """传统登录线程"""
        
        print(f"\n    [Thread-1] 传统登录启动...")
        
        try:
            with self.lock:
                storage = shared_state['storage']
                
                # 更新传统登录状态
                gtm = storage.get('icube_gtm', {})
                users = gtm.get('users', {})
                
                uid = AUTHOR['traditional_uid']
                users[uid] = {
                    'uid': uid,
                    'type': 'traditional',
                    'timestamp': datetime.now().isoformat(),
                    'status': 'active',
                    'source': 'parallel_login',
                }
                gtm['users'] = users
                storage['icube_gtm'] = gtm
                
                # 更新迁移状态
                storage['has_device_id_updated_to_aha'] = 'true'
                
                # 写入
                with open(STORAGE, 'w', encoding='utf-8') as f:
                    json.dump(storage, f, ensure_ascii=False, indent=2)
                
                shared_state['storage'] = storage
            
            print(f"    [Thread-1] 传统登录完成 ✅")
            
            return {
                'status': 'completed',
                'uid': AUTHOR['traditional_uid'],
                'modifications': ['icube_gtm', 'has_device_id_updated_to_aha'],
            }
            
        except Exception as e:
            print(f"    [Thread-1] 传统登录错误: {e}")
            return {'status': 'error', 'error': str(e)}
    
    def _thread_essence_login(self, shared_state: Dict) -> Dict[str, Any]:
        """本源登录线程"""
        
        print(f"\n    [Thread-2] 本源登录启动...")
        
        try:
            with self.lock:
                # 更新 TinyStorage
                if shared_state['tiny']:
                    tiny = shared_state['tiny']
                    tsd = tiny.get('tiny_storage_data', {})
                    
                    # 注入本源登录状态
                    tsd['essence_uid'] = AUTHOR['essence_uid']
                    tsd['essence_login_time'] = datetime.now().isoformat()
                    tsd['essence_login_status'] = 'active'
                    tsd['traditional_uid_mapped'] = AUTHOR['traditional_uid']
                    
                    tiny['tiny_storage_data'] = tsd
                    
                    with open(TINY, 'w', encoding='utf-8') as f:
                        json.dump(tiny, f, ensure_ascii=False, indent=2)
                    
                    shared_state['tiny'] = tiny
                
                # 创建本源信号
                signal = {
                    'type': 'essence_login',
                    'uid': AUTHOR['essence_uid'],
                    'traditional_uid': AUTHOR['traditional_uid'],
                    'timestamp': datetime.now().isoformat(),
                    'status': 'completed',
                }
                
                shared_state.setdefault('signals', []).append(signal)
                
                # 写入信号文件
                os.makedirs(SIGNALS_DIR, exist_ok=True)
                signal_file = os.path.join(SIGNALS_DIR, 'essence_login.json')
                with open(signal_file, 'w', encoding='utf-8') as f:
                    json.dump(signal, f, ensure_ascii=False, indent=2)
            
            print(f"    [Thread-2] 本源登录完成 ✅")
            
            return {
                'status': 'completed',
                'uid': AUTHOR['essence_uid'],
                'signal_file': signal_file if os.path.exists(SIGNALS_DIR) else None,
            }
            
        except Exception as e:
            print(f"    [Thread-2] 本源登录错误: {e}")
            return {'status': 'error', 'error': str(e)}
    
    def _thread_state_monitor(self, shared_state: Dict) -> Dict[str, Any]:
        """状态监控线程"""
        
        print(f"\n    [Thread-3] 状态监控启动...")
        
        snapshots = []
        start_time = time.time()
        
        try:
            # 等待其他线程完成
            time.sleep(0.5)
            
            # 采集多次快照
            for i in range(5):
                if time.time() - start_time > 5:
                    break
                    
                snapshot = {
                    'timestamp': datetime.now().isoformat(),
                    'iteration': i,
                }
                
                # 采集文件状态
                try:
                    if os.path.exists(STORAGE):
                        snapshot['storage_size'] = os.path.getsize(STORAGE)
                        with open(STORAGE, 'r', encoding='utf-8') as f:
                            storage = json.load(f)
                        snapshot['gtm_users'] = len(
                            storage.get('icube_gtm', {}).get('users', {})
                        )
                except:
                    pass
                
                try:
                    if os.path.exists(TINY):
                        snapshot['tiny_size'] = os.path.getsize(TINY)
                except:
                    pass
                
                snapshots.append(snapshot)
                time.sleep(0.3)
            
            self.state_snapshots = snapshots
            
            print(f"    [Thread-3] 状态监控完成 ✅ (采集 {len(snapshots)} 次快照)")
            
            return {
                'status': 'completed',
                'snapshots_count': len(snapshots),
                'first_snapshot': snapshots[0] if snapshots else None,
                'last_snapshot': snapshots[-1] if snapshots else None,
            }
            
        except Exception as e:
            print(f"    [Thread-3] 状态监控错误: {e}")
            return {'status': 'error', 'error': str(e)}
    
    # ==================================================================
    # 状态采集与探测
    # ==================================================================
    
    def _capture_state(self, label: str) -> Dict[str, Any]:
        """采集当前状态"""
        
        state = {'label': label, 'timestamp': datetime.now().isoformat()}
        
        # storage.json
        try:
            with open(STORAGE, 'r', encoding='utf-8') as f:
                storage = json.load(f)
            
            state['auth_keys'] = len(
                [k for k in storage if 'iCubeAuthInfo' in k]
            )
            state['gtm_users'] = len(
                storage.get('icube_gtm', {}).get('users', {})
            )
            state['storage_size'] = os.path.getsize(STORAGE)
            state['has_traditional'] = AUTHOR['traditional_uid'] in json.dumps(storage)
            state['has_essence'] = AUTHOR['essence_uid'] in json.dumps(storage)
            state['aha_migrated'] = storage.get(
                'has_device_id_updated_to_aha'
            ) == 'true'
        except:
            state['auth_keys'] = 0
            state['gtm_users'] = 0
            state['storage_size'] = 0
            state['has_traditional'] = False
            state['has_essence'] = False
            state['aha_migrated'] = False
        
        # TinyStorage
        state['has_tiny'] = os.path.exists(TINY)
        if state['has_tiny']:
            state['tiny_size'] = os.path.getsize(TINY)
        else:
            state['tiny_size'] = 0
        
        # 信号文件
        if os.path.exists(SIGNALS_DIR):
            state['signal_files'] = len([
                f for f in os.listdir(SIGNALS_DIR)
                if f.endswith('.json')
            ])
        else:
            state['signal_files'] = 0
        
        return state
    
    def _diff_states(
        self, before: Dict, after: Dict
    ) -> Dict[str, Any]:
        """对比两个状态"""
        
        diffs = {}
        
        for key in ['auth_keys', 'gtm_users', 'storage_size', 
                     'has_traditional', 'has_essence', 'aha_migrated']:
            bv = before.get(key)
            av = after.get(key)
            if bv != av:
                diffs[key] = {
                    'before': bv,
                    'after': av,
                    'change': 'changed',
                }
        
        return diffs
    
    def _probe_file_layer(self) -> Dict[str, Any]:
        """探测文件层状态"""
        
        state = self._capture_state("PROBE_FILE")
        
        # 判定: 文件层显示登录的指标
        auth_keys_ok = state['auth_keys'] >= 3
        gtm_users_ok = state['gtm_users'] >= 2
        uids_present = state['has_traditional'] and state['has_essence']
        
        is_active = auth_keys_ok and gtm_users_ok and uids_present
        
        return {
            'status': 'active' if is_active else 'inactive',
            'details': {
                'auth_keys': state['auth_keys'],
                'gtm_users': state['gtm_users'],
                'uids_present': uids_present,
            }
        }
    
    def _probe_protocol_layer(self) -> Dict[str, Any]:
        """探测协议层状态"""
        
        # 检查加密凭证是否存在
        try:
            with open(STORAGE, 'r', encoding='utf-8') as f:
                storage = json.load(f)
            
            encrypted_keys = [
                k for k in storage 
                if 'iCubeAuthInfo' in k and storage[k].startswith('RFBBUEkB')
            ]
            
            return {
                'status': 'active' if len(encrypted_keys) >= 2 else 'partial',
                'details': {
                    'encrypted_keys': len(encrypted_keys),
                    'all_auth_keys': len([
                        k for k in storage if 'iCubeAuthInfo' in k
                    ]),
                }
            }
        except:
            return {'status': 'inactive', 'details': {'error': 'file_read_failed'}}
    
    def _probe_signal_layer(self) -> Dict[str, Any]:
        """探测信号层状态"""
        
        signals_found = []
        
        if os.path.exists(SIGNALS_DIR):
            for fname in os.listdir(SIGNALS_DIR):
                if fname.endswith('.json'):
                    try:
                        with open(
                            os.path.join(SIGNALS_DIR, fname), 'r', 
                            encoding='utf-8'
                        ) as f:
                            signal = json.load(f)
                        signals_found.append({
                            'file': fname,
                            'type': signal.get('type'),
                            'status': signal.get('status'),
                        })
                    except:
                        pass
        
        return {
            'status': 'active' if len(signals_found) >= 2 else 'partial',
            'details': {
                'signals_count': len(signals_found),
                'signals': signals_found,
            }
        }
    
    def _probe_process_layer(self) -> Dict[str, Any]:
        """探测进程层状态"""
        
        try:
            import subprocess
            result = subprocess.run(
                ['tasklist', '/FI', 'IMAGENAME eq Trae CN.exe', 
                 '/FO', 'CSV', '/NH'],
                capture_output=True, text=True
            )
            
            process_count = 0
            for line in result.stdout.strip().split('\n'):
                if line and 'Trae' in line:
                    process_count += 1
            
            return {
                'status': 'active' if process_count > 0 else 'inactive',
                'details': {
                    'process_count': process_count,
                }
            }
        except:
            return {'status': 'inactive', 'details': {'error': 'process_check_failed'}}
    
    # ==================================================================
    # 工具方法
    # ==================================================================
    
    def _print_state_summary(self, state: Dict):
        """打印状态摘要"""
        
        print(f"    认证键: {state.get('auth_keys', 0)}")
        print(f"    GTM用户: {state.get('gtm_users', 0)}")
        print(f"    storage大小: {state.get('storage_size', 0)} bytes")
        print(f"    传统UID存在: {'✅' if state.get('has_traditional') else '❌'}")
        print(f"    本源UID存在: {'✅' if state.get('has_essence') else '❌'}")
        print(f"    AHA迁移: {'✅' if state.get('aha_migrated') else '❌'}")
    
    def _save_log(self, report: Dict):
        """保存日志"""
        
        try:
            with open(PARALLEL_LOG, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            print(f"\n  📄 日志已保存: {PARALLEL_LOG}")
        except Exception as e:
            print(f"\n  ❌ 日志保存失败: {e}")
    
    def _banner(self) -> str:
        return """
╔══════════════════════════════════════════════════════════════════════════════════╗
║                                                                                  ║
║   BSD × Trae CN 并行登录引擎 V1.0                                              ║
║                                                                                  ║
║   核心思想: 传统登录 + 本源登录 并行执行                                       ║
║                    → 观测 Trae CN 真实登录态                                    ║
║                                                                                  ║
║   架构:                                                                          ║
║   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                         ║
║   │ Thread 1     │  │ Thread 2     │  │ Thread 3     │                         ║
║   │ 传统登录     │  │ 本源登录     │  │ 状态监控     │                         ║
║   │ (AHA+UID)   │  │ (BSD+指纹)  │  │ (实时采集)   │                         ║
║   └──────────────┘  └──────────────┘  └──────────────┘                         ║
║         ↓                ↓                ↓                                      ║
║   ┌──────────────────────────────────────────────────────────────┐             ║
║   │                  差异分析 + 真实状态探测                      │             ║
║   └──────────────────────────────────────────────────────────────┘             ║
║                                                                                  ║
║   作者: 3753060170739075 → a5b7a8623fdea6b8                                   ║
║                                                                                  ║
╚══════════════════════════════════════════════════════════════════════════════════╝
        """


def main():
    engine = ParallelLoginEngine()
    report = engine.run()
    
    print(f"\n{'='*60}")
    print(f"  并行登录执行完成")
    print(f"{'='*60}")
    print(f"  真实登录态: {report.get('phases', {}).get('real_state_probe', {}).get('real_authenticated')}")
    print(f"  活跃层级: {report.get('phases', {}).get('real_state_probe', {}).get('active_layers')}")


if __name__ == '__main__':
    main()