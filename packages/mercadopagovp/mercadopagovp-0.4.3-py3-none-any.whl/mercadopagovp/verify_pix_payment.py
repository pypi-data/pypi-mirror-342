# Version: 1.0.1
# Author: Reinan Br
# Date: 2021-07-07
# This is the VerifyPixPayment class that is responsible for verifying the status of a PIX payment.
# It contains the method verify_payment that returns a PixPayment object representing the verified payment.
# from mercadopago import mercadopago

import mercadopago
from datetime import datetime
from mercadopagovp.load_sdk import LoadSDK
from dataclasses import dataclass
from mercadopagovp.pix_payment import PixPayment
import pytz


class VerifyPixPayment:
    """Class responsible for verifying the status of a PIX payment."""
    
    def __init__(self,key_sdk: str|bool=None):
        """
        Initializes the VerifyPixPayment class.

        Args:
            payment_id (str): ID of the payment to be verified.
        """
        self.sdk = LoadSDK(key_sdk=key_sdk).get_sdk()
    
    def verify_payment(self,payment_id) -> PixPayment:
        """
        Verifies the status of a PIX payment.

        Returns:
            PixPayment: Object representing the verified payment.
        """
        request = mercadopago.config.RequestOptions()
        payment_response = self.sdk.payment().get(payment_id, request)
        date_expiration = datetime.fromisoformat(payment_response['response']['date_of_expiration'])
        date_created = datetime.fromisoformat(payment_response['response']['date_created'])
        date_now = datetime.now(pytz.timezone("America/Sao_Paulo"))
        delta_time = int((date_expiration - date_now).total_seconds())
        return PixPayment(
            id=payment_response['response']['id'],
            amount=payment_response['response']['transaction_amount'],
            qr_code=payment_response['response']['point_of_interaction']['transaction_data']['qr_code'],
            qr_code_base64=payment_response['response']['point_of_interaction']['transaction_data']['qr_code_base64'],
            description=payment_response['response']['description'],
            currency_id=payment_response['response']['currency_id'],
            payment_method=payment_response['response']['payment_method_id'],
            date_last_updated=payment_response['response']['date_last_updated'],
            ticket_url=payment_response['response']['transaction_details']['external_resource_url'],
            date_init=payment_response['response']['date_created'],
            date_end=payment_response['response']['date_of_expiration'],
            status_code=payment_response['response']['status'],
            status_payment=payment_response['response']['status_detail'],
            time_to_end=delta_time,
            sdk=self.sdk
        )