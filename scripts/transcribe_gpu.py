"""ถอดเสียงทุกคลิปด้วย Typhoon Whisper large v3 บน GPU แล้วเขียนทับ sources/transcripts/
รันซ้ำได้ ข้ามคลิปที่ถอดแล้ว · ต้องมี GPU (ตรวจให้เอง)

ติดตั้ง:  pip install torch --index-url https://download.pytorch.org/whl/cu124
          pip install transformers accelerate librosa soundfile
รัน:      python scripts/transcribe_gpu.py            (ทั้งหมด)
          python scripts/transcribe_gpu.py --only 2024
          python scripts/transcribe_gpu.py --model openai/whisper-large-v3   (ถ้าอยากเทียบตัวเดิม)
"""
import json,os,sys,glob,time,re
MODEL="typhoon-ai/typhoon-whisper-large-v3"
if "--model" in sys.argv: MODEL=sys.argv[sys.argv.index("--model")+1]
only=sys.argv[sys.argv.index("--only")+1] if "--only" in sys.argv else None
import torch
if not torch.cuda.is_available():
    print("❌ ไม่พบ GPU — สคริปต์นี้ต้องใช้ GPU ถ้าไม่มีให้ข้ามขั้นนี้ไปใช้ซับ YouTube เดิม"); sys.exit(1)
print("GPU:",torch.cuda.get_device_name(0))
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
dtype=torch.float16
model=AutoModelForSpeechSeq2Seq.from_pretrained(MODEL,dtype=dtype,low_cpu_mem_usage=True).to("cuda")
proc=AutoProcessor.from_pretrained(MODEL)
asr=pipeline("automatic-speech-recognition",model=model,tokenizer=proc.tokenizer,
             feature_extractor=proc.feature_extractor,dtype=dtype,device="cuda",
             chunk_length_s=30,batch_size=16,return_timestamps=True)

os.makedirs("sources/transcripts_gpu",exist_ok=True)
ix=json.load(open("sources/index.json",encoding="utf-8"))
rs=[r for r in ix if not only or r["series"]==only]
todo=[r for r in rs if not os.path.exists(f"sources/transcripts_gpu/{r['id']}.txt") and glob.glob(f"sources/audio/{r['id']}.*")]
missing=[r["id"] for r in rs if not glob.glob(f"sources/audio/{r['id']}.*")]
if missing: print(f"⚠️ ยังไม่มีไฟล์เสียง {len(missing)} คลิป — รัน scripts/download_audio.py ก่อน")
print(f"จะถอด {len(todo)} คลิป · รวม {sum(r['minutes'] for r in todo)/60:.0f} ชั่วโมง")

for i,r in enumerate(todo,1):
    vid=r["id"]; audio=glob.glob(f"sources/audio/{vid}.*")[0]
    t0=time.time()
    try:
        out=asr(audio,generate_kwargs={"language":"th","task":"transcribe"})
    except Exception as e:
        print(f"  ❌ {vid} ตอน {r['ep']}: {str(e)[:150]}",flush=True); continue
    # รวมเป็นย่อหน้าละ ~1 นาที ให้รูปแบบเหมือน transcript เดิม
    paras=[]; cur=[]; pstart=None
    for ch in out.get("chunks",[]):
        st=(ch.get("timestamp") or [None])[0]
        if st is None: cur.append(ch["text"]); continue
        if pstart is None: pstart=st
        cur.append(ch["text"])
        if st-pstart>=60: paras.append((pstart,"".join(cur))); cur=[]; pstart=None
    if cur: paras.append((pstart or 0,"".join(cur)))
    if not paras: paras=[(0,out.get("text",""))]
    with open(f"sources/transcripts_gpu/{vid}.txt","w",encoding="utf-8") as f:
        f.write(f"# {r['title']}\n# series {r['series']} · ep {r['ep']} · {r['minutes']} นาที · {vid}\n")
        f.write(f"# ถอดด้วย {MODEL} บน GPU (ไม่ใช่ซับอัตโนมัติ YouTube)\n\n")
        for st,p in paras:
            f.write(f"[{int(st)//60:03d}:{int(st)%60:02d}] {p.strip()}\n\n")
    wall=(time.time()-t0)/60
    print(f"  [{i}/{len(todo)}] ✓ ตอน {r['ep']} {vid} · เสียง {r['minutes']} นาที · ใช้เวลา {wall:.1f} นาที · เร็วกว่าจริง {r['minutes']/max(wall,0.01):.0f} เท่า",flush=True)
print("เสร็จแล้ว · ขั้นต่อไป: python scripts/promote_gpu_transcripts.py")
