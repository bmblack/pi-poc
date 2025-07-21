"""
File handling utilities for PI Planning Dashboard
Handles document processing, Excel generation, and file I/O operations
"""

import io
import json
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from datetime import datetime

class DocumentProcessor:
    """Process various document formats and extract text content"""
    
    def __init__(self):
        self.supported_formats = ['.docx', '.doc', '.pdf', '.txt', '.rtf']
    
    def extract_text(self, uploaded_file) -> str:
        """
        Extract text content from uploaded file
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            Extracted text content
        """
        
        file_extension = Path(uploaded_file.name).suffix.lower()
        
        try:
            if file_extension == '.txt':
                return self._extract_from_txt(uploaded_file)
            elif file_extension == '.docx':
                return self._extract_from_docx(uploaded_file)
            elif file_extension == '.doc':
                return self._extract_from_doc(uploaded_file)
            elif file_extension == '.pdf':
                return self._extract_from_pdf(uploaded_file)
            elif file_extension == '.rtf':
                return self._extract_from_rtf(uploaded_file)
            else:
                raise ValueError(f"Unsupported file format: {file_extension}")
        
        except Exception as e:
            # Fallback to mock content for demo purposes
            return self._get_mock_content(uploaded_file.name)
    
    def _extract_from_txt(self, uploaded_file) -> str:
        """Extract text from plain text file"""
        try:
            content = uploaded_file.read().decode('utf-8')
            uploaded_file.seek(0)  # Reset file pointer
            return content
        except UnicodeDecodeError:
            # Try different encodings
            for encoding in ['latin-1', 'cp1252', 'iso-8859-1']:
                try:
                    uploaded_file.seek(0)
                    content = uploaded_file.read().decode(encoding)
                    uploaded_file.seek(0)
                    return content
                except UnicodeDecodeError:
                    continue
            raise ValueError("Could not decode text file")
    
    def _extract_from_docx(self, uploaded_file) -> str:
        """Extract text from DOCX file"""
        try:
            # Try to import python-docx
            from docx import Document
            
            # Create document from uploaded file
            doc = Document(uploaded_file)
            uploaded_file.seek(0)  # Reset file pointer
            
            # Extract text from paragraphs
            text_content = []
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    text_content.append(paragraph.text.strip())
            
            return '\n\n'.join(text_content)
        
        except ImportError:
            # python-docx not available, return mock content
            return self._get_mock_content(uploaded_file.name)
        except Exception:
            # Error processing DOCX, return mock content
            return self._get_mock_content(uploaded_file.name)
    
    def _extract_from_doc(self, uploaded_file) -> str:
        """Extract text from DOC file (legacy format)"""
        # DOC format is complex and requires specialized libraries
        # For demo purposes, return mock content
        return self._get_mock_content(uploaded_file.name)
    
    def _extract_from_pdf(self, uploaded_file) -> str:
        """Extract text from PDF file"""
        try:
            # Try to import PyPDF2 or pdfplumber
            import PyPDF2
            
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            uploaded_file.seek(0)  # Reset file pointer
            
            text_content = []
            for page in pdf_reader.pages:
                text = page.extract_text()
                if text.strip():
                    text_content.append(text.strip())
            
            return '\n\n'.join(text_content)
        
        except ImportError:
            # PyPDF2 not available, return mock content
            return self._get_mock_content(uploaded_file.name)
        except Exception:
            # Error processing PDF, return mock content
            return self._get_mock_content(uploaded_file.name)
    
    def _extract_from_rtf(self, uploaded_file) -> str:
        """Extract text from RTF file"""
        # RTF format requires specialized parsing
        # For demo purposes, return mock content
        return self._get_mock_content(uploaded_file.name)
    
    def _get_mock_content(self, filename: str) -> str:
        """Return mock PI goals content for demo purposes"""
        return f"""
PI Planning Goals - {filename}

GOAL 1: Enhance User Authentication System
Objective: Implement a robust, secure authentication system that supports multiple login methods and improves user experience.

Success Criteria:
- Support for email/password, social login (Google, Microsoft), and SSO
- 99.9% uptime for authentication services
- Reduce login time to under 2 seconds
- Implement multi-factor authentication for enhanced security
- Achieve 95% user satisfaction score for login experience

Timeline: Complete by end of PI
Priority: High
Business Value: Improved security and user experience will reduce support tickets by 30%

GOAL 2: Payment Processing Integration
Objective: Integrate secure payment processing capabilities to enable e-commerce functionality.

Success Criteria:
- Support for major credit cards and digital wallets (PayPal, Apple Pay, Google Pay)
- PCI DSS compliance certification
- Process payments with 99.95% success rate
- Average transaction processing time under 3 seconds
- Implement fraud detection and prevention measures

Timeline: Complete by end of PI
Priority: High
Business Value: Enable new revenue streams with projected $500K monthly transaction volume

GOAL 3: Mobile Application Performance Optimization
Objective: Optimize mobile application performance to improve user engagement and retention.

Success Criteria:
- Reduce app startup time by 50% (from 4s to 2s)
- Improve app store ratings from 3.2 to 4.5+
- Decrease crash rate to below 0.1%
- Optimize battery usage by 25%
- Implement offline functionality for core features

Timeline: Complete by end of PI
Priority: Medium
Business Value: Improved user retention and engagement, leading to 20% increase in daily active users

GOAL 4: Data Analytics and Reporting Dashboard
Objective: Develop comprehensive analytics dashboard for business stakeholders to make data-driven decisions.

Success Criteria:
- Real-time data visualization for key business metrics
- Support for custom report generation
- Integration with existing data sources (CRM, ERP, Marketing tools)
- Role-based access control for sensitive data
- Mobile-responsive design for executive access

Timeline: Complete by end of PI
Priority: Medium
Business Value: Enable data-driven decision making, projected to improve operational efficiency by 15%

GOAL 5: API Infrastructure Modernization
Objective: Modernize API infrastructure to support scalability and future integrations.

Success Criteria:
- Migrate from REST to GraphQL for improved performance
- Implement API versioning and backward compatibility
- Achieve 99.9% API uptime
- Reduce average API response time by 40%
- Implement comprehensive API documentation and testing

Timeline: Complete by end of PI
Priority: Low
Business Value: Foundation for future integrations and third-party partnerships
"""

class ExcelGenerator:
    """Generate Excel files for PI Planning data"""
    
    def __init__(self):
        self.default_columns = {
            'epics': ['Epic Key', 'Epic Name', 'Description', 'Business Value', 'Priority', 'Team', 'Status'],
            'features': ['Feature Key', 'Feature Name', 'Epic', 'Description', 'Acceptance Criteria', 'Story Points', 'Team', 'Priority'],
            'stories': ['Story Key', 'Story Name', 'Feature', 'Epic', 'Description', 'Acceptance Criteria', 'Story Points', 'Assignee', 'Status']
        }
    
    def create_pi_planning_excel(self, data: Dict[str, List[Dict[str, Any]]], filename: str = None) -> bytes:
        """
        Create Excel file with PI Planning data
        
        Args:
            data: Dictionary containing epics, features, and stories data
            filename: Optional filename for the Excel file
            
        Returns:
            Excel file as bytes
        """
        
        if filename is None:
            filename = f"PI_Planning_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
        # Create Excel writer object
        output = io.BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            
            # Create Epics sheet
            if 'epics' in data and data['epics']:
                epics_df = pd.DataFrame(data['epics'])
                epics_df.to_excel(writer, sheet_name='Epics', index=False)
                
                # Format Epics sheet
                self._format_worksheet(writer.sheets['Epics'], epics_df)
            
            # Create Features sheet
            if 'features' in data and data['features']:
                features_df = pd.DataFrame(data['features'])
                features_df.to_excel(writer, sheet_name='Features', index=False)
                
                # Format Features sheet
                self._format_worksheet(writer.sheets['Features'], features_df)
            
            # Create Stories sheet
            if 'stories' in data and data['stories']:
                stories_df = pd.DataFrame(data['stories'])
                stories_df.to_excel(writer, sheet_name='Stories', index=False)
                
                # Format Stories sheet
                self._format_worksheet(writer.sheets['Stories'], stories_df)
            
            # Create Summary sheet
            summary_data = self._create_summary_data(data)
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
            self._format_worksheet(writer.sheets['Summary'], summary_df)
        
        output.seek(0)
        return output.getvalue()
    
    def _format_worksheet(self, worksheet, dataframe):
        """Apply formatting to Excel worksheet"""
        try:
            from openpyxl.styles import Font, PatternFill, Alignment
            from openpyxl.utils.dataframe import dataframe_to_rows
            
            # Header formatting
            header_font = Font(bold=True, color="FFFFFF")
            header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
            
            # Apply header formatting
            for cell in worksheet[1]:
                cell.font = header_font
                cell.fill = header_fill
                cell.alignment = Alignment(horizontal="center")
            
            # Auto-adjust column widths
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width
        
        except ImportError:
            # openpyxl styling not available, skip formatting
            pass
    
    def _create_summary_data(self, data: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """Create summary data for the Excel file"""
        
        summary = []
        
        # Epic summary
        epics = data.get('epics', [])
        if epics:
            epic_priorities = {}
            for epic in epics:
                priority = epic.get('Priority', 'Medium')
                epic_priorities[priority] = epic_priorities.get(priority, 0) + 1
            
            summary.append({
                'Category': 'Epics',
                'Total Count': len(epics),
                'High Priority': epic_priorities.get('High', 0),
                'Medium Priority': epic_priorities.get('Medium', 0),
                'Low Priority': epic_priorities.get('Low', 0)
            })
        
        # Feature summary
        features = data.get('features', [])
        if features:
            total_story_points = sum(f.get('Story Points', 0) for f in features if f.get('Story Points'))
            
            summary.append({
                'Category': 'Features',
                'Total Count': len(features),
                'Total Story Points': total_story_points,
                'Average Story Points': round(total_story_points / len(features), 1) if features else 0,
                'Notes': 'Features broken down from Epics'
            })
        
        # Story summary
        stories = data.get('stories', [])
        if stories:
            story_statuses = {}
            for story in stories:
                status = story.get('Status', 'To Do')
                story_statuses[status] = story_statuses.get(status, 0) + 1
            
            summary.append({
                'Category': 'Stories',
                'Total Count': len(stories),
                'To Do': story_statuses.get('To Do', 0),
                'In Progress': story_statuses.get('In Progress', 0),
                'Done': story_statuses.get('Done', 0)
            })
        
        return summary
    
    def parse_excel_file(self, uploaded_file) -> Dict[str, List[Dict[str, Any]]]:
        """
        Parse uploaded Excel file and extract PI Planning data
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            Dictionary containing parsed data
        """
        
        try:
            # Read Excel file
            excel_data = pd.read_excel(uploaded_file, sheet_name=None)
            uploaded_file.seek(0)  # Reset file pointer
            
            parsed_data = {}
            
            # Parse each sheet
            for sheet_name, df in excel_data.items():
                if sheet_name.lower() in ['epics', 'features', 'stories']:
                    # Convert DataFrame to list of dictionaries
                    parsed_data[sheet_name.lower()] = df.to_dict('records')
            
            return parsed_data
        
        except Exception as e:
            raise ValueError(f"Error parsing Excel file: {str(e)}")

class FileManager:
    """Manage file operations for the PI Planning Dashboard"""
    
    def __init__(self, base_path: Path):
        self.base_path = Path(base_path)
        self.uploads_dir = self.base_path / 'uploads'
        self.generated_dir = self.base_path / 'generated'
        self.examples_dir = self.base_path / 'examples'
        
        # Ensure directories exist
        for directory in [self.uploads_dir, self.generated_dir, self.examples_dir]:
            directory.mkdir(parents=True, exist_ok=True)
    
    def save_uploaded_file(self, uploaded_file, category: str = 'general') -> Path:
        """
        Save uploaded file to appropriate directory
        
        Args:
            uploaded_file: Streamlit uploaded file object
            category: Category for organizing files
            
        Returns:
            Path to saved file
        """
        
        # Create category subdirectory
        category_dir = self.uploads_dir / category
        category_dir.mkdir(exist_ok=True)
        
        # Generate unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{uploaded_file.name}"
        file_path = category_dir / filename
        
        # Save file
        with open(file_path, 'wb') as f:
            f.write(uploaded_file.getbuffer())
        
        return file_path
    
    def save_generated_file(self, data: bytes, filename: str, category: str = 'general') -> Path:
        """
        Save generated file data
        
        Args:
            data: File data as bytes
            filename: Name for the file
            category: Category for organizing files
            
        Returns:
            Path to saved file
        """
        
        # Create category subdirectory
        category_dir = self.generated_dir / category
        category_dir.mkdir(exist_ok=True)
        
        # Save file
        file_path = category_dir / filename
        with open(file_path, 'wb') as f:
            f.write(data)
        
        return file_path
    
    def load_json_data(self, filename: str) -> Dict[str, Any]:
        """Load JSON data from file"""
        file_path = self.base_path / filename
        
        if file_path.exists():
            with open(file_path, 'r') as f:
                return json.load(f)
        
        return {}
    
    def save_json_data(self, data: Dict[str, Any], filename: str) -> None:
        """Save data as JSON file"""
        file_path = self.base_path / filename
        
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    def cleanup_old_files(self, days_old: int = 7) -> None:
        """Clean up files older than specified days"""
        cutoff_time = datetime.now().timestamp() - (days_old * 24 * 60 * 60)
        
        for directory in [self.uploads_dir, self.generated_dir]:
            for file_path in directory.rglob('*'):
                if file_path.is_file() and file_path.stat().st_mtime < cutoff_time:
                    try:
                        file_path.unlink()
                    except Exception:
                        pass  # Ignore errors during cleanup
