from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDockWidget,
    QLabel,
    QListWidget,
    QMainWindow,
    QStatusBar,
    QTabWidget,
    QToolBar,
    QWidget,
)


class MainWindow(QMainWindow):
    """Initial executable shell for RAGE Garage.

    Codex should replace this shell incrementally with the full project,
    viewer, metadata editor, validation, conversion, and build workflows
    described in CODEX.md while keeping the application runnable.
    """

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("RAGE Garage")
        self.resize(1440, 900)

        self._build_toolbar()
        self._build_vehicle_dock()
        self._build_properties_dock()
        self._build_center()
        self.setStatusBar(QStatusBar(self))
        self.statusBar().showMessage("Ready")

    def _build_toolbar(self) -> None:
        toolbar = QToolBar("Main", self)
        toolbar.setMovable(False)
        for label in (
            "New Project",
            "Open Project",
            "Add Vehicle",
            "Add Folder",
            "Convert Selected",
            "Convert All",
            "Validate Pack",
            "Build Mod",
        ):
            toolbar.addAction(label)
        self.addToolBar(toolbar)

    def _build_vehicle_dock(self) -> None:
        dock = QDockWidget("Vehicles", self)
        dock.setObjectName("vehiclesDock")
        vehicle_list = QListWidget(dock)
        vehicle_list.addItem("No vehicles imported")
        dock.setWidget(vehicle_list)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, dock)

    def _build_properties_dock(self) -> None:
        dock = QDockWidget("Properties", self)
        dock.setObjectName("propertiesDock")
        dock.setWidget(QLabel("Select a vehicle to inspect its properties.", dock))
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)

    def _build_center(self) -> None:
        tabs = QTabWidget(self)
        tabs.addTab(self._placeholder("3D viewer"), "Viewer")
        tabs.addTab(self._placeholder("vehicles.meta editor"), "Vehicle")
        tabs.addTab(self._placeholder("handling.meta editor"), "Handling")
        tabs.addTab(self._placeholder("carvariations.meta editor"), "Variations")
        tabs.addTab(self._placeholder("carcols.meta editor"), "Carcols")
        tabs.addTab(self._placeholder("Texture inspection"), "Textures")
        tabs.addTab(self._placeholder("Pack diagnostics"), "Validation")
        tabs.addTab(self._placeholder("Build pipeline"), "Build")
        self.setCentralWidget(tabs)

    @staticmethod
    def _placeholder(text: str) -> QWidget:
        label = QLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return label
