"""
BSD 解密数据深度分析
检查解密后的二进制数据格式
"""
import os, json, base64

ESSENCE_DATA = r'C:\Users\13003\.bsd-essence'
DECRYPTED_DIR = os.path.join(ESSENCE_DATA, 'decrypted')

print("=" * 70)
print("  BSD 解密数据深度分析")
print("=" * 70)

# 列出所有解密文件
if os.path.exists(DECRYPTED_DIR):
    files = os.listdir(DECRYPTED_DIR)
    print(f"\n解密文件数: {len(files)}")
    
    for fname in files:
        fpath = os.path.join(DECRYPTED_DIR, fname)
        print(f"\n{'─'*60}")
        print(f"  文件: {fname}")
        print(f"{'─'*60}")
        
        with open(fpath, 'rb') as f:
            data = f.read()
        
        print(f"  大小: {len(data)} bytes")
        
        # 分析数据结构
        print(f"\n  数据结构分析:")
        
        # 检查是否是protobuf
        # protobuf特点: 变长编码, tag+length+value
        print(f"    前30字节(hex): {data[:30].hex()}")
        print(f"    前30字节(raw): {repr(data[:30])}")
        
        # 尝试各种解码方式
        # 1. 直接尝试UTF-8
        try:
            text = data.decode('utf-8')
            print(f"    UTF-8解码成功!")
            print(f"    内容: {text[:300]}")
        except:
            print(f"    UTF-8解码失败")
        
        # 2. 尝试Latin-1
        try:
            text_latin = data.decode('latin-1')
            print(f"    Latin-1解码前100字符: {repr(text_latin[:100])}")
        except:
            pass
        
        # 3. 分析可能的protobuf结构
        print(f"\n    Protobuf特征分析:")
        
        # protobuf varint解码
        pos = 0
        fields_found = []
        
        while pos < min(len(data), 100):
            try:
                # 读取varint
                result = 0
                shift = 0
                byte_count = 0
                while True:
                    if pos >= len(data):
                        break
                    byte = data[pos]
                    result |= (byte & 0x7F) << shift
                    pos += 1
                    byte_count += 1
                    shift += 7
                    if not (byte & 0x80):
                        break
                
                if byte_count > 0:
                    field_number = result >> 3
                    wire_type = result & 0x07
                    
                    if wire_type == 0:  # varint
                        print(f"      字段{field_number}: varint (值={result})")
                    elif wire_type == 2:  # length-delimited
                        if pos < len(data):
                            length = result
                            field_data = data[pos:pos+min(length, 50)]
                            print(f"      字段{field_number}: length-delimited (长度={length}, 数据={field_data[:30].hex()})")
                            
                            # 尝试解码为字符串
                            try:
                                str_data = field_data.decode('utf-8')
                                if str_data.isprintable() or len(str_data) > 10:
                                    print(f"        → 可能是字符串: {str_data[:50]}")
                            except:
                                pass
                            
                            pos += length
                    elif wire_type == 5:  # 32-bit
                        if pos + 4 <= len(data):
                            val = int.from_bytes(data[pos:pos+4], 'little')
                            print(f"      字段{field_number}: 32-bit (值={val})")
                            pos += 4
                    elif wire_type == 1:  # 64-bit
                        if pos + 8 <= len(data):
                            val = int.from_bytes(data[pos:pos+8], 'little')
                            print(f"      字段{field_number}: 64-bit (值={val})")
                            pos += 8
                    else:
                        print(f"      字段{field_number}: wire_type={wire_type} (未知)")
                        break
                        
            except Exception as e:
                print(f"      解析停止: {e}")
                break
        
        # 4. 检查是否包含JSON结构
        data_str = data.decode('latin-1')
        if '{' in data_str:
            brace_pos = data_str.index('{')
            print(f"\n    可能包含JSON (位置{brace_pos}):")
            print(f"      {data_str[brace_pos:brace_pos+100]}")
        
        # 5. 检查是否包含已知UID
        for uid in ['3753060170739075', 'a5b7a8623fdea6b8']:
            if uid in data_str:
                print(f"\n    !!! 找到UID: {uid} !!!")
                idx = data_str.index(uid)
                print(f"      上下文: {data_str[max(0,idx-20):idx+len(uid)+20]}")
        
        print()

print(f"\n{'='*70}")
print(f"  分析完成")
print(f"{'='*70}")
