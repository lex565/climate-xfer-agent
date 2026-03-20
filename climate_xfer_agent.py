"""
CLIMATE-XFER · Multimodal Agent
Assignment 4 — Agentic Workflow · Tool Use · Multimodal Extraction
MSc Artificial Intelligence and Large Models · Beihang University
"""

import base64
import html as html_lib
import json
import re
import time
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CLIMATE-XFER · Multimodal Agent",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Asset Paths ──────────────────────────────────────────────────────────────
CLIMATE_BASE = Path(
    "D:/Masters Program 2025-2027/Semester 1_2/"
    "Artificial Intelligence and Large  Models/"
    "Final  Project/CLIMATE_XFER"
)
A3_DIR       = Path(
    "D:/Masters Program 2025-2027/Semester 1_2/"
    "Artificial Intelligence and Large  Models/"
    "Assignmnets/Assignment 3"
)
FIGURES_DIR  = CLIMATE_BASE / "reports" / "figures"
REPORTS_DIR  = CLIMATE_BASE / "reports"
LOGO_PATH    = A3_DIR / "SCHOOL LOGO.png"
BHU_LOGO     = CLIMATE_BASE / "Beihang Logo.jpg"

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:ital,wght@0,600;0,700;0,800;1,600&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background: #F4F7FB;
    color: #1A202C;
}

/* ── HERO ── */
.hero {
    background: linear-gradient(135deg, #071E38 0%, #0F3460 40%, #16578A 70%, #1A7BBF 100%);
    border-radius: 22px;
    padding: 0;
    margin-bottom: 1.8rem;
    color: white;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(7,30,56,0.25);
    display: flex;
    align-items: stretch;
}
.hero-left {
    flex: 1;
    padding: 2.6rem 2.5rem 2.2rem;
    position: relative;
}
.hero-left::after {
    content: '';
    position: absolute;
    width: 280px; height: 280px;
    border-radius: 50%;
    background: rgba(255,255,255,0.035);
    bottom: -100px; right: -60px;
    pointer-events: none;
}
.hero-right {
    width: 180px;
    background: rgba(255,255,255,0.06);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 1rem;
    padding: 1.5rem 1rem;
    border-left: 1px solid rgba(255,255,255,0.1);
    flex-shrink: 0;
}
.hero-logo-box {
    background: white;
    border-radius: 12px;
    padding: 0.5rem;
    width: 100px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 2px 10px rgba(0,0,0,0.15);
}
.hero-logo-box img { width: 100%; border-radius: 8px; }
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.55rem;
    font-weight: 800;
    line-height: 1.1;
    margin-bottom: 0.4rem;
    letter-spacing: -0.02em;
}
.hero-title span {
    font-style: italic;
    color: #7EC8F5;
}
.hero-sub {
    font-size: 0.95rem;
    font-weight: 300;
    opacity: 0.8;
    margin-bottom: 1.3rem;
    letter-spacing: 0.01em;
    line-height: 1.5;
}
.hero-badges { display: flex; flex-wrap: wrap; gap: 0.4rem; margin-bottom: 1.2rem; }
.badge {
    background: rgba(255,255,255,0.11);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 24px;
    padding: 0.26rem 0.85rem;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
.badge.accent {
    background: rgba(126,200,245,0.2);
    border-color: rgba(126,200,245,0.4);
    color: #B8E4FF;
}
.hero-authors {
    font-size: 0.76rem;
    opacity: 0.55;
    line-height: 1.8;
}
.hero-authors strong { opacity: 1; font-weight: 600; color: rgba(255,255,255,0.85); }
.hero-uni {
    font-size: 0.68rem;
    text-align: center;
    opacity: 0.6;
    color: #B8E4FF;
    font-weight: 500;
    letter-spacing: 0.03em;
}

/* ── SECTION LABEL ── */
.section-label {
    font-size: 0.62rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: #A0AEC0;
    margin-bottom: 0.75rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #E8EDF3;
}

/* ── CARDS ── */
.card {
    background: white;
    border-radius: 14px;
    padding: 1.5rem;
    box-shadow: 0 1px 12px rgba(0,0,0,0.06);
    border: 1px solid #E8EDF3;
    margin-bottom: 1rem;
}
.card-accent {
    border-top: 3px solid #1A7BBF;
}

/* ── NOTICE BANNER ── */
.notice {
    background: linear-gradient(135deg, #EBF8FF, #E6FFFA);
    border: 1px solid #BEE3F8;
    border-left: 4px solid #2E86AB;
    border-radius: 10px;
    padding: 1rem 1.4rem;
    margin-bottom: 1.2rem;
    font-size: 0.84rem;
    color: #2C5282;
    line-height: 1.65;
}
.notice strong { color: #1A365D; }

/* ── AGENT TRACE ── */
.trace-wrap { display: flex; flex-direction: column; gap: 0.5rem; }
.trace-step {
    border-radius: 10px;
    border-left: 4px solid #CBD5E0;
    padding: 0.85rem 1.25rem;
    box-shadow: 0 1px 5px rgba(0,0,0,0.05);
    background: white;
}
.trace-step.think  { border-left-color: #ED8936; background: #FFFAF0; }
.trace-step.call   { border-left-color: #3182CE; background: #EBF8FF; }
.trace-step.result { border-left-color: #38A169; background: #F0FFF4; }
.trace-step.final  { border-left-color: #805AD5; background: #FAF5FF; }
.trace-tag {
    font-size: 0.6rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 0.35rem;
}
.trace-step.think  .trace-tag { color: #C05621; }
.trace-step.call   .trace-tag { color: #2B6CB0; }
.trace-step.result .trace-tag { color: #276749; }
.trace-step.final  .trace-tag { color: #553C9A; }
.trace-content { font-size: 0.84rem; line-height: 1.65; color: #2D3748; }
.trace-content pre {
    background: #F7FAFC;
    border: 1px solid #E2E8F0;
    border-radius: 6px;
    padding: 0.65rem 0.85rem;
    font-size: 0.73rem;
    overflow-x: auto;
    margin-top: 0.45rem;
    white-space: pre-wrap;
    word-break: break-word;
}
.trace-content code {
    background: #EDF2F7;
    padding: 0.1rem 0.35rem;
    border-radius: 3px;
    font-size: 0.8rem;
    color: #2B6CB0;
}

/* ── STEP INDICATOR ── */
.step-card {
    background: white;
    border-radius: 12px;
    padding: 1rem 0.75rem;
    text-align: center;
    border: 1px solid #E8EDF3;
    box-shadow: 0 1px 6px rgba(0,0,0,0.05);
    transition: all 0.4s ease;
}
.step-card.done {
    background: linear-gradient(135deg, #F0FFF4, #E6FFFA);
    border-color: #9AE6B4;
    box-shadow: 0 2px 10px rgba(56,161,105,0.12);
}
.step-card.active {
    background: linear-gradient(135deg, #EBF8FF, #E9F5FF);
    border-color: #90CDF4;
    box-shadow: 0 2px 10px rgba(49,130,206,0.12);
}

/* ── BUTTONS ── */
div.stButton > button {
    background: linear-gradient(135deg, #0F3460 0%, #1A7BBF 100%);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 600;
    font-size: 0.9rem;
    padding: 0.6rem 2.2rem;
    letter-spacing: 0.02em;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}
div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(26,123,191,0.4);
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] { gap: 0.3rem; background: transparent; }
.stTabs [data-baseweb="tab"] {
    border-radius: 8px 8px 0 0;
    font-weight: 500;
    font-size: 0.88rem;
}

/* ── DATAFRAME ── */
.stDataFrame { border-radius: 10px; overflow: hidden; }

/* ── MISC ── */
#MainMenu, footer, header { visibility: hidden; }
hr { border-color: #EDF2F7; margin: 1rem 0; }
</style>
""", unsafe_allow_html=True)


# ─── Logo helper ──────────────────────────────────────────────────────────────
def img_to_b64(path):
    p = Path(path)
    if not p.exists():
        return None
    ext = p.suffix.lower().lstrip(".")
    mime = "jpeg" if ext in ("jpg", "jpeg") else "png"
    data = base64.b64encode(p.read_bytes()).decode()
    return f"data:image/{mime};base64,{data}"


logo_b64  = img_to_b64(LOGO_PATH)
bhu_b64   = img_to_b64(BHU_LOGO)

# Build logo HTML for hero
logo_html = ""
if bhu_b64:
    logo_html += f'<div class="hero-logo-box"><img src="{bhu_b64}" alt="Beihang"></div>'
if logo_b64:
    logo_html += f'<div class="hero-logo-box"><img src="{logo_b64}" alt="School"></div>'

hero_right = (
    f'<div class="hero-right">{logo_html}<div class="hero-uni">Beihang University<br>MSc AI &amp; Large Models<br>2025 – 2027</div></div>'
    if logo_html else ""
)

# ─── Hero Header ──────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
  <div class="hero-left">
    <div class="hero-title">🌊 CLIMATE&#8209;<span>XFER</span></div>
    <div class="hero-sub">
      Multimodal AI Agent &nbsp;·&nbsp; Diagram &amp; Table Extraction Pipeline<br>
      Agentic Workflow with Sequential Tool Use
    </div>
    <div class="hero-badges">
      <span class="badge">Assignment 4</span>
      <span class="badge">Sessions 9–10</span>
      <span class="badge accent">Agentic Workflow</span>
      <span class="badge accent">Tool Use</span>
      <span class="badge accent">Multimodal</span>
    </div>
    <div class="hero-authors">
      <strong>Tanaka Alex Mbendana</strong> &nbsp;LS2525233<br>
      <strong>Fitrotur Rofiqoh</strong> &nbsp;LS2525220<br>
      <strong>Munashe Innocent Mafuta</strong> &nbsp;LS2557204
    </div>
  </div>
  {hero_right}
</div>
""", unsafe_allow_html=True)

# ─── Session State ────────────────────────────────────────────────────────────
for _k, _v in [
    ("trace", []),
    ("extracted", {}),
    ("agent_done", False),
    ("final_text", ""),
    ("input_choice", "📊 Metrics Comparison (fig2)"),
]:
    if _k not in st.session_state:
        st.session_state[_k] = _v

# ─── Simulated Agent Data ─────────────────────────────────────────────────────
# All numbers are real values from metrics_all_summary.csv

SIMULATED_STEPS = [
    {
        "type": "think",
        "tag": "🧠 Agent Planning",
        "delay": 0.6,
        "content": (
            "I have received a multimodal input containing a metrics comparison figure and/or "
            "results table from the CLIMATE-XFER project. Let me plan my tool-call sequence:\n\n"
            "**Step 1** — `extract_performance_metrics`: Read RMSE, MAE, and Correlation "
            "values for all model/region combinations.\n"
            "**Step 2** — `identify_model_architectures`: Identify the neural network types, "
            "input features, and transfer strategies depicted.\n"
            "**Step 3** — `compare_transfer_learning`: Quantify the improvement from zero-shot "
            "to fine-tuned transfer and select the best configuration.\n"
            "**Step 4** — `generate_engineering_summary`: Synthesise findings into a structured "
            "engineering interpretation.\n\n"
            "Beginning execution now."
        ),
    },
    {
        "type": "call",
        "tag": "⚙️ Tool Call  ·  extract_performance_metrics",
        "delay": 0.5,
        "content": (
            "**`extract_performance_metrics`**\n"
            "```json\n"
            '{\n'
            '  "metrics": [\n'
            '    {"model": "mean_gru",             "region": "SADC", "transfer": "none",      "rmse": 0.1929, "mae": 0.1621, "correlation": 0.8350},\n'
            '    {"model": "persistence",           "region": "SADC", "transfer": "none",      "rmse": 0.2022, "mae": 0.1484, "correlation": 0.8068},\n'
            '    {"model": "cnn_gru",               "region": "SADC", "transfer": "none",      "rmse": 0.2268, "mae": 0.1951, "correlation": 0.7583},\n'
            '    {"model": "sadc_mean_gru",         "region": "SEA",  "transfer": "zero_shot", "rmse": 0.3113, "mae": 0.2524, "correlation": 0.8820},\n'
            '    {"model": "sea_mean_gru_finetuned","region": "SEA",  "transfer": "finetune",  "rmse": 0.2363, "mae": 0.1954, "correlation": 0.9028},\n'
            '    {"model": "persistence",           "region": "SEA",  "transfer": "none",      "rmse": 0.1844, "mae": 0.1441, "correlation": 0.9172}\n'
            '  ]\n'
            '}\n'
            "```"
        ),
    },
    {
        "type": "result",
        "tag": "✅ Tool Result  ·  extract_performance_metrics",
        "delay": 0.4,
        "content": (
            "```json\n"
            '{"status": "success", "extracted_rows": 6, "csv_rows_available": 8}\n'
            "```"
        ),
    },
    {
        "type": "call",
        "tag": "⚙️ Tool Call  ·  identify_model_architectures",
        "delay": 0.5,
        "content": (
            "**`identify_model_architectures`**\n"
            "```json\n"
            '{\n'
            '  "architectures": ["CNN-GRU (convolutional + gated recurrent unit)", "Mean-GRU (mean-pooled GRU baseline)"],\n'
            '  "input_features": ["Sea Surface Temperature — Indian Ocean (SST_IND)", "Sea Surface Temperature — Pacific Ocean (SST_PAC)", "SPEI drought index (target)"],\n'
            '  "transfer_strategies": ["Zero-shot transfer (SADC → SEA, no retraining)", "Fine-tuned transfer (SADC → SEA, partial retraining)"],\n'
            '  "regions": ["SADC — Southern Africa (source domain)", "SEA — Southeast Asia (target domain)"]\n'
            '}\n'
            "```"
        ),
    },
    {
        "type": "result",
        "tag": "✅ Tool Result  ·  identify_model_architectures",
        "delay": 0.4,
        "content": (
            "```json\n"
            '{"status": "success", "architectures": 2, "transfer_strategies": 2, "regions": 2}\n'
            "```"
        ),
    },
    {
        "type": "call",
        "tag": "⚙️ Tool Call  ·  compare_transfer_learning",
        "delay": 0.5,
        "content": (
            "**`compare_transfer_learning`**\n"
            "```json\n"
            '{\n'
            '  "zero_shot_rmse": 0.3113,\n'
            '  "finetuned_rmse": 0.2363,\n'
            '  "baseline_rmse": 0.1844,\n'
            '  "improvement_pct": 24.1,\n'
            '  "best_model": "sea_mean_gru_finetuned",\n'
            '  "recommendation": "Fine-tuning the SADC-trained model on a small SEA sample reduces RMSE by 24.1% over zero-shot transfer. While still above the SEA persistence baseline (0.1844), fine-tuning is the recommended strategy for cross-regional deployment."\n'
            '}\n'
            "```"
        ),
    },
    {
        "type": "result",
        "tag": "✅ Tool Result  ·  compare_transfer_learning",
        "delay": 0.4,
        "content": (
            "```json\n"
            '{"status": "success", "improvement_pct": 24.1, "best_model": "sea_mean_gru_finetuned"}\n'
            "```"
        ),
    },
    {
        "type": "call",
        "tag": "⚙️ Tool Call  ·  generate_engineering_summary",
        "delay": 0.5,
        "content": (
            "**`generate_engineering_summary`**\n"
            "```json\n"
            '{\n'
            '  "title": "CLIMATE-XFER: Cross-Regional Drought Prediction via Transfer Learning",\n'
            '  "summary": "The CLIMATE-XFER system demonstrates that a GRU-based model trained on SADC drought patterns can be transferred to Southeast Asia with measurable skill. Fine-tuning achieves an RMSE of 0.2363 on SEA — a 24.1% improvement over zero-shot transfer (0.3113) — validating the transfer learning hypothesis. The SADC source domain model (RMSE 0.1929) outperforms the persistence baseline (0.2022), confirming that deep learning adds genuine predictive value.",\n'
            '  "key_findings": [\n'
            '    "Mean-GRU (RMSE 0.1929) outperforms CNN-GRU (0.2268) and the persistence baseline (0.2022) on the SADC source domain.",\n'
            '    "Zero-shot SEA transfer degrades performance significantly (RMSE 0.3113 vs baseline 0.1844), confirming domain shift between SADC and SEA climate regimes.",\n'
            '    "Fine-tuning closes the gap by 24.1%, reducing SEA RMSE to 0.2363 — the best learned model for that region.",\n'
            '    "Correlation improves substantially with fine-tuning (0.8820 → 0.9028), indicating better temporal pattern capture."\n'
            '  ],\n'
            '  "limitations": "The SEA fine-tuned model still does not beat the persistence baseline on RMSE (0.2363 vs 0.1844), suggesting that SPEI in Southeast Asia is highly auto-correlated and the model training data may be insufficient for full domain adaptation.",\n'
            '  "future_work": "Investigate PEFT/LoRA-style partial fine-tuning to reduce data requirements. Include monsoon seasonality features specific to SEA. Explore larger source domain pre-training corpora spanning multiple climate zones."\n'
            '}\n'
            "```"
        ),
    },
    {
        "type": "result",
        "tag": "✅ Tool Result  ·  generate_engineering_summary",
        "delay": 0.4,
        "content": (
            "```json\n"
            '{"status": "success", "key_findings_count": 4}\n'
            "```"
        ),
    },
    {
        "type": "final",
        "tag": "🤖 Agent Final Response",
        "delay": 0.6,
        "content": (
            "All four tool calls completed successfully. The extraction pipeline processed the "
            "CLIMATE-XFER multimodal inputs and produced structured engineering outputs.\n\n"
            "**Summary of execution:**\n"
            "- Extracted 6 model-performance records across 2 regions\n"
            "- Identified 2 neural architectures, 3 input features, 2 transfer strategies\n"
            "- Quantified 24.1% RMSE improvement from zero-shot to fine-tuned transfer\n"
            "- Generated a 4-point engineering findings report with limitations and future work\n\n"
            "Full structured report is available in the **📊 Extracted Report** tab."
        ),
    },
]

# Extracted data mirroring the tool call inputs above
SIMULATED_EXTRACTED = {
    "extract_performance_metrics": {
        "metrics": [
            {"model": "mean_gru",             "region": "SADC", "transfer": "none",      "rmse": 0.1929, "mae": 0.1621, "correlation": 0.8350},
            {"model": "persistence",          "region": "SADC", "transfer": "none",      "rmse": 0.2022, "mae": 0.1484, "correlation": 0.8068},
            {"model": "cnn_gru",              "region": "SADC", "transfer": "none",      "rmse": 0.2268, "mae": 0.1951, "correlation": 0.7583},
            {"model": "sadc_mean_gru",        "region": "SEA",  "transfer": "zero_shot", "rmse": 0.3113, "mae": 0.2524, "correlation": 0.8820},
            {"model": "sea_mean_gru_finetuned","region": "SEA", "transfer": "finetune",  "rmse": 0.2363, "mae": 0.1954, "correlation": 0.9028},
            {"model": "persistence",          "region": "SEA",  "transfer": "none",      "rmse": 0.1844, "mae": 0.1441, "correlation": 0.9172},
        ]
    },
    "identify_model_architectures": {
        "architectures":       ["CNN-GRU (convolutional + gated recurrent unit)", "Mean-GRU (mean-pooled GRU baseline)"],
        "input_features":      ["SST — Indian Ocean", "SST — Pacific Ocean", "SPEI drought index (target)"],
        "transfer_strategies": ["Zero-shot transfer (SADC → SEA, no retraining)", "Fine-tuned transfer (SADC → SEA, partial retraining)"],
        "regions":             ["SADC — Southern Africa (source domain)", "SEA — Southeast Asia (target domain)"],
    },
    "compare_transfer_learning": {
        "zero_shot_rmse":  0.3113,
        "finetuned_rmse":  0.2363,
        "baseline_rmse":   0.1844,
        "improvement_pct": 24.1,
        "best_model":      "sea_mean_gru_finetuned",
        "recommendation":  (
            "Fine-tuning the SADC-trained model on a small SEA sample reduces RMSE by 24.1% "
            "over zero-shot transfer. While still above the SEA persistence baseline (0.1844), "
            "fine-tuning is the recommended strategy for cross-regional deployment."
        ),
    },
    "generate_engineering_summary": {
        "title":   "CLIMATE-XFER: Cross-Regional Drought Prediction via Transfer Learning",
        "summary": (
            "The CLIMATE-XFER system demonstrates that a GRU-based model trained on SADC drought "
            "patterns can be transferred to Southeast Asia with measurable skill. Fine-tuning "
            "achieves an RMSE of 0.2363 on SEA — a 24.1% improvement over zero-shot transfer "
            "(0.3113) — validating the transfer learning hypothesis. The SADC source domain model "
            "(RMSE 0.1929) outperforms the persistence baseline (0.2022), confirming that deep "
            "learning adds genuine predictive value."
        ),
        "key_findings": [
            "Mean-GRU (RMSE 0.1929) outperforms CNN-GRU (0.2268) and persistence baseline (0.2022) on SADC.",
            "Zero-shot SEA transfer degrades performance significantly (RMSE 0.3113 vs baseline 0.1844), confirming domain shift.",
            "Fine-tuning closes the gap by 24.1%, reducing SEA RMSE to 0.2363 — best learned model for the region.",
            "Correlation improves with fine-tuning (0.8820 → 0.9028), indicating better temporal pattern capture.",
        ],
        "limitations": (
            "The fine-tuned SEA model still does not beat the persistence baseline on RMSE "
            "(0.2363 vs 0.1844), suggesting SPEI in Southeast Asia is highly auto-correlated "
            "and training data may be insufficient for full domain adaptation."
        ),
        "future_work": (
            "Investigate PEFT/LoRA-style partial fine-tuning to reduce data requirements. "
            "Include monsoon seasonality features specific to SEA. Explore larger source domain "
            "pre-training corpora spanning multiple climate zones."
        ),
    },
}

FINAL_TEXT = (
    "All four tool calls completed successfully. The extraction pipeline processed the "
    "CLIMATE-XFER multimodal inputs and produced structured engineering outputs.\n\n"
    "Extracted 6 model-performance records · Identified 2 architectures & 2 transfer strategies · "
    "Quantified 24.1% RMSE improvement · Generated 4-point findings report with limitations."
)

# ─── Trace Helpers ────────────────────────────────────────────────────────────
def _md_to_html(text):
    def replace_code(m):
        code = html_lib.escape(m.group(1))
        return f"<pre><code>{code}</code></pre>"
    out = re.sub(r"```\w*\n(.*?)```", replace_code, text, flags=re.DOTALL)
    out = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"`(.*?)`", r"<code>\1</code>", out)
    out = out.replace("\n", "<br>")
    return out


def render_trace(placeholder):
    parts = ['<div class="trace-wrap">']
    for step in st.session_state.trace:
        content_html = _md_to_html(step["content"])
        parts.append(
            f'<div class="trace-step {step["type"]}">'
            f'<div class="trace-tag">{step["tag"]}</div>'
            f'<div class="trace-content">{content_html}</div>'
            f"</div>"
        )
    parts.append("</div>")
    placeholder.markdown("\n".join(parts), unsafe_allow_html=True)


# ─── Simulated Agent Runner ───────────────────────────────────────────────────
def run_simulation(speed, placeholder):
    st.session_state.trace     = []
    st.session_state.extracted = {}
    st.session_state.agent_done = False
    st.session_state.final_text = ""

    delays = {0: 0.0, 1: 0.35, 2: 0.7}
    d = delays.get(speed, 0.35)

    for step in SIMULATED_STEPS:
        time.sleep(step["delay"] * d)
        entry = {"type": step["type"], "tag": step["tag"], "content": step["content"]}
        st.session_state.trace.append(entry)
        render_trace(placeholder)

        # Populate extracted after result steps
        if step["type"] == "result":
            tag = step["tag"]
            if "extract_performance_metrics" in tag:
                st.session_state.extracted["extract_performance_metrics"] = \
                    SIMULATED_EXTRACTED["extract_performance_metrics"]
            elif "identify_model_architectures" in tag:
                st.session_state.extracted["identify_model_architectures"] = \
                    SIMULATED_EXTRACTED["identify_model_architectures"]
            elif "compare_transfer_learning" in tag:
                st.session_state.extracted["compare_transfer_learning"] = \
                    SIMULATED_EXTRACTED["compare_transfer_learning"]
            elif "generate_engineering_summary" in tag:
                st.session_state.extracted["generate_engineering_summary"] = \
                    SIMULATED_EXTRACTED["generate_engineering_summary"]

    st.session_state.final_text  = FINAL_TEXT
    st.session_state.agent_done  = True


# ─── TABS ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📂  Multimodal Input",
    "🤖  Agent Execution Loop",
    "📊  Extracted Report",
    "ℹ️  About",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — INPUT
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-label">Select Engineering Input</div>', unsafe_allow_html=True)
    col_l, col_r = st.columns([1, 1.4])

    with col_l:
        choice = st.selectbox(
            "Input source",
            options=[
                "📊 Metrics Comparison Figure (fig2)",
                "🗺️ Spatial Maps Figure (fig4)",
                "📋 Results Table (CSV)",
                "📊 + 📋 Figure + Table (Combined)",
            ],
            index=0,
            label_visibility="collapsed",
        )
        st.session_state.input_choice = choice

        st.markdown("""
        <div class="card card-accent" style="margin-top:1rem;">
          <div class="section-label">ℹ️ Input Guide</div>
          <table style="font-size:0.79rem;color:#4A5568;border-collapse:collapse;width:100%;">
            <tr>
              <td style="padding:0.35rem 0.8rem 0.35rem 0;font-weight:600;color:#1A4A7A;white-space:nowrap;vertical-align:top;">fig2</td>
              <td style="padding:0.35rem 0;line-height:1.5;">Bar chart comparing RMSE, MAE &amp; Correlation across all models</td>
            </tr>
            <tr>
              <td style="padding:0.35rem 0.8rem 0.35rem 0;font-weight:600;color:#1A4A7A;white-space:nowrap;vertical-align:top;">fig4</td>
              <td style="padding:0.35rem 0;line-height:1.5;">Spatial SPEI prediction maps for SADC &amp; SEA regions</td>
            </tr>
            <tr>
              <td style="padding:0.35rem 0.8rem 0.35rem 0;font-weight:600;color:#1A4A7A;white-space:nowrap;vertical-align:top;">CSV</td>
              <td style="padding:0.35rem 0;line-height:1.5;">Raw metrics table — 8 rows, 5 model configurations</td>
            </tr>
            <tr>
              <td style="padding:0.35rem 0.8rem 0.35rem 0;font-weight:600;color:#1A4A7A;white-space:nowrap;vertical-align:top;">Combined</td>
              <td style="padding:0.35rem 0;line-height:1.5;">fig2 image + CSV table sent together for richer context</td>
            </tr>
          </table>
        </div>
        """, unsafe_allow_html=True)

    with col_r:
        if "fig2" in choice:
            p = FIGURES_DIR / "fig2_metrics_comparison.png"
            if p.exists():
                st.image(str(p), caption="fig2 — Metrics Comparison (RMSE · MAE · Correlation)", use_container_width=True)
        elif "fig4" in choice:
            p = FIGURES_DIR / "fig4_spatial_maps.png"
            if p.exists():
                st.image(str(p), caption="fig4 — Spatial SPEI Predictions across SADC & SEA", use_container_width=True)
        elif "CSV" in choice and "+" not in choice:
            try:
                df = pd.read_csv(REPORTS_DIR / "metrics_all_summary.csv")
                cols = [c for c in ["region", "model", "transfer", "rmse", "mae", "corr"] if c in df.columns]
                st.markdown('<div class="section-label">Results Table — metrics_all_summary.csv</div>', unsafe_allow_html=True)
                st.dataframe(df[cols].dropna(subset=["rmse"]), use_container_width=True, hide_index=True)
            except Exception as e:
                st.error(f"Could not load CSV: {e}")
        else:
            p = FIGURES_DIR / "fig2_metrics_comparison.png"
            if p.exists():
                st.image(str(p), caption="Combined input: fig2 image + CSV table", use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — AGENT EXECUTION LOOP
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    col_btn, col_speed, col_status = st.columns([1, 1.2, 2.5])
    with col_btn:
        run_btn = st.button("▶  Run Agent", use_container_width=True)
    with col_speed:
        speed = st.select_slider(
            "Replay speed",
            options=["Fast", "Normal", "Slow"],
            value="Normal",
            label_visibility="visible",
        )
        speed_val = {"Fast": 0, "Normal": 1, "Slow": 2}[speed]
    with col_status:
        st.write("")
        if st.session_state.agent_done:
            st.success("✅ Agent completed — 4 tools executed, report ready.")
        elif st.session_state.trace:
            st.info("⏳ Agent is running…")
        else:
            st.caption("Select an input in **📂 Tab 1**, then click **▶ Run Agent**.")

    st.markdown("<hr>", unsafe_allow_html=True)

    # Step indicators
    STEPS = [
        ("extract_performance_metrics",  "📏", "Extract Metrics"),
        ("identify_model_architectures", "🏗️", "Identify Architectures"),
        ("compare_transfer_learning",    "⚖️", "Compare Transfer"),
        ("generate_engineering_summary", "📝", "Generate Summary"),
    ]
    done_tools = set(st.session_state.extracted.keys())
    s_cols = st.columns(4)
    for col, (tool, icon, label) in zip(s_cols, STEPS):
        done = tool in done_tools
        cls  = "done" if done else ""
        c_lbl = "#276749" if done else "#A0AEC0"
        c_chk = "#48BB78" if done else "#E2E8F0"
        with col:
            st.markdown(
                f'<div class="step-card {cls}">'
                f'<div style="font-size:1.35rem;">{icon}</div>'
                f'<div style="font-size:0.7rem;font-weight:600;margin-top:0.3rem;color:{c_lbl};">{label}</div>'
                f'<div style="font-size:0.68rem;margin-top:0.18rem;color:{c_chk};">{"✓ Done" if done else "· Pending"}</div>'
                f"</div>",
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    trace_placeholder = st.empty()
    if st.session_state.trace:
        render_trace(trace_placeholder)

    if run_btn:
        run_simulation(speed_val, trace_placeholder)
        st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — EXTRACTED REPORT
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    if not st.session_state.agent_done:
        st.markdown("""
        <div class="card" style="text-align:center;padding:3rem 1.5rem;">
          <div style="font-size:2.8rem;">📊</div>
          <div style="font-size:1rem;font-weight:600;margin-top:0.8rem;color:#4A5568;">No Report Yet</div>
          <div style="font-size:0.84rem;color:#A0AEC0;margin-top:0.4rem;">
            Run the agent in <strong>🤖 Tab 2</strong> to generate the extraction report.
          </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        ext = st.session_state.extracted

        # Engineering Summary
        if "generate_engineering_summary" in ext:
            s = ext["generate_engineering_summary"]
            st.markdown(
                f'<div class="card card-accent">'
                f'<div class="section-label">📝 Engineering Summary</div>'
                f'<h3 style="font-family:\'Playfair Display\',serif;font-size:1.2rem;'
                f'color:#071E38;margin-bottom:0.8rem;line-height:1.3;">'
                f'{html_lib.escape(s.get("title","CLIMATE-XFER Analysis"))}</h3>'
                f'<p style="font-size:0.88rem;line-height:1.8;color:#4A5568;">'
                f'{html_lib.escape(s.get("summary",""))}</p></div>',
                unsafe_allow_html=True,
            )

            kf = s.get("key_findings", [])
            if kf:
                items = "".join(
                    f'<li style="margin-bottom:0.5rem;padding-left:0.3rem;">{html_lib.escape(f)}</li>'
                    for f in kf
                )
                st.markdown(
                    f'<div class="card"><div class="section-label">🔍 Key Findings</div>'
                    f'<ul style="font-size:0.86rem;line-height:1.75;color:#4A5568;padding-left:1.3rem;">'
                    f"{items}</ul></div>",
                    unsafe_allow_html=True,
                )

            c_lim, c_fw = st.columns(2)
            with c_lim:
                if s.get("limitations"):
                    st.markdown(
                        f'<div class="card"><div class="section-label">⚠️ Limitations</div>'
                        f'<p style="font-size:0.84rem;color:#718096;line-height:1.7;">'
                        f'{html_lib.escape(s["limitations"])}</p></div>',
                        unsafe_allow_html=True,
                    )
            with c_fw:
                if s.get("future_work"):
                    st.markdown(
                        f'<div class="card"><div class="section-label">🚀 Future Work</div>'
                        f'<p style="font-size:0.84rem;color:#718096;line-height:1.7;">'
                        f'{html_lib.escape(s["future_work"])}</p></div>',
                        unsafe_allow_html=True,
                    )

        # Metrics Table + Chart
        if "extract_performance_metrics" in ext:
            metrics_data = ext["extract_performance_metrics"].get("metrics", [])
            if metrics_data:
                df_m = pd.DataFrame(metrics_data)
                st.markdown('<div class="section-label" style="margin-top:0.5rem;">📏 Extracted Performance Metrics</div>', unsafe_allow_html=True)

                fmt = {c: "{:.4f}" for c in ["rmse", "mae", "correlation"] if c in df_m.columns}
                st.dataframe(
                    df_m.style.format(fmt, na_rep="—").highlight_min(
                        subset=["rmse", "mae"], color="#C6F6D5"
                    ).highlight_max(
                        subset=["correlation"], color="#C6F6D5"
                    ),
                    use_container_width=True,
                    hide_index=True,
                )

                # Metric summary pills
                if "rmse" in df_m.columns:
                    df_v = df_m.dropna(subset=["rmse"])
                    if not df_v.empty:
                        best = df_v.sort_values("rmse").iloc[0]
                        c1, c2, c3, c4 = st.columns(4)
                        c1.metric("Best RMSE", f"{best['rmse']:.4f}", delta="lowest ↓")
                        c2.metric("Best Model", best.get("model", "—"))
                        c3.metric("Region", best.get("region", "—"))
                        c4.metric("Models Evaluated", str(len(df_m)))

                # Plotly chart
                if len(df_m) >= 2 and "rmse" in df_m.columns:
                    try:
                        df_plot = df_m.dropna(subset=["rmse"]).copy()
                        df_plot["label"] = df_plot["model"] + " (" + df_plot["region"] + ")"
                        fig = px.bar(
                            df_plot,
                            x="label",
                            y="rmse",
                            color="region",
                            barmode="group",
                            title="Model RMSE by Region  —  lower is better",
                            labels={"rmse": "RMSE ↓", "label": ""},
                            color_discrete_map={"SADC": "#1A7BBF", "SEA": "#38A169"},
                            template="simple_white",
                        )
                        fig.update_layout(
                            font_family="Inter",
                            title_font_size=13,
                            title_font_color="#071E38",
                            legend=dict(orientation="h", y=1.08, x=0),
                            margin=dict(t=55, b=10, l=10, r=10),
                            xaxis_tickangle=-25,
                        )
                        fig.update_traces(marker_line_width=0)
                        st.plotly_chart(fig, use_container_width=True)
                    except Exception:
                        pass

        # Transfer Learning
        if "compare_transfer_learning" in ext:
            cmp = ext["compare_transfer_learning"]
            rows = []
            if cmp.get("zero_shot_rmse") is not None:
                rows.append(f"<strong>Zero-shot RMSE:</strong> {cmp['zero_shot_rmse']:.4f}")
            if cmp.get("finetuned_rmse") is not None:
                rows.append(f"<strong>Fine-tuned RMSE:</strong> {cmp['finetuned_rmse']:.4f}")
            if cmp.get("baseline_rmse") is not None:
                rows.append(f"<strong>Persistence baseline RMSE:</strong> {cmp['baseline_rmse']:.4f}")
            if cmp.get("improvement_pct") is not None:
                rows.append(f"<strong>Improvement (zero-shot → fine-tuned):</strong> {cmp['improvement_pct']:.1f}%")
            rows.append(f"<strong>Best model:</strong> {html_lib.escape(cmp.get('best_model','—'))}")
            rows.append(f"<strong>Recommendation:</strong> {html_lib.escape(cmp.get('recommendation','—'))}")
            st.markdown(
                f'<div class="card"><div class="section-label">⚖️ Transfer Learning Comparison</div>'
                f'<p style="font-size:0.86rem;line-height:2;color:#4A5568;">{"<br>".join(rows)}</p></div>',
                unsafe_allow_html=True,
            )

        # Architectures
        if "identify_model_architectures" in ext:
            arch = ext["identify_model_architectures"]
            st.markdown('<div class="section-label" style="margin-top:0.3rem;">🏗️ Architecture Details</div>', unsafe_allow_html=True)
            cols3 = st.columns(3)
            secs = [
                ("Architectures",      arch.get("architectures", [])),
                ("Input Features",     arch.get("input_features", [])),
                ("Transfer Strategies", arch.get("transfer_strategies", [])),
            ]
            for col, (title, items) in zip(cols3, secs):
                with col:
                    li = "".join(
                        f'<li style="margin-bottom:0.35rem;">{html_lib.escape(x)}</li>'
                        for x in items
                    ) or '<li style="color:#A0AEC0;">—</li>'
                    st.markdown(
                        f'<div class="card"><div class="section-label">{title}</div>'
                        f'<ul style="font-size:0.81rem;color:#4A5568;padding-left:1.1rem;line-height:1.65;">'
                        f"{li}</ul></div>",
                        unsafe_allow_html=True,
                    )

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — ABOUT
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    col_a, col_b = st.columns([1.6, 1])

    with col_a:
        st.markdown("""
        <div class="card card-accent">
          <div class="section-label">📌 About This Application</div>
          <p style="font-size:0.88rem;line-height:1.8;color:#4A5568;">
            This app demonstrates an <strong>agentic workflow</strong> for multimodal engineering
            data extraction — a core concept from <em>Sessions 9–10</em> of the
            MSc AI &amp; Large Models course. The agent receives complex engineering inputs
            (figures and tables from the CLIMATE-XFER project) and executes a planned
            sequence of <strong>four tool calls</strong> to extract structured knowledge.
          </p>
        </div>

        <div class="card">
          <div class="section-label">🔄 How the Agentic Loop Works</div>
          <table style="font-size:0.82rem;color:#4A5568;border-collapse:collapse;width:100%;">
            <tr style="border-bottom:1px solid #EDF2F7;">
              <td style="padding:0.5rem 0.8rem 0.5rem 0;font-weight:600;color:#0F3460;white-space:nowrap;">Step 1</td>
              <td style="padding:0.5rem 0;"><strong>Plan</strong> — agent reasons about the input and decides which tools to call</td>
            </tr>
            <tr style="border-bottom:1px solid #EDF2F7;">
              <td style="padding:0.5rem 0.8rem 0.5rem 0;font-weight:600;color:#0F3460;">Step 2</td>
              <td style="padding:0.5rem 0;"><strong>Extract Metrics</strong> — RMSE, MAE, Correlation per model/region</td>
            </tr>
            <tr style="border-bottom:1px solid #EDF2F7;">
              <td style="padding:0.5rem 0.8rem 0.5rem 0;font-weight:600;color:#0F3460;">Step 3</td>
              <td style="padding:0.5rem 0;"><strong>Identify Architectures</strong> — CNN-GRU, Mean-GRU, input features, transfer strategies</td>
            </tr>
            <tr style="border-bottom:1px solid #EDF2F7;">
              <td style="padding:0.5rem 0.8rem 0.5rem 0;font-weight:600;color:#0F3460;">Step 4</td>
              <td style="padding:0.5rem 0;"><strong>Compare Transfer</strong> — zero-shot vs fine-tuned RMSE, % improvement</td>
            </tr>
            <tr>
              <td style="padding:0.5rem 0.8rem 0.5rem 0;font-weight:600;color:#0F3460;">Step 5</td>
              <td style="padding:0.5rem 0;"><strong>Summarise</strong> — structured engineering report with findings, limitations, future work</td>
            </tr>
          </table>
        </div>
        """, unsafe_allow_html=True)

        # ── Prompt Engineering Section ───────────────────────────────────────
        st.markdown("""
        <div class="card" style="border-top:3px solid #805AD5;">
          <div class="section-label" style="color:#553C9A;">🧑‍💻 Prompt Engineering — What Was Sent to the Model</div>
          <p style="font-size:0.84rem;color:#4A5568;line-height:1.7;margin-bottom:1rem;">
            The agent is driven by two carefully crafted prompts passed to
            <code>claude-opus-4-6</code> via the Anthropic Messages API.
            Prompt design controls the agent's behaviour — without explicit instructions
            to use <em>all four tools in order</em>, the model may skip steps or stop early.
          </p>

          <div class="section-label">① System Prompt — Sets the Agent's Role &amp; Rules</div>
          <pre style="background:#FAF5FF;border:1px solid #E9D8FD;border-radius:8px;padding:1rem;font-size:0.76rem;line-height:1.6;color:#2D3748;white-space:pre-wrap;word-break:break-word;">You are a climate machine learning engineering agent.
Use all four tools in the exact order specified.
Extract real numbers from the provided inputs.</pre>
          <p style="font-size:0.78rem;color:#718096;margin:0.4rem 0 1rem 0;line-height:1.5;">
            <strong>Why:</strong> A concise, directive system prompt is more reliable than a long one.
            Naming the constraint explicitly (<em>"all four tools in exact order"</em>) prevents the model
            from short-circuiting the loop after the first tool call.
          </p>

          <div class="section-label">② User Message — Multimodal Input Construction</div>
          <pre style="background:#FAF5FF;border:1px solid #E9D8FD;border-radius:8px;padding:1rem;font-size:0.76rem;line-height:1.6;color:#2D3748;white-space:pre-wrap;word-break:break-word;">[
  {
    "type": "image",
    "source": {
      "type": "base64",
      "media_type": "image/png",
      "data": "&lt;base64-encoded fig2_metrics_comparison.png&gt;"
    }
  },
  {
    "type": "text",
    "text": "Results table (CSV):\\n```csv\\nregion,model,rmse,mae,...\\n```"
  },
  {
    "type": "text",
    "text": "You are an AI engineering agent analysing the CLIMATE-XFER project —
a GRU-based climate transfer learning model predicting SPEI drought indices
across SADC (Southern Africa) and SEA (Southeast Asia).
Thoroughly analyse the provided diagram and/or table.
You MUST call all four tools in sequence:
(1) extract_performance_metrics,
(2) identify_model_architectures,
(3) compare_transfer_learning,
(4) generate_engineering_summary.
Be precise — use the actual numbers you observe."
  }
]</pre>
          <p style="font-size:0.78rem;color:#718096;margin:0.4rem 0 1rem 0;line-height:1.5;">
            <strong>Why multimodal:</strong> Sending both the image and the CSV table gives the model
            two complementary evidence sources — visual bar heights from the figure and exact numeric
            values from the table — improving extraction accuracy.
            The numbered tool list in the instruction is a prompt engineering technique that enforces
            a deterministic execution order in the agentic loop.
          </p>

          <div class="section-label">③ Example Tool Schema — extract_performance_metrics</div>
          <pre style="background:#FAF5FF;border:1px solid #E9D8FD;border-radius:8px;padding:1rem;font-size:0.76rem;line-height:1.6;color:#2D3748;white-space:pre-wrap;word-break:break-word;">{
  "name": "extract_performance_metrics",
  "description": "Extract quantitative performance metrics (RMSE, MAE, Correlation)
for each model and geographic region from the provided engineering diagram or table.",
  "input_schema": {
    "type": "object",
    "properties": {
      "metrics": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "model":       { "type": "string" },
            "region":      { "type": "string" },
            "transfer":    { "type": "string", "description": "none | zero_shot | finetune" },
            "rmse":        { "type": "number" },
            "mae":         { "type": "number" },
            "correlation": { "type": "number" }
          },
          "required": ["model", "region"]
        }
      }
    },
    "required": ["metrics"]
  }
}</pre>
          <p style="font-size:0.78rem;color:#718096;margin:0.4rem 0 0 0;line-height:1.5;">
            <strong>Why JSON schema:</strong> The structured <code>input_schema</code> forces the model
            to return machine-readable, typed output rather than free text — this is what enables
            downstream automated processing of the extracted data. All four tools follow this pattern.
          </p>
        </div>
        """, unsafe_allow_html=True)

        # Why no live API notice — prominent but tasteful
        st.markdown("""
        <div class="notice">
          <strong>📝 Note on API Usage — Why This App Uses Simulated Agent Responses</strong><br><br>
          This demonstration uses a <strong>pre-scripted simulation</strong> of the Claude API
          agentic loop rather than live API calls. The agent's planning text, tool call inputs,
          tool results, and final summary are all derived from the real CLIMATE-XFER project
          data (using actual RMSE, MAE, and Correlation values from
          <code>metrics_all_summary.csv</code>), but are replayed locally without contacting
          the Anthropic API.<br><br>
          <strong>Why?</strong> The Anthropic API operates on a credit-based billing model.
          Each live multimodal agent run — sending images and multi-turn tool-use messages
          to <code>claude-opus-4-6</code> — consumes API credits. For an educational
          demonstration where the workflow is the deliverable (not the API response itself),
          a high-fidelity simulation achieves the same learning objective without recurring
          cost. The tool call structure, JSON schemas, multi-turn conversation format, and
          agent reasoning shown here are <strong>identical</strong> to what a live API call
          would produce — only the HTTP request is omitted.
        </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown("""
        <div class="card">
          <div class="section-label">🌊 CLIMATE-XFER Project</div>
          <p style="font-size:0.83rem;line-height:1.7;color:#4A5568;">
            A GRU-based deep learning system for predicting SPEI
            (Standardised Precipitation-Evapotranspiration Index)
            drought conditions across two geographic domains:
          </p>
          <ul style="font-size:0.82rem;color:#4A5568;padding-left:1.1rem;line-height:1.8;margin-top:0.5rem;">
            <li><strong>SADC</strong> — Southern Africa (source domain, primary training)</li>
            <li><strong>SEA</strong> — Southeast Asia (target domain, transfer learning)</li>
          </ul>
          <p style="font-size:0.82rem;line-height:1.7;color:#718096;margin-top:0.7rem;">
            Input features: SST Indian Ocean, SST Pacific Ocean.
            Transfer strategies: zero-shot and fine-tuned.
          </p>
        </div>

        <div class="card">
          <div class="section-label">🛠️ Tools Defined</div>
          <ul style="font-size:0.82rem;color:#4A5568;padding-left:1.1rem;line-height:2;">
            <li><code>extract_performance_metrics</code></li>
            <li><code>identify_model_architectures</code></li>
            <li><code>compare_transfer_learning</code></li>
            <li><code>generate_engineering_summary</code></li>
          </ul>
        </div>

        <div class="card">
          <div class="section-label">👥 Authors</div>
          <p style="font-size:0.82rem;line-height:2;color:#4A5568;">
            <strong>Tanaka Alex Mbendana</strong><br>LS2525233<br>
            <strong>Fitrotur Rofiqoh</strong><br>LS2525220<br>
            <strong>Munashe Innocent Mafuta</strong><br>LS2557204
          </p>
        </div>
        """, unsafe_allow_html=True)

        # Show logos in About tab too
        if bhu_b64 or logo_b64:
            logo_row = ""
            if bhu_b64:
                logo_row += f'<img src="{bhu_b64}" style="height:60px;border-radius:8px;margin-right:12px;box-shadow:0 2px 8px rgba(0,0,0,0.1);">'
            if logo_b64:
                logo_row += f'<img src="{logo_b64}" style="height:60px;border-radius:8px;box-shadow:0 2px 8px rgba(0,0,0,0.1);">'
            st.markdown(
                f'<div style="display:flex;align-items:center;margin-top:0.5rem;">{logo_row}</div>',
                unsafe_allow_html=True,
            )
