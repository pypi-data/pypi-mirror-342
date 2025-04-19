from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.update_gcp_trigger_json_body_subscription_mode_subscription_mode import (
    UpdateGcpTriggerJsonBodySubscriptionModeSubscriptionMode,
)

T = TypeVar("T", bound="UpdateGcpTriggerJsonBodySubscriptionMode")


@_attrs_define
class UpdateGcpTriggerJsonBodySubscriptionMode:
    """ "This is a union type representing the subscription mode.
     - 'existing': Represents an existing GCP subscription, and should be accompanied by an 'ExistingGcpSubscription'
    object.
     - 'create_update': Represents a new or updated GCP subscription, and should be accompanied by a
    'CreateUpdateConfig' object."

        Attributes:
            subscription_mode (UpdateGcpTriggerJsonBodySubscriptionModeSubscriptionMode): The mode of subscription.
                'existing' means using an existing GCP subscription, while 'create_update' involves creating or updating a new
                subscription.
    """

    subscription_mode: UpdateGcpTriggerJsonBodySubscriptionModeSubscriptionMode
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        subscription_mode = self.subscription_mode.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "subscription_mode": subscription_mode,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        subscription_mode = UpdateGcpTriggerJsonBodySubscriptionModeSubscriptionMode(d.pop("subscription_mode"))

        update_gcp_trigger_json_body_subscription_mode = cls(
            subscription_mode=subscription_mode,
        )

        update_gcp_trigger_json_body_subscription_mode.additional_properties = d
        return update_gcp_trigger_json_body_subscription_mode

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
