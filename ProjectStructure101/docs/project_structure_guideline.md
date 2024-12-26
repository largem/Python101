# Project Structure Example
Here's a common layout for a Python project:

project_root/
├── src/
│   ├── __init__.py
│   ├── module1.py
│   ├── module2.py
│   └── ... (other modules)
├── tests/
│   ├── __init__.py
│   ├── test_module1.py
│   ├── test_module2.py
│   └── ... (other test files)
├── .gitignore
├── README.md
├── requirements.txt
├── setup.py
└── pytest.ini

## Guidelines:

### Source Code (src/):
- Place all your source code here. Each module you create should have its own directory under src/ and the actual .py files for that module inside those directories.
- Use an __init__.py file to initialize the package if necessary.

### Test Code (tests/):
- Place all your test code here. Each set of tests related to a specific module should be grouped together in its own directory or files under tests/.
- Use an __init__.py file as needed for the same reasons mentioned above regarding source code modules.

### Separate Concerns:
- By keeping your source code and test code separate, you make it easier to manage dependencies and avoid conflicts between production code and testing utilities.
- This separation also helps in maintaining a clean project structure that is easy for others (or yourself) to understand and navigate.

### Configuration Files:
- `.gitignore` should be used to specify which files or directories should not be tracked by Git, preventing unnecessary clutter from build artifacts, logs, etc.
- `README.md` can serve as a project description and guide for anyone using your codebase.
- `requirements.txt` lists all the dependencies required to run your application.
- `setup.py` is used to define metadata about your package and how it should be built, installed, etc.
- `pytest.ini` (if you're using pytest) can configure options or plugins specific to that testing framework.

## References
- https://docs.python-guide.org/writing/structure/#modules