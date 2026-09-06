# RAGE Garage — Master Build Specification

## Product

Build a Windows-first desktop application called **RAGE Garage**.

RAGE Garage is an IDE/build system for GTA V vehicle mods. Its primary workflow is importing one or many existing Legacy/Gen8 vehicles, converting supported assets to Enhanced/Gen9, visually inspecting assets, editing metadata through structured GUI forms, validating cross-car references/conflicts, and building one installable multi-car Enhanced DLC/mod package.

## Technology

Use:

- Python 3.12+
- PySide6 / Qt 6
- lxml
- Pydantic and/or dataclasses
- SQLite
- NumPy
- ModernGL
- multiprocessing for isolated conversion jobs
- pytest
- Nuitka or pyside6-deploy

Integrate `szio` / PyMateria only behind an abstract backend and only after confirming the current API and licensing/redistribution terms. The application must remain functional without that optional dependency by exposing a clear unavailable-backend state rather than faking conversion.

## Core user workflow

1. Create/open a project.
2. Add one or many vehicle mods.
3. Inspect discovered assets and metadata.
4. Convert selected/all supported Gen8 assets to Gen9.
5. View vehicle and texture information.
6. Edit metadata through forms.
7. Validate each vehicle and the pack.
8. Auto-fix safe namespace/ID conflicts.
9. Compile all vehicle metadata.
10. Build a GTA V Enhanced DLC/mod package.

## 1. Project system

- Create/open/save `.gvsproject` files.
- One project represents one vehicle pack.
- One project can contain many vehicles.
- Preserve imported originals.
- Maintain working copies, cache, backups, logs, and builds separately.
- Autosave recoverable project state.
- Store lightweight project metadata in JSON and/or SQLite; do not store binary GTA assets in SQLite.

Suggested project layout:

```text
ProjectName/
├── ProjectName.gvsproject
├── vehicles/
│   ├── vehicle_001/
│   └── vehicle_002/
├── cache/
├── backups/
├── logs/
└── builds/
```

## 2. Vehicle importer

Support importing:

- an extracted DLC folder
- a folder containing loose vehicle assets and metadata
- multiple vehicle folders at once
- recursively discovered vehicle mods where practical

Detect and classify:

- `*.yft`
- `*_hi.yft`
- `*.ytd`
- optional `.ydr`, `.ydd`, `.ybn`
- `vehicles.meta`
- `handling.meta`
- `carvariations.meta`
- `carcols.meta`
- optional `vehiclelayouts.meta`
- optional tuning/mod assets
- optional audio-related assets

Create a `VehicleRecord` with lightweight metadata. Heavy assets must be lazily loaded.

## 3. Multi-car project management

The main window must include:

- vehicle list/tree
- Add Vehicle
- Add Folder
- Convert Selected
- Convert All
- Validate Pack
- Build Mod

Support multi-select for conversion/validation operations.

## 4. Asset backend abstraction

Define a replaceable interface similar to:

```python
class AssetBackend(Protocol):
    def available(self) -> bool: ...
    def supports(self, path: Path) -> bool: ...
    def inspect(self, path: Path) -> AssetInfo: ...
    def load_scene(self, path: Path) -> SceneModel: ...
    def convert(self, source: Path, target_generation: str, output: Path) -> ConversionResult: ...
```

Implement a placeholder-disabled backend state if no compliant Gen8/Gen9 implementation is installed. Do not emulate or claim successful binary conversion without real output.

If current `szio` / PyMateria APIs and terms permit, implement a backend for:

- Gen8/Legacy input
- Gen9/Enhanced output
- supported YFT/YTD/YDR/YDD/YBN formats

Run native conversion in isolated worker processes.

## 5. Conversion UX

Support:

- one vehicle
- selected vehicles
- whole pack
- progress reporting
- cancellation
- detailed per-file logs
- conversion report
- file-hash caching to skip unchanged assets

A conversion result must distinguish:

- converted
- skipped/cached
- unsupported
- warning
- failed

## 6. 3D model viewer

Use Qt + ModernGL.

Do not couple rendering directly to szio/PyMateria types. Define an intermediate scene model:

```python
@dataclass
class SceneModel:
    meshes: list[Mesh]
    materials: list[Material]
    textures: list[TextureRef]
    skeleton: Skeleton | None
```

Viewer features:

- orbit
- pan
- zoom
- reset camera
- solid
- textured
- wireframe
- normals overlay
- skeleton overlay
- bounding boxes
- LOD selection

Display statistics where available:

- generation
- vertices
- triangles
- materials
- geometries
- bones
- textures
- file sizes

If no binary parser backend is installed, the viewer must show a clear unsupported/unavailable state rather than crash.

## 7. Texture viewer

For supported YTD inspection display:

- texture name
- dimensions
- format
- mip count

Add Enhanced-oriented validation hooks including detection of `script_rt_*` texture names and format warnings where rules are known and documented.

## 8. META/XML editing principles

Primary files:

- `vehicles.meta`
- `handling.meta`
- `carvariations.meta`
- `carcols.meta`

Use `lxml`.

Do not rebuild XML from an incomplete typed schema. Retain the original XML DOM and modify targeted nodes.

Preserve wherever practical:

- unknown elements
- comments
- unsupported fields
- ordering

Each metadata editor needs:

- structured Form view
- Raw XML view
- Changes/Diff view
- search
- undo/redo
- save/revert

Back up working metadata before writes.

## 9. vehicles.meta editor

Provide structured controls for at least:

- modelName
- txdName
- handlingId
- gameName
- vehicleMakeName
- audioNameHash
- layout
- type
- vehicleClass
- wheelType
- plateType
- dashboardType where present
- flags
- advanced/unknown fields via XML view

Organize into tabs such as General, Assets, Audio, Layout, Type/Class, Flags, Advanced.

## 10. handling.meta editor

Support common `CHandlingData` fields with correct numeric controls.

Tabs:

- General
- Mass/Drag
- Drivetrain
- Transmission
- Brakes
- Steering
- Traction
- Suspension
- Damage
- Advanced

Include at least:

- handlingName
- fMass
- fInitialDragCoeff
- vecCentreOfMassOffset
- fDriveBiasFront
- nInitialDriveGears
- fInitialDriveForce
- fDriveInertia
- fInitialDriveMaxFlatVel
- fBrakeForce
- fBrakeBiasFront
- fHandBrakeForce
- fSteeringLock
- fTractionCurveMax
- fTractionCurveMin
- fTractionCurveLateral
- fTractionBiasFront
- fSuspensionForce
- fSuspensionCompDamp
- fSuspensionReboundDamp
- fSuspensionUpperLimit
- fSuspensionLowerLimit
- fSuspensionRaise
- fSuspensionBiasFront
- fAntiRollBarForce
- fAntiRollBarBiasFront
- common damage multipliers

## 11. carvariations.meta editor

Tabs:

- General
- Colors
- Liveries
- Kits
- Lights
- Sirens
- Plates

Support at least:

- modelName
- colors/indices
- liveries
- kits
- plate probabilities
- lightSettings
- sirenSettings

## 12. carcols.meta editor

Tabs:

- Modkits
- Visible Mods
- Stat Mods
- Liveries
- Lights
- Sirens

Support at least:

- kitName
- modkit id
- kitType
- visibleMods
- linkMods
- statMods
- livery-related names where present
- light IDs/settings structures
- siren IDs/settings structures

## 13. Cross-file validation

Understand and validate relationships including:

```text
vehicles.meta:modelName -> YFT
vehicles.meta:txdName -> YTD
vehicles.meta:handlingId -> handling.meta:handlingName
carvariations.meta:modelName -> vehicles.meta:modelName
carvariations.meta:kits -> carcols.meta:kitName
carvariations.meta:lightSettings -> carcols light ID
carvariations.meta:sirenSettings -> carcols siren ID
```

Diagnostics must have severity:

- INFO
- WARNING
- ERROR

Diagnostics must be clickable where possible and navigate to the relevant editor/field.

Provide safe automatic fixes for straightforward broken references.

## 14. Pack registry and conflict detection

Track globally:

- model/spawn names
- handling names
- modkit names
- modkit IDs
- light IDs
- siren IDs

Detect:

- duplicate spawn names
- duplicate handling IDs/names
- duplicate modkit IDs
- duplicate modkit names where problematic
- duplicate light IDs
- duplicate siren IDs

Create a central allocator/registry. Renaming an identifier through a safe fix must update dependent references atomically.

Target platform must be explicit:

- GTA V Legacy single-player
- GTA V Enhanced single-player
- optional FiveM later

Do not apply FiveM-specific ID assumptions to Enhanced single-player.

## 15. Enhanced compatibility validation

Per vehicle display where information is available:

- Gen8/Gen9 status
- missing YFT
- missing `_hi.yft`
- missing YTD
- missing primary metadata
- geometry/material counts
- texture warnings
- unresolved metadata references
- duplicate namespace/ID conflicts
- conversion failures

Overall vehicle status:

- READY
- WARNING
- ERROR

Overall pack status must aggregate individual vehicles plus cross-pack conflicts.

## 16. Metadata compiler

Keep per-vehicle metadata separate while editing.

During build, compile all entries into pack-level metadata files:

- vehicles.meta
- handling.meta
- carvariations.meta
- carcols.meta
- vehiclelayouts.meta when applicable

Do not concatenate XML strings.

Pipeline:

```text
parse -> validate -> clone/merge relevant nodes -> validate -> serialize
```

Create dedicated compiler classes per metadata type.

## 17. DLC/build system

Implement a deterministic build pipeline:

1. validate project
2. verify required target-generation assets
3. resolve/update references
4. compile metadata
5. generate `content.xml`
6. generate `setup2.xml`
7. stage vehicle assets
8. stage tuning assets
9. create nested archive plan
10. create final DLC archive if an RPF backend is available
11. validate build output
12. generate build manifest
13. generate installation instructions

## 18. RPF backend abstraction

Define:

```python
class RpfBackend(Protocol):
    def available(self) -> bool: ...
    def create_archive(self, path: Path): ...
    def add_file(self, archive, source: Path, target_path: str): ...
    def add_bytes(self, archive, data: bytes, target_path: str): ...
    def finalize(self, archive): ...
```

Always provide a filesystem staging backend that builds the full intended DLC tree.

If a reliable legal RPF writer is not available, Build must stop before falsely claiming `dlc.rpf` success. The UI should clearly state that staging succeeded and final RPF generation requires a configured backend.

## 19. Target staging layout

Support an output conceptually similar to:

```text
packname/
├── common/
│   └── data/
│       ├── vehicles.meta
│       ├── handling.meta
│       ├── carcols.meta
│       ├── carvariations.meta
│       └── optional vehiclelayouts.meta
├── x64/
│   ├── vehicles.rpf/ or staged equivalent
│   └── vehiclemods/ or staged equivalent
├── content.xml
└── setup2.xml
```

Exact archive details should be handled by the RPF backend and documented/tested.

## 20. Build manifest

Generate JSON containing:

- pack name
- project name
- version
- target
- application version
- UTC build timestamp
- vehicles/spawn names
- source and output hashes where practical
- validation summary
- conversion summary
- backend versions

## 21. Optional installer architecture

Build Mod must never modify a GTA installation.

A separate installer module may later:

- detect GTA V Enhanced
- copy a built DLC to the user's mods environment
- update the mod-side `dlclist.xml`
- create backups
- uninstall only assets/entries owned by RAGE Garage

Keep installer operations explicit and reversible.

## 22. UI design

Create a professional desktop IDE-style UI.

Suggested layout:

```text
+---------------------------------------------------------------+
| RAGE Garage                              [VALIDATE] [BUILD]    |
+----------------+---------------------------+------------------+
| VEHICLES       |                           | PROPERTIES       |
|                |       3D VIEWER           |                  |
| Supra          |                           | Spawn            |
| Skyline        |                           | Generation       |
| Huracan        |                           | Handling         |
|                |                           | Modkit           |
| + Add Vehicle  |                           |                  |
+----------------+---------------------------+------------------+
| Vehicle | Handling | Variations | Carcols | Textures | Build |
+---------------------------------------------------------------+
| Pack diagnostics / status                                    |
+---------------------------------------------------------------+
```

Use proper Qt model/view patterns rather than manually rebuilding large widget trees for every list/table update.

## 23. Performance

Design for 100+ vehicles.

- lazy-load binary assets
- keep lightweight `VehicleRecord`s
- use hashing and build caches
- use worker processes for conversion
- avoid blocking the Qt UI thread
- cap conversion concurrency

## 24. Reliability

Implement:

- logging
- user-facing diagnostics
- autosave/recovery
- backup before metadata save
- malformed XML handling
- missing asset handling
- failed conversion isolation
- cancellation where practical
- safe atomic writes for project/config files

## 25. Testing

Add unit/integration tests for at least:

- project serialization
- vehicle discovery
- META parsing
- preservation of unknown XML nodes/comments
- field edits
- undo/revert logic where testable
- handling reference validation
- model/txd reference validation
- modkit conflict detection
- ID allocation
- safe rename propagation
- metadata merging
- `content.xml` generation
- `setup2.xml` generation
- build manifest generation
- staging backend output
- AssetBackend interface behavior
- RpfBackend interface behavior

Use synthetic fixtures. Do not commit Rockstar/GTA game assets.

## 26. Documentation

Maintain:

- README.md
- AGENTS.md
- CODEX.md
- ARCHITECTURE.md
- DEVELOPMENT.md

Document optional binary backend setup separately from core app installation.

## 27. Required run target

The development application must launch with:

```bash
python -m rage_garage
```

## 28. V1 acceptance criteria

V1 is accepted when:

- the application launches successfully
- a project can be created/opened/saved
- multiple vehicle folders can be imported
- the vehicle list and selection work
- primary assets/meta files are discovered
- all four primary META files have structured editors plus raw XML
- edits persist while unknown XML content is preserved
- undo/revert works for metadata edits at a useful level
- cross-file references are validated
- pack-level duplicates are detected
- safe conflict auto-fixes work
- AssetBackend exists and conversion jobs do not block the UI
- supported SceneModel data renders in the viewer
- metadata compiles into pack-level files
- a complete Enhanced-oriented staging tree is produced
- `content.xml`, `setup2.xml`, build manifest, and installation instructions are generated
- RPF generation either works via a verified backend or is explicitly reported as unavailable without pretending success
- tests pass

## 29. Codex execution rule

Do not stop after scaffolding. Implement vertical slices that are executable. Run the app, run tests, inspect failures, fix them, and continue toward the acceptance criteria. If one external binary-format integration is blocked, document it and continue implementing all independent functionality.
