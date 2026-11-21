from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, validator
from typing import List, Dict
import re

app = FastAPI(title="CodeGuardAI", version="0.1.0")


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Simple health endpoint."""
    return {"status": "ok"}


class FileDiff(BaseModel):
    """A minimal representation of a file change in a PR."""
    filename: str = Field(..., description="Path of the changed file")
    added_lines: List[str] = Field(
        default_factory=list,
        description="Lines added in the diff (without the leading '+')",
    )
    removed_lines: List[str] = Field(
        default_factory=list,
        description="Lines removed in the diff (without the leading '-')",
    )

    @validator("filename")
    def must_be_python_or_js(cls, v):
        if not (v.endswith(".py") or v.endswith(".js") or v.endswith(".ts")):
            raise ValueError("Only .py, .js, .ts files are supported for demo")
        return v


class PRReviewRequest(BaseModel):
    """Payload representing a pull‑request diff."""
    title: str = Field(..., description="Title of the pull request")
    description: str = Field("", description="Optional description")
    files: List[FileDiff] = Field(..., description="Changed files in the PR")


class Issue(BaseModel):
    """Single issue found by the analysis."""
    file: str
    line: int
    severity: str
    message: str


class PRReviewResponse(BaseModel):
    """Result of the automated review."""
    pr_title: str
    issues: List[Issue]
    summary: str


def simple_security_scan(line: str) -> List[str]:
    """Detect very basic security patterns."""
    patterns = {
        "hardcoded_secret": r"(?i)api[_-]?key\s*=\s*['\"][A-Za-z0-9]{20,}['\"]",
        "sql_injection": r".*execute\(.+%s.+\)",
    }
    findings = []
    for name, pat in patterns.items():
        if re.search(pat, line):
            findings.append(name)
    return findings


def simple_style_check(line: str) -> List[str]:
    """Detect simple style problems."""
    issues = []
    if len(line) > 120:
        issues.append("line_too_long")
    if re.search(r"\bprint\(", line) and not line.strip().startswith("#"):
        issues.append("debug_print")
    return issues


@app.post("/review", response_model=PRReviewResponse)
async def review_pr(request: PRReviewRequest) -> PRReviewResponse:
    """
    Analyze a pull‑request diff and return a list of detected issues.
    This demo uses simple regex checks to illustrate the core idea.
    """
    issues: List[Issue] = []

    for file in request.files:
        for idx, line in enumerate(file.added_lines, start=1):
            # security checks
            sec_findings = simple_security_scan(line)
            for f in sec_findings:
                issues.append(
                    Issue(
                        file=file.filename,
                        line=idx,
                        severity="high",
                        message=f"Potential {f.replace('_', ' ')} detected",
                    )
                )
            # style checks
            style_findings = simple_style_check(line)
            for f in style_findings:
                issues.append(
                    Issue(
                        file=file.filename,
                        line=idx,
                        severity="low",
                        message=f"Style issue: {f.replace('_', ' ')}",
                    )
                )

    summary = (
        f"Analysis complete: {len(issues)} issue{'s' if len(issues)!=1 else ''} found."
    )
    return PRReviewResponse(pr_title=request.title, issues=issues, summary=summary)
