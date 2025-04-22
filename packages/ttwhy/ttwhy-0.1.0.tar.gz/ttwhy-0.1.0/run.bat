@echo off
where uv >nul 2>nul
if %errorlevel% neq 0 (
  echo uv is not installed. Installing now...
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
)
uv lock
uv sync
uv run ttwhy
