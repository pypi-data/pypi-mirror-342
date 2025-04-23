"""
The `lunae.repl` module provides an interactive Read-Eval-Print Loop (REPL) for testing and debugging.
"""

import traceback
from importlib.metadata import PackageNotFoundError, version
from os import path
from textwrap import dedent

from lunae.interpreter import Interpreter, create_global_env
from lunae.parser import parse
from lunae.tokenizer import tokenize
from lunae.utils.errors import SourceError
from lunae.utils.indent import indent


def get_version() -> str:
    """
    Fetch the installed lunae version.
    """
    try:
        return version("lunae")
    except PackageNotFoundError:
        version_file_path = path.join(path.dirname(__file__), "..", "..", "VERSION")
        if path.exists(version_file_path):
            with open(version_file_path, encoding="utf-8") as f:
                return f.read().strip()
        else:
            return "unknown"


class REPL:
    """
    Represents the REPL (Read-Eval-Print Loop) for the language.
    """

    def __init__(self):
        """
        Initializes the REPL.
        """
        self.interpreter = Interpreter()
        self.lines = []
        self.debuging = False
        self.quiting = False

        self.reset()

        print(f"LUNAE {get_version()} - REPL")
        print('Type "help()" for more information')

    def eval(self, source: str):
        """
        Evaluates a source code string.

        Args:
            source (str): The source code to evaluate.
        """
        try:
            ast = parse(tokenize(source))
            result = None
            for child in ast.statements:
                result = self.interpreter.eval(child)
                formated = indent(result, ". ").replace(". ", "> ", 1)
                print(formated)
        except Exception as e:  # pylint: disable=broad-exception-caught
            if isinstance(e, SourceError):
                e.with_source(source)

            if isinstance(e, SourceError) and not self.debuging:
                print("ERR", e)
                if e.note:
                    print(e.note)
            else:
                print(" ERROR ".center(60, "-"))
                traceback.print_exc()
                print("-" * 60)

    def load(self, filename: str):
        """
        Loads and evaluates a source code file.

        Args:
            filename (str): The path to the source code file.
        """
        with open(filename, encoding="utf-8") as f:
            source = f.read()
            try:
                self.eval(source)
            except SourceError as e:
                e.with_source(source)
                raise e

    def debug(self):
        """
        Enables debug mode.
        """
        self.debuging = True

    def quit(self):
        """
        Quits the REPL.
        """
        self.quiting = True

    def print(self, *args):
        """
        Prints arguments to the console.
        """
        print(" ", *args)

    def help(self, var=None):
        """
        Displays help information for a value or lists available functions and variables.

        Args:
            value (Any, optional): The value to display help for. Defaults to None.
        """
        if var:
            if callable(var):
                target = var
            else:
                target = type(var)

            print("Help on", target.__qualname__)
            if target.__doc__:
                print(indent(dedent(target.__doc__)))
            else:
                print("No information available :-(")
        else:
            functions = []
            others = []
            for name, env_var in self.interpreter.global_env.vars.items():
                if callable(env_var):
                    functions.append(f"{name.ljust(15)} - {env_var.__qualname__}")
                else:
                    others.append(f"{name.ljust(15)} - {repr(env_var)}")

            print("== FUNCTIONS ==")
            for fn in functions:
                print(fn)
            if others:
                print("== OTHERS ==")
                for val in others:
                    print(val)

    def reset(self):
        """
        Resets the REPL environment.
        """
        env = create_global_env()

        # REPL
        env.set("load", self.load)
        env.set("quit", self.quit)
        env.set("debug", self.debug)
        env.set("reset", self.reset)
        env.set("help", self.help)

        # DEBUG
        env.set("tokenize", tokenize)
        env.set("parse", parse)

        # OTHERS
        env.set("print", self.print)
        env.set("range", lambda n: list(range(int(n))))

        self.interpreter.global_env = env

    def start(self):
        """
        Starts the REPL loop.
        """
        while not self.quiting:
            inp = input("... " if self.lines else ">>> ")
            if inp:
                self.lines.append(inp)

            if not inp or (len(self.lines) == 1 and inp[-1] != ":"):
                self.eval("\n".join(self.lines))
                self.lines.clear()


__all__ = ("REPL",)
