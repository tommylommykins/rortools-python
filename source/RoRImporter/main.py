import inspect, os

original_working_directory = os.getcwd()
try:
    os.chdir(os.path.dirname(inspect.getfile(inspect.currentframe())))
    ch
    import Importer; reload(Importer)
    Importer.Importer()
finally: pass

os.chdir(original_working_directory)


