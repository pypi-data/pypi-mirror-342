import textwrap
import pathlib

import llm
from llm_fragments_symbex import symbex_loader

def create_file(path: pathlib.Path, src: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(src), encoding="utf8")

def test_symbex_loader_basic(tmp_path):
    # Create a little fake project
    pkg = tmp_path / "myproj"
    # Simple function with docstring
    create_file(
        pkg / "f1.py",
        """
        def f1():
            \"\"\"This is f1\"\"\"
            pass
        """,
    )
    # A class with a method that has a type annotation and docstring
    create_file(
        pkg / "pkg2" / "f2.py",
        """
        class C2:
            def m2(self, x: int) -> str:
                \"\"\"method m2\"\"\"
                return str(x)
        """,
    )

    fragment = symbex_loader(str(pkg))
    assert isinstance(fragment, llm.Fragment)
    assert fragment.source == f"symbex:{pkg.resolve()}"

    expected = textwrap.dedent("""
    # from f1 import f1
    def f1():
        "This is f1"

    # from pkg2.f2 import C2
    class C2:

        def m2(self, x: int) -> str:
            "method m2"
    """).strip()
    assert str(fragment) == expected
