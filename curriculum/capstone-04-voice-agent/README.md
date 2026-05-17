# Capstone 4 — Voice-First Agent

**XP:** 750  
**Difficulty:** Advanced  
**Requires:** Levels 1–9 (streaming, production, tool calling)  
**Estimated build time:** 3–4 days  
**API cost:** ~$0.05–0.20 per conversation (STT + LLM + TTS combined)

---

## Why This Exists

Text is the default interface for AI agents. It shouldn't be.

Most people don't type to each other — they talk. Voice is faster, more natural, and more accessible. And since 2023, voice AI has crossed a threshold: with the right architecture, you can build a voice agent that responds in under 800ms, handles interruptions, and sounds natural enough that users forget they're talking to a machine.

The companies moving fastest on AI are moving to voice: customer service agents that handle calls without human agents, accessibility tools that let people who can't type use computers, automotive interfaces, healthcare intake systems. The voice AI market is growing faster than the text AI market because the use cases are wider.

Most AI engineers know nothing about building voice systems. This capstone changes that.

---

## What This Unlocks

**Roles:**
- Voice AI Engineer (dedicated role at companies like Vapi, ElevenLabs, Bland AI)
- Conversational AI Engineer at enterprise software companies
- AI Product Engineer building accessibility or customer service tools
- Freelance AI developer (voice agents for small business customer service is a real market right now)

**Projects you can pitch after this:**
- A voice agent for any small business that replaces a phone receptionist
- An accessibility tool that lets people navigate software by speaking
- A voice interface for the Learning Coach from Capstone 3
- A multilingual voice agent (Japanese + English — relevant to CareerSync's user base)

**What you can say:** "I built a real-time voice AI system with sub-800ms response latency. Here's how I handled streaming, interruption detection, and the tradeoff between latency and quality."

---

## The System

Build a voice-first AI agent that:

1. Listens to the user via microphone
2. Detects when they've stopped speaking (Voice Activity Detection)
3. Transcribes speech to text in near real-time
4. Routes the transcribed text to an LLM agent
5. Streams the LLM response to a Text-to-Speech engine
6. Plays the response while handling interruptions — if the user starts talking mid-response, the agent stops and listens

The hard parts are not the happy path. They are:
- **Latency** — every step adds delay. The architecture must minimise it.
- **Interruption handling** — a natural conversation allows the user to cut in. Most implementations don't handle this, which makes them feel robotic.
- **Streaming** — you can't wait for the full LLM response before starting TTS. You need to start speaking the first sentence while the rest is still generating.

---

## Technologies

| Layer | Technology | Why |
|-------|-----------|-----|
| Speech-to-Text | OpenAI Whisper (local) or Deepgram (API) | Whisper is free and accurate; Deepgram is faster (lower latency) |
| Voice Activity Detection | Silero VAD or WebRTC VAD | Detects speech start/stop without transcribing silence |
| LLM | Claude Haiku or GPT-4o-mini | Low latency response; use streaming mode |
| Text-to-Speech | ElevenLabs (quality) or Coqui TTS (free, local) | ElevenLabs sounds better; Coqui costs nothing |
| Audio I/O | PyAudio or sounddevice | Microphone capture and speaker output |
| Streaming | asyncio + WebSockets | Concurrent STT → LLM → TTS pipeline |

**The latency budget (target: under 800ms end-to-end):**
- VAD detects end of speech: ~50ms
- STT transcription: ~200ms (Deepgram streaming) or ~400ms (Whisper)
- LLM first token: ~200ms (Haiku streaming)
- TTS first audio chunk: ~150ms
- **Total: ~600–800ms if implemented correctly**

---

## Research Areas

- **Streaming LLM inference** — how partial outputs are generated token by token and how to pipe them directly to TTS
- **Voice Activity Detection** — how models distinguish speech from noise and detect sentence boundaries
- **Turn-taking in conversation** — the linguistics of when it's your turn to speak, and how to model this computationally
- **Duplex communication** — architectures where both parties can speak simultaneously (like a real phone call, not walkie-talkie)
- **Neural TTS quality** — what makes synthesised speech sound natural vs robotic

**Papers worth reading:**
- "Whisper: Robust Speech Recognition via Large-Scale Weak Supervision" — OpenAI
- "Real-Time Voice Cloning" — CorentinJ (GitHub) — understanding TTS architecture
- Google Duplex (2018) — the original demo of natural voice AI

---

## Agent Team

| Agent | Role |
|-------|------|
| Audio Capture Agent | Continuously reads microphone input in chunks. Forwards to VAD. |
| VAD Agent | Analyses audio chunks for speech presence. Fires "speech ended" event when silence detected after speech. |
| STT Agent | Receives audio segment, returns transcribed text. Handles noise and accents. |
| Intent Router | Classifies the transcribed text — is this a question, a command, a follow-up? Routes to the right handler. |
| Response Agent | Core LLM agent. Generates response in streaming mode. Chunks output into sentences for TTS. |
| TTS Agent | Converts each sentence chunk to audio as it arrives. Queues audio for playback. |
| Interruption Monitor | Runs in parallel with TTS playback. If VAD detects speech during playback, cancels the TTS queue and restarts the pipeline. |

---

## Build Stages

### Part A — Audio Pipeline (no AI yet)
Get microphone input → VAD → audio segmentation → playback working end-to-end. No LLM, no TTS. Just: detect when someone speaks, record that segment, play it back. If this isn't clean, everything downstream will be broken.

### Part B — STT Integration
Add Whisper or Deepgram. Transcribe the recorded segments. Measure accuracy on your own voice. Test with background noise. Log every transcription — you'll need this for debugging later.

### Part C — LLM in Streaming Mode
Add the LLM. Use streaming mode — you receive tokens as they generate, not the complete response. Split on sentence boundaries. Do not start TTS until you have a complete sentence (minimum unit for natural-sounding speech).

### Part D — TTS Integration
Add TTS. Stream sentence chunks from the LLM into TTS as they complete. Measure the end-to-end latency from the user finishing speaking to the first audio output. Target: under 800ms. Log every step — you need to know where the time is going.

### Part E — Interruption Handling
This is the hardest part. Run the VAD in parallel with TTS playback. When VAD detects speech during playback:
1. Stop TTS playback immediately
2. Cancel any pending TTS queue
3. Record the new speech
4. Restart the pipeline from STT

Test this rigorously. A voice agent that can't be interrupted feels broken.

### Part F — Evaluation & Reflection
Measure: latency distribution (p50, p95), interruption detection accuracy, STT accuracy on 20 test phrases, naturalness score (play recordings to 3 people, ask them to rate 1–5).

Write a 300-word reflection: What was the hardest architectural decision? What tradeoffs did you make between latency and quality? Where would this break with 100 concurrent users?

---

## Completion Checklist

- [ ] Audio pipeline working: VAD detects speech, segments correctly
- [ ] STT integrated, accuracy tested on 20+ phrases
- [ ] LLM in streaming mode, sentence-chunked output
- [ ] TTS streaming from LLM output, not waiting for full response
- [ ] End-to-end latency measured: first audio out under 800ms
- [ ] Interruption handling: user speaking mid-response stops playback and restarts
- [ ] Latency logged per stage (STT / LLM first token / TTS first chunk)
- [ ] Tested with background noise
- [ ] Reflection write-up complete

---

## What Completing This Demonstrates

- You understand streaming architecture across multiple I/O layers simultaneously
- You can manage real-time concurrent pipelines (VAD running while TTS plays)
- You think about latency as a design constraint, not an afterthought
- You've built a modality that most AI engineers have never touched

Voice agents are one of the highest-value AI products right now. Most are bad because the engineers who build them don't understand the architecture. You will.
