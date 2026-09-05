"""ค้นอัลกุรอาน: quran.py 2:255  |  quran.py 56:58-59  |  quran.py --th "น้ำอสุจิ"  |  quran.py --ar "خلق"  (ตัวบทจาก alquran.cloud uthmani + แปลไทย)"""
import json,sys,re,unicodedata
AR=json.load(open("evidence/quran/quran-uthmani.json",encoding="utf-8"))["data"]["surahs"]
TH=json.load(open("evidence/quran/quran-th.json",encoding="utf-8"))["data"]["surahs"]
def strip_ar(s): return "".join(c for c in unicodedata.normalize("NFD",s) if not unicodedata.combining(c) and c not in "ـۣۖۗۘۙۚۛۜ۟۠ۡۢۤۥۦۧۨ۩۪ۭ۫۬").replace("ٱ","ا").replace("أ","ا").replace("إ","ا").replace("آ","ا").replace("ى","ي").replace("ة","ه")
def show(si,ai):
    s=AR[si-1]; a=s["ayahs"][ai-1]; t=TH[si-1]["ayahs"][ai-1]["text"]
    print(f"ซูเราะฮ์{s['englishName']} / {s['name']} ({si}) : {ai}\n{a['text']}\n{t}\n")
args=sys.argv[1:]
if args and args[0]=="--th":
    q=args[1]; n=0
    for si,s in enumerate(TH,1):
        for ai,a in enumerate(s["ayahs"],1):
            if q in a["text"]: show(si,ai); n+=1
            if n>=int(args[2]) if len(args)>2 else n>=15: sys.exit()
elif args and args[0]=="--ar":
    q=strip_ar(args[1]); n=0
    for si,s in enumerate(AR,1):
        for ai,a in enumerate(s["ayahs"],1):
            if q in strip_ar(a["text"]): show(si,ai); n+=1
            if n>=15: sys.exit()
else:
    for ref in args:
        m=re.match(r"(\d+):(\d+)(?:-(\d+))?$",ref); si,a1,a2=int(m.group(1)),int(m.group(2)),int(m.group(3) or m.group(2))
        for ai in range(a1,a2+1): show(si,ai)
