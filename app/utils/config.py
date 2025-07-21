"""
Configuration management for PI Planning Dashboard
Handles environment variables, settings, and application configuration
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def load_config() -> Dict[str, Any]:
    """Load application configuration from environment and config files"""
    
    # Get the project root directory
    project_root = Path(__file__).parent.parent.parent
    
    # Default configuration
    config = {
        # Application settings
        'app_name': 'PI Planning Dashboard',
        'version': '1.0.0',
        'debug': os.getenv('DEBUG', 'False').lower() == 'true',
        
        # API Keys and credentials
        'openai_api_key': os.getenv('OPENAI_API_KEY', ''),
        'anthropic_api_key': os.getenv('ANTHROPIC_API_KEY', ''),
        
        # JIRA configuration
        'jira_server': os.getenv('JIRA_SERVER', 'https://your-company.atlassian.net'),
        'jira_user': os.getenv('JIRA_USER', ''),
        'jira_token': os.getenv('JIRA_TOKEN', ''),
        'jira_project_key': os.getenv('JIRA_PROJECT_KEY', 'PI'),
        
        # MCP server configuration
        'mcp_servers': {
            'team_mcp': {
                'host': os.getenv('TEAM_MCP_HOST', 'localhost'),
                'port': int(os.getenv('TEAM_MCP_PORT', '8001')),
                'enabled': os.getenv('TEAM_MCP_ENABLED', 'True').lower() == 'true'
            },
            'jira_mcp': {
                'host': os.getenv('JIRA_MCP_HOST', 'localhost'),
                'port': int(os.getenv('JIRA_MCP_PORT', '8002')),
                'enabled': os.getenv('JIRA_MCP_ENABLED', 'True').lower() == 'true'
            },
            'goal_mcp': {
                'host': os.getenv('GOAL_MCP_HOST', 'localhost'),
                'port': int(os.getenv('GOAL_MCP_PORT', '8003')),
                'enabled': os.getenv('GOAL_MCP_ENABLED', 'True').lower() == 'true'
            }
        },
        
        # CrewAI configuration
        'crewai': {
            'model': os.getenv('CREWAI_MODEL', 'gpt-4'),
            'temperature': float(os.getenv('CREWAI_TEMPERATURE', '0.1')),
            'max_tokens': int(os.getenv('CREWAI_MAX_TOKENS', '2000')),
            'verbose': os.getenv('CREWAI_VERBOSE', 'True').lower() == 'true'
        },
        
        # File handling
        'upload_max_size': int(os.getenv('UPLOAD_MAX_SIZE', '10485760')),  # 10MB
        'allowed_extensions': {
            'documents': ['.docx', '.doc', '.pdf', '.txt'],
            'spreadsheets': ['.xlsx', '.xls', '.csv']
        },
        
        # Paths
        'data_dir': project_root / 'data',
        'uploads_dir': project_root / 'data' / 'uploads',
        'generated_dir': project_root / 'data' / 'generated',
        'examples_dir': project_root / 'data' / 'examples',
        
        # Demo mode settings
        'demo_mode': os.getenv('DEMO_MODE', 'True').lower() == 'true',
        'mock_jira': os.getenv('DEMO_MODE', 'True').lower() == 'true',
        'mock_mcp': os.getenv('DEMO_MODE', 'True').lower() == 'true',
    }
    
    # Load MCP configuration file if it exists
    mcp_config_path = project_root / 'config' / 'mcp_config.json'
    if mcp_config_path.exists():
        try:
            with open(mcp_config_path, 'r') as f:
                mcp_config = json.load(f)
                config['mcp_servers'].update(mcp_config.get('servers', {}))
        except Exception as e:
            st.warning(f"Could not load MCP configuration: {e}")
    
    # Ensure data directories exist
    for dir_path in [config['data_dir'], config['uploads_dir'], 
                     config['generated_dir'], config['examples_dir']]:
        dir_path.mkdir(parents=True, exist_ok=True)
    
    return config

def get_jira_config() -> Dict[str, str]:
    """Get JIRA-specific configuration"""
    config = load_config()
    return {
        'server': config['jira_server'],
        'user': config['jira_user'],
        'token': config['jira_token'],
        'project_key': config['jira_project_key'],
        'mock_mode': config['mock_jira']
    }

def get_mcp_config() -> Dict[str, Any]:
    """Get MCP server configuration"""
    config = load_config()
    return config['mcp_servers']

def get_crewai_config() -> Dict[str, Any]:
    """Get CrewAI configuration"""
    config = load_config()
    return config['crewai']

def validate_api_keys() -> Dict[str, bool]:
    """Validate that required API keys are present"""
    config = load_config()
    
    validation = {
        'openai': bool(config['openai_api_key']),
        'anthropic': bool(config['anthropic_api_key']),
        'jira': bool(config['jira_user'] and config['jira_token']) or config['mock_jira']
    }
    
    return validation

def is_demo_mode() -> bool:
    """Check if application is running in demo mode"""
    config = load_config()
    return config['demo_mode']

def get_file_upload_config() -> Dict[str, Any]:
    """Get file upload configuration"""
    config = load_config()
    return {
        'max_size': config['upload_max_size'],
        'allowed_extensions': config['allowed_extensions'],
        'upload_dir': config['uploads_dir']
    }

def save_session_data(key: str, data: Any) -> None:
    """Save data to session state with persistence"""
    st.session_state[key] = data
    
    # Optionally save to file for persistence across sessions
    config = load_config()
    if config['debug']:
        session_file = config['data_dir'] / f'session_{key}.json'
        try:
            with open(session_file, 'w') as f:
                json.dump(data, f, indent=2, default=str)
        except Exception:
            pass  # Fail silently in production

def load_session_data(key: str, default: Any = None) -> Any:
    """Load data from session state with optional file fallback"""
    if key in st.session_state:
        return st.session_state[key]
    
    # Try to load from file if in debug mode
    config = load_config()
    if config['debug']:
        session_file = config['data_dir'] / f'session_{key}.json'
        if session_file.exists():
            try:
                with open(session_file, 'r') as f:
                    data = json.load(f)
                    st.session_state[key] = data
                    return data
            except Exception:
                pass
    
    return default

def get_agent_config(agent_name: str) -> Dict[str, Any]:
    """Get configuration for a specific agent"""
    crewai_config = get_crewai_config()
    
    # Agent-specific configurations
    agent_configs = {
        'goal_validator': {
            'role': 'SMART Goals Analyst',
            'goal': 'Validate and improve PI goals from documents',
            'backstory': 'Expert in SMART goal methodology and PI planning best practices',
            'tools': ['document_parser', 'goal_validator', 'smart_criteria_checker'],
            'model': crewai_config['model'],
            'temperature': 0.1,  # Lower temperature for validation tasks
            'max_tokens': crewai_config['max_tokens']
        },
        'epic_generator': {
            'role': 'Epic & Feature Architect',
            'goal': 'Generate structured Epics and Features from validated goals',
            'backstory': 'Experienced in breaking down high-level goals into actionable work items',
            'tools': ['epic_generator', 'feature_creator', 'team_mapper'],
            'model': crewai_config['model'],
            'temperature': 0.3,  # Moderate creativity for generation
            'max_tokens': crewai_config['max_tokens']
        },
        'story_analyzer': {
            'role': 'Backlog Quality Auditor',
            'goal': 'Identify and improve poorly written user stories',
            'backstory': 'Quality assurance expert specializing in user story best practices',
            'tools': ['story_analyzer', 'quality_checker', 'improvement_suggester'],
            'model': crewai_config['model'],
            'temperature': 0.2,  # Low creativity for analysis
            'max_tokens': crewai_config['max_tokens']
        },
        'dependency_agent': {
            'role': 'Cross-Team Dependency Mapper',
            'goal': 'Identify team dependencies and potential blockers',
            'backstory': 'Systems thinking expert with deep understanding of team dynamics',
            'tools': ['dependency_mapper', 'team_analyzer', 'risk_assessor'],
            'model': crewai_config['model'],
            'temperature': 0.1,  # Very low creativity for dependency analysis
            'max_tokens': crewai_config['max_tokens']
        }
    }
    
    return agent_configs.get(agent_name, crewai_config)

# Initialize configuration on module import
_config = load_config()
