"""ค้นหะดีษอาหรับ (ไม่สนสระ): hadith.py "انما الاعمال بالنيات" [max]  · หรือ hadith.py bukhari 1  (ฐาน fawazahmed0/hadith-api: bukhari muslim abudawud tirmidhi nasai ibnmajah malik nawawi qudsi dehlawi)"""
import json,sys,glob,os,unicodedata,re
def strip_ar(s): 
    s="".join(c for c in unicodedata.normalize("NFD",s) if not unicodedata.combining(c))
    return re.sub(r"[ـ]","",s).replace("أ","ا").replace("إ","ا").replace("آ","ا").replace("ى","ي").replace("ة","ه")
DB={}
for f in glob.glob("evidence/hadith/ara-*.json"):
    DB[os.path.basename(f)[4:-5]]=json.load(open(f,encoding="utf-8"))["hadiths"]
a=sys.argv[1:]
if a and a[0] in DB:
    h=[x for x in DB[a[0]] if x["hadithnumber"]==int(a[1])]; print(a[0],a[1]); print(h[0]["text"] if h else "ไม่พบ"); sys.exit()
q=strip_ar(" ".join(a[:1])); mx=int(a[1]) if len(a)>1 else 10; n=0
for book,hs in DB.items():
    for h in hs:
        if q in strip_ar(h["text"]):
            print(f"[{book} #{h['hadithnumber']}] {h['text'][:400]}\n"); n+=1
            if n>=mx: sys.exit()
print("พบ",n)
