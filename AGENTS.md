# Codex Instructions for RAGE Garage

Read this file before making changes.

## Mission

Build **RAGE Garage**, a Windows-first desktop application for GTA V vehicle-pack workflows. The application must support multi-car projects, Legacy/Gen8 to Enhanced/Gen9 conversion through a replaceable backend, 3D and texture inspection, structured GUI editing of vehicle META files, cross-file and pack-wide validation, metadata compilation, and final mod/DLC packaging through a replaceable RPF backend.

## Non-negotiable rules

- Deliver working functionality, not a static mockup.
- Keep the UI independent from binary-format and RPF implementations.
- Never destroy or overwrite imported originals. Work on project copies and create backups before metadata writes.
- Do not regenerate META XML from a partial schema. Preserve unknown XML nodes, comments, and unsupported fields wherever practical.
- Do not fake Gen8→Gen9 conversion or RPF creation. If a reliable backend is unavailable, expose the limitation clearly and keep the interface ready for integration.
- Do not bundle copyrighted GTA V assets or proprietary third-party binaries unless their redistribution terms explicitly allow it.
- Use synthetic XML and asset metadata fixtures in automated tests.
- Optimize for projects with 100+ vehicles: lazy-load heavy models/textures and use isolated worker processes for conversion.
- Use type hints throughout new Python code.
- Add tests for every core service or validator added.
- Keep user-facing errors actionable and specific.
- Run tests after material changes and fix failures before stopping.

## Required reading

1. `CODEX.md` — product requirements and acceptance criteria.
2. `ARCHITECTURE.md` — module boundaries and design rules.
3. `README.md` — user-facing product intent.

## Preferred stack

- Python 3.12+
- PySide6
- lxml
- Pydantic/dataclasses
- NumPy
- ModernGL
- SQLite
- multiprocessing
- pytest
- optional szio/PyMateria backend after API/license verification
- Nuitka or pyside6-deploy for Windows distribution

## Definition of done for V1

At minimum:

- `python -m rage_garage` launches a usable desktop app.
- Create/open/save a `.gvsproject` project.
- Add multiple vehicle folders.
- Discover YFT/YTD and META files.
- Switch between vehicles.
- Edit the four primary META files with structured GUI forms plus raw XML view.
- Preserve unknown XML content on save.
- Validate cross-file references.
- Detect duplicate pack identifiers.
- Provide safe auto-fixes for selected conflicts.
- Expose conversion via an AssetBackend interface and run conversion jobs outside the UI thread.
- Provide a model-viewer framework and actual rendering for supported parsed scene data.
- Compile per-car metadata into pack-level files.
- Stage a complete DLC build tree including generated `content.xml` and `setup2.xml`.
- Expose RPF creation through an `RpfBackend` abstraction.
- Produce a build manifest and installation instructions.
- Tests pass.

If a third-party binary dependency prevents one binary feature from being implemented reliably, finish all unaffected V1 functionality and document the exact integration gap.
