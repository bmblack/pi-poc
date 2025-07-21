"""
Epic Generator Agent for PI Planning Dashboard
CrewAI agent that generates Epics and Features from validated PI goals
"""

import re
import time
import random
from typing import Dict, List, Any, Optional
from datetime import datetime

class EpicGeneratorAgent:
    """
    CrewAI agent specialized in generating Epics and Features from PI goals
    """
    
    def __init__(self):
        self.agent_name = "Epic Generator Agent"
        self.role = "Epic & Feature Architect"
        self.goal = "Generate structured Epics and Features from PI goals"
        self.backstory = "Expert in breaking down high-level goals into actionable development work"
        
        # Team categories for assignment
        self.team_categories = {
            'Frontend': ['UI', 'UX', 'React', 'Angular', 'Vue', 'mobile', 'web', 'interface'],
            'Backend': ['API', 'service', 'database', 'server', 'microservice', 'integration'],
            'DevOps': ['deployment', 'infrastructure', 'CI/CD', 'monitoring', 'security'],
            'QA': ['testing', 'quality', 'automation', 'validation', 'verification'],
            'Data': ['analytics', 'reporting', 'data', 'metrics', 'dashboard'],
            'Security': ['security', 'authentication', 'authorization', 'compliance']
        }
        
        # Effort estimation guidelines (story points)
        self.effort_guidelines = {
            'XS': {'points': 1, 'description': 'Simple configuration or minor UI change'},
            'S': {'points': 2, 'description': 'Small feature or bug fix'},
            'M': {'points': 3, 'description': 'Medium complexity feature'},
            'L': {'points': 5, 'description': 'Large feature requiring multiple components'},
            'XL': {'points': 8, 'description': 'Complex feature with significant integration'},
            'XXL': {'points': 13, 'description': 'Epic-level work requiring breakdown'}
        }
    
    def generate_epics_and_features(self, goals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Main method to generate Epics and Features from validated goals
        """
        
        # Simulate agent processing time
        time.sleep(2)
        
        generated_epics = []
        all_features = []
        
        for goal in goals:
            # Generate Epic from goal
            epic = self._generate_epic_from_goal(goal)
            
            # Generate Features for the Epic
            features = self._generate_features_for_epic(epic, goal)
            
            epic['features'] = features
            epic['feature_count'] = len(features)
            epic['total_effort'] = sum(f['effort_points'] for f in features)
            
            generated_epics.append(epic)
            all_features.extend(features)
        
        # Generate team assignments
        team_assignments = self._assign_teams_to_features(all_features)
        
        # Calculate summary statistics
        total_effort = sum(epic['total_effort'] for epic in generated_epics)
        
        return {
            'epics': generated_epics,
            'features': all_features,
            'team_assignments': team_assignments,
            'summary': {
                'total_epics': len(generated_epics),
                'total_features': len(all_features),
                'total_effort_points': total_effort,
                'estimated_weeks': max(1, total_effort // 20),
                'teams_involved': len(team_assignments)
            },
            'generated_at': datetime.now().isoformat()
        }
    
    def _generate_epic_from_goal(self, goal: Dict[str, Any]) -> Dict[str, Any]:
        """Generate an Epic from a PI goal"""
        
        goal_text = goal.get('text', goal.get('original_text', ''))
        goal_title = goal.get('title', 'Untitled Goal')
        
        # Extract epic title from goal
        epic_title = self._extract_epic_title(goal_text, goal_title)
        
        return {
            'id': f"EPIC-{random.randint(1000, 9999)}",
            'title': epic_title,
            'description': goal_text[:200] + "..." if len(goal_text) > 200 else goal_text,
            'priority': goal.get('priority', 'Medium'),
            'category': goal.get('category', 'Business'),
            'acceptance_criteria': [
                "All features are implemented and tested",
                "Business requirements are met",
                "Performance targets are achieved"
            ],
            'original_goal': goal_text,
            'status': 'To Do'
        }
    
    def _extract_epic_title(self, goal_text: str, goal_title: str) -> str:
        """Extract a meaningful epic title from goal text"""
        
        if goal_title and goal_title != 'Untitled Goal':
            return goal_title[:60]
        
        # Look for action verbs
        action_patterns = [
            r'(implement|develop|create|build|establish|design)\s+([^.]+)',
            r'(improve|enhance|optimize)\s+([^.]+)'
        ]
        
        for pattern in action_patterns:
            match = re.search(pattern, goal_text, re.IGNORECASE)
            if match:
                action = match.group(1).title()
                objective = match.group(2).strip()[:50]
                return f"{action} {objective}"
        
        return "Epic: Business Objective Implementation"
    
    def _generate_features_for_epic(self, epic: Dict[str, Any], goal: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate Features for an Epic"""
        
        features = []
        goal_text = goal.get('text', goal.get('original_text', ''))
        
        # Generate 3-5 features per epic
        feature_templates = self._get_feature_templates(goal_text, epic['category'])
        
        for i, template in enumerate(feature_templates[:5]):
            feature = {
                'id': f"FEAT-{random.randint(1000, 9999)}",
                'epic_id': epic['id'],
                'title': template['title'],
                'description': template['description'],
                'acceptance_criteria': template['acceptance_criteria'],
                'priority': epic['priority'],
                'effort_size': template['effort_size'],
                'effort_points': self.effort_guidelines[template['effort_size']]['points'],
                'assigned_team': self._suggest_team_assignment(template['title']),
                'status': 'To Do'
            }
            features.append(feature)
        
        return features
    
    def _get_feature_templates(self, goal_text: str, category: str) -> List[Dict[str, Any]]:
        """Get feature templates based on goal content"""
        
        templates = [
            {
                'title': 'Requirements Analysis and Design',
                'description': 'Analyze requirements and create technical design',
                'acceptance_criteria': ['Requirements documented', 'Design approved'],
                'effort_size': 'M'
            },
            {
                'title': 'Core Implementation',
                'description': 'Implement core functionality',
                'acceptance_criteria': ['Core features working', 'Unit tests passing'],
                'effort_size': 'L'
            },
            {
                'title': 'User Interface Development',
                'description': 'Create user interface components',
                'acceptance_criteria': ['UI components created', 'Responsive design'],
                'effort_size': 'M'
            },
            {
                'title': 'Integration and Testing',
                'description': 'Integrate components and perform testing',
                'acceptance_criteria': ['Integration complete', 'All tests passing'],
                'effort_size': 'M'
            },
            {
                'title': 'Documentation and Deployment',
                'description': 'Create documentation and deploy to production',
                'acceptance_criteria': ['Documentation complete', 'Successfully deployed'],
                'effort_size': 'S'
            }
        ]
        
        return templates
    
    def _suggest_team_assignment(self, feature_title: str) -> str:
        """Suggest team assignment based on feature content"""
        
        title_lower = feature_title.lower()
        
        for team, keywords in self.team_categories.items():
            for keyword in keywords:
                if keyword.lower() in title_lower:
                    return team
        
        return 'Backend'  # Default assignment
    
    def _assign_teams_to_features(self, features: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """Generate team assignments summary"""
        
        team_assignments = {}
        
        for feature in features:
            team = feature['assigned_team']
            if team not in team_assignments:
                team_assignments[team] = []
            team_assignments[team].append(feature['title'])
        
        return team_assignments
