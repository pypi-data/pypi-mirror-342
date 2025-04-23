from enum import StrEnum, auto
from typing import Any, Optional, Set, Tuple, Union


class Variance(StrEnum):
    COVARIANT = auto()
    CONTRAVARIANT = auto()
    INVARIANT = auto()

    def __repr__(self):
        return f"Variance.{self.name}"


class Type:
    def __init__(
        self,
        name: str,
        parameters: Tuple[Tuple["Type", Variance], ...] = (),
        supertype: Optional["Type"] = None,
    ):
        self.name = name
        self.parameters = parameters
        self.supertype = supertype

    def is_subtype_of(self, other: "Type") -> bool:
        if self == other:
            return True

        if self.name == other.name:
            # Ensure the number of parameters match
            if len(self.parameters) != len(other.parameters):
                return False

            # Check parameter variance
            for (self_param, self_variance), (other_param, other_variance) in zip(
                self.parameters, other.parameters
            ):
                if self_variance == Variance.COVARIANT:
                    if not self_param.is_subtype_of(other_param):
                        return False
                elif self_variance == Variance.CONTRAVARIANT:
                    if not other_param.is_subtype_of(self_param):
                        return False
                elif self_variance == Variance.INVARIANT:
                    if not self_param == other_param:
                        return False

                return True

        # Check if the current type's supertype is a subtype of the other type
        if self.supertype and self.supertype.is_subtype_of(other):
            return True

        return False

    def __getitem__(self, parameters: Union["Type", Tuple["Type", ...]]):
        params = parameters if isinstance(parameters, tuple) else (parameters,)

        if len(params) != len(self.parameters):
            raise TypeError(
                f"Invalid number of parameters to subscript {self}: got {params}"
            )

        return Type(
            self.name,
            tuple((np, p[1]) for (np, p) in zip(params, self.parameters)),
            self.supertype,
        )

    def __repr__(self) -> str:
        if self.parameters:
            params = ", ".join(repr(p[0]) for p in self.parameters)
            return f"{self.name}[{params}]"
        return self.name

    def __eq__(self, other: Any) -> bool:
        return (
            isinstance(other, Type)
            and self.name == other.name
            and self.parameters == other.parameters
            and self.supertype == other.supertype
        )

    def __hash__(self) -> int:
        return hash((self.name, self.parameters, self.supertype))


if __name__ == "__main__":
    any_t = Type("any")
    float_t = Type("float", supertype=any_t)
    int_t = Type("int", supertype=float_t)
    bool_t = Type("bool", supertype=int_t)

    list_t = Type("list", ((any_t, Variance.COVARIANT),), supertype=any_t)
    set_t = Type("set", ((any_t, Variance.COVARIANT),), supertype=any_t)
    dict_t = Type(
        "dict",
        ((any_t, Variance.COVARIANT), (any_t, Variance.COVARIANT)),
        supertype=any_t,
    )

    int_list_t = list_t[int_t]

    assert int_t.is_subtype_of(any_t)
    assert int_list_t.is_subtype_of(list_t)
