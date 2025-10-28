## Quick context

- This is a very small Streamlit-based project. The interactive app lives in `app.py` and is a single-file Streamlit UI. A tiny helper script `main.py` currently only prints a greeting.
- No dependency manifest (requirements.txt / pyproject.toml) or tests were found in the repo root — Streamlit is used in `app.py`, so add a requirements file when you add dependencies.

## What an AI coding agent should know (short, actionable)

- Project purpose: a minimal demo/learning app for Children Data Analysis using Streamlit. Primary file to modify: `app.py`.
- Runtime: run the UI locally with the Streamlit CLI: `streamlit run app.py` (PowerShell or other shells). If deploying to Streamlit Cloud, push the repository and add a `requirements.txt` listing `streamlit`.
- Minimal conventions: keep UI code in `app.py`. New modules can be added under a top-level package (e.g., `src/` or `children_da/`) if the project grows; update `requirements.txt` accordingly.

## Editing patterns and examples

- To change the UI text/title, edit `app.py` — e.g. `st.title("Children Data Analysis")` and `st.write("...")`.
- To add a new route or page, prefer creating small helper modules and import them from `app.py` rather than stuffing everything into one file.

## Developer workflows (discovered / recommended)

- Run locally (assumes Streamlit installed):

  streamlit run app.py

- If dependencies are added, create `requirements.txt` with pinned versions (example: `streamlit==1.###`). The repo currently has no dependency manifest.
 - If dependencies are added, create `requirements.txt` with pinned versions (example: `streamlit==1.26.0`). The repo currently has no dependency manifest.

## Integration points & external dependencies

- Streamlit is the only external library referenced. There are no discovered integrations (databases, APIs, CI configs) in the repository as-is.

## Things to avoid / project-specific notes

- Don't assume a test suite or CI pipeline exists. If you add tests, include a minimal runner (e.g., `pytest`) and mention it in `README.md` and `requirements.txt`.
- Because the project is a single-file Streamlit app, prefer small, incremental refactors (extract helpers into modules) rather than large reorganizations without updating import paths.

## Where to look first (important files)

- `app.py` — primary Streamlit UI (title + write calls). Edit here for UI changes.
- `main.py` — trivial script printing a greeting; can be removed or repurposed.

---
If you'd like, I can (1) add a `requirements.txt` with `streamlit` pinned, (2) extract a small module scaffold (src/) and move logic out of `app.py`, or (3) expand these instructions with deployment notes for Streamlit Cloud. Which should I do next?
