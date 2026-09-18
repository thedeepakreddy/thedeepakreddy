<!-- Profile README · Gorisi Deepak Reddy -->

<div align="center">

# Gorisi Deepak Reddy

### Business-aware AI Systems Engineer · Agentic AI · Multimodal Computer Use · Data & ML

<a href="https://github.com/thedeepakreddy"><img src="https://img.shields.io/badge/GitHub-thedeepakreddy-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"/></a>
<a href="https://www.linkedin.com/in/deepak-reddy-038582223/"><img src="https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"/></a>
<a href="mailto:thedeepakreddy1@gmail.com"><img src="https://img.shields.io/badge/Email-Contact-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Email"/></a>

**Budapest, Hungary · Open to AI, ML, Data, Analytics and AI Product roles across the EU and internationally**

</div>

---

## About me

I am a **Computer Science Engineering graduate** with an **MSc in Business Data Analytics**. I build AI systems that connect models to real users, real workflows and verifiable outcomes.

My work sits at the intersection of:

- **Agentic AI and multimodal computer use**
- **AI software and product engineering**
- **Machine learning, forecasting and explainability**
- **Business analytics and decision support**
- **Real-time communication and privacy-aware systems**

I do not use AI as an unconstrained source of truth. My design principle is:

> **Probabilistic reasoning with deterministic execution boundaries.**
>
> AI interprets intent, retrieves relevant evidence and selects tools. Authoritative systems compute results, typed tools enforce boundaries, safety policies control actions, and verification determines whether the task actually succeeded.

That principle appears throughout my work:

- Data Science Studio computes analytical metrics through real Python services; the LLM explains the results.
- Gita.AI retrieves from an embedding corpus of all **701 Bhagavad Gita verses** instead of relying on the model's latent memory for quotations.
- Echo observes, acts, verifies and updates state instead of treating a tool response as proof of success.
- Financial and operational systems turn model outputs into transparent decision support rather than unexplained predictions.

---

## Flagship project: ECHO

### **ECHO — Executive Computer Heuristic Operator**

<a href="https://github.com/thedeepakreddy/Echo-mac"><img src="https://img.shields.io/badge/Explore_Echo_Mac-181717?style=for-the-badge&logo=github&logoColor=white" alt="Echo Mac"/></a>

Echo is a functioning local-first autonomous agent runtime for macOS. It is much more than a voice assistant: it is an operating layer that combines perception, planning, tool execution, memory, verification, recovery and learning.

#### What Echo can do

- See and understand the desktop through screenshots, OCR and macOS accessibility APIs
- Operate applications using semantic controls, text targeting, vision and native system actions
- Stream voice input and output with wake-word detection, VAD, STT, TTS and barge-in interruption
- Execute coding and research workflows through terminal, filesystem and agent tools
- Maintain project-scoped long-term memory with provenance, retention and deletion controls
- Learn reusable skills and workflows from demonstrations
- Preview workflows before execution and re-resolve controls by meaning rather than fixed coordinates
- Use task postconditions to verify that an action really happened
- Track uncertain, partial, failed and verified operations separately
- Record durable agent journals, checkpoints, heartbeats and provider/tool exchanges
- Recover interrupted tasks without blindly repeating uncertain side effects
- Replay agent runs and inspect why a task stopped
- Switch live between Claude, Gemini and local Ollama brains
- Delegate work to durable agent clones and structured multi-agent missions
- Run background research, screen monitoring, shadow coding and proactive assistance
- Control displays, phone remotes, messaging, maps, media, calendars and system settings
- Support local-first OCR, transcription, presence detection and model execution

#### Agent training loop

Echo records frontier-model execution trajectories—including observations, tool calls, actions, results and verification state—for training and analysis. I am using synthetic data and verified Echo trajectories to fine-tune and optimize a Qwen 2.5-VL policy with GRPO.

```text
frontier-model teacher
        ↓
Echo observations, actions and tool calls
        ↓
filter, label and verify trajectories
        ↓
synthetic + real training dataset
        ↓
Qwen 2.5-VL fine-tuning / GRPO
        ↓
local multimodal agent
        ↓
new verified trajectories and evaluation
```

The goal is to distill reliable computer-use behavior into a more efficient local model while preserving tool correctness, safety and task verification.

---

## Featured work

### [Aira.AI — Cross-platform AI workspace](https://github.com/thedeepakreddy/Aira.AI-Website)

A multi-surface AI platform with web and Tauri desktop clients, an authenticated gateway, browser automation, shared memory, MCP integrations, coding workflows and approval-based tool permissions.

- Web, macOS and Windows desktop shells
- Gateway-based credential boundaries; provider keys remain server-side
- OpenCode and MCP integration
- Isolated browser and coding runtimes
- User-scoped memory and authentication
- Permission-aware file, shell, subagent and tool execution
- Type checking, unit tests, integration tests and release-readiness checks

### [AskDeepakAI Data Science Studio](https://github.com/thedeepakreddy/AskDeepakAI-DataScienceStudio) · [Live app](https://askdeepakai-datascientist.onrender.com/)

An AI-assisted data science workstation designed to make SQL, Python, ML, deep learning, visualization and stakeholder reporting accessible to both technical and non-technical users.

- React/TypeScript frontend with Node orchestration and FastAPI services
- Real server-side EDA and model training
- Scikit-learn, XGBoost and SHAP
- Agentic reason-act-observe analysis workflows
- Visual SQL builder and drift monitoring
- LLM narration grounded in computed results; no fabricated metrics
- Tested and CI'd

### [Talktual — Real-time P2P voice translation](https://github.com/thedeepakreddy/Talktual) · [Live app](https://talktual.onrender.com/)

Built from a real cross-cultural communication problem: helping two people speak naturally when they do not share a language. Talktual connects two users through a QR handshake and translates spoken conversation with phone-call-like interaction.

- WebRTC communication and custom signaling
- Push-to-talk voice interaction
- Speech recognition, translation and synthesized speech
- Multilingual conversation design
- Graceful fallback when network speech services are unavailable

### [Tata Dransfer — Large-file P2P communication](https://github.com/thedeepakreddy/Tata-Dransfer-by-AskDeepakAI) · [Live app](https://tata-dransfer-by-askdeepakai-1.onrender.com/)

A privacy-oriented collaboration platform created to go beyond the limitations of free file-transfer services.

- Transfers up to 100GB+ through direct-to-disk streaming
- WebRTC-first transfer with signaling fallback
- AES-GCM encrypted chat and file payloads
- Audio calls, video calls and screen sharing
- Typing indicators and real-time messaging
- Designed for Wi-Fi and mobile-data conditions

### [Gita.AI — Retrieval-grounded Gita counsellor](https://github.com/thedeepakreddy/Gita.AI)

A multilingual conversational application donated to ISKCON. Users describe a personal problem, and the system retrieves semantically relevant passages from an embedding corpus containing all 701 Bhagavad Gita verses before generating an explanation.

- Source-grounded retrieval instead of relying on model memory for verses
- Contextual verse discovery through natural language
- Multilingual reading and interaction
- Clear separation between source text and AI interpretation
- Designed around a real personal and community need

---

## Business analytics and applied ML

| Project | What it demonstrates |
|---|---|
| [Automated Risk Intelligence Analyst](https://github.com/thedeepakreddy/Automated-Risk-Intelligence-Analyst) | Market/news ingestion, transparent systemic-risk scoring, explainable risk briefings and decision support |
| [Automated Market Intelligence Analyst](https://github.com/thedeepakreddy/Automated-Market-Intelligence-Analyst) | Price, macro and sentiment features, XGBoost/LSTM ensemble forecasting, SHAP and time-series validation |
| [Prescriptive Churn Analytics](https://github.com/thedeepakreddy/Prescriptive-Churn-Analytics-in-E-commerce) | Profit-optimized retention decisions, threshold optimization and business-cost-aware ML |
| [Enterprise Churn Optimization](https://github.com/thedeepakreddy/Enterprise-Churn-Optimization) | Gradient Boosting, SHAP, customer attrition and capital-at-risk analysis |
| [Last-Mile Delivery Analytics](https://github.com/thedeepakreddy/Last-Mile-Delivery-Analytics-Budapest) | PostgreSQL, SQL window functions, SLA analysis, financial bleed and Tableau decision support |
| [Inflation Forecasting Decision System](https://github.com/thedeepakreddy/Inflation-Forecasting-Decision-System) | Prophet, SARIMAX, XGBoost, backtesting and executive forecasting dashboards |
| [Trade Policy Decision Support](https://github.com/thedeepakreddy/AI-Driven-Trade-Policy-Impact-and-Decision-Support-System) | Tariff-shock scenarios, economic impact modeling and sourcing recommendations |
| [UNICEF Transaction Volume Analysis](https://github.com/thedeepakreddy/UNICEF-Transaction-Volume-Analysis) | Operational trends, anomaly detection and service-delivery performance analysis |

---

## How I build AI systems

```text
real user or business problem
              ↓
understand the workflow, users and constraints
              ↓
authoritative data, retrieval or direct observation
              ↓
AI reasoning and tool selection
              ↓
typed actions with permissions and safety gates
              ↓
observe the resulting state
              ↓
verify postconditions
              ↓
update memory, logs and models from verified outcomes
```

I care about the full path from **problem framing to deployment and adoption**—not only model accuracy. A good system should be useful to the person operating it, understandable to stakeholders and honest about what it knows, did and verified.

---

## Technical toolkit

**Languages:** Python · TypeScript · JavaScript · SQL · Swift · Rust

**AI/ML:** PyTorch · Transformers · Qwen 2.5-VL · GRPO · Scikit-learn · XGBoost · SHAP · TensorFlow · Keras · Prophet · SARIMAX · embeddings · RAG

**Agent engineering:** Claude Agent SDK · Gemini · Ollama · MCP · tool calling · structured outputs · agent memory · workflow learning · multi-agent orchestration · replay and recovery · verification-driven execution

**Backend and data:** FastAPI · Node.js · Express · PostgreSQL · SQLite · Pandas · NumPy · ETL · REST · WebSockets

**Frontend and apps:** React · Vite · Electron · Tauri · Recharts · Streamlit · Tableau · Power BI

**Systems and deployment:** WebRTC · macOS automation · accessibility APIs · OCR · Docker · GitHub Actions · Render · Vercel · Google Cloud

---

## Roles I am interested in

- Forward Deployed AI Engineer
- AI Software Engineer
- Agentic AI Engineer
- Applied AI Engineer
- Multimodal AI Engineer
- AI Product Engineer
- Computer-Use Agent Engineer
- LLM / Agent Platform Engineer
- AI Automation Engineer
- Research Engineer, Agent Systems
- Data Scientist / ML Engineer
- Business Intelligence and Decision Science roles

My background combines a **Computer Science Engineering bachelor's degree**, an **MSc in Business Data Analytics**, and hands-on experience building AI products for technical users, non-technical stakeholders and real human problems.

---

## Connect

<div align="center">

**If you are building reliable AI products, autonomous agents, data platforms or decision-support systems, I would be glad to connect.**

<a href="mailto:thedeepakreddy1@gmail.com">Email</a> ·
<a href="https://www.linkedin.com/in/deepak-reddy-038582223/">LinkedIn</a> ·
<a href="https://github.com/thedeepakreddy?tab=repositories">All repositories</a>

</div>
