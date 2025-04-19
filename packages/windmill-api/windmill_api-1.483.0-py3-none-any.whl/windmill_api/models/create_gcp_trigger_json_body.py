from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_gcp_trigger_json_body_subscription_mode import CreateGcpTriggerJsonBodySubscriptionMode


T = TypeVar("T", bound="CreateGcpTriggerJsonBody")


@_attrs_define
class CreateGcpTriggerJsonBody:
    """
    Attributes:
        gcp_resource_path (str):
        topic_id (str):
        subscription_mode (CreateGcpTriggerJsonBodySubscriptionMode): "This is a union type representing the
            subscription mode.
             - 'existing': Represents an existing GCP subscription, and should be accompanied by an
            'ExistingGcpSubscription' object.
             - 'create_update': Represents a new or updated GCP subscription, and should be accompanied by a
            'CreateUpdateConfig' object."
        path (str):
        script_path (str):
        is_flow (bool):
        enabled (Union[Unset, bool]):
    """

    gcp_resource_path: str
    topic_id: str
    subscription_mode: "CreateGcpTriggerJsonBodySubscriptionMode"
    path: str
    script_path: str
    is_flow: bool
    enabled: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        gcp_resource_path = self.gcp_resource_path
        topic_id = self.topic_id
        subscription_mode = self.subscription_mode.to_dict()

        path = self.path
        script_path = self.script_path
        is_flow = self.is_flow
        enabled = self.enabled

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "gcp_resource_path": gcp_resource_path,
                "topic_id": topic_id,
                "subscription_mode": subscription_mode,
                "path": path,
                "script_path": script_path,
                "is_flow": is_flow,
            }
        )
        if enabled is not UNSET:
            field_dict["enabled"] = enabled

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.create_gcp_trigger_json_body_subscription_mode import CreateGcpTriggerJsonBodySubscriptionMode

        d = src_dict.copy()
        gcp_resource_path = d.pop("gcp_resource_path")

        topic_id = d.pop("topic_id")

        subscription_mode = CreateGcpTriggerJsonBodySubscriptionMode.from_dict(d.pop("subscription_mode"))

        path = d.pop("path")

        script_path = d.pop("script_path")

        is_flow = d.pop("is_flow")

        enabled = d.pop("enabled", UNSET)

        create_gcp_trigger_json_body = cls(
            gcp_resource_path=gcp_resource_path,
            topic_id=topic_id,
            subscription_mode=subscription_mode,
            path=path,
            script_path=script_path,
            is_flow=is_flow,
            enabled=enabled,
        )

        create_gcp_trigger_json_body.additional_properties = d
        return create_gcp_trigger_json_body

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
