from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.gcp_create_update_subscription_delivery_type import GcpCreateUpdateSubscriptionDeliveryType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.gcp_create_update_subscription_delivery_config import GcpCreateUpdateSubscriptionDeliveryConfig


T = TypeVar("T", bound="GcpCreateUpdateSubscription")


@_attrs_define
class GcpCreateUpdateSubscription:
    """
    Attributes:
        delivery_type (GcpCreateUpdateSubscriptionDeliveryType):
        subscription_id (Union[Unset, str]):
        delivery_config (Union[Unset, GcpCreateUpdateSubscriptionDeliveryConfig]):
    """

    delivery_type: GcpCreateUpdateSubscriptionDeliveryType
    subscription_id: Union[Unset, str] = UNSET
    delivery_config: Union[Unset, "GcpCreateUpdateSubscriptionDeliveryConfig"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        delivery_type = self.delivery_type.value

        subscription_id = self.subscription_id
        delivery_config: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.delivery_config, Unset):
            delivery_config = self.delivery_config.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "delivery_type": delivery_type,
            }
        )
        if subscription_id is not UNSET:
            field_dict["subscription_id"] = subscription_id
        if delivery_config is not UNSET:
            field_dict["delivery_config"] = delivery_config

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.gcp_create_update_subscription_delivery_config import GcpCreateUpdateSubscriptionDeliveryConfig

        d = src_dict.copy()
        delivery_type = GcpCreateUpdateSubscriptionDeliveryType(d.pop("delivery_type"))

        subscription_id = d.pop("subscription_id", UNSET)

        _delivery_config = d.pop("delivery_config", UNSET)
        delivery_config: Union[Unset, GcpCreateUpdateSubscriptionDeliveryConfig]
        if isinstance(_delivery_config, Unset):
            delivery_config = UNSET
        else:
            delivery_config = GcpCreateUpdateSubscriptionDeliveryConfig.from_dict(_delivery_config)

        gcp_create_update_subscription = cls(
            delivery_type=delivery_type,
            subscription_id=subscription_id,
            delivery_config=delivery_config,
        )

        gcp_create_update_subscription.additional_properties = d
        return gcp_create_update_subscription

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
