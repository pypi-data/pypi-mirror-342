from lunae.interpreter import Interpreter


def test_add():
    def add(a, b):
        raise NotImplementedError

    interpreter = Interpreter()
    interpreter.global_env.set("add", add)

    try:
        interpreter.execute(
            """
func add2(a, b):
    result = a + b
    result

add2(1, 2)
            """
        )
    except NotImplementedError:
        pass
    else:
        assert False

    result = interpreter.execute(
        """
func add3(a, b):
    result = a - -b
    result

add3(1, 2)
            """
    )
    assert result == 3


def test_sub():
    interpreter = Interpreter()
    result = interpreter.execute("func sub(a, b): a + (-b)\nsub(5, 3)")
    assert result == 2


def test_if_else():
    interpreter = Interpreter()
    result = interpreter.execute(
        """
a = 1
b = 0

if a:
    if b: "err"
    else: "ok"
else: "err"
        """
    )
    assert result == "ok"


def test_nested_loops():
    interpreter = Interpreter()
    interpreter.global_env.set("range", lambda n: list(range(int(n))))
    result = interpreter.execute("for i in range(5): for j in range(5): i * j")
    assert result == [[i * j for j in range(5)] for i in range(5)]


def test_while_loop():
    interpreter = Interpreter()
    result = interpreter.execute(
        """
b = 0
a = 1
c = 0
while (b < 10):
    b = b + 1
    a = !a
    if a: c = c + 1
"""
    )
    assert result == 5
