from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.metadata_with_current_value_current_value import MetadataWithCurrentValueCurrentValue


T = TypeVar("T", bound="MetadataWithCurrentValue")


@attr.s(auto_attribs=True)
class MetadataWithCurrentValue:
    """
    Attributes:
        current_value (Union[Unset, MetadataWithCurrentValueCurrentValue]):
    """

    current_value: Union[Unset, "MetadataWithCurrentValueCurrentValue"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        current_value: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.current_value, Unset):
            current_value = self.current_value.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if current_value is not UNSET:
            field_dict["currentValue"] = current_value

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.metadata_with_current_value_current_value import MetadataWithCurrentValueCurrentValue

        d = src_dict.copy()
        _current_value = d.pop("currentValue", UNSET)
        current_value: Union[Unset, MetadataWithCurrentValueCurrentValue]
        if isinstance(_current_value, Unset):
            current_value = UNSET
        else:
            current_value = MetadataWithCurrentValueCurrentValue.from_dict(_current_value)

        metadata_with_current_value = cls(
            current_value=current_value,
        )

        metadata_with_current_value.additional_properties = d
        return metadata_with_current_value

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
