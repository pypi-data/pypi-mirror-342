from app.additional_settings import fetch_pincodes
from app.utils import asbool, _get_error_resp, geocode_address, _flatten_address
from dicttodot import DictToDot

def common_generate_label(shipment_data, shipment_box_info):

    shipment = shipment_data.get('shipment', {})
    billing_paid_by = shipment_data.get('billing',{}).get('paid_by') or ''
    description = shipment_data.get('description')
    slug = shipment_data.get('slug')
    purpose = shipment_data.get('purpose')
    order_source = shipment_data.get('order_source')
    parcel_contents = shipment_data.get('parcel_contents')
    _is_document = shipment_data.get('is_document')
    __service_type = shipment_data.get('service_type')
    customer_reference = shipment_data.get('customer_reference')

    ship_from = shipment.get('ship_from', {})
    ship_to = shipment.get('ship_to', {})
    return_to = shipment.get('return_to', {})
    ship_to_country = ship_to.get('country') or 'IN'
    _is_to_pay = shipment.get('is_to_pay')
    cod_currency = shipment_data.get('collect_on_delivery').get('currency') or 'INR'

    vendor_id = shipment_data.get('vendor_id')
    user_id = shipment_data.get('api_token')
    payment_mode = shipment_data.get('payment_mode') or {}

    parcels = shipment.get('parcels') or []
 
    return_carrier_response = asbool(shipment_data.get('return_carrier_response'))

    invoice_number = shipment_data.get('invoice_number')
    invoice_date = shipment_data.get('invoice_date')
    __gst_invoices = shipment_data.get('gst_invoices', []) or []

    collect_on_delivery = shipment_data.get('collect_on_delivery', {}).get('amount')
    is_appt_based_delivery = asbool(shipment.get('is_appt_based_delivery'))
    appointment_delivery_details = shipment.get('appointment_delivery_details') or {}
    return_reason = shipment.get('return_reason')
    special_instructions = shipment_data.get('special_instruction')
    is_qc_checked = shipment.get('is_qc_checked')
    parcels = shipment.get('parcels')

    pre_del_date = ''
    pre_del_slot = ''
    if is_appt_based_delivery and appointment_delivery_details:
        try:
            prefer_delivery_date = appointment_delivery_details.get('appointment_date')
            prefer_delivery_time = appointment_delivery_details.get('appointment_time')
            pre_del_date = prefer_delivery_date.strftime("%Y-%m-%d")
            pre_del_slot = f"{pre_del_date} {prefer_delivery_time}"
        except Exception as e:
            print(str(e))
            pre_del_date = ''

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
        total_inv_val = sum([(ix.get('price', {}).get('amount') * (ix.get('quantity', 1) or 1)) 
                             for x in parcels for ix in x.get('items', [])])

    pickup_lat = ship_from.get('lat')
    pickup_lng = ship_from.get('lng')
    drop_lat = ship_to.get('lat')
    drop_lng = ship_to.get('lng')

    if not pickup_lng or not pickup_lat:
        pickup_lat, pickup_lng = geocode_address(_flatten_address(ship_from))
    if not drop_lng or not drop_lat:
        drop_lat, drop_lng = geocode_address(_flatten_address(ship_to))

    payload_map = {
    "vendor_id": vendor_id,
    "user_id": user_id,
    "billing_paid_by": billing_paid_by,
    "description": description,
    "slug": slug,
    "purpose": purpose,
    "order_source": order_source or 'eShipz',
    "parcel_contents": parcel_contents,

    "ship_from": {
        "contact_name": ship_from.get("contact_name"),
        "company_name": ship_from.get("company_name"),
        "street1": ship_from.get("street1"),
        "city": ship_from.get("city"),
        "state": ship_from.get("state"),
        "postal_code": ship_from.get("postal_code"),
        "country": ship_from.get("country"),
        "type": ship_from.get("type"),
        "phone": ship_from.get("phone"),
        "street2": ship_from.get("street2"),
        "tax_id": ship_from.get("tax_id"),
        "street3": ship_from.get("street3"),
        "fax": ship_from.get("fax"),
        "email": ship_from.get("email"),
        "alias_name": ship_from.get("alias_name"),
        "is_primary": ship_from.get("is_primary"),
    },
    "ship_to": {
        "contact_name": ship_to.get("contact_name"),
        "company_name": ship_to.get("company_name"),
        "street1": ship_to.get("street1"),
        "city": ship_to.get("city"),
        "state": ship_to.get("state"),
        "postal_code": ship_to.get("postal_code"),
        "country": ship_to.get("country"),
        "type": ship_to.get("type"),
        "phone": ship_to.get("phone"),
        "street2": ship_to.get("street2"),
        "tax_id": ship_to.get("tax_id"),
        "street3": ship_to.get("street3"),
        "fax": ship_to.get("fax"),
        "email": ship_to.get("email"),
        "id": ship_to.get("id"),
        "is_primary": ship_to.get("is_primary"),
    },
    "return_to": {
        "contact_name": return_to.get("contact_name"),
        "company_name": return_to.get("company_name"),
        "street1": return_to.get("street1"),
        "city": return_to.get("city"),
        "state": return_to.get("state"),
        "postal_code": return_to.get("postal_code"),
        "country": return_to.get("country"),
        "type": return_to.get("type"),
        "phone": return_to.get("phone"),
        "street2": return_to.get("street2"),
        "tax_id": return_to.get("tax_id"),
        "street3": return_to.get("street3"),
        "fax": return_to.get("fax"),
        "email": return_to.get("email"),
        "id": return_to.get("id"),
        "is_primary": return_to.get("is_primary"),
    },
    "is_reverse": shipment_box_info.get('is_reverse'),
    "is_to_pay": _is_to_pay,
    "is_cod": shipment_box_info.get('is_cod'),
    "cod_currency": cod_currency,
    "is_document": _is_document,
    "service_type": __service_type,
    "customer_reference": customer_reference,
    "return_carrier_response": return_carrier_response,
    "invoice_number": invoice_number,
    "invoice_date": invoice_date,
    "invoice_number_array": invoice_number_array,
    "gst_invoices": __gst_invoices,
    "_ewaybill_list": _ewaybill_list,
    "collect_on_delivery": collect_on_delivery if shipment_box_info.get('is_cod') else 0,
    "box_length": shipment_box_info.get('box_length'),
    "box_width": shipment_box_info.get('box_width'),
    "box_height": shipment_box_info.get('box_height'),
    "item_details": shipment_box_info.get('item_details'),
    "total_weight": shipment_box_info.get('total_weight'),
    "appointment_delivery_details": {
        "is_appt_based_delivery": is_appt_based_delivery,
        "pre_del_date": pre_del_date,
        "pre_del_slot": pre_del_slot,
    },
    "return_reason": return_reason,
    "special_instructions": special_instructions,
    "is_qc_checked": is_qc_checked,
    "total_inv_val": total_inv_val,
    "pickup_coordinates": {
        "lat": pickup_lat,
        "lng": pickup_lng,
    },
    "drop_coordinates": {
        "lat": drop_lat,
        "lng": drop_lng,
    },
    "parcels": parcels,
    "payment_mode": payment_mode,
}
    return DictToDot(payload_map)


    # return {
    #     "vendor_id": vendor_id,
    #     "user_id": user_id,
    #     "billing_paid_by" : billing_paid_by,
    #     "description" : description,
    #     "slug" :slug ,
    #     "purpose" : purpose,
    #     "order_source": order_source or 'eShipz',
    #     "parcel_contents" : parcel_contents,

    #     "ship_from.contact_name": ship_from.get("contact_name"),
    #     "ship_from.company_name": ship_from.get("company_name"),
    #     "ship_from.street1": ship_from.get("street1"),
    #     "ship_from.city": ship_from.get("city"),
    #     "ship_from.state": ship_from.get("state"),
    #     "ship_from.postal_code": ship_from.get("postal_code"),
    #     "ship_from.country": ship_from.get("country"),
    #     "ship_from.type": ship_from.get("type"),
    #     "ship_from.phone": ship_from.get("phone"),
    #     "ship_from.street2": ship_from.get("street2"),
    #     "ship_from.tax_id": ship_from.get("tax_id"),
    #     "ship_from.street3": ship_from.get("street3"),
    #     "ship_from.fax": ship_from.get("fax"),
    #     "ship_from.email": ship_from.get("email"),
    #     "ship_from.alias_name": ship_from.get("alias_name"),
    #     "ship_from.is_primary": ship_from.get("is_primary"),

    #     "ship_to.contact_name": ship_to.get("contact_name"),
    #     "ship_to.company_name": ship_to.get("company_name"),
    #     "ship_to.street1": ship_to.get("street1"),
    #     "ship_to.city": ship_to.get("city"),
    #     "ship_to.state": ship_to.get("state"),
    #     "ship_to.postal_code": ship_to.get("postal_code"),
    #     "ship_to.country": ship_to.get("country"),
    #     "ship_to.type": ship_to.get("type"),
    #     "ship_to.phone": ship_to.get("phone"),
    #     "ship_to.street2": ship_to.get("street2"),
    #     "ship_to.tax_id": ship_to.get("tax_id"),
    #     "ship_to.street3": ship_to.get("street3"),
    #     "ship_to.fax": ship_to.get("fax"),
    #     "ship_to.email": ship_to.get("email"),
    #     "ship_to.id": ship_to.get("id"),
    #     "ship_to.is_primary": ship_to.get("is_primary"),

    #     "return_to.contact_name": return_to.get("contact_name"),
    #     "return_to.company_name": return_to.get("company_name"),
    #     "return_to.street1": return_to.get("street1"),
    #     "return_to.city": return_to.get("city"),
    #     "return_to.state": return_to.get("state"),
    #     "return_to.postal_code": return_to.get("postal_code"),
    #     "return_to.country": return_to.get("country"),
    #     "return_to.type": return_to.get("type"),
    #     "return_to.phone": return_to.get("phone"),
    #     "return_to.street2": return_to.get("street2"),
    #     "return_to.tax_id": return_to.get("tax_id"),
    #     "return_to.street3": return_to.get("street3"),
    #     "return_to.fax": return_to.get("fax"),
    #     "return_to.email": return_to.get("email"),
    #     "return_to.id": return_to.get("id"),
    #     "return_to.is_primary": return_to.get("is_primary"),

    #     "is_reverse": shipment_box_info.get('is_reverse'),
    #     "is_to_pay": _is_to_pay,
    #     "is_cod": shipment_box_info.get('is_cod'),
    #     "cod_currency" : cod_currency,
    #     "is_document": _is_document,
    #     "service_type": __service_type,
    #     "customer_reference": customer_reference,
    #     "order_source": order_source,
    #     "return_carrier_response": return_carrier_response,
    #     "invoice_number": invoice_number,
    #     "invoice_date": invoice_date,
    #     "invoice_number_array" : invoice_number_array,
    #     "gst_invoices": __gst_invoices,
    #     "_ewaybill_list": _ewaybill_list,
    #     "collect_on_delivery": collect_on_delivery if shipment_box_info.get('is_cod') else 0,
    #     "box_length" : shipment_box_info.get('box_length'),
    #     "box_width" : shipment_box_info.get('box_width'),
    #     "box_height" : shipment_box_info.get('box_height'),
    #     "item_details" : shipment_box_info.get('item_details'),
    #     "total_weight" : shipment_box_info.get('total_weight'),
    #      "appointment_delivery_details.is_appt_based_delivery": is_appt_based_delivery,
    #     "appointment_delivery_details.pre_del_date": pre_del_date,
    #     "appointment_delivery_details.pre_del_slot": pre_del_slot,

    #     "return_reason": return_reason,
    #     "special_instructions": special_instructions,
    #     "is_qc_checked": is_qc_checked,
    #     "total_inv_val": total_inv_val,

    #     "pickup_coordinates.lat": pickup_lat,
    #     "pickup_coordinates.lng": pickup_lng,

    #     "drop_coordinates.lat": drop_lat,
    #     "drop_coordinates.lng": drop_lng,
    #     "parcels" : parcels,
    #     "payment_mode" : payment_mode,

    # }


def common_response(response):
    if isinstance(response, list) :
        response = response[0]



def common_vendor_settings(cfg_vendor_settings, shipment_info):
    use_uploaded_pincodes = asbool(cfg_vendor_settings.get('use_uploaded_pincodes'))
    ignore_service_check = asbool(cfg_vendor_settings.get('ignore_service_check'))
    _is_cod = shipment_info.get('is_cod')
    _is_reverse = shipment_info.get('is_reverse')
    ship_from = shipment_info.get('ship_from', {})
    ship_to = shipment_info.get('ship_to', {})
    is_test = True if 'test' == cfg_vendor_settings.get('account_type') else False
    
    if use_uploaded_pincodes and not ignore_service_check:
        
        if _is_cod:
            _method = "cod_pincode"
        elif _is_reverse:
            _method = "reverse_pincode"
        else:
            _method = "prepaid_pincode"
        
        user_id = shipment_info.get('user_id')
        vendor_id = shipment_info.get('vendor_id')
        
        delivery_available = fetch_pincodes(user_id, vendor_id, ship_to.get('postal_code'), _method)
        if not delivery_available:
            return _get_error_resp('The Destination Pincode is either not serviceable or not configured against the carrier config on your account')
        
        pickup_available = fetch_pincodes(user_id, vendor_id, ship_from.get('postal_code'), _method)
        if not pickup_available:
            return _get_error_resp('The Origin Pincode is either not serviceable or not configured against the carrier config on your account')

    return {
        "status": "success",
        "is_test" : is_test
            }

