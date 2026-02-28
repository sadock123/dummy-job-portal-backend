from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil

app = FastAPI()

# Allow your React app (running on localhost:5173) to talk to this API
# Allow your React app to talk to this API
app.add_middleware(
    CORSMiddleware,
    # CHANGE THIS LINE to your exact Vercel link (No slash at the end!)
    allow_origins=["https://dummy-job-portal-frontend.vercel.app"], 
    allow_credentials=False, # Changed to False for better compatibility
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create a folder to save uploaded resumes/cover letters for testing
UPLOAD_DIR = "uploaded_applications"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/api/apply")
async def submit_application(
    jobId: str = Form(...),
    resume: UploadFile = File(...),
    coverLetter: UploadFile = File(None) # Optional
):
    print(f"--- New Application Received for Job ID: {jobId} ---")
    print(f"Resume uploaded: {resume.filename}")
    
    # Save the resume to the upload folder
    resume_path = os.path.join(UPLOAD_DIR, resume.filename)
    with open(resume_path, "wb") as buffer:
        shutil.copyfileobj(resume.file, buffer)

    response_data = {
        "status": "success",
        "message": f"Application for Job {jobId} received successfully.",
        "resume_saved": resume.filename
    }

    # Handle the optional cover letter
    if coverLetter and coverLetter.filename:
        print(f"Cover letter uploaded: {coverLetter.filename}")
        cl_path = os.path.join(UPLOAD_DIR, coverLetter.filename)
        with open(cl_path, "wb") as buffer:
            shutil.copyfileobj(coverLetter.file, buffer)
        response_data["cover_letter_saved"] = coverLetter.filename
    
    print("--------------------------------------------------")
    
    return response_data

