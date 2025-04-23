import decimal
from decimal import Decimal
from datetime import date, datetime
import json
import requests
import time
from typing import List
import logging
import logstash

from amper_api.complaint import *
from amper_api.order import *
from amper_api.document import *
from amper_api.cashdocument import *
from amper_api.customer import *
from amper_api.product import *
from amper_api.log import LogSeverity


class AmperJsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, (datetime, date)):
            return o.isoformat()
        if type(o) is Decimal:
            return str(o)

        return o.__dict__


class Backend:
    def __init__(self, token, amper_url, log_source="amper-translator"):
        self.token = token
        amper_url = amper_url if amper_url.endswith('/') else f'{amper_url}/'
        amper_url = amper_url if not amper_url.startswith('http://') else amper_url.replace('http://', 'https://')
        amper_url = amper_url if amper_url.startswith('https://') else f'https://{amper_url}'
        self.amper_url = amper_url

        self.amper_logger = logging.getLogger('python-logstash-logger')
        self.amper_logger.setLevel(logging.DEBUG)
        self.amper_logger.addHandler(logstash.UDPLogstashHandler('51.83.242.93', 5000, version=1))
        self.amper_logger_extra = {'translator.Source': log_source}

    def get_authorization_header(self):
        self.validate_jwt_token()
        return {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token["access_token"]}'
        }

    def validate_jwt_token(self):
        # try:
        #     result = jwt.decode(self.token['access_token'], os.environ.get('KEYCLOAK_CLIENT_PUBLIC_KEY'), algorithms=["RS256"])
        #     print(result)
        # except jwt.ExpiredSignatureError:
        #     self.token = requests.request("POST", f'{self.amper_url}auth/token-refresh/', headers=self.get_authorization_header(), data=self.token)
        pass

    def create_log_entry_async(self, severity, message, exception=None):
        if severity == LogSeverity.Info:
            self.amper_logger.info(message, exc_info=exception, extra=self.amper_logger_extra)
        elif severity == LogSeverity.Error:
            self.amper_logger.error(message, exc_info=exception, extra=self.amper_logger_extra)
        elif severity == LogSeverity.Warning:
            self.amper_logger.warning(message, exc_info=exception, extra=self.amper_logger_extra)
        elif severity == LogSeverity.Debug:
            self.amper_logger.debug(message, exc_info=exception, extra=self.amper_logger_extra)
        print(f'{severity}:{message}')

    def send_products(self, payload):
        try:
            self.create_log_entry_async(LogSeverity.Info, f"About to send {len(payload)} products records.")
            start_time = time.time()
            response = requests.request(
                "POST",
                f'{self.amper_url}/api/products-import',
                headers=self.get_authorization_header(),
                data=json.dumps(payload, cls=AmperJsonEncoder)
            )
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            if response.status_code not in [200, 201]:
                self.create_log_entry_async(LogSeverity.Error,
                                            f"FAILURE while sending products after {elapsed_time:.2f} ms; "
                                            f"{response.text}")
            else:
                self.create_log_entry_async(LogSeverity.Info, f"Success while sending products records after {elapsed_time:.2f} ms.")
        except Exception as e:
            self.create_log_entry_async(LogSeverity.Error, str(e), e)

    def send_product_categories(self, payload):
        try:
            self.create_log_entry_async(LogSeverity.Info, f"About to send {len(payload)} product categories records.")
            start_time = time.time()
            response = requests.request(
                "POST",
                f'{self.amper_url}/api/product-categories-import',
                headers=self.get_authorization_header(),
                data=json.dumps(payload, cls=AmperJsonEncoder)
            )
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            if response.status_code not in [200, 201]:
                self.create_log_entry_async(LogSeverity.Error,
                                            f"FAILURE while sending product categories after {elapsed_time:.2f} ms; "
                                            f"{response.text}")
            else:
                self.create_log_entry_async(LogSeverity.Info, f"Success while sending product categories records after {elapsed_time:.2f} ms.")
        except Exception as e:
            self.create_log_entry_async(LogSeverity.Error, str(e), e)

    def send_product_categories_relation(self, payload):
        try:
            self.create_log_entry_async(LogSeverity.Info, f"About to send {len(payload)} product categories relation records.")
            start_time = time.time()
            response = requests.request(
                "POST",
                f'{self.amper_url}/api/product-categories-relation-import',
                headers=self.get_authorization_header(),
                data=json.dumps(payload, cls=AmperJsonEncoder)
            )
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            if response.status_code not in [200, 201]:
                self.create_log_entry_async(LogSeverity.Error,
                                            f"FAILURE while sending product categories relation after {elapsed_time:.2f} ms; "
                                            f"{response.text}")
            else:
                self.create_log_entry_async(LogSeverity.Info, f"Success while sending product categories relation records after {elapsed_time:.2f} ms.")
        except Exception as e:
            self.create_log_entry_async(LogSeverity.Error, str(e), e)

    def send_accounts(self, payload):
        try:
            self.create_log_entry_async(LogSeverity.Info, f"About to send {len(payload)} accounts records.")
            start_time = time.time()
            response = requests.request(
                "POST",
                f'{self.amper_url}/api/accounts-import',
                headers=self.get_authorization_header(),
                data=json.dumps(payload, cls=AmperJsonEncoder)
            )
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            if response.status_code not in [200, 201]:
                self.create_log_entry_async(LogSeverity.Error,
                                            f"FAILURE while sending accounts after {elapsed_time:.2f} ms; "
                                            f"{response.text}")
            else:
                self.create_log_entry_async(LogSeverity.Info, f"Success while sending accounts records after {elapsed_time:.2f} ms.")
        except Exception as e:
            self.create_log_entry_async(LogSeverity.Error, str(e), e)

    def send_price_levels(self, payload):
        try:
            self.create_log_entry_async(LogSeverity.Info, f"About to send {len(payload)} price levels records.")
            start_time = time.time()
            response = requests.request(
                "POST",
                f'{self.amper_url}/api/price-levels-import',
                headers=self.get_authorization_header(),
                data=json.dumps(payload, cls=AmperJsonEncoder)
            )
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            if response.status_code not in [200, 201]:
                self.create_log_entry_async(LogSeverity.Error,
                                            f"FAILURE while sending price levels after {elapsed_time:.2f} ms; "
                                            f"{response.text}")
            else:
                self.create_log_entry_async(LogSeverity.Info,
                                            f"Success while sending price levels records after {elapsed_time:.2f} ms.")
        except Exception as e:
            self.create_log_entry_async(LogSeverity.Error, str(e), e)

    def send_prices(self, payload):
        try:
            self.create_log_entry_async(LogSeverity.Info, f"About to send {len(payload)} prices records.")
            start_time = time.time()
            response = requests.request(
                "POST",
                f'{self.amper_url}/api/prices-import',
                headers=self.get_authorization_header(),
                data=json.dumps(payload, cls=AmperJsonEncoder)
            )
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            if response.status_code not in [200, 201]:
                self.create_log_entry_async(LogSeverity.Error,
                                            f"FAILURE while sending prices after {elapsed_time:.2f} ms; "
                                            f"{response.text}")
            else:
                self.create_log_entry_async(LogSeverity.Info,
                                            f"Success while sending prices records after {elapsed_time:.2f} ms.")
        except Exception as e:
            self.create_log_entry_async(LogSeverity.Error, str(e), e)

    def send_stock_locations(self, payload):
        try:
            self.create_log_entry_async(LogSeverity.Info, f"About to send {len(payload)} stock locations records.")
            start_time = time.time()
            response = requests.request(
                "POST",
                f'{self.amper_url}/api/stock-locations-import',
                headers=self.get_authorization_header(),
                data=json.dumps(payload, cls=AmperJsonEncoder)
            )
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            if response.status_code not in [200, 201]:
                self.create_log_entry_async(LogSeverity.Error,
                                            f"FAILURE while sending stock locations after {elapsed_time:.2f} ms; "
                                            f"{response.text}")
            else:
                self.create_log_entry_async(LogSeverity.Info,
                                            f"Success while sending stock locations records after {elapsed_time:.2f} ms.")
        except Exception as e:
            self.create_log_entry_async(LogSeverity.Error, str(e), e)

    def send_stocks(self, payload):
        try:
            self.create_log_entry_async(LogSeverity.Info, f"About to send {len(payload)} stocks records.")
            start_time = time.time()
            response = requests.request(
                "POST",
                f'{self.amper_url}/api/stocks-import',
                headers=self.get_authorization_header(),
                data=json.dumps(payload, cls=AmperJsonEncoder)
            )
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            if response.status_code not in [200, 201]:
                self.create_log_entry_async(LogSeverity.Error,
                                            f"FAILURE while sending stocks after {elapsed_time:.2f} ms; "
                                            f"{response.text}")
            else:
                self.create_log_entry_async(LogSeverity.Info,
                                            f"Success while sending stocks records after {elapsed_time:.2f} ms.")
        except Exception as e:
            self.create_log_entry_async(LogSeverity.Error, str(e), e)

    def send_customer_products_relations(self, payload):
        try:
            self.create_log_entry_async(LogSeverity.Info, f"About to send {len(payload)} customer products relations records.")
            start_time = time.time()
            response = requests.request(
                "POST",
                f'{self.amper_url}/api/customer-products-import',
                headers=self.get_authorization_header(),
                data=json.dumps(payload, cls=AmperJsonEncoder)
            )
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            if response.status_code not in [200, 201]:
                self.create_log_entry_async(LogSeverity.Error,
                                            f"FAILURE while sending customer products relations after {elapsed_time:.2f} ms; "
                                            f"{response.text}")
            else:
                self.create_log_entry_async(LogSeverity.Info,
                                            f"Success while sending customer products relations records after {elapsed_time:.2f} ms.")
        except Exception as e:
            self.create_log_entry_async(LogSeverity.Error, str(e), e)

    def send_customer_product_logistic_minimums(self, payload):
        try:
            self.create_log_entry_async(LogSeverity.Info,
                                        f"About to send {len(payload)} customer product logistic minimum records.")
            start_time = time.time()
            response = requests.request(
                "POST",
                f'{self.amper_url}/api/customer-logistic-minimum-import',
                headers=self.get_authorization_header(),
                data=json.dumps(payload, cls=AmperJsonEncoder)
            )
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            if response.status_code not in [200, 201]:
                self.create_log_entry_async(LogSeverity.Error,
                                            f"FAILURE while sending customer product logistic minimum after {elapsed_time:.2f} ms; "
                                            f"{response.text}")
            else:
                self.create_log_entry_async(LogSeverity.Info,
                                            f"Success while sending customer product logistic minimum records after {elapsed_time:.2f} ms.")
        except Exception as e:
            self.create_log_entry_async(LogSeverity.Error, str(e), e)

    def send_related_products(self, payload):
        try:
            self.create_log_entry_async(LogSeverity.Info, f"About to send {len(payload)} related product records.")
            start_time = time.time()
            response = requests.request(
                "POST",
                f'{self.amper_url}/api/product-related-products-import',
                headers=self.get_authorization_header(),
                data=json.dumps(payload, cls=AmperJsonEncoder)
            )
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            if response.status_code not in [200, 201]:
                self.create_log_entry_async(LogSeverity.Error,
                                            f"FAILURE while sending related products after {elapsed_time:.2f} ms; "
                                            f"{response.text}")
            else:
                self.create_log_entry_async(LogSeverity.Info,
                                            f"Success while sending related product records after {elapsed_time:.2f} ms.")
        except Exception as e:
            self.create_log_entry_async(LogSeverity.Error, str(e), e)

    def send_product_sets(self, payload):
        try:
            self.create_log_entry_async(LogSeverity.Info, f"About to send {len(payload)} product sets records.")
            start_time = time.time()
            response = requests.request(
                "POST",
                f'{self.amper_url}/api/product-sets-import',
                headers=self.get_authorization_header(),
                data=json.dumps(payload, cls=AmperJsonEncoder)
            )
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            if response.status_code not in [200, 201]:
                self.create_log_entry_async(LogSeverity.Error,
                                            f"FAILURE while sending product sets after {elapsed_time:.2f} ms; "
                                            f"{response.text}")
            else:
                self.create_log_entry_async(LogSeverity.Info,
                                            f"Success while sending product sets records after {elapsed_time:.2f} ms.")
        except Exception as e:
            self.create_log_entry_async(LogSeverity.Error, str(e), e)

    def send_documents(self, payload):
        try:
            self.create_log_entry_async(LogSeverity.Info, f"About to send {len(payload)} document records.")
            documents: List[Document] = payload
            parts = [documents[i:i + 1000] for i in range(0, len(documents), 1000)]
            start_time = time.time()
            for p in parts:
                response = requests.request(
                    "POST",
                    f'{self.amper_url}/api/document-import',
                    headers=self.get_authorization_header(),
                    data=json.dumps(p, cls=AmperJsonEncoder)
                )
                elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds

                if response.status_code not in [200, 201]:
                    self.create_log_entry_async(LogSeverity.Error,
                                                f"FAILURE while sending a batch of {len(p)} document records after {elapsed_time:.2f} ms; "
                                                f"{response.text}")

            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            self.create_log_entry_async(LogSeverity.Info, f"Success while sending document records after {elapsed_time:.2f} ms.")

        except Exception as e:
            self.create_log_entry_async(LogSeverity.Error, str(e), e)

    def send_align_documents(self, payload):
        try:
            self.create_log_entry_async(LogSeverity.Info, f"About to send {len(payload)} align document records.")
            start_time = time.time()
            response = requests.request(
                "POST",
                f'{self.amper_url}/api/document-align',
                headers=self.get_authorization_header(),
                data=json.dumps(payload, cls=AmperJsonEncoder)
            )
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            if response.status_code not in [200, 201]:
                self.create_log_entry_async(LogSeverity.Error,
                                            f"FAILURE while sending align documents after {elapsed_time:.2f} ms; "
                                            f"{response.text}")
            else:
                self.create_log_entry_async(LogSeverity.Info,
                                            f"Success while sending align document records after {elapsed_time:.2f} ms.")
        except Exception as e:
            self.create_log_entry_async(LogSeverity.Error, str(e), e)

    def send_settlements(self, payload):
        try:
            self.create_log_entry_async(LogSeverity.Info, f"About to send {len(payload)} settlement records.")
            start_time = time.time()
            response = requests.request(
                "POST",
                f'{self.amper_url}/api/settlement-import',
                headers=self.get_authorization_header(),
                data=json.dumps(payload, cls=AmperJsonEncoder)
            )
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            if response.status_code not in [200, 201]:
                self.create_log_entry_async(LogSeverity.Error,
                                            f"FAILURE while sending settlements after {elapsed_time:.2f} ms; "
                                            f"{response.text}")
            else:
                self.create_log_entry_async(LogSeverity.Info,
                                            f"Success while sending settlement records after {elapsed_time:.2f} ms.")
        except Exception as e:
            self.create_log_entry_async(LogSeverity.Error, str(e), e)

    def send_category_discount(self, payload):
        try:
            self.create_log_entry_async(LogSeverity.Info, f"About to send {len(payload)} category discount records.")
            category_discounts: List[CategoryDiscount] = payload
            parts = [category_discounts[i:i + 50000] for i in range(0, len(category_discounts), 50000)]
            start_time = time.time()

            for p in parts:
                first_package = "1"
                last_package = "0"
                single_thread = "1"

                if len(p) < 50000:
                    last_package = "1"
                    single_thread = "0"


                response = requests.request(
                    "POST",
                    f'{self.amper_url}/api/category-discount-import?single_thread=1' +
                    f'&first_package={first_package}&last_package={last_package}&single_thread={single_thread}',
                    headers=self.get_authorization_header(),
                    data=json.dumps(p, cls=AmperJsonEncoder)
                )
                elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds

                if response.status_code not in [200, 201]:
                    self.create_log_entry_async(LogSeverity.Error,
                                                f"FAILURE while sending a batch of {len(p)} category discounts after {elapsed_time:.2f} ms; "
                                                f"{response.text}")

            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            self.create_log_entry_async(LogSeverity.Info, f"Success while sending {len(payload)} category discount records after {elapsed_time:.2f} ms.")

        except Exception as e:
            self.create_log_entry_async(LogSeverity.Error, str(e), e)

    def send_file(self, payload):
        try:
            self.create_log_entry_async(LogSeverity.Info, f"About to send file {payload['fileName']}")
            start_time = time.time()
            multipart_form_data = {
                'image': (payload['fileName'], open(payload['path'], 'rb')),
                'order': (None, payload['order']),
                'product_id': (None, '0'),
                'alt': (None, payload['fileName']),
                'product_external_id': (None, payload['product_external_id'])
            }
            response = requests.request(
                "POST",
                f'{self.amper_url}/product-images/',
                files=multipart_form_data,
                headers=self.get_authorization_header()
            )
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            if response.status_code not in [200, 201]:
                self.create_log_entry_async(LogSeverity.Error,
                                            f"FAILURE while getting order after {elapsed_time:.2f} ms; "
                                            f"{response.text}")
            else:
                self.create_log_entry_async(LogSeverity.Info,
                                            f"Success while getting order after {elapsed_time:.2f} ms.")

        except Exception as e:
            self.create_log_entry_async(LogSeverity.Error, str(e), e)

    def get_order(self, payload):
        try:
            self.create_log_entry_async(LogSeverity.Info, f"About to get order for token {payload}")
            start_time = time.time()
            response = requests.request(
                "GET",
                f'{self.amper_url}/orders-translator/{payload}/',
                headers=self.get_authorization_header()
            )
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            if response.status_code not in [200, 201]:
                self.create_log_entry_async(LogSeverity.Error,
                                            f"FAILURE while getting order after {elapsed_time:.2f} ms; "
                                            f"{response.text}")
            else:
                self.create_log_entry_async(LogSeverity.Info,
                                            f"Success while getting order after {elapsed_time:.2f} ms.")

        except Exception as e:
            self.create_log_entry_async(LogSeverity.Error, str(e), e)

    def change_order_status(self, payload):
        try:
            self.create_log_entry_async(LogSeverity.Info, f"About to change order status for token {payload['token']}")
            start_time = time.time()
            content = {"status": payload["status"]}
            response = requests.request(
                "PATCH",
                f'{self.amper_url}/orders-translator/{payload["token"]}/',
                headers=self.get_authorization_header(),
                data=json.dumps(content, cls=AmperJsonEncoder)
            )
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            if response.status_code not in [200, 201]:
                self.create_log_entry_async(LogSeverity.Error,
                                            f"FAILURE while changing order status after {elapsed_time:.2f} ms; "
                                            f"{response.text}")
            else:
                self.create_log_entry_async(LogSeverity.Info,
                                            f"Success while changing order status after {elapsed_time:.2f} ms.")

        except Exception as e:
            self.create_log_entry_async(LogSeverity.Error, str(e), e)

    def send_addresses(self, payload):
        try:
            self.create_log_entry_async(LogSeverity.Info, f"About to send {len(payload)} addresses.")
            start_time = time.time()
            response = requests.request(
                "POST",
                f'{self.amper_url}/api/addresses-import',
                headers=self.get_authorization_header(),
                data=json.dumps(payload, cls=AmperJsonEncoder)
            )
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            if response.status_code not in [200, 201]:
                self.create_log_entry_async(LogSeverity.Error,
                                            f"FAILURE while sending addresses after {elapsed_time:.2f} ms; "
                                            f"{response.text}")
            else:
                self.create_log_entry_async(LogSeverity.Info,
                                            f"Success while sending addresses after {elapsed_time:.2f} ms.")

        except Exception as e:
            self.create_log_entry_async(LogSeverity.Error, str(e), e)

    def change_complaint_status(self, payload):
        try:
            self.create_log_entry_async(LogSeverity.Info, f"About to change complaint status for token {payload['token']}.")
            start_time = time.time()
            content = {"status": payload["status"]}
            response = requests.request(
                "PATCH",
                f'{self.amper_url}/complaints-translator/{payload}/',
                headers=self.get_authorization_header(),
                data=json.dumps(content, cls=AmperJsonEncoder)
            )
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            if response.status_code not in [200, 201]:
                self.create_log_entry_async(LogSeverity.Error,
                                            f"FAILURE while changing complaint status after {elapsed_time:.2f} ms; "
                                            f"{response.text}")
            else:
                self.create_log_entry_async(LogSeverity.Info,
                                            f"Success while changing complaint status after {elapsed_time:.2f} ms.")

        except Exception as e:
            self.create_log_entry_async(LogSeverity.Error, str(e), e)

    def send_customer_categories(self, payload):
        try:
            self.create_log_entry_async(LogSeverity.Info, f"About to send {len(payload)} categories.")
            start_time = time.time()
            response = requests.request(
                "POST",
                f'{self.amper_url}/api/customer-categories-import',
                headers=self.get_authorization_header(),
                data=json.dumps(payload, cls=AmperJsonEncoder)
            )
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            if response.status_code not in [200, 201]:
                self.create_log_entry_async(LogSeverity.Error,
                                            f"FAILURE while sending categories after {elapsed_time:.2f} ms; "
                                            f"{response.text}")
            else:
                self.create_log_entry_async(LogSeverity.Info,
                                            f"Success while sending categories after {elapsed_time:.2f} ms.")

        except Exception as e:
            self.create_log_entry_async(LogSeverity.Error, str(e), e)

    def send_customer_categories_relation(self, payload):
        try:
            self.create_log_entry_async(LogSeverity.Info, f"About to send {len(payload)} customer categories relations.")
            start_time = time.time()
            response = requests.request(
                "POST",
                f'{self.amper_url}/api/customer-categories-relation-import',
                headers=self.get_authorization_header(),
                data=json.dumps(payload, cls=AmperJsonEncoder)
            )
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            if response.status_code not in [200, 201]:
                self.create_log_entry_async(LogSeverity.Error,
                                            f"FAILURE while sending customer categories relations after {elapsed_time:.2f} ms; "
                                            f"{response.text}")
            else:
                self.create_log_entry_async(LogSeverity.Info,
                                            f"Success while sending customer categories relations after {elapsed_time:.2f} ms.")

        except Exception as e:
            self.create_log_entry_async(LogSeverity.Error, str(e), e)

    def send_price_level_assignment(self, payload):
        try:
            self.create_log_entry_async(LogSeverity.Info, f"About to send {len(payload)} price level assignments.")
            start_time = time.time()
            response = requests.request(
                "POST",
                f'{self.amper_url}/api/price-level-assigment-import',
                headers=self.get_authorization_header(),
                data=json.dumps(payload, cls=AmperJsonEncoder)
            )
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            if response.status_code not in [200, 201]:
                self.create_log_entry_async(LogSeverity.Error,
                                            f"FAILURE while sending price level assignments after {elapsed_time:.2f} ms; "
                                            f"{response.text}")
            else:
                self.create_log_entry_async(LogSeverity.Info,
                                            f"Success while sending price level assignments after {elapsed_time:.2f} ms.")

        except Exception as e:
            self.create_log_entry_async(LogSeverity.Error, str(e), e)

    def send_promotions(self, payload):
        try:
            self.create_log_entry_async(LogSeverity.Info, f"About to send {len(payload)} promotions.")
            start_time = time.time()
            response = requests.request(
                "POST",
                f'{self.amper_url}/api/promotions-import',
                headers=self.get_authorization_header(),
                data=json.dumps(payload, cls=AmperJsonEncoder)
            )
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            if response.status_code not in [200, 201]:
                self.create_log_entry_async(LogSeverity.Error,
                                            f"FAILURE while sending promotions after {elapsed_time:.2f} ms; "
                                            f"{response.text}")
            else:
                self.create_log_entry_async(LogSeverity.Info,
                                            f"Success while sending promotions after {elapsed_time:.2f} ms.")

        except Exception as e:
            self.create_log_entry_async(LogSeverity.Error, str(e), e)

    def send_promotion_customers(self, payload):
        try:
            self.create_log_entry_async(LogSeverity.Info, f"About to send {len(payload)} promotion customers.")
            start_time = time.time()
            response = requests.request(
                "POST",
                f'{self.amper_url}/api/promotions-customers-import',
                headers=self.get_authorization_header(),
                data=json.dumps(payload, cls=AmperJsonEncoder)
            )
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            if response.status_code not in [200, 201]:
                self.create_log_entry_async(LogSeverity.Error,
                                            f"FAILURE while sending promotion customers after {elapsed_time:.2f} ms; "
                                            f"{response.text}")
            else:
                self.create_log_entry_async(LogSeverity.Info,
                                            f"Success while sending promotion customers after {elapsed_time:.2f} ms.")

        except Exception as e:
            self.create_log_entry_async(LogSeverity.Error, str(e), e)

    def send_promotion_customer_categories(self, payload):
        try:
            self.create_log_entry_async(LogSeverity.Info, f"About to send {len(payload)} promotion customer categories.")
            start_time = time.time()
            response = requests.request(
                "POST",
                f'{self.amper_url}/api/promotions-customer-categories-import',
                headers=self.get_authorization_header(),
                data=json.dumps(payload, cls=AmperJsonEncoder)
            )
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            if response.status_code not in [200, 201]:
                self.create_log_entry_async(LogSeverity.Error,
                                            f"FAILURE while sending promotion customer categories after {elapsed_time:.2f} ms; "
                                            f"{response.text}")
            else:
                self.create_log_entry_async(LogSeverity.Info,
                                            f"Success while sending promotion customer categories after {elapsed_time:.2f} ms.")

        except Exception as e:
            self.create_log_entry_async(LogSeverity.Error, str(e), e)

    def get_document(self, payload):
        try:
            self.create_log_entry_async(LogSeverity.Info, f"About to get a document.")
            start_time = time.time()
            response = requests.request(
                "GET",
                f'{self.amper_url}/documents-translator/{payload}/',
                headers=self.get_authorization_header()
            )
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            if response.status_code not in [200, 201]:
                self.create_log_entry_async(LogSeverity.Error,
                                            f"FAILURE while getting a document after {elapsed_time:.2f} ms; "
                                            f"{response.text}")
            else:
                self.create_log_entry_async(LogSeverity.Info,
                                            f"Success while getting a document after {elapsed_time:.2f} ms.")
                document = self.create_amper_object(Document, json.loads(response.text))
                return document

        except Exception as e:
            self.create_log_entry_async(LogSeverity.Error, str(e), e)

    def change_document_status(self, payload):
        try:
            self.create_log_entry_async(LogSeverity.Info, f"About to change document status for id {payload['id']}")
            content = {"status": payload["status"]}
            start_time = time.time()
            response = requests.request(
                "PATCH",
                f'{self.amper_url}/documents-translator/{payload["id"]}/',
                headers=self.get_authorization_header(),
                data=json.dumps(content, cls=AmperJsonEncoder)
            )
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            if response.status_code not in [200, 201]:
                self.create_log_entry_async(LogSeverity.Error,
                                            f"FAILURE while changing order status after {elapsed_time:.2f} ms; "
                                            f"{response.text}")
            else:
                self.create_log_entry_async(LogSeverity.Info,
                                            f"Success while changing order status after {elapsed_time:.2f} ms.")

        except Exception as e:
            self.create_log_entry_async(LogSeverity.Error, str(e), e)

    def send_unit_of_measures(self, payload):
        try:
            self.create_log_entry_async(LogSeverity.Info, f"About to send {len(payload)} units of measure")
            start_time = time.time()
            response = requests.request(
                "POST",
                f'{self.amper_url}/api/unitofmeasure-import',
                headers=self.get_authorization_header(),
                data=json.dumps(payload, cls=AmperJsonEncoder)
            )
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            if response.status_code not in [200, 201]:
                self.create_log_entry_async(LogSeverity.Error,
                                            f"FAILURE while sending units of measure after {elapsed_time:.2f} ms; "
                                            f"{response.text}")
            else:
                self.create_log_entry_async(LogSeverity.Info,
                                            f"Success while sending units of measure after {elapsed_time:.2f} ms.")

        except Exception as e:
            self.create_log_entry_async(LogSeverity.Error, str(e), e)

    def send_default_price_overwrite_for_category_discount(self, payload):
        try:
            self.create_log_entry_async(LogSeverity.Info, f"About to send {len(payload)} default price overwrites for category discounts.")
            start_time = time.time()
            response = requests.request(
                "POST",
                f'{self.amper_url}/api/default-price-overwrite-import',
                headers=self.get_authorization_header(),
                data=json.dumps(payload, cls=AmperJsonEncoder)
            )
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            if response.status_code not in [200, 201]:
                self.create_log_entry_async(LogSeverity.Error,
                                            f"FAILURE while sending default price overwrites for category discounts after {elapsed_time:.2f} ms; "
                                            f"{response.text}")
            else:
                self.create_log_entry_async(LogSeverity.Info,
                                            f"Success while sending default price overwrites for category discounts after {elapsed_time:.2f} ms.")

        except Exception as e:
            self.create_log_entry_async(LogSeverity.Error, str(e), e)

    def send_payment_forms(self, payload):
        try:
            self.create_log_entry_async(LogSeverity.Info, f"About to send {len(payload)} payment forms.")
            start_time = time.time()
            response = requests.request(
                "POST",
                f'{self.amper_url}/api/payment-forms-import',
                headers=self.get_authorization_header(),
                data=json.dumps(payload, cls=AmperJsonEncoder)
            )
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            if response.status_code not in [200, 201]:
                self.create_log_entry_async(LogSeverity.Error,
                                            f"FAILURE while sending payment forms after {elapsed_time:.2f} ms; "
                                            f"{response.text}")
            else:
                self.create_log_entry_async(LogSeverity.Info,
                                            f"Success while sending payment forms after {elapsed_time:.2f} ms.")

        except Exception as e:
            self.create_log_entry_async(LogSeverity.Error, str(e), e)

    def send_customer_sales_representative_relation(self, payload):
        try:
            self.create_log_entry_async(LogSeverity.Info, f"About to send {len(payload)} customer sales rep relations.")
            start_time = time.time()
            response = requests.request(
                "POST",
                f'{self.amper_url}/api/customer-sales-representative-import',
                headers=self.get_authorization_header(),
                data=json.dumps(payload, cls=AmperJsonEncoder)
            )
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            if response.status_code not in [200, 201]:
                self.create_log_entry_async(LogSeverity.Error,
                                            f"FAILURE while sending customer sales rep relations after {elapsed_time:.2f} ms; "
                                            f"{response.text}")
            else:
                self.create_log_entry_async(LogSeverity.Info,
                                            f"Success while sending customer sales rep relations after {elapsed_time:.2f} ms.")

        except Exception as e:
            self.create_log_entry_async(LogSeverity.Error, str(e), e)

    def send_schedules(self, payload):
        try:
            self.create_log_entry_async(LogSeverity.Info, f"About to send {len(payload)} schedules.")
            start_time = time.time()
            response = requests.request(
                "POST",
                f'{self.amper_url}/api/schedules-import',
                headers=self.get_authorization_header(),
                data=json.dumps(payload, cls=AmperJsonEncoder)
            )
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            if response.status_code not in [200, 201]:
                self.create_log_entry_async(LogSeverity.Error,
                                            f"FAILURE while sending schedules after {elapsed_time:.2f} ms; "
                                            f"{response.text}")
            else:
                self.create_log_entry_async(LogSeverity.Info,
                                            f"Success while sending schedules after {elapsed_time:.2f} ms.")

        except Exception as e:
            self.create_log_entry_async(LogSeverity.Error, str(e), e)

    def send_customer_tasks(self, payload):
        try:
            self.create_log_entry_async(LogSeverity.Info, f"About to send {len(payload)} customer tasks.")
            start_time = time.time()
            response = requests.request(
                "POST",
                f'{self.amper_url}/api/customer-tasks-import',
                headers=self.get_authorization_header(),
                data=json.dumps(payload, cls=AmperJsonEncoder)
            )
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            if response.status_code not in [200, 201]:
                self.create_log_entry_async(LogSeverity.Error,
                                            f"FAILURE while sending customer tasks after {elapsed_time:.2f} ms; "
                                            f"{response.text}")
            else:
                self.create_log_entry_async(LogSeverity.Info,
                                            f"Success while sending customer tasks after {elapsed_time:.2f} ms.")

        except Exception as e:
            self.create_log_entry_async(LogSeverity.Error, str(e), e)

    def send_manufacturers(self, payload):
        try:
            self.create_log_entry_async(LogSeverity.Info, f"About to send {len(payload)} manufacturers.")
            start_time = time.time()
            response = requests.request(
                "POST",
                f'{self.amper_url}/api/manufacturers-import',
                headers=self.get_authorization_header(),
                data=json.dumps(payload, cls=AmperJsonEncoder)
            )
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            if response.status_code not in [200, 201]:
                self.create_log_entry_async(LogSeverity.Error,
                                            f"FAILURE while sending manufacturers after {elapsed_time:.2f} ms; "
                                            f"{response.text}")
            else:
                self.create_log_entry_async(LogSeverity.Info,
                                            f"Success while sending manufacturers after {elapsed_time:.2f} ms.")

        except Exception as e:
            self.create_log_entry_async(LogSeverity.Error, str(e), e)

    def send_manufacturer_brands(self, payload):
        try:
            self.create_log_entry_async(LogSeverity.Info, f"About to send {len(payload)} brands.")
            start_time = time.time()
            response = requests.request(
                "POST",
                f'{self.amper_url}/api/manufacturer-brand-import',
                headers=self.get_authorization_header(),
                data=json.dumps(payload, cls=AmperJsonEncoder)
            )
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            if response.status_code not in [200, 201]:
                self.create_log_entry_async(LogSeverity.Error,
                                            f"FAILURE while sending brands after {elapsed_time:.2f} ms; "
                                            f"{response.text}")
            else:
                self.create_log_entry_async(LogSeverity.Info,
                                            f"Success while sending brands after {elapsed_time:.2f} ms.")

        except Exception as e:
            self.create_log_entry_async(LogSeverity.Error, str(e), e)

    def add_customer_to_category(self, payload):
        try:
            self.create_log_entry_async(LogSeverity.Info, f"About to add customer to category")
            content = {"customer": payload['customer_id'], "category": payload['category_id']}
            start_time = time.time()
            response = requests.request(
                "POST",
                f'{self.amper_url}/customer-categories-relation/',
                headers=self.get_authorization_header(),
                data=json.dumps(content, cls=AmperJsonEncoder)
            )
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            if response.status_code not in [200, 201]:
                self.create_log_entry_async(LogSeverity.Error,
                                            f"FAILURE while adding customer to category after {elapsed_time:.2f} ms; "
                                            f"{response.text}")
            else:
                self.create_log_entry_async(LogSeverity.Info,
                                            f"Success while adding customer to category after {elapsed_time:.2f} ms.")

        except Exception as e:
            self.create_log_entry_async(LogSeverity.Error, str(e), e)

    def add_translator_relation(self, payload):
        try:
            self.create_log_entry_async(LogSeverity.Info, f"About to add customer to category")
            content = {"object_type": payload['objectType'], "external_id": payload['externalId'], "internal_id": payload['internalId']}
            start_time = time.time()
            response = requests.request(
                "POST",
                f'{self.amper_url}/translator/add-relation',
                headers=self.get_authorization_header(),
                data=json.dumps(content, cls=AmperJsonEncoder)
            )
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            if response.status_code not in [200, 201]:
                self.create_log_entry_async(LogSeverity.Error,
                                            f"FAILURE while adding translator relation after {elapsed_time:.2f} ms; "
                                            f"{response.text}")
            else:
                self.create_log_entry_async(LogSeverity.Info,
                                            f"Success while adding translator relation after {elapsed_time:.2f} ms.")

        except Exception as e:
            self.create_log_entry_async(LogSeverity.Error, str(e), e)

    def change_cash_document_status(self, payload):
        try:
            self.create_log_entry_async(LogSeverity.Info, f"About to change cash document status for id {payload['id']}")
            content = {"status": payload['status']}
            start_time = time.time()
            response = requests.request(
                "PATCH",
                f'{self.amper_url}/cash-documents-translator/{payload["id"]}/',
                headers=self.get_authorization_header(),
                data=json.dumps(content, cls=AmperJsonEncoder)
            )
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            if response.status_code not in [200, 201]:
                self.create_log_entry_async(LogSeverity.Error,
                                            f"FAILURE while changing cash document status after {elapsed_time:.2f} ms; "
                                            f"{response.text}")
            else:
                self.create_log_entry_async(LogSeverity.Info,
                                            f"Success while changing cash document status after {elapsed_time:.2f} ms.")

        except Exception as e:
            self.create_log_entry_async(LogSeverity.Error, str(e), e)

    def send_users(self, payload):
        try:
            self.create_log_entry_async(LogSeverity.Info, f"About to send {len(payload)} users.")
            start_time = time.time()
            response = requests.request(
                "POST",
                f'{self.amper_url}/api/users-import',
                headers=self.get_authorization_header(),
                data=json.dumps(payload, cls=AmperJsonEncoder)
            )
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            if response.status_code not in [200, 201]:
                self.create_log_entry_async(LogSeverity.Error,
                                            f"FAILURE while sending users after {elapsed_time:.2f} ms; "
                                            f"{response.text}")
            else:
                self.create_log_entry_async(LogSeverity.Info,
                                            f"Success while sending users after {elapsed_time:.2f} ms.")

        except Exception as e:
            self.create_log_entry_async(LogSeverity.Error, str(e), e)

    def send_orders(self, payload):
        try:
            self.create_log_entry_async(LogSeverity.Info, f"About to send {len(payload)} orders.")
            orders: List[Order] = payload
            parts = [orders[i:i + 1000] for i in range(0, len(orders), 1000)]
            start_time = time.time()
            for p in parts:
                response = requests.request(
                    "POST",
                    f'{self.amper_url}/api/orders-import',
                    headers=self.get_authorization_header(),
                    data=json.dumps(p, cls=AmperJsonEncoder)
                )
                elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds

                if response.status_code not in [200, 201]:
                    self.create_log_entry_async(LogSeverity.Error,
                                                f"FAILURE while sending a batch of {len(p)} orders after {elapsed_time:.2f} ms; "
                                                f"{response.text}")

            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            self.create_log_entry_async(LogSeverity.Info, f"Success while sending orders after {elapsed_time:.2f} ms.")

        except Exception as e:
            self.create_log_entry_async(LogSeverity.Error, str(e), e)

    def align_images(self, payload):
        try:
            self.create_log_entry_async(LogSeverity.Info, f"About to send {len(payload)} images.")
            start_time = time.time()
            response = requests.request(
                "POST",
                f'{self.amper_url}/api/product-images-align',
                headers=self.get_authorization_header(),
                data=json.dumps(payload, cls=AmperJsonEncoder)
            )
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            if response.status_code not in [200, 201]:
                self.create_log_entry_async(LogSeverity.Error,
                                            f"FAILURE while sending images after {elapsed_time:.2f} ms; "
                                            f"{response.text}")
            else:
                self.create_log_entry_async(LogSeverity.Info,
                                            f"Success while sending images after {elapsed_time:.2f} ms.")

        except Exception as e:
            self.create_log_entry_async(LogSeverity.Error, str(e), e)

    def transfer_document(self, payload):
        try:
            self.create_log_entry_async(LogSeverity.Info, f"About to transfer document")
            content = {"document_id": payload['document_id'], "sales_rep_identifier": payload['sales_rep_identifier']}
            start_time = time.time()
            response = requests.request(
                "POST",
                f'{self.amper_url}/translator/transfer-document',
                headers=self.get_authorization_header(),
                data=json.dumps(content, cls=AmperJsonEncoder)
            )
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            if response.status_code not in [200, 201]:
                self.create_log_entry_async(LogSeverity.Error,
                                            f"FAILURE while adding transferring document after {elapsed_time:.2f} ms; "
                                            f"{response.text}")
            else:
                self.create_log_entry_async(LogSeverity.Info,
                                            f"Success while adding transferring document after {elapsed_time:.2f} ms.")

        except Exception as e:
            self.create_log_entry_async(LogSeverity.Error, str(e), e)

    def send_condition_relation(self, payload):
        try:
            self.create_log_entry_async(LogSeverity.Info, f"About to send {len(payload)} conditions.")
            start_time = time.time()
            response = requests.request(
                "POST",
                f'{self.amper_url}/api/promotions-conndition-relation-import',
                headers=self.get_authorization_header(),
                data=json.dumps(payload, cls=AmperJsonEncoder)
            )
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            if response.status_code not in [200, 201]:
                self.create_log_entry_async(LogSeverity.Error,
                                            f"FAILURE while sending conditions after {elapsed_time:.2f} ms; "
                                            f"{response.text}")
            else:
                self.create_log_entry_async(LogSeverity.Info,
                                            f"Success while sending conditions after {elapsed_time:.2f} ms.")

        except Exception as e:
            self.create_log_entry_async(LogSeverity.Error, str(e), e)

    def send_condition_relation_promotion_condition(self, payload):
        try:
            self.create_log_entry_async(LogSeverity.Info, f"About to send {len(payload)} ConditionRelationPromotionCondition.")
            start_time = time.time()
            response = requests.request(
                "POST",
                f'{self.amper_url}/api/promotions-conndition-relation-import',
                headers=self.get_authorization_header(),
                data=json.dumps(payload, cls=AmperJsonEncoder)
            )
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            if response.status_code not in [200, 201]:
                self.create_log_entry_async(LogSeverity.Error,
                                            f"FAILURE while sending conndition-relation-promotion-condition after {elapsed_time:.2f} ms; "
                                            f"{response.text}")
            else:
                self.create_log_entry_async(LogSeverity.Info,
                                            f"Success while sending conndition-relation-promotion-condition after {elapsed_time:.2f} ms.")

        except Exception as e:
            self.create_log_entry_async(LogSeverity.Error, str(e), e)

    def send_promotion_condition(self, payload):
        try:
            self.create_log_entry_async(LogSeverity.Info, f"About to send {len(payload)} PromotionCondition.")
            start_time = time.time()
            response = requests.request(
                "POST",
                f'{self.amper_url}/api/promotions-promotion-condition-import',
                headers=self.get_authorization_header(),
                data=json.dumps(payload, cls=AmperJsonEncoder)
            )
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            if response.status_code not in [200, 201]:
                self.create_log_entry_async(LogSeverity.Error,
                                            f"FAILURE while sending PromotionCondition after {elapsed_time:.2f} ms; "
                                            f"{response.text}")
            else:
                self.create_log_entry_async(LogSeverity.Info,
                                            f"Success while sending PromotionCondition after {elapsed_time:.2f} ms.")

        except Exception as e:
            self.create_log_entry_async(LogSeverity.Error, str(e), e)

    def send_promotion_condition_item(self, payload):
        try:
            self.create_log_entry_async(LogSeverity.Info, f"About to send {len(payload)} PromotionConditionItem.")
            start_time = time.time()
            response = requests.request(
                "POST",
                f'{self.amper_url}/api/promotions-promotion-condition-item-import',
                headers=self.get_authorization_header(),
                data=json.dumps(payload, cls=AmperJsonEncoder)
            )
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            if response.status_code not in [200, 201]:
                self.create_log_entry_async(LogSeverity.Error,
                                            f"FAILURE while sending PromotionConditionItem after {elapsed_time:.2f} ms; "
                                            f"{response.text}")
            else:
                self.create_log_entry_async(LogSeverity.Info,
                                            f"Success while sending PromotionConditionItem after {elapsed_time:.2f} ms.")

        except Exception as e:
            self.create_log_entry_async(LogSeverity.Error, str(e), e)

    def send_promotion_rewards(self, payload):
        try:
            self.create_log_entry_async(LogSeverity.Info, f"About to send {len(payload)} PromotionRewards.")
            start_time = time.time()
            response = requests.request(
                "POST",
                f'{self.amper_url}/api/promotions-rewards-import',
                headers=self.get_authorization_header(),
                data=json.dumps(payload, cls=AmperJsonEncoder)
            )
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            if response.status_code not in [200, 201]:
                self.create_log_entry_async(LogSeverity.Error,
                                            f"FAILURE while sending PromotionRewards after {elapsed_time:.2f} ms; "
                                            f"{response.text}")
            else:
                self.create_log_entry_async(LogSeverity.Info,
                                            f"Success while sending PromotionRewards after {elapsed_time:.2f} ms.")

        except Exception as e:
            self.create_log_entry_async(LogSeverity.Error, str(e), e)

    def send_sales_representatives(self, payload):
        try:
            self.create_log_entry_async(LogSeverity.Info, f"About to send {len(payload)} SalesRepresentatives.")
            start_time = time.time()
            response = requests.request(
                "POST",
                f'{self.amper_url}/api/sales-representatives-import',
                headers=self.get_authorization_header(),
                data=json.dumps(payload, cls=AmperJsonEncoder)
            )
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            if response.status_code not in [200, 201]:
                self.create_log_entry_async(LogSeverity.Error,
                                            f"FAILURE while sending SalesRepresentatives after {elapsed_time:.2f} ms; "
                                            f"{response.text}")
            else:
                self.create_log_entry_async(LogSeverity.Info,
                                            f"Success while sending SalesRepresentatives after {elapsed_time:.2f} ms.")

        except Exception as e:
            self.create_log_entry_async(LogSeverity.Error, str(e), e)

    def get_list_of_orders(self, payload):
        orders: List[Order] = []
        try:
            self.create_log_entry_async(LogSeverity.Info, f"About to get list of orders for status {payload['status']}")
            start_time = time.time()
            response = requests.request(
                "GET",
                f'{self.amper_url}orders-translator/?status={payload["status"]}',
                headers=self.get_authorization_header()
            )
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            if response.status_code not in [200, 201]:
                self.create_log_entry_async(LogSeverity.Error,
                                            f"FAILURE while getting list of orders after {elapsed_time:.2f} ms; "
                                            f"{response.text}")
            else:
                orders_object = json.loads(response.text)
                for order_object in orders_object:
                    order = self.create_amper_object(Order, order_object)
                    orders.append(order)

        except Exception as e:
            self.create_log_entry_async(LogSeverity.Error, str(e), e)
        return orders

    def get_list_of_documents(self, payload):
        documents: List[Document] = []
        try:
            self.create_log_entry_async(LogSeverity.Info, f"About to get list of documents for status {payload['status']}")
            start_time = time.time()
            response = requests.request(
                "GET",
                f'{self.amper_url}documents-translator/?status={payload["status"]}',
                headers=self.get_authorization_header()
            )
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            if response.status_code not in [200, 201]:
                self.create_log_entry_async(LogSeverity.Error,
                                            f"FAILURE while getting list of documents after {elapsed_time:.2f} ms; "
                                            f"{response.text}")
            else:
                documents_object = json.loads(response.text)
                for document_object in documents_object:
                    document = self.create_amper_object(Document, document_object)
                    documents.append(document)

        except Exception as e:
            self.create_log_entry_async(LogSeverity.Error, str(e), e)
        return documents

    def get_list_of_cash_documents(self, payload):
        cash_documents: List[CashDocument] = []
        try:
            self.create_log_entry_async(LogSeverity.Info, f"About to get list of cash documents for status {payload['status']}")
            start_time = time.time()
            response = requests.request(
                "GET",
                f'{self.amper_url}cash-documents-translator/?status={payload["status"]}',
                headers=self.get_authorization_header()
            )
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            if response.status_code not in [200, 201]:
                self.create_log_entry_async(LogSeverity.Error,
                                            f"FAILURE while getting list of cash documents after {elapsed_time:.2f} ms; "
                                            f"{response.text}")
            else:
                cash_documents_object = json.loads(response.text)
                for cash_document_object in cash_documents_object:
                    cash_document = self.create_amper_object(CashDocument, cash_document_object)
                    cash_documents.append(cash_document)

        except Exception as e:
            self.create_log_entry_async(LogSeverity.Error, str(e), e)
        return cash_documents

    def get_list_of_customers(self):
        customers: List[CustomerForExport] = []
        try:
            self.create_log_entry_async(LogSeverity.Info, f"About to get list of customers.")
            start_time = time.time()
            response = requests.request(
                "GET",
                f'{self.amper_url}customers-translator/',
                headers=self.get_authorization_header()
            )
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            if response.status_code not in [200, 201]:
                self.create_log_entry_async(LogSeverity.Error,
                                            f"FAILURE while getting list of customers after {elapsed_time:.2f} ms; "
                                            f"{response.text}")
            else:
                customers_object = json.loads(response.text)
                for customer_object in customers_object:
                    customer = self.create_amper_object(CustomerForExport, customer_object)
                    customers.append(customer)

        except Exception as e:
            self.create_log_entry_async(LogSeverity.Error, str(e), e)
        return customers

    def get_list_of_complaints(self):
        complaints: List[Complaint] = []
        try:
            self.create_log_entry_async(LogSeverity.Info, f"About to get list of complaints.")
            start_time = time.time()
            response = requests.request(
                "GET",
                f'{self.amper_url}complaints-translator/?status=NEW',
                headers=self.get_authorization_header()
            )
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            if response.status_code not in [200, 201]:
                self.create_log_entry_async(LogSeverity.Error,
                                            f"FAILURE while getting list of complaints after {elapsed_time:.2f} ms; "
                                            f"{response.text}")
            else:
                complaints_object = json.loads(response.text)
                for complaint_object in complaints_object:
                    complaint = self.create_amper_object(Complaint, complaint_object)
                    complaints.append(complaint)

        except Exception as e:
            self.create_log_entry_async(LogSeverity.Error, str(e), e)
        return complaints

    def create_amper_object(self, object_type, dictionary):
        amper_object: object_type = object_type()
        for key, val in dictionary.items():
            attr_type = None
            try:
                attr = getattr(amper_object, key)
                attr_type = type(attr)
            except AttributeError:
                continue  # ignore keys not used in API

            if type(val) is list:
                object_child: object_type = amper_object.FieldType(key)
                object_child1 = []
                if object_child is None:
                    setattr(amper_object, key, val)
                    continue
                else:
                    for cObj in val:
                        c = self.create_amper_object(object_child, cObj)
                        object_child1.append(c)
                    setattr(amper_object, key, object_child1)
                    continue
            elif type(val) is dict:
                try:
                    object_child: object_type = amper_object.FieldType(key)
                    c = self.create_amper_object(object_child, val)
                    setattr(amper_object, key, c)
                    continue
                except:
                    pass
            elif attr is None:
                attr_type = amper_object.FieldType(key)
            if attr_type is Decimal:
                if val is not None:
                    setattr(amper_object, key, decimal.Decimal(val))
            elif attr_type is int:
                if val is not None:
                    setattr(amper_object, key, int(val))
            elif attr_type is bool:
                if val is not None:
                    setattr(amper_object, key, bool(val))
            elif attr_type is datetime:
                if val is not None:
                    dt = val
                    if ":" == dt[-3]:
                        dt = dt[:-3] + dt[-2:]
                    setattr(amper_object, key, datetime.strptime(dt, '%Y-%m-%dT%H:%M:%S.%f%z'))
            else:
                setattr(amper_object, key, val)
        return amper_object
