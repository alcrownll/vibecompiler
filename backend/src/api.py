from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .compiler import compile_and_run_source, CompilerError
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add this after app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify ["http://localhost:5173"] for more security
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
        return CompileResponse(assembly_code=[], program_output="", error=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 