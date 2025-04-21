import sys
import ast
import re
from ..utils import debug_print

def extract_imports(source_code):
    """
    Extracts all import statements from the given source code.

    Args:
        source_code (str): The Python source code to analyze

    Returns:
        list: A list of import statements found in the code
    """
    try:
        tree = ast.parse(source_code)
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for name in node.names:
                    imports.append(f"import {name.name}" + (f" as {name.asname}" if name.asname else ""))
            elif isinstance(node, ast.ImportFrom):
                module = node.module
                names = []
                for name in node.names:
                    if name.asname:
                        names.append(f"{name.name} as {name.asname}")
                    else:
                        names.append(name.name)
                level_str = "." * node.level if node.level > 0 else ""
                module_str = module if module else ""
                imports.append(f"from {level_str}{module_str} import {', '.join(names)}")
        return imports
    except SyntaxError:
        debug_print("AST parsing failed, falling back to regex")
        imports = []
        import_pattern = r'^import\s+(.+)$'
        from_pattern = r'^from\s+(.+?)\s+import\s+(.+)$'
        for line in source_code.splitlines():
            line = line.strip()
            import_match = re.match(import_pattern, line)
            if import_match:
                imports.append(line)
                continue
            from_match = re.match(from_pattern, line)
            if from_match:
                imports.append(line)
                continue
        return imports

def _get_stdlib_modules():
    """Returns a set of standard library module names."""
    return set(sys.builtin_module_names) | {
        'abc', 'aifc', 'argparse', 'array', 'ast', 'asyncio', 'atexit', 'audioop',
        'base64', 'bdb', 'binascii', 'binhex', 'bisect', 'builtins', 'bz2', 'cProfile',
        'calendar', 'cgi', 'cgitb', 'chunk', 'cmath', 'cmd', 'code', 'codecs',
        'codeop', 'collections', 'colorsys', 'compileall', 'concurrent', 'configparser',
        'contextlib', 'contextvars', 'copy', 'copyreg', 'crypt', 'csv', 'ctypes', 'curses',
        'dataclasses', 'datetime', 'dbm', 'decimal', 'difflib', 'dis', 'distutils',
        'doctest', 'dummy_threading', 'email', 'encodings', 'ensurepip', 'enum', 'errno',
        'faulthandler', 'fcntl', 'filecmp', 'fileinput', 'fnmatch', 'formatter', 'fractions',
        'ftplib', 'functools', 'gc', 'getopt', 'getpass', 'gettext', 'glob', 'grp', 'gzip',
        'hashlib', 'heapq', 'hmac', 'html', 'http', 'idlelib', 'imaplib', 'imghdr', 'imp',
        'importlib', 'inspect', 'io', 'ipaddress', 'itertools', 'json', 'keyword', 'lib2to3',
        'linecache', 'locale', 'logging', 'lzma', 'macpath', 'mailbox', 'mailcap', 'marshal',
        'math', 'mimetypes', 'mmap', 'modulefinder', 'msilib', 'msvcrt', 'multiprocessing',
        'netrc', 'nis', 'nntplib', 'numbers', 'operator', 'optparse', 'os', 'ossaudiodev',
        'parser', 'pathlib', 'pdb', 'pickle', 'pickletools', 'pipes', 'pkgutil', 'platform',
        'plistlib', 'poplib', 'posix', 'pprint', 'profile', 'pstats', 'pty', 'pwd', 'py_compile',
        'pyclbr', 'pydoc', 'queue', 'quopri', 'random', 're', 'readline', 'reprlib', 'resource',
        'rlcompleter', 'runpy', 'sched', 'secrets', 'select', 'selectors', 'shelve', 'shlex',
        'shutil', 'signal', 'site', 'smtpd', 'smtplib', 'sndhdr', 'socket', 'socketserver',
        'spwd', 'sqlite3', 'ssl', 'stat', 'statistics', 'string', 'stringprep', 'struct',
        'subprocess', 'sunau', 'symbol', 'symtable', 'sys', 'sysconfig', 'syslog', 'tabnanny',
        'tarfile', 'telnetlib', 'tempfile', 'termios', 'test', 'textwrap', 'threading', 'time',
        'timeit', 'tkinter', 'token', 'tokenize', 'trace', 'traceback', 'tracemalloc', 'tty',
        'turtle', 'turtledemo', 'types', 'typing', 'unicodedata', 'unittest', 'urllib', 'uu',
        'uuid', 'venv', 'warnings', 'wave', 'weakref', 'webbrowser', 'winreg', 'winsound',
        'wsgiref', 'xdrlib', 'xml', 'xmlrpc', 'zipapp', 'zipfile', 'zipimport', 'zlib'
    }

def _extract_used_names(source_code):
    """
    Extract all names (variables, functions, classes) referenced in the given source code.

    Args:
        source_code (str): The Python source code to analyze

    Returns:
        set: A set of all names referenced in the code
    """
    used_names = set()
    try:
        tree = ast.parse(source_code)
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                used_names.add(node.id)
            elif isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
                used_names.add(node.value.id)
    except SyntaxError:
        debug_print("AST parsing failed when extracting used names, falling back to regex")
        pattern = r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b'
        used_names = set(re.findall(pattern, source_code))
    return used_names

def _filter_imports_by_usage(imports, used_names):
    """
    Filter a list of import statements to only include those that are used in the code.

    Args:
        imports (list): List of import statements
        used_names (set): Set of names used in the code

    Returns:
        list: Filtered list of import statements that are relevant to the used names
    """
    filtered_imports = []

    for imp in imports:
        if imp.startswith('import '):
            parts = imp.replace('import ', '').split(' as ')
            module_name = parts[0].strip()
            alias = parts[1].strip() if len(parts) > 1 else module_name
            module_parts = module_name.split('.')
            if alias in used_names or module_parts[0] in used_names:
                filtered_imports.append(imp)

        elif imp.startswith('from '):
            match = re.match(r'from\s+(.+?)\s+import\s+(.+)$', imp)
            if match:
                module_name = match.group(1)
                imports_part = match.group(2)
                imported_items = [item.strip() for item in imports_part.split(',')]
                if module_name in used_names:
                    filtered_imports.append(imp)
                    continue
                for item in imported_items:
                    parts = item.split(' as ')
                    name = parts[0].strip()
                    alias = parts[1].strip() if len(parts) > 1 else name
                    if name == '*' or alias in used_names or name in used_names:
                        filtered_imports.append(imp)
                        break

    return filtered_imports
