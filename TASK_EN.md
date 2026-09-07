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
11. Commit after roughly every 5 new clips, in Thai, then TRY `git push`.
    - If the push succeeds, you have been added as a collaborator. Push on every commit from then
      on, so the owner sees progress arrive and can pull partial results without waiting.
    - If it fails with 403 / permission denied, you have not been invited. Do not retry. Keep
      committing locally and zip the `cards/` folder back at the end.
      Never pause the work waiting for access — just carry on.

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

DELIVERING THE WORK BACK — read all of this, do not send only the cards

TWO things must come back, not one:
1. cards/ — all the extracted idea cards (the main product)
2. sources/transcripts/ — the GPU re-transcribed text. THIS MATTERS.
   The project owner's machine has no GPU and cannot regenerate this set. If it does not come
   back it is gone for good, and both evidence-checking and the actual book writing fall back to
   the poor YouTube auto-captions.
3. sources/transcripts_gpu/ as well, if it still exists.

Do NOT send back: sources/audio/ (about 10 GB, re-downloadable), the evidence/ Quran and hadith
databases (restore_evidence.py fetches them), sources/raw/, sources/docs/*.pdf

How to send — pick one:

OPTION A (best) push to GitHub. If `git push` works, nothing else is needed. Both cards and
transcripts are tracked in git. Make a final push and tell the owner you are done.

OPTION B zip to Google Drive, if push does not work.
1. Zip both folders together, keeping the folder structure (do not zip the loose files):
     aqeedah-work.zip
       cards/
       sources/transcripts/
2. Upload to Google Drive
3. IMPORTANT: set sharing to "Anyone with the link". If it stays restricted, the owner's side
   downloads an HTML login page instead of the file.
4. Send the link to the owner along with the five-point closing report below.

Do not send through LINE or chat apps — files get recompressed or expire.

CLOSING REPORT — cover all five points
1. how many clips have cards, out of how many total, and the total card count
2. whether GPU re-transcription completed, which model, and which clips failed
3. how many old cards were redone in phase 2, and how many still come from the YouTube captions
4. which clips had audio or captions bad enough that someone should listen to the real audio
   during evidence verification
5. anything blocked, undone, or that you are unsure about. Say it plainly rather than staying quiet.
