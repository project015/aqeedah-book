# Task — read this and start

Do every step yourself, end to end. Keep going until every clip is done or the owner stops you.

ON STOPPING TO ASK — be precise about this
Never stop to ask permission for routine work: launching the next clip, committing, continuing
after a usage limit. Just do it, and resume on your own when a limit resets.

But DO stop and report immediately if you hit any of these five, because they mean an assumption
behind the job is broken rather than something merely being slow:
1. transcripts missing or corrupted across more than 5 clips
2. more than 5 clips deleted or private on YouTube so audio cannot be fetched
3. subagents returning malformed output on 3 consecutive clips despite following the template
4. out of disk space, or GPU out of memory so transcription cannot run
5. anything requiring you to delete files beyond the card-redo procedure described here

SETUP (one time — skip any step already done)
1. pip install yt-dlp pymupdf
3. Copy the folder _skill/research-book to ~/.claude/skills/research-book
4. Run: python scripts/restore_evidence.py   (re-downloads the Quran and hadith databases)
5. Read STATE.md and HANDOFF.md in full before starting. They are in Thai — read them anyway,
   they carry all the agreed rules.

STEP 0 — RE-TRANSCRIBE ON GPU FIRST (do this before extracting any cards)
If this machine has a GPU, always do this first. It costs zero Claude quota and improves everything
downstream. The transcripts currently in the repo are YouTube auto-captions: roughly 60% readable,
Arabic terms wrong almost everywhere, page and verse numbers mangled.

A. pip install torch --index-url https://download.pytorch.org/whl/cu124
   pip install transformers accelerate librosa soundfile
B. python scripts/download_audio.py        (fetches audio for all 114 clips, about 10 GB, resumable)
C. python scripts/transcribe_gpu.py        (Typhoon Whisper large v3, Thai-tuned on 11,000 hours)
   Leave it running overnight. It prints its realtime speed factor. Resumable.
D. python scripts/promote_gpu_transcripts.py   (makes the new transcripts primary, backs up the old)
E. Then continue from step 5 below.

If there is no GPU, skip step 0 entirely and extract from the existing transcripts.

Note: passages where the teacher recites Quran in Arabic will still come out garbled, because the
model is tuned on Thai speech. That is fine — Arabic source text is pulled from standard databases
during the evidence-verification stage. What improves sharply is Thai prose, scholar names, book
titles and numbers, which is most of the problem.

THE JOB: extract "idea cards" from the remaining lecture clips. 80 clips are left.
6. Run: python scripts/next_batch.py 6   to see which clips still have no cards
7. Take the template in scripts/EXTRACT_PROMPT.md, fill in every {PLACEHOLDER}, and spawn one
   subagent per clip with the Agent tool, passing model: "opus" on every single one.
   Never leave the model unset and never use sonnet. Run 6 in parallel.
   Write the clip ids you are currently working on into cards/_inflight.txt so you never
   launch the same clip twice.
8. When a subagent finishes, verify two things before counting that clip as done:
   - the card file ends with a "## ไม่ทำการ์ด" section
   - the last card's time range reaches close to the clip's full length
   If either is missing the subagent died mid-write. Re-run that whole clip from scratch.
   If both are fine, remove the id from cards/_inflight.txt and launch a new clip in its place.
9. Loop like this until next_batch.py reports 0 clips remaining.
10. If you hit a usage limit, resume the moment it resets. Do not wait for me to tell you.
    Subagents killed by a limit often wrote their file already but incompletely, so always
    apply the check in step 8 before deciding whether to redo a clip.
11. Commit after roughly every 5 new clips, in Thai. Local commits only — do not push, you have
    no write access to the repo. Commits are just restore points.

IMPORTANT: the card files themselves must be written in Thai, following scripts/CARD_FORMAT.md
exactly. Only your conversation with me is in English.

DO NOT
- Do not start writing the book. The project owner approves the outline first.
- Do not edit or delete any card file that already exists in cards/
- Do not use sonnet for subagents. It was tested and it silently drops the evidence field,
  which is the single most important field in this project.
- Do not drop any topic during extraction, even material too advanced for a new Muslim.
  Label it "ลึกเกิน" (too deep) instead. Filtering happens later, when the book is written.

IF YOU DID STEP 0 — redo the old cards in this fixed order
The 34 existing card files came from the older, worse transcripts. promote_gpu_transcripts.py
prints exactly which ones. Do not try to judge whether "quota allows" — you cannot measure that.
Just work down this list until it is finished or you are told to stop.

- PHASE 1: extract the 80 clips that have no cards. Do not touch phase 2 until next_batch.py
  reports 0 remaining.
- PHASE 2: redo the old cards, in this priority order, one clip at a time exactly as in phase 1:
  1. series 2020 episodes 11-28 (tawhid, shirk, angels — the core of the book)
  2. series 2020 episodes 1-10 (introduction, why study creed, proofs of God)
  3. everything else
  To redo a clip: delete its card file and next_batch.py will offer it again.
  Commit once before deleting, so the old version can be recovered if the new one comes out worse.
- If a usage limit interrupts either phase, continue from where you were once it resets.

When everything is done, report: how many clips, how many cards, and which clips had subtitles
so poor that someone will need to go back and listen to the actual audio.
