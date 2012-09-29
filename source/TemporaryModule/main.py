import shutil
import random
import string

def temporary_module(original_module):
    """Generates a temporary module by copying its contents into a new folder and importing that.
    only works for relative import. 
    """
    copy_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(50))
    try:
        shutil.copytree(original_module, copy_name)
        return __import__(copy_name)
    finally:
        shutil.rmtree(copy_name, True)