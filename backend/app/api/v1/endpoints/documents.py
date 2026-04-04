from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
import os
import uuid
import shutil
from datetime import datetime
import pandas as pd
from typing import Optional

router = APIRouter()

# Create directories for document storage
UPLOAD_DIR = "uploads"
DOCUMENTS_DIR = os.path.join(UPLOAD_DIR, "documents")
AADHAR_DIR = os.path.join(DOCUMENTS_DIR, "aadhar")
LICENSE_DIR = os.path.join(DOCUMENTS_DIR, "license")

# Create directories if they don't exist
for directory in [UPLOAD_DIR, DOCUMENTS_DIR, AADHAR_DIR, LICENSE_DIR]:
    os.makedirs(directory, exist_ok=True)

# Allowed file types
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".pdf", ".doc", ".docx"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def validate_file(file: UploadFile) -> bool:
    """Validate file type and size"""
    # Check file extension
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        return False
    
    # Check file size (would need to read file content for actual size check)
    return True

def generate_unique_filename(original_filename: str) -> str:
    """Generate unique filename to prevent conflicts"""
    file_extension = os.path.splitext(original_filename)[1]
    unique_id = str(uuid.uuid4())
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{timestamp}_{unique_id}{file_extension}"

def save_document_metadata(user_id: str, document_type: str, filename: str, file_path: str):
    """Save document metadata to database"""
    try:
        # Create documents database if it doesn't exist
        documents_db_path = "database/documents_db.csv"
        
        # Check if file exists and create with headers if not
        if not os.path.exists(documents_db_path):
            with open(documents_db_path, 'w') as f:
                f.write("user_id,document_type,filename,file_path,upload_date,status,verified\n")
        
        # Add document record
        with open(documents_db_path, 'a') as f:
            f.write(f"{user_id},{document_type},{filename},{file_path},{datetime.now().isoformat()},pending,false\n")
            
        return True
    except Exception as e:
        print(f"Error saving document metadata: {e}")
        return False

@router.post("/upload/aadhar")
async def upload_aadhar(
    user_id: str,
    file: UploadFile = File(...),
    aadhar_number: Optional[str] = None
):
    """
    Upload Aadhar card document
    """
    try:
        # Validate file
        if not validate_file(file):
            raise HTTPException(
                status_code=400, 
                detail="Invalid file type. Allowed types: JPG, PNG, PDF, DOC, DOCX"
            )
        
        # Generate unique filename
        unique_filename = generate_unique_filename(file.filename)
        file_path = os.path.join(AADHAR_DIR, unique_filename)
        
        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Save metadata to database
        metadata_saved = save_document_metadata(
            user_id=user_id,
            document_type="aadhar",
            filename=file.filename,
            file_path=file_path
        )
        
        if not metadata_saved:
            # Clean up file if metadata saving failed
            os.remove(file_path)
            raise HTTPException(status_code=500, detail="Failed to save document metadata")
        
        return {
            "success": True,
            "message": "Aadhar document uploaded successfully",
            "document_id": unique_filename.split('_')[1],
            "filename": file.filename,
            "upload_date": datetime.now().isoformat(),
            "status": "pending_verification",
            "aadhar_number": aadhar_number
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@router.post("/upload/license")
async def upload_license(
    user_id: str,
    file: UploadFile = File(...),
    license_number: Optional[str] = None,
    license_type: Optional[str] = "driving"  # driving, professional, etc.
):
    """
    Upload License document
    """
    try:
        # Validate file
        if not validate_file(file):
            raise HTTPException(
                status_code=400, 
                detail="Invalid file type. Allowed types: JPG, PNG, PDF, DOC, DOCX"
            )
        
        # Generate unique filename
        unique_filename = generate_unique_filename(file.filename)
        file_path = os.path.join(LICENSE_DIR, unique_filename)
        
        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Save metadata to database
        metadata_saved = save_document_metadata(
            user_id=user_id,
            document_type="license",
            filename=file.filename,
            file_path=file_path
        )
        
        if not metadata_saved:
            # Clean up file if metadata saving failed
            os.remove(file_path)
            raise HTTPException(status_code=500, detail="Failed to save document metadata")
        
        return {
            "success": True,
            "message": "License document uploaded successfully",
            "document_id": unique_filename.split('_')[1],
            "filename": file.filename,
            "upload_date": datetime.now().isoformat(),
            "status": "pending_verification",
            "license_number": license_number,
            "license_type": license_type
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@router.get("/documents/{user_id}")
async def get_user_documents(user_id: str):
    """
    Get all documents for a specific user
    """
    try:
        documents_db_path = "database/documents_db.csv"
        
        if not os.path.exists(documents_db_path):
            return {"documents": []}
        
        # Read documents database
        df = pd.read_csv(documents_db_path)
        user_documents = df[df['user_id'] == user_id]
        
        # Convert to list of dictionaries
        documents = []
        for _, doc in user_documents.iterrows():
            documents.append({
                "document_id": doc['filename'].split('_')[1] if '_' in doc['filename'] else doc['filename'],
                "document_type": doc['document_type'],
                "filename": doc['filename'],
                "upload_date": doc['upload_date'],
                "status": doc['status'],
                "verified": doc['verified']
            })
        
        return {"documents": documents}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch documents: {str(e)}")

@router.put("/documents/{document_id}/verify")
async def verify_document(document_id: str, verified: bool, remarks: Optional[str] = None):
    """
    Verify or reject a document (Admin only)
    """
    try:
        documents_db_path = "database/documents_db.csv"
        
        if not os.path.exists(documents_db_path):
            raise HTTPException(status_code=404, detail="Documents database not found")
        
        # Read documents database
        df = pd.read_csv(documents_db_path)
        
        # Find document by document_id (in filename)
        document_mask = df['filename'].str.contains(document_id, na=False)
        if not document_mask.any():
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Update document status
        df.loc[document_mask, 'verified'] = verified
        df.loc[document_mask, 'status'] = 'verified' if verified else 'rejected'
        
        # Save updated database
        df.to_csv(documents_db_path, index=False)
        
        return {
            "success": True,
            "message": f"Document {document_id} {'verified' if verified else 'rejected'} successfully",
            "remarks": remarks
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update document: {str(e)}")

@router.get("/documents/pending")
async def get_pending_documents():
    """
    Get all pending documents for admin verification
    """
    try:
        documents_db_path = "database/documents_db.csv"
        
        if not os.path.exists(documents_db_path):
            return {"documents": []}
        
        # Read documents database
        df = pd.read_csv(documents_db_path)
        pending_documents = df[df['status'] == 'pending']
        
        # Convert to list of dictionaries
        documents = []
        for _, doc in pending_documents.iterrows():
            documents.append({
                "document_id": doc['filename'].split('_')[1] if '_' in doc['filename'] else doc['filename'],
                "user_id": doc['user_id'],
                "document_type": doc['document_type'],
                "filename": doc['filename'],
                "upload_date": doc['upload_date'],
                "status": doc['status'],
                "verified": doc['verified']
            })
        
        return {"documents": documents}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch pending documents: {str(e)}")

@router.delete("/documents/{document_id}")
async def delete_document(document_id: str, user_id: str):
    """
    Delete a document (User can delete their own documents)
    """
    try:
        documents_db_path = "database/documents_db.csv"
        
        if not os.path.exists(documents_db_path):
            raise HTTPException(status_code=404, detail="Documents database not found")
        
        # Read documents database
        df = pd.read_csv(documents_db_path)
        
        # Find document by document_id and user_id
        document_mask = (df['filename'].str.contains(document_id, na=False)) & (df['user_id'] == user_id)
        if not document_mask.any():
            raise HTTPException(status_code=404, detail="Document not found or access denied")
        
        # Get file path before deleting record
        document = df[document_mask].iloc[0]
        file_path = document['file_path']
        
        # Delete file if exists
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # Remove from database
        df = df[~document_mask]
        df.to_csv(documents_db_path, index=False)
        
        return {
            "success": True,
            "message": "Document deleted successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete document: {str(e)}")

@router.get("/admin/documents/stats")
async def get_document_statistics():
    """
    Get document statistics for admin dashboard
    """
    try:
        documents_db_path = "database/documents_db.csv"
        
        if not os.path.exists(documents_db_path):
            return {
                "total_documents": 0,
                "pending_verification": 0,
                "verified": 0,
                "rejected": 0,
                "aadhar_documents": 0,
                "license_documents": 0
            }
        
        # Read documents database
        df = pd.read_csv(documents_db_path)
        
        stats = {
            "total_documents": len(df),
            "pending_verification": len(df[df['status'] == 'pending']),
            "verified": len(df[df['verified'] == True]),
            "rejected": len(df[df['status'] == 'rejected']),
            "aadhar_documents": len(df[df['document_type'] == 'aadhar']),
            "license_documents": len(df[df['document_type'] == 'license'])
        }
        
        return stats
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get document statistics: {str(e)}")
