"""ย้าย transcript ที่ถอดด้วย GPU มาเป็นตัวหลัก และสำรองของเดิมไว้
ถ้าคลิปไหนมีการ์ดอยู่แล้ว จะเตือนว่าการ์ดนั้นสกัดจากซับเก่า อาจอยากรื้อทำใหม่"""
import os,glob,shutil,json
os.makedirs("sources/transcripts_ytsub",exist_ok=True)
moved=0; had_cards=[]
for f in sorted(glob.glob("sources/transcripts_gpu/*.txt")):
    vid=os.path.basename(f)[:-4]
    old=f"sources/transcripts/{vid}.txt"
    if os.path.exists(old): shutil.copy2(old,f"sources/transcripts_ytsub/{vid}.txt")
    shutil.copy2(f,old); moved+=1
    if os.path.exists(f"cards/{vid}.md"): had_cards.append(vid)
print(f"ย้าย transcript แล้ว {moved} คลิป (ของเดิมสำรองไว้ที่ sources/transcripts_ytsub/)")
if had_cards:
    print(f"\n⚠️ {len(had_cards)} คลิปนี้มีการ์ดอยู่แล้ว ซึ่งสกัดมาจากซับเก่าที่คุณภาพแย่กว่า:")
    print("   "+" ".join(had_cards))
    print("   ถ้าโควตาเหลือ ควรรื้อทำใหม่จาก transcript ใหม่ (ลบไฟล์การ์ดแล้วรัน next_batch.py จะขึ้นมาเอง)")
