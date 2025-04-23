# This file is part of mesibo PatANN Python SDK for various platforms.
#         
# By accessing and utilizing this work, you hereby acknowledge that you have thoroughly 
# reviewed, comprehended, and commit to adhering to the terms and conditions stipulated 
# on the mesibo website, thereby entering into a legally binding agreement.
# 
# https://patann.dev
# https://mesibo.com
#
# Copyright (c) 2019-Present Mesibo Inc, San Francisco, United States
# All rights reserved.
#  

"""
Pattern-Aware Approximate Nearest Neighbor (PatANN) search library interface

PatANN is a massively parallel, distributed, and scalable vector database library
for efficient nearest neighbor search across large-scale datasets by finding vector patterns.

PatANN leverages pattern probing for searching which is a fundamental shift from conventional
vector search methodologies. Pattern probing is a preliminary filtering mechanism that examines
vector patterns before applying computationally expensive distance metrics. This two-phase
approach significantly reduces the search space by quickly identifying potential matches
based on pattern similarity rather than calculating exact distances.

Supported platforms:
- Linux (x86_64 and ARM)
- MacOS (Apple Silicon M series)
- Windows
- Android
- iOS

Websites:
- https://patann.dev
- https://github.com/mesibo/patann

For support/questions, please contact: support@mesibo.com

"""



__patann_version__ = '0.1.1'


import ctypes
import platform
import multiprocessing
import sys
import os
import warnings
import inspect
import filecmp
import numpy as np
import shutil

def system_exit_error(err):
    info = "\nSystem: " + platform.system().lower() +  "\nPlatform: " + platform.machine() + "\nVersion: " + get_version_folder() + "\n" + "patann: " + __patann_version__;
    raise SystemExit(info + "\n\n==> Error: " + err + "\n")

def get_version_folder():
    return platform.python_version_tuple()[0] + "." + platform.python_version_tuple()[1]

def get_system():
    system = platform.system().lower()
    if("" == system):
        system = "unknown"

    if("cygwin" in system):
        system = "windows"

    if("darwin" in system):
        system = "macos"

    return system

def get_platform_folder():
    system = get_system()

    machine = platform.machine()
    if("" == machine):
        machine = "unknown"

    if(machine.lower() == "amd64"):
        machine = "x86_64"

    return os.path.join(system.lower(), machine.lower())

def get_patann_lib():
    system = get_system()
    lib = "libpatann.so"
    if(system == "windows"):
        lib = "patann.dll"
    return lib

def get_pypatann_lib():
    system = get_system()
    lib = "_patann.so"
    if(system == "windows"):
        lib = "_patann.pyd"
    system = platform.system().lower()
    if("cygwin" in system):
        lib = "_patann.dll"
    return lib

def get_pypatann_checksum():
    return "_patann.sum"

CLIB_DIR = "clib"
def get_full_path_to_lib():
    package_dir = os.path.dirname(os.path.realpath(__file__))
    clib_dir = os.path.join(package_dir, CLIB_DIR)
    platform_lib = get_platform_folder()
    lib_path = os.path.join(clib_dir, platform_lib)
    return lib_path

def get_pypatann_path():
    path = get_full_path_to_lib()
    path = os.path.join(path, get_version_folder())
    return path

def set_path_to_lib():
    sys.path.append(get_pypatann_path());

def get_patann_lib_path():
    path = get_full_path_to_lib()
    return os.path.join(path, get_patann_lib())

def get_pypatann_lib_path():
    path = get_pypatann_path()
    return os.path.join(path, get_pypatann_lib())

def get_python_lib_path():
    package_dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(package_dir, get_pypatann_lib())

def get_pypatann_checksum_path():
    path = get_pypatann_path()
    return os.path.join(path, get_pypatann_checksum())

def get_python_checksum_path():
    package_dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(package_dir, get_pypatann_checksum())

def excepthook(type, value, traceback):
    print(value)

def is_installed():
    if not os.path.exists(get_pypatann_checksum_path()):
        return False
    if not os.path.exists(get_pypatann_lib_path()):
        return False
    return True

def is_copied():
    if not os.path.exists(get_python_lib_path()):
        return False

    pypath = get_python_checksum_path()
    patannpath = get_pypatann_checksum_path()
    if not os.path.exists(pypath):
        return False

    try:
        filecmp.clear_cache()
        return filecmp.cmp(pypath, patannpath, False)
    except Exception:
        return False

def copy_files():
    if(is_copied()):
        return

    pypath = get_python_checksum_path()
    patannpath = get_pypatann_checksum_path()

    import shutil
    try:
        shutil.copy2(patannpath, pypath)
        pypath = get_python_lib_path()
        patannpath = get_pypatann_lib_path()
        shutil.copy2(patannpath, pypath)
    except Exception:
        pass

    if(is_copied()):
        return

    sys.excepthook = excepthook
    patannpath = get_pypatann_path()
    package_dir = os.path.dirname(os.path.realpath(__file__))
    error = "patann requires following file to be copied. Execute the following command to copy and try again:\n\n $ sudo /bin/cp -f " + patannpath + "/* " + package_dir + "/\n";
    system_exit_error(error)


if not is_installed():
    error = "missing files. Please uninstall and install patann again\n";
    system_exit_error(error)

set_path_to_lib();
copy_files();

if __package__ or "." in __name__:
    from ._patann import *
else:
    from _patann import *

def _get_raw_string(s):
    if(not s):
        s = ""
    return s.encode('raw_unicode_escape')

_patann_lib = get_patann_lib_path()

print("PatANN Version: " + __patann_version__)
python_version = str(sys.version_info.major) + '.' + str(sys.version_info.minor) + '.' + str(sys.version_info.micro)
print("Python Version: " + python_version)

system = platform.system().lower()
if("cygwin" in system):
    if 'CYGWINPATH' in os.environ:
        cygpath = os.environ['CYGWINPATH']
        _patann_lib = cygpath + _patann_lib
    else:
        _patann_lib = os.path.relpath(_patann_lib)

if(0 != patann_init(_patann_lib, __patann_version__, python_version)):
    system_exit_error('Unable to load: '+ _patann_lib + ' Platform not supported. Contact us at https://mesibo.com/support')

def getPatANNInstance(dim):
    return PatANNInstance(dim);




def help():
    """
    PatANN: Pattern-Aware Approximate Nearest Neighbors Search
    
    Example Helper Functions:
    -----------------------
    patann.help()              - Display this help message
    patann.list_examples()     - List all available examples with descriptions
    patann.get_examples_dir()  - Get the directory path where examples are located
    patann.copy_examples()     - Copy all example files to your current directory
    
    Available Examples:
    -----------------
    patann_sync_example.py:
        - Demonstrates synchronous (blocking) usage of PatANN
        - Shows how to create an index, add vectors, and perform queries in a sequential manner
        - Suitable for simple applications where asynchronous operation is not needed
    
    patann_async_example.py:
        - Demonstrates basic asynchronous usage with a single query
        - Shows how to set up callbacks for index building and query results
        - Good starting point for understanding PatANN's asynchronous operation
    
    patann_async_parallel_example.py:
        - Demonstrates advanced usage with multiple parallel queries
        - Shows how to handle multiple unique query vectors simultaneously
        - Suitable for high-throughput applications needing parallel processing
    
    To run an example after copying:
    $ python patann_sync_example.py
    
    For more information, visit: https://github.com/mesibo/patann
    """
    print(help.__doc__)

def get_examples_dir():
    """
    Return the directory containing example files.
    
    Returns:
        str: Absolute path to the examples directory
    """
    return os.path.join(os.path.dirname(__file__), 'examples')

def list_examples():
    """
    List all available examples with their descriptions.
    
    This function prints the locations of examples and their descriptions,
    and returns the examples directory path.
    
    Returns:
        str: Path to the examples directory
    """
    examples_dir = get_examples_dir()
    
    examples = {
        'patann_sync_example.py': 'Synchronous (blocking) usage of PatANN',
        'patann_async_example.py': 'Basic asynchronous usage with a single query',
        'patann_async_parallel_example.py': 'Advanced parallel query processing with multiple vectors'
    }
    
    print(f"Example files located at: {examples_dir}\n")
    print("Available examples:")
    for name, desc in examples.items():
        print(f"- {name}: {desc}")
    
    print("\nTo copy examples to current directory, run: patann.copy_examples()")
    
    return examples_dir

def copy_examples(destination='.'):
    """
    Copy example files to the specified destination.
    
    Args:
        destination (str): Directory where to copy the examples (default: current directory)
    
    Returns:
        bool: True if copying was successful, False otherwise
        
    Example:
        >>> import patann
        >>> patann.copy_examples()  # Copies to current directory
        >>> patann.copy_examples("my_examples")  # Copies to a specific directory
    """
    examples_dir = get_examples_dir()
    
    if not os.path.exists(examples_dir):
        print("Examples directory not found!")
        return False
    
    # Create destination if it doesn't exist
    if not os.path.exists(destination):
        os.makedirs(destination)
    
    # Copy all examples
    copied = []
    for filename in os.listdir(examples_dir):
        if filename.endswith('.py'):
            src = os.path.join(examples_dir, filename)
            dst = os.path.join(destination, filename)
            shutil.copy2(src, dst)
            copied.append(filename)
    
    print(f"Copied {len(copied)} examples to {os.path.abspath(destination)}:")
    for filename in copied:
        print(f"- {filename}")
    
    print("\nYou can run an example with: python patann_sync_example.py")
    
    return True

