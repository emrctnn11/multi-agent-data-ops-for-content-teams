🚀 Features
🧠 Multi-Agent Orchestration: Uses LangGraph to manage state and handoffs between agents.

🔄 Self-Correction Loop: Includes a "Fact-Checker" agent that can reject drafts and send them back to the "Writer" for revision (up to a limit).

⚡ Real-time Updates: Frontend updates instantly via Supabase Realtime when agents complete tasks.

📄 PDF Export: One-click download of the final blog post in PDF format (preserving layout).

🗄️ History Tracking: View and reload previously generated content from the history sidebar.

hybrid Architecture:

Frontend: Next.js 14 (App Router), TypeScript, Tailwind CSS.

Backend: Python (FastAPI), LangChain, LangGraph.

Database: Supabase (PostgreSQL).

🛠️ Tech Stack
Frontend: Next.js, React, Tailwind CSS, Axios, html2pdf.js.

Backend: Python 3.9+, FastAPI, Uvicorn.

AI Framework: LangChain, LangGraph.

LLMs: Google Gemini Pro (or OpenAI GPT-4o).

Infrastructure: Supabase (Auth, Database, Realtime).

🧩 Agent Workflow
The system follows a strict graph-based workflow:

🕵️‍♂️ Researcher: Analyzes the PRD and gathers necessary technical information.

✍️ Writer: Drafts the initial blog post based on research.

⚖️ Fact-Checker: Reviews the draft.

If issues found: Sends feedback back to Writer (Loop).

If approved: Passes to Style Polisher.

✨ Style Polisher: Refines tone, grammar, and formatting for the final output.

📦 Installation & Setup
1. Prerequisites
Node.js & npm

Python 3.9+

Supabase Account

Google AI Studio API Key (or OpenAI Key)

2. Database Setup (Supabase)
Go to your Supabase SQL Editor and run the following script to create the necessary table:

SQL

create table workflow_runs (
  id uuid default gen_random_uuid() primary key,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null,
  prd_text text not null,
  status text default 'pending',
  current_step text,
  final_output text,
  metadata jsonb
);

-- IMPORTANT: Enable Realtime for this table in Supabase Dashboard (Table Editor -> Edit Table -> Enable Realtime)
3. Backend Setup
Bash

cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure Environment Variables
# Create a .env file in /backend folder:
# SUPABASE_URL=your_supabase_url
# SUPABASE_ANON_KEY=your_supabase_anon_key
# GOOGLE_API_KEY=your_gemini_api_key
Run the backend server:

Bash

uvicorn main:app --reload
4. Frontend Setup
Bash

cd frontend

# Install dependencies
npm install

# Configure Environment Variables
# Create a .env.local file in /frontend folder:
# NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
# NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
Run the frontend:

Bash

npm run dev
Visit http://localhost:3000 to start generating content!

🇹🇷 Çok Ajanlı İçerik Operasyon Asistanı
Ham Ürün Gereksinim Dokümanlarını (PRD) alıp, yayınlanmaya hazır, profesyonel blog yazılarına dönüştüren yapay zeka tabanlı bir platform.

Bu proje, LangGraph tarafından yönetilen bir Çoklu Ajan Sistemi (Multi-Agent System) kullanır. Özelleşmiş yapay zeka ajanları (Araştırmacı, Yazar, Doğrulayıcı, Editör) işbirliği içinde çalışır, birbirlerinin işini denetler ve en kaliteli çıktıyı üretmek için düzeltme döngülerine girer.

🚀 Özellikler
🧠 Çoklu Ajan Orkestrasyonu: Ajanlar arası veri akışını ve durum yönetimini LangGraph ile sağlar.

🔄 Kendi Kendini Düzeltme (Loop): "Fact-Checker" ajanı, taslağı beğenmezse "Writer" ajanına geri bildirimle birlikte iade eder (Revize Döngüsü).

⚡ Gerçek Zamanlı Güncelleme: Ajanlar işi bitirdiğinde Supabase Realtime sayesinde arayüz anlık olarak güncellenir.

📄 PDF Çıktısı: Oluşturulan blog yazısı, formatı bozulmadan PDF olarak indirilebilir.

🗄️ Geçmiş Takibi: Tamamlanan işler sağ panelde listelenir ve tekrar görüntülenebilir.

Hibrit Mimari: Frontend (Next.js) ve Backend (Python FastAPI) yapısının entegrasyonu.

🛠️ Teknolojiler
Arayüz: Next.js 14, React, Tailwind CSS, html2pdf.js.

Sunucu: Python, FastAPI.

AI Altyapısı: LangChain, LangGraph.

Modeller: Google Gemini Pro (Alternatif: OpenAI GPT-4).

Veritabanı: Supabase (PostgreSQL + Realtime).

🧩 Ajan İş Akışı
Sistem, graf tabanlı (Graph-based) bir akış izler:

🕵️‍♂️ Researcher (Araştırmacı): Girilen PRD'yi analiz eder ve gerekli teknik bilgileri toplar.

✍️ Writer (Yazar): Araştırma verilerine dayanarak ilk taslağı yazar.

⚖️ Fact-Checker (Doğrulayıcı): Taslağı kontrol eder.

Hata varsa: Yazara geri gönderir (Revize).

Onaylarsa: Editöre iletir.

✨ Style Polisher (Editör): Yazının tonunu, imlasını ve akıcılığını son haline getirir.

📦 Kurulum ve Çalıştırma
1. Gereksinimler
Node.js

Python 3.9 veya üzeri

Supabase Hesabı

Google AI Studio API Anahtarı

2. Veritabanı Kurulumu (Supabase)
Supabase panelinde SQL Editor'ü açın ve şu kodu çalıştırın:

SQL

create table workflow_runs (
  id uuid default gen_random_uuid() primary key,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null,
  prd_text text not null,
  status text default 'pending',
  current_step text,
  final_output text,
  metadata jsonb
);

-- ÖNEMLİ: Tablo ayarlarından "Enable Realtime" seçeneğini açmayı unutmayın!
3. Backend Kurulumu
Bash

cd backend

# Sanal ortam oluştur
python -m venv venv
source venv/bin/activate  # Windows için: venv\Scripts\activate

# Paketleri yükle
pip install -r requirements.txt

# .env Dosyasını Oluştur (/backend klasöründe)
# SUPABASE_URL=senin_supabase_url
# SUPABASE_ANON_KEY=senin_supabase_key
# GOOGLE_API_KEY=senin_gemini_key
Sunucuyu başlat:

Bash

uvicorn main:app --reload
4. Frontend Kurulumu
Bash

cd frontend

# Paketleri yükle
npm install

# .env.local Dosyasını Oluştur (/frontend klasöründe)
# NEXT_PUBLIC_SUPABASE_URL=senin_supabase_url
# NEXT_PUBLIC_SUPABASE_ANON_KEY=senin_supabase_key
Uygulamayı başlat:

Bash

npm run dev
http://localhost:3000 adresine giderek ilk blog yazınızı üretebilirsiniz!

Developed by Emre Cetin.