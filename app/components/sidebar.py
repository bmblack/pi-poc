"""
Shared sidebar component for PI Planning Dashboard
Provides navigation and progress tracking across all pages
"""

import streamlit as st
from typing import Dict, List

def get_workflow_status() -> Dict[str, str]:
    """Get the current workflow status from session state"""
    if 'workflow_status' not in st.session_state:
        st.session_state.workflow_status = {
            'jira_wipe': 'pending',
            'goals_upload': 'pending',
            'epics_generation': 'pending',
            'review_push': 'pending',
            'backlog_analysis': 'pending',
            'dependency_check': 'pending'
        }
    return st.session_state.workflow_status

def update_workflow_status(step: str, status: str):
    """Update the status of a workflow step"""
    workflow_status = get_workflow_status()
    workflow_status[step] = status
    st.session_state.workflow_status = workflow_status

def get_status_badge(status: str) -> str:
    """Return HTML for status badge"""
    if status == 'complete':
        return '<span class="status-badge status-complete">✅ Complete</span>'
    elif status == 'progress':
        return '<span class="status-badge status-progress">🔄 In Progress</span>'
    else:
        return '<span class="status-badge status-pending">⏳ Pending</span>'

def render_sidebar():
    """Render the main sidebar with navigation and progress tracking"""
    
    with st.sidebar:
        st.markdown("# 🎯 PI Planning")
        st.markdown("### Workflow Progress")
        
        # Get current workflow status
        status = get_workflow_status()
        
        # Workflow steps with status
        workflow_steps = [
            {
                'key': 'jira_wipe',
                'title': '🗑️ JIRA Cleanup',
                'page': 'pages/1_🗑️_Wipe_JIRA.py',
                'description': 'Clean project data'
            },
            {
                'key': 'goals_upload',
                'title': '📄 Upload Goals',
                'page': 'pages/2_📄_Upload_Goals.py',
                'description': 'Upload PI goals document'
            },
            {
                'key': 'epics_generation',
                'title': '⚡ Generate Epics',
                'page': 'pages/3_⚡_Generate_Epics.py',
                'description': 'AI-generated Epics & Features'
            },
            {
                'key': 'review_push',
                'title': '📊 Review & Push',
                'page': 'pages/4_📊_Review_Push.py',
                'description': 'Review and push to JIRA'
            },
            {
                'key': 'backlog_analysis',
                'title': '🔍 Analyze Backlog',
                'page': 'pages/5_🔍_Analyze_Backlog.py',
                'description': 'Story quality analysis'
            },
            {
                'key': 'dependency_check',
                'title': '🔗 Dependencies',
                'page': 'pages/6_🔗_Dependency_Check.py',
                'description': 'Team dependency mapping'
            }
        ]
        
        # Render workflow steps
        for i, step in enumerate(workflow_steps, 1):
            step_status = status.get(step['key'], 'pending')
            
            # Create expandable section for each step
            with st.expander(f"{i}. {step['title']}", expanded=False):
                st.markdown(f"**Status:** {get_status_badge(step_status)}", unsafe_allow_html=True)
                st.markdown(f"*{step['description']}*")
                
                if st.button(f"Go to {step['title']}", key=f"nav_{step['key']}", use_container_width=True):
                    st.switch_page(step['page'])
        
        st.markdown("---")
        
        # Configuration section
        st.markdown("### ⚙️ Configuration")
        
        # JIRA connection status
        jira_connected = st.session_state.get('jira_connected', False)
        jira_status = "🟢 Connected" if jira_connected else "🔴 Disconnected"
        st.markdown(f"**JIRA:** {jira_status}")
        
        # MCP servers status
        mcp_status = st.session_state.get('mcp_servers_active', 0)
        st.markdown(f"**MCP Servers:** {mcp_status}/3 Active")
        
        # AI agents status
        agents_ready = st.session_state.get('agents_ready', False)
        agents_status = "🟢 Ready" if agents_ready else "🟡 Initializing"
        st.markdown(f"**AI Agents:** {agents_status}")
        
        st.markdown("---")
        
        # Quick stats
        st.markdown("### 📊 Quick Stats")
        
        # Session statistics
        stats = st.session_state.get('session_stats', {
            'goals_processed': 0,
            'epics_generated': 0,
            'stories_analyzed': 0,
            'dependencies_found': 0
        })
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Goals", stats['goals_processed'])
            st.metric("Stories", stats['stories_analyzed'])
        
        with col2:
            st.metric("Epics", stats['epics_generated'])
            st.metric("Dependencies", stats['dependencies_found'])
        
        st.markdown("---")
        
        # Help and support
        st.markdown("### 🆘 Help & Support")
        
        if st.button("📖 View Documentation", use_container_width=True):
            st.info("Check the README.md file for detailed documentation and troubleshooting guides.")
        
        if st.button("🔄 Reset Workflow", use_container_width=True):
            # Reset workflow status
            st.session_state.workflow_status = {
                'jira_wipe': 'pending',
                'goals_upload': 'pending',
                'epics_generation': 'pending',
                'review_push': 'pending',
                'backlog_analysis': 'pending',
                'dependency_check': 'pending'
            }
            st.session_state.session_stats = {
                'goals_processed': 0,
                'epics_generated': 0,
                'stories_analyzed': 0,
                'dependencies_found': 0
            }
            st.success("Workflow reset successfully!")
            st.rerun()
        
        # Version info
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; font-size: 0.8rem; color: #666;">
            PI Planning Dashboard v1.0<br>
            Powered by CrewAI & MCP
        </div>
        """, unsafe_allow_html=True)

def render_page_header(title: str, description: str, step_number: int):
    """Render a consistent page header"""
    st.markdown(f"""
    <div style="background: linear-gradient(90deg, #1f77b4, #17a2b8); padding: 1.5rem; border-radius: 10px; margin-bottom: 2rem;">
        <h1 style="color: white; margin: 0; font-size: 2.5rem;">
            Step {step_number}: {title}
        </h1>
        <p style="color: #e8f4f8; margin: 0.5rem 0 0 0; font-size: 1.1rem;">
            {description}
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_progress_indicator(current_step: int, total_steps: int = 6):
    """Render a progress indicator showing current step"""
    progress = current_step / total_steps
    
    st.markdown("### 📈 Workflow Progress")
    st.progress(progress)
    st.markdown(f"**Step {current_step} of {total_steps}** ({int(progress * 100)}% complete)")
    
    # Show next step hint
    if current_step < total_steps:
        next_step = current_step + 1
        st.info(f"💡 **Next:** Step {next_step} - Continue to the next phase of your PI Planning workflow.")
