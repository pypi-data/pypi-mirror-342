"""
The `lunae.interpreter` package provides tools for interpreting parsed data and executing commands.
"""

from typing import Any, Optional

from lunae.interpreter.environment import Environment
from lunae.language.ast.base.block import Block
from lunae.language.ast.base.expr import Expr
from lunae.language.ast.controls.forexpr import ForExpr
from lunae.language.ast.controls.ifexpr import IfExpr
from lunae.language.ast.controls.whileexpr import WhileExpr
from lunae.language.ast.functions.funccall import FuncCall
from lunae.language.ast.functions.funcdef import FuncDef
from lunae.language.ast.values.assign import Assign
from lunae.language.ast.values.number import Number
from lunae.language.ast.values.string import String
from lunae.language.ast.values.var import Var
from lunae.parser import parse
from lunae.tokenizer import tokenize
from lunae.utils.errors import InterpreterError

OPERATORS = {
    "add": lambda a, b: a + b,
    "sub": lambda a, b: a - b,
    "mul": lambda a, b: a * b,
    "div": lambda a, b: a / b,
    "mod": lambda a, b: a % b,
    "is": lambda a, b: a == b,
    "less": lambda a, b: a < b,
    "more": lambda a, b: a > b,
    "neg": lambda a: -a,
    "not": lambda a: not a,
}


def create_global_env() -> Environment:
    """
    Creates and initializes the global environment with predefined operators.

    Returns:
        Environment: The global environment.
    """
    env = Environment()

    for op, fn in OPERATORS.items():
        env.set(op, fn)

    return env


class Interpreter:
    """
    The main interpreter class that evaluates the abstract syntax tree (AST).
    """

    def __init__(self, global_env: Optional[Environment] = None):
        """
        Initializes the interpreter with a global environment.

        Args:
            global_env (Optional[Environment]): The global environment to use.
        """
        self.global_env = global_env or create_global_env()

    def execute(self, source: str):
        """
        Execute the provided source.
        This method is sugar for interpreter.eval(parser.parse(tokenizer.tokenize(source)))

        Args:
            source (str): The code to be executed.

        Returns:
            Any: The result of the execution
        """
        tokens = tokenize(source)
        ast = parse(tokens)
        return self.eval(ast)

    def eval(self, node: Expr, env: "Environment | None" = None) -> Any:
        """
        Evaluates a given AST node.

        Args:
            node (Expr): The AST node to evaluate.
            env (Environment | None): The environment to use for evaluation.

        Returns:
            Any: The result of the evaluation.

        Raises:
            InterpreterError: If the node type is unknown.
        """
        if env is None:
            env = self.global_env

        method = getattr(self, "eval_" + node.__class__.__name__.lower(), None)

        if method is None:
            raise InterpreterError(f"Unknown node to eval: {node}", None)

        return method(node, env)

    def eval_number(self, node: Number, _env: Environment):
        """
        Evaluates a number node.

        Args:
            node (Number): The number node.
            env (Environment): The current environment.

        Returns:
            int | float: The value of the number.
        """
        return node.value

    def eval_string(self, node: String, _env: Environment):
        """
        Evaluates a string node.

        Args:
            node (String): The string node.
            env (Environment): The current environment.

        Returns:
            str: The value of the string.
        """
        return node.value

    def eval_var(self, node: Var, env: Environment):
        """
        Evaluates a variable node.

        Args:
            node (Var): The variable node.
            env (Environment): The current environment.

        Returns:
            Any: The value of the variable.
        """
        return env.get(node.name)

    def eval_assign(self, node: Assign, env: Environment):
        """
        Evaluates an assignment node.

        Args:
            node (Assign): The assignment node.
            env (Environment): The current environment.

        Returns:
            Any: The value assigned.
        """
        val = self.eval(node.value, env)
        env.set(node.name, val)
        return val

    def eval_funccall(self, node: FuncCall, env: Environment):
        """
        Evaluates a function call node.

        Args:
            node (FuncCall): The function call node.
            env (Environment): The current environment.

        Returns:
            Any: The result of the function call.
        """
        fn = env.get(node.func)
        args = [self.eval(a, env) for a in node.args]
        return fn(*args)

    def eval_ifexpr(self, node: IfExpr, env: Environment):
        """
        Evaluates an if expression node.

        Args:
            node (IfExpr): The if expression node.
            env (Environment): The current environment.

        Returns:
            Any: The result of the evaluation.
        """
        cond = self.eval(node.cond, env)
        return (
            self.eval(node.then_branch, env)
            if cond
            else (self.eval(node.else_branch, env) if node.else_branch else None)
        )

    def eval_whileexpr(self, node: WhileExpr, env: Environment):
        """
        Evaluates a while expression node.

        Args:
            node (WhileExpr): The while expression node.
            env (Environment): The current environment.

        Returns:
            Any: The result of the evaluation.
        """
        result = None
        while self.eval(node.cond, env):
            result = self.eval(node.body, env)
        return result

    def eval_forexpr(self, node: ForExpr, env: Environment):
        """
        Evaluates a for expression node.

        Args:
            node (ForExpr): The for expression node.
            env (Environment): The current environment.

        Returns:
            list: The results of evaluating the body for each item in the iterable.
        """
        lst = self.eval(node.iterable, env)
        results = []
        for item in lst:
            env.set(node.var, item)
            results.append(self.eval(node.body, env))
        return results

    def eval_funcdef(self, node: FuncDef, env: Environment):
        """
        Evaluates a function definition node.

        Args:
            node (FuncDef): The function definition node.
            env (Environment): The current environment.

        Returns:
            Callable: The defined function.
        """

        def function(*args):
            local = Environment(env)
            for name, val in zip(node.params, args):
                local.set(name, val)
            return self.eval(node.body, local)

        env.set(node.name, function)
        return function

    def eval_block(self, node: Block, env: Environment):
        """
        Evaluates a block node.

        Args:
            node (Block): The block node.
            env (Environment): The current environment.

        Returns:
            Any: The result of the last expr in the block.
        """
        res = None
        for stmt in node.statements:
            res = self.eval(stmt, env)
        return res


def execute(source: str) -> Any:
    """
    Executes the provided source code using the interpreter.

    Args:
        source (str): The source code to execute.

    Returns:
        Any: The result of the execution.
    """
    interpreter = Interpreter()
    result = interpreter.execute(source)
    return result


__all__ = ("Interpreter", "execute", "create_global_env")
