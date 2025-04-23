import time
from typing import List, Optional, Union

from ethereal.constants import API_PREFIX
from ethereal.rest.util import generate_nonce, uuid_to_bytes32
from ethereal.models.rest import (
    OrderDto,
    OrderDryRunDto,
    PageOfOrderDtos,
    PageOfOrderFillDtos,
    PageOfTradeDtos,
    SubmitOrderDto,
    SubmitDryOrderDto,
    SubmitOrderLimitDtoData,
    SubmitOrderMarketDtoData,
    CancelOrderDto,
    CancelOrderDtoData,
    CancelOrderResultDto,
    V1OrderGetParametersQuery,
    V1OrderFillGetParametersQuery,
    V1OrderTradeGetParametersQuery,
)


def list_orders(self, **kwargs) -> PageOfOrderDtos:
    """Lists orders for a subaccount.

    Args:
        subaccount_id (str): UUID of the subaccount. Required.

    Other Parameters:
        product_ids (List[str], optional): List of product UUIDs to filter. Optional.
        created_after (float, optional): Filter for orders created after this timestamp. Optional.
        created_before (float, optional): Filter for orders created before this timestamp. Optional.
        side (int, optional): Order side (BUY = 0, SELL = 1). Optional.
        close (bool, optional): Filter for close orders. Optional.
        stop_types (List[int], optional): List of stop types. Optional.
        statuses (List[str], optional): List of order statuses. Optional.
        order_by (str, optional): Field to order by, e.g., 'type'. Optional.
        order (str, optional): Sort order, 'asc' or 'desc'. Optional.
        limit (float, optional): Maximum number of results to return. Optional.
        cursor (str, optional): Pagination cursor for fetching the next page. Optional.
        **kwargs: Additional request parameters accepted by the API. Optional.

    Returns:
        PageOfOrderDtos: List of order information.
    """
    res = self.get_validated(
        url_path=f"{API_PREFIX}/order",
        request_model=V1OrderGetParametersQuery,
        response_model=PageOfOrderDtos,
        **kwargs,
    )
    return res.data


def list_fills(
    self,
    **kwargs,
) -> PageOfOrderFillDtos:
    """Lists order fills for a subaccount.

    Args:
        subaccount_id (str): UUID of the subaccount. Required.

    Other Parameters:
        product_ids (List[str], optional): List of product UUIDs to filter. Optional.
        created_after (float, optional): Filter for fills created after this timestamp. Optional.
        created_before (float, optional): Filter for fills created before this timestamp. Optional.
        side (int, optional): Fill side (BUY = 0, SELL = 1). Optional.
        statuses (List[str], optional): List of fill statuses. Optional.
        order_by (str, optional): Field to order by, e.g., 'productId'. Optional.
        order (str, optional): Sort order, 'asc' or 'desc'. Optional.
        limit (float, optional): Maximum number of results to return. Optional.
        cursor (str, optional): Pagination cursor for fetching the next page. Optional.
        include_self_trades (bool, optional): Whether to include self trades. Optional.
        **kwargs: Additional request parameters accepted by the API. Optional.

    Returns:
        PageOfOrderFillDtos: List of order fill information.
    """
    res = self.get_validated(
        url_path=f"{API_PREFIX}/order/fill",
        request_model=V1OrderFillGetParametersQuery,
        response_model=PageOfOrderFillDtos,
        **kwargs,
    )
    return res.data


def list_trades(
    self,
    **kwargs,
) -> PageOfTradeDtos:
    """Lists trades for a product if specified, otherwise lists trades for all products.

    Other Parameters:
        product_id (str, optional): UUID of the product. Optional.
        order_by (str, optional): Field to order by, e.g., 'createdAt'. Optional.
        order (str, optional): Sort order, 'asc' or 'desc'. Optional.
        limit (float, optional): Maximum number of results to return. Optional.
        cursor (str, optional): Pagination cursor for fetching the next page. Optional.
        **kwargs: Additional request parameters accepted by the API. Optional.

    Returns:
        PageOfTradeDtos: List of trade information.
    """
    res = self.get_validated(
        url_path=f"{API_PREFIX}/order/trade",
        request_model=V1OrderTradeGetParametersQuery,
        response_model=PageOfTradeDtos,
        **kwargs,
    )
    return res.data


def get_order(self, id: str, **kwargs) -> OrderDto:
    """Gets a specific order by ID.

    Args:
        id (str): UUID of the order. Required.

    Other Parameters:
        **kwargs: Additional request parameters accepted by the API. Optional.

    Returns:
        OrderDto: Order information.
    """
    endpoint = f"{API_PREFIX}/order/{id}"
    response = self.get(endpoint, **kwargs)
    return OrderDto(**response)


def submit_order(
    self,
    sender: str,
    price: str,
    quantity: str,
    side: int,
    subaccount: str,
    onchain_id: float,
    order_type: str,
    time_in_force: Optional[str] = None,
    post_only: Optional[bool] = False,
    reduce_only: Optional[bool] = False,
    close: Optional[bool] = None,
    stop_price: Optional[float] = None,
    stop_type: Optional[int] = None,
    otoco_trigger: Optional[bool] = None,
    otoco_group_id: Optional[str] = None,
    dryrun: Optional[bool] = False,
    **kwargs,
) -> Union[OrderDto, OrderDryRunDto]:
    """Submits a new order.

    Args:
        sender (str): Address of the sender. Required.
        price (str): Order price. Required.
        quantity (str): Order quantity. Required.
        side (int): Order side (BUY = 0, SELL = 1). Required.
        subaccount (str): Subaccount name as a bytes string. Required.
        onchain_id (float): On-chain product ID. Required.
        order_type (str): Type of order (LIMIT/MARKET). Required.
        time_in_force (str, optional): Time in force for limit orders. Optional.
        post_only (bool, optional): Post-only flag for limit orders. Optional.
        reduce_only (bool, optional): Reduce-only flag. Optional.
        close (bool, optional): Whether the order is a close order. Optional.
        stop_price (float, optional): The stop price for stop orders. Optional.
        stop_type (int, optional): The stop type (0 = STOP, 1 = STOP_LIMIT). Optional.
        otoco_trigger (bool, optional): Whether the order is an OCO or OTO trigger. Optional.
        otoco_group_id (str, optional): The OCO or OTO group ID. Optional.
        dryrun (bool, optional): Dry-run flag. If provided, the order will be submitted to the
            `dry-run` endpoint, otherwise it will be submitted. Optional.

    Other Parameters:
        **kwargs: Additional request parameters accepted by the API. Optional.

    Returns:
        OrderDto or OrderDryRunDto: Created order information or dry-run result.
    """
    domain = self.rpc_config.domain.model_dump(mode="json", by_alias=True)
    primary_type = "TradeOrder"
    types = self.chain.get_signature_types(self.rpc_config, primary_type)

    signed_at = str(int(time.time()))
    nonce = generate_nonce()

    # Common order data
    order_data = {
        "sender": sender,
        "subaccount": subaccount,
        "quantity": quantity,
        "price": price,
        "side": side,
        "engineType": 0,  # PERP
        "onchainId": onchain_id,
        "nonce": nonce,
        "type": order_type,
        "reduceOnly": reduce_only,
        "signedAt": signed_at,
        "close": close,
        "stopPrice": stop_price,
        "stopType": stop_type,
        "otocoTrigger": otoco_trigger,
        "otocoGroupId": otoco_group_id,
    }

    message = {
        "sender": sender,
        "subaccount": subaccount,
        "quantity": int(float(quantity) * 1e9),
        "price": int(float(price) * 1e9),
        "reduceOnly": reduce_only,
        "side": side,
        "engineType": 0,
        "productId": int(onchain_id),
        "nonce": nonce,
        "signedAt": signed_at,
    }

    # Create specific order data based on type
    if order_type == "LIMIT":
        order_data.update(
            {
                "timeInForce": time_in_force,
                "postOnly": post_only,
            }
        )
        data_model: Union[SubmitOrderLimitDtoData, SubmitOrderMarketDtoData] = (
            SubmitOrderLimitDtoData.model_validate(order_data)
        )
    elif order_type == "MARKET":
        data_model = SubmitOrderMarketDtoData.model_validate(order_data)
    else:
        raise ValueError(f"Invalid order type: {order_type}")

    if dryrun:
        submit_order_dry = SubmitDryOrderDto(data=data_model)

        endpoint = f"{API_PREFIX}/order/dry-run"
        res = self.post(
            endpoint,
            data=submit_order_dry.model_dump(mode="json", by_alias=True),
            **kwargs,
        )
        return OrderDryRunDto.model_validate(res)
    else:
        # Prepare signature
        signature = self.chain.sign_message(
            self.chain.private_key, domain, types, primary_type, message
        )
        submit_order = SubmitOrderDto(data=data_model, signature=signature)
        endpoint = f"{API_PREFIX}/order/submit"
        res = self.post(
            endpoint,
            data=submit_order.model_dump(mode="json", by_alias=True, exclude_none=True),
            **kwargs,
        )
        return OrderDto(**res)


def cancel_order(
    self, order_id: str, sender: str, subaccount: str, **kwargs
) -> List[CancelOrderResultDto]:
    """Cancels an existing order.

    Args:
        order_id (str): UUID of the order to cancel. Required.
        sender (str): Address of the sender. Required.
        subaccount (str): Subaccount name as a bytes string. Required.

    Other Parameters:
        **kwargs: Additional request parameters accepted by the API. Optional.

    Returns:
        List[CancelOrderResultDto]: List of canceled orders.
    """
    endpoint = f"{API_PREFIX}/order/cancel"

    domain = self.rpc_config.domain.model_dump(mode="json", by_alias=True)
    primary_type = "CancelOrder"
    types = self.chain.get_signature_types(self.rpc_config, primary_type)

    nonce = generate_nonce()

    data = CancelOrderDtoData(
        sender=sender, subaccount=subaccount, nonce=nonce, orderIds=[order_id]
    )

    # Prepare message for signing
    message = data.model_dump(mode="json", by_alias=True)
    message["orderIds"] = [uuid_to_bytes32(order_id)]

    signature = self.chain.sign_message(
        self.chain.private_key, domain, types, primary_type, message
    )

    cancel_order = CancelOrderDto(data=data, signature=signature)

    response = self.post(
        endpoint, data=cancel_order.model_dump(mode="json", by_alias=True), **kwargs
    )
    return [CancelOrderResultDto(**o) for o in response.get("data", [])]


def cancel_orders(
    self, order_ids: List[str], sender: str, subaccount: str, **kwargs
) -> List[CancelOrderResultDto]:
    """Cancels a set of existing orders.

    Args:
        order_ids (List[str]): UUIDs of the orders to cancel. Required.
        sender (str): Address of the sender. Required.
        subaccount (str): Subaccount name as a bytes string. Required.

    Other Parameters:
        **kwargs: Additional request parameters accepted by the API. Optional.

    Returns:
        List[CancelOrderResultDto]: List of canceled orders.
    """
    endpoint = f"{API_PREFIX}/order/cancel"

    domain = self.rpc_config.domain.model_dump(mode="json", by_alias=True)
    primary_type = "CancelOrder"
    types = self.chain.get_signature_types(self.rpc_config, primary_type)

    nonce = generate_nonce()

    data = CancelOrderDtoData(
        sender=sender, subaccount=subaccount, nonce=nonce, orderIds=order_ids
    )

    # Prepare message for signing
    message = data.model_dump(mode="json", by_alias=True)
    message["orderIds"] = [uuid_to_bytes32(order_id) for order_id in order_ids]

    signature = self.chain.sign_message(
        self.chain.private_key, domain, types, primary_type, message
    )

    cancel_order = CancelOrderDto(data=data, signature=signature)

    response = self.post(
        endpoint, data=cancel_order.model_dump(mode="json", by_alias=True), **kwargs
    )
    return [CancelOrderResultDto(**o) for o in response.get("data", [])]
