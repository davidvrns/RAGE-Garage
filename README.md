# RAGE Garage

**RAGE Garage** is a Windows-first desktop studio for managing GTA V vehicle mods, with a primary workflow of converting Legacy/Gen8 vehicles to Enhanced/Gen9, visually inspecting assets, editing vehicle metadata through structured GUI forms, validating multi-car packs, and building an installable Enhanced DLC package.

## Product goals

RAGE Garage should let a user:

1. Create a vehicle-pack project.
2. Import one or many existing Legacy vehicle mods.
3. Inspect each vehicle and its metadata.
4. Convert supported binary assets from Gen8 to Gen9 through a replaceable asset backend.
5. View vehicles and textures in-app.
6. Edit `vehicles.meta`, `handling.meta`, `carvariations.meta`, and `carcols.meta` without hand-editing XML.
7. Detect and safely resolve pack-wide conflicts such as duplicate spawn names, handling IDs, modkit IDs, light IDs, and siren IDs.
8. Validate Enhanced compatibility.
9. Merge vehicle metadata and assets into one pack.
10. Build a final GTA V Enhanced DLC/mod package through a replaceable RPF backend.

## Proposed stack

- Python 3.12+
- PySide6 / Qt 6
- `lxml`
- Pydantic/dataclasses
- SQLite
- NumPy
- ModernGL
- `szio` / PyMateria behind an abstraction layer, subject to API and license verification
- multiprocessing for conversion workers
- pytest
- Nuitka / `pyside6-deploy`

## Codex

Codex should read `AGENTS.md` first, then `CODEX.md` and `ARCHITECTURE.md`.

The implementation target is a functional V1, not a UI mockup or scaffold. Run the application and tests, fix failures, and continue until the acceptance criteria in `CODEX.md` are satisfied or a genuinely external binary-format dependency blocks a feature. External blockers must be isolated behind an interface and documented precisely; do not fake successful conversion or RPF generation.

## Run target

```bash
python -m rage_garage
```

## Legal / compatibility note

RAGE Garage is intended as an independent mod-development utility. Do not bundle copyrighted GTA V assets. Use synthetic fixtures for automated tests. Third-party libraries must be reviewed for redistribution and integration terms before being bundled in releases.
