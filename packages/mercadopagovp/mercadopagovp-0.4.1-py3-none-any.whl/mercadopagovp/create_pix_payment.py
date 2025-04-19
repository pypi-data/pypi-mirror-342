# Version: 1.0.1
# Author: Reinan Br
# Date: 2021-07-07
# This is the CreatePixPayment class that is responsible for creating PIX payments on MercadoPago.
# It contains the methods set_value, create_client, create_payment, and the constructor __init__.
# from mercadopago import mercadopago

import mercadopago
from datetime import datetime, timedelta
from mercadopagovp.load_sdk import LoadSDK
from dataclasses import dataclass
from mercadopagovp.pix_payment import PixPayment
from kitano import puts
import pytz

class CreatePixPayment:
    """Class responsible for creating PIX payments on MercadoPago."""
    
    def __init__(self, key_sdk: str|bool=None):
        """
        Initializes the CreatePixPayment class.

        Args:
            notification_url (str, optional): Notification URL for the payment.
        """
        if key_sdk:
            self.sdk = LoadSDK(key_sdk=key_sdk).get_sdk()
        else:
            self.sdk = LoadSDK().get_sdk()
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
        puts(f"Setting payment value: {value}")
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
    
    def set_time_limit(self, minutes: int) -> None:
        """
        Sets the expiration time limit for the payment in Mercado Pago Pix format.

        Args:
            minutes (int): Number of minutes until expiration.
        """
        timezone = pytz.timezone("America/Sao_Paulo")
        expiration_time = datetime.now(timezone) + timedelta(minutes=minutes)

        # Constrói a string no formato: "2025-03-06T11:02:55.203-04:00"
        offset = expiration_time.strftime('%z')  # ex: -0300
        offset_formatted = f"{offset[:3]}:{offset[3:]}"  # ex: -03:00
        expiration_str = expiration_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + offset_formatted

        self.date_limit = expiration_str
        puts(f"Setting expiration time limit: {self.date_limit}")
            
        
    def create_client(self, first_name: str, last_name: str, email: str) -> None:
        """
        Sets client details.

        Args:
            first_name (str): Client's first name.
            last_name (str): Client's last name.
            email (str): Client's email.
        """
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        puts(f"Client details set: {self.first_name} {self.last_name}, Email: {self.email}")
    
    def create_payment(self, description: str) -> PixPayment:
        """
        Creates a PIX payment.

        Args:
            description (str): Payment description.

        Returns:
            PixPayment: Object representing the created payment.
        """
        puts("Creating data payment...")
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
        puts(f"Payment data:\n {data}")
        try:
            puts("Creating payment...")
            request_options = mercadopago.config.RequestOptions()
            puts(f"Setting request options: {request_options}")
            payment_pix = self.sdk.payment().create(data, request_options)
            puts(f"Payment created: {payment_pix}")
            date_expiration = datetime.fromisoformat(payment_pix['response']['date_of_expiration'])
            date_created = datetime.fromisoformat(payment_pix['response']['date_created'])
            date_now = datetime.now(pytz.timezone("America/Sao_Paulo"))
            delta_time = (date_expiration - date_now).total_seconds()
            return PixPayment(
                id=payment_pix['response']['id'],
                amount=payment_pix['response']['transaction_amount'],
                qr_code=payment_pix['response']['point_of_interaction']['transaction_data']['qr_code'],
                description=payment_pix['response']['description'],
                currency_id=payment_pix['response']['currency_id'],
                date_last_updated=payment_pix['response']['date_last_updated'],
                ticket_url=payment_pix['response']['transaction_details']['external_resource_url'],
                date_init=payment_pix['response']['date_created'],
                date_end=payment_pix['response']['date_of_expiration'],
                status_code=payment_pix['response']['status'],
                status_payment=payment_pix['response']['status_detail'],
                time_to_end=delta_time,
                sdk=self.sdk
            )
        except Exception as e:
            print(f"Error creating payment: {e}")
            return None
