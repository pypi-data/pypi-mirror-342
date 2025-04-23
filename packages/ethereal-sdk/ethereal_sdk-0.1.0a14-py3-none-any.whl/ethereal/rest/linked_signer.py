from typing import List

from ethereal.constants import API_PREFIX
from ethereal.models.rest import (
    LinkSignerDto,
    LinkSignerDtoData,
    SignerDto,
    AccountSignerQuotaDto,
    V1LinkedSignerGetParametersQuery,
    PageOfSignersDto,
    V1LinkedSignerQuotaGetParametersQuery,
)
from ethereal.rest.util import generate_nonce


# TODO: Add revoke signer


def list_signers(
    self,
    **kwargs,
) -> List[SignerDto]:
    """Lists all linked signers for a subaccount.

    Args:
        subaccount_id (str): UUID of the subaccount. Required.

    Other Parameters:
        order (str, optional): Sort order, 'asc' or 'desc'. Optional.
        limit (float, optional): Maximum number of results to return. Optional.
        cursor (str, optional): Pagination cursor for fetching the next page. Optional.
        active (bool, optional): Filter for active signers. Optional.
        order_by (str, optional): Field to order by, e.g., 'createdAt'. Optional.
        **kwargs: Additional request parameters accepted by the API. Optional.

    Returns:
        List[SignerDto]: List of linked signers for the subaccount.
    """
    res = self.get_validated(
        url_path=f"{API_PREFIX}/linked-signer",
        request_model=V1LinkedSignerGetParametersQuery,
        response_model=PageOfSignersDto,
        **kwargs,
    )
    return res.data


def get_signer(
    self,
    id: str,
    **kwargs,
) -> SignerDto:
    """Gets a specific linked signer by ID.

    Args:
        id (str): UUID of the signer. Required.

    Other Parameters:
        **kwargs: Additional request parameters accepted by the API. Optional.

    Returns:
        SignerDto: Linked signer information.
    """
    endpoint = f"{API_PREFIX}/linked-signer/{id}"
    res = self.get(endpoint, **kwargs)
    return SignerDto(**res)


def get_signer_quota(
    self,
    **kwargs,
) -> AccountSignerQuotaDto:
    """Gets the signer quota configuration for a subaccount.

    Args:
        subaccount_id (str): UUID of the subaccount. Required.

    Other Parameters:
        **kwargs: Additional request parameters accepted by the API. Optional.

    Returns:
        AccountSignerQuotaDto: Signer quota configuration for the subaccount.
    """
    res = self.get_validated(
        url_path=f"{API_PREFIX}/linked-signer/quota",
        request_model=V1LinkedSignerQuotaGetParametersQuery,
        response_model=AccountSignerQuotaDto,
        **kwargs,
    )
    return res


def link_signer(
    self,
    sender: str,
    signer: str,
    signerSignature: str,
    subaccount: str,
    subaccountId: str,
    **kwargs,
) -> SignerDto:
    """Links a new signer to a subaccount.

    Args:
        sender (str): Address of the sender. Required.
        signer (str): Address of the signer to be linked. Required.
        signerSignature (str): Signature from the signer. Required.
        subaccount (str): Address of the subaccount. Required.
        subaccountId (str): UUID of the subaccount. Required.

    Other Parameters:
        **kwargs: Additional request parameters accepted by the API. Optional.

    Returns:
        SignerDto: Information about the newly linked signer.
    """
    endpoint = f"{API_PREFIX}/linked-signer/link"

    domain = self.rpc_config.domain.model_dump(mode="json", by_alias=True)
    primary_type = "LinkSigner"
    types = self.chain.get_signature_types(self.rpc_config, primary_type)

    data = {
        "sender": sender,
        "signer": signer,
        "subaccountId": subaccountId,
        "subaccount": subaccount,
        "nonce": generate_nonce(),
    }
    model_data = LinkSignerDtoData.model_validate(data)
    message = model_data.model_dump(mode="json", by_alias=True)
    signature = self.chain.sign_message(
        self.chain.private_key, domain, types, primary_type, message
    )

    link_signer = LinkSignerDto(
        data=model_data, signature=signature, signerSignature=signerSignature
    )
    res = self.post(
        endpoint, data=link_signer.model_dump(mode="json", by_alias=True), **kwargs
    )
    return SignerDto(**res)
