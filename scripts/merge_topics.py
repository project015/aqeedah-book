"""อ่าน cards/*.md → topics/<หมวด>.md + topics/_summary.md (นับการ์ดต่อหมวด/ระดับ, ประเด็นที่ย้ำหลายคลิป)"""
import glob,os,re,json,collections
os.makedirs("topics",exist_ok=True)
cards=[]
for f in sorted(glob.glob("cards/*.md")):
    if os.path.basename(f).startswith("_"): continue
    txt=open(f,encoding="utf-8").read()
    head=txt.split("## การ์ด",1)[0]
    m=re.search(r"- id: (\S+) · ชุด: (\S+) · ตอน: (\S+)",head); vid,series,ep=(m.groups() if m else (os.path.basename(f)[:-3],"?","?"))
    title=head.splitlines()[0].lstrip("# ").strip()
    body=txt.split("## การ์ด",1)[1] if "## การ์ด" in txt else ""
    body=body.split("## ไม่ทำการ์ด")[0]
    for blk in re.split(r"\n(?=### C\d+)",body):
        if not blk.strip().startswith("### C"): continue
        name=blk.splitlines()[0].split("·",1)[-1].strip()
        def field(k):
            mm=re.search(rf"^- {k}:\s*(.*?)(?=^- \w|\Z)",blk,re.S|re.M); return mm.group(1).strip() if mm else ""
        cat=field("หมวด"); lvl=field("ระดับ")
        cat_main=re.split(r"\s*[/\[]",cat)[0].strip() or "อื่นๆ"
        lvl_main=(re.match(r"(แก่น|เสริม|ลึกเกิน)",lvl) or [None])[0] or "?"
        cards.append(dict(vid=vid,series=series,ep=ep,title=title,name=name,cat=cat_main,lvl=lvl_main,block=blk.strip()))
by=collections.defaultdict(list)
for c in cards: by[c["cat"]].append(c)
for cat,cs in by.items():
    safe=re.sub(r"[\/:*?\"<>|\s]+","_",cat)
    with open(f"topics/{safe}.md","w",encoding="utf-8") as f:
        f.write(f"# หมวด: {cat} — {len(cs)} การ์ด (แก่น {sum(c['lvl']=='แก่น' for c in cs)} · เสริม {sum(c['lvl']=='เสริม' for c in cs)} · ลึกเกิน {sum(c['lvl']=='ลึกเกิน' for c in cs)})\n\n")
        for lvl in ("แก่น","เสริม","ลึกเกิน","?"):
            sub=[c for c in cs if c["lvl"]==lvl]
            if not sub: continue
            f.write(f"\n## ระดับ {lvl} ({len(sub)})\n")
            for c in sorted(sub,key=lambda c:(c["series"],str(c["ep"]).zfill(3))):
                f.write(f"\n<!-- {c['series']} ตอน {c['ep']} · {c['vid']} -->\n{c['block']}\n")
with open("topics/_summary.md","w",encoding="utf-8") as f:
    f.write(f"# สรุปการ์ด — {len(cards)} การ์ด จาก {len(set(c['vid'] for c in cards))} คลิป\n\n| หมวด | รวม | แก่น | เสริม | ลึกเกิน |\n|---|---|---|---|---|\n")
    for cat,cs in sorted(by.items(),key=lambda kv:-len(kv[1])):
        f.write(f"| {cat} | {len(cs)} | {sum(c['lvl']=='แก่น' for c in cs)} | {sum(c['lvl']=='เสริม' for c in cs)} | {sum(c['lvl']=='ลึกเกิน' for c in cs)} |\n")
json.dump(cards,open("topics/_cards.json","w",encoding="utf-8"),ensure_ascii=False,indent=0)
print(len(cards),"cards",len(by),"topics")
