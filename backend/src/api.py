from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .compiler import compile_and_run_source, CompilerError
from .errors import format_error
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# Get CORS origins from environment variable
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

# Add this after app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CompileRequest(BaseModel):
    source_code: str

class CompileResponse(BaseModel):
    assembly_code: list[str]
    program_output: str = None
    error: str = None

@app.post("/compile", response_model=CompileResponse)
async def compile_code(request: CompileRequest):
    try:
        result = compile_and_run_source(request.source_code)
        return CompileResponse(assembly_code=result['assembly_code'], program_output=result['program_output'])
    except CompilerError as e:
        formatted_error = format_error(e)
        return CompileResponse(assembly_code=[], program_output="", error=formatted_error)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    log_level = os.getenv("LOG_LEVEL", "info").lower()
    uvicorn.run(app, host="0.0.0.0", port=port, log_level=log_level) 