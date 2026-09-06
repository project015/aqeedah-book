"""โหลดไฟล์เสียงทุกคลิปเพื่อเอาไปถอดด้วย GPU — python scripts/download_audio.py [--only 2020|2024]
ข้ามคลิปที่มีไฟล์อยู่แล้ว รันซ้ำได้ ราว 10 GB ทั้งหมด"""
import json,os,subprocess,sys,glob
only=None
if "--only" in sys.argv: only=sys.argv[sys.argv.index("--only")+1]
os.makedirs("sources/audio",exist_ok=True)
ix=json.load(open("sources/index.json",encoding="utf-8"))
rs=[r for r in ix if not only or r["series"]==only]
print(f"เป้าหมาย {len(rs)} คลิป · รวม {sum(r['minutes'] for r in rs)/60:.0f} ชั่วโมง")
ok=skip=fail=0
for i,r in enumerate(rs,1):
    vid=r["id"]
    if glob.glob(f"sources/audio/{vid}.*"): skip+=1; continue
    p=subprocess.run(["yt-dlp","--no-warnings","-q","-f","bestaudio","-o",f"sources/audio/{vid}.%(ext)s",
                      f"https://www.youtube.com/watch?v={vid}"],capture_output=True,text=True)
    if glob.glob(f"sources/audio/{vid}.*"): ok+=1
    else: fail+=1; print(f"  ล้มเหลว {vid} ตอน {r['ep']}: {p.stderr.strip()[:120]}")
    if i%10==0: print(f"  [{i}/{len(rs)}] โหลดใหม่ {ok} · มีอยู่แล้ว {skip} · ล้มเหลว {fail}",flush=True)
print(f"เสร็จ: โหลดใหม่ {ok} · มีอยู่แล้ว {skip} · ล้มเหลว {fail}")
