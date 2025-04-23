import time
from decimal import Decimal
from typing import List

from ethereal.constants import API_PREFIX
from ethereal.models.rest import (
    TokenDto,
    WithdrawDto,
    TransferDto,
    InitiateWithdrawDto,
    InitiateWithdrawDtoData,
    V1TokenGetParametersQuery,
    V1TokenTransferGetParametersQuery,
    V1TokenWithdrawGetParametersQuery,
    PageOfTokensDtos,
    PageOfTransfersDtos,
    PageOfWithdrawDtos,
)
from ethereal.rest.util import generate_nonce


def list_tokens(
    self,
    **kwargs,
) -> List[TokenDto]:
    """Lists all tokens.

    Other Parameters:
        order (str, optional): Sort order, 'asc' or 'desc'. Optional.
        limit (float, optional): Maximum number of results to return. Optional.
        cursor (str, optional): Pagination cursor for fetching the next page. Optional.
        deposit_enabled (bool, optional): Filter for deposit-enabled tokens. Optional.
        withdraw_enabled (bool, optional): Filter for withdraw-enabled tokens. Optional.
        order_by (str, optional): Field to order by, e.g., 'createdAt'. Optional.
        **kwargs: Additional request parameters accepted by the API. Optional.

    Returns:
        List[TokenDto]: A list containing all token information.
    """
    res = self.get_validated(
        url_path=f"{API_PREFIX}/token",
        request_model=V1TokenGetParametersQuery,
        response_model=PageOfTokensDtos,
        **kwargs,
    )
    return res.data


def get_token(
    self,
    id: str,
    **kwargs,
) -> TokenDto:
    """Gets a specific token by ID.

    Args:
        id (str): The token identifier. Required.

    Other Parameters:
        **kwargs: Additional request parameters accepted by the API. Optional.

    Returns:
        TokenDto: The requested token information.
    """
    endpoint = f"{API_PREFIX}/token/{id}"
    res = self.get(endpoint, **kwargs)
    return TokenDto(**res)


def list_token_withdraws(
    self,
    **kwargs,
) -> List[WithdrawDto]:
    """Lists token withdrawals for a subaccount.

    Args:
        subaccount_id (str): UUID of the subaccount. Required.

    Other Parameters:
        order (str, optional): Sort order, 'asc' or 'desc'. Optional.
        limit (float, optional): Maximum number of results to return. Optional.
        cursor (str, optional): Pagination cursor for fetching the next page. Optional.
        active (bool, optional): Filter for active withdrawals. Optional.
        order_by (str, optional): Field to order by, e.g., 'createdAt'. Optional.
        **kwargs: Additional request parameters accepted by the API. Optional.

    Returns:
        List[WithdrawDto]: A list of withdrawal information.
    """
    res = self.get_validated(
        url_path=f"{API_PREFIX}/token/withdraw",
        request_model=V1TokenWithdrawGetParametersQuery,
        response_model=PageOfWithdrawDtos,
        **kwargs,
    )
    return res.data


def list_token_transfers(
    self,
    **kwargs,
) -> List[TransferDto]:
    """Lists token transfers for a subaccount.

    Args:
        subaccount_id (str): UUID of the subaccount. Required.

    Other Parameters:
        order (str, optional): Sort order, 'asc' or 'desc'. Optional.
        limit (float, optional): Maximum number of results to return. Optional.
        cursor (str, optional): Pagination cursor for fetching the next page. Optional.
        statuses (List[str], optional): List of transfer statuses. Optional.
        order_by (str, optional): Field to order by, e.g., 'createdAt'. Optional.
        **kwargs: Additional request parameters accepted by the API. Optional.

    Returns:
        List[TransferDto]: A list of transfer information.
    """
    res = self.get_validated(
        url_path=f"{API_PREFIX}/token/transfer",
        request_model=V1TokenTransferGetParametersQuery,
        response_model=PageOfTransfersDtos,
        **kwargs,
    )
    return res.data


def withdraw_token(
    self,
    subaccount: str,
    token_id: str,
    token: str,
    amount: int,
    account: str,
    **kwargs,
):
    """Initiates a token withdrawal.

    Args:
        subaccount (str): Name of the subaccount as a string. Required.
        token_id (str): UUID of the token. Required.
        token (str): Token address. Required.
        amount (int): Amount to withdraw. Required.
        account (str): Destination address. Required.

    Other Parameters:
        **kwargs: Additional request parameters accepted by the API. Optional.

    Returns:
        WithdrawDto: The withdrawal information.
    """
    endpoint = f"{API_PREFIX}/token/{token_id}/withdraw"

    domain = self.rpc_config.domain.model_dump(mode="json", by_alias=True)
    primary_type = "InitiateWithdraw"
    types = self.chain.get_signature_types(self.rpc_config, primary_type)

    nonce = generate_nonce()
    signed_at = str(int(time.time()))

    withdraw_data = {
        "account": account,
        "subaccount": subaccount,
        "token": token,
        "amount": amount,
        "nonce": nonce,
        "signedAt": signed_at,
    }
    message = {
        "account": account,
        "subaccount": subaccount,
        "token": token,
        "amount": str(Decimal(amount * 1e9)),
        "nonce": nonce,
        "signedAt": signed_at,
    }

    data = InitiateWithdrawDtoData.model_validate(withdraw_data)
    signature = self.chain.sign_message(
        self.chain.private_key, domain, types, primary_type, message
    )

    initiate_withdraw = InitiateWithdrawDto(data=data, signature=signature)
    response = self.post(
        endpoint,
        data=initiate_withdraw.model_dump(mode="json", by_alias=True),
        **kwargs,
    )
    return WithdrawDto(**response)
