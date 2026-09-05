import sys,time,json
from faster_whisper import WhisperModel
vid=sys.argv[1]; model_name=sys.argv[2] if len(sys.argv)>2 else "large-v3"
t0=time.time()
m=WhisperModel(model_name,device="cpu",compute_type="int8",cpu_threads=16)
segs,info=m.transcribe(next(str(p) for p in __import__("pathlib").Path("sources/audio").glob(vid+".*") if p.suffix in (".m4a",".webm",".opus",".mp3",".wav")),language="th",beam_size=1,vad_filter=True)
out=[]
with open(f"sources/audio/{vid}_{model_name}.txt","w",encoding="utf-8") as f:
    for s in segs:
        f.write(f"[{int(s.start)//60:02d}:{int(s.start)%60:02d}] {s.text.strip()}\n"); f.flush()
print("done",vid,model_name,"audio_min",round(info.duration/60,1),"wall_min",round((time.time()-t0)/60,1))
