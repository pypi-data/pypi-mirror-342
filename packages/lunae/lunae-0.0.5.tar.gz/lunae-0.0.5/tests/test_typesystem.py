from lunae.language.typesystem import Type, Variance


def basic_types():
    any_t = Type("any")
    float_t = Type("float", supertype=any_t)
    int_t = Type("int", supertype=float_t)
    bool_t = Type("bool", supertype=int_t)

    list_t = Type("list", ((any_t, Variance.COVARIANT),), supertype=any_t)

    int_list_t = list_t[int_t]

    return any_t, bool_t, int_t, float_t, list_t, int_list_t


def test_hash_and_eq_for_same_signature():
    any_t, bool_t, int_t, float_t, list_t, int_list_t = basic_types()

    t1 = list_t[int_t]
    t2 = list_t[int_t]
    assert t1 == t2
    assert hash(t1) == hash(t2)


def test_subtype_basic():
    any_t, bool_t, int_t, float_t, list_t, int_list_t = basic_types()

    assert bool_t.is_subtype_of(any_t)
    assert any_t.is_subtype_of(any_t)
    assert not any_t.is_subtype_of(int_t)


def test_deep_subtype_chain():
    root = Type("Root")
    mid = Type("Mid", supertype=root)
    leaf = Type("Leaf", supertype=mid)
    assert leaf.is_subtype_of(mid)
    assert leaf.is_subtype_of(root)
    assert not mid.is_subtype_of(leaf)


def test_repr_for_parameterized():
    any_t, bool_t, int_t, float_t, list_t, int_list_t = basic_types()
    assert repr(int_list_t) == "list[int]"


def test_equality():
    base = Type("Base")
    derived1 = Type("Derived", supertype=base)
    derived2 = Type("Derived", supertype=base)
    assert derived1 == derived2


def test_covariance():
    any_t, bool_t, int_t, float_t, list_t, int_list_t = basic_types()

    box = Type("box", ((any_t, Variance.COVARIANT),))

    box_int = box[int_t]
    box_float = box[float_t]
    assert box_int.is_subtype_of(box_float)
    assert box_int.is_subtype_of(box)


def test_contravariance():
    any_t, bool_t, int_t, float_t, list_t, int_list_t = basic_types()

    hander = Type("handler", ((any_t, Variance.CONTRAVARIANT),))

    h_float = hander[float_t]
    h_int = hander[int_t]
    assert h_float.is_subtype_of(h_int)  # Because Handler is contravariant


def test_invariance():
    any_t, bool_t, int_t, float_t, list_t, int_list_t = basic_types()

    ibox = Type("invariantBox", ((any_t, Variance.INVARIANT),))

    box_int = ibox[int_t]
    box_float = ibox[float_t]
    assert not box_int.is_subtype_of(box_float)
    assert not box_float.is_subtype_of(box_int)


def test_practical_list_subtyping():
    any_t, bool_t, int_t, float_t, list_t, int_list_t = basic_types()

    float_list_t = list_t[float_t]

    # Practical check: list[int] <: list[float] because int <: float
    assert int_t.is_subtype_of(float_t)
    assert int_list_t.is_subtype_of(float_list_t)

    # Negative: list[float] ⊄ list[int]
    assert not float_list_t.is_subtype_of(int_list_t)
