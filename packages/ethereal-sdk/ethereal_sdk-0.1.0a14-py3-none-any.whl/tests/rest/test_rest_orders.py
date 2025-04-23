"""Test simple REST API calls for submitting orders"""

import pytest
import time
from typing import List
from ethereal.models.rest import OrderDto, OrderDryRunDto, CancelOrderResultDto


def test_rest_limit_order_submit_cancel(rc, sid):
    """Test submitting and cancelling a limit order."""
    subaccount = [s for s in rc.subaccounts if s.id == sid][0]

    pid = rc.products[0].id
    tick_size = float(rc.products_by_id[pid].tick_size)
    prices = rc.list_market_prices(product_ids=[pid])[0]
    best_bid_price = float(prices.best_bid_price)

    # bid 10% below the best bid price
    bid_price = best_bid_price * 0.90
    bid_price = round(bid_price / tick_size) * tick_size
    order_params = {
        "order_type": "LIMIT",
        "product_id": pid,
        "side": 0,
        "price": bid_price,
        "quantity": 0.001,
        "time_in_force": "GTD",
        "post_only": False,
    }
    order = rc.create_order(**order_params)
    rc.logger.info(f"Limit order: {order}")
    assert isinstance(order, OrderDto)

    # cancel the order
    cancelled_orders = rc.cancel_order(
        sender=rc.chain.address, subaccount=subaccount.name, order_id=order.id
    )
    rc.logger.info(f"Cancelled orders: {cancelled_orders}")
    assert isinstance(cancelled_orders, List)
    assert all(isinstance(o, CancelOrderResultDto) for o in cancelled_orders)


def test_rest_limit_order_submit_cancel_multiple(rc, sid):
    """Test submitting and cancelling multiple limit orders."""
    subaccount = [s for s in rc.subaccounts if s.id == sid][0]

    pid = rc.products[0].id
    tick_size = float(rc.products_by_id[pid].tick_size)
    prices = rc.list_market_prices(product_ids=[pid])[0]
    best_bid_price = float(prices.best_bid_price)

    # bid 10% below the best bid price
    bid_price = best_bid_price * 0.90
    bid_price = round(bid_price / tick_size) * tick_size
    order_params = {
        "order_type": "LIMIT",
        "product_id": pid,
        "side": 0,
        "price": bid_price,
        "quantity": 0.001,
        "time_in_force": "GTD",
        "post_only": False,
    }

    order_ids_to_cancel = []
    for i in range(2):
        order = rc.create_order(**order_params)
        rc.logger.info(f"Limit order: {order}")
        assert isinstance(order, OrderDto)

        # append the order ID to the list of orders to cancel
        order_ids_to_cancel.append(order.id)

    # cancel the orders
    cancelled_orders = rc.cancel_orders(
        sender=rc.chain.address,
        subaccount=subaccount.name,
        order_ids=order_ids_to_cancel,
    )
    rc.logger.info(f"Cancelled orders: {cancelled_orders}")
    assert isinstance(cancelled_orders, List)
    assert all(isinstance(o, CancelOrderResultDto) for o in cancelled_orders)


def test_rest_limit_order_submit_cancel_all(rc, sid):
    """Test submitting and cancelling several limit orders simultaneously."""
    subaccount = [s for s in rc.subaccounts if s.id == sid][0]
    pid = rc.products[0].id

    # start by cancelling all orders
    cancelled_orders = rc.cancel_all_orders(
        sender=rc.chain.address, subaccount_id=subaccount.id, product_ids=[pid]
    )

    tick_size = float(rc.products_by_id[pid].tick_size)
    prices = rc.list_market_prices(product_ids=[pid])[0]
    best_bid_price = float(prices.best_bid_price)

    # bid 10% below the best bid price
    order_ids = []
    for i in range(5):
        bid_price = best_bid_price * (0.90 + i * 0.01)
        bid_price = round(bid_price / tick_size) * tick_size
        order_params = {
            "order_type": "LIMIT",
            "product_id": pid,
            "side": 0,
            "price": bid_price,
            "quantity": 0.001,
        }
        order = rc.create_order(**order_params)
        assert isinstance(order, OrderDto)

        order_ids.append(order.id)
    rc.logger.info(f"Order ids: {order_ids}")

    # cancel the orders
    cancelled_orders = rc.cancel_all_orders(
        sender=rc.chain.address, subaccount_id=subaccount.id, product_ids=[pid]
    )
    rc.logger.info(f"Cancelled orders: {cancelled_orders}")
    assert isinstance(cancelled_orders, List)
    assert len(cancelled_orders) == len(order_ids)
    assert all(isinstance(o, CancelOrderResultDto) for o in cancelled_orders)
    assert all([o.success for o in cancelled_orders])

    # check each of the orders
    # wait for the orders to be cancelled
    time.sleep(1)
    for order_id in order_ids:
        order = rc.get_order(id=order_id)
        assert isinstance(order, OrderDto)
        assert order.status.value == "CANCELED"


def test_rest_limit_order_submit_cancel_all_specify_products(rc, sid):
    """Test submitting and cancelling several limit orders simultaneously.
    This test uses multiple products to test the order cancellation process."""
    subaccount = [s for s in rc.subaccounts if s.id == sid][0]

    order_ids = {}
    for i in range(2):
        pid = rc.products[i].id
        tick_size = float(rc.products_by_id[pid].tick_size)
        lot_size = float(rc.products_by_id[pid].lot_size)
        prices = rc.list_market_prices(product_ids=[pid])[0]
        best_bid_price = float(prices.best_bid_price)

        # bid 10% below the best bid price
        order_ids[pid] = []
        for j in range(5):
            bid_price = best_bid_price * (0.90 + j * 0.01)
            bid_price = round(bid_price / tick_size) * tick_size
            order_params = {
                "order_type": "LIMIT",
                "product_id": pid,
                "side": 0,
                "price": bid_price,
                "quantity": lot_size,
                "time_in_force": "GTD",
                "post_only": False,
            }
            order = rc.create_order(**order_params)
            assert isinstance(order, OrderDto)

            order_ids[pid].append(order.id)

    rc.logger.info(f"Order ids: {order_ids}")

    # cancel the orders for product 1
    cancelled_orders = rc.cancel_all_orders(
        sender=rc.chain.address,
        subaccount_id=subaccount.id,
        product_ids=[rc.products[0].id],
    )
    rc.logger.info(f"Cancelled orders: {cancelled_orders}")
    assert isinstance(cancelled_orders, List)
    assert len(cancelled_orders) == len(order_ids[rc.products[0].id])
    assert all(isinstance(o, CancelOrderResultDto) for o in cancelled_orders)
    assert all([o.success for o in cancelled_orders])

    # check each of the orders
    # wait for the orders to be cancelled
    time.sleep(1)
    for order_id in order_ids[rc.products[0].id]:
        order = rc.get_order(id=order_id)
        assert isinstance(order, OrderDto)
        assert order.status.value == "CANCELED"

    for order_id in order_ids[rc.products[1].id]:
        order = rc.get_order(id=order_id)
        assert isinstance(order, OrderDto)
        assert order.status.value == "NEW"

    # cancel the orders for product 2
    cancelled_orders = rc.cancel_all_orders(
        sender=rc.chain.address,
        subaccount_id=subaccount.id,
        product_ids=[rc.products[1].id],
    )
    rc.logger.info(f"Cancelled orders: {cancelled_orders}")
    assert isinstance(cancelled_orders, List)
    assert len(cancelled_orders) == len(order_ids[rc.products[1].id])
    assert all(isinstance(o, CancelOrderResultDto) for o in cancelled_orders)
    assert all([o.success for o in cancelled_orders])

    # check each of the orders
    # wait for the orders to be cancelled
    time.sleep(1)
    for order_id in order_ids[rc.products[1].id]:
        order = rc.get_order(id=order_id)
        assert isinstance(order, OrderDto)
        assert order.status.value == "CANCELED"


def test_rest_limit_order_submit_cancel_all_multiple_products(rc, sid):
    """Test submitting and cancelling several limit orders simultaneously.
    This test uses multiple products to test the order cancellation process
    across two products at once."""
    subaccount = [s for s in rc.subaccounts if s.id == sid][0]

    order_ids = []
    for i in range(2):
        pid = rc.products[i].id
        tick_size = float(rc.products_by_id[pid].tick_size)
        lot_size = float(rc.products_by_id[pid].lot_size)
        prices = rc.list_market_prices(product_ids=[pid])[0]
        best_bid_price = float(prices.best_bid_price)

        # bid 10% below the best bid price
        for j in range(5):
            bid_price = best_bid_price * (0.90 + j * 0.01)
            bid_price = round(bid_price / tick_size) * tick_size
            order_params = {
                "order_type": "LIMIT",
                "product_id": pid,
                "side": 0,
                "price": bid_price,
                "quantity": lot_size,
                "time_in_force": "GTD",
                "post_only": False,
            }
            order = rc.create_order(**order_params)
            assert isinstance(order, OrderDto)

            order_ids.append(order.id)

    rc.logger.info(f"Order ids: {order_ids}")

    # cancel the orders
    cancelled_orders = rc.cancel_all_orders(
        sender=rc.chain.address,
        subaccount_id=subaccount.id,
    )
    rc.logger.info(f"Cancelled orders: {cancelled_orders}")
    assert isinstance(cancelled_orders, List)
    assert len(cancelled_orders) == len(order_ids)
    assert all(isinstance(o, CancelOrderResultDto) for o in cancelled_orders)
    assert all([o.success for o in cancelled_orders])

    # check each of the orders
    # wait for the orders to be cancelled
    time.sleep(1)
    for order_id in order_ids:
        order = rc.get_order(id=order_id)
        assert isinstance(order, OrderDto)
        assert order.status.value == "CANCELED"


def test_rest_limit_order_dry(rc, sid):
    """Test dry running a limit order."""
    pid = rc.products[0].id
    tick_size = float(rc.products_by_id[pid].tick_size)
    prices = rc.list_market_prices(product_ids=[pid])[0]
    best_bid_price = float(prices.best_bid_price)

    # bid 10% below the best bid price
    bid_price = best_bid_price * 0.90
    bid_price = round(bid_price / tick_size) * tick_size
    order_params = {
        "order_type": "LIMIT",
        "product_id": pid,
        "side": 0,
        "price": bid_price,
        "quantity": 0.001,
        "time_in_force": "GTD",
        "post_only": False,
        "dry_run": True,
    }
    order = rc.create_order(**order_params)
    rc.logger.info(f"Limit order: {order}")
    assert isinstance(order, OrderDryRunDto)


def test_rest_market_order_dry(rc, sid):
    """Test dry running a market order."""
    pid = rc.products[0].id
    order_params = {
        "order_type": "MARKET",
        "product_id": pid,
        "side": 0,
        "quantity": 0.001,
        "dry_run": True,
    }
    order = rc.create_order(**order_params)
    rc.logger.info(f"Market order: {order}")
    assert isinstance(order, OrderDryRunDto)


def test_rest_market_order_submit(rc, sid):
    """Test submitting a market order."""
    pid = rc.products[0].id
    order_params = {
        "order_type": "MARKET",
        "product_id": pid,
        "side": 0,
        "quantity": 0.001,
    }
    order = rc.create_order(**order_params)
    rc.logger.info(f"Market order: {order}")
    assert isinstance(order, OrderDto)


def test_rest_market_order_submit_close(rc, sid):
    """Test submitting a market order then a close order."""
    pid = rc.products[0].id
    order_1_params = {
        "order_type": "MARKET",
        "product_id": pid,
        "side": 0,
        "quantity": 0.001,
    }
    order_1 = rc.create_order(**order_1_params)
    rc.logger.info(f"Market order: {order_1}")
    assert isinstance(order_1, OrderDto)

    # close the order
    order_2_params = {
        "order_type": "MARKET",
        "product_id": pid,
        "side": 1,
        "quantity": 0,
        "reduce_only": True,
        "close": True,
    }
    order_2 = rc.create_order(**order_2_params)
    rc.logger.info(f"Close order: {order_2}")
    assert isinstance(order_2, OrderDto)


def test_rest_limit_order_with_stop(rc, sid):
    """Test submitting a limit order with stop parameters."""
    pid = rc.products[0].id
    tick_size = float(rc.products_by_id[pid].tick_size)
    prices = rc.list_market_prices(product_ids=[pid])[0]
    best_bid_price = float(prices.best_bid_price)

    # bid 10% below the best bid price
    bid_price = best_bid_price * 0.90
    bid_price = round(bid_price / tick_size) * tick_size
    stop_price = best_bid_price * 0.80
    stop_price = round(stop_price / tick_size) * tick_size

    order_params = {
        "order_type": "LIMIT",
        "product_id": pid,
        "side": 0,
        "price": bid_price,
        "quantity": 0.001,
        "time_in_force": "GTD",
        "post_only": False,
        "stop_type": 1,
        "stop_price": stop_price,
    }
    order = rc.create_order(**order_params)
    rc.logger.info(f"Limit order: {order}")
    assert isinstance(order, OrderDto)


def test_rest_limit_order_with_otoco(rc, sid):
    """Test submitting a limit order with OCO parameters."""
    subaccount = [s for s in rc.subaccounts if s.id == sid][0]
    pid = rc.products[0].id
    tick_size = float(rc.products_by_id[pid].tick_size)
    prices = rc.list_market_prices(product_ids=[pid])[0]
    best_bid_price = float(prices.best_bid_price)

    # bid 10% below the best bid price
    bid_price = best_bid_price * 0.90
    bid_price = round(bid_price / tick_size) * tick_size
    order_params = {
        "order_type": "LIMIT",
        "product_id": pid,
        "side": 0,
        "price": bid_price,
        "quantity": 0.001,
        "time_in_force": "GTD",
        "post_only": False,
        "otoco_trigger": True,
    }
    order = rc.create_order(**order_params)
    rc.logger.info(f"Limit order: {order}")
    assert isinstance(order, OrderDto)

    # cancel it
    cancelled_orders = rc.cancel_order(
        sender=rc.chain.address, subaccount=subaccount.name, order_id=order.id
    )
    assert isinstance(cancelled_orders, List)
    assert all(isinstance(o, CancelOrderResultDto) for o in cancelled_orders)


def test_rest_limit_orders_with_otoco_group(rc, sid):
    """Test submitting a limit order with OCO and add order to group."""
    subaccount = [s for s in rc.subaccounts if s.id == sid][0]
    pid = rc.products[0].id
    tick_size = float(rc.products_by_id[pid].tick_size)
    prices = rc.list_market_prices(product_ids=[pid])[0]
    best_bid_price = float(prices.best_bid_price)

    # bid 10% below the best bid price
    bid_price = best_bid_price * 0.90
    bid_price = round(bid_price / tick_size) * tick_size
    order_1_params = {
        "order_type": "LIMIT",
        "product_id": pid,
        "side": 0,
        "price": bid_price,
        "quantity": 0.001,
        "time_in_force": "GTD",
        "post_only": False,
        "otoco_trigger": True,
    }
    order_1 = rc.create_order(**order_1_params)
    rc.logger.info(f"Limit order: {order_1}")
    assert isinstance(order_1, OrderDto)

    otoco_group = order_1.otoco_group_id
    order_2_params = {
        "order_type": "LIMIT",
        "product_id": pid,
        "side": 0,
        "price": bid_price,
        "quantity": 0.001,
        "time_in_force": "GTD",
        "post_only": False,
        "otoco_group_id": otoco_group,
    }
    order_2 = rc.create_order(**order_2_params)
    rc.logger.info(f"Limit order: {order_2}")
    assert isinstance(order_2, OrderDto)

    # cancel both
    cancelled_orders = rc.cancel_orders(
        sender=rc.chain.address,
        subaccount=subaccount.name,
        order_ids=[order_1.id, order_2.id],
    )
    assert isinstance(cancelled_orders, List)
    assert all(isinstance(o, CancelOrderResultDto) for o in cancelled_orders)


def test_rest_market_order_submit_read_only(rc_ro, sid):
    """Test submitting a market order from a read-only client fails."""
    pid = rc_ro.products[0].id
    order_params = {
        "order_type": "MARKET",
        "product_id": pid,
        "side": 0,
        "quantity": 0.001,
    }

    with pytest.raises(Exception):
        rc_ro.create_order(**order_params)


def test_rest_limit_order_submit_replace_cancel(rc, sid):
    """Test submitting, replacing, and cancelling a limit order."""
    subaccount = [s for s in rc.subaccounts if s.id == sid][0]

    pid = rc.products[0].id
    tick_size = float(rc.products_by_id[pid].tick_size)
    prices = rc.list_market_prices(product_ids=[pid])[0]
    best_bid_price = float(prices.best_bid_price)

    # bid 10% below the best bid price
    bid_price = best_bid_price * 0.90
    bid_price = round(bid_price / tick_size) * tick_size
    order_params = {
        "order_type": "LIMIT",
        "product_id": pid,
        "side": 0,
        "price": bid_price,
        "quantity": 0.001,
        "time_in_force": "GTD",
        "post_only": False,
    }
    order = rc.create_order(**order_params)
    rc.logger.info(f"Limit order: {order}")
    assert isinstance(order, OrderDto)

    # replace the order
    new_price = float(order.price) * 1.01
    new_price = round(new_price / tick_size) * tick_size
    new_order, old_order_cancelled = rc.replace_order(
        order_id=order.id, price=new_price
    )
    rc.logger.info(f"Replaced order: {new_order}")
    assert isinstance(new_order, OrderDto)
    assert isinstance(old_order_cancelled, bool)
    assert old_order_cancelled is True
    assert new_order.id != order.id

    # check the original order
    time.sleep(1)
    order = rc.get_order(id=order.id)
    assert isinstance(order, OrderDto)
    assert order.status.value == "CANCELED"

    # cancel the order
    cancelled_orders = rc.cancel_order(
        sender=rc.chain.address, subaccount=subaccount.name, order_id=new_order.id
    )
    rc.logger.info(f"Cancelled orders: {cancelled_orders}")
    assert isinstance(cancelled_orders, List)
    assert all(isinstance(o, CancelOrderResultDto) for o in cancelled_orders)
