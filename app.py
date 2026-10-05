import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from io import StringIO

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Merchant MDR Copilot",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Design tokens
INK, PAPER, TEAL = "#0e1b2c", "#f3f5f8", "#0f766e"
C_OK, C_OVER, C_UNDER, C_DATA = "#0f9d75", "#d9372b", "#e08a00", "#64748b"
STATUS_COLOR = {
    "Correct": C_OK,
    "Over-Deduction": C_OVER,
    "Under-Deduction": C_UNDER,
    "Data Issue": C_DATA,
}
STATUS_EMOJI = {
    "Correct": "🟢",
    "Over-Deduction": "🔴",
    "Under-Deduction": "🟠",
    "Data Issue": "⚪",
}

# =========================================================
# CSS
# =========================================================
st.markdown(
    f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {{ font-family: 'Manrope', sans-serif; }}
.stApp {{ background: {PAPER}; }}
.block-container {{ padding-top: 1.2rem; padding-bottom: 3rem; max-width: 1400px; }}
header[data-testid="stHeader"] {{ background: transparent; }}

/* Hero */
.hero {{
    display: grid; grid-template-columns: 1.3fr 1fr; gap: 28px; align-items: center;
    padding: 30px 34px; border-radius: 20px; color: #fff; margin-bottom: 22px;
    background: linear-gradient(120deg, {INK} 0%, #14304a 70%, #0f4c4a 100%);
    box-shadow: 0 16px 40px rgba(14,27,44,.18);
    animation: rise .6s ease both;
}}
.hero h1 {{ margin: 0; font-size: 2.1rem; font-weight: 800; letter-spacing: -.8px; }}
.hero p {{ margin: 8px 0 0; color: #b6c4d4; font-size: .98rem; max-width: 520px; line-height: 1.55; }}
.hero-right {{
    background: rgba(255,255,255,.07); border: 1px solid rgba(255,255,255,.14);
    border-radius: 16px; padding: 18px 22px;
}}
.hero-right .lbl {{ color: #b6c4d4; font-size: .85rem; font-weight: 600; }}
.hero-right .big {{ font-size: 2.6rem; font-weight: 800; letter-spacing: -1.5px; line-height: 1.1; font-variant-numeric: tabular-nums; }}
.hero-right .sub {{ color: #b6c4d4; font-size: .85rem; margin-top: 4px; }}
.hero-right.bad .big {{ color: #ff8a80; }}
.hero-right.good .big {{ color: #6ee7b7; }}

.section-title {{ font-size: 1.1rem; font-weight: 800; color: {INK}; margin: 22px 0 10px; }}

/* KPI cards */
.kpi {{
    background: #fff; border: 1px solid #e3e8ef; border-left: 4px solid var(--c, {TEAL});
    border-radius: 14px; padding: 14px 16px; height: 100%;
}}
.kpi .k-label {{ color: #5b6b7f; font-size: .82rem; font-weight: 600; }}
.kpi .k-value {{ color: {INK}; font-size: 1.55rem; font-weight: 800; letter-spacing: -.5px; font-variant-numeric: tabular-nums; }}
.kpi .k-sub {{ color: #7a8899; font-size: .78rem; margin-top: 2px; }}

/* Category cards */
.cat {{
    background: #fff; border: 1px solid #e3e8ef; border-radius: 14px; padding: 14px 16px;
    transition: border-color .2s, box-shadow .2s;
}}
.cat:hover {{ border-color: {TEAL}; box-shadow: 0 8px 22px rgba(15,118,110,.12); }}
.cat.active {{ border-color: {TEAL}; box-shadow: 0 0 0 2px rgba(15,118,110,.18); }}
.cat .name {{ font-weight: 700; color: {INK}; }}
.cat .meta {{ font-size: .78rem; color: #7a8899; margin: 2px 0 8px; }}
.cat .bar {{ height: 6px; border-radius: 6px; background: #e8edf3; overflow: hidden; }}
.cat .bar span {{ display: block; height: 100%; background: {C_OK}; }}
.cat .flag {{ font-size: .86rem; font-weight: 700; margin-top: 8px; }}
.cat .flag.bad {{ color: {C_OVER}; }}
.cat .flag.good {{ color: {C_OK}; }}

/* Recommendation */
.rec {{ border-radius: 14px; padding: 18px 20px; border-left: 5px solid; line-height: 1.65; }}
.rec.danger {{ background: #fef2f1; border-color: {C_OVER}; color: #7f1d1d; }}
.rec.warn {{ background: #fff7e6; border-color: {C_UNDER}; color: #7a4a00; }}
.rec.ok {{ background: #ecfaf4; border-color: {C_OK}; color: #065f46; }}

/* Explainer steps */
.step {{ background: #fff; border: 1px solid #e3e8ef; border-radius: 14px; padding: 14px 16px; height: 100%; }}
.step .t {{ color: #5b6b7f; font-size: .8rem; font-weight: 600; }}
.step .v {{ color: {INK}; font-size: 1.2rem; font-weight: 800; margin-top: 3px; font-variant-numeric: tabular-nums; }}
.step .d {{ color: #7a8899; font-size: .78rem; margin-top: 3px; }}

/* Streamlit widgets */
div[data-testid="stTabs"] button[role="tab"] {{ font-weight: 700; font-size: .95rem; }}
div[data-testid="stTabs"] button[aria-selected="true"] {{ color: {TEAL}; }}
section[data-testid="stSidebar"] {{ background: #fff; border-right: 1px solid #e3e8ef; }}
.stButton > button, .stDownloadButton > button {{
    border-radius: 10px; font-weight: 700; border: 1px solid #cfd8e3; transition: all .15s;
}}
.stButton > button:hover, .stDownloadButton > button:hover {{ border-color: {TEAL}; color: {TEAL}; }}
div[data-testid="stDataFrame"] {{ border: 1px solid #e3e8ef; border-radius: 12px; overflow: hidden; }}

@keyframes rise {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; transform: none; }} }}
@media (max-width: 900px) {{ .hero {{ grid-template-columns: 1fr; }} }}
@media (prefers-reduced-motion: reduce) {{ .hero {{ animation: none; }} }}
</style>
""",
    unsafe_allow_html=True,
)


# =========================================================
# HELPERS
# =========================================================
def inr(v, d=2):
    return f"₹{v:,.{d}f}"


def kpi(label, value, sub="", color=TEAL):
    return (
        f'<div class="kpi" style="--c:{color}"><div class="k-label">{label}</div>'
        f'<div class="k-value">{value}</div><div class="k-sub">{sub}</div></div>'
    )


def style_fig(fig, height=300):
    fig.update_layout(
        height=height,
        margin=dict(l=10, r=10, t=36, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Manrope, sans-serif", color=INK),
        legend=dict(orientation="h", y=-0.15),
        title_font=dict(size=14),
    )
    fig.update_xaxes(gridcolor="#e8edf3", zeroline=False)
    fig.update_yaxes(gridcolor="#e8edf3", zeroline=False)
    return fig


# =========================================================
# DEMO DATA
# =========================================================
def demo_data():
    return pd.read_csv(
        StringIO(
            """
Transaction_ID,Date,Category,Payment_Type,Amount,Actual_Deduction,Net_Settlement
TXN001,2026-10-15,Grocery,UPI,1500,0,1500
TXN002,2026-10-15,Electronics,UPI,2500,10,2490
TXN003,2026-10-16,Pharmacy,UPI,5000,20,4980
TXN004,2026-10-16,Retail,UPI,1800,0,1800
TXN005,2026-10-17,Grocery,UPI,3000,12,2988
TXN006,2026-10-17,Electronics,UPI,4500,18,4482
TXN007,2026-10-18,Retail,UPI,7500,30,7470
TXN008,2026-10-18,Pharmacy,UPI,2200,8.80,2191.20
TXN009,2026-10-19,Grocery,UPI,1200,0,1200
TXN010,2026-10-19,Electronics,UPI,6000,24,5976
TXN011,2026-10-20,Retail,UPI,3500,20,3480
TXN012,2026-10-20,Pharmacy,UPI,2700,10.80,2689.20
TXN013,2026-10-21,Electronics,UPI,8000,32,7968
TXN014,2026-10-21,Grocery,UPI,2100,8.40,2091.60
TXN015,2026-10-22,Retail,UPI,5500,22,5478
TXN016,2026-10-22,Pharmacy,UPI,1600,0,1600
TXN017,2026-10-23,Electronics,UPI,4000,16,3984
TXN018,2026-10-23,Grocery,UPI,2800,15,2785
TXN019,2026-10-24,Retail,UPI,9000,36,8964
TXN020,2026-10-24,Pharmacy,UPI,3200,5,3195
TXN021,2026-10-25,Others,UPI,4200,16.80,4183.20
TXN022,2026-10-25,Others,UPI,1750,0,1750
TXN023,2026-10-26,Others,UPI,6800,35,6765
TXN024,2026-10-26,Others,UPI,3200,12.80,3187.20
TXN025,2026-10-27,Others,UPI,9500,50,9450
"""
        )
    )


# =========================================================
# AUDIT ENGINE (rules unchanged)
# =========================================================
def audit(df, threshold, rate, cap):
    x = df.copy()
    for c in ["Amount", "Actual_Deduction", "Net_Settlement"]:
        x[c] = pd.to_numeric(x[c], errors="coerce")
    x["Date"] = pd.to_datetime(x["Date"], errors="coerce")

    def fee(v):
        if pd.isna(v) or v <= threshold:
            return 0.0
        f = v * rate
        if cap and cap > 0:
            return round(min(f, cap), 2)
        return round(f, 2)

    x["Expected_Deduction"] = x["Amount"].apply(fee)
    x["Difference"] = (x["Actual_Deduction"] - x["Expected_Deduction"]).round(2)
    x["Expected_Settlement"] = (x["Amount"] - x["Expected_Deduction"]).round(2)

    def status(r):
        if pd.isna(r["Amount"]) or pd.isna(r["Actual_Deduction"]):
            return "Data Issue"
        if abs(r["Difference"]) < 0.01:
            return "Correct"
        return "Over-Deduction" if r["Difference"] > 0 else "Under-Deduction"

    x["Status"] = x.apply(status, axis=1)
    return x


# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown("### ⚙️ Audit rules")
    threshold = st.number_input("Threshold amount (₹)", min_value=0.0, value=2000.0, step=100.0,
                                help="Transactions at or below this amount carry no MDR.")
    rate_pct = st.number_input("MDR rate (%)", min_value=0.0, max_value=100.0, value=0.40,
                               step=0.05, format="%.2f")
    cap_enabled = st.checkbox("Enable deduction cap")
    cap = (
        st.number_input("Maximum deduction (₹)", min_value=0.0, value=50.0, step=5.0)
        if cap_enabled else None
    )
    st.caption("Rules are deterministic. Change them here and every number on the page recalculates.")
    st.divider()
    uploaded = st.file_uploader("📂 Upload transaction CSV", type=["csv"])
    if not uploaded:
        st.caption("Showing demo data. Upload a CSV to audit your own settlements.")

# =========================================================
# DATA
# =========================================================
data = pd.read_csv(uploaded) if uploaded else demo_data()
required = {"Transaction_ID", "Date", "Category", "Payment_Type", "Amount",
            "Actual_Deduction", "Net_Settlement"}
missing = required - set(data.columns)
if missing:
    st.error("Your file is missing these columns: " + ", ".join(sorted(missing))
             + ". Add them and upload again.")
    st.stop()

result = audit(data, threshold, rate_pct / 100, cap)
categories = sorted(result["Category"].dropna().astype(str).unique())

# Category selection lives in session state so cards and radio stay in sync
if "selected" not in st.session_state or st.session_state.selected not in ["All Categories"] + categories:
    st.session_state.selected = "All Categories"

# Overall numbers for the hero (always full dataset)
all_over = result.loc[result.Status == "Over-Deduction", "Difference"].sum()
all_over_n = int((result.Status == "Over-Deduction").sum())
all_rate = (result.Status == "Correct").mean() * 100 if len(result) else 0

hero_cls = "bad" if all_over > 0 else "good"
hero_lbl = "Excess deducted from your settlements" if all_over > 0 else "Settlements fully reconciled"
hero_big = inr(all_over) if all_over > 0 else "₹0.00"
hero_sub = (f"Across {all_over_n} of {len(result)} transactions" if all_over > 0
            else f"All {len(result)} transactions match your rule")

st.markdown(
    f"""
<div class="hero">
  <div>
    <h1>💳 Merchant MDR Copilot</h1>
    <p>Check every settlement against your MDR rule, see exactly where money was over-deducted,
    and generate a claim you can send to your payment provider.</p>
  </div>
  <div class="hero-right {hero_cls}">
    <div class="lbl">{hero_lbl}</div>
    <div class="big">{hero_big}</div>
    <div class="sub">{hero_sub} · {all_rate:.0f}% match rate</div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

# =========================================================
# CATEGORY SELECTOR
# =========================================================
st.markdown('<div class="section-title">🏪 Categories</div>', unsafe_allow_html=True)
icons = {"Grocery": "🛒", "Electronics": "💻", "Pharmacy": "💊", "Retail": "🛍️", "Others": "📦"}

selected = st.radio("Category", ["All Categories"] + categories, horizontal=True,
                    key="selected", label_visibility="collapsed")

cols = st.columns(len(categories))
for col, cat in zip(cols, categories):
    q = result[result["Category"].astype(str) == cat]
    ex = q.loc[q.Status == "Over-Deduction", "Difference"].sum()
    ok_pct = (q.Status == "Correct").mean() * 100 if len(q) else 0
    flag = (f'<div class="flag bad">⚠ Excess {inr(ex)}</div>' if ex > 0
            else '<div class="flag good">✓ No excess</div>')
    active = " active" if cat == selected else ""
    col.markdown(
        f"""<div class="cat{active}">
        <div class="name">{icons.get(cat, '📦')} {cat}</div>
        <div class="meta">{len(q)} transactions · {inr(q.Amount.sum(), 0)}</div>
        <div class="bar"><span style="width:{ok_pct:.0f}%"></span></div>
        {flag}</div>""",
        unsafe_allow_html=True,
    )

view = result if selected == "All Categories" else result[result["Category"].astype(str) == selected]

correct = view[view.Status == "Correct"]
over = view[view.Status == "Over-Deduction"]
under = view[view.Status == "Under-Deduction"]
issues = view[view.Status == "Data Issue"]
n = len(view)

total_amount = view["Amount"].sum()
expected_mdr = view["Expected_Deduction"].sum()
actual_ded = view["Actual_Deduction"].sum()
excess = over["Difference"].sum()
match_rate = len(correct) / n * 100 if n else 0

# =========================================================
# TABS
# =========================================================
st.markdown(
    f'<div class="section-title">📊 {"Overall" if selected == "All Categories" else selected} dashboard</div>',
    unsafe_allow_html=True,
)
tab_over, tab_explore, tab_explain, tab_action = st.tabs(
    ["Overview", "Transactions", "Explain a transaction", "Recover & export"]
)

# ---------- OVERVIEW ----------
with tab_over:
    k = st.columns(5)
    k[0].markdown(kpi("Transaction volume", inr(total_amount), f"{n} transactions"), unsafe_allow_html=True)
    k[1].markdown(kpi("Expected MDR", inr(expected_mdr), "Per your rule"), unsafe_allow_html=True)
    k[2].markdown(kpi("Actual deductions", inr(actual_ded), "From settlements", "#2563eb"), unsafe_allow_html=True)
    k[3].markdown(kpi("Potential excess", inr(excess), f"{len(over)} over-deducted",
                      C_OVER if excess > 0 else C_OK), unsafe_allow_html=True)
    k[4].markdown(kpi("Match rate", f"{match_rate:.1f}%", f"{len(correct)} correct", C_OK), unsafe_allow_html=True)

    st.write("")
    c1, c2 = st.columns([1, 1.4])

    with c1:
        counts = [len(correct), len(over), len(under), len(issues)]
        labels = list(STATUS_COLOR.keys())
        fig = go.Figure(go.Pie(
            labels=labels, values=counts, hole=0.64, sort=False,
            marker=dict(colors=list(STATUS_COLOR.values()), line=dict(color="#fff", width=2)),
            textinfo="value", hovertemplate="%{label}: %{value} (%{percent})<extra></extra>",
        ))
        fig.add_annotation(text=f"<b>{match_rate:.0f}%</b><br>correct", showarrow=False,
                           font=dict(size=20, color=INK))
        fig.update_layout(title="Transaction status")
        st.plotly_chart(style_fig(fig, 320), use_container_width=True, config={"displayModeBar": False})

    with c2:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=[0, view["Amount"].max() if n else 1],
            y=[0, (view["Amount"].max() if n else 1) * rate_pct / 100],
            mode="lines", name="Rule (uncapped)", line=dict(color="#94a3b8", dash="dot"),
        ))
        for s, color in STATUS_COLOR.items():
            d = view[view.Status == s]
            if len(d):
                fig.add_trace(go.Scatter(
                    x=d["Amount"], y=d["Actual_Deduction"], mode="markers", name=s,
                    marker=dict(color=color, size=11, line=dict(color="#fff", width=1.5)),
                    customdata=d[["Transaction_ID", "Expected_Deduction", "Difference"]],
                    hovertemplate="<b>%{customdata[0]}</b><br>Amount ₹%{x:,.2f}<br>Actual ₹%{y:,.2f}"
                                  "<br>Expected ₹%{customdata[1]:,.2f}<br>Diff ₹%{customdata[2]:,.2f}<extra></extra>",
                ))
        fig.update_layout(title="Actual deduction vs amount (dots above the line paid too much)",
                          xaxis_title="Transaction amount (₹)", yaxis_title="Deduction (₹)")
        st.plotly_chart(style_fig(fig, 320), use_container_width=True, config={"displayModeBar": False})

    c3, c4 = st.columns(2)
    with c3:
        by_cat = (result.groupby(result["Category"].astype(str))
                  .apply(lambda g: g.loc[g.Status == "Over-Deduction", "Difference"].sum(),
                         include_groups=False)
                  .reset_index(name="Excess"))
        fig = go.Figure(go.Bar(
            x=by_cat["Category"], y=by_cat["Excess"],
            marker_color=[C_OVER if v > 0 else C_OK for v in by_cat["Excess"]],
            text=[inr(v) for v in by_cat["Excess"]], textposition="outside",
            hovertemplate="%{x}: ₹%{y:,.2f}<extra></extra>",
        ))
        fig.update_layout(title="Excess deducted by category", yaxis_title="₹")
        st.plotly_chart(style_fig(fig, 300), use_container_width=True, config={"displayModeBar": False})

    with c4:
        t = view.dropna(subset=["Date"]).sort_values("Date")
        t = t.assign(Excess=t["Difference"].where(t.Status == "Over-Deduction", 0))
        daily = t.groupby("Date")["Excess"].sum().cumsum().reset_index()
        fig = go.Figure(go.Scatter(
            x=daily["Date"], y=daily["Excess"], mode="lines+markers", fill="tozeroy",
            line=dict(color=C_OVER, width=3), fillcolor="rgba(217,55,43,.10)",
            hovertemplate="%{x|%d %b}: ₹%{y:,.2f}<extra></extra>",
        ))
        fig.update_layout(title="Cumulative excess over time", yaxis_title="₹")
        st.plotly_chart(style_fig(fig, 300), use_container_width=True, config={"displayModeBar": False})

# ---------- TRANSACTIONS ----------
with tab_explore:
    f1, f2, f3 = st.columns([1.2, 1.2, 1])
    status_filter = f1.multiselect("Status", list(STATUS_COLOR.keys()), default=list(STATUS_COLOR.keys()))
    search = f2.text_input("Search transaction ID", placeholder="e.g. TXN013")
    sort_by = f3.selectbox("Sort by", ["Date", "Amount", "Difference"], index=2)

    flt = view[view.Status.isin(status_filter)]
    if search:
        flt = flt[flt.Transaction_ID.astype(str).str.contains(search, case=False, na=False)]
    flt = flt.sort_values(sort_by, ascending=(sort_by == "Date"))

    show = flt.assign(Status=flt.Status.map(lambda s: f"{STATUS_EMOJI[s]} {s}"))[
        ["Transaction_ID", "Date", "Category", "Payment_Type", "Amount", "Actual_Deduction",
         "Expected_Deduction", "Difference", "Net_Settlement", "Status"]
    ]
    st.caption(f"{len(show)} of {n} transactions")
    st.dataframe(
        show, use_container_width=True, hide_index=True, height=440,
        column_config={
            "Date": st.column_config.DateColumn("Date", format="DD MMM YYYY"),
            "Amount": st.column_config.NumberColumn("Amount", format="₹%.2f"),
            "Actual_Deduction": st.column_config.NumberColumn("Actual", format="₹%.2f"),
            "Expected_Deduction": st.column_config.NumberColumn("Expected", format="₹%.2f"),
            "Difference": st.column_config.NumberColumn("Difference", format="₹%.2f"),
            "Net_Settlement": st.column_config.NumberColumn("Net settlement", format="₹%.2f"),
        },
    )

# ---------- EXPLAINER ----------
with tab_explain:
    if n == 0:
        st.info("No transactions in this category yet.")
    else:
        default_ix = 0
        if len(over):
            default_ix = list(view.Transaction_ID.astype(str)).index(str(over.sort_values("Difference", ascending=False).iloc[0].Transaction_ID))
        tid = st.selectbox("Pick a transaction (largest over-deduction is preselected)",
                           view.Transaction_ID.astype(str), index=default_ix)
        row = view[view.Transaction_ID.astype(str) == tid].iloc[0]

        if row.Status == "Correct":
            st.success("Exact match. The deduction follows your MDR rule.")
        elif row.Status == "Over-Deduction":
            st.error(f"Over-deducted by {inr(abs(row.Difference))}.")
        elif row.Status == "Under-Deduction":
            st.warning(f"Under-deducted by {inr(abs(row.Difference))}.")
        else:
            st.warning("This row has a missing or invalid Amount or Actual Deduction.")

        if pd.notna(row.Amount):
            if row.Amount <= threshold:
                calc = f"{inr(row.Amount)} is at or below {inr(threshold)}, so no MDR applies."
                raw_fee = 0.0
            else:
                raw_fee = row.Amount * rate_pct / 100
                calc = f"{inr(row.Amount)} × {rate_pct:.2f}% = {inr(raw_fee)}"
                if cap and raw_fee > cap:
                    calc += f", capped at {inr(cap)}"
        else:
            calc, raw_fee = "Amount is missing.", 0.0

        s = st.columns(4)
        steps = [
            ("1. Amount", inr(row.Amount) if pd.notna(row.Amount) else "—", "What the customer paid"),
            ("2. Expected fee", inr(row.Expected_Deduction), calc),
            ("3. Actual fee", inr(row.Actual_Deduction) if pd.notna(row.Actual_Deduction) else "—",
             "What the provider took"),
            ("4. Difference", inr(row.Difference) if pd.notna(row.Difference) else "—",
             f"Expected settlement {inr(row.Expected_Settlement)}" if pd.notna(row.Expected_Settlement) else ""),
        ]
        for col, (t, v, d) in zip(s, steps):
            col.markdown(f'<div class="step"><div class="t">{t}</div><div class="v">{v}</div>'
                         f'<div class="d">{d}</div></div>', unsafe_allow_html=True)

        if pd.notna(row.Amount) and pd.notna(row.Actual_Deduction):
            fig = go.Figure(go.Bar(
                x=["Expected fee", "Actual fee"], y=[row.Expected_Deduction, row.Actual_Deduction],
                marker_color=[C_OK, C_OVER if row.Difference > 0 else C_UNDER if row.Difference < 0 else C_OK],
                text=[inr(row.Expected_Deduction), inr(row.Actual_Deduction)], textposition="outside",
            ))
            fig.update_layout(showlegend=False, yaxis_title="₹")
            st.plotly_chart(style_fig(fig, 260), use_container_width=True, config={"displayModeBar": False})

# ---------- ACTION ----------
with tab_action:
    if n == 0:
        st.info("No transactions in this category yet.")
    else:
        if excess > 0:
            cls, head = "danger", "🔴 Action recommended"
            body = (f"{len(over)} transaction(s) were charged <b>{inr(excess)}</b> more than your rule allows. "
                    "Ask your provider for an adjustment or credit, and check the amount against their "
                    "official settlement report first.")
        elif len(under):
            cls, head = "warn", "🟠 Review recommended"
            body = (f"{len(under)} transaction(s) were charged <b>{inr(abs(under['Difference'].sum()))}</b> "
                    "less than expected. This can come from a different commercial agreement, so check your "
                    "provider statement before adjusting anything.")
        elif len(issues):
            cls, head = "warn", "⚠️ Fix data first"
            body = (f"{len(issues)} transaction(s) have a missing or invalid Amount or Actual Deduction. "
                    "Complete them before treating this category as reconciled.")
        else:
            cls, head = "ok", "🟢 Fully reconciled"
            body = (f"All {n} transaction(s) match your rule. Expected {inr(expected_mdr)}, "
                    f"actual {inr(actual_ded)}. No adjustment needed.")
        st.markdown(f'<div class="rec {cls}"><b>{head}</b><br>{body}</div>', unsafe_allow_html=True)

        st.write("")
        s1, s2, s3 = st.columns(3)
        s1.markdown(kpi("Expected settlement", inr(view.Expected_Settlement.sum()), "If the rule was applied"),
                    unsafe_allow_html=True)
        s2.markdown(kpi("Actual settlement", inr(view.Net_Settlement.sum()), "What you received", "#2563eb"),
                    unsafe_allow_html=True)
        s3.markdown(kpi("Net variance", inr(actual_ded - expected_mdr), "Actual minus expected fees",
                        C_OVER if actual_ded > expected_mdr else C_OK), unsafe_allow_html=True)

        if excess > 0:
            st.markdown('<div class="section-title">✉️ Claim draft</div>', unsafe_allow_html=True)
            lines = "\n".join(
                f"  {r.Transaction_ID} | {r.Date:%d %b %Y} | Amount {inr(r.Amount)} | "
                f"Charged {inr(r.Actual_Deduction)} | Expected {inr(r.Expected_Deduction)} | Excess {inr(r.Difference)}"
                for r in over.sort_values("Date").itertuples() if pd.notna(r.Date)
            )
            rule_txt = (f"MDR of {rate_pct:.2f}% on transactions above {inr(threshold)}"
                        + (f", capped at {inr(cap)} per transaction" if cap else ""))
            letter = (
                "Subject: MDR over-deduction claim for reconciliation\n\n"
                "Hello,\n\n"
                f"During our settlement reconciliation we found {len(over)} transaction(s) where the MDR "
                f"deducted was higher than our agreed terms ({rule_txt}).\n\n"
                f"Total excess deducted: {inr(excess)}\n\n"
                f"Transactions:\n{lines}\n\n"
                "Please review these against your settlement report and credit the excess to our account.\n\n"
                "Thank you."
            )
            letter = st.text_area("Edit before sending", letter, height=300)
            st.download_button("⬇️ Download claim draft (.txt)", letter.encode(), "mdr_claim_draft.txt", "text/plain")

        st.markdown('<div class="section-title">📥 Export</div>', unsafe_allow_html=True)
        fname = ("merchant_mdr_audit_all.csv" if selected == "All Categories"
                 else f"merchant_mdr_audit_{selected.lower()}.csv")
        e1, e2 = st.columns(2)
        e1.download_button("⬇️ Download current view (CSV)", view.to_csv(index=False).encode(), fname, "text/csv",
                           use_container_width=True)
        e2.download_button("⬇️ Download over-deductions only (CSV)", over.to_csv(index=False).encode(),
                           "merchant_mdr_over_deductions.csv", "text/csv", use_container_width=True,
                           disabled=len(over) == 0)

st.divider()
st.caption("Merchant MDR Copilot is a prototype for explainable reconciliation. "
           "Verify your official MDR terms before relying on it for real financial decisions.")
