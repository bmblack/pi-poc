"""
PI Planning Dashboard - Main Streamlit Application
A comprehensive dashboard for PI Planning with AI agents and JIRA integration
"""

import streamlit as st
import sys
import os
from pathlib import Path

# Add the app directory to Python path for imports
app_dir = Path(__file__).parent
sys.path.insert(0, str(app_dir))

from components.sidebar import render_sidebar
from utils.config import load_config

# Page configuration
st.set_page_config(
    page_title="PI Planning Dashboard",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """Main application entry point"""
    
    # Load configuration
    config = load_config()
    
    # Custom CSS for better styling and text contrast (dark mode compatible)
    st.markdown("""
    <style>
    /* Ensure proper text contrast for dark backgrounds */
    .stApp {
        color: #ffffff !important;
    }
    
    .main-header {
        font-size: 3rem;
        color: #4fc3f7;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .feature-card {
        background-color: rgba(255, 255, 255, 0.1);
        color: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid #4fc3f7;
        box-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .feature-card h3 {
        color: #4fc3f7;
        margin-bottom: 1rem;
    }
    
    .feature-card p, .feature-card li {
        color: #ffffff;
    }
    
    .status-badge {
        padding: 0.25rem 0.75rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    
    .status-complete { background-color: #4caf50; color: #ffffff; }
    .status-progress { background-color: #ff9800; color: #ffffff; }
    .status-pending { background-color: #757575; color: #ffffff; }
    
    /* Fix all text elements for dark mode */
    .stMarkdown, .stMarkdown p, .stMarkdown li, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #ffffff !important;
    }
    
    /* Fix info boxes for dark mode */
    .stAlert {
        background-color: rgba(33, 150, 243, 0.1) !important;
        color: #ffffff !important;
        border: 1px solid #2196f3 !important;
    }
    
    /* Fix buttons */
    .stButton > button {
        background-color: #4fc3f7;
        color: #000000;
        border: none;
    }
    
    .stButton > button:hover {
        background-color: #29b6f6;
        color: #000000;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Render sidebar
    render_sidebar()
    
    # Main content
    st.markdown('<h1 class="main-header">🎯 PI Planning Dashboard</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    Welcome to the **PI Planning Dashboard** - your one-stop solution for intelligent PI Planning with AI agents and JIRA integration.
    
    This dashboard orchestrates a team of AI agents powered by **CrewAI** to automate and enhance your PI Planning process.
    """)
    
    # Feature overview cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🤖 AI Agent Orchestration</h3>
            <p>Powered by <strong>CrewAI</strong> with specialized agents:</p>
            <ul>
                <li><strong>Goal Validator</strong> - SMART goals analysis</li>
                <li><strong>Epic Generator</strong> - Automated Epic/Feature creation</li>
                <li><strong>Story Analyzer</strong> - Backlog quality assessment</li>
                <li><strong>Dependency Agent</strong> - Cross-team dependency mapping</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3>🔌 MCP Server Integration</h3>
            <p>Model Context Protocol servers provide:</p>
            <ul>
                <li><strong>Team MCP</strong> - Team ownership & capacity rules</li>
                <li><strong>JIRA MCP</strong> - Project templates & configurations</li>
                <li><strong>Goal MCP</strong> - SMART goals validation & examples</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>📊 Complete Workflow</h3>
            <p>End-to-end PI Planning process:</p>
            <ol>
                <li>Clean JIRA project data</li>
                <li>Upload & validate PI goals</li>
                <li>Generate Epics & Features</li>
                <li>Review & push to JIRA</li>
                <li>Analyze backlog quality</li>
                <li>Check team dependencies</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3>🎯 Key Benefits</h3>
            <ul>
                <li><strong>Automated</strong> - AI agents handle complex analysis</li>
                <li><strong>Integrated</strong> - Seamless JIRA connectivity</li>
                <li><strong>Intelligent</strong> - SMART goals & quality validation</li>
                <li><strong>Collaborative</strong> - Team dependency awareness</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Getting started section
    st.markdown("---")
    st.markdown("## 🚀 Getting Started")
    
    st.info("""
    **Ready to begin your PI Planning journey?**
    
    1. **Start with Page 1** - Clean your JIRA project to prepare for new PI data
    2. **Follow the workflow** - Each page builds on the previous step
    3. **Review AI recommendations** - Agents provide intelligent suggestions throughout
    4. **Customize as needed** - All generated content can be reviewed and modified
    
    Use the sidebar navigation to move between pages. Your progress will be tracked automatically.
    """)
    
    # Quick actions
    st.markdown("### Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🗑️ Start with JIRA Cleanup", use_container_width=True):
            st.switch_page("pages/1_🗑️_Wipe_JIRA.py")
    
    with col2:
        if st.button("📄 Upload PI Goals", use_container_width=True):
            st.switch_page("pages/2_📄_Upload_Goals.py")
    
    with col3:
        if st.button("📊 View Documentation", use_container_width=True):
            st.info("Check the README.md file for detailed setup instructions and API documentation.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem;">
        PI Planning Dashboard v1.0 | Powered by CrewAI, Streamlit & MCP
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
