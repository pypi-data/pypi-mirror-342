from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.update_gcp_trigger_json_body_subscription_mode import UpdateGcpTriggerJsonBodySubscriptionMode


T = TypeVar("T", bound="UpdateGcpTriggerJsonBody")


@_attrs_define
class UpdateGcpTriggerJsonBody:
    """
    Attributes:
        topic_id (str):
        subscription_mode (UpdateGcpTriggerJsonBodySubscriptionMode): "This is a union type representing the
            subscription mode.
             - 'existing': Represents an existing GCP subscription, and should be accompanied by an
            'ExistingGcpSubscription' object.
             - 'create_update': Represents a new or updated GCP subscription, and should be accompanied by a
            'CreateUpdateConfig' object."
        path (str):
        script_path (str):
        is_flow (bool):
        enabled (bool):
        gcp_resource_path (Union[Unset, str]):
    """

    topic_id: str
    subscription_mode: "UpdateGcpTriggerJsonBodySubscriptionMode"
    path: str
    script_path: str
    is_flow: bool
    enabled: bool
    gcp_resource_path: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        topic_id = self.topic_id
        subscription_mode = self.subscription_mode.to_dict()

        path = self.path
        script_path = self.script_path
        is_flow = self.is_flow
        enabled = self.enabled
        gcp_resource_path = self.gcp_resource_path

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "topic_id": topic_id,
                "subscription_mode": subscription_mode,
                "path": path,
                "script_path": script_path,
                "is_flow": is_flow,
                "enabled": enabled,
            }
        )
        if gcp_resource_path is not UNSET:
            field_dict["gcp_resource_path"] = gcp_resource_path

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.update_gcp_trigger_json_body_subscription_mode import UpdateGcpTriggerJsonBodySubscriptionMode

        d = src_dict.copy()
        topic_id = d.pop("topic_id")

        subscription_mode = UpdateGcpTriggerJsonBodySubscriptionMode.from_dict(d.pop("subscription_mode"))

        path = d.pop("path")

        script_path = d.pop("script_path")

        is_flow = d.pop("is_flow")

        enabled = d.pop("enabled")

        gcp_resource_path = d.pop("gcp_resource_path", UNSET)

        update_gcp_trigger_json_body = cls(
            topic_id=topic_id,
            subscription_mode=subscription_mode,
            path=path,
            script_path=script_path,
            is_flow=is_flow,
            enabled=enabled,
            gcp_resource_path=gcp_resource_path,
        )

        update_gcp_trigger_json_body.additional_properties = d
        return update_gcp_trigger_json_body

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
