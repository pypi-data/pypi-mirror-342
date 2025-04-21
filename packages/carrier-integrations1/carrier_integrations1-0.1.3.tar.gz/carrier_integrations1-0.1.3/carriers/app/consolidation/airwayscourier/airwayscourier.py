import copy
import json
from collections import defaultdict
from functools import lru_cache
import requests
import time
import base64
from app.additional_settings import fetch_pincodes
from app.consolidation import aslist_cronly, render_shipping_label_html, pdf_merge_from_byte, \
    update_label_settings_params, CANCELLATION_SUCCESS_DEFAULT, CANCELLATION_FAILURE_DEFAULT
from app.consolidation import cred_check_error_msg, cred_check_success_msg, aslist_cronly
from app.consolidation.airwayscourier import CARRIER_SLUG, CARRIER_LOGO, CARRIER_TC
from app.consolidation.airwayscourier import ENDPOINTS
from app.consolidation import trigger_service_failure
from app.consolidation.utilization.db_operations import ReadWriteOperation
from app.consolidation.utilization.final_order_db_updator import FinalOrderUpdate
from app.consolidation.utilization.generic_order_id_generator import get_order_id
from app.consolidation.utilization.utils import success_resp, curlify_carrier_request
from app.consolidation.carrier_integration_base import CarrierIntegration
from app.mongo import Conn
from app.utils import asbool, _get_error_resp

def get_ttl_hash(seconds=86400):
    """Return the same value withing `seconds` time period"""
    return round(time.time() / seconds)

@lru_cache(50)
def fetch_token_map(username, password, is_test, ttl_hash=None):
    """
        # Usage: token, message = fetch_token_map(self.api_key, self.__env, ttl_hash=get_ttl_hash())
    :param username:
    :param password:
    :param env:
    :param ttl_hash:
    :return:
    """
    credentials = f"{username}:{password}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    url = ENDPOINTS.get('staging' if is_test else 'live', {}).get('auth') or ''

    payload = {}

    headers = {
      'Authorization': f'Basic {encoded_credentials}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    response_json = response.json()
    print(url)
    print(headers)
    print(payload)
    print(response.text)

    if 199 < response.status_code < 300:        
        token = response_json.get("authToken")
        return token, 'Success'
    else:
        return None, response_json.get('description')

class AirwaysCourierIntegration(CarrierIntegration):

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
        try:
            token = AirwaysCourierIntegration.generate_token(username, password, is_test)
            if token:
                return cred_check_success_msg(CARRIER_SLUG)
            else:
                return cred_check_error_msg(CARRIER_SLUG)
        except Exception as e:
            print("Error")
            print(str(e))

        return cred_check_success_msg(CARRIER_SLUG)
    
    def get_box_details(self, parcels):
        return super().get_box_details(parcels)

    def _custom_label(self, input_data):
        return super()._custom_label(input_data)

    @staticmethod
    def generate_token(username, password, is_test, regenerate_token=False):
        """
        :param username:
        :param password:
        :param is_test:
        :return:
        """
        ttl_hash = get_ttl_hash()
        if regenerate_token:
            ttl_hash = ttl_hash + 1
        token, message = fetch_token_map(username, password, is_test, ttl_hash=ttl_hash)
        return token
    
    def fetch_quotes(self, request_data, vendor_id, airwayscourier_vendor_config, retry=0):
        """

        :param request_data:
        :param vendor_id:
        :param airwayscourier_vendor_config:
        :param retry:
        :return:
        """
        airwayscourier_vendor_config = {
            'username' : 'MD03',
            'password' : 'MD03@123',
            'account_type' : 'test',
            'service_type' : 'AIR, SURFACE, EXPRESS'
        }
        username = airwayscourier_vendor_config.get('username')
        password = airwayscourier_vendor_config.get('password')
        service_types = airwayscourier_vendor_config.get('service_type')
        if service_types:
            service_types = [str(service).strip().upper() for service in service_types.split(',')]

        is_test = 'test' == airwayscourier_vendor_config.get('account_type')
        env = 'staging' if is_test else 'live'

        ship_from_pincode = request_data.get("shipment", {}).get("ship_from", {}).get('postal_code')
        ship_to_pincode = request_data.get("shipment", {}).get("ship_to", {}).get('postal_code')

        ship_from_url = ENDPOINTS.get(env).get('serviceability').format(pincode = ship_from_pincode)
        ship_to_url = ENDPOINTS.get(env).get('serviceability').format(pincode = ship_to_pincode)

        ship_from_resp = {}
        ship_to_resp = {}
    
        payload = {}
        headers = {
          'Authorization': f'Bearer {self.generate_token(username, password, is_test)}'
        }

        ship_from_response = requests.request("GET", ship_from_url, headers=headers, data=payload)
        ship_to_response = requests.request("GET", ship_to_url, headers=headers, data=payload)    
    
        technicality = []
        if  ship_from_response.status_code == 200 and ship_to_response.status_code == 200:

            ship_from_resp = ship_from_response.json()
            ship_to_resp = ship_to_response.json()
     
            ship_from_code = ship_from_resp.get("serviceStatus").get('code')
            ship_from_desc  = ship_from_resp.get("serviceStatus").get('description')
            ship_to_code = ship_to_resp.get("serviceStatus").get('code')
            ship_to_desc  = ship_to_resp.get("serviceStatus").get('description')

            if ship_from_code == "200"  and ship_from_desc == "Success" and ship_to_code == "200" and ship_to_desc == "Success" :
                for service in service_types :     
                    service_detail = {
                        "error_message": None,
                        "transit_time": None,
                        "detailed_charges": {},
                        "total_charge": {
                            "amount": 0,
                            "currency": 'INR'
                        },
                        "service_type": service.upper(),
                        "charge_weight": {
                            "value": 0.0,
                            "unit": "KG"
                        },
                        "service_name": service.upper(),
                        "info_message": None,
                        "booking_cut_off": None,
                        "delivery_date": None,
                        "pickup_deadline": None
                    }
                    technicality.append(service_detail)
            
        if not technicality:
            return trigger_service_failure(msg="{slug}".format(slug=CARRIER_SLUG), slug=CARRIER_SLUG, vendor_id=vendor_id, desc=airwayscourier_vendor_config.get("description", "") or CARRIER_SLUG)

        return {
            "slug": CARRIER_SLUG,
            "vendor_id": vendor_id,
            "description": airwayscourier_vendor_config.get("description", ""),
            "code": 200,
            "technicality": technicality
        }

    def generate_label(self):
        """
        :return:
        """
        shipment = self.__request_data.get('shipment')
        ship_from = shipment.get('ship_from')
        ship_to = shipment.get('ship_to')
        return_to = shipment.get('return_to')
        ship_to_country = ship_to.get('country') or 'IN'
        _is_reverse = shipment.get('is_reverse')
        _is_to_pay = shipment.get('is_to_pay')

        vendor_id = self.__request_data.get('vendor_id')
        user_id = self.__request_data.get('api_token')

        _is_cod = self.__request_data.get('is_cod')
        _is_document = self.__request_data.get('is_document')
        description = self.__request_data.get('description')
        parcels = shipment.get('parcels', [])
        parcel_dimensions = parcels[0].get('dimension')
        parcel_length = parcel_dimensions.get('length')
        parcel_width = parcel_dimensions.get('width')
        parcel_height = parcel_dimensions.get('height')

        _db_op = ReadWriteOperation(user_id)
        cfg_vendor_settings = _db_op.get_the_keys(vendor_id, CARRIER_SLUG)

        # TODO 
        cfg_vendor_settings = {
            "username" : "MD03",
            "password" : "MD03@123",
            "account_type" : "test",
            "risk_surcharge" : "CLIENT"
        }

        username = cfg_vendor_settings.get('username')
        password = cfg_vendor_settings.get('password')
        # _db_op.get_the_keys(vendor_id, CARRIER_SLUG)
        __service_type = self.__request_data.get('service_type')
        risk_surcharge = cfg_vendor_settings.get('risk_surcharge') or "NONE"

        customer_reference = self.__request_data.get('customer_reference')
        return_carrier_response = asbool(self.__request_data.get('return_carrier_response'))

        invoice_number = self.__request_data.get('invoice_number')
        invoice_date = self.__request_data.get('invoice_date')
        __gst_invoices = self.__request_data.get('gst_invoices', []) or []
        collect_on_delivery = self.__request_data.get('collect_on_delivery', {}).get('amount')
        is_appt_based_delivery = asbool(shipment.get('is_appt_based_delivery'))
        appointment_delivery_details = shipment.get('appointment_delivery_details') or {}
        special_instructions = self.__request_data.get('special_instruction')
        ewaybill_number = __gst_invoices[0].get("ewaybill_number")

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

        use_uploaded_pincodes = asbool(cfg_vendor_settings.get('use_uploaded_pincodes'))
        # ignore_service_check = asbool(cfg_vendor_settings.get('ignore_service_check'))

        if use_uploaded_pincodes:  # and not ignore_service_check:
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
            
        if len(parcels) > 1:
            return _get_error_resp('Multi-box shipments currently not configured for {}'.format(CARRIER_SLUG.title()))

        is_test = True if 'test' == cfg_vendor_settings.get('account_type') else False

        consignment_dimension, total_weight = self.get_box_details(parcels)

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
            total_inv_val = sum([(ix.get('price', {}).get('amount') * (ix.get('quantity', 1) or 1)) for x in parcels for
                                 ix in x.get('items')])
        

        _url = ENDPOINTS.get('staging' if is_test else 'live', {}).get('booking') or ''

        headers = {
          'Authorization': f'Bearer {self.generate_token(username, password, is_test)}',
          'Content-Type': 'application/json'
        }

        payload = {
          "AwbType": "VIRTUAL",
          "WaybillNo": "",
          "OrderId": customer_reference,
          "PickupLocation": ship_from.get('city'),
          "FromCustomer": '{},{}'.format(ship_from.get('contact_name') or '', ship_from.get('company_name') or ''),
          "FromAddress1": '{},{}'.format(ship_from.get('street1') or '', ship_from.get('street2') or ''),
          "FromAddress2": ship_from.get('street3') or '',
          "FromCity": ship_from.get('city') or '',
          "FromPin": ship_from.get('postal_code') or '',
          "FromMobile": ship_from.get('phone') or '',
          "FromPhone": "",
          "FromMail": ship_from.get('email') or '',
          "FromGST": ship_from.get('tax_id') or '',
          "ToCustomer": '{},{}'.format(ship_to.get('contact_name') or '', ship_to.get('company_name') or ''),
          "ToAddress1": '{},{}'.format(ship_to.get('street1') or '', ship_to.get('street2') or ''),
          "ToAddress2": ship_to.get('street3') or '',
          "ToCity": ship_to.get('city') or '',
          "ToPin": ship_to.get('postal_code') or '',
          "ToMobile": ship_to.get('phone') or '',
          "ToPhone": "",
          "ToMail": ship_to.get('email') or '',
          "ToGST": ship_to.get('tax_id') or '',
          "ServiceMode": __service_type.upper(),
          "PayMode": "TOPAY" if _is_to_pay else ("COD" if _is_cod else "PREPAID"),
          "Topay": collect_on_delivery if (_is_to_pay and _is_cod) else 0,
          "COD": collect_on_delivery if not _is_to_pay and _is_cod else 0.0,
          "Contents": "Document" if _is_document else "Others",
          "InvoiceValue": total_inv_val,
          "Weight": total_weight,
          "Length": parcel_length,
          "Width": parcel_width,
          "Height": parcel_height,
          "RiskCoveredBy": risk_surcharge.upper(),                       
          "EwaybillNo": ewaybill_number,
          "TransporterId": "",                        
          "RTOLocation": return_to.get('city')[:10] if return_to.get('city') else '',   ### max upto 10 characters
          "Remarks": description,
          "ReversePickup": "YES" if _is_reverse else "NO"
        }

        response = requests.post(_url, data=json.dumps(payload), headers=headers)
        print(response.text)

        curl_resp = curlify_carrier_request(response)
        carrier_info = curl_resp if return_carrier_response else None
        resp_json = {}
        error_message = ''
        if 199 < response.status_code < 300:
            resp_json = response.json()

            if resp_json.get('code') == '201':
                docket_number = resp_json.get('WayBillNo')

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
                        "service_name": __service_type.upper(),
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

                    the_label_link = self._custom_label(something_wanting_attention)
                    print(the_label_link)
                    # the_label_link = ''

                    deatails = {
                        "request_data": self.__request_data,
                        "order_id": esz_order_id,
                        "docket_number": docket_number,
                        "tracking_number": [docket_number],
                        "label_link": the_label_link,
                        "tracking_link": "https://track.eshipz.com/track?awb=%s" % docket_number or '',
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

                    return success_resp(user_id, esz_order_id, docket_number, the_label_link, slug=CARRIER_SLUG, 
                        extra_fields={
                            'org_code': '',
                            'dest_code': '',
                            'customer_reference': customer_reference,
                            'service_type': self.__request_data.get('service_type'),
                            'carrier_info': carrier_info
                        })
   
        elif response.status_code == 400 :
            resp_json = response.json()
            error_message = resp_json.get('description')
            return _get_error_resp('Error occurred while manifesting AirwaysCourier shipment - %s' % error_message or '-N.A-')

        return _get_error_resp('Error occurred while manifesting AirwaysCourier shipment - %s' % response.text or '-N.A-')

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
                "awb": ["89000069364"],
                "account_info": {
                    "vendor_id": ""
                },
                "order_status": "success"
            }
            if not shipment_details:
                return CANCELLATION_FAILURE_DEFAULT

            awb = shipment_details.get('awb')
            if awb:
                awb = awb[0]

            shipment_vendor_info = Conn().vendor_info.find_one({
                'user_id': input_field.get('api_token')
            })

            if shipment_vendor_info:
                vendorid = shipment_details.get('account_info', {}).get('vendor_id')
                if vendorid:
                    user_cred = shipment_vendor_info.get('accounts', {}).get(CARRIER_SLUG).get(vendorid)

            #TODO
            user_cred = {
                'username' : 'MD03',
                'password' : 'MD03@123',
                "account_type" : "test"
                        }
            if user_cred:
                is_test = True if user_cred.get('account_type') == 'test' else False
                username = user_cred.get('username')
                password = user_cred.get('password')

                headers = {
                      'Authorization': f'Bearer {self.generate_token(username, password, is_test)}'
                    }
                payload = {}

                if shipment_details.get('order_status') in ['success', 'pickup_schedule']:
                    cancel_url = ENDPOINTS.get('staging' if is_test else 'live', {}).get('cancellation').format(tracking_number = awb)
                    _url = cancel_url or ''
                
                    resp = requests.request("DELETE", _url, headers=headers, data=payload)
                    resp_json = resp.json()
                    print(resp.text)
                    if 199 < resp.status_code < 300:                        
                        cancel_status = copy.deepcopy(CANCELLATION_SUCCESS_DEFAULT)
                        cancel_status['meta']['details'] = resp_json.get('description','')
                        return cancel_status
                    else:
                        cancel_status = copy.deepcopy(CANCELLATION_FAILURE_DEFAULT)
                        cancel_status['meta']['details'] = resp_json.get('description','')
                        return cancel_status

        return CANCELLATION_FAILURE_DEFAULT
