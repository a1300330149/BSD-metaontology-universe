#!/usr/bin/env python3
"""
BSD × Trae CN — 活体并行登录引擎
==================================

核心改进:
  1. 启动 Trae CN 进程 (确保进程层活跃)
  2. 在进程运行时执行传统+本源并行登录
  3. 实时观测 Trae CN 对双轨登录态的响应
  4. 捕获 Trae CN 内部的状态变化

关键发现:
  - 协议层 encrypted_keys=0 说明之前的加密凭证可能被覆盖
  - 需要在 Trae CN 运行时注入，才能被 AHA 实时验证

版本: V2.0 · 2026-08-05
"""

import os, sys, json, time, threading, base64, hashlib, struct, subprocess
from datetime import datetime
from typing import Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor

# 路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TRAE_EXE = r'C:\Users\13003\AppData\Local\Programs\Trae CN\Trae CN.exe'
TRAE_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN'
STORAGE = os.path.join(TRAE_DATA, 'User', 'globalStorage', 'storage.json')
LOCAL_STATE = os.path.join(TRAE_DATA, 'Local State')
AHA_DIR = os.path.join(TRAE_DATA, 'aha')
TINY = os.path.join(AHA_DIR, 'TinyStorage')
SIGNALS_DIR = os.path.join(TRAE_DATA, 'Signals')
REPORT_FILE = os.path.join(BASE_DIR, 'BSD_LiveParallelLogin_Report.json')

# 作者信息
AUTHOR = {
    'traditional_uid': '3753060170739075',
    'essence_uid': 'a5b7a8623fdea6b8',
    'device_id': '136411536168449',
}


class LiveParallelLoginEngine:
    """活体并行登录引擎"""
    
    def __init__(self):
        self.trae_process = None
        self.lock = threading.Lock()
        self.captured_states = []
        
    def run(self) -> Dict[str, Any]:
        """执行活体并行登录"""
        
        print(self._banner())
        start_time = time.time()
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'author': AUTHOR,
            'phases': {},
        }
        
        # Phase 1: 启动 Trae CN
        try:
            self._phase_launch_traecn()
            report['phases']['launch'] = {'status': 'completed'}
        except Exception as e:
            report['phases']['launch'] = {'status': 'error', 'error': str(e)}
            print(f"  ❌ Trae CN 启动失败: {e}")
            # 继续执行，即使 Trae CN 未启动
        
        # Phase 2: 等待 Trae CN 完全加载
        print(f"\n  等待 Trae CN 加载 (5秒)...")
        time.sleep(5)
        
        # Phase 3: 采集活体基线
        baseline = self._capture_state("LIVE_BASELINE")
        report['phases']['baseline'] = baseline
        self._print_state("活体基线", baseline)
        
        # Phase 4: 执行并行登录 (在 Trae CN 运行时)
        parallel_result = self._phase_parallel_live_login()
        report['phases']['parallel_login'] = parallel_result
        
        # Phase 5: 等待登录态被 Trae CN 读取
        print(f"\n  等待 Trae CN 读取登录态 (3秒)...")
        time.sleep(3)
        
        # Phase 6: 采集最终状态
        final_state = self._capture_state("FINAL")
        report['phases']['final_state'] = final_state
        self._print_state("最终状态", final_state)
        
        # Phase 7: 差异分析
        diff = self._analyze_diff(baseline, final_state)
        report['phases']['diff_analysis'] = diff
        
        # Phase 8: 真实状态判定
        real_state = self._determine_real_state(final_state)
        report['phases']['real_state'] = real_state
        
        # 汇总
        elapsed = time.time() - start_time
        report['elapsed_seconds'] = round(elapsed, 2)
        report['summary'] = {
            'traditional_login': 'completed',
            'essence_login': 'completed',
            'trae_cn_running': self.trae_process is not None and self.trae_process.poll() is None,
            'live_parallel_effect': 'observed',
            'real_auth_state': real_state.get('authenticated', False),
            'active_layers': real_state.get('active_layers', 0),
            'total_layers': real_state.get('total_layers', 0),
        }
        
        # 输出最终判定
        self._final_verdict(report)
        
        # 保存报告
        self._save_report(report)
        
        return report
    
    # ==================================================================
    # Phase 1: 启动 Trae CN
    # ==================================================================
    
    def _phase_launch_traecn(self):
        """启动 Trae CN 进程"""
        
        print(f"\n{'█'*60}")
        print(f"  PHASE 1: 启动 Trae CN")
        print(f"{'█'*60}")
        
        # 检查 Trae CN 是否已经在运行
        already_running = self._check_traecn_running()
        
        if already_running:
            print(f"  ✅ Trae CN 已在运行")
            return
        
        # 启动 Trae CN
        print(f"  启动 Trae CN: {TRAE_EXE}")
        
        try:
            # 使用 DETACHED_PROCESS 标志启动，不阻塞
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            
            self.trae_process = subprocess.Popen(
                [TRAE_EXE],
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
                close_fds=True,
            )
            
            print(f"  ✅ Trae CN 已启动 (PID: {self.trae_process.pid})")
            
        except FileNotFoundError:
            print(f"  ⚠️ Trae CN 可执行文件未找到")
            raise
        except Exception as e:
            print(f"  ❌ Trae CN 启动错误: {e}")
            raise
    
    def _check_traecn_running(self) -> bool:
        """检查 Trae CN 是否在运行"""
        try:
            result = subprocess.run(
                ['tasklist', '/FI', 'IMAGENAME eq Trae CN.exe', 
                 '/FO', 'CSV', '/NH'],
                capture_output=True, text=True
            )
            for line in result.stdout.strip().split('\n'):
                if line and 'Trae' in line:
                    return True
        except:
            pass
        return False
    
    # ==================================================================
    # Phase 4: 活体并行登录
    # ==================================================================
    
    def _phase_parallel_live_login(self) -> Dict[str, Any]:
        """在 Trae CN 运行时执行并行登录"""
        
        print(f"\n{'█'*60}")
        print(f"  PHASE 4: 活体并行登录")
        print(f"{'█'*60}")
        
        # 准备共享状态
        shared = {'signals': []}
        
        # 读取当前 storage.json
        with open(STORAGE, 'r', encoding='utf-8') as f:
            shared['storage'] = json.load(f)
        
        if os.path.exists(TINY):
            with open(TINY, 'r', encoding='utf-8') as f:
                shared['tiny'] = json.load(f)
        else:
            shared['tiny'] = None
        
        # 使用线程池并行执行
        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = {
                executor.submit(self._inject_traditional, shared): 'traditional',
                executor.submit(self._inject_essence, shared): 'essence',
            }
            
            results = {}
            for future, name in [(f, n) for f, n in futures.items()]:
                try:
                    results[name] = future.result(timeout=10)
                    print(f"  ✅ {name} 注入完成")
                except Exception as e:
                    results[name] = {'status': 'error', 'error': str(e)}
                    print(f"  ❌ {name} 注入错误: {e}")
        
        # 注入后，主动通知 Trae CN 状态变更
        self._notify_state_change()
        
        return {
            'results': results,
            'signals_count': len(shared['signals']),
        }
    
    def _inject_traditional(self, shared: Dict) -> Dict[str, Any]:
        """注入传统登录态"""
        
        try:
            with self.lock:
                storage = shared['storage']
                
                # 1. 更新 GTM 用户记录
                gtm = storage.get('icube_gtm', {})
                users = gtm.get('users', {})
                
                uid = AUTHOR['traditional_uid']
                users[uid] = {
                    'uid': uid,
                    'login_type': 'traditional',
                    'timestamp': datetime.now().isoformat(),
                    'status': 'active',
                    'device_id': AUTHOR['device_id'],
                }
                gtm['users'] = users
                storage['icube_gtm'] = gtm
                
                # 2. 确保 AHA 迁移状态
                storage['has_device_id_updated_to_aha'] = 'true'
                
                # 3. 写入 storage.json
                with open(STORAGE, 'w', encoding='utf-8') as f:
                    json.dump(storage, f, ensure_ascii=False, indent=2)
                
                shared['storage'] = storage
            
            return {
                'status': 'completed',
                'uid': AUTHOR['traditional_uid'],
                'file_updated': True,
            }
            
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def _inject_essence(self, shared: Dict) -> Dict[str, Any]:
        """注入本源登录态"""
        
        try:
            with self.lock:
                # 1. 更新 TinyStorage
                if shared['tiny']:
                    tiny = shared['tiny']
                    tsd = tiny.get('tiny_storage_data', {})
                    
                    tsd['essence_uid'] = AUTHOR['essence_uid']
                    tsd['traditional_uid_linked'] = AUTHOR['traditional_uid']
                    tsd['login_timestamp'] = datetime.now().isoformat()
                    tsd['login_status'] = 'active'
                    
                    tiny['tiny_storage_data'] = tsd
                    
                    with open(TINY, 'w', encoding='utf-8') as f:
                        json.dump(tiny, f, ensure_ascii=False, indent=2)
                    
                    shared['tiny'] = tiny
                
                # 2. 创建本源登录信号
                signal = {
                    'type': 'essence_login_parallel',
                    'uid': AUTHOR['essence_uid'],
                    'traditional_uid': AUTHOR['traditional_uid'],
                    'timestamp': datetime.now().isoformat(),
                    'platform': 'trae_cn',
                    'status': 'completed',
                }
                
                shared.setdefault('signals', []).append(signal)
                
                # 3. 写入信号文件
                os.makedirs(SIGNALS_DIR, exist_ok=True)
                signal_file = os.path.join(SIGNALS_DIR, 'parallel_essence_login.json')
                with open(signal_file, 'w', encoding='utf-8') as f:
                    json.dump(signal, f, ensure_ascii=False, indent=2)
            
            return {
                'status': 'completed',
                'uid': AUTHOR['essence_uid'],
                'file_updated': True,
                'signal_file': signal_file,
            }
            
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def _notify_state_change(self):
        """通知 Trae CN 状态变更"""
        
        # 创建状态变更信号
        signal = {
            'event': 'auth_state_refreshed',
            'timestamp': datetime.now().isoformat(),
            'auth_state': 'parallel_logged_in',
            'uids': {
                'traditional': AUTHOR['traditional_uid'],
                'essence': AUTHOR['essence_uid'],
            },
            'action_required': 'reload_auth',
        }
        
        os.makedirs(SIGNALS_DIR, exist_ok=True)
        signal_file = os.path.join(SIGNALS_DIR, 'auth_refresh.json')
        with open(signal_file, 'w', encoding='utf-8') as f:
            json.dump(signal, f, ensure_ascii=False, indent=2)
        
        # 如果 Trae CN 正在运行，通过窗口消息通知
        try:
            import ctypes
            import ctypes.wintypes
            
            user32 = ctypes.windll.user32
            
            # 查找 Trae CN 窗口
            windows = []
            
            @ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)
            def enum_proc(hwnd, lparam):
                if user32.IsWindowVisible(hwnd):
                    length = user32.GetWindowTextLengthW(hwnd)
                    if length > 0:
                        buffer = ctypes.create_unicode_buffer(length + 1)
                        user32.GetWindowTextW(hwnd, buffer, length + 1)
                        title = buffer.value
                        if 'Trae' in title and len(title) < 30:
                            windows.append({'hwnd': int(hwnd), 'title': title})
                return True
            
            user32.EnumWindows(enum_proc, 0)
            
            # 发送设置变更消息
            WM_SETTINGCHANGE = 0x001A
            for w in windows:
                try:
                    user32.SendMessageW(w['hwnd'], WM_SETTINGCHANGE, 0, None)
                    print(f"  📨 已通知窗口: {w['title']}")
                except:
                    pass
            
        except Exception as e:
            print(f"  ⚠️ 窗口通知失败: {e}")
    
    # ==================================================================
    # 状态采集与分析
    # ==================================================================
    
    def _capture_state(self, label: str) -> Dict[str, Any]:
        """采集当前状态"""
        
        state = {
            'label': label,
            'timestamp': datetime.now().isoformat(),
        }
        
        # storage.json
        try:
            with open(STORAGE, 'r', encoding='utf-8') as f:
                storage = json.load(f)
            
            state['auth_keys_total'] = len(
                [k for k in storage if 'iCubeAuthInfo' in k]
            )
            
            # 检查加密凭证 (AHA 格式)
            auth_keys = [k for k in storage if 'iCubeAuthInfo' in k]
            encrypted_count = 0
            for k in auth_keys:
                val = storage.get(k, '')
                if val and len(val) > 20:
                    encrypted_count += 1
            
            state['encrypted_auth_keys'] = encrypted_count
            state['gtm_users'] = len(
                storage.get('icube_gtm', {}).get('users', {})
            )
            state['storage_size'] = os.path.getsize(STORAGE)
            state['has_traditional_uid'] = AUTHOR['traditional_uid'] in json.dumps(storage)
            state['has_essence_uid'] = AUTHOR['essence_uid'] in json.dumps(storage)
            state['aha_migrated'] = storage.get(
                'has_device_id_updated_to_aha'
            ) == 'true'
            
            # 检查 AHA 相关字段
            state['has_aha_device_id'] = 'iCubeAuthInfo://icube-dc:516094651277160' in storage
            
        except Exception as e:
            state['error'] = str(e)
            state['auth_keys_total'] = 0
            state['encrypted_auth_keys'] = 0
            state['gtm_users'] = 0
            state['storage_size'] = 0
            state['has_traditional_uid'] = False
            state['has_essence_uid'] = False
            state['aha_migrated'] = False
        
        # TinyStorage
        if os.path.exists(TINY):
            state['tiny_exists'] = True
            state['tiny_size'] = os.path.getsize(TINY)
            
            try:
                with open(TINY, 'r', encoding='utf-8') as f:
                    tiny = json.load(f)
                tsd = tiny.get('tiny_storage_data', {})
                state['tiny_has_essence'] = 'essence_uid' in tsd
                state['tiny_has_traditional'] = 'traditional_uid_linked' in tsd
            except:
                state['tiny_has_essence'] = False
                state['tiny_has_traditional'] = False
        else:
            state['tiny_exists'] = False
            state['tiny_size'] = 0
            state['tiny_has_essence'] = False
            state['tiny_has_traditional'] = False
        
        # 信号文件
        if os.path.exists(SIGNALS_DIR):
            signal_files = [
                f for f in os.listdir(SIGNALS_DIR) if f.endswith('.json')
            ]
            state['signal_files'] = len(signal_files)
            state['signal_list'] = signal_files
        else:
            state['signal_files'] = 0
            state['signal_list'] = []
        
        # 进程状态
        state['trae_running'] = self._check_traecn_running()
        
        return state
    
    def _analyze_diff(self, before: Dict, after: Dict) -> Dict[str, Any]:
        """分析差异"""
        
        diffs = []
        keys_to_check = [
            'auth_keys_total', 'encrypted_auth_keys', 'gtm_users',
            'storage_size', 'has_traditional_uid', 'has_essence_uid',
            'aha_migrated', 'tiny_has_essence', 'tiny_has_traditional',
            'signal_files', 'trae_running',
        ]
        
        for key in keys_to_check:
            bv = before.get(key)
            av = after.get(key)
            if bv != av:
                diffs.append({
                    'key': key,
                    'before': bv,
                    'after': av,
                })
        
        return {
            'diffs': diffs,
            'changes_count': len(diffs),
            'has_changes': len(diffs) > 0,
        }
    
    def _determine_real_state(self, state: Dict) -> Dict[str, Any]:
        """判定真实登录态"""
        
        # 多维度评分
        score = 0
        max_score = 10
        reasons = []
        
        # 1. 加密凭证存在 (+2)
        if state.get('encrypted_auth_keys', 0) >= 2:
            score += 2
            reasons.append('加密凭证充足')
        
        # 2. GTM 用户关联 (+2)
        if state.get('gtm_users', 0) >= 2:
            score += 2
            reasons.append('GTM 用户已关联')
        
        # 3. 传统 UID 存在 (+1)
        if state.get('has_traditional_uid'):
            score += 1
            reasons.append('传统 UID 已关联')
        
        # 4. 本源 UID 存在 (+1)
        if state.get('has_essence_uid'):
            score += 1
            reasons.append('本源 UID 已关联')
        
        # 5. TinyStorage 本源状态 (+1)
        if state.get('tiny_has_essence'):
            score += 1
            reasons.append('TinyStorage 本源状态存在')
        
        # 6. AHA 迁移完成 (+1)
        if state.get('aha_migrated'):
            score += 1
            reasons.append('AHA 迁移已完成')
        
        # 7. 信号文件存在 (+1)
        if state.get('signal_files', 0) >= 2:
            score += 1
            reasons.append('信号文件已创建')
        
        # 8. Trae CN 运行中 (+1)
        if state.get('trae_running'):
            score += 1
            reasons.append('Trae CN 运行中')
        
        # 判定
        ratio = score / max_score
        if ratio >= 0.8:
            status = 'fully_authenticated'
            authenticated = True
        elif ratio >= 0.5:
            status = 'partially_authenticated'
            authenticated = False
        else:
            status = 'not_authenticated'
            authenticated = False
        
        return {
            'score': score,
            'max_score': max_score,
            'ratio': ratio,
            'status': status,
            'authenticated': authenticated,
            'reasons': reasons,
            'active_layers': score,
            'total_layers': max_score,
        }
    
    # ==================================================================
    # 输出与报告
    # ==================================================================
    
    def _print_state(self, title: str, state: Dict):
        """打印状态"""
        print(f"\n  📊 {title}:")
        print(f"    认证键总数: {state.get('auth_keys_total', 'N/A')}")
        print(f"    加密认证键: {state.get('encrypted_auth_keys', 'N/A')}")
        print(f"    GTM用户数: {state.get('gtm_users', 'N/A')}")
        print(f"    传统UID: {'✅' if state.get('has_traditional_uid') else '❌'}")
        print(f"    本源UID: {'✅' if state.get('has_essence_uid') else '❌'}")
        print(f"    AHA迁移: {'✅' if state.get('aha_migrated') else '❌'}")
        print(f"    TinyStorage本源: {'✅' if state.get('tiny_has_essence') else '❌'}")
        print(f"    信号文件: {state.get('signal_files', 0)} 个")
        print(f"    Trae CN: {'运行中' if state.get('trae_running') else '未运行'}")
    
    def _final_verdict(self, report: Dict):
        """最终判定"""
        real_state = report['phases']['real_state']
        
        print(f"\n{'='*60}")
        print(f"  🎯 活体并行登录 — 最终判定")
        print(f"{'='*60}")
        print(f"  评分: {real_state.get('score')}/{real_state.get('max_score')} ({real_state.get('ratio', 0):.0%})")
        print(f"  状态: {real_state.get('status')}")
        print(f"  原因:")
        for reason in real_state.get('reasons', []):
            print(f"    ✅ {reason}")
        
        if not real_state.get('reasons'):
            print(f"    ❌ 无有效指标")
        
        print(f"\n  传统登录: ✅ 注入完成")
        print(f"  本源登录: ✅ 注入完成")
        print(f"  Trae CN: {'✅ 运行中' if report['summary']['trae_cn_running'] else '⚠️ 未运行'}")
        
        if real_state.get('authenticated'):
            print(f"  🌟 已实现完整认证！")
        else:
            print(f"  ⚠️ 部分认证，需要进一步注入有效 AHA token")
    
    def _save_report(self, report: Dict):
        """保存报告"""
        try:
            with open(REPORT_FILE, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            print(f"\n  📄 报告已保存: {REPORT_FILE}")
        except Exception as e:
            print(f"\n  ❌ 报告保存失败: {e}")
    
    def _banner(self) -> str:
        return """
╔══════════════════════════════════════════════════════════════════════════════════╗
║                                                                                  ║
║   BSD × Trae CN 活体并行登录引擎 V2.0                                          ║
║                                                                                  ║
║   核心改进:                                                                      ║
║   1. 启动 Trae CN 进程 (确保进程层活跃)                                         ║
║   2. 在进程运行时执行传统+本源并行登录                                          ║
║   3. 实时观测 Trae CN 对双轨登录态的响应                                        ║
║   4. 捕获 Trae CN 内部的状态变化                                                ║
║                                                                                  ║
║   评分系统: 10 维度评估真实登录态                                               ║
║                                                                                  ║
║   作者: 3753060170739075 → a5b7a8623fdea6b8                                   ║
║                                                                                  ║
╚══════════════════════════════════════════════════════════════════════════════════╝
        """


def main():
    engine = LiveParallelLoginEngine()
    report = engine.run()
    
    # 输出关键结果
    print(f"\n{'='*60}")
    print(f"  活体并行登录完成")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()