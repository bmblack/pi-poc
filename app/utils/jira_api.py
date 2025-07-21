"""
JIRA API Client for PI Planning Dashboard
Handles JIRA integration with mock implementations for demo mode
"""

import time
import random
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

class JIRAClient:
    """JIRA API client with mock implementation for demo purposes"""
    
    def __init__(self, config: Dict[str, str]):
        self.config = config
        self.mock_mode = config.get('mock_mode', True)
        self.server = config.get('server', '')
        self.user = config.get('user', '')
        self.token = config.get('token', '')
        self.project_key = config.get('project_key', 'PI')
        
        # Mock data for demo mode
        self.mock_data = self._initialize_mock_data()
    
    def _initialize_mock_data(self) -> Dict[str, Any]:
        """Initialize mock JIRA data for demo purposes"""
        return {
            'epics': [
                {
                    'key': 'PI-1',
                    'summary': 'User Authentication System',
                    'status': 'To Do',
                    'assignee': 'john.doe@company.com',
                    'created': datetime.now() - timedelta(days=30)
                },
                {
                    'key': 'PI-2',
                    'summary': 'Payment Processing Integration',
                    'status': 'In Progress',
                    'assignee': 'jane.smith@company.com',
                    'created': datetime.now() - timedelta(days=25)
                },
                {
                    'key': 'PI-3',
                    'summary': 'Mobile App Performance Optimization',
                    'status': 'To Do',
                    'assignee': 'mike.johnson@company.com',
                    'created': datetime.now() - timedelta(days=20)
                }
            ],
            'stories': [
                {
                    'key': 'PI-10',
                    'summary': 'As a user, I want to login with email and password',
                    'status': 'To Do',
                    'epic': 'PI-1',
                    'story_points': 5,
                    'assignee': 'john.doe@company.com'
                },
                {
                    'key': 'PI-11',
                    'summary': 'As a user, I want to reset my password',
                    'status': 'To Do',
                    'epic': 'PI-1',
                    'story_points': 3,
                    'assignee': 'john.doe@company.com'
                },
                {
                    'key': 'PI-12',
                    'summary': 'As a customer, I want to pay with credit card',
                    'status': 'In Progress',
                    'epic': 'PI-2',
                    'story_points': 8,
                    'assignee': 'jane.smith@company.com'
                },
                {
                    'key': 'PI-13',
                    'summary': 'As a user, I want the app to load quickly',
                    'status': 'To Do',
                    'epic': 'PI-3',
                    'story_points': 13,
                    'assignee': 'mike.johnson@company.com'
                },
                {
                    'key': 'PI-14',
                    'summary': 'Fix login bug',  # Poorly written story for analysis
                    'status': 'To Do',
                    'epic': 'PI-1',
                    'story_points': None,
                    'assignee': None
                }
            ],
            'tasks': [
                {
                    'key': 'PI-20',
                    'summary': 'Setup authentication database tables',
                    'status': 'Done',
                    'parent': 'PI-10',
                    'assignee': 'john.doe@company.com'
                },
                {
                    'key': 'PI-21',
                    'summary': 'Implement password hashing',
                    'status': 'In Progress',
                    'parent': 'PI-10',
                    'assignee': 'john.doe@company.com'
                }
            ],
            'bugs': [
                {
                    'key': 'PI-30',
                    'summary': 'Login form validation not working',
                    'status': 'Open',
                    'priority': 'High',
                    'assignee': 'john.doe@company.com'
                }
            ],
            'components': ['Frontend', 'Backend', 'Mobile', 'API'],
            'versions': ['v1.0', 'v1.1', 'v2.0'],
            'labels': ['authentication', 'payment', 'performance', 'mobile', 'security']
        }
    
    def is_connected(self) -> bool:
        """Check if connected to JIRA"""
        if self.mock_mode:
            return True
        
        # TODO: Implement real JIRA connection check
        # For now, return True if credentials are provided
        return bool(self.server and self.user and self.token)
    
    def get_project_summary(self) -> Dict[str, int]:
        """Get summary of current project state"""
        # Check if we have valid JIRA credentials
        has_valid_credentials = bool(self.server and self.user and self.token and self.token != 'your-jira-api-token')
        
        if self.mock_mode or not has_valid_credentials:
            # Simulate API delay
            time.sleep(0.5)
            
            return {
                'epics': len(self.mock_data['epics']),
                'stories': len(self.mock_data['stories']),
                'tasks': len(self.mock_data['tasks']),
                'bugs': len(self.mock_data['bugs'])
            }
        
        # Real JIRA API call
        try:
            from jira import JIRA
            
            # Connect to JIRA
            jira = JIRA(server=self.server, basic_auth=(self.user, self.token))
            
            # Get project issues
            epics = jira.search_issues(f'project = {self.project_key} AND issuetype = Epic')
            stories = jira.search_issues(f'project = {self.project_key} AND issuetype = Story')
            tasks = jira.search_issues(f'project = {self.project_key} AND issuetype = Task')
            bugs = jira.search_issues(f'project = {self.project_key} AND issuetype = Bug')
            
            return {
                'epics': len(epics),
                'stories': len(stories),
                'tasks': len(tasks),
                'bugs': len(bugs)
            }
            
        except Exception as e:
            # If JIRA connection fails, return empty project
            print(f"JIRA connection failed: {e}")
            return {'epics': 0, 'stories': 0, 'tasks': 0, 'bugs': 0}
    
    def cleanup_items(self, item_type: str) -> Dict[str, Any]:
        """Clean up specific type of items"""
        # Check if we have valid JIRA credentials
        has_valid_credentials = bool(self.server and self.user and self.token and self.token != 'your-jira-api-token')
        
        if self.mock_mode or not has_valid_credentials:
            # Simulate API processing time
            time.sleep(random.uniform(0.5, 2.0))
            
            # Mock cleanup results
            cleanup_counts = {
                'epics': len(self.mock_data['epics']),
                'stories': len(self.mock_data['stories']),
                'tasks': len(self.mock_data['tasks']),
                'bugs': len(self.mock_data['bugs']),
                'subtasks': random.randint(0, 5),
                'components': len(self.mock_data['components']),
                'versions': len(self.mock_data['versions']),
                'labels': len(self.mock_data['labels']),
                'workflows': random.randint(0, 3)
            }
            
            count = cleanup_counts.get(item_type, 0)
            
            # Simulate occasional failures for realism
            if random.random() < 0.1:  # 10% chance of failure
                return {
                    'success': False,
                    'error': f'Failed to delete {item_type}: Permission denied'
                }
            
            # Clear the mock data for this item type
            if item_type in self.mock_data:
                self.mock_data[item_type] = []
            
            return {
                'success': True,
                'count': count,
                'message': f'Deleted {count} {item_type}'
            }
        
        # Real JIRA cleanup implementation
        try:
            from jira import JIRA
            
            # Connect to JIRA
            jira = JIRA(server=self.server, basic_auth=(self.user, self.token))
            
            # Map item types to JIRA issue types
            issue_type_mapping = {
                'epics': 'Epic',
                'stories': 'Story', 
                'tasks': 'Task',
                'bugs': 'Bug',
                'subtasks': 'Sub-task'
            }
            
            if item_type in issue_type_mapping:
                # Get all issues of this type
                jql = f'project = {self.project_key} AND issuetype = "{issue_type_mapping[item_type]}"'
                issues = jira.search_issues(jql)
                
                # Delete each issue
                deleted_count = 0
                for issue in issues:
                    try:
                        issue.delete()
                        deleted_count += 1
                    except Exception as e:
                        print(f"Failed to delete {issue.key}: {e}")
                
                return {
                    'success': True,
                    'count': deleted_count,
                    'message': f'Deleted {deleted_count} {item_type}'
                }
            
            elif item_type == 'components':
                # Delete project components
                project = jira.project(self.project_key)
                components = jira.project_components(project)
                deleted_count = len(components)
                
                for component in components:
                    try:
                        component.delete()
                    except Exception as e:
                        print(f"Failed to delete component {component.name}: {e}")
                
                return {
                    'success': True,
                    'count': deleted_count,
                    'message': f'Deleted {deleted_count} components'
                }
            
            elif item_type == 'versions':
                # Delete project versions
                project = jira.project(self.project_key)
                versions = jira.project_versions(project)
                deleted_count = len(versions)
                
                for version in versions:
                    try:
                        version.delete()
                    except Exception as e:
                        print(f"Failed to delete version {version.name}: {e}")
                
                return {
                    'success': True,
                    'count': deleted_count,
                    'message': f'Deleted {deleted_count} versions'
                }
            
            else:
                return {
                    'success': True,
                    'count': 0,
                    'message': f'No {item_type} found to delete'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'JIRA cleanup failed: {str(e)}'
            }
    
    def get_all_issues(self, issue_types: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Get all issues from the project"""
        if self.mock_mode:
            all_issues = []
            
            if not issue_types or 'Epic' in issue_types:
                all_issues.extend(self.mock_data['epics'])
            
            if not issue_types or 'Story' in issue_types:
                all_issues.extend(self.mock_data['stories'])
            
            if not issue_types or 'Task' in issue_types:
                all_issues.extend(self.mock_data['tasks'])
            
            if not issue_types or 'Bug' in issue_types:
                all_issues.extend(self.mock_data['bugs'])
            
            return all_issues
        
        # TODO: Implement real JIRA API call
        return []
    
    def create_epic(self, epic_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new Epic in JIRA"""
        if self.mock_mode:
            # Simulate API delay
            time.sleep(random.uniform(0.5, 1.5))
            
            # Generate mock epic key
            epic_key = f"{self.project_key}-{random.randint(100, 999)}"
            
            epic = {
                'key': epic_key,
                'summary': epic_data.get('summary', 'New Epic'),
                'description': epic_data.get('description', ''),
                'status': 'To Do',
                'assignee': epic_data.get('assignee'),
                'created': datetime.now(),
                'labels': epic_data.get('labels', []),
                'components': epic_data.get('components', [])
            }
            
            # Add to mock data
            self.mock_data['epics'].append(epic)
            
            return {
                'success': True,
                'key': epic_key,
                'url': f"{self.server}/browse/{epic_key}"
            }
        
        # TODO: Implement real JIRA Epic creation
        return {
            'success': False,
            'error': 'Real JIRA Epic creation not implemented yet'
        }
    
    def create_story(self, story_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new Story in JIRA"""
        if self.mock_mode:
            # Simulate API delay
            time.sleep(random.uniform(0.3, 1.0))
            
            # Generate mock story key
            story_key = f"{self.project_key}-{random.randint(100, 999)}"
            
            story = {
                'key': story_key,
                'summary': story_data.get('summary', 'New Story'),
                'description': story_data.get('description', ''),
                'status': 'To Do',
                'assignee': story_data.get('assignee'),
                'epic': story_data.get('epic_key'),
                'story_points': story_data.get('story_points'),
                'created': datetime.now(),
                'labels': story_data.get('labels', []),
                'components': story_data.get('components', [])
            }
            
            # Add to mock data
            self.mock_data['stories'].append(story)
            
            return {
                'success': True,
                'key': story_key,
                'url': f"{self.server}/browse/{story_key}"
            }
        
        # TODO: Implement real JIRA Story creation
        return {
            'success': False,
            'error': 'Real JIRA Story creation not implemented yet'
        }
    
    def bulk_create_issues(self, issues_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create multiple issues in bulk"""
        if self.mock_mode:
            created_issues = []
            errors = []
            
            for issue_data in issues_data:
                issue_type = issue_data.get('issue_type', 'Story')
                
                try:
                    if issue_type == 'Epic':
                        result = self.create_epic(issue_data)
                    else:
                        result = self.create_story(issue_data)
                    
                    if result['success']:
                        created_issues.append(result)
                    else:
                        errors.append(result['error'])
                
                except Exception as e:
                    errors.append(str(e))
            
            return {
                'success': len(errors) == 0,
                'created_count': len(created_issues),
                'error_count': len(errors),
                'created_issues': created_issues,
                'errors': errors
            }
        
        # TODO: Implement real JIRA bulk creation
        return {
            'success': False,
            'error': 'Real JIRA bulk creation not implemented yet'
        }
    
    def analyze_story_quality(self, story: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the quality of a user story"""
        issues = []
        score = 100
        
        # Check story format
        summary = story.get('summary', '')
        if not summary.lower().startswith('as a'):
            issues.append('Story does not follow "As a... I want... So that..." format')
            score -= 20
        
        # Check for acceptance criteria
        description = story.get('description', '')
        if not description or 'acceptance criteria' not in description.lower():
            issues.append('Missing acceptance criteria')
            score -= 15
        
        # Check story points
        if not story.get('story_points'):
            issues.append('Missing story points estimation')
            score -= 10
        
        # Check assignee
        if not story.get('assignee'):
            issues.append('No assignee specified')
            score -= 10
        
        # Check epic link
        if not story.get('epic'):
            issues.append('Not linked to an Epic')
            score -= 10
        
        # Check summary length
        if len(summary) < 10:
            issues.append('Summary too short')
            score -= 5
        elif len(summary) > 100:
            issues.append('Summary too long')
            score -= 5
        
        # Determine quality level
        if score >= 90:
            quality = 'Excellent'
        elif score >= 70:
            quality = 'Good'
        elif score >= 50:
            quality = 'Fair'
        else:
            quality = 'Poor'
        
        return {
            'score': max(0, score),
            'quality': quality,
            'issues': issues,
            'recommendations': self._get_story_recommendations(issues)
        }
    
    def _get_story_recommendations(self, issues: List[str]) -> List[str]:
        """Get recommendations based on story issues"""
        recommendations = []
        
        for issue in issues:
            if 'format' in issue.lower():
                recommendations.append('Rewrite using: "As a [user type], I want [functionality] so that [benefit]"')
            elif 'acceptance criteria' in issue.lower():
                recommendations.append('Add clear acceptance criteria with Given/When/Then format')
            elif 'story points' in issue.lower():
                recommendations.append('Estimate story points using planning poker or similar technique')
            elif 'assignee' in issue.lower():
                recommendations.append('Assign to appropriate team member based on skills required')
            elif 'epic' in issue.lower():
                recommendations.append('Link to relevant Epic to show business context')
            elif 'summary' in issue.lower():
                recommendations.append('Adjust summary length to be clear and concise (10-100 characters)')
        
        return recommendations
    
    def get_team_dependencies(self) -> List[Dict[str, Any]]:
        """Get team dependencies from JIRA data"""
        if self.mock_mode:
            # Mock dependency data
            return [
                {
                    'source_team': 'Frontend Team',
                    'target_team': 'Backend Team',
                    'dependency_type': 'API Integration',
                    'epic': 'PI-1',
                    'description': 'Frontend needs authentication API from Backend',
                    'risk_level': 'Medium',
                    'estimated_impact': '2-3 days delay if not coordinated'
                },
                {
                    'source_team': 'Mobile Team',
                    'target_team': 'Backend Team',
                    'dependency_type': 'API Integration',
                    'epic': 'PI-2',
                    'description': 'Mobile app needs payment processing API',
                    'risk_level': 'High',
                    'estimated_impact': '1 week delay if API not ready'
                },
                {
                    'source_team': 'QA Team',
                    'target_team': 'All Teams',
                    'dependency_type': 'Testing Environment',
                    'epic': 'All',
                    'description': 'QA needs stable test environment for all features',
                    'risk_level': 'Low',
                    'estimated_impact': 'Minimal if managed properly'
                }
            ]
        
        # TODO: Implement real dependency analysis
        return []
