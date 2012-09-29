import inspect, os


#Workaround for working-directory issues: Need to cd to directory where local packages are stored
#before executing the script, then change back when finished.
original_working_directory = os.getcwd()
try:
    os.chdir(os.path.dirname(inspect.getfile(inspect.currentframe())))
    import TemporaryModule
    rortools = TemporaryModule.temporary_module("rortools")
    rortools.RoRExporter.Exporter()
finally: 
    os.chdir(original_working_directory)
