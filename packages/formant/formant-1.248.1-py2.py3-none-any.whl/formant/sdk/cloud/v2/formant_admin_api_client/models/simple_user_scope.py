from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="SimpleUserScope")


@attr.s(auto_attribs=True)
class SimpleUserScope:
    """
    Attributes:
        tags (Any):
        roles (Union[Unset, Any]):
        users (Union[Unset, Any]):
        teams (Union[Unset, Any]):
        devices (Union[Unset, Any]):
        fleets (Union[Unset, Any]):
        events (Union[Unset, Any]):
        views (Union[Unset, Any]):
        key_value (Union[Unset, Any]):
    """

    tags: Any
    roles: Union[Unset, Any] = UNSET
    users: Union[Unset, Any] = UNSET
    teams: Union[Unset, Any] = UNSET
    devices: Union[Unset, Any] = UNSET
    fleets: Union[Unset, Any] = UNSET
    events: Union[Unset, Any] = UNSET
    views: Union[Unset, Any] = UNSET
    key_value: Union[Unset, Any] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        tags = self.tags
        roles = self.roles
        users = self.users
        teams = self.teams
        devices = self.devices
        fleets = self.fleets
        events = self.events
        views = self.views
        key_value = self.key_value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "tags": tags,
            }
        )
        if roles is not UNSET:
            field_dict["roles"] = roles
        if users is not UNSET:
            field_dict["users"] = users
        if teams is not UNSET:
            field_dict["teams"] = teams
        if devices is not UNSET:
            field_dict["devices"] = devices
        if fleets is not UNSET:
            field_dict["fleets"] = fleets
        if events is not UNSET:
            field_dict["events"] = events
        if views is not UNSET:
            field_dict["views"] = views
        if key_value is not UNSET:
            field_dict["keyValue"] = key_value

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        tags = d.pop("tags")

        roles = d.pop("roles", UNSET)

        users = d.pop("users", UNSET)

        teams = d.pop("teams", UNSET)

        devices = d.pop("devices", UNSET)

        fleets = d.pop("fleets", UNSET)

        events = d.pop("events", UNSET)

        views = d.pop("views", UNSET)

        key_value = d.pop("keyValue", UNSET)

        simple_user_scope = cls(
            tags=tags,
            roles=roles,
            users=users,
            teams=teams,
            devices=devices,
            fleets=fleets,
            events=events,
            views=views,
            key_value=key_value,
        )

        simple_user_scope.additional_properties = d
        return simple_user_scope

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
