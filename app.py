import streamlit as st
import pandas as pd
from data_loader import generate_mock_listings, SAMPLE_LEADS, get_lead_by_id
from rag_engine import SimpleRAGEngine

# Page Configuration
st.set_page_config(
    page_title="Sales Copilot",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom Minimal CSS
st.markdown("""
<style>
    /* Clean Minimalist Styling */
    .stApp {
        background-color: #0F172A;
        color: #F8FAFC;
    }
    .main-title {
        font-size: 28px;
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 4px;
    }
    .sub-title {
        font-size: 14px;
        color: #94A3B8;
        margin-bottom: 24px;
    }
    .clean-card {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 16px;
    }
    .prop-card {
        background: #0F172A;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 16px;
        margin-top: 10px;
    }
    .badge {
        background: #3B82F6;
        color: #FFFFFF;
        font-size: 11px;
        font-weight: 600;
        padding: 3px 8px;
        border-radius: 12px;
    }
    .badge-green {
        background: #10B981;
        color: #FFFFFF;
        font-size: 11px;
        font-weight: 600;
        padding: 3px 8px;
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

# Load Data
@st.cache_data
def load_data():
    return generate_mock_listings(n=100)

listings_df = load_data()

@st.cache_resource
def load_rag():
    return SimpleRAGEngine(listings_df, SAMPLE_LEADS)

rag_engine = load_rag()

# Header
st.markdown('<div class="main-title">⚡ Sales Copilot</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Simple RAG-powered assistant for real estate sales calls</div>', unsafe_allow_html=True)

# Simple Top Navigation Tabs
tab_copilot, tab_briefs, tab_listings = st.tabs(["💬 Live Copilot", "📋 Call Briefs", "🏡 Listings Database"])

# ==========================================
# TAB 1: LIVE COPILOT
# ==========================================
with tab_copilot:
    col_input, col_output = st.columns([1, 1.2])
    
    with col_input:
        st.markdown("##### 1. Select Active Lead")
        selected_lead_id = st.selectbox(
            "Lead Name",
            options=[l["id"] for l in SAMPLE_LEADS],
            format_func=lambda x: f"{get_lead_by_id(x)['name']} ({get_lead_by_id(x)['type']})",
            label_visibility="collapsed"
        )
        
        lead = get_lead_by_id(selected_lead_id)
        
        st.markdown(f"""
<div class="clean-card">
<h4 style="margin: 0 0 8px 0; color: #F8FAFC;">{lead['name']}</h4>
<p style="margin: 0; color: #94A3B8; font-size: 14px;">Budget: <strong>{lead['budget']}</strong> | Cap Target: <strong>{lead['target_cap_rate']}</strong></p>
<p style="margin: 4px 0 0 0; color: #94A3B8; font-size: 14px;">Zoning: <strong>{lead['preferred_zoning']}</strong></p>
</div>
""", unsafe_allow_html=True)
        
        st.markdown("##### 2. Live Conversation / Notes Input")
        user_query = st.text_input(
            "Query or Call Note",
            value=f"Looking for {lead['preferred_zoning']} with cap rate {lead['target_cap_rate']}",
            placeholder="Type buyer preferences..."
        )

    with col_output:
        st.markdown("##### 3. Copilot Insights & Matches")
        
        insights = rag_engine.get_copilot_insights(lead, user_query)
        
        # Motivations Card
        st.markdown("""
        <div class="clean-card">
            <span class="badge">Buyer Motivations</span>
            <ul style="margin-top: 10px; margin-bottom: 0; padding-left: 20px; color: #E2E8F0;">
        """ + "".join([f"<li>{m}</li>" for m in insights["buyer_motivations"]]) + """
            </ul>
        </div>
        """, unsafe_allow_html=True)

        # Property Recommendations
        st.markdown("<h6 style='margin-top: 16px; margin-bottom: 8px;'>Matching Properties</h6>", unsafe_allow_html=True)
        for prop in insights["matched_properties"]:
            st.markdown(f"""
            <div class="prop-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <strong style="color: #F8FAFC; font-size: 15px;">{prop['title']}</strong>
                    <span class="badge-green">${prop['price']:,}</span>
                </div>
                <p style="margin: 4px 0; color: #94A3B8; font-size: 13px;">{prop['address']}</p>
                <p style="margin: 0; color: #CBD5E1; font-size: 13px;">Cap Rate: <strong>{prop['cap_rate']}%</strong> | Zoning: <strong>{prop['zoning']}</strong></p>
            </div>
            """, unsafe_allow_html=True)
            
        st.info(f"💡 **Pitch Cue:** {insights['recommended_pitch']}")

# ==========================================
# TAB 2: CALL BRIEFS
# ==========================================
with tab_briefs:
    st.markdown("##### Select Scheduled Lead Brief")
    selected_brief_id = st.selectbox(
        "Scheduled Calls",
        options=[l["id"] for l in SAMPLE_LEADS],
        format_func=lambda x: f"{get_lead_by_id(x)['name']} — Scheduled at {get_lead_by_id(x)['scheduled_time']}",
        label_visibility="collapsed"
    )
    
    brief_lead = get_lead_by_id(selected_brief_id)
    
    col_b1, col_b2 = st.columns([1, 1])
    
    with col_b1:
        st.markdown(f"""
<div class="clean-card">
<span class="badge">Lead Summary</span>
<h3 style="margin-top: 10px; margin-bottom: 4px;">{brief_lead['name']}</h3>
<p style="color: #94A3B8; font-size: 14px; margin-bottom: 16px;">{brief_lead['type']} | Call: {brief_lead['scheduled_time']}</p>
<p><strong>Target Budget:</strong> {brief_lead['budget']}</p>
<p><strong>Target Cap Rate:</strong> {brief_lead['target_cap_rate']}</p>
<p><strong>Zoning Preference:</strong> {brief_lead['preferred_zoning']}</p>
<p><strong>Last Contact:</strong> {brief_lead['last_contact']}</p>
</div>
""", unsafe_allow_html=True)
        
    with col_b2:
        st.markdown("""
        <div class="clean-card">
            <span class="badge">Interaction Log History</span>
            <div style="margin-top: 12px;">
        """ + "".join([f"<p style='margin-bottom: 8px; color: #CBD5E1; font-size: 14px;'>• {log}</p>" for log in brief_lead['interaction_logs']]) + """
            </div>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# TAB 3: PROPERTY LISTINGS DATABASE
# ==========================================
with tab_listings:
    col_s1, col_s2 = st.columns([1, 2])
    with col_s1:
        search_term = st.text_input("Search Title or City", placeholder="e.g. Austin or Commercial")
    with col_s2:
        zoning_select = st.selectbox("Filter Zoning", ["All"] + list(listings_df['zoning'].unique()))

    df_view = listings_df.copy()
    if search_term:
        df_view = df_view[df_view['title'].str.contains(search_term, case=False) | df_view['address'].str.contains(search_term, case=False)]
    if zoning_select != "All":
        df_view = df_view[df_view['zoning'] == zoning_select]

    st.dataframe(
        df_view[['id', 'title', 'address', 'zoning', 'price', 'cap_rate', 'status']],
        use_container_width=True,
        height=400
    )
