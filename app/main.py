"""FastAPI application providing endpoints and serving the CodeForge web application."""

import difflib
import os
from typing import Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.engine.analyzer import detect_language, diagnose_code, get_dsa_complexity_summary
from app.engine.repairer import repair_code
from app.engine.sandbox import execute_in_sandbox
from app.engine.translator import translate_all
from app.presets import PRESETS

app = FastAPI(title="CodeForge — Autonomous Multi-Language Code Repair & Polyglot Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CodePayload(BaseModel):
    filename: str = ""
    code: str
    language: str | None = None


class ExecutePayload(BaseModel):
    language: str
    code: str


@app.get("/api/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy", "service": "CodeForge Autonomous Engine"}


@app.get("/api/presets")
async def get_presets() -> list[dict[str, Any]]:
    """Returns available sample presets."""
    return PRESETS


@app.post("/api/detect")
async def api_detect_language(payload: CodePayload) -> dict[str, Any]:
    """Detects programming language from payload."""
    lang, confidence = detect_language(payload.filename, payload.code)
    return {"language": lang, "confidence": round(confidence, 2)}


@app.post("/api/analyze")
async def api_analyze_code(payload: CodePayload) -> dict[str, Any]:
    """Analyzes code and returns defect diagnosis."""
    lang = payload.language or detect_language(payload.filename, payload.code)[0]
    diagnoses = diagnose_code(payload.code, lang)
    dsa = get_dsa_complexity_summary(payload.code)
    return {
        "language": lang,
        "diagnoses": diagnoses,
        "dsa": dsa,
    }


@app.post("/api/execute")
async def api_execute_code(payload: ExecutePayload) -> dict[str, Any]:
    """Runs code in requested sandbox."""
    res = execute_in_sandbox(payload.language, payload.code)
    return res.to_dict()


@app.post("/api/process")
async def api_process_code(payload: CodePayload) -> dict[str, Any]:
    """Autonomous end-to-end processing pipeline: Triage -> Repair -> Execute -> Translate."""
    code = payload.code.strip()
    if not code:
        raise HTTPException(status_code=400, detail="Empty code payload supplied.")

    # 1. Detect language
    detected_lang, confidence = detect_language(payload.filename, code)
    lang = payload.language or detected_lang

    # 2. Diagnose defects
    diagnoses = diagnose_code(code, lang)
    dsa_summary = get_dsa_complexity_summary(code)

    # 3. Repair in original language
    fixed_code = repair_code(code, lang)

    # 4. Compute line diff
    orig_lines = code.splitlines(keepends=True)
    fixed_lines = fixed_code.splitlines(keepends=True)
    unified_diff = "".join(difflib.unified_diff(
        orig_lines,
        fixed_lines,
        fromfile=f"original/{payload.filename or 'source'}",
        tofile=f"repaired/{payload.filename or 'source'}",
    ))

    # 5. Execute repaired code in sandbox
    execution_result = execute_in_sandbox(lang, fixed_code)

    # 6. Polyglot translation across other skills
    polyglot_grid = translate_all(lang, fixed_code)

    return {
        "detected_language": lang,
        "confidence": round(confidence, 2),
        "diagnoses": diagnoses,
        "dsa_summary": dsa_summary,
        "fixed_code": fixed_code,
        "diff": unified_diff,
        "execution": execution_result.to_dict(),
        "polyglot_grid": polyglot_grid,
    }


# Mount static frontend
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.isdir(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
