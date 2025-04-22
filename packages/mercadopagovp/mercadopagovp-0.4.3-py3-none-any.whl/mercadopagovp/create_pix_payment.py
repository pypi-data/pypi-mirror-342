# Version: 1.0.1
# Author: Reinan Br
# Date: 2021-07-07
# This is the CreatePixPayment class responsible for creating PIX payments on MercadoPago.

import mercadopago
from datetime import datetime, timedelta
from mercadopagovp.load_sdk import LoadSDK
from mercadopagovp.pix_payment import PixPayment
from kitano import puts
import pytz


class CreatePixPayment:
    """Class responsible for creating PIX payments on MercadoPago."""

    def __init__(self, key_sdk: str | bool = None):
        """
        Initializes the CreatePixPayment class.

        Args:
            key_sdk (str | bool, optional): SDK key for MercadoPago. Defaults to None.
        """
        self.sdk = LoadSDK(key_sdk=key_sdk).get_sdk() if key_sdk else LoadSDK().get_sdk()
        self.notification_url = None
        self.first_name = None
        self.last_name = None
        self.value = None
        self.email = None
        self.date_limit = None

    def set_url_notification(self, notification_url: str) -> None:
        """
        Sets the notification URL for the payment.

        Args:
            notification_url (str): Notification URL.
        """
        self.notification_url = notification_url

    def set_value(self, value: float) -> None:
        """
        Sets the payment amount.

        Args:
            value (float): Payment amount.

        Raises:
            ValueError: If the amount is less than R$2.00.
        """
        if value < 2.00:
            raise ValueError("The minimum allowed amount is R$2.00.")
        self.value = value
        puts(f"Payment value set: {value}")

    def set_time_limit(self, minutes: int) -> None:
        """
        Sets the expiration time limit for the payment.

        Args:
            minutes (int): Number of minutes until expiration.
        """
        timezone = pytz.timezone("America/Sao_Paulo")
        expiration_time = datetime.now(timezone) + timedelta(minutes=minutes)
        offset = expiration_time.strftime('%z')
        offset_formatted = f"{offset[:3]}:{offset[3:]}"
        self.date_limit = expiration_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + offset_formatted
        puts(f"Expiration time limit set: {self.date_limit}")
        

    def set_firtname(self, firstname):
        """
        Sets the first name of the client.
        Args:
            firstname (str): First name of the client.
        """
        self.first_name = firstname
        puts(f"Client first name set: {firstname}")
        
        
    def set_lastname(self, lastname):
        """
        Sets the last name of the client.
        Args:
            lastname (str): Last name of the client.
        """
        self.last_name = lastname
        puts(f"Client last name set: {lastname}")
        
        
    def set_email(self, email):
        """
        Sets the email of the client.
        Args:
            email (str): Email of the client.
        """
        self.email = email
        puts(f"Client email set: {email}")


    def create_payment(self, description: str) -> PixPayment:
        """
        Creates a PIX payment.

        Args:
            description (str): Payment description.

        Returns:
            PixPayment: Object representing the created payment.

        Raises:
            ValueError: If required details are missing.
        """
        if not all([self.first_name, self.last_name, self.email, self.value]):
            raise ValueError("All client details and value must be set before creating a payment.")

        data = {
            "payer": {
                "email": self.email,
                "first_name": self.first_name,
                "last_name": self.last_name
            },
            "payment_method_id": "pix",
            "transaction_amount": self.value,
            "description": description,
            "notification_url": self.notification_url,
            "date_of_expiration": self.date_limit,
        }
        puts(f"Payment data:\n{data}")

        try:
            puts("Creating payment...")
            request_options = mercadopago.config.RequestOptions()
            payment_pix = self.sdk.payment().create(data, request_options)
            puts(f"Payment created: {payment_pix}")

            response = payment_pix['response']
            date_expiration = datetime.fromisoformat(response['date_of_expiration'])
            date_now = datetime.now(pytz.timezone("America/Sao_Paulo"))
            delta_time = (date_expiration - date_now).total_seconds()

            return PixPayment(
                id=response['id'],
                amount=response['transaction_amount'],
                qr_code=response['point_of_interaction']['transaction_data']['qr_code'],
                qr_code_base64=response['point_of_interaction']['transaction_data']['qr_code_base64'],
                description=response['description'],
                payment_method=response['payment_method_id'],
                currency_id=response['currency_id'],
                date_last_updated=response['date_last_updated'],
                ticket_url=response['transaction_details']['external_resource_url'],
                date_init=response['date_created'],
                date_end=response['date_of_expiration'],
                status_code=response['status'],
                status_payment=response['status_detail'],
                time_to_end=delta_time,
                sdk=self.sdk
            )
        except Exception as e:
            puts(f"Error creating payment: {e}")
            return None
