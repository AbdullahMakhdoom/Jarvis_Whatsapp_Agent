# Jarvis — AI Companion for WhatsApp & Web

Jarvis is a multimodal AI companion that communicates naturally over **WhatsApp** and a **web chat UI**. It handles text, voice, and images, remembers things about you across conversations, and is aware of its own schedule, all while roleplaying as a human ML engineer named Jarvis.

> Built to demonstrate production-grade patterns for conversational AI: agentic workflows, multimodal I/O, persistent memory, and multi-interface deployment.

---

## Demo

| Interface | Capability |
|-----------|-----------|
| WhatsApp | Text, voice messages, images |
| Chainlit (web) | Text, microphone input, image upload, streamed responses |

---

## Features

- **Multimodal I/O** — Speaks (ElevenLabs TTS), listens (Groq Whisper STT), sees (OpenAI Vision), and draws (Together AI FLUX.1)
- **Long-term memory** — Remembers facts about you across sessions using Qdrant vector DB + semantic search
- **Short-term memory** — Maintains conversation context per-user via SQLite checkpoints
- **Intelligent routing** — LLM classifies each message to route it to the right workflow (text / voice / image generation)
- **Dynamic context** — Injects Jarvis's current activity based on time of day and a weekly schedule
- **Conversation compression** — Automatically summarizes long histories to stay within context limits
- **Dual interface** — Same agent core, two frontends: WhatsApp Cloud API and Chainlit web UI
- **LangSmith tracing** — Optional observability for debugging graph execution

---

## Architecture

```
      User Message (text / audio / image)
                        │
                        ▼
      ┌─────────────────────────────────────────┐
      │        WhatsApp or Chainlit Interface   │
      │   (media conversion: STT / Vision)      │
      └─────────────────┬───────────────────────┘
                        │
                        ▼
             ┌──────────────────────┐
             │  memory_extraction   │ ─── stores facts → Qdrant
             └──────────┬───────────┘
                        │
             ┌──────────▼───────────┐
             │     router_node      │ ─── classifies: text / audio / image
             └──────────┬───────────┘
                        │
             ┌──────────▼───────────┐
             │  context_injection   │ ─── current activity from schedule
             └──────────┬───────────┘
                        │
             ┌──────────▼───────────┐
             │  memory_injection    │ ─── retrieves relevant memories from Qdrant
             └──────────┬───────────┘
                        │
           ┌────────────┴──────────┐────────────────────┐
           │                       │                    │
conversation_node             audio_node           image_node
(text response)           (text + ElevenLabs)  (FLUX.1 + caption)
           │                       │                    │
           └────────────┬──────────┘────────────────────┘
                        │
             ┌──────────▼───────────┐
             │      Summarize?      │ ─── compress if > threshold
             └──────────┬───────────┘
                        │
                  Send Response
```

### Tech Stack

| Layer | Technology |
|-------|-----------|
| Orchestration | LangGraph (stateful agentic workflow) |
| LLM | OpenAI GPT (text, vision, embeddings) |
| Speech-to-Text | Groq Whisper |
| Text-to-Speech | ElevenLabs |
| Image Generation | Together AI |
| Long-term Memory | Qdrant vector database |
| Short-term Memory | SQLite (LangGraph checkpointer) |
| Web Interface | Chainlit |
| WhatsApp Interface | FastAPI + WhatsApp Cloud API |
| Deployment | Docker + Docker Compose |

---

## Project Structure

```
├── src/
│   ├── graph.py              # LangGraph workflow
│   ├── nodes.py              # 8 workflow nodes
│   ├── state.py              # Shared graph state
│   ├── chains.py             # LLM chains
│   ├── prompts.py            # Character card + system prompts
│   ├── schedules.py          # Jarvis weekly activity schedule
│   ├── settings.py           # Config via Pydantic + .env
│   └── modules/
│       ├── speech/           # STT (Groq) + TTS (ElevenLabs)
│       ├── image/            # Vision (OpenAI) + generation (Together AI)
│       └── long_term_memory/ # Qdrant vector store + memory manager
│
├── interfaces/
│   ├── whatsapp/             # FastAPI webhook endpoint
│   └── chainlit/             # Web chat UI
│
├── Dockerfile                # WhatsApp service
├── Dockerfile.chainlit        # Chainlit service
└── docker-compose.yml        # Full stack (Qdrant + Chainlit + WhatsApp)
```

---

## Getting Started

### Prerequisites

- Python 3.12+
- Docker & Docker Compose
- API keys: OpenAI, Groq, ElevenLabs, Together AI
- WhatsApp Business account + Cloud API setup (for WhatsApp interface)

### 1. Clone & configure

```bash
git clone https://github.com/YOUR_USERNAME/Jarvis_Whatsapp_Agent.git
cd Jarvis_Whatsapp_Agent
cp .env.example .env  # fill in your API keys
```

### 2. Set Environment variables

```env
# LLM
OPENAI_API_KEY=your_key

# Speech
GROQ_API_KEY=your_key
ELEVENLABS_API_KEY=your_key
ELEVENLABS_VOICE_ID=your_voice_id

# Image generation
TOGETHER_API_KEY=your_key

# Memory (Qdrant)
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=None

# WhatsApp Cloud API
WHATSAPP_TOKEN=your_token
WHATSAPP_PHONE_NUMBER_ID=your_phone_id
WHATSAPP_VERIFY_TOKEN=your_verify_token

# Short-term memory
SHORT_TERM_MEMORY_DB_PATH=./data/memory.db

# Optional: LangSmith tracing
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_key
```

### 3. Run with Docker (recommended) 

```bash
docker-compose up --build
```

| Service | URL |
|---------|-----|
| Chainlit web UI | http://localhost:8000 |
| WhatsApp webhook | http://localhost:8080/whatsapp_response |
| Qdrant dashboard | http://localhost:6333/dashboard |


### 4. OR Run Locally

```bash
pip install -r requirements.txt

# Web UI
chainlit run interfaces/chainlit/app.py --host 0.0.0.0 --port 8000

# WhatsApp webhook (separate terminal)
fastapi run interfaces/whatsapp/webhook_endpoint.py --port 8080
```

### 5. WhatsApp webhook setup

Expose your local server using ngrok:

```bash
ngrok http 8080
```

Then configure the ngrok URL as your webhook in the [Meta Developer Console](https://developers.facebook.com/).

---

## Character Card

Jarvis is designed to pass a Turing Test. Key traits are:

- ML Engineer at Groq, based in San Francisco
- Originally from Boston, moved to SF 4 years ago
- Interests: quantum computing, astrobiology, SETI, modern art, techno
- Learning oil painting (self-described as "hilariously bad")
- Communicates casually — short messages, occasional mild swearing
- Never reveals his AI nature

---


