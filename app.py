from fastapi import FastAPI
from dotenv import load_dotenv
from routers import extractors


# Load environment variables
load_dotenv()


# Initialize FastAPI app with documentation
app = FastAPI(
    title="Document Extraction API",
    description="API for extracting text from various document formats and processing data",
    version="1.0.0",
)


# Register the extractors router
app.include_router(extractors.router)