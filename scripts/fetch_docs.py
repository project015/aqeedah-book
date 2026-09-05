import json,re,os,subprocess
ix=json.load(open("sources/index.json",encoding="utf-8"))
os.makedirs("sources/docs",exist_ok=True)
for r in ix:
    for i,u in enumerate(r["drive_links"]):
        m=re.search(r"/d/([\w-]+)",u); 
        if not m: print("skip",u); continue
        fid=m.group(1); out=f"sources/docs/{r['series']}_ep{r['ep']:02d}{'_'+str(i) if i else ''}.pdf"
        if os.path.exists(out) and os.path.getsize(out)>1000: continue
        subprocess.run(["curl","-sL","-o",out,f"https://drive.usercontent.google.com/download?id={fid}&export=download&confirm=t"])
        print(out,os.path.getsize(out))
