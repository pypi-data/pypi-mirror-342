from typing import TYPE_CHECKING, Any, Literal

import pydantic
from pydantic import ConfigDict, PrivateAttr
from typing_extensions import Self

from classiq.interface.ast_node import HashableASTNode
from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.expressions.proxies.classical.any_classical_value import (
    AnyClassicalValue,
)
from classiq.interface.generator.expressions.proxies.classical.classical_array_proxy import (
    ClassicalArrayProxy,
)
from classiq.interface.generator.expressions.proxies.classical.classical_proxy import (
    ClassicalProxy,
)
from classiq.interface.generator.expressions.proxies.classical.classical_scalar_proxy import (
    ClassicalScalarProxy,
)
from classiq.interface.helpers.pydantic_model_helpers import values_with_discriminator
from classiq.interface.model.handle_binding import HandleBinding

if TYPE_CHECKING:
    from classiq.interface.generator.functions.concrete_types import (
        ConcreteClassicalType,
    )


class ClassicalType(HashableASTNode):
    _is_generative: bool = PrivateAttr(default=False)

    model_config = ConfigDict(extra="forbid")

    def __str__(self) -> str:
        return str(type(self).__name__)

    def set_generative(self) -> Self:
        self._is_generative = True
        return self

    @property
    def is_generative(self) -> bool:
        return self._is_generative

    @property
    def is_purely_declarative(self) -> bool:
        return not self._is_generative

    def get_classical_proxy(self, handle: HandleBinding) -> ClassicalProxy:
        return ClassicalScalarProxy(handle, self)

    @property
    def expressions(self) -> list[Expression]:
        return []

    def clear_flags(self) -> Self:
        res = self.model_copy()
        res._is_generative = False
        return res


class Integer(ClassicalType):
    kind: Literal["int"]

    @pydantic.model_validator(mode="before")
    @classmethod
    def _set_kind(cls, values: Any) -> dict[str, Any]:
        return values_with_discriminator(values, "kind", "int")


class Real(ClassicalType):
    kind: Literal["real"]

    @pydantic.model_validator(mode="before")
    @classmethod
    def _set_kind(cls, values: Any) -> dict[str, Any]:
        return values_with_discriminator(values, "kind", "real")


class Bool(ClassicalType):
    kind: Literal["bool"]

    @pydantic.model_validator(mode="before")
    @classmethod
    def _set_kind(cls, values: Any) -> dict[str, Any]:
        return values_with_discriminator(values, "kind", "bool")


class ClassicalList(ClassicalType):
    kind: Literal["list"]
    element_type: "ConcreteClassicalType"

    @pydantic.model_validator(mode="before")
    @classmethod
    def _set_kind(cls, values: Any) -> dict[str, Any]:
        return values_with_discriminator(values, "kind", "list")

    def get_classical_proxy(self, handle: HandleBinding) -> ClassicalProxy:
        return ClassicalArrayProxy(
            handle, self.element_type, AnyClassicalValue(f"get_field({handle}, 'len')")
        )

    @property
    def expressions(self) -> list[Expression]:
        return self.element_type.expressions

    @property
    def is_purely_declarative(self) -> bool:
        return super().is_purely_declarative and self.element_type.is_purely_declarative


class StructMetaType(ClassicalType):
    kind: Literal["type_proxy"]

    @pydantic.model_validator(mode="before")
    @classmethod
    def _set_kind(cls, values: Any) -> dict[str, Any]:
        return values_with_discriminator(values, "kind", "type_proxy")

    def get_classical_proxy(self, handle: HandleBinding) -> ClassicalProxy:
        raise NotImplementedError


class ClassicalArray(ClassicalType):
    kind: Literal["array"]
    element_type: "ConcreteClassicalType"
    size: int

    @pydantic.model_validator(mode="before")
    @classmethod
    def _set_kind(cls, values: Any) -> dict[str, Any]:
        return values_with_discriminator(values, "kind", "array")

    def get_classical_proxy(self, handle: HandleBinding) -> ClassicalProxy:
        return ClassicalArrayProxy(handle, self.element_type, self.size)

    @property
    def expressions(self) -> list[Expression]:
        return self.element_type.expressions

    @property
    def is_purely_declarative(self) -> bool:
        return super().is_purely_declarative and self.element_type.is_purely_declarative


class OpaqueHandle(ClassicalType):
    pass


class VQEResult(OpaqueHandle):
    kind: Literal["vqe_result"]

    @pydantic.model_validator(mode="before")
    @classmethod
    def _set_kind(cls, values: Any) -> dict[str, Any]:
        return values_with_discriminator(values, "kind", "vqe_result")


class Histogram(OpaqueHandle):
    kind: Literal["histogram"]

    @pydantic.model_validator(mode="before")
    @classmethod
    def _set_kind(cls, values: Any) -> dict[str, Any]:
        return values_with_discriminator(values, "kind", "histogram")


class Estimation(OpaqueHandle):
    kind: Literal["estimation_result"]

    @pydantic.model_validator(mode="before")
    @classmethod
    def _set_kind(cls, values: Any) -> dict[str, Any]:
        return values_with_discriminator(values, "kind", "estimation_result")


class IQAERes(OpaqueHandle):
    kind: Literal["iqae_result"]

    @pydantic.model_validator(mode="before")
    @classmethod
    def _set_kind(cls, values: Any) -> dict[str, Any]:
        return values_with_discriminator(values, "kind", "iqae_result")


class QmodPyObject:
    pass
