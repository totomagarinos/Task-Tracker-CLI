from setuptools import setup, find_packages

setup(
    name="task-cli",
    version="0.1.0",
    py_modules=["task_cli"],
    entry_points={
        'console_scripts': [
            'task-cli=task_cli:main',
        ],
    },
)