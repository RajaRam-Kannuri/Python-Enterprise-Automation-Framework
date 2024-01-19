from enum import StrEnum

from pydantic import BaseModel


class ScriptType(StrEnum):
    PYTHON = "python"
    BASH = "bash"
    POWERSHELL = "powershell"
    DESKTOP = "desktop"


class ScriptProjectInput(BaseModel):
    name: str
    description: str | None
    type: ScriptType
    metadata: dict = {}
    cmdargs: str | None


class ScriptProject(ScriptProjectInput):
    id: int
    children: list
    created_at: str
    updated_at: str
