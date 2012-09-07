import inspect, os


#Workaround for working-directory issues: Need to cd to directory where local packages are stored
#before executing the script, then change back when finished.
original_working_directory = os.getcwd()
try:
    os.chdir(os.path.dirname(inspect.getfile(inspect.currentframe())))
    import RoRExporter; reload(RoRExporter)
    RoRExporter.Exporter.Exporter()
finally: pass

os.chdir(original_working_directory)
