import importlib
import pkgutil

def load_all():
    from Rooms import secondaryRooms
    for pkg in (__package__, secondaryRooms.__name__): #select directory, --package__ does take the current directory
        path = importlib.import_module(pkg).__path__ #set directory
        for m in pkgutil.iter_modules(path):
            if not m.ispkg and m.name != "baseRoom":
                importlib.import_module(f"{pkg}.{m.name}")
    importlib.import_module("menu.startupMenu") #separte imports as not in rooms
    importlib.import_module("menu.endingScreen")