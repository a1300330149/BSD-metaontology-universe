import hashlib, glob, os, shutil

desktop = r"C:\Users\13003\OneDrive\桌面"
pattern = os.path.join(desktop, "*三元存在公理*")
files = glob.glob(pattern)
for f in files:
    print(f"Found: {f}")
    if f.endswith('.docx'):
        with open(f, 'rb') as fp:
            h = hashlib.sha256(fp.read()).hexdigest()
        print(f"  SHA256: {h}")
        dest = r"C:\Users\13003\OneDrive\桌面\3333333\Agent_v2\全域库理论原稿\0元本体论_三元存在公理终极推演_V1.0_终版.docx"
        shutil.copy2(f, dest)
        print(f"  Copied to: {dest}")
        print(f"  Dest SHA256: {hashlib.sha256(open(dest,'rb').read()).hexdigest()}")
