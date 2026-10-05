import streamlit as st
import pandas as pd
from io import StringIO

st.set_page_config(page_title="Merchant MDR Copilot", page_icon="💳", layout="wide")

st.markdown("""
<style>
.block-container{padding-top:1.5rem;max-width:1400px}
.hero{padding:24px;border-radius:18px;background:linear-gradient(135deg,#111827,#374151);color:white;margin-bottom:22px}
.hero h1{margin:0;font-size:2.2rem}.hero p{margin:5px 0 0;color:#d1d5db}
div[data-testid="stMetric"]{border:1px solid #e5e7eb;border-radius:14px;padding:10px;background:#fafafa}
.category-card{border:1px solid #e5e7eb;border-radius:14px;padding:14px;background:white}
</style>
""", unsafe_allow_html=True)

def demo_data():
    return pd.read_csv(StringIO("""Transaction_ID,Date,Category,Payment_Type,Amount,Actual_Deduction,Net_Settlement
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
TXN020,2026-10-24,Pharmacy,UPI,3200,5,3195"""))

def audit(df, threshold, rate, cap):
    x=df.copy()
    for c in ["Amount","Actual_Deduction","Net_Settlement"]:
        x[c]=pd.to_numeric(x[c],errors="coerce")
    def fee(v):
        if pd.isna(v) or v<=threshold:return 0.0
        f=v*rate
        return round(min(f,cap),2) if cap and cap>0 else round(f,2)
    x["Expected_Deduction"]=x["Amount"].apply(fee)
    x["Difference"]=(x["Actual_Deduction"]-x["Expected_Deduction"]).round(2)
    x["Expected_Settlement"]=(x["Amount"]-x["Expected_Deduction"]).round(2)
    def status(r):
        if pd.isna(r["Amount"]) or pd.isna(r["Actual_Deduction"]): return "Data Issue"
        if abs(r["Difference"])<0.01:return "Correct"
        return "Over-Deduction" if r["Difference"]>0 else "Under-Deduction"
    x["Status"]=x.apply(status,axis=1)
    return x

st.markdown('<div class="hero"><h1>💳 Merchant MDR Copilot</h1><p>Explainable settlement-audit dashboard for small merchants</p></div>',unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ Audit Configuration")
    threshold=st.number_input("Threshold amount (₹)",min_value=0.0,value=2000.0,step=100.0)
    rate_pct=st.number_input("MDR rate (%)",min_value=0.0,max_value=100.0,value=0.40,step=0.05,format="%.2f")
    cap_enabled=st.checkbox("Enable deduction cap")
    cap=st.number_input("Maximum deduction (₹)",min_value=0.0,value=50.0,step=5.0) if cap_enabled else None
    st.caption("Manual rules only. No AI changes financial rules.")
    st.divider()
    uploaded=st.file_uploader("Upload transaction CSV",type=["csv"])

data=pd.read_csv(uploaded) if uploaded else demo_data()
required={"Transaction_ID","Date","Category","Payment_Type","Amount","Actual_Deduction","Net_Settlement"}
missing=required-set(data.columns)
if missing:
    st.error("Missing required columns: "+", ".join(sorted(missing)))
    st.stop()

result=audit(data,threshold,rate_pct/100,cap)
categories=sorted(result["Category"].dropna().astype(str).unique())

st.subheader("🏪 Category Access")
selected=st.radio("Choose a category",["All Categories"]+list(categories),horizontal=True,label_visibility="collapsed")
view=result if selected=="All Categories" else result[result["Category"].astype(str)==selected]

# Category cards
card_cols=st.columns(len(categories))
for col,cat in zip(card_cols,categories):
    q=result[result["Category"].astype(str)==cat]
    excess=q.loc[q.Status=="Over-Deduction","Difference"].sum()
    with col:
        st.markdown(f"""<div class="category-card"><b>🏪 {cat}</b><br>
        {len(q)} transactions<br>Flagged excess: <b>₹{excess:,.2f}</b></div>""",unsafe_allow_html=True)

st.subheader("📊 "+("Overall Dashboard" if selected=="All Categories" else selected+" Dashboard"))

correct=view[view.Status=="Correct"]; over=view[view.Status=="Over-Deduction"]; under=view[view.Status=="Under-Deduction"]; issues=view[view.Status=="Data Issue"]

a,b,c,d,e=st.columns(5)
a.metric("Transactions",len(view))
b.metric("Expected MDR",f"₹{view.Expected_Deduction.sum():,.2f}")
c.metric("Actual Deductions",f"₹{view.Actual_Deduction.sum():,.2f}")
d.metric("Potential Excess",f"₹{over.Difference.sum():,.2f}")
e.metric("Correct",len(correct))

st.subheader("🔎 Discrepancy Breakdown")
a,b,c,d=st.columns(4)
a.metric("🟢 Correct",len(correct)); b.metric("🔴 Over-Deduction",len(over)); c.metric("🟠 Under-Deduction",len(under)); d.metric("⚠️ Data Issues",len(issues))
chart=pd.DataFrame({"Transactions":[len(correct),len(over),len(under),len(issues)]},index=["Correct","Over-Deduction","Under-Deduction","Data Issue"])
st.bar_chart(chart)

st.subheader("🎯 Status Filter")
status=st.selectbox("Show",["All","Correct","Over-Deduction","Under-Deduction","Data Issue"])
filtered=view if status=="All" else view[view.Status==status]

cols=["Transaction_ID","Date","Category","Payment_Type","Amount","Actual_Deduction","Expected_Deduction","Difference","Net_Settlement","Status"]
st.dataframe(filtered[cols],use_container_width=True,hide_index=True)

st.subheader("🧾 Transaction Explainer")
if len(view):
    tid=st.selectbox("Select transaction",view.Transaction_ID.astype(str))
    row=view[view.Transaction_ID.astype(str)==tid].iloc[0]
    a,b,c,d=st.columns(4)
    a.metric("Amount",f"₹{row.Amount:,.2f}"); b.metric("Expected",f"₹{row.Expected_Deduction:,.2f}"); c.metric("Actual",f"₹{row.Actual_Deduction:,.2f}"); d.metric("Difference",f"₹{row.Difference:,.2f}")
    if row.Status=="Correct": st.success("🟢 Actual deduction matches the configured rule.")
    elif row.Status=="Over-Deduction": st.error(f"🔴 ₹{abs(row.Difference):,.2f} more was deducted than expected.")
    elif row.Status=="Under-Deduction": st.warning(f"🟠 ₹{abs(row.Difference):,.2f} less was deducted than expected.")
    else: st.warning("⚠️ Check transaction data.")
    if row.Amount<=threshold:
        st.write(f"₹{row.Amount:,.2f} is at/below the ₹{threshold:,.2f} threshold → expected MDR = ₹0.00")
    else:
        st.write(f"₹{row.Amount:,.2f} × {rate_pct:.2f}% = ₹{row.Amount*rate_pct/100:,.2f}")
    st.write(f"Expected settlement = ₹{row.Expected_Settlement:,.2f}")

st.subheader("📥 Export")
filename="merchant_mdr_audit_all.csv" if selected=="All Categories" else f"merchant_mdr_audit_{selected.lower()}.csv"
st.download_button("Download Current View as CSV",view.to_csv(index=False).encode(),filename,"text/csv")

st.divider()
st.caption("Prototype only. Verify applicable official MDR rules before real financial use.")
