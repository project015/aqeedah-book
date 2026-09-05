"""พิมพ์คลิปถัดไปที่ยังไม่มีการ์ด (ลำดับ: 2020 ตามตอน → 2024 ตอน 30+ → 2024 ตอน 1–29) · usage: next_batch.py N"""
import json,os,sys,re
n=int(sys.argv[1]) if len(sys.argv)>1 else 4
ix=json.load(open("sources/index.json",encoding="utf-8"))
def key(r):
    s=r["series"]; e=r["ep"] or 999
    return (0,e) if s=="2020" else ((1,e) if e>=30 else (2,e))
inflight=set(open('cards/_inflight.txt',encoding='utf-8').read().split()) if os.path.exists('cards/_inflight.txt') else set()
todo=[]
for r in sorted(ix,key=key):
    if not r["has_sub"] or r['id'] in inflight: continue
    if os.path.exists(f"cards/{r['id']}.md") and os.path.getsize(f"cards/{r['id']}.md")>2000: continue
    todo.append(r)
print(f"เหลือ {len(todo)} คลิป")
for r in todo[:n]:
    slides=f"sources/docs/{r['series']}_ep{r['ep']:02d}.md" if r["ep"] else ""
    slides=slides if os.path.exists(slides) else "-"
    print(f"{r['id']} | ชุด {r['series']} ตอน {r['ep']} | {r['minutes']} นาที | {r['chars']} ตัวอักษร | สไลด์: {slides} | {r['title'][:60]}")
