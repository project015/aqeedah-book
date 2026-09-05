"""กู้คลังหะดีษอาหรับกลับมา (ไฟล์ใหญ่ ไม่ได้ใส่มาในซิป) — python scripts/restore_evidence.py"""
import json,subprocess,os,sys
os.makedirs("evidence/hadith",exist_ok=True); os.makedirs("evidence/quran",exist_ok=True)
def get(url,out):
    if os.path.exists(out) and os.path.getsize(out)>10000: print("มีแล้ว",out); return
    print("โหลด",out,"...",flush=True); subprocess.run(["curl","-sL","-o",out,url]); print("  ",os.path.getsize(out),"bytes")
get("https://cdn.jsdelivr.net/gh/fawazahmed0/hadith-api@1/editions.json","evidence/hadith/editions.json")
ed=json.load(open("evidence/hadith/editions.json",encoding="utf-8"))
for book,v in ed.items():
    for c in v["collection"]:
        if c["language"]=="Arabic" and not c["name"].endswith("1"):
            get(c["link"].replace(".min.json",".json"),f"evidence/hadith/{c['name']}.json")
get("https://api.alquran.cloud/v1/quran/quran-uthmani","evidence/quran/quran-uthmani.json")
get("https://api.alquran.cloud/v1/quran/th.thai","evidence/quran/quran-th.json")
print("เสร็จแล้ว ลองรัน: python scripts/quran.py 2:255")
