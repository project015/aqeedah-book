"""ดึงหะดีษแปลไทย+อาหรับ+สถานะ+คำอธิบาย จาก hadeethenc.com (ทุกหมวดราก) → evidence/hadith/hadeethenc_th.json"""
import json,subprocess,os,time
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128 Safari/537.36"
def get(url):
    for _ in range(3):
        r=subprocess.run(["curl","-s","-A",UA,url],capture_output=True,text=True,encoding="utf-8").stdout
        try: return json.loads(r)
        except Exception: time.sleep(2)
    return None
out="evidence/hadith/hadeethenc_th.json"
db=json.load(open(out,encoding="utf-8")) if os.path.exists(out) else {}
roots=get("https://hadeethenc.com/api/v1/categories/roots/?language=th")
order=[3,1,2,5,6,7,4]  # อะกีดะฮ์ก่อน
for cid in order:
    page=1
    while True:
        d=get(f"https://hadeethenc.com/api/v1/hadeeths/list/?language=th&category_id={cid}&per_page=50&page={page}")
        if not d or not d.get("data"): break
        for h in d["data"]:
            if h["id"] in db: continue
            one=get(f"https://hadeethenc.com/api/v1/hadeeths/one/?language=th&id={h['id']}")
            if one: db[h["id"]]={k:one.get(k) for k in ("id","title","hadeeth","attribution","grade","explanation","hints","categories","hadeeth_ar","attribution_ar","grade_ar","explanation_ar")}; db[h["id"]]["root"]=cid
        json.dump(db,open(out,"w",encoding="utf-8"),ensure_ascii=False)
        print("cat",cid,"page",page,"total",len(db),flush=True)
        if len(d["data"])<50: break
        page+=1
print("done",len(db))
