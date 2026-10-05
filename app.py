import streamlit as st
import pandas as pd
from io import StringIO

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Merchant MDR Copilot",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Main background */
.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(99,102,241,0.10), transparent 25%),
        radial-gradient(circle at 90% 20%, rgba(16,185,129,0.08), transparent 25%),
        #f6f8fc;
}

/* Container */
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

/* =====================================================
   HERO
   ===================================================== */

.hero {
    position: relative;
    overflow: hidden;
    padding: 32px;
    border-radius: 24px;
    color: white;
    margin-bottom: 25px;

    background:
        radial-gradient(circle at 90% 10%, rgba(129,140,248,0.35), transparent 25%),
        radial-gradient(circle at 10% 90%, rgba(16,185,129,0.25), transparent 25%),
        linear-gradient(135deg, #0f172a, #1e293b 55%, #312e81);

    box-shadow: 0 18px 45px rgba(15,23,42,0.18);
    animation: fadeUp 0.7s ease;
}

.hero:after {
    content: "";
    position: absolute;
    width: 180px;
    height: 180px;
    right: -60px;
    top: -70px;
    border-radius: 50%;
    background: rgba(255,255,255,0.06);
}

.hero h1 {
    margin: 0;
    font-size: 2.4rem;
    font-weight: 800;
    letter-spacing: -1px;
}

.hero p {
    margin: 8px 0 0;
    color: #cbd5e1;
    font-size: 1rem;
}

.hero-badge {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 999px;
    background: rgba(255,255,255,0.10);
    border: 1px solid rgba(255,255,255,0.15);
    font-size: 0.78rem;
    margin-bottom: 12px;
}

/* =====================================================
   SECTION TITLES
   ===================================================== */

.section-title {
    font-size: 1.25rem;
    font-weight: 800;
    color: #111827;
    margin-top: 28px;
    margin-bottom: 14px;
}

/* =====================================================
   CATEGORY CARDS
   ===================================================== */

.category-card {
    border: 1px solid #e5e7eb;
    border-radius: 18px;
    padding: 17px;
    background: rgba(255,255,255,0.92);
    min-height: 118px;
    transition: all 0.25s ease;
    box-shadow: 0 6px 18px rgba(15,23,42,0.05);
    animation: fadeUp 0.6s ease;
}

.category-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 14px 30px rgba(15,23,42,0.12);
    border-color: #a5b4fc;
}

.category-icon {
    font-size: 1.45rem;
}

.category-name {
    font-weight: 700;
    font-size: 0.95rem;
    color: #111827;
}

.category-count {
    font-size: 0.78rem;
    color: #64748b;
    margin-top: 4px;
}

.category-excess {
    font-size: 1rem;
    font-weight: 800;
    color: #dc2626;
    margin-top: 7px;
}

/* =====================================================
   METRICS
   ===================================================== */

div[data-testid="stMetric"] {
    background: rgba(255,255,255,0.95);
    border: 1px solid #e5e7eb;
    border-radius: 18px;
    padding: 15px 17px;
    box-shadow: 0 6px 18px rgba(15,23,42,0.05);
    transition: all 0.25s ease;
}

div[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 25px rgba(15,23,42,0.10);
}

/* =====================================================
   SUMMARY / RECOMMENDATION
   ===================================================== */

.summary-card {
    border-radius: 22px;
    padding: 24px;
    margin-top: 18px;
    margin-bottom: 20px;
    border: 1px solid #e2e8f0;
    background: linear-gradient(135deg, #ffffff, #f8fafc);
    box-shadow: 0 10px 28px rgba(15,23,42,0.07);
    animation: fadeUp 0.7s ease;
}

.summary-title {
    font-size: 1.15rem;
    font-weight: 800;
    color: #111827;
}

.summary-text {
    color: #475569;
    line-height: 1.7;
    margin-top: 8px;
}

.recommendation {
    margin-top: 15px;
    padding: 16px;
    border-radius: 15px;
    background: #eef2ff;
    border-left: 5px solid #6366f1;
    color: #312e81;
}

.recommendation-danger {
    background: #fef2f2;
    border-left-color: #ef4444;
    color: #991b1b;
}

.recommendation-success {
    background: #ecfdf5;
    border-left-color: #10b981;
    color: #065f46;
}

.recommendation-warning {
    background: #fffbeb;
    border-left-color: #f59e0b;
    color: #92400e;
}

/* =====================================================
   STATUS PILLS
   ===================================================== */

.status-pill {
    display: inline-block;
    padding: 5px 10px;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 700;
}

/* =====================================================
   SIDEBAR
   ===================================================== */

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #f8fafc, #eef2ff);
    border-right: 1px solid #e2e8f0;
}

/* =====================================================
   BUTTONS
   ===================================================== */

.stButton > button {
    border-radius: 12px;
    border: 1px solid #e2e8f0;
    font-weight: 600;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    border-color: #818cf8;
    box-shadow: 0 8px 20px rgba(99,102,241,0.15);
}

/* =====================================================
   ANIMATIONS
   ===================================================== */

@keyframes fadeUp {
    from {
        opacity: 0;
        transform: translateY(12px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.03); }
    100% { transform: scale(1); }
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# DEMO DATA
# =========================================================

def demo_data():

    return pd.read_csv(StringIO("""
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
"""))


# =========================================================
# AUDIT ENGINE
# =========================================================

def audit(df, threshold, rate, cap):

    x = df.copy()

    for c in ["Amount", "Actual_Deduction", "Net_Settlement"]:
        x[c] = pd.to_numeric(x[c], errors="coerce")

    def fee(v):

        if pd.isna(v) or v <= threshold:
            return 0.0

        f = v * rate

        if cap and cap > 0:
            return round(min(f, cap), 2)

        return round(f, 2)

    x["Expected_Deduction"] = x["Amount"].apply(fee)

    x["Difference"] = (
        x["Actual_Deduction"] -
        x["Expected_Deduction"]
    ).round(2)

    x["Expected_Settlement"] = (
        x["Amount"] -
        x["Expected_Deduction"]
    ).round(2)

    def status(r):

        if pd.isna(r["Amount"]) or pd.isna(r["Actual_Deduction"]):
            return "Data Issue"

        if abs(r["Difference"]) < 0.01:
            return "Correct"

        if r["Difference"] > 0:
            return "Over-Deduction"

        return "Under-Deduction"

    x["Status"] = x.apply(status, axis=1)

    return x


# =========================================================
# HERO
# =========================================================

st.markdown("""
<div class="hero">

    <div class="hero-badge">FINTECH • DATA ANALYTICS • RECONCILIATION</div>

    <h1>💳 Merchant MDR Copilot</h1>

    <p>
        Explainable settlement intelligence for merchants —
        detect deduction mismatches, quantify losses and reconcile payments.
    </p>

</div>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## ⚙️ Audit Configuration")

    threshold = st.number_input(
        "Threshold amount (₹)",
        min_value=0.0,
        value=2000.0,
        step=100.0
    )

    rate_pct = st.number_input(
        "MDR rate (%)",
        min_value=0.0,
        max_value=100.0,
        value=0.40,
        step=0.05,
        format="%.2f"
    )

    cap_enabled = st.checkbox(
        "Enable deduction cap"
    )

    cap = (
        st.number_input(
            "Maximum deduction (₹)",
            min_value=0.0,
            value=50.0,
            step=5.0
        )
        if cap_enabled
        else None
    )

    st.info(
        "🔐 Financial rules are deterministic. "
        "The dashboard explains the configured rule "
        "instead of changing it automatically."
    )

    st.divider()

    uploaded = st.file_uploader(
        "📂 Upload transaction CSV",
        type=["csv"]
    )


# =========================================================
# DATA
# =========================================================

data = pd.read_csv(uploaded) if uploaded else demo_data()

required = {
    "Transaction_ID",
    "Date",
    "Category",
    "Payment_Type",
    "Amount",
    "Actual_Deduction",
    "Net_Settlement"
}

missing = required - set(data.columns)

if missing:

    st.error(
        "Missing required columns: "
        + ", ".join(sorted(missing))
    )

    st.stop()


result = audit(
    data,
    threshold,
    rate_pct / 100,
    cap
)

categories = sorted(
    result["Category"]
    .dropna()
    .astype(str)
    .unique()
)


# =========================================================
# CATEGORY ACCESS
# =========================================================

st.markdown(
    '<div class="section-title">🏪 Category Access</div>',
    unsafe_allow_html=True
)

st.caption(
    "Select a merchant category to instantly focus the audit."
)

selected = st.radio(
    "Choose category",
    ["All Categories"] + list(categories),
    horizontal=True,
    label_visibility="collapsed"
)

view = (
    result
    if selected == "All Categories"
    else result[
        result["Category"].astype(str) == selected
    ]
)


# =========================================================
# CATEGORY CARDS
# =========================================================

st.markdown(
    '<div class="section-title">📌 Category Snapshot</div>',
    unsafe_allow_html=True
)

icons = {
    "Grocery": "🛒",
    "Electronics": "💻",
    "Pharmacy": "💊",
    "Retail": "🛍️",
    "Others": "📦"
}

card_cols = st.columns(len(categories))

for col, cat in zip(card_cols, categories):

    q = result[
        result["Category"].astype(str) == cat
    ]

    excess = q.loc[
        q.Status == "Over-Deduction",
        "Difference"
    ].sum()

    transaction_amount = q["Amount"].sum()

    icon = icons.get(cat, "📦")

    with col:

        excess_class = (
            "category-excess"
            if excess > 0
            else ""
        )

        st.markdown(
            f"""
            <div class="category-card">

                <div class="category-icon">
                    {icon}
                </div>

                <div class="category-name">
                    {cat}
                </div>

                <div class="category-count">
                    {len(q)} transactions
                    • ₹{transaction_amount:,.0f} volume
                </div>

                <div class="{excess_class}">
                    {'⚠️ ' if excess > 0 else '✓ '}
                    Excess ₹{excess:,.2f}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# DASHBOARD HEADER
# =========================================================

dashboard_title = (
    "Overall Dashboard"
    if selected == "All Categories"
    else f"{selected} Dashboard"
)

st.markdown(
    f'<div class="section-title">📊 {dashboard_title}</div>',
    unsafe_allow_html=True
)


# =========================================================
# MAIN METRICS
# =========================================================

correct = view[view.Status == "Correct"]
over = view[view.Status == "Over-Deduction"]
under = view[view.Status == "Under-Deduction"]
issues = view[view.Status == "Data Issue"]

total_amount = view["Amount"].sum()

expected_mdr = view["Expected_Deduction"].sum()

actual_deductions = view["Actual_Deduction"].sum()

potential_excess = over["Difference"].sum()

a, b, c, d, e = st.columns(5)

a.metric(
    "💰 Transaction Volume",
    f"₹{total_amount:,.2f}"
)

b.metric(
    "🎯 Expected MDR",
    f"₹{expected_mdr:,.2f}"
)

c.metric(
    "💸 Actual Deductions",
    f"₹{actual_deductions:,.2f}"
)

d.metric(
    "⚠️ Potential Excess",
    f"₹{potential_excess:,.2f}"
)

e.metric(
    "✅ Correct",
    len(correct)
)


# =========================================================
# DISCREPANCY BREAKDOWN
# =========================================================

st.markdown(
    '<div class="section-title">🔎 Discrepancy Breakdown</div>',
    unsafe_allow_html=True
)

a, b, c, d = st.columns(4)

a.metric(
    "🟢 Correct",
    len(correct)
)

b.metric(
    "🔴 Over-Deduction",
    len(over)
)

c.metric(
    "🟠 Under-Deduction",
    len(under)
)

d.metric(
    "⚠️ Data Issues",
    len(issues)
)

chart = pd.DataFrame(
    {
        "Transactions": [
            len(correct),
            len(over),
            len(under),
            len(issues)
        ]
    },
    index=[
        "Correct",
        "Over-Deduction",
        "Under-Deduction",
        "Data Issue"
    ]
)

st.bar_chart(chart)


# =========================================================
# STATUS FILTER
# =========================================================

st.markdown(
    '<div class="section-title">🎯 Transaction Explorer</div>',
    unsafe_allow_html=True
)

status = st.selectbox(
    "Filter transactions",
    [
        "All",
        "Correct",
        "Over-Deduction",
        "Under-Deduction",
        "Data Issue"
    ]
)

filtered = (
    view
    if status == "All"
    else view[view.Status == status]
)

cols = [
    "Transaction_ID",
    "Date",
    "Category",
    "Payment_Type",
    "Amount",
    "Actual_Deduction",
    "Expected_Deduction",
    "Difference",
    "Net_Settlement",
    "Status"
]

st.dataframe(
    filtered[cols],
    use_container_width=True,
    hide_index=True
)


# =========================================================
# TRANSACTION EXPLAINER
# =========================================================

st.markdown(
    '<div class="section-title">🧾 Transaction Explainer</div>',
    unsafe_allow_html=True
)

if len(view):

    tid = st.selectbox(
        "Select transaction",
        view.Transaction_ID.astype(str)
    )

    row = view[
        view.Transaction_ID.astype(str) == tid
    ].iloc[0]

    a, b, c, d = st.columns(4)

    a.metric(
        "Transaction Amount",
        f"₹{row.Amount:,.2f}"
    )

    b.metric(
        "Expected Deduction",
        f"₹{row.Expected_Deduction:,.2f}"
    )

    c.metric(
        "Actual Deduction",
        f"₹{row.Actual_Deduction:,.2f}"
    )

    d.metric(
        "Difference",
        f"₹{row.Difference:,.2f}"
    )

    if row.Status == "Correct":

        st.success(
            "🟢 Exact match — actual deduction matches "
            "the configured MDR rule."
        )

    elif row.Status == "Over-Deduction":

        st.error(
            f"🔴 Over-deduction detected: "
            f"₹{abs(row.Difference):,.2f} "
            f"more than expected."
        )

    elif row.Status == "Under-Deduction":

        st.warning(
            f"🟠 Under-deduction detected: "
            f"₹{abs(row.Difference):,.2f} "
            f"less than expected."
        )

    else:

        st.warning(
            "⚠️ Check transaction data."
        )

    if row.Amount <= threshold:

        st.write(
            f"₹{row.Amount:,.2f} is at/below the "
            f"₹{threshold:,.2f} threshold → "
            f"expected MDR = ₹0.00"
        )

    else:

        raw_fee = row.Amount * rate_pct / 100

        st.write(
            f"₹{row.Amount:,.2f} × "
            f"{rate_pct:.2f}% = "
            f"₹{raw_fee:,.2f}"
        )

        if cap and raw_fee > cap:

            st.info(
                f"Deduction cap applied: "
                f"₹{cap:,.2f}"
            )

    st.write(
        f"Expected settlement = "
        f"₹{row.Expected_Settlement:,.2f}"
    )


# =========================================================
# SMART CATEGORY SUMMARY
# =========================================================

st.markdown(
    '<div class="section-title">🧠 Reconciliation Summary & Recommendation</div>',
    unsafe_allow_html=True
)

transaction_count = len(view)

expected_settlement = view["Expected_Settlement"].sum()

actual_settlement = view["Net_Settlement"].sum()

total_difference = (
    view["Actual_Deduction"].sum()
    - view["Expected_Deduction"].sum()
)

match_rate = (
    (len(correct) / transaction_count) * 100
    if transaction_count > 0
    else 0
)

if transaction_count == 0:

    st.info(
        "No transactions available for this category."
    )

else:

    if potential_excess > 0:

        summary_class = "recommendation-danger"

        recommendation = f"""
        <div class="recommendation {summary_class}">

        <b>🔴 Action Recommended — Reconciliation Required</b>

        <br><br>

        The selected category has
        <b>₹{potential_excess:,.2f}</b> in potential
        excess deductions across
        <b>{len(over)}</b> transaction(s).

        <br><br>

        To reconcile the account, compare the actual
        deduction against the configured MDR rule and
        request an adjustment/credit of approximately
        <b>₹{potential_excess:,.2f}</b>, subject to
        verification against the payment provider's
        settlement report.

        </div>
        """

    elif len(under) > 0:

        summary_class = "recommendation-warning"

        recommendation = f"""
        <div class="recommendation {summary_class}">

        <b>🟠 Review Recommended</b>

        <br><br>

        The category contains
        <b>{len(under)}</b> under-deducted transaction(s).

        The total deduction is below the configured
        MDR expectation by
        <b>₹{abs(under['Difference'].sum()):,.2f}</b>.

        <br><br>

        Review the provider settlement statement before
        making any adjustment, because an apparent
        under-deduction may result from a different
        commercial agreement or fee rule.

        </div>
        """

    elif len(issues) > 0:

        summary_class = "recommendation-warning"

        recommendation = f"""
        <div class="recommendation {summary_class}">

        <b>⚠️ Data Quality Check Required</b>

        <br><br>

        <b>{len(issues)}</b> transaction(s) contain
        incomplete or invalid financial data.

        <br><br>

        Complete the missing Amount or Actual Deduction
        values before treating the category as fully
        reconciled.

        </div>
        """

    else:

        summary_class = "recommendation-success"

        recommendation = f"""
        <div class="recommendation {summary_class}">

        <b>🟢 Fully Reconciled</b>

        <br><br>

        Excellent — all
        <b>{transaction_count}</b> transaction(s)
        match the configured MDR rule.

        <br><br>

        Expected deductions:
        <b>₹{expected_mdr:,.2f}</b>

        <br>

        Actual deductions:
        <b>₹{actual_deductions:,.2f}</b>

        <br><br>

        No reconciliation adjustment is currently
        indicated by this audit.

        </div>
        """

    st.markdown(
        f"""
        <div class="summary-card">

            <div class="summary-title">
                📌 {selected} — Financial Reconciliation Summary
            </div>

            <div class="summary-text">

                <b>Transaction volume:</b>
                ₹{total_amount:,.2f}

                <br>

                <b>Expected settlement:</b>
                ₹{expected_settlement:,.2f}

                <br>

                <b>Actual settlement:</b>
                ₹{actual_settlement:,.2f}

                <br>

                <b>Reconciliation accuracy:</b>
                {match_rate:.1f}%

                <br>

                <b>Total deduction variance:</b>
                ₹{abs(total_difference):,.2f}

            </div>

            {recommendation}

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# EXPORT
# =========================================================

st.markdown(
    '<div class="section-title">📥 Export Audit</div>',
    unsafe_allow_html=True
)

filename = (
    "merchant_mdr_audit_all.csv"
    if selected == "All Categories"
    else f"merchant_mdr_audit_{selected.lower()}.csv"
)

st.download_button(
    "⬇️ Download Current View as CSV",
    view.to_csv(index=False).encode(),
    filename,
    "text/csv"
)


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "💳 Merchant MDR Copilot • Prototype for explainable "
    "fintech reconciliation • Verify applicable official "
    "MDR rules before real financial use."
)
