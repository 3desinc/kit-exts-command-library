import omni.ext
import omni.ui as ui
import omni.kit.commands # New
import omni.usd # New
from typing import List # New

# Any class derived from `omni.ext.IExt` in top level module (defined in `python.modules` of `extension.toml`) will be
# instantiated when extension gets enabled and `on_startup(ext_id)` will be called. Later when extension gets disabled
# on_shutdown() is called.
class DliExampleCommand_libraryExtension(omni.ext.IExt):
    # ext_id is current extension id. It can be used with extension manager to query additional information, like where
    # this extension is located on filesystem.
    def on_startup(self, ext_id):
        print("[dli.example.command_library] MyExtension startup")

        self._window = ui.Window("My Window", width=300, height=300)
        with self._window.frame:
            with ui.VStack():
                ui.Label("Prim Scaler")

                def on_click():
                    prim_paths = get_selection()
                    omni.kit.commands.execute('ScaleIncrement', prim_paths=prim_paths)

                ui.Button("Scale up!", clicked_fn=lambda: on_click())

    def on_shutdown(self):
        print("[dli.example.command_library] MyExtension shutdown")
        self._window.destroy()
        self._window = None

class ScaleIncrement(omni.kit.commands.Command):
    def __init__(self, prim_paths: List[str]):
        self.prim_paths = prim_paths
        self.stage = omni.usd.get_context().get_stage()

    def do(self):
        self.set_scale(False)

    def undo(self):
        self.set_scale(True)

    def set_scale(self, undo: bool):
        for path in self.prim_paths:
            prim = self.stage.GetPrimAtPath(path)
            old_scale = prim.GetAttribute('xformOp:scale').Get()
            new_scale = tuple(x + 1 for x in old_scale)
            if undo:
                new_scale = tuple(x - 1 for x in old_scale)
            prim.GetAttribute('xformOp:scale').Set(new_scale)


def get_selection() -> List[str]:
    """Get the list of currently selected prims"""
    return omni.usd.get_context().get_selection().get_selected_prim_paths()