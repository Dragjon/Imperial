import sys
from cx_Freeze import setup, Executable

# Define the executable
executables = [
    Executable('main.py', target_name='imperious.exe')
]

# Setup configuration
setup(
    name='Imperious',
    version='1.0',
    description='Imperious Chess',
    executables=executables
)
