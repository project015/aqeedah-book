"""json3 (YouTube auto-sub) -> clean transcript paragraphs + sources/index.json"""
import json,glob,os,re
PL={"PLsD2Riy9_YZHyqOT6j4OM4Oe4wh4Dek0i":"2020","PLsD2Riy9_YZHXvxI-zP3yrqiGxMdpR78l":"2024","PLsD2Riy9_YZF_LW4XbEoyiaXU20LkSGfT":"2024"}
os.makedirs("sources/transcripts",exist_ok=True)
index=[]
for inf in sorted(glob.glob("sources/raw/*.info.json")):
    vid=os.path.basename(inf).split(".")[0]
    i=json.load(open(inf,encoding="utf-8"))
    desc=i.get("description","") or ""
    links=sorted(set(re.findall(r"https?://(?:drive|docs)\.google\.com/[^\s\)\]]+",desc)))
    title=i.get("title") or ""
    m=re.search(r"ตอนที่\s*(\d+)",title); ep=int(m.group(1)) if m else None
    series=PL.get(i.get("playlist_id"),"?")
    rec={"id":vid,"series":series,"ep":ep,"title":title,"minutes":round((i.get("duration") or 0)/60),"upload":i.get("upload_date"),"drive_links":links,"has_sub":False}
    j3=f"sources/raw/{vid}.th-orig.json3"
    if os.path.exists(j3):
        d=json.load(open(j3,encoding="utf-8"))
        words=[]
        for ev in d.get("events",[]):
            if "segs" not in ev: continue
            t0=ev["tStartMs"]
            for s in ev["segs"]:
                w=s.get("utf8","")
                if w.strip()=="" : continue
                words.append((t0+s.get("tOffsetMs",0),w))
        # paragraphs of ~60s
        paras=[]; cur=[]; pstart=None
        for t,w in words:
            if pstart is None: pstart=t
            cur.append(w)
            if t-pstart>=60000:
                paras.append((pstart,"".join(cur))); cur=[]; pstart=None
        if cur: paras.append((pstart,"".join(cur)))
        with open(f"sources/transcripts/{vid}.txt","w",encoding="utf-8") as f:
            f.write(f"# {title}\n# series {series} · ep {ep} · {rec['minutes']} นาที · {vid}\n\n")
            for t,p in paras:
                f.write(f"[{t//60000:03d}:{(t//1000)%60:02d}] {p.strip()}\n\n")
        rec["has_sub"]=True; rec["words"]=len(words); rec["chars"]=sum(len(w) for _,w in words)
    index.append(rec)
index.sort(key=lambda r:(r["series"],r["ep"] or 999))
json.dump(index,open("sources/index.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print(len(index),"videos;",sum(r["has_sub"] for r in index),"with sub;",sum(r.get("chars",0) for r in index),"chars total")
for s in ("2020","2024"):
    rs=[r for r in index if r["series"]==s]; print(s,len(rs),"clips",sum(r["minutes"] for r in rs)//60,"h", sum(1 for r in rs if r["drive_links"]),"with drive")
