from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Union

import sympy
from sympy import Integer
from typing_extensions import TypeGuard

from classiq.interface.exceptions import ClassiqIndexError
from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.expressions.non_symbolic_expr import NonSymbolicExpr
from classiq.interface.generator.expressions.proxies.classical.any_classical_value import (
    AnyClassicalValue,
)
from classiq.interface.generator.expressions.proxies.classical.classical_proxy import (
    ClassicalProxy,
)
from classiq.interface.model.handle_binding import (
    HandleBinding,
    SlicedHandleBinding,
    SubscriptHandleBinding,
)

if TYPE_CHECKING:
    from classiq.interface.generator.expressions.expression_types import ExpressionValue
    from classiq.interface.generator.functions.concrete_types import (
        ConcreteClassicalType,
    )


def _is_int(val: Any) -> TypeGuard[Union[int, sympy.Basic]]:
    if isinstance(val, AnyClassicalValue):
        return False
    if isinstance(val, sympy.Basic):
        return val.is_Number
    return isinstance(val, int)


class ClassicalArrayProxy(NonSymbolicExpr, ClassicalProxy):
    def __init__(
        self,
        handle: HandleBinding,
        element_type: "ConcreteClassicalType",
        length: "ExpressionValue",
    ) -> None:
        super().__init__(handle)
        self._element_type = element_type
        self._length = length

    @property
    def fields(self) -> Mapping[str, "ExpressionValue"]:
        return {"len": self._length}

    @property
    def type_name(self) -> str:
        return "Array"

    @property
    def length(self) -> "ExpressionValue":
        return self._length

    def __getitem__(
        self, key: Union[slice, int, Integer, ClassicalProxy]
    ) -> ClassicalProxy:
        return (
            self._get_slice(key) if isinstance(key, slice) else self._get_subscript(key)
        )

    def _get_slice(self, slice_: slice) -> ClassicalProxy:
        start_ = slice_.start
        stop_ = slice_.stop
        if _is_int(start_) and _is_int(stop_):
            start = int(start_)
            stop = int(stop_)
            if start >= stop:
                raise ClassiqIndexError("Array slice has non-positive length")
            if start < 0 or (isinstance(self._length, int) and stop > self._length):
                raise ClassiqIndexError("Array slice is out of bounds")
        return ClassicalArrayProxy(
            SlicedHandleBinding(
                base_handle=self.handle,
                start=Expression(expr=str(start_)),
                end=Expression(expr=str(stop_)),
            ),
            self._element_type,
            stop_ - start_,
        )

    def _get_subscript(
        self, index_: Union[int, Integer, ClassicalProxy]
    ) -> ClassicalProxy:
        if _is_int(index_):
            index = int(index_)
            if index < 0:
                raise ClassiqIndexError(
                    "Array index is out of bounds (negative indices are not supported)"
                )
            if isinstance(self._length, int) and index >= self._length:
                raise ClassiqIndexError("Array index is out of bounds")
        return self._element_type.get_classical_proxy(
            SubscriptHandleBinding(
                base_handle=self._handle, index=Expression(expr=str(index_))
            )
        )
