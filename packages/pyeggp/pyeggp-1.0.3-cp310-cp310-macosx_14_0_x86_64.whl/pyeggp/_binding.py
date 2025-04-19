def __bootstrap__():
   global __bootstrap__, __file__, __loader__
   import sys, os, pkg_resources, importlib.util
   __file__ = pkg_resources.resource_filename(__name__,'_binding.cpython-310-darwin.so')
   del __bootstrap__
   if '__loader__' in globals():
       del __loader__

   old_dir = os.getcwd()
   try:
     os.chdir(os.path.dirname(__file__))

     spec = importlib.util.spec_from_file_location(
                __name__, __file__)
     mod = importlib.util.module_from_spec(spec)
     spec.loader.exec_module(mod)
   finally:

     os.chdir(old_dir)
__bootstrap__()
