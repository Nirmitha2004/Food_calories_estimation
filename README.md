# 🍽️ Food Vision AI

> Real-time food recognition + nutritional insights — **free, open-source, no GPU needed**

[![Hugging Face Spaces](https://img.shields.io/badge/🤗%20HF%20Spaces-Live%20Demo-orange)](https://huggingface.co/spaces/yourusername/food-vision-ai)
[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-red)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 📸 What It Does

Upload or snap a food photo → AI identifies it in under 1 second → instant nutritional breakdown.

- **101 food categories** via `nateraw/food` (ViT fine-tuned on Food-101)
- **Webcam support** — live capture in the browser
- **Nutrition info** — calories, protein, carbs, fat per serving
- **Confidence bars** — visual breakdown of top-5 predictions
- **Dark mode SaaS UI** — mobile-responsive, no sign-up needed

---

## 🗂️ Project Structure

```
food-vision-ai/
├── app.py                  ← Main Streamlit app (single file)
├── requirements.txt        ← Python dependencies
├── README.md               ← This file
└── .streamlit/
    └── config.toml         ← Streamlit theme + server config
```

---

## ⚡ Run Locally (3 steps)

```bash
# 1. Clone & enter
git clone https://github.com/yourusername/food-vision-ai.git
cd food-vision-ai

# 2. Install (first time only)
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Run
streamlit run app.py
# → opens http://localhost:8501
```

> **First run** downloads the ViT model (~350 MB) automatically and caches it.
> Subsequent starts are instant.

---

## 🚀 Deploy Free Online — Step-by-Step Guide

### ✅ RECOMMENDED: Hugging Face Spaces (Best for AI apps)

**Why HF Spaces?**
- Free, permanent public URL (no sleep timeout like Streamlit Cloud free tier)
- Built for AI/ML apps — model weights cached on their servers
- Streamlit SDK natively supported
- No credit card required

#### Step-by-step:

**Step 1 — Push your code to GitHub**

```bash
# If you haven't already:
git init
git add .
git commit -m "🍽️ Initial commit — Food Vision AI"

# Create a repo on github.com/new, then:
git remote add origin https://github.com/yourusername/food-vision-ai.git
git branch -M main
git push -u origin main
```

**Step 2 — Create a Hugging Face Space**

1. Go to → **https://huggingface.co/new-space**
2. Fill in:
   - **Space name:** `food-vision-ai`
   - **SDK:** Streamlit
   - **Hardware:** CPU Basic (Free) ✅
   - **Visibility:** Public
3. Click **Create Space**

**Step 3 — Connect GitHub → HF Spaces**

Option A (easiest): In HF Space settings → **Link GitHub repo** → select your repo → auto-deploys on every push.

Option B (manual): HF gives you a git remote URL. Push directly:
```bash
git remote add hf https://huggingface.co/spaces/yourusername/food-vision-ai
git push hf main
```

**Step 4 — Wait ~3 minutes** for the build to complete.

**Step 5 — Share your public link!** 🎉
```
https://huggingface.co/spaces/yourusername/food-vision-ai
```

---

### Option B: Streamlit Cloud (Also free)

1. Go to → **https://share.streamlit.io**
2. Sign in with GitHub
3. Click **New app**
4. Select repo → branch `main` → Main file: `app.py`
5. Click **Deploy**

Public URL: `https://yourusername-food-vision-ai-app-xxxxx.streamlit.app`

⚠️ Note: Streamlit Cloud free tier **sleeps after inactivity** (needs wake-up click). HF Spaces does not.

---

### Option C: Render (Good for custom domains)

1. Go to → **https://render.com** → New → Web Service
2. Connect GitHub repo
3. Settings:
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `streamlit run app.py --server.port $PORT --server.headless true`
   - **Plan:** Free
4. Deploy

---

## 📡 How to Share Your App

Once deployed on HF Spaces:

```
🔗 Your public link: My app link
https://huggingface.co/spaces/nirmitha/food-vision-ai/blob/main/app.py

Share it anywhere:
• WhatsApp / Telegram — paste the link
• Twitter / LinkedIn — post a demo screenshot + link
• GitHub README — add the HF Spaces badge (see top of this file)
```

Anyone with the link can use the app — no login, no install, no cost.

---

## 🔧 Common Deployment Issues & Fixes

| Problem | Fix |
|---|---|
| `torch` install fails on HF Spaces | Already handled — `requirements.txt` uses CPU torch |
| App crashes on boot | Check **Logs** tab in HF Space for the error message |
| Camera not working in browser | Browser needs HTTPS — HF Spaces provides it automatically |
| Model download times out | HF Spaces has fast HuggingFace Hub access — won't timeout |
| `port 7860` error | Already set in `.streamlit/config.toml` |
| Build succeeds but blank screen | Hard refresh (Ctrl+Shift+R) and wait 30s for model to load |
| Streamlit Cloud sleeps | Switch to HF Spaces — no sleep on free tier |

---

## 🧠 Model Details

| Property | Value |
|---|---|
| Model | `nateraw/food` |
| Architecture | Vision Transformer (ViT-base-patch16-224) |
| Training data | Food-101 (101,000 images, 101 categories) |
| Input size | 224 × 224 px |
| Inference time | ~200–600 ms on CPU |
| Fallback | `google/vit-base-patch16-224` |

---

## 🍕 Supported Food Categories (sample)

Pizza · Burger · Sushi · Taco · Ice Cream · Pasta · Salad · Donut ·
French Fries · Steak · Cake · Banana · Apple · Hot Dog · Sandwich ·
Fried Chicken · Waffle · Pancake · Burrito · Rice · Bread · Chocolate ·
Coffee · Avocado · Egg · Ramen · Salmon · Mango · Strawberry · + 70 more

---

## 📜 License

MIT — free to use, fork, deploy, and modify.
Nutritional data is estimated and for informational purposes only.

---

## ⭐ If you find this useful, please star the repo!
