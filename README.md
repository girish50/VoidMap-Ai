# 🌌 VoidMap AI — Adaptive System Audit Engine

VoidMap AI is an intelligent, full-stack architectural auditing platform that identifies **missing engineering requirements (blueprint voids)** in technical proposals, stress-tests designs under adversarial simulation sandboxes, and maps failure domino effects before a single line of production code is written.

### 🌐 Live Deployment Links
* **Frontend Web Application (Vercel):** [Live Demo](https://voidmap-ai.vercel.app)
* **Backend API Engine (Render):** [Live API Endpoint](https://voidmap-backend.onrender.com)

---

## 🚀 Key Features

* **Blueprint Absence Engine:** Parses raw text project descriptions or structured checklists (via NLP parsing) and compares them against domain graph schemas (Neo4j) to pinpoint missing safety safeguards.
* **Blindspot Index & Gaps Grid:** Computes a dynamic risk score (0-100%) and categorizes missing items along with their down-stream cascading hazards.
* **Absence Counterfactual Simulator:** Sandbox sliders that allow users to simulate real-world disasters (e.g. scanner degradation, regulatory tightening, traffic surges) to see how system risk escalates dynamically.
* **Directed Consequence Ripple Trees:** An interactive 2D node map (React Flow) rendering the exact domino-effect paths showing how a single blueprint omission cascades into a system collapse.
* **Disaster DNA Proximity:** Computes cosine semantic similarity between your project's gaps and famous historic software failures (e.g., Knight Capital, Therac-25, IBM Watson Oncology) to extract direct preventative architecture lessons.
* **Boardroom Clash Feed:** Generates adversarial dialogue logs between virtual corporate personas (e.g., Clinical Safety Officer vs VC Investor) debating trade-offs.

---

## 🛠️ Technology Stack

### Frontend UI
* **React 18 & Vite:** Fast client environment bundling and state rendering.
* **Tailwind CSS:** Rich dark-mode glassmorphism aesthetics.
* **React Flow:** Render interactive directed acyclic graphs for the ripple maps.
* **Zustand & Axios:** Global client-side store management and asynchronous HTTP communication.

### Backend API & ML Engines
* **FastAPI & Uvicorn:** High-performance, asynchronous REST API routing.
* **Sentence-Transformers (BERT):** Embeds and matches missing components with the Historical Failure DNA catalog.
* **spaCy (NLP):** Natural language processing models for keyphrase extraction.
* **Scikit-Learn, Pandas & NumPy:** Regressive and classification threat modeling algorithms.

### Database Layer
* **PostgreSQL (Supabase Cloud) & SQLModel:** Relational database storage of audited project histories and metadata.
* **Neo4j Aura Cloud:** External graph network governing domain requirement links.

---

## 🛡️ Engineering Feature: Self-Healing Fallbacks

The project is built with **zero-point failure tolerance**, making it robust for both local testing and remote deployments. On startup, the backend automatically runs connection audits:

```
[Postgres Database Connection] ──(Fails?)──► [Automatic Switch to Local SQLite 'voidmap.db']
[Neo4j Graph Database Connection] ──(Fails?)──► [Automatic Switch to In-Memory NetworkX Graph]
```

This prevents application startup crashes if the internet goes offline or if cloud databases pause due to inactivity, seamlessly preserving system functionality.

---

## 💻 Local Installation & Setup

### Prerequisites
* Python 3.10+
* Node.js 18+

### 1. Backend Setup
Navigate to the backend directory, create a virtual environment, install requirements, and run database seeding:

```bash
cd backend
python -m venv venv
# Activate virtual env:
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

To initialize your databases (PostgreSQL/SQLite and Neo4j) with seeded default projects and nodes, run:
```bash
python app/seed.py
```

Start the backend API server:
```bash
python run.py
```
*The API server will run at `http://127.0.0.1:8000`.*

### 2. Frontend Setup
Navigate to the frontend directory, install dependencies, and start the Vite development server:

```bash
cd ../frontend
npm install
npm run dev
```
*The React application will run at `http://localhost:5173`.*

---

## 📄 License
Distributed under the MIT License. See [LICENSE](LICENSE) for more information.
