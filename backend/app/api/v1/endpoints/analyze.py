"""
Analysis Endpoints
Code and diagram security analysis endpoints
"""

import structlog
from fastapi import APIRouter, File, UploadFile, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.core.config import settings
from app.schemas.analysis import (
    CodeAnalysisRequest,
    CodeAnalysisResponse,
    DiagramAnalysisResponse
)
from app.services.code_analyzer import CodeAnalyzerService
from app.services.diagram_analyzer import DiagramAnalyzerService

logger = structlog.get_logger(__name__)
router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post("/code", response_model=CodeAnalysisResponse)
@limiter.limit(settings.ANALYSIS_RATE_LIMIT)
async def analyze_code(request: CodeAnalysisRequest):
    """
    Analyze code for security vulnerabilities

    This endpoint performs comprehensive security analysis including:
    - OWASP Top 10 vulnerabilities
    - CWE Top 25 weaknesses
    - Secret detection
    - Dependency vulnerabilities
    - Code quality issues

    **Rate Limit:** 10 requests per hour
    """
    try:
        logger.info(
            "Code analysis requested",
            language=request.language,
            code_length=len(request.code)
        )

        # Validate code length
        lines = request.code.count('\n') + 1
        if lines > settings.CODE_MAX_LINES:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"Code exceeds maximum {settings.CODE_MAX_LINES} lines"
            )

        # Perform analysis
        analyzer = CodeAnalyzerService()
        result = await analyzer.analyze(
            code=request.code,
            language=request.language,
            filename=request.filename
        )

        logger.info(
            "Code analysis completed",
            vulnerabilities=len(result.get("vulnerabilities", [])),
            severity_summary=result.get("summary")
        )

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Code analysis failed", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )


@router.post("/diagram", response_model=DiagramAnalysisResponse)
@limiter.limit(settings.ANALYSIS_RATE_LIMIT)
async def analyze_diagram(file: UploadFile = File(...)):
    """
    Analyze architecture diagram for security issues

    Accepts PNG, JPG, or SVG diagrams and provides:
    - Component identification
    - Security assessment
    - Zero Trust recommendations
    - Secure-by-Design proposals
    - Compliance gaps

    **Rate Limit:** 10 requests per hour
    **Max File Size:** 50MB
    """
    try:
        logger.info(
            "Diagram analysis requested",
            filename=file.filename,
            content_type=file.content_type
        )

        # Validate file type
        if file.content_type not in settings.ALLOWED_IMAGE_TYPES:
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail=f"Unsupported file type: {file.content_type}"
            )

        # Read file
        file_content = await file.read()

        # Validate file size
        if len(file_content) > settings.MAX_UPLOAD_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File size exceeds maximum {settings.MAX_UPLOAD_SIZE} bytes"
            )

        # Perform analysis
        analyzer = DiagramAnalyzerService()
        result = await analyzer.analyze(
            file_content=file_content,
            filename=file.filename,
            content_type=file.content_type
        )

        logger.info(
            "Diagram analysis completed",
            components=len(result.get("components", [])),
            weaknesses=len(result.get("weaknesses", []))
        )

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Diagram analysis failed", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )


@router.get("/status/{analysis_id}")
async def get_analysis_status(analysis_id: str):
    """
    Get status of an ongoing analysis

    For long-running analyses, this endpoint provides progress updates
    """
    # TODO: Implement analysis status tracking
    return {
        "analysis_id": analysis_id,
        "status": "completed",
        "progress": 100
    }
