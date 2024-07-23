import sys
from cx_Freeze import setup, Executable

# Define the executable
executables = [
    Executable(
        script='imperious.py',
        target_name='imperious.exe',
        base=None,  # None for console applications
        icon=None,  # Add path to icon file if you have one
    )
]

# Setup configuration
setup(
    name='Imperious',
    version='0.0.6',
    description='Imperious Chess',
    options={
        'build_exe': {
            'packages': [],  # List packages that should be included
            'include_files': [],  # List additional files that should be included
            'excludes': [],  # List packages to exclude
            'path': sys.path + ['C:\\Users\\dragon\\Downloads\\pypy3.10-v7.3.16-win64\\pypy3.10-v7.3.16-win64'],  # Ensure PyPy is in the path
        }
    },
    executables=executables
)
