import re

MAIN_JS = r'C:\Users\13003\AppData\Local\Programs\Trae CN\resources\app\out\main.js'

with open(MAIN_JS, 'r', encoding='utf-8') as f:
    code = f.read()

print("=== Patch Verification ===")
print("BSD本源用户:", "BSD本源用户" in code)
print("bsd@essence.local:", "bsd@essence.local" in code)
print("Jx=(t,e,i)=:", "Jx=(t,e,i)=" in code)
print("getUserInfo:", "getUserInfo" in code)

# Find Jx function
for m in re.finditer(r'Jx=\(t,e,i\)', code):
    pos = m.start()
    ctx = code[pos:pos+200]
    print(f"\nJx @{pos}: {ctx[:200]}")

# Check if ScreenName still exists in Jx
if "username:t.ScreenName" in code:
    print("\nWARNING: username:t.ScreenName still exists!")
    # Find all occurrences
    for m in re.finditer(r'username:t\.ScreenName', code):
        print(f"  @{m.start()}: ...{code[max(0,m.start()-20):m.end()+20]}...")
elif 'username:"BSD本源用户"' in code:
    print('\nOK: username:"BSD本源用户" found')
else:
    print("\nNeither found - checking what Jx uses:")
    for m in re.finditer(r'username:', code):
        ctx = code[m.start():m.start()+50]
        print(f"  @{m.start()}: {ctx}")
        break
