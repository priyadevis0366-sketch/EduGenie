from pathlib import Path

from fastapi import (
    FastAPI,
    Request,
    HTTPException
)

from fastapi.responses import (
    HTMLResponse,
    JSONResponse
)

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel, Field

from config import validate_config

from qna import answer_question
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import (
    get_learning_recommendations
)


BASE_DIR = Path(__file__).resolve().parent


app = FastAPI(
    title="EduGenie",
    description=(
        "Google Gemini Powered Learning Assistant"
    ),
    version="1.0.0"
)


app.mount(
    "/static",
    StaticFiles(
        directory=BASE_DIR / "static"
    ),
    name="static"
)


templates = Jinja2Templates(
    directory=BASE_DIR / "templates"
)


# --------------------------------------------------
# Request Models
# --------------------------------------------------

class TextRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=20000
    )


class LearningRequest(BaseModel):
    topic: str = Field(
        ...,
        min_length=1,
        max_length=1000
    )

    level: str = Field(
        default="Beginner",
        max_length=100
    )


# --------------------------------------------------
# Frontend
# --------------------------------------------------

@app.get(
    "/",
    response_class=HTMLResponse
)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


# --------------------------------------------------
# Health Check
# --------------------------------------------------

@app.get("/health")
async def health():

    valid, message = validate_config()

    return {
        "status": "ok" if valid else "warning",
        "gemini_configured": valid,
        "message": message
    }


# --------------------------------------------------
# Q&A
# --------------------------------------------------

@app.post("/qa")
async def qa(request: TextRequest):

    try:

        result = answer_question(
            request.text
        )

        return {
            "success": True,
            "result": result
        }

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )


# --------------------------------------------------
# Explanation
# --------------------------------------------------

@app.post("/explain")
async def explain(request: TextRequest):

    try:

        result = explain_topic(
            request.text
        )

        return {
            "success": True,
            "result": result
        }

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )


# --------------------------------------------------
# Quiz
# --------------------------------------------------

@app.post("/quiz")
async def quiz(request: TextRequest):

    try:

        questions = generate_quiz(
            request.text
        )

        return {
            "success": True,
            "questions": questions
        }

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )


# --------------------------------------------------
# Summarization
# --------------------------------------------------

@app.post("/summarize")
async def summarize(request: TextRequest):

    try:

        result = summarize_text(
            request.text
        )

        return {
            "success": True,
            "result": result
        }

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )


# --------------------------------------------------
# Learning Path
# --------------------------------------------------

@app.post("/learn/recommendations")
async def learning_recommendations(
    request: LearningRequest
):

    try:

        result = get_learning_recommendations(
            request.topic,
            request.level
        )

        return {
            "success": True,
            "result": result
        }

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )


# --------------------------------------------------
# Global Exception Handler
# --------------------------------------------------

@app.exception_handler(Exception)
async def general_exception_handler(
    request: Request,
    exc: Exception
):

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": str(exc)
        }
    )