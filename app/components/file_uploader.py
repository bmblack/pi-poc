"""
Reusable file upload components for PI Planning Dashboard
"""

import streamlit as st
from typing import List, Optional, Dict, Any
from pathlib import Path

def render_file_uploader(
    label: str,
    accepted_types: List[str],
    max_size_mb: int = 10,
    help_text: Optional[str] = None,
    key: Optional[str] = None
) -> Optional[Any]:
    """
    Render a file uploader with validation and preview
    
    Args:
        label: Label for the file uploader
        accepted_types: List of accepted file extensions (without dots)
        max_size_mb: Maximum file size in MB
        help_text: Optional help text
        key: Optional key for the widget
    
    Returns:
        Uploaded file object or None
    """
    
    # File uploader
    uploaded_file = st.file_uploader(
        label,
        type=accepted_types,
        help=help_text or f"Maximum file size: {max_size_mb}MB",
        key=key
    )
    
    if uploaded_file is not None:
        # Validate file size
        file_size_mb = uploaded_file.size / (1024 * 1024)
        
        if file_size_mb > max_size_mb:
            st.error(f"File size ({file_size_mb:.1f}MB) exceeds maximum allowed size ({max_size_mb}MB)")
            return None
        
        # Display file info
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("File Name", uploaded_file.name)
        
        with col2:
            st.metric("File Size", f"{file_size_mb:.1f}MB")
        
        with col3:
            file_type = Path(uploaded_file.name).suffix.lower()
            st.metric("File Type", file_type)
        
        return uploaded_file
    
    return None

def render_drag_drop_area(
    label: str,
    accepted_types: List[str],
    max_size_mb: int = 10,
    key: Optional[str] = None
) -> Optional[Any]:
    """
    Render a drag-and-drop file upload area
    
    Args:
        label: Label for the upload area
        accepted_types: List of accepted file extensions
        max_size_mb: Maximum file size in MB
        key: Optional key for the widget
    
    Returns:
        Uploaded file object or None
    """
    
    # Custom CSS for drag-drop styling
    st.markdown("""
    <style>
    .upload-area {
        border: 2px dashed #cccccc;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        background-color: #f8f9fa;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    .upload-area:hover {
        border-color: #1f77b4;
        background-color: #e8f4f8;
    }
    .upload-icon {
        font-size: 3rem;
        color: #666;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Upload area
    st.markdown(f"""
    <div class="upload-area">
        <div class="upload-icon">📁</div>
        <h3>{label}</h3>
        <p>Drag and drop your file here, or click to browse</p>
        <p><small>Accepted formats: {', '.join(accepted_types)} | Max size: {max_size_mb}MB</small></p>
    </div>
    """, unsafe_allow_html=True)
    
    # File uploader (hidden styling)
    uploaded_file = st.file_uploader(
        "Choose file",
        type=accepted_types,
        label_visibility="collapsed",
        key=key
    )
    
    return uploaded_file

def validate_file_content(uploaded_file, expected_content_type: str) -> Dict[str, Any]:
    """
    Validate file content based on expected type
    
    Args:
        uploaded_file: Streamlit uploaded file object
        expected_content_type: Expected content type ('document', 'spreadsheet', 'image')
    
    Returns:
        Dictionary with validation results
    """
    
    if uploaded_file is None:
        return {'valid': False, 'error': 'No file provided'}
    
    file_extension = Path(uploaded_file.name).suffix.lower()
    
    # Define valid extensions for each content type
    valid_extensions = {
        'document': ['.docx', '.doc', '.pdf', '.txt', '.rtf'],
        'spreadsheet': ['.xlsx', '.xls', '.csv', '.ods'],
        'image': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg'],
        'any': []  # Accept any file type
    }
    
    if expected_content_type != 'any':
        expected_extensions = valid_extensions.get(expected_content_type, [])
        
        if file_extension not in expected_extensions:
            return {
                'valid': False,
                'error': f'Invalid file type. Expected: {", ".join(expected_extensions)}'
            }
    
    # Additional validation based on file content
    try:
        # Read first few bytes to validate file signature
        file_bytes = uploaded_file.read(1024)
        uploaded_file.seek(0)  # Reset file pointer
        
        # Basic file signature validation
        if expected_content_type == 'document':
            if file_extension == '.pdf' and not file_bytes.startswith(b'%PDF'):
                return {'valid': False, 'error': 'Invalid PDF file format'}
            elif file_extension in ['.docx', '.xlsx'] and not file_bytes.startswith(b'PK'):
                return {'valid': False, 'error': 'Invalid Office document format'}
        
        return {'valid': True, 'message': 'File validation successful'}
    
    except Exception as e:
        return {'valid': False, 'error': f'File validation error: {str(e)}'}

def display_file_preview(uploaded_file, max_preview_size: int = 500) -> None:
    """
    Display a preview of the uploaded file content
    
    Args:
        uploaded_file: Streamlit uploaded file object
        max_preview_size: Maximum number of characters to preview
    """
    
    if uploaded_file is None:
        return
    
    file_extension = Path(uploaded_file.name).suffix.lower()
    
    st.markdown("### 👀 File Preview")
    
    try:
        if file_extension == '.txt':
            # Text file preview
            content = uploaded_file.read().decode('utf-8')
            uploaded_file.seek(0)  # Reset file pointer
            
            preview_content = content[:max_preview_size]
            if len(content) > max_preview_size:
                preview_content += "..."
            
            st.text_area("File content preview", preview_content, height=200, disabled=True)
        
        elif file_extension == '.csv':
            # CSV file preview
            import pandas as pd
            df = pd.read_csv(uploaded_file)
            uploaded_file.seek(0)  # Reset file pointer
            
            st.dataframe(df.head(10), use_container_width=True)
            st.info(f"Showing first 10 rows of {len(df)} total rows")
        
        elif file_extension in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
            # Image preview
            st.image(uploaded_file, caption=uploaded_file.name, use_column_width=True)
        
        else:
            # Generic file info
            st.info(f"Preview not available for {file_extension} files. File will be processed when submitted.")
    
    except Exception as e:
        st.warning(f"Could not generate preview: {str(e)}")

def create_download_link(data, filename: str, mime_type: str = "application/octet-stream") -> None:
    """
    Create a download link for generated data
    
    Args:
        data: Data to download (bytes or string)
        filename: Name for the downloaded file
        mime_type: MIME type for the file
    """
    
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    st.download_button(
        label=f"📥 Download {filename}",
        data=data,
        file_name=filename,
        mime=mime_type,
        use_container_width=True
    )

def render_file_upload_progress(current_step: int, total_steps: int, step_name: str) -> None:
    """
    Render a progress indicator for file upload/processing
    
    Args:
        current_step: Current step number
        total_steps: Total number of steps
        step_name: Name of the current step
    """
    
    progress = current_step / total_steps
    
    st.markdown("### 📊 Processing Progress")
    st.progress(progress)
    st.markdown(f"**Step {current_step} of {total_steps}:** {step_name}")
    
    if current_step < total_steps:
        st.info("Please wait while we process your file...")
    else:
        st.success("✅ Processing complete!")
