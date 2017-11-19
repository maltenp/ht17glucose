def find_module(modulename, filename=None):
    """Finds a python module or package on the standard path.
       If a filename is specified, add its containing folder
       to the system path.
 
       Returns a string of the full path to the module/package."""
    import imp
    import sys
    import os
 
    full_path = []
    if filename:
        full_path.append(os.path.dirname(os.path.abspath(filename)))
    full_path += sys.path
    fname = imp.find_module(modulename, full_path)
    return fname[1]