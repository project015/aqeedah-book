import fitz,glob,os,sys
for pdf in sorted(glob.glob("sources/docs/*.pdf")):
    out=pdf[:-4]+".md"
    if os.path.exists(out): continue
    d=fitz.open(pdf); parts=[f"# {os.path.basename(pdf)} · {len(d)} หน้า"]; blank=0
    for i,p in enumerate(d):
        t=p.get_text().strip()
        if not t: blank+=1
        parts.append(f"\n## หน้า {i+1}" + (" (ไม่มีข้อความ เป็นรูปล้วน)" if not t else "") + "\n" + t)
    parts[0]+=f" · หน้าที่ไม่มีข้อความ {blank}"
    open(out,"w",encoding="utf-8").write("\n".join(parts)); print(out,len(d),"pages, blank",blank)
