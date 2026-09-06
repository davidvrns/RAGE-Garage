# RAGE Garage Architecture

## Design goals

RAGE Garage should remain maintainable even if the GTA binary-conversion or RPF-writing technology changes. The UI must depend on application services and internal models, never directly on third-party binary libraries.

## Core layers

```text
PySide6 UI
   |
Application services
   |
+-- Project / pack domain
+-- META/XML domain
+-- Validation / registry
+-- Conversion service
+-- Build/compiler service
+-- Viewer scene service
   |
Backend interfaces
   |
+-- AssetBackend
+-- RpfBackend
+-- RenderBackend (optional abstraction)
```

## Package layout

```text
rage_garage/
├── __init__.py
├── __main__.py
├── app.py
├── ui/
│   ├── main_window.py
│   ├── project_tree.py
│   ├── diagnostics.py
│   ├── editors/
│   │   ├── vehicles_editor.py
│   │   ├── handling_editor.py
│   │   ├── carvariations_editor.py
│   │   └── carcols_editor.py
│   ├── viewer/
│   └── build/
├── project/
│   ├── models.py
│   ├── project_file.py
│   ├── importer.py
│   └── autosave.py
├── meta/
│   ├── document.py
│   ├── vehicles.py
│   ├── handling.py
│   ├── carvariations.py
│   ├── carcols.py
│   └── diff.py
├── registry/
│   ├── pack_registry.py
│   └── allocator.py
├── validation/
│   ├── models.py
│   ├── references.py
│   ├── conflicts.py
│   └── enhanced.py
├── assets/
│   ├── models.py
│   ├── backend.py
│   ├── null_backend.py
│   └── pymateria_backend.py
├── renderer/
│   ├── scene.py
│   ├── camera.py
│   ├── renderer.py
│   └── shaders/
├── conversion/
│   ├── service.py
│   ├── workers.py
│   └── cache.py
├── compiler/
│   ├── vehicles.py
│   ├── handling.py
│   ├── carvariations.py
│   ├── carcols.py
│   └── vehiclelayouts.py
├── build/
│   ├── service.py
│   ├── content_xml.py
│   ├── setup2_xml.py
│   ├── manifest.py
│   ├── staging.py
│   ├── rpf_backend.py
│   └── installer.py
└── util/
    ├── hashing.py
    ├── atomic.py
    └── logging.py
```

## Domain objects

### `PackProject`

Owns project-level state:

- project metadata
- target platform/generation
- list of `VehicleRecord`
- build settings
- validation state
- cache paths

### `VehicleRecord`

Lightweight. Store:

- stable UUID
- source/original path
- working path
- spawn/model name when known
- paths to discovered assets
- paths to metadata
- summary conversion state
- summary validation state

Do not eagerly load model geometry or texture payloads.

### `VehicleProject`

Loaded-on-demand richer object for a selected vehicle. It can expose parsed metadata documents, asset inspection data, and viewer scene information.

## META editing

`MetaDocument` must wrap the original `lxml` tree. Typed adapters may expose known fields, but the XML tree remains the source of truth.

```text
Original XML DOM
      |
Known-field adapter
      |
Qt form widgets
```

A form edit should target an existing XML node or safely create a known node. Unknown nodes must remain untouched.

All metadata writes should use atomic temp-file replacement and write a timestamped project backup first.

## Validation

Use a normalized diagnostic object:

```python
@dataclass
class Diagnostic:
    severity: Severity
    code: str
    message: str
    vehicle_id: str | None
    file_kind: str | None
    xml_path: str | None
    fix_id: str | None
```

Validators should be pure or mostly pure functions over domain data wherever possible.

## Pack registry

`PackRegistry` builds indexes for:

- model/spawn names
- handling names
- modkit names
- modkit IDs
- light IDs
- siren IDs

Conflict detection and ID allocation belong here, not in Qt widgets.

## Conversion

`ConversionService` orchestrates jobs and cache behavior.

The backend interface owns binary-format details. Workers must be process-isolated for native libraries where practical.

Never expose PyMateria/szio objects to UI code.

## Renderer

The renderer consumes only `SceneModel`, `Mesh`, `Material`, `TextureRef`, and optional `Skeleton` internal models. Asset backends translate their parsed representation into this neutral format.

## Compiler/build

Editing uses per-vehicle metadata. Build uses compiler modules to merge relevant XML entries into pack-level files.

The build service produces an explicit staging directory before any RPF work. This makes the build testable even when no RPF backend is configured.

```text
Project
  -> validate
  -> compile metadata
  -> stage assets
  -> generate content/setup XML
  -> generate manifest
  -> optional RPF backend
```

## Dependency direction

Allowed:

```text
ui -> services -> domain/backends
```

Forbidden:

```text
meta -> ui
validation -> ui
assets/backend -> ui
build -> ui
```

Qt signals or application-service callbacks should bridge long-running operations to the UI.

## External dependencies

Third-party libraries with unclear or restrictive redistribution terms must remain optional and documented. Do not copy source from projects whose license does not clearly permit reuse.

## Testing strategy

Core project/meta/validation/compiler/build logic must be testable without launching Qt and without real GTA assets. Use synthetic XML and fake backends.

Viewer tests can cover scene conversion and math separately from an actual OpenGL context where practical.
