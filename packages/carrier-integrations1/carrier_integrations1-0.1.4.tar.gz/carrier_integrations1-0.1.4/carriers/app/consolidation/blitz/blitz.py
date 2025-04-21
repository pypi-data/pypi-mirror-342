import copy
import json
from collections import defaultdict
import requests
import time
from app.consolidation import CANCELLATION_SUCCESS_DEFAULT, CANCELLATION_FAILURE_DEFAULT
from app.consolidation import trigger_service_failure
from app.consolidation.blitz import CARRIER_SLUG, CARRIER_LOGO, CARRIER_TC
from app.additional_settings import fetch_pincodes
from app.consolidation import cred_check_error_msg, cred_check_success_msg
from app.consolidation import aslist_cronly, render_shipping_label_html, pdf_merge_from_byte, update_label_settings_params
from app.consolidation.utilization.db_operations import ReadWriteOperation
from app.consolidation.utilization.final_order_db_updator import FinalOrderUpdate
from app.consolidation.utilization.generic_order_id_generator import get_order_id
from app.consolidation.utilization.utils import success_resp, curlify_carrier_request
from app.mongo import Conn
from app.utils import asbool, _get_error_resp, geocode_address, _flatten_address
from app.consolidation.carrier_integration_base import CarrierIntegration
from app.consolidation.blitz import ENDPOINTS


def get_ttl_hash(seconds=86400):
    """Return the same value withing `seconds` time period"""
    return round(time.time() / seconds)

def fetch_token_map(username, password, is_test, ttl_hash=None):
    """
        # Usage: token, message = fetch_token_map(self.api_key, self.__env, ttl_hash=get_ttl_hash())
    :param client_uuid:
    :param client_key:
    :param app_id:
    :param device_id:
    :param env:
    :param ttl_hash:
    :return:
    """

    url = ENDPOINTS.get('staging' if is_test else 'live', {}).get('auth')

    payload = json.dumps({
        "request_type": "authenticate",
        "payload": {
            "username": username,
            "password": password
        }
    })

    headers = {
        'Content-Type': 'application/json'
    }
    print(url)
    print(payload)
    print(headers)

    response = requests.request("POST", url, headers=headers, data=payload)

    response_json = response.json()

    if 199 < response.status_code < 300:
        response_json = response.json()
        token = response_json.get("id_token")
        print(token)

        return token, 'success'
    else:
        error_message = response_json.get("message")
        return None, error_message
    
class BlitzIntegration(CarrierIntegration):
    
    CARRIER_LOGO = CARRIER_LOGO
    CARRIER_SLUG = CARRIER_SLUG
    CARRIER_TC = CARRIER_TC

    def __init__(self, **kw):
        self.__request_data = kw.get('input', {})

    @staticmethod
    def cred_check(data):
        """
        :param data:
        :return:
        """
        creds = data.get('cred') or {}
        username = creds.get('username')
        password = creds.get('password')
        is_test = 'test' == creds.get('account_type')
        env = 'staging' if is_test else 'live'
        try:
            token = BlitzIntegration.generate_token(username, password, is_test)
            if token:
                return cred_check_success_msg(CARRIER_SLUG)
            else:
                return cred_check_error_msg(CARRIER_SLUG)
        except Exception as e:
            print("Error")
            print(str(e))

        return cred_check_success_msg(CARRIER_SLUG)

    def generate_token(self, username, password, is_test, regenerate_token=False):
        """

        :param username:
        :param password:
        :param is_test:
        :param regenerate_token:
        :return:
        """
        ttl_hash = get_ttl_hash()
        if regenerate_token:
            ttl_hash = ttl_hash + 1
        token, message = fetch_token_map(username, password, is_test, ttl_hash=ttl_hash)
        return token
    
    def get_box_details(self, parcels):
        return super().get_box_details(parcels)

    def _custom_label(self, input_data):
        return super()._custom_label(input_data)
    
    def fetch_quotes(self, request_data, vendor_id, blitz_vendor_config, retry=0):
        """
        :param request_data:
        :param vendor_id:
        :param blitz_vendor_config:
        :return:
        """
        # TODO hardcoded
        blitz_vendor_config = {
            'account_type': 'live',
            'service_type': 'air,surface',
            'username': 'SPLsv9jJC2Zm',
            'password': 'B,PaFYnE58~Jd',
        }
        if retry > 3:
            return trigger_service_failure(msg='Please recheck credentials configured' or "{slug}".format(slug=CARRIER_SLUG), slug=CARRIER_SLUG, vendor_id=vendor_id, desc=blitz_vendor_config.get("description", "") or CARRIER_SLUG)

        username = blitz_vendor_config.get('username')
        password = blitz_vendor_config.get('password')
        is_test = True if 'test' == blitz_vendor_config.get('account_type') else False

        service_resp = {}
        is_cod = request_data.get("is_cod")
        ship_from_pincode = request_data.get("shipment", {}).get("ship_from", {}).get('postal_code')
        ship_to_pincode = request_data.get("shipment", {}).get("ship_to", {}).get('postal_code')
        env = 'staging' if is_test else 'live'

        service_types = blitz_vendor_config.get('service_type')
        if service_types:
            service_types = [str(service).strip().lower() for service in service_types.split(',')]

        payload = json.dumps({
            "src_pin": ship_from_pincode,
            "channel_id": "",
            "dest_pin": ship_to_pincode,
            "user_warehouse_config": {
                "start": 1,
                "end": 20,
                "picking_hours": 1
            }
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'{self.generate_token(username, password, is_test, regenerate_token=retry > 0)}',
        }
        serviceability_url = ENDPOINTS.get(env, {}).get('serviceability')
        _url = serviceability_url or ''
        service_resp = requests.request("POST", _url, headers=headers, data=payload)

        print(service_resp.text)
        error_msg = ''
        technicality = []
        if service_resp:
            if 199 < service_resp.status_code < 300:
                service_resp_json = service_resp.json()
                serv_resp = service_resp_json.get('response', {})
                is_serviceable = serv_resp.get('serviceable')
                cod_allowed = serv_resp.get('cod_allowed')

                if is_serviceable:
                    for service in service_types:
                        if is_cod and not cod_allowed:
                            continue
                        service_detail = {
                            "error_message": None,
                            "transit_time": None,
                            "detailed_charges": [],
                            "total_charge": {
                                "amount": None,
                                "currency": 'INR'
                            },
                            "service_type": service,
                            "charge_weight": {
                                "value": 0.0,
                                "unit": "KG"
                            },
                            "service_name": service,
                            "info_message": None,
                            "booking_cut_off": None,
                            "delivery_date": None,
                            "pickup_deadline": None
                        }
                        technicality.append(service_detail)
            elif service_resp.status_code in [401, 402]:
                return self.fetch_quotes(request_data, vendor_id, blitz_vendor_config, retry=retry + 1)
        if not technicality:
            return trigger_service_failure(msg=error_msg or "{slug}".format(slug=CARRIER_SLUG), slug=CARRIER_SLUG, vendor_id=vendor_id, desc=blitz_vendor_config.get("description", "") or CARRIER_SLUG)

        return {
            "slug": CARRIER_SLUG,
            "vendor_id": vendor_id,
            "description": blitz_vendor_config.get("description", ""),
            "code": 200,
            "technicality": technicality
        }

    def generate_label(self, retry=0):
        """

        :return:
        """
        if retry > 3:
            return _get_error_resp('Authentication error - Kindly check the carrier credentials currently configured for {}'.format(CARRIER_SLUG.title()))

        shipment = self.__request_data.get('shipment')
        _is_reverse = shipment.get('is_reverse')
        ship_from = shipment.get('ship_from')
        ship_to = shipment.get('ship_to')
        return_to = shipment.get('return_to')
        ship_to_country = ship_to.get('country') or 'IN'

        _is_to_pay = shipment.get('is_to_pay')
        vendor_id = self.__request_data.get('vendor_id')
        user_id = self.__request_data.get('api_token')
        _is_cod = self.__request_data.get('is_cod')

        _is_document = self.__request_data.get('is_document')
        parcels = shipment.get('parcels') or []
        if len(parcels) > 1:
            return _get_error_resp('Multi-box shipments currently not configured for {}'.format(CARRIER_SLUG.title()))

        _db_op = ReadWriteOperation(user_id)
        cfg_vendor_settings = _db_op.get_the_keys(vendor_id, CARRIER_SLUG)
        # TODO: To be taken from DB
        cfg_vendor_settings = {
            'account_type': 'live',
            'username': 'SPLsv9jJC2Zm',
            'password': 'B,PaFYnE58~Jd',
            'use_carrier_label': True
        
        }
        _username = cfg_vendor_settings.get("username")
        _password = cfg_vendor_settings.get("password")

        __service_type = self.__request_data.get('service_type')
        customer_reference = self.__request_data.get('customer_reference')
        order_source = self.__request_data.get('order_source')

        return_carrier_response = asbool(self.__request_data.get('return_carrier_response'))

        invoice_number = self.__request_data.get('invoice_number')
        invoice_date = self.__request_data.get('invoice_date')
        __gst_invoices = self.__request_data.get('gst_invoices', []) or []
        collect_on_delivery = self.__request_data.get('collect_on_delivery', {}).get('amount')
        is_appt_based_delivery = asbool(shipment.get('is_appt_based_delivery'))
        appointment_delivery_details = shipment.get('appointment_delivery_details') or {}
        return_reason = shipment.get('return_reason')
        use_carrier_label = asbool(cfg_vendor_settings.get('use_carrier_label'))

        pre_del_date = ''
        pre_del_slot = ''

        if is_appt_based_delivery and appointment_delivery_details:
            try:
                prefer_delivery_date = appointment_delivery_details.get('appointment_date')
                prefer_delivery_time = appointment_delivery_details.get('appointment_time')
                pre_del_date = prefer_delivery_date.strftime("%Y-%m-%d")
                pre_del_slot = '%s %s' % (pre_del_date, prefer_delivery_time)
            except Exception as e:
                print(str(e))
                pre_del_date = ''

        # print(cfg_vendor_settings)
        use_uploaded_pincodes = asbool(cfg_vendor_settings.get('use_uploaded_pincodes'))
        ignore_service_check = asbool(cfg_vendor_settings.get('ignore_service_check'))

        if use_uploaded_pincodes and not ignore_service_check:
            if _is_cod:
                _method = "cod_pincode"
            elif _is_reverse:
                _method = "reverse_pincode"
            else:
                _method = "prepaid_pincode"
            delivery_available = fetch_pincodes(user_id, vendor_id, ship_to.get('postal_code'), _method)
            if not delivery_available:
                return _get_error_resp('The Destination Pincode is either not serviceable or not configured against the carrier config on your account')
            pickup_available = fetch_pincodes(user_id, vendor_id, ship_from.get('postal_code'), _method)
            if not pickup_available:
                return _get_error_resp('The Origin Pincode is either not serviceable or not configured against the carrier config on your account')

        is_test = True if 'test' == cfg_vendor_settings.get('account_type') else False
        is_qc_checked = shipment.get('is_qc_checked')

        consignment_dimension, total_weight = self.get_box_details(parcels)
        special_instructions = self.__request_data.get('special_instruction')

        pickup_lat = ship_from.get('lat')
        pickup_lng = ship_from.get('lng')
        drop_lat = ship_to.get('lat')
        drop_lng = ship_to.get('lng')

        if not pickup_lng or not pickup_lat:
            pickup_lat, pickup_lng = geocode_address(_flatten_address(ship_from))
        if not drop_lng or not drop_lat:
            drop_lat, drop_lng = geocode_address(_flatten_address(ship_to))

        if None in [pickup_lng, pickup_lat, drop_lng, drop_lat]:
            return _get_error_resp("{slug}: Kindly provide a valid address with latitude & longitude.".format(slug=CARRIER_SLUG.title()))

        url = ENDPOINTS.get('staging' if is_test else 'live', {}).get('booking')
        _url = url or ''

        invoice_number_array = []
        _invoice_amount_list = []
        _ewaybill_list = []
        total_inv_val = 0.0
        for inv in __gst_invoices:
            invoice_number_array.append({
                'invoice_number': inv.get('invoice_number') or '-',
                'invoice_number_value': inv.get('invoice_value'),
            })
            if inv.get('ewaybill_number'):
                _ewaybill_list.append(inv.get('ewaybill_number') or '')
            if inv.get('invoice_value'):
                _invoice_amount_list.append(inv.get("invoice_value"))

        if _invoice_amount_list:
            total_inv_val = sum(_invoice_amount_list)
        else:
            total_inv_val = sum([(ix.get('price', {}).get('amount') * (ix.get('quantity', 1) or 1)) for x in parcels for ix in x.get('items')])

        item_details = []
        parcel_length = 1
        parcel_height = 1
        parcel_width = 1
        for parcel in parcels:
            dimension = parcel.get('dimension', {})
            parcel_length = dimension.get('length', '')
            parcel_width = dimension.get('width', '')
            parcel_height = dimension.get('height', '')

            for item in parcel.get("items", []):
                item_dict = {
                    "name": item.get('description', ''),
                    "description": '{} {}'.format(item.get('description', ''), item.get('variant', '') or ''),
                    "quantity": str(item.get('quantity') or '1'),
                    "item_value": str(item.get('price', {}).get('amount', '')),
                    "skuCode": item.get('sku', '') or ''
                }
                ### below code is for reverse shipment, for now not required ###
                qc_params_list = []
                item_qc_details = item.get('item_qc_details', {})    
                item_url = item_qc_details.get('item_url')
                item_comments = item_qc_details.get('comments')
                item_variant = item_qc_details.get('item_variant')
                item_size = item_qc_details.get('item_size')

                if _is_reverse and is_qc_checked:
                    if item_url:
                        qc_params_list.append("ITEM_IMAGES")
                    if item_comments:
                        qc_params_list.append("BRAND")
                    if item_variant:
                        qc_params_list.append("COLOR")
                    if item_size:
                        qc_params_list.append("SIZE")
                    if item.get('description'):
                        qc_params_list.append("DESCRIPTION")
                    if item.get('quantity'):
                        qc_params_list.append("QUANTITY")
                    if item.get('sku'):
                        qc_params_list.append("SKU")
                    if shipment.get('return_reason'):
                        qc_params_list.append('RETURN_REASON')

                    item_dict.update({"qc_params": qc_params_list})
                else:
                    item_dict.update({"qc_params": []})

                if _is_reverse:
                    item_dict.update({
                        "additional": {
                            "images": item_url,
                            "brand": item_comments,
                            "color": item_variant,
                            "size": item_size,
                            "return_reason": shipment.get('return_reason') or 'wrong product'
                        }
                    })

                item_details.append(item_dict)

        payload = json.dumps({
            "channelId": order_source or 'eShipz',
            "returnShipmentFlag": "true" if _is_reverse else "false",
            "Shipment": {
                "code": customer_reference,
                "orderCode": customer_reference,
                "weight": str(total_weight * 1000),  # grams
                "length": str(parcel_length * 10),   # mm
                "height": str(parcel_height * 10),   # mm
                "breadth": str(parcel_width * 10),   # mm
                "items": item_details
            },
            "deliveryAddressDetails": {
                "name": '{},{}'.format(ship_to.get('contact_name') or '', ship_to.get('company_name') or ''),
                "phone": ship_to.get('phone', ''),
                "address1": '{},{}'.format(ship_to.get('street1') or '', ship_to.get('street2') or ''),
                "address2": ship_to.get('street3') or '',
                "pincode": ship_to.get('postal_code', ''),
                "city": ship_to.get('city', ''),
                "state": ship_to.get('state', ''),
                "country": ship_to.get('country', ''),
                "lat": drop_lat or '',
                "lng": drop_lng or ''
            },
            "pickupAddressDetails": {
                "name": '{},{}'.format(ship_from.get('contact_name') or '', ship_from.get('company_name') or ''),
                "phone": ship_to.get('phone', ''),
                "address1": '{},{}'.format(ship_from.get('street1') or '', ship_from.get('street2') or ''),
                "address2": ship_from.get('street3') or '',
                "pincode": ship_from.get('postal_code', ''),
                "city": ship_from.get('city', ''),
                "state": ship_from.get('state', ''),
                "country": ship_from.get('country', ''),
                "lat": pickup_lat or '',
                "lng": pickup_lng or ''
            },
            "currencyCode": self.__request_data.get('rate', {}).get('currency'),
            "paymentMode": "COD" if _is_cod else "PREPAID",
            "totalAmount": str(total_inv_val),
            "collectableAmount": str(collect_on_delivery) if _is_cod else "0"
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'{self.generate_token(_username, _password, is_test, regenerate_token=retry > 0)}'
        }

        response = requests.request("POST", _url, headers=headers, data=payload)
        print(url)
        print(headers)
        print(payload)
        curl_resp = curlify_carrier_request(response)
        carrier_info = curl_resp if return_carrier_response else None

        print(response.text)
        resp_json = {}
        if response.status_code in [401, 402]:
            return self.generate_label(retry=retry + 1)

        if 199 < response.status_code < 300:
            resp_json = response.json()
            if resp_json.get('status') == 'SUCCESS':
                docket_number = resp_json.get('waybill')
                courierName = resp_json.get('courierName')

                if docket_number:
                    esz_order_id = get_order_id()

                    something_wanting_attention = {
                        "barcodes": '',
                        "docket_number": docket_number,
                        "order_id": esz_order_id,
                        "shipper_address": ship_from,
                        "reciever_address": ship_to,
                        "parcel": parcels,
                        "is_cod": _is_cod,
                        "cod_amt": collect_on_delivery,
                        "cod_currency": "INR",
                        "awb": [docket_number],
                        "service_name": courierName if courierName else __service_type.upper(),
                        "cust_ref": customer_reference,
                        "invoice": invoice_number,
                        "content": self.__request_data.get('parcel_contents'),
                        "source_code": '',
                        "source_location": '',
                        "destination_code": '',
                        "destination_location": '',
                        "is_doc": "docs" if _is_document else "parcel",
                        "customer_code": '',
                        "rto_address": return_to,
                        "is_to_pay": _is_to_pay,
                        "total_weight": total_weight,
                        'ewaybill_number': ','.join(list(set(_ewaybill_list))) if _ewaybill_list and len(_ewaybill_list) > 0 else '',
                        'gst_invoices': self.__request_data.get('gst_invoices'),
                        "payment_mode": self.__request_data.get('payment_mode') or {},
                        "special_instruction": special_instructions
                    }
                    # TODO: AJ - The Above code too could be made generic across all carriers
                    something_wanting_attention.update(update_label_settings_params(user_id=user_id, slug=CARRIER_SLUG, vendor_id=vendor_id))
                    if use_carrier_label:
                        the_label_link = resp_json.get("shippingLabel")
                    else:
                        the_label_link = self.__custom_label(something_wanting_attention)
                    print(the_label_link)
                    # the_label_link = ''

                    deatails = {
                        "request_data": self.__request_data,
                        "order_id": esz_order_id,
                        "docket_number": docket_number,
                        "tracking_number": [docket_number],
                        "label_link": the_label_link,
                        "tracking_link": "https://track.blitznow.in/{}".format(docket_number or ''),
                        "slug": CARRIER_SLUG,
                        "charge_weight_value": "",
                        "charge_weight_unit": "KG",
                        "invoice_link": None,
                        "meta_collection": {
                            'carrier_response': curl_resp.get('carrier_response'),
                            'carrier_request': curl_resp.get('carrier_request'),
                            "src_code": '',
                            "src_loc": '',
                            "dst_code": '',
                            "dst_loc": ''
                        },
                        "is_reverse": _is_reverse,
                        "is_to_pay": _is_to_pay,
                        'async_ops_completed': True
                    }
                    obj = FinalOrderUpdate(deatails)
                    obj.update_db()

                    return success_resp(user_id, esz_order_id, docket_number, the_label_link, slug=CARRIER_SLUG, extra_fields={
                        'org_code': '',
                        'dest_code': '',
                        'customer_reference': customer_reference,
                        'service_type': self.__request_data.get('service_type'),
                        'carrier_info': carrier_info
                    })
            else:
                error_message = resp_json.get('message')
                return _get_error_resp('Error occurred while manifesting Blitz shipment - %s' % error_message)

        return _get_error_resp('Error occurred while manifesting Blitz shipment - %s' % response.text or '-N.A-')

    def cancel_shipment(self):
        """
        :return:
        """
        input_field = self.__request_data or {}
        for orderid in input_field.get('order_id'):
            user_cred = defaultdict()
            shipment_details = Conn().final_orders.find_one({
                'order_id': orderid
            })
            
            # TODO hardcoded
            shipment_details = {
                "order_id": '',
                "customer_referenc": "skjcnio",
                "account_info": {
                    "vendor_id": ""
                },
                "order_status": "success"
            }
            if not shipment_details:
                return CANCELLATION_FAILURE_DEFAULT

            customer_reference = shipment_details.get('customer_referenc')

            shipment_vendor_info = Conn().vendor_info.find_one({
                'user_id': input_field.get('api_token')
            })

            if shipment_vendor_info:
                vendorid = shipment_details.get('account_info', {}).get('vendor_id')
                if vendorid:
                    user_cred = shipment_vendor_info.get('accounts', {}).get(CARRIER_SLUG).get(vendorid)
            #
            # # TODO hardcoded
            user_cred = {
                'account_type': 'live',
                'username': 'SPLsv9jJC2Zm',
                'password': 'B,PaFYnE58~Jd',
            }

            if user_cred:
                _username = user_cred.get('username')
                _password = user_cred.get('password')
                is_test = True if user_cred.get('account_type') == 'test' else False

                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'{self.generate_token(_username, _password, is_test)}',
                }
                payload = json.dumps([{
                    "field": "channel_order_id",
                    "value": customer_reference
                }])
                if shipment_details.get('order_status') in ['success', 'pickup_schedule']:
                    cancel_url = ENDPOINTS.get('staging' if is_test else 'live', {}).get('cancellation')
                    _url = cancel_url or ''
                    response = requests.request("POST", _url, headers=headers, data=payload)
                    print(response.text)
                    if 199 < response.status_code < 300:
                        resp_json = response.json()
                        cancel_resp = resp_json.get('response')
                        status = cancel_resp[0].get('success')
                        if status is True:
                            return CANCELLATION_SUCCESS_DEFAULT
                        elif status is False:
                            cancel_status = copy.deepcopy(CANCELLATION_FAILURE_DEFAULT)
                            cancel_status['meta']['details'] = [cancel_resp[0].get('message', '')]
                            return cancel_status

                    else:
                        return CANCELLATION_FAILURE_DEFAULT

        return CANCELLATION_FAILURE_DEFAULT
