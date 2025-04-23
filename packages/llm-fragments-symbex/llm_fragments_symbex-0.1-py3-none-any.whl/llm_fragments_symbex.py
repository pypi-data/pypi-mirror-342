import llm
import pathlib
from symbex.lib import read_file, find_symbol_nodes, code_for_node, import_line_for_function

@llm.hookimpl
def register_fragment_loaders(register):
    """
    Register the 'symbex' loader.  Usage:
        llm -f symbex:/path/to/folder ...
    """
    register("symbex", symbex_loader)

def symbex_loader(argument: str) -> llm.Fragment:
    """
    Walk the given directory, parse every .py file, and for every
    top-level function or class-method produce its signature and
    docstring plus an import line.
    """
    folder = pathlib.Path(argument).expanduser().resolve()
    if not folder.is_dir():
        raise ValueError(f"symbex loader: '{folder}' is not a directory")
    snippets = []
    seen_imports = set()    
    # We'll treat the base folder as the root for import-line generation
    possible_roots = [str(folder)]
    # Recursively find all .py files
    for py_file in sorted(folder.rglob("*.py")):
        try:
            source = read_file(py_file)
        except Exception:
            # skip unreadable files
            continue
        # match everything: top-level defs (*) and methods (*.*)
        matches = find_symbol_nodes(source, str(py_file), ["*", "*.*"])
        for node, class_name in matches:
            # extract signature + docstring
            snippet, _lineno = code_for_node(
                source,
                node,
                class_name,
                signatures=True,
                docstrings=True,
            )
            # pick the correct symbol name for import
            symbol = class_name if class_name else node.name
            imp = import_line_for_function(symbol, str(py_file), possible_roots)
            # only emit each import-line comment once
            if imp in seen_imports:
                full = snippet
            else:
                seen_imports.add(imp)
                full = f"# {imp}\n{snippet}"
            snippets.append(full)
    body = "\n\n".join(snippets)
    return llm.Fragment(body, source=f"symbex:{folder}")
