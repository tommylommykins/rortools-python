import inspect, os


#Workaround for working-directory issues: Need to cd to directory where local packages are stored
#before executing the script, then change back when finished.
original_working_directory = os.getcwd()
try:
    os.chdir(os.path.dirname(inspect.getfile(inspect.currentframe())))
    import rortools; reload(rortools)
    rortools.RoRImporter.Importer.Importer()
finally: pass

os.chdir(original_working_directory)