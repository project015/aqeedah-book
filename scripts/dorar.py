"""ค้น dorar.net (สถานะหะดีษตามนักหะดีษ): dorar.py "إنما الأعمال بالنيات" [max]"""
import sys,json,re,html,subprocess,urllib.parse
q=sys.argv[1]; mx=int(sys.argv[2]) if len(sys.argv)>2 else 8
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128 Safari/537.36"
url="https://dorar.net/dorar_api.json?skey="+urllib.parse.quote(q)
r=subprocess.run(["curl","-s","-A",UA,url],capture_output=True,text=True,encoding="utf-8").stdout
try: t=json.loads(r)["ahadith"]["result"]
except Exception: print("ERR",r[:300]); sys.exit(1)
t=re.sub(r"<[^>]+>"," ",html.unescape(t)); t=re.sub(r"[ \t]+"," ",t)
items=[i.strip() for i in t.split("--------------") if i.strip()]
for i in items[:mx]:
    i=re.sub(r"\n\s*\n+","\n",i); print(i.strip()); print("—")
print(f"(รวม {len(items)} รายการในหน้าแรก)")
