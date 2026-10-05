# Enhanced Merchant MDR Copilot

Features:
- Category access for Grocery, Retail, Pharmacy, Electronics, etc.
- Category-specific dashboards
- Category summary cards
- Status filtering
- Improved UI
- CSV upload
- Manual threshold/rate/cap
- Transaction explainer
- CSV export

Run:
python -m pip install -r requirements.txt
streamlit run app.py

END-TO-END FLOW

Settlement CSV
      ↓
Data Pipeline & Validation
      ↓
Deterministic MDR Rule Engine
      ↓
Streamlit Dashboard
      ↓
Insights + Accounting-Ready Reporting
      ↓
Historical Storage / Trend Monitoring
