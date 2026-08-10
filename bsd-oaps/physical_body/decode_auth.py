import json
import base64
import os

# Read the storage.json file
file_path = r'C:\Users\13003\AppData\Roaming\TRAE SOLO CN\User\globalStorage\storage.json'

with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

print("=" * 60)
print("Auth Keys Found:")
print("=" * 60)

# Look for auth-related keys
auth_keys = [k for k in data.keys() if 'auth' in k.lower() or 'token' in k.lower() or 'cloud' in k.lower() or 'jwt' in k.lower()]

for key in auth_keys:
    value = data[key]
    print(f"\nKey: {key}")
    print(f"Value Length: {len(value)} chars")
    
    # Try to decode as base64
    try:
        decoded = base64.b64decode(value)
        print(f"Decoded (first 200 bytes): {decoded[:200]}")
        
        # Try to parse as JSON
        try:
            json_data = json.loads(decoded)
            print(f"JSON Content: {json.dumps(json_data, indent=2)[:500]}")
        except:
            print(f"Raw text: {decoded[:300]}")
    except Exception as e:
        print(f"Base64 decode failed: {e}")
        print(f"Raw value: {value[:200]}")