"""
Goal Validator Agent for PI Planning Dashboard
CrewAI agent that validates and improves PI goals using SMART criteria
"""

import re
import time
import random
from typing import Dict, List, Any, Optional
from datetime import datetime

class GoalValidatorAgent:
    """
    CrewAI agent specialized in validating and improving PI goals
    Uses SMART criteria (Specific, Measurable, Achievable, Relevant, Time-bound)
    """
    
    def __init__(self):
        self.agent_name = "Goal Validator Agent"
        self.role = "SMART Goals Analyst"
        self.goal = "Validate and improve PI goals from documents"
        self.backstory = "Expert in SMART goal methodology and PI planning best practices"
        
        # SMART criteria definitions
        self.smart_criteria = {
            'specific': {
                'description': 'Goal is clear and well-defined',
                'keywords': ['implement', 'develop', 'create', 'build', 'establish', 'achieve'],
                'anti_keywords': ['improve', 'enhance', 'better', 'optimize', 'increase']
            },
            'measurable': {
                'description': 'Goal has quantifiable success criteria',
                'keywords': ['%', 'percent', 'number', 'count', 'metric', 'kpi', 'score', 'rating'],
                'patterns': [r'\d+%', r'\d+\.\d+', r'\$\d+', r'\d+\s*(seconds?|minutes?|hours?|days?|weeks?)']
            },
            'achievable': {
                'description': 'Goal is realistic and attainable',
                'keywords': ['realistic', 'feasible', 'attainable', 'possible'],
                'warning_keywords': ['revolutionary', 'groundbreaking', '100%', 'perfect', 'eliminate all']
            },
            'relevant': {
                'description': 'Goal aligns with business objectives',
                'keywords': ['business value', 'revenue', 'customer', 'user', 'efficiency', 'cost'],
                'contexts': ['business', 'customer', 'user experience', 'performance', 'security']
            },
            'time_bound': {
                'description': 'Goal has clear timeline and deadlines',
                'keywords': ['by', 'within', 'deadline', 'timeline', 'end of', 'complete by'],
                'patterns': [r'by\s+\w+\s+\d{4}', r'within\s+\d+\s+\w+', r'end\s+of\s+\w+']
            }
        }
    
    def validate_goals(self, text_content: str) -> Dict[str, Any]:
        """
        Main method to validate goals from text content
        
        Args:
            text_content: Raw text content from uploaded document
            
        Returns:
            Dictionary containing validation results and improved goals
        """
        
        # Simulate agent processing time
        time.sleep(1)
        
        # Extract individual goals from text
        goals = self._extract_goals(text_content)
        
        # Validate each goal against SMART criteria
        validated_goals = []
        total_smart_score = 0
        
        for i, goal_text in enumerate(goals):
            goal_analysis = self._analyze_single_goal(goal_text, i + 1)
            validated_goals.append(goal_analysis)
            total_smart_score += goal_analysis['smart_score']
        
        # Calculate overall assessment
        overall_smart_score = int(total_smart_score / len(goals)) if goals else 0
        quality_level = self._determine_quality_level(overall_smart_score)
        
        return {
            'original_text': text_content,
            'goals_count': len(goals),
            'goals': validated_goals,
            'smart_score': overall_smart_score,
            'quality_level': quality_level,
            'recommendations': self._generate_overall_recommendations(validated_goals),
            'processed_at': datetime.now().isoformat()
        }
    
    def _extract_goals(self, text_content: str) -> List[str]:
        """Extract individual goals from text content"""
        
        # Look for common goal patterns
        goal_patterns = [
            r'GOAL\s+\d+:.*?(?=GOAL\s+\d+:|$)',
            r'OBJECTIVE\s+\d+:.*?(?=OBJECTIVE\s+\d+:|$)',
            r'Goal:.*?(?=Goal:|$)',
            r'Objective:.*?(?=Objective:|$)'
        ]
        
        goals = []
        
        for pattern in goal_patterns:
            matches = re.findall(pattern, text_content, re.DOTALL | re.IGNORECASE)
            goals.extend([match.strip() for match in matches])
        
        # If no structured goals found, try to split by common separators
        if not goals:
            # Split by double newlines or numbered sections
            potential_goals = re.split(r'\n\s*\n|\d+\.\s+', text_content)
            goals = [goal.strip() for goal in potential_goals if len(goal.strip()) > 50]
        
        # Clean up goals
        cleaned_goals = []
        for goal in goals:
            # Remove extra whitespace and normalize
            cleaned_goal = re.sub(r'\s+', ' ', goal.strip())
            if len(cleaned_goal) > 20:  # Minimum goal length
                cleaned_goals.append(cleaned_goal)
        
        return cleaned_goals[:10]  # Limit to 10 goals max
    
    def _analyze_single_goal(self, goal_text: str, goal_number: int) -> Dict[str, Any]:
        """Analyze a single goal against SMART criteria"""
        
        # Extract goal title
        title_match = re.search(r'(?:GOAL\s+\d+:|Goal:)?\s*([^\n]+)', goal_text, re.IGNORECASE)
        title = title_match.group(1).strip() if title_match else f"Goal {goal_number}"
        
        # Analyze against each SMART criterion
        smart_assessment = {}
        issues = []
        recommendations = []
        smart_score = 0
        
        # Specific
        specific_score = self._check_specific(goal_text)
        smart_assessment['specific'] = specific_score > 0.4
        if not smart_assessment['specific']:
            issues.append("Goal lacks specificity - too vague or general")
            recommendations.append("Be more specific about what exactly will be accomplished")
        smart_score += specific_score * 20
        
        # Measurable
        measurable_score = self._check_measurable(goal_text)
        smart_assessment['measurable'] = measurable_score > 0.3
        if not smart_assessment['measurable']:
            issues.append("Goal lacks measurable success criteria")
            recommendations.append("Add specific metrics, numbers, or quantifiable outcomes")
        smart_score += measurable_score * 20
        
        # Achievable
        achievable_score = self._check_achievable(goal_text)
        smart_assessment['achievable'] = achievable_score > 0.3
        if not smart_assessment['achievable']:
            issues.append("Goal may be unrealistic or overly ambitious")
            recommendations.append("Ensure the goal is realistic given available resources and time")
        smart_score += achievable_score * 20
        
        # Relevant
        relevant_score = self._check_relevant(goal_text)
        smart_assessment['relevant'] = relevant_score > 0.3
        if not smart_assessment['relevant']:
            issues.append("Goal lacks clear business relevance or value")
            recommendations.append("Clearly state the business value and impact")
        smart_score += relevant_score * 20
        
        # Time-bound
        time_bound_score = self._check_time_bound(goal_text)
        smart_assessment['time_bound'] = time_bound_score > 0.3
        if not smart_assessment['time_bound']:
            issues.append("Goal lacks clear timeline or deadline")
            recommendations.append("Add specific deadlines and milestones")
        smart_score += time_bound_score * 20
        
        # Generate improved version
        improved_version = self._generate_improved_goal(goal_text, smart_assessment, issues)
        
        return {
            'title': title,
            'original_text': goal_text,
            'improved_version': improved_version,
            'smart_assessment': smart_assessment,
            'smart_score': int(smart_score),
            'issues': issues,
            'recommendations': recommendations
        }
    
    def _check_specific(self, goal_text: str) -> float:
        """Check if goal is specific"""
        score = 0.0
        text_lower = goal_text.lower()
        
        # Check for specific action words
        specific_words = self.smart_criteria['specific']['keywords']
        for word in specific_words:
            if word in text_lower:
                score += 0.2
        
        # Penalize vague words
        vague_words = self.smart_criteria['specific']['anti_keywords']
        for word in vague_words:
            if word in text_lower:
                score -= 0.1
        
        # Check for detailed descriptions
        if len(goal_text.split()) > 20:
            score += 0.2
        
        return min(1.0, max(0.0, score))
    
    def _check_measurable(self, goal_text: str) -> float:
        """Check if goal is measurable"""
        score = 0.0
        text_lower = goal_text.lower()
        
        # Check for measurement keywords
        measure_words = self.smart_criteria['measurable']['keywords']
        for word in measure_words:
            if word in text_lower:
                score += 0.2
        
        # Check for numeric patterns
        patterns = self.smart_criteria['measurable']['patterns']
        for pattern in patterns:
            if re.search(pattern, goal_text):
                score += 0.3
        
        # Check for success criteria section
        if 'success criteria' in text_lower or 'metrics' in text_lower:
            score += 0.3
        
        return min(1.0, max(0.0, score))
    
    def _check_achievable(self, goal_text: str) -> float:
        """Check if goal is achievable"""
        score = 0.7  # Default to achievable unless red flags
        text_lower = goal_text.lower()
        
        # Check for warning words that suggest unrealistic goals
        warning_words = self.smart_criteria['achievable']['warning_keywords']
        for word in warning_words:
            if word in text_lower:
                score -= 0.2
        
        # Check for realistic language
        realistic_words = self.smart_criteria['achievable']['keywords']
        for word in realistic_words:
            if word in text_lower:
                score += 0.1
        
        return min(1.0, max(0.0, score))
    
    def _check_relevant(self, goal_text: str) -> float:
        """Check if goal is relevant to business"""
        score = 0.0
        text_lower = goal_text.lower()
        
        # Check for business relevance keywords
        relevant_words = self.smart_criteria['relevant']['keywords']
        for word in relevant_words:
            if word in text_lower:
                score += 0.2
        
        # Check for business value statement
        if 'business value' in text_lower or 'impact' in text_lower:
            score += 0.3
        
        # Check for context alignment
        contexts = self.smart_criteria['relevant']['contexts']
        for context in contexts:
            if context in text_lower:
                score += 0.1
        
        return min(1.0, max(0.0, score))
    
    def _check_time_bound(self, goal_text: str) -> float:
        """Check if goal is time-bound"""
        score = 0.0
        text_lower = goal_text.lower()
        
        # Check for time-related keywords
        time_words = self.smart_criteria['time_bound']['keywords']
        for word in time_words:
            if word in text_lower:
                score += 0.2
        
        # Check for time patterns
        patterns = self.smart_criteria['time_bound']['patterns']
        for pattern in patterns:
            if re.search(pattern, goal_text, re.IGNORECASE):
                score += 0.4
        
        # Check for PI-specific timeline
        if 'pi' in text_lower or 'program increment' in text_lower:
            score += 0.3
        
        return min(1.0, max(0.0, score))
    
    def _generate_improved_goal(self, original_goal: str, smart_assessment: Dict[str, bool], issues: List[str]) -> str:
        """Generate an improved version of the goal"""
        
        # Extract the core objective
        title_match = re.search(r'(?:GOAL\s+\d+:|Goal:)?\s*([^\n]+)', original_goal, re.IGNORECASE)
        core_objective = title_match.group(1).strip() if title_match else "Achieve objective"
        
        # Build improved goal components
        improved_parts = []
        
        # Start with specific objective
        if not smart_assessment.get('specific', False):
            improved_parts.append(f"Implement and deliver {core_objective.lower()}")
        else:
            improved_parts.append(core_objective)
        
        # Add measurable criteria
        if not smart_assessment.get('measurable', False):
            improved_parts.append("with measurable success criteria including specific KPIs and performance targets")
        
        # Add business relevance
        if not smart_assessment.get('relevant', False):
            improved_parts.append("to deliver clear business value and improve operational efficiency")
        
        # Add timeline
        if not smart_assessment.get('time_bound', False):
            improved_parts.append("by the end of the current Program Increment (PI)")
        
        # Combine parts
        improved_goal = " ".join(improved_parts)
        
        # Add success criteria template
        improved_goal += "\n\nSuccess Criteria:\n"
        improved_goal += "- Define specific, quantifiable metrics\n"
        improved_goal += "- Establish baseline and target values\n"
        improved_goal += "- Identify key stakeholders and beneficiaries\n"
        improved_goal += "- Set clear acceptance criteria\n"
        improved_goal += "- Define timeline with key milestones"
        
        return improved_goal
    
    def _determine_quality_level(self, smart_score: int) -> str:
        """Determine overall quality level based on SMART score"""
        if smart_score >= 90:
            return "Excellent"
        elif smart_score >= 75:
            return "Good"
        elif smart_score >= 60:
            return "Fair"
        elif smart_score >= 40:
            return "Poor"
        else:
            return "Very Poor"
    
    def _generate_overall_recommendations(self, validated_goals: List[Dict[str, Any]]) -> List[str]:
        """Generate overall recommendations for all goals"""
        
        recommendations = []
        
        # Analyze common issues across goals
        all_issues = []
        for goal in validated_goals:
            all_issues.extend(goal['issues'])
        
        # Count issue frequency
        issue_counts = {}
        for issue in all_issues:
            issue_type = issue.split(' - ')[0] if ' - ' in issue else issue
            issue_counts[issue_type] = issue_counts.get(issue_type, 0) + 1
        
        # Generate recommendations based on common issues
        if issue_counts.get("Goal lacks specificity", 0) > len(validated_goals) * 0.5:
            recommendations.append("Focus on making goals more specific and actionable")
        
        if issue_counts.get("Goal lacks measurable success criteria", 0) > len(validated_goals) * 0.5:
            recommendations.append("Add quantifiable metrics and KPIs to all goals")
        
        if issue_counts.get("Goal lacks clear timeline", 0) > len(validated_goals) * 0.5:
            recommendations.append("Establish clear deadlines and milestones for all goals")
        
        if issue_counts.get("Goal lacks clear business relevance", 0) > len(validated_goals) * 0.5:
            recommendations.append("Clearly articulate business value and impact for each goal")
        
        # Add general recommendations
        recommendations.extend([
            "Consider breaking down large goals into smaller, manageable objectives",
            "Ensure goals align with overall PI objectives and business strategy",
            "Review and validate goals with key stakeholders",
            "Establish regular check-ins and progress reviews"
        ])
        
        return recommendations[:6]  # Limit to top 6 recommendations
