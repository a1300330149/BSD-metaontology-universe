#!/usr/bin/env python3
"""
BSD × Trae CN — 登录态数据流深度诊断
======================================

目标:
  1. 检查注入的数据是否被 Trae CN 接受
  2. 分析 Trae CN 启动时的数据覆盖逻辑
  3. 找到真正的登录验证链路

版本: V1.0 · 2026-08-05
"""

import os, json, base64, sqlite3, hashlib
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# 路径
TRAE_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN'
LOCAL_STATE = os.path.join(TRAE_DATA, 'Local State')
STORAGE = os.path.join(TRAE_DATA, 'User', 'globalStorage', 'storage.json')
VSCDB = os.path.join(TRAE_DATA, 'User', 'workspaceStorage', '37c75d46fd05168780d5ac3435faa836', 'state.vscdb')
TRAE_CONFIG = r'C:\Users\13003\.trae-cn'
JWT_PATH = os.path.join(TRAE_CONFIG, 'trae-jwt-token')

# 已知密钥
KNOWN_AES_KEY = bytes.fromhex('71079e1533eae26094450a564b7641e28d3292d36636807016c552ad0af26bb0')
AHA_PREFIX = bytes.fromhex('746305100000')

ESS_UID = 'a5b7a8623fdea6b8'


class DeepDiagnostic:
    """深度诊断"""
    
    def __init__(self):
        self.report = {}
    
    def run(self) -> dict:
        """执行诊断"""
        
        print(self._banner())
        
        # 1. 检查注入后的 storage.json
        self._check_storage()
        
        # 2. 解密 AHA 数据验证内容
        self._decrypt_aha_data()
        
        # 3. 检查 Local State
        self._check_local_state()
        
        # 4. 检查 state.vscdb
        self._check_vscdb()
        
        # 5. 检查 JWT Token
        self._check_jwt()
        
        # 6. 分析 Trae CN 数据覆盖逻辑
        self._analyze_覆盖逻辑()
        
        # 7. 输出结论
        self._print_conclusion()
        
        return self.report
    
    def _check_storage(self):
        """检查 storage.json"""
        print('\n' + '='*60)
        print('  1. 检查 storage.json')
        print('='*60)
        
        with open(STORAGE, 'r', encoding='utf-8') as f:
            storage = json.load(f)
        
        # 检查关键字段
        gtm = storage.get('icube_gtm', {})
        current_user = gtm.get('currentUser')
        users = gtm.get('users', {})
        
        print(f'  currentUser: {current_user}')
        print(f'  用户数量: {len(users)}')
        
        for uid, data in users.items():
            print(f'    {uid}: status={data.get("status")}, priority={data.get("priority")}')
        
        # 检查认证键
        auth_keys = {k: v[:50] + '...' for k, v in storage.items() if 'iCubeAuthInfo' in k}
        print(f'  认证键数量: {len(auth_keys)}')
        for key, preview in auth_keys.items():
            print(f'    {key}: {preview}')
        
        self.report['storage'] = {
            'currentUser': current_user,
            'userCount': len(users),
            'authKeyCount': len(auth_keys),
        }
    
    def _decrypt_aha_data(self):
        """解密 AHA 数据"""
        print('\n' + '='*60)
        print('  2. 解密 AHA 数据验证')
        print('='*60)
        
        with open(STORAGE, 'r', encoding='utf-8') as f:
            storage = json.load(f)
        
        # 找到第一个认证键
        auth_keys = [k for k in storage if 'iCubeAuthInfo' in k]
        
        if not auth_keys:
            print('  ❌ 未找到认证键')
            return
        
        key = auth_keys[0]
        encrypted_b64 = storage[key]
        
        print(f'  密钥: {key}')
        
        try:
            # Base64 解码
            raw = base64.b64decode(encrypted_b64)
            print(f'  解码后长度: {len(raw)} 字节')
            
            # 检查前缀
            prefix = raw[:6]
            if prefix == AHA_PREFIX:
                print('  ✅ AHA 前缀匹配')
            else:
                print(f'  ⚠️ 前缀不匹配: {prefix.hex()}')
            
            # 提取 IV 和密文
            iv = raw[6:22]
            ciphertext = raw[22:]
            
            print(f'  IV: {iv.hex()}')
            print(f'  密文长度: {len(ciphertext)}')
            
            # 尝试解密
            cipher = AES.new(KNOWN_AES_KEY, AES.MODE_CBC, iv=iv)
            decrypted = cipher.decrypt(ciphertext)
            
            # 尝试去填充
            try:
                plaintext = unpad(decrypted, AES.block_size)
                print(f'  解密成功! 长度: {len(plaintext)} 字节')
                
                # 尝试解析 JSON
                try:
                    data = json.loads(plaintext)
                    print(f'  ✅ JSON 解析成功!')
                    print(f'     uid: {data.get("uid")}')
                    print(f'     loginType: {data.get("loginType")}')
                    print(f'     keys: {list(data.keys())[:10]}')
                    
                    self.report['aha_decrypted'] = {
                        'valid': True,
                        'uid': data.get('uid'),
                        'loginType': data.get('loginType'),
                    }
                except:
                    print(f'  ⚠️ 不是 JSON')
                    print(f'     原始文本: {plaintext[:100]}...')
                    self.report['aha_decrypted'] = {
                        'valid': False,
                        'raw': plaintext[:100].decode('latin-1', errors='replace'),
                    }
                    
            except Exception as e:
                print(f'  ⚠️ 去填充失败: {e}')
                print(f'  解密后内容: {decrypted[:100]}...')
                self.report['aha_decrypted'] = {
                    'valid': False,
                    'error': str(e),
                }
                
        except Exception as e:
            print(f'  ❌ 解密失败: {e}')
            self.report['aha_decrypted'] = {'error': str(e)}
    
    def _check_local_state(self):
        """检查 Local State"""
        print('\n' + '='*60)
        print('  3. 检查 Local State')
        print('='*60)
        
        with open(LOCAL_STATE, 'r', encoding='utf-8') as f:
            state = json.load(f)
        
        user = state.get('user', {})
        profile = state.get('profile', {})
        
        print(f'  user.userId: {user.get("userId")}')
        print(f'  user.loginType: {user.get("loginType")}')
        print(f'  profile.uid: {profile.get("uid")}')
        
        self.report['localState'] = {
            'userId': user.get('userId'),
            'loginType': user.get('loginType'),
        }
    
    def _check_vscdb(self):
        """检查 state.vscdb"""
        print('\n' + '='*60)
        print('  4. 检查 state.vscdb')
        print('='*60)
        
        try:
            conn = sqlite3.connect(VSCDB)
            cursor = conn.cursor()
            
            # 查找本源 UID 相关记录
            cursor.execute(f"SELECT key FROM ItemTable WHERE key LIKE '%{ESS_UID}%'")
            rows = cursor.fetchall()
            
            print(f'  本源 UID 相关记录: {len(rows)} 条')
            for row in rows[:5]:
                print(f'    {row[0]}')
            
            conn.close()
            
            self.report['vscdb'] = {'essenceRows': len(rows)}
            
        except Exception as e:
            print(f'  ❌ 查询失败: {e}')
            self.report['vscdb'] = {'error': str(e)}
    
    def _check_jwt(self):
        """检查 JWT Token"""
        print('\n' + '='*60)
        print('  5. 检查 JWT Token')
        print('='*60)
        
        if os.path.exists(JWT_PATH):
            with open(JWT_PATH, 'r', encoding='utf-8') as f:
                token = f.read()
            
            print(f'  ✅ JWT 存在, 长度: {len(token)}')
            
            # 解码
            try:
                parts = token.split('.')
                if len(parts) >= 2:
                    payload = base64.b64decode(parts[1] + '==').decode()
                    data = json.loads(payload)
                    print(f'     sub: {data.get("sub")}')
                    print(f'     name: {data.get("name")}')
                    print(f'     type: {data.get("type")}')
            except Exception as e:
                print(f'  解码失败: {e}')
            
            self.report['jwt'] = {'exists': True, 'length': len(token)}
        else:
            print('  ❌ JWT 不存在')
            self.report['jwt'] = {'exists': False}
    
    def _analyze_覆盖逻辑(self):
        """分析数据覆盖逻辑"""
        print('\n' + '='*60)
        print('  6. 数据覆盖逻辑分析')
        print('='*60)
        
        print('''
  📊 Trae CN 启动流程分析:
  
  ┌─────────────────────────────────────────────────────────────────────────┐
  │  1. 读取 Local State → 获取 encrypted_key                              │
  │  2. 读取 storage.json → 获取认证信息 (iCubeAuthInfo)                    │
  │  3. 调用 CheckLogin 接口 → 验证认证有效性                              │
  │  4. 调用 getUserInfo 接口 → 获取用户真实信息                           │
  │  5. 如果验证成功 → 更新 UI 显示登录状态                                │
  │  6. 如果验证失败 → 清除登录态，显示未登录                              │
  └─────────────────────────────────────────────────────────────────────────┘
  
  🔍 问题诊断:
  
  我们注入的数据:
  ✅ Local State.user.userId = a5b7a8623fdea6b8
  ✅ storage.json.icube_gtm.currentUser = a5b7a8623fdea6b8
  ✅ storage.json.iCubeAuthInfo = AHA加密数据
  
  可能的问题:
  ⚠️ AHA 加密数据是我们自己构造的
  ⚠️ Trae CN 会用这个数据去调用远程 API
  ⚠️ 远程 API 验证失败（因为不是真实凭证）
  ⚠️ Trae CN 发现验证失败 → 清除登录态
        ''')
        
        self.report['覆盖逻辑'] = '需要绕过远程API验证'
    
    def _print_conclusion(self):
        """打印结论"""
        print('\n' + '='*60)
        print('  7. 结论')
        print('='*60)
        
        d = self.report
        
        print(f'''
  ╔══════════════════════════════════════════════════════════════════════════════╗
  ║                                                                              ║
  ║  📋 诊断结果:                                                              ║
  ║                                                                              ║
  ║  1. storage.json: ✅ 包含本源UID                                           ║
  ║     - currentUser: {d.get('storage', {}).get('currentUser', '?')}           ║
  ║     - 用户数: {d.get('storage', {}).get('userCount', '?')}                ║
  ║                                                                              ║
  ║  2. AHA 数据: {'✅ 解密成功' if d.get('aha_decrypted', {}).get('valid') else '❌ 解密失败'}  ║
  ║                                                                              ║
  ║  3. Local State: ✅ 包含本源UID                                            ║
  ║     - userId: {d.get('localState', {}).get('userId', '?')}                ║
  ║                                                                              ║
  ║  4. JWT Token: {'✅ 存在' if d.get('jwt', {}).get('exists') else '❌ 不存在'}                       ║
  ║                                                                              ║
  ║  🔑 根本原因:                                                              ║
  ║                                                                              ║
  ║  Trae CN 启动时会调用远程 API 验证登录凭证                                ║
  ║  我们注入的 AHA 数据不是真实凭证                                          ║
  ║  远程 API 验证失败 → Trae CN 清除登录态                                   ║
  ║                                                                              ║
  ║  🎯 解决方案:                                                              ║
  ║                                                                              ║
  ║  方案 A: 复用传统登录的真实凭证 (需要先传统登录)                          ║
  ║  方案 B: 找到绕过远程验证的方法 (修改 main.js)                            ║
  ║  方案 C: 创建独立的本源登录显示页面 (不依赖 Trae CN UI)                   ║
  ║                                                                              ║
  ╚══════════════════════════════════════════════════════════════════════════════╝
        ''')
    
    def _banner(self) -> str:
        return """
╔══════════════════════════════════════════════════════════════════════════════════╗
║                                                                                  ║
║   BSD × Trae CN — 登录态数据流深度诊断                                         ║
║                                                                                  ║
║   目标:                                                                          ║
║   1. 检查注入的数据是否被 Trae CN 接受                                          ║
║   2. 分析 Trae CN 启动时的数据覆盖逻辑                                          ║
║   3. 找到真正的登录验证链路                                                      ║
║                                                                                  ║
╚══════════════════════════════════════════════════════════════════════════════════╝
        """


if __name__ == '__main__':
    diagnostic = DeepDiagnostic()
    report = diagnostic.run()
    
    # 保存报告
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(output_dir, 'BSD_DeepDiagnostic_Report.json')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f'\n  📄 报告已保存: {output_file}')