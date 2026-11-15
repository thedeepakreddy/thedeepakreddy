<!-- Profile README · Gorisi Deepak Reddy
     Visuals are generated: edit the DATA block in scripts/build_assets.py, then run `python3 scripts/build_assets.py`. -->

<div align="center">

<p><img src="assets/hero.svg" width="100%" alt="Gorisi Deepak Reddy. I build AI systems that act, then prove they did. Budapest, Hungary. Open to roles."/></p>

<p>
<a href="mailto:thedeepakreddy1@gmail.com"><img src="assets/btn-email.svg" width="32%" alt="Email"/></a>
<a href="https://www.linkedin.com/in/deepak-reddy-038582223/"><img src="assets/btn-linkedin.svg" width="32%" alt="LinkedIn"/></a>
<a href="https://github.com/thedeepakreddy?tab=repositories"><img src="assets/btn-github.svg" width="32%" alt="All repositories"/></a>
</p>

</div>

<br/>

<p><img src="assets/h-about.svg" width="100%" alt="01 · Principle"/></p>

I am a **Computer Science Engineering graduate** with an **MSc in Business Data Analytics**, based in Budapest. I build AI systems that connect models to real users, real workflows and outcomes that can be checked.

I do not treat a model as a source of truth. The model interprets intent, retrieves evidence and picks tools. Everything after that is deterministic: authoritative systems compute, typed tools enforce boundaries, safety policy gates actions, and verification decides whether the task actually succeeded.

<p><img src="assets/principle.svg" width="100%" alt="Probabilistic reasoning, deterministic execution boundaries: AI interprets, retrieves and selects; typed tools, permissions and safety policy form the gate; systems compute and verification decides."/></p>

| Where it shows up | What the principle looks like in practice |
|---|---|
| **Echo** | Observes, acts, verifies and updates state. A tool response is never taken as proof of success. |
| **Data Science Studio** | Real Python services compute every metric. The LLM only explains results that already exist. |
| **Gita.AI** | Retrieves from an embedding corpus of all **701 verses** instead of quoting from model memory. |
| **Risk and forecasting systems** | Model outputs become transparent decision support, not unexplained predictions. |

<br/>

<p><img src="assets/h-echo.svg" width="100%" alt="02 · Flagship: Echo"/></p>

<p><a href="https://github.com/thedeepakreddy/Echo-mac"><img src="assets/echo.svg" width="100%" alt="Echo, Executive Computer Heuristic Operator: perceive, plan, act, verify, recover, learn. Screen understanding, voice, an agent journal with verified, uncertain and partial states, and live brain switching between Claude, Gemini and Ollama."/></a></p>

**[ECHO · Executive Computer Heuristic Operator](https://github.com/thedeepakreddy/Echo-mac)** is a working local-first autonomous agent runtime for macOS. It is an operating layer that combines perception, planning, tool execution, memory, verification, recovery and learning.

<details>
<summary><b>Everything Echo can do</b></summary>
<br/>

| Area | Capabilities |
|---|---|
| **Perception** | Understands the desktop through screenshots, OCR and macOS accessibility APIs |
| **Action** | Operates apps with semantic controls, text targeting, vision and native system actions; re-resolves controls by meaning, not fixed coordinates |
| **Voice** | Streaming input and output with wake word, VAD, STT, TTS and barge-in interruption |
| **Verification** | Task postconditions confirm an action really happened; uncertain, partial, failed and verified operations are tracked separately |
| **Recovery** | Durable journals, checkpoints, heartbeats and provider/tool exchanges; interrupted tasks resume without blindly repeating uncertain side effects |
| **Replay** | Agent runs can be replayed to inspect why a task stopped |
| **Memory** | Project-scoped long-term memory with provenance, retention and deletion controls |
| **Learning** | Reusable skills and workflows learned from demonstrations, previewed before execution |
| **Brains** | Live switching between Claude, Gemini and local Ollama |
| **Delegation** | Durable agent clones and structured multi-agent missions |
| **Background work** | Research, screen monitoring, shadow coding and proactive assistance |
| **Reach** | Terminal, filesystem, displays, phone remotes, messaging, maps, media, calendars and system settings |
| **Local-first** | OCR, transcription, presence detection and model execution on device |

</details>

<p><img src="assets/training-loop.svg" width="100%" alt="Agent training loop: frontier teacher, Echo trajectories, filter label verify, synthetic plus real dataset, Qwen 2.5-VL with GRPO, local multimodal agent, and new verified trajectories feeding back."/></p>

Echo records frontier-model trajectories: observations, tool calls, actions, results and verification state. I use those verified trajectories plus synthetic data to fine-tune a **Qwen 2.5-VL** policy with **GRPO**, distilling reliable computer use into an efficient local model without losing tool correctness, safety or task verification.

<br/>

<p><img src="assets/h-work.svg" width="100%" alt="03 · Featured work"/></p>

<p align="center">
<a href="https://github.com/thedeepakreddy/Aira.AI-Website"><img src="assets/card-aira.svg" width="49%" alt="Aira.AI: cross-platform AI workspace behind a permission gateway"/></a>
<a href="https://github.com/thedeepakreddy/AskDeepakAI-DataScienceStudio"><img src="assets/card-studio.svg" width="49%" alt="Data Science Studio: real server-side EDA and training, the LLM only narrates"/></a>
<a href="https://github.com/thedeepakreddy/Talktual"><img src="assets/card-talktual.svg" width="49%" alt="Talktual: real-time peer-to-peer voice translation"/></a>
<a href="https://github.com/thedeepakreddy/Tata-Dransfer-by-AskDeepakAI"><img src="assets/card-transfer.svg" width="49%" alt="Tata Dransfer: encrypted peer-to-peer files, calls and chat, 100GB+"/></a>
<a href="https://github.com/thedeepakreddy/Gita.AI"><img src="assets/card-gita.svg" width="49%" alt="Gita.AI: retrieval grounded in all 701 Bhagavad Gita verses"/></a>
<a href="#analytics"><img src="assets/card-analytics.svg" width="49%" alt="Analytics and applied ML: eight decision systems"/></a>
</p>

| Project | Why it exists | Links |
|---|---|---|
| **Aira.AI** | One AI workspace across web, macOS and Windows. Provider keys stay server-side behind an authenticated gateway; file, shell, subagent and tool actions need approval. Typed, unit and integration tested. | [Repo](https://github.com/thedeepakreddy/Aira.AI-Website) |
| **Data Science Studio** | SQL, Python, ML and reporting for technical and non-technical users. Agentic reason-act-observe analysis, visual SQL builder, drift monitoring. No fabricated metrics. | [Repo](https://github.com/thedeepakreddy/AskDeepakAI-DataScienceStudio) · [Live](https://askdeepakai-datascientist.onrender.com/) |
| **Talktual** | Built from a real cross-cultural problem: two people without a shared language. QR handshake, push-to-talk, graceful fallback when speech services drop. | [Repo](https://github.com/thedeepakreddy/Talktual) · [Live](https://talktual.onrender.com/) |
| **Tata Dransfer** | Past the limits of free file-transfer services: 100GB+ direct-to-disk streaming, AES-GCM encrypted chat and files, audio, video and screen sharing. | [Repo](https://github.com/thedeepakreddy/Tata-Dransfer-by-AskDeepakAI) · [Live](https://tata-dransfer-by-askdeepakai-1.onrender.com/) |
| **Gita.AI** | Donated to ISKCON. Describe a personal problem and get semantically relevant verses, with source text kept separate from AI interpretation. Multilingual. | [Repo](https://github.com/thedeepakreddy/Gita.AI) |

<br/>

<a name="analytics"></a>
<p><img src="assets/h-analytics.svg" width="100%" alt="04 · Analytics and applied ML"/></p>

| Project | Decision it supports | Methods |
|---|---|---|
| [Automated Risk Intelligence Analyst](https://github.com/thedeepakreddy/Automated-Risk-Intelligence-Analyst) | How exposed are we right now, and why? | Market and news ingestion, transparent systemic-risk scoring, explainable briefings |
| [Automated Market Intelligence Analyst](https://github.com/thedeepakreddy/Automated-Market-Intelligence-Analyst) | Where is the market heading? | Price, macro and sentiment features, XGBoost/LSTM ensemble, SHAP, time-series validation |
| [Prescriptive Churn Analytics](https://github.com/thedeepakreddy/Prescriptive-Churn-Analytics-in-E-commerce) | Who is worth retaining, at what cost? | Profit-optimized thresholds, business-cost-aware ML |
| [Enterprise Churn Optimization](https://github.com/thedeepakreddy/Enterprise-Churn-Optimization) | How much capital is at risk from attrition? | Gradient Boosting, SHAP, capital-at-risk analysis |
| [Last-Mile Delivery Analytics](https://github.com/thedeepakreddy/Last-Mile-Delivery-Analytics-Budapest) | Where are SLAs bleeding money? | PostgreSQL, SQL window functions, Tableau |
| [Inflation Forecasting Decision System](https://github.com/thedeepakreddy/Inflation-Forecasting-Decision-System) | What should we plan for next quarter? | Prophet, SARIMAX, XGBoost, backtesting, executive dashboards |
| [Trade Policy Decision Support](https://github.com/thedeepakreddy/AI-Driven-Trade-Policy-Impact-and-Decision-Support-System) | How do we source under a tariff shock? | Scenario modeling, economic impact, sourcing recommendations |
| [UNICEF Transaction Volume Analysis](https://github.com/thedeepakreddy/UNICEF-Transaction-Volume-Analysis) | Where is service delivery slipping? | Operational trends, anomaly detection |

<br/>

<p><img src="assets/h-toolkit.svg" width="100%" alt="05 · Toolkit"/></p>

<p><img src="assets/toolkit.svg" width="100%" alt="Languages: Python, TypeScript, JavaScript, SQL, Swift, Rust. Agents: Claude Agent SDK, Gemini, Ollama, MCP, tool calling, structured outputs, agent memory, workflow learning, multi-agent orchestration, replay and recovery, verification-driven execution. AI/ML: PyTorch, Transformers, Qwen 2.5-VL, GRPO, scikit-learn, XGBoost, SHAP, TensorFlow, Keras, Prophet, SARIMAX, embeddings, RAG. Backend and data: FastAPI, Node.js, Express, PostgreSQL, SQLite, Pandas, NumPy, ETL, REST, WebSockets. Frontend and apps: React, Vite, Electron, Tauri, Recharts, Streamlit, Tableau, Power BI. Systems: WebRTC, macOS automation, accessibility APIs, OCR, Docker, GitHub Actions, Render, Vercel, Google Cloud."/></p>

<br/>

<p><img src="assets/h-roles.svg" width="100%" alt="06 · Target roles"/></p>

<p><img src="assets/roles.svg" width="100%" alt="Primary target role: Forward Deployed AI Engineer. Also: AI Software Engineer, Agentic AI Engineer, Applied AI Engineer, Multimodal AI Engineer, AI Product Engineer, Computer-Use Agent Engineer, LLM / Agent Platform Engineer, AI Automation Engineer, Research Engineer (Agent Systems), Data Scientist / ML Engineer, BI and Decision Science. Education: BSc Computer Science Engineering and MSc Business Data Analytics."/></p>

I care about the full path from **problem framing to deployment and adoption**, not only model accuracy. A good system is useful to the person operating it, understandable to stakeholders, and honest about what it knows, did and verified.

<br/>

<div align="center">

<p><img src="assets/footer.svg" width="100%" alt="Status: available. Building agents that have to be right? Let's connect."/></p>

<p>
<a href="mailto:thedeepakreddy1@gmail.com"><img src="assets/btn-email.svg" width="32%" alt="Email"/></a>
<a href="https://www.linkedin.com/in/deepak-reddy-038582223/"><img src="assets/btn-linkedin.svg" width="32%" alt="LinkedIn"/></a>
<a href="https://github.com/thedeepakreddy?tab=repositories"><img src="assets/btn-github.svg" width="32%" alt="All repositories"/></a>
</p>

</div>
