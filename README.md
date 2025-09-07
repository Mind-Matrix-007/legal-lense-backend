# ⚖️ LegalLense  

**LegalLense** is a next-gen **legal document analysis platform** powered by AI 🤖.  
It streamlines the journey from **upload → processing → results** with a modern interface, clear risk indicators, and negotiation insights.  

Built during a hackathon 🏆, LegalLense reimagines how professionals review and understand legal documents.

---

## ✨ Key Features
- 🖼️ **Hero Landing Page** – AI-generated legal imagery with drag & drop upload.  
- 📂 **Seamless File Uploads** – Real-time progress tracking and secure cloud storage.  
- ⚡ **Automated Processing** – AI backend extracts clauses, metadata, and risks.  
- 📊 **Results Dashboard** – TL;DR summary, document health score, clause-by-clause analysis.  
- 🧑‍⚖️ **Negotiation Assistant** – Sidebar with suggestions, scenario simulation, and Q&A chat.  
- 📑 **Comparison Mode** – Quickly contrast contracts or track redlines.  

---

## 🏗️ Backend Architecture (Parts A–D)

Our backend is modular 🔌 and split into **four core parts** (+ an optional extension).  

### 🔹 Part A — Signed URL Service  
- Provides **secure, time-limited URLs** for clients to upload files directly to Google Cloud Storage (GCS).  
- Prevents exposing bucket credentials while enabling safe uploads.  

### 🔹 Part B — Upload Processor  
- Triggered when a file is uploaded to GCS.  
- Extracts **raw text** from PDFs or docs 📑.  
- Handles OCR (if needed), cleans text, and prepares it for AI processing.  

### 🔹 Part C — Processing & AI Extraction  
- Runs the **main NLP/AI pipeline**:  
  - Clause extraction  
  - Entity recognition  
  - Risk scoring 🚨  
  - Summarization  
- Outputs structured JSON results with page mapping and highlights.  

### 🔹 Part D — Firestore Storage & Results API  
- Stores extracted results in **Firestore** under user/project IDs.  
- Enables frontend dashboard to **query results in real-time**.  
- Supports TL;DR summaries, clause-level details, and negotiation suggestions.  

---

## 🔸 Optional Part E — Enhancements  
- **Comparison Engine** 🆚: Spot differences between multiple documents.  
- **Scenario Simulator** 🎭: Run "what-if" cases for negotiations.  
- **Chatbot Assistant** 💬: Answer user questions about the uploaded contract.  
- **Export/Download** ⬇️: PDF/CSV export with annotations and summaries.  

---

## 🎨 UI & Experience  
From our [Figma Designs](./LegalLense%20(Figma).pdf) and [Wireframes](./LegalLense-WireFrame.pdf):  
- Dark-themed, modern, and professional.  
- Step-by-step flow: **Upload → Processing → Dashboard → Insights**.  
- Clear risk flags 🔴🟡🟢 for each clause.  

---

## 🚀 Tech Stack
 
- **Backend:** Python (FastAPI/Flask) + GCP Cloud Functions / Cloud Run  
- **Database:** Firestore (NoSQL)  
- **Storage:** Google Cloud Storage (buckets)  
- **AI/NLP:** Transformers, OpenAI/GPT APIs (for summarization & entity extraction)  

---

