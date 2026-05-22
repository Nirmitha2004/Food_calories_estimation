"""
╔══════════════════════════════════════════════════════════════════╗
║           🍽️  FOOD VISION AI  —  Production v2.0               ║
║   Real-time food recognition + nutritional insights             ║
║   Deployed on Hugging Face Spaces (free, public, no GPU needed) ║
╚══════════════════════════════════════════════════════════════════╝

Stack : Streamlit · Hugging Face Transformers · ViT-Food101
Author: Your Name  |  License: MIT  |  Open-Source ✅
"""

import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import time
import base64
from io import BytesIO

# ─────────────────────────────────────────────────────────────────
# PAGE CONFIG  (must be the very first Streamlit call)
# ─────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Food Vision AI — Identify Any Food Instantly",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed",   # hero-first on mobile
    menu_items={
        "Get Help": "https://github.com/yourusername/food-vision-ai",
        "Report a bug": "https://github.com/yourusername/food-vision-ai/issues",
        "About": "# 🍽️ Food Vision AI\nFree, open-source food recognition powered by Vision Transformers.",
    },
)

# ─────────────────────────────────────────────────────────────────
# NUTRITION DATABASE  (25+ foods, easy to extend)
# ─────────────────────────────────────────────────────────────────
NUTRITION_DB = {
    "pizza":         {"calories": 266, "protein": 11,  "carbs": 33,  "fat": 10,  "emoji": "🍕", "serving": "1 slice (~100g)",    "color": "#FF6B35"},
    "apple":         {"calories": 52,  "protein": 0.3, "carbs": 14,  "fat": 0.2, "emoji": "🍎", "serving": "1 medium (~182g)",   "color": "#4CAF50"},
    "burger":        {"calories": 295, "protein": 17,  "carbs": 24,  "fat": 14,  "emoji": "🍔", "serving": "1 burger (~150g)",   "color": "#FF9800"},
    "salad":         {"calories": 20,  "protein": 1.5, "carbs": 3.5, "fat": 0.3, "emoji": "🥗", "serving": "1 bowl (~150g)",     "color": "#66BB6A"},
    "banana":        {"calories": 89,  "protein": 1.1, "carbs": 23,  "fat": 0.3, "emoji": "🍌", "serving": "1 medium (~118g)",   "color": "#FFD700"},
    "sushi":         {"calories": 143, "protein": 5,   "carbs": 28,  "fat": 0.5, "emoji": "🍣", "serving": "6 pieces (~100g)",   "color": "#EF5350"},
    "ice cream":     {"calories": 207, "protein": 3.5, "carbs": 24,  "fat": 11,  "emoji": "🍦", "serving": "1 scoop (~100g)",    "color": "#EC407A"},
    "hot dog":       {"calories": 290, "protein": 10,  "carbs": 22,  "fat": 17,  "emoji": "🌭", "serving": "1 hot dog (~120g)",  "color": "#FF7043"},
    "sandwich":      {"calories": 210, "protein": 11,  "carbs": 28,  "fat": 6,   "emoji": "🥪", "serving": "1 sandwich (~150g)", "color": "#A5D6A7"},
    "steak":         {"calories": 271, "protein": 26,  "carbs": 0,   "fat": 18,  "emoji": "🥩", "serving": "1 serving (~100g)",  "color": "#EF5350"},
    "pasta":         {"calories": 158, "protein": 6,   "carbs": 31,  "fat": 0.9, "emoji": "🍝", "serving": "1 cup cooked",       "color": "#FFA726"},
    "soup":          {"calories": 70,  "protein": 3,   "carbs": 8,   "fat": 3,   "emoji": "🍲", "serving": "1 bowl (~240ml)",    "color": "#26C6DA"},
    "cake":          {"calories": 347, "protein": 4,   "carbs": 52,  "fat": 14,  "emoji": "🎂", "serving": "1 slice (~100g)",    "color": "#AB47BC"},
    "donut":         {"calories": 452, "protein": 4.9, "carbs": 51,  "fat": 25,  "emoji": "🍩", "serving": "1 donut (~60g)",     "color": "#EC407A"},
    "french fries":  {"calories": 312, "protein": 3.4, "carbs": 41,  "fat": 15,  "emoji": "🍟", "serving": "medium (~100g)",     "color": "#FFD54F"},
    "fried chicken": {"calories": 320, "protein": 28,  "carbs": 11,  "fat": 18,  "emoji": "🍗", "serving": "1 piece (~100g)",    "color": "#FFA726"},
    "waffle":        {"calories": 291, "protein": 7.9, "carbs": 37,  "fat": 13,  "emoji": "🧇", "serving": "1 waffle (~75g)",    "color": "#FFCC02"},
    "pancake":       {"calories": 227, "protein": 6,   "carbs": 36,  "fat": 7,   "emoji": "🥞", "serving": "2 pancakes (~100g)", "color": "#FFB74D"},
    "taco":          {"calories": 226, "protein": 9,   "carbs": 20,  "fat": 13,  "emoji": "🌮", "serving": "1 taco (~90g)",      "color": "#66BB6A"},
    "burrito":       {"calories": 290, "protein": 14,  "carbs": 36,  "fat": 10,  "emoji": "🌯", "serving": "1 burrito (~150g)",  "color": "#26A69A"},
    "rice":          {"calories": 130, "protein": 2.7, "carbs": 28,  "fat": 0.3, "emoji": "🍚", "serving": "1 cup cooked",       "color": "#ECEFF1"},
    "bread":         {"calories": 265, "protein": 9,   "carbs": 49,  "fat": 3.2, "emoji": "🍞", "serving": "2 slices (~60g)",    "color": "#BCAAA4"},
    "chocolate":     {"calories": 546, "protein": 5,   "carbs": 60,  "fat": 31,  "emoji": "🍫", "serving": "1 bar (~45g)",       "color": "#6D4C41"},
    "coffee":        {"calories": 2,   "protein": 0.3, "carbs": 0,   "fat": 0,   "emoji": "☕", "serving": "1 cup (240ml)",      "color": "#795548"},
    "avocado":       {"calories": 160, "protein": 2,   "carbs": 9,   "fat": 15,  "emoji": "🥑", "serving": "½ avocado (~100g)",  "color": "#66BB6A"},
    "egg":           {"calories": 155, "protein": 13,  "carbs": 1,   "fat": 11,  "emoji": "🍳", "serving": "2 eggs (~100g)",     "color": "#FFF176"},
    "ramen":         {"calories": 436, "protein": 18,  "carbs": 57,  "fat": 14,  "emoji": "🍜", "serving": "1 bowl (~500g)",     "color": "#FF7043"},
    "salmon":        {"calories": 208, "protein": 20,  "carbs": 0,   "fat": 13,  "emoji": "🐟", "serving": "100g",               "color": "#EF9A9A"},
    "mango":         {"calories": 60,  "protein": 0.8, "carbs": 15,  "fat": 0.4, "emoji": "🥭", "serving": "1 cup (~165g)",      "color": "#FFA726"},
    "strawberry":    {"calories": 32,  "protein": 0.7, "carbs": 7.7, "fat": 0.3, "emoji": "🍓", "serving": "1 cup (~150g)",      "color": "#EF5350"},
    "cheesecake":    {"calories": 321, "protein": 5.5, "carbs": 25,  "fat": 23,  "emoji": "🎂", "serving": "1 slice (~100g)",    "color": "#CE93D8"},
    "popcorn":       {"calories": 375, "protein": 11,  "carbs": 74,  "fat": 4.5, "emoji": "🍿", "serving": "3 cups (~28g)",      "color": "#FFF9C4"},
    "default":       {"calories": 150, "protein": 5,   "carbs": 20,  "fat": 5,   "emoji": "🍽️", "serving": "1 serving (~100g)", "color": "#90A4AE"},
}

# ─────────────────────────────────────────────────────────────────
# LABEL → NUTRITION KEY MAP
# ─────────────────────────────────────────────────────────────────
LABEL_MAP = {
    "pizza": "pizza", "apple": "apple", "granny smith": "apple",
    "hamburger": "burger", "burger": "burger", "cheeseburger": "burger",
    "salad": "salad", "caesar salad": "salad", "banana": "banana",
    "sushi": "sushi", "maki": "sushi", "sashimi": "sushi",
    "ice cream": "ice cream", "icecream": "ice cream", "gelato": "ice cream",
    "hot dog": "hot dog", "hotdog": "hot dog",
    "sandwich": "sandwich", "club sandwich": "sandwich",
    "steak": "steak", "beef": "steak", "filet mignon": "steak",
    "pasta": "pasta", "spaghetti": "pasta", "noodle": "pasta", "linguine": "pasta",
    "soup": "soup", "stew": "soup", "ramen": "ramen",
    "cake": "cake", "birthday cake": "cake",
    "doughnut": "donut", "donut": "donut",
    "french fries": "french fries", "fries": "french fries",
    "fried chicken": "fried chicken", "chicken wings": "fried chicken",
    "waffle": "waffle", "pancake": "pancake",
    "taco": "taco", "burrito": "burrito",
    "rice": "rice", "fried rice": "rice",
    "bread": "bread", "baguette": "bread", "toast": "bread",
    "chocolate": "chocolate", "chocolate cake": "chocolate",
    "coffee": "coffee", "espresso": "coffee", "latte": "coffee",
    "avocado": "avocado", "guacamole": "avocado",
    "egg": "egg", "omelette": "egg", "scrambled eggs": "egg",
    "salmon": "salmon", "mango": "mango", "strawberry": "strawberry",
    "cheesecake": "cheesecake", "popcorn": "popcorn",
}

# ─────────────────────────────────────────────────────────────────
# CSS — Modern SaaS Dark Theme  (mobile-first)
# ─────────────────────────────────────────────────────────────────
def inject_css():
    st.markdown("""
    <style>
    /* ── Base & fonts ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
    .main .block-container { padding: 0 !important; max-width: 100% !important; }
    #MainMenu, footer, header { visibility: hidden; }

    /* ── Hero section ── */
    .hero {
        background: linear-gradient(135deg, #0a0a1a 0%, #12122a 40%, #1a0a2e 100%);
        padding: 70px 40px 50px;
        text-align: center;
        position: relative;
        overflow: hidden;
        border-bottom: 1px solid #ffffff10;
    }
    .hero::before {
        content: "";
        position: absolute; inset: 0;
        background:
            radial-gradient(ellipse 60% 50% at 20% 50%, #FF6B3520 0%, transparent 70%),
            radial-gradient(ellipse 60% 50% at 80% 50%, #7C3AED20 0%, transparent 70%);
        pointer-events: none;
    }
    .hero-badge {
        display: inline-block;
        background: linear-gradient(90deg, #FF6B3530, #7C3AED30);
        border: 1px solid #FF6B3560;
        color: #FF6B35;
        padding: 6px 18px;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 20px;
    }
    .hero-title {
        font-size: clamp(2.2rem, 6vw, 4rem);
        font-weight: 900;
        line-height: 1.1;
        background: linear-gradient(135deg, #ffffff 0%, #FF6B35 50%, #FFD700 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0 0 16px;
    }
    .hero-sub {
        color: #9ca3af;
        font-size: clamp(0.95rem, 2.5vw, 1.15rem);
        max-width: 600px;
        margin: 0 auto 30px;
        line-height: 1.7;
    }
    .hero-stats {
        display: flex;
        justify-content: center;
        gap: 40px;
        flex-wrap: wrap;
        margin-top: 30px;
    }
    .hero-stat { text-align: center; }
    .hero-stat-num { font-size: 1.8rem; font-weight: 800; color: #FF6B35; }
    .hero-stat-lbl { font-size: 0.75rem; color: #6b7280; text-transform: uppercase; letter-spacing: 1px; }

    /* ── App body ── */
    .app-body {
        background: #080818;
        min-height: 100vh;
        padding: 40px 32px;
    }

    /* ── Section title ── */
    .section-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #e5e7eb;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .section-title::after {
        content: "";
        flex: 1;
        height: 1px;
        background: linear-gradient(90deg, #FF6B3540, transparent);
    }

    /* ── Glassmorphism cards ── */
    .glass-card {
        background: linear-gradient(135deg, #ffffff08, #ffffff04);
        border: 1px solid #ffffff12;
        border-radius: 20px;
        padding: 24px;
        backdrop-filter: blur(10px);
        margin-bottom: 16px;
    }

    /* ── Metric pill ── */
    .metric-pill {
        background: linear-gradient(135deg, #1a1a35, #2a1a45);
        border: 1px solid #ffffff15;
        border-radius: 16px;
        padding: 18px 22px;
        text-align: center;
    }
    .metric-pill-val {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #FF6B35, #FFD700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1;
    }
    .metric-pill-lbl {
        font-size: 0.72rem;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-top: 6px;
    }

    /* ── Confidence bar ── */
    .conf-wrap { margin: 6px 0 14px; }
    .conf-bg {
        background: #1a1a2e;
        border-radius: 999px;
        height: 10px;
        overflow: hidden;
    }
    .conf-fill {
        height: 100%;
        border-radius: 999px;
        transition: width 0.8s cubic-bezier(0.4,0,0.2,1);
    }

    /* ── Prediction tag ── */
    .pred-tag {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        background: linear-gradient(90deg, #FF6B3520, #7C3AED20);
        border: 1px solid #FF6B3540;
        color: #FF6B35;
        padding: 4px 12px;
        border-radius: 999px;
        font-size: 0.82rem;
        font-weight: 600;
        margin: 3px;
    }

    /* ── Nutrition row ── */
    .nut-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 10px;
        margin: 14px 0;
    }
    .nut-cell {
        background: #0d0d22;
        border: 1px solid #ffffff10;
        border-radius: 14px;
        padding: 12px 8px;
        text-align: center;
    }
    .nut-val { font-size: 1.4rem; font-weight: 700; }
    .nut-key { font-size: 0.68rem; color: #6b7280; text-transform: uppercase; letter-spacing: 1px; margin-top: 3px; }

    /* ── Upload zone ── */
    [data-testid="stFileUploadDropzone"] {
        background: linear-gradient(135deg, #0d0d2240, #1a0a2e40) !important;
        border: 2px dashed #FF6B3560 !important;
        border-radius: 16px !important;
    }

    /* ── Camera input ── */
    [data-testid="stCameraInput"] > div {
        border-radius: 16px !important;
        overflow: hidden;
        border: 2px solid #7C3AED40 !important;
    }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        background: #0d0d22;
        border-radius: 12px;
        padding: 4px;
        gap: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        color: #9ca3af;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #FF6B35, #F7931E) !important;
        color: white !important;
    }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: #080818;
        border-right: 1px solid #ffffff10;
    }
    section[data-testid="stSidebar"] * { color: #e5e7eb !important; }

    /* ── Slider ── */
    .stSlider [data-baseweb="slider"] [data-testid="stThumbValue"] { color: #FF6B35 !important; }

    /* ── Spinner ── */
    .stSpinner > div > div { border-top-color: #FF6B35 !important; }

    /* ── Feature badges (hero) ── */
    .feat-badges {
        display: flex;
        justify-content: center;
        gap: 10px;
        flex-wrap: wrap;
        margin-top: 20px;
    }
    .feat-badge {
        background: #ffffff08;
        border: 1px solid #ffffff15;
        color: #9ca3af;
        padding: 6px 14px;
        border-radius: 999px;
        font-size: 0.78rem;
    }

    /* ── Divider ── */
    .glow-divider {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #FF6B3560, transparent);
        margin: 28px 0;
    }

    /* ── Footer ── */
    .app-footer {
        text-align: center;
        padding: 40px 20px;
        color: #374151;
        font-size: 0.8rem;
        border-top: 1px solid #ffffff08;
        margin-top: 60px;
    }
    .app-footer a { color: #FF6B35; text-decoration: none; }

    /* ── Mobile responsive ── */
    @media (max-width: 768px) {
        .hero { padding: 50px 20px 36px; }
        .app-body { padding: 24px 16px; }
        .nut-grid { grid-template-columns: repeat(2, 1fr); }
        .hero-stats { gap: 20px; }
    }
    </style>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
# MODEL LOADING  (cached — downloads once, instant after)
# ─────────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_model():
    """
    Load ViT-Food101 from Hugging Face Hub.
    Primary : nateraw/food  (101 food classes, fine-tuned ViT)
    Fallback: google/vit-base-patch16-224  (ImageNet, 1000 classes)
    Both run on CPU — no GPU required.
    """
    try:
        from transformers import pipeline
        clf = pipeline("image-classification", model="nateraw/food", top_k=5)
        return clf, "nateraw/food", True
    except Exception as e1:
        try:
            from transformers import pipeline
            clf = pipeline("image-classification", model="google/vit-base-patch16-224", top_k=5)
            return clf, "google/vit-base-patch16-224 (fallback)", True
        except Exception as e2:
            return None, f"Load error: {e2}", False


# ─────────────────────────────────────────────────────────────────
# INFERENCE
# ─────────────────────────────────────────────────────────────────
def run_inference(clf, img: Image.Image, threshold: float):
    try:
        results = clf(img)
        filtered = [r for r in results if r["score"] >= threshold]
        return filtered if filtered else results[:1]
    except Exception as e:
        return [{"label": "error", "score": 0.0, "_error": str(e)}]


def lookup_nutrition(label: str):
    label_lower = label.lower().replace("_", " ")
    for kw, key in LABEL_MAP.items():
        if kw in label_lower:
            return key, NUTRITION_DB[key]
    return "unknown", NUTRITION_DB["default"]


# ─────────────────────────────────────────────────────────────────
# IMAGE ANNOTATION
# ─────────────────────────────────────────────────────────────────
def annotate_image(img: Image.Image, preds: list) -> Image.Image:
    img = img.copy().convert("RGB")
    if not preds:
        return img
    W, H = img.size
    top   = preds[0]
    label = top["label"].replace("_", " ").title()
    score = top["score"]
    _, nut = lookup_nutrition(top["label"])
    emoji  = nut["emoji"]
    accent = nut["color"]

    # Parse accent hex → RGB
    def hex_to_rgb(h):
        h = h.lstrip("#")
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    r, g, b = hex_to_rgb(accent)

    # Top banner overlay
    banner_h = max(54, H // 9)
    overlay  = Image.new("RGBA", img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.rectangle([0, 0, W, banner_h], fill=(r, g, b, 40))
    od.rectangle([0, 0, 5, banner_h], fill=(r, g, b, 220))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    try:
        fnt_lg = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", max(18, H // 22))
        fnt_sm = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",     max(13, H // 32))
    except Exception:
        fnt_lg = fnt_sm = ImageFont.load_default()

    draw.text((14, 10), f"{emoji} {label}  {score*100:.1f}%", fill=(255, 220, 60), font=fnt_lg)

    y = H - len(preds) * max(22, H // 28) - 8
    for p in preds[1:]:
        lbl = p["label"].replace("_", " ").title()
        draw.text((14, y), f"  • {lbl}: {p['score']*100:.1f}%", fill=(200, 200, 200), font=fnt_sm)
        y += max(22, H // 28)

    return img


# ─────────────────────────────────────────────────────────────────
# UI COMPONENTS
# ─────────────────────────────────────────────────────────────────
def render_hero():
    st.markdown("""
    <div class="hero">
        <div class="hero-badge">🤖 AI-Powered · Free · Open Source</div>
        <h1 class="hero-title">Identify Any Food<br>Instantly with AI</h1>
        <p class="hero-sub">
            Snap or upload a photo of any dish. Our Vision Transformer model
            recognises 101 food categories and gives you an instant nutritional breakdown —
            completely free, no sign-up required.
        </p>
        <div class="feat-badges">
            <span class="feat-badge">📷 Webcam Support</span>
            <span class="feat-badge">🖼️ Image Upload</span>
            <span class="feat-badge">⚡ Real-time Inference</span>
            <span class="feat-badge">🥦 Nutrition Info</span>
            <span class="feat-badge">🔒 Privacy First</span>
        </div>
        <div class="hero-stats">
            <div class="hero-stat">
                <div class="hero-stat-num">101</div>
                <div class="hero-stat-lbl">Food Classes</div>
            </div>
            <div class="hero-stat">
                <div class="hero-stat-num">&lt;1s</div>
                <div class="hero-stat-lbl">Inference Time</div>
            </div>
            <div class="hero-stat">
                <div class="hero-stat-num">100%</div>
                <div class="hero-stat-lbl">Free Forever</div>
            </div>
            <div class="hero-stat">
                <div class="hero-stat-num">0</div>
                <div class="hero-stat-lbl">Sign-ups Needed</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar(model_name: str, ok: bool):
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        st.divider()

        threshold = st.slider(
            "Confidence Threshold", 0.0, 1.0, 0.15, 0.05,
            help="Only show predictions at or above this score."
        )
        st.divider()

        # Model status
        icon = "✅" if ok else "❌"
        st.markdown(f"**{icon} Model**")
        st.caption(f"`{model_name}`")
        st.caption("ViT fine-tuned on Food-101")
        st.divider()

        st.markdown("**📖 How to use**")
        st.caption("1. Choose **Webcam** or **Upload** tab")
        st.caption("2. Capture or upload a food image")
        st.caption("3. Results appear instantly!")
        st.divider()

        st.markdown("**🥗 Sample Foods**")
        sample = ["🍕 Pizza","🍔 Burger","🍣 Sushi","🌮 Taco",
                  "🍦 Ice Cream","🍝 Pasta","🥗 Salad","🍩 Donut",
                  "🍟 Fries","🥩 Steak","🎂 Cake","🍌 Banana"]
        cols = st.columns(2)
        for i, f in enumerate(sample):
            cols[i % 2].caption(f)

        st.divider()
        st.caption("🔒 No images are stored. Everything runs in-memory.")
        st.caption("⭐ [Star on GitHub](https://github.com/yourusername/food-vision-ai)")

    return threshold


def render_metrics(preds: list):
    if not preds:
        return
    top   = preds[0]
    label = top["label"].replace("_", " ").title()
    score = top["score"]
    db_key, nut = lookup_nutrition(top["label"])
    emoji  = nut["emoji"]
    color  = nut["color"]

    conf_color = "#4CAF50" if score > 0.7 else "#FF9800" if score > 0.4 else "#EF5350"

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
        <div class="metric-pill">
            <div style="font-size:2.4rem">{emoji}</div>
            <div class="metric-pill-val" style="font-size:1.2rem;color:{color};">{label}</div>
            <div class="metric-pill-lbl">Predicted Food</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="metric-pill">
            <div class="metric-pill-val" style="-webkit-text-fill-color:{conf_color};">{score*100:.1f}%</div>
            <div class="metric-pill-lbl">Confidence</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="metric-pill">
            <div class="metric-pill-val">{nut['calories']}</div>
            <div class="metric-pill-lbl">kcal / serving</div>
        </div>""", unsafe_allow_html=True)

    # Prediction confidence bars
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">🎯 All Predictions</div>', unsafe_allow_html=True)
    for p in preds:
        lbl   = p["label"].replace("_", " ").title()
        sc    = p["score"]
        _, n  = lookup_nutrition(p["label"])
        col   = n["color"]
        pct   = int(sc * 100)
        st.markdown(f"""
        <div style="margin-bottom:10px;">
            <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                <span style="color:#e5e7eb;font-size:0.88rem;font-weight:500;">{n['emoji']} {lbl}</span>
                <span style="color:{col};font-size:0.88rem;font-weight:700;">{pct}%</span>
            </div>
            <div class="conf-bg">
                <div class="conf-fill" style="width:{pct}%;background:linear-gradient(90deg,{col}aa,{col});"></div>
            </div>
        </div>""", unsafe_allow_html=True)


def render_nutrition(db_key: str, nut: dict):
    emoji   = nut["emoji"]
    color   = nut["color"]
    serving = nut["serving"]
    cal, prot, carbs, fat = nut["calories"], nut["protein"], nut["carbs"], nut["fat"]

    cal_pct  = min(100, int(cal  / 600 * 100))
    prot_pct = min(100, int(prot / 50  * 100))
    carb_pct = min(100, int(carbs/ 80  * 100))
    fat_pct  = min(100, int(fat  / 40  * 100))

    st.markdown(f"""
    <div class="glass-card" style="border-color:{color}30;">
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:6px;">
            <span style="font-size:2.2rem">{emoji}</span>
            <div>
                <div style="font-size:1.3rem;font-weight:700;color:{color};">{db_key.title()}</div>
                <div style="font-size:0.78rem;color:#6b7280;">Per {serving}</div>
            </div>
        </div>

        <div class="nut-grid">
            <div class="nut-cell">
                <div class="nut-val" style="color:#FF6B35;">{cal}</div>
                <div class="nut-key">kcal</div>
            </div>
            <div class="nut-cell">
                <div class="nut-val" style="color:#4CAF50;">{prot}g</div>
                <div class="nut-key">protein</div>
            </div>
            <div class="nut-cell">
                <div class="nut-val" style="color:#2196F3;">{carbs}g</div>
                <div class="nut-key">carbs</div>
            </div>
            <div class="nut-cell">
                <div class="nut-val" style="color:#FF9800;">{fat}g</div>
                <div class="nut-key">fat</div>
            </div>
        </div>

        <div style="font-size:0.78rem;color:#4b5563;margin-bottom:5px;">Calories</div>
        <div class="conf-bg conf-wrap"><div class="conf-fill" style="width:{cal_pct}%;background:linear-gradient(90deg,#FF6B35,#FFD700);"></div></div>

        <div style="font-size:0.78rem;color:#4b5563;margin-bottom:5px;">Protein</div>
        <div class="conf-bg conf-wrap"><div class="conf-fill" style="width:{prot_pct}%;background:linear-gradient(90deg,#4CAF50,#81C784);"></div></div>

        <div style="font-size:0.78rem;color:#4b5563;margin-bottom:5px;">Carbohydrates</div>
        <div class="conf-bg conf-wrap"><div class="conf-fill" style="width:{carb_pct}%;background:linear-gradient(90deg,#2196F3,#64B5F6);"></div></div>

        <div style="font-size:0.78rem;color:#4b5563;margin-bottom:5px;">Fat</div>
        <div class="conf-bg conf-wrap"><div class="conf-fill" style="width:{fat_pct}%;background:linear-gradient(90deg,#FF9800,#FFB74D);"></div></div>

        <div style="font-size:0.7rem;color:#374151;margin-top:14px;padding-top:10px;border-top:1px solid #ffffff08;">
            ⚠️ Estimates only — not a substitute for professional dietary advice.
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────
def main():
    inject_css()
    render_hero()

    # Load model
    with st.spinner("🧠 Loading AI model… first run downloads ~350 MB, cached after that."):
        clf, model_name, model_ok = load_model()

    threshold = render_sidebar(model_name, model_ok)

    if not model_ok or clf is None:
        st.error(f"❌ Model could not load: {model_name}")
        st.info("Check your internet connection — the model needs to be downloaded on first run.")
        return

    # ── Body ──
    st.markdown('<div class="app-body">', unsafe_allow_html=True)

    tab_cam, tab_upload = st.tabs(["📷  Webcam Capture", "📁  Upload Image"])
    image_to_predict = None

    with tab_cam:
        st.markdown("")
        st.markdown('<div class="section-title">📷 Live Camera</div>', unsafe_allow_html=True)
        st.caption("Allow camera access, then click **Take Photo** to snap your food.")
        try:
            cam = st.camera_input("", label_visibility="collapsed")
            if cam:
                image_to_predict = Image.open(cam).convert("RGB")
        except Exception as e:
            st.warning(f"⚠️ Camera unavailable ({e}). Please use the Upload tab.")

    with tab_upload:
        st.markdown("")
        st.markdown('<div class="section-title">📁 Upload Image</div>', unsafe_allow_html=True)
        st.caption("Drag & drop or browse for a JPEG / PNG food photo.")
        up = st.file_uploader("", type=["jpg","jpeg","png","webp"], label_visibility="collapsed")
        if up:
            image_to_predict = Image.open(up).convert("RGB")

    # ── Prediction ──
    if image_to_predict is not None:
        st.markdown('<hr class="glow-divider">', unsafe_allow_html=True)

        col_img, col_res = st.columns([1.05, 1], gap="large")

        with col_img:
            st.markdown('<div class="section-title">🖼️ Analysed Image</div>', unsafe_allow_html=True)
            with st.spinner("🔍 Running AI inference…"):
                t0    = time.perf_counter()
                preds = run_inference(clf, image_to_predict, threshold)
                ms    = (time.perf_counter() - t0) * 1000

            annotated = annotate_image(image_to_predict, preds)
            st.image(annotated, use_container_width=True)
            st.caption(f"⚡ Inference completed in **{ms:.0f} ms** · Model: `{model_name}`")

        with col_res:
            if preds and "_error" not in preds[0]:
                st.markdown('<div class="section-title">📊 Results</div>', unsafe_allow_html=True)
                render_metrics(preds)

                st.markdown('<hr class="glow-divider">', unsafe_allow_html=True)
                st.markdown('<div class="section-title">🥦 Nutritional Breakdown</div>', unsafe_allow_html=True)
                db_key, nut = lookup_nutrition(preds[0]["label"])
                render_nutrition(db_key, nut)

                with st.expander("🔧 Raw model output (JSON)"):
                    st.json(preds)
            else:
                st.error("❌ Prediction failed — try a clearer, well-lit image.")
                if preds:
                    st.caption(preds[0].get("_error", "Unknown error"))

    else:
        # ── Empty / landing state ──
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align:center;padding:70px 30px;
                    background:linear-gradient(135deg,#0d0d22,#1a0a2e);
                    border-radius:24px;border:2px dashed #FF6B3530;margin-top:20px;">
            <div style="font-size:5.5rem;filter:drop-shadow(0 0 30px #FF6B3560);">🍽️</div>
            <h2 style="color:#e5e7eb;margin:16px 0 10px;font-weight:700;">Ready to Identify Your Food</h2>
            <p style="color:#6b7280;max-width:400px;margin:0 auto;">
                Use the <strong style="color:#FF6B35;">Webcam</strong> or
                <strong style="color:#FF6B35;">Upload</strong> tab above to get
                an instant AI prediction with full nutrition info.
            </p>
            <div style="margin-top:28px;display:flex;gap:10px;justify-content:center;flex-wrap:wrap;">
                <span style="background:#FF6B3520;border:1px solid #FF6B3540;color:#FF6B35;
                             padding:6px 16px;border-radius:999px;font-size:0.82rem;">101 Food Classes</span>
                <span style="background:#7C3AED20;border:1px solid #7C3AED40;color:#a78bfa;
                             padding:6px 16px;border-radius:999px;font-size:0.82rem;">Sub-second Inference</span>
                <span style="background:#4CAF5020;border:1px solid #4CAF5040;color:#4CAF50;
                             padding:6px 16px;border-radius:999px;font-size:0.82rem;">No GPU Required</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # close app-body

    # ── Footer ──
    st.markdown("""
    <div class="app-footer">
        🍽️ <strong>Food Vision AI</strong> · Built with
        <a href="https://streamlit.io">Streamlit</a> &
        <a href="https://huggingface.co/nateraw/food">Hugging Face ViT-Food101</a> ·
        <a href="https://github.com/yourusername/food-vision-ai">⭐ Star on GitHub</a> ·
        Nutritional values are estimates for informational purposes only.
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
