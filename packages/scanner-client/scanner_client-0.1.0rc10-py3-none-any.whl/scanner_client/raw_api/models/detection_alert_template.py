from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.template_entry import TemplateEntry


T = TypeVar("T", bound="DetectionAlertTemplate")


@_attrs_define
class DetectionAlertTemplate:
    """Detection alert template using `TemplateEntry` types.

    Attributes:
        actions (list['TemplateEntry']):
        info (list['TemplateEntry']):
    """

    actions: list["TemplateEntry"]
    info: list["TemplateEntry"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        actions = []
        for actions_item_data in self.actions:
            actions_item = actions_item_data.to_dict()
            actions.append(actions_item)

        info = []
        for info_item_data in self.info:
            info_item = info_item_data.to_dict()
            info.append(info_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "actions": actions,
                "info": info,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.template_entry import TemplateEntry

        d = src_dict.copy()
        actions = []
        _actions = d.pop("actions")
        for actions_item_data in _actions:
            actions_item = TemplateEntry.from_dict(actions_item_data)

            actions.append(actions_item)

        info = []
        _info = d.pop("info")
        for info_item_data in _info:
            info_item = TemplateEntry.from_dict(info_item_data)

            info.append(info_item)

        detection_alert_template = cls(
            actions=actions,
            info=info,
        )

        detection_alert_template.additional_properties = d
        return detection_alert_template

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
