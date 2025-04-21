from datetime import datetime

import curlify

from app.mongo import Conn


def curlify_carrier_request(response_object):
    """

    :param response_object:
    :return:
    """
    if response_object:
        try:
            return {
                "carrier_request": curlify.to_curl(response_object.request),
                "carrier_response": response_object.text,
            }
        except Exception as e:
            try:
                return {
                    'carrier_request': '',
                    "carrier_response": response_object.text,
                }
            except Exception as e:
                pass
    return {
        'carrier_request': '',
        "carrier_response": '',
    }


def get_vendor_label_setting(user_id, slug=None, vendor_id=None):
    try:
        _label_setting = Conn().vendor_info.find_one({
            "user_id": user_id
        })
        return _label_setting
    except Exception as ex:
        print(ex)
    return {}


def success_resp(api, order_id, awb, the_label_link, slug=None, extra_fields={}):
    if type(awb) is list:
        awb = awb
    else:
        awb = [awb]
    resp1 = {
        "data": {
            "user_id": api,
            "order_id": order_id,
            "description": "",
            "slug": slug,
            "tracking_link": "",
            "customer_reference": extra_fields.get('customer_reference') or '',
            "rate": {
                "charge_weight": {
                    "value": extra_fields.get('charge_weight') or '',
                    "unit": "KG"
                },
                "service_type": extra_fields.get('service_type') or '',
                "booking_cut_off": None,
                "total_charge": {
                    "amount": extra_fields.get('total_charge') or '',
                    "currency": "INR"
                },
                "error_message": None,
                "detailed_charges": [],
                "service_name": "",
                "info_message": None,
                "delivery_date": None,
                "transit_time": None,
                "pickup_deadline": None
            },
            "tracking_numbers": awb,
            "service_type": extra_fields.get('service_type') or '',
            "references": [],
            "created_at": str(datetime.utcnow().isoformat()),
            "ship_date": "",
            "status": "created",
            "updated_at": str(datetime.utcnow().isoformat()),
            "entered_weight": {
                "value": "",
                "unit": ""
            },

            "files": {
                "label": {
                    "paper_size": extra_fields.get('paper_size') if extra_fields.get('paper_size') else "PAPER_4X6",
                    "label_meta": {
                        'awb': awb[0],
                        'url': the_label_link,
                        'org_code': extra_fields.get('org_code') or '',
                        'dest_code': extra_fields.get('dest_code') or '',
                        'package_series': extra_fields.get('package_numbers') or [],
                        'package_sticker_url': extra_fields.get('package_sticker_url')
                    },
                    "file_type": "pdf",
                    "invoice": ""
                }
            }
        }
    }
    if 'carrier_info' in extra_fields and extra_fields.get('carrier_info'):
        resp1['data'].update({
            'carrier_exchange': extra_fields.get('carrier_info')
        })
    meta = {
        "meta": {
            "code": 200,
            "message": "OK",
            "details": []
        }
    }
    resp1.update(meta)
    return resp1


def label_error_resp(err_msg, carrier_info=None):
    fullresp = {
        "meta": {
            "status": "error",
            "code": 400,
            "message": "The request was invalid or cannot be otherwise served.",
            "details": [err_msg]

        },
        "data": {}
    }
    if carrier_info:
        fullresp['data'].update({
            'carrier_exchange': carrier_info
        })
    return fullresp


def rate_resp(res_data):
    """
    res_data = {
        "vendor_id":{
            description= "", # data coming from db,
            "slug":
            service_type:{
                is_success = True/False,
                "charges":"",
                error_message:
                info_message:
            }
        },
        "vendor_id":{....}

    }
    """
    final_resp = []
    for i in res_data:
        data = {
            "code": "",
            "description": res_data.get(i).get('description'),
            "slug": res_data.get(i).get('slug'),
            'vendor_id': i,
            "technicality": []
        }
        for j in res_data[i]:
            data['code'] = 200 if res_data.get(i).get(j).get('is_success') else 400
            data['description'] = res_data.get(i).get(j).get('description')
            data['slug'] = res_data.get(i).get(j).get('slug')
            data['vendor_id'] = i
            d = {
                "booking_cut_off": None,
                "charge_weight": {
                    "unit": "KG",
                    "value": res_data.get(i).get(j).get('charge_weight')
                },
                "delivery_date": None,
                "detailed_charges": [],
                "error_message": res_data.get(i).get(j).get('error_message'),
                "info_message": None,
                "pickup_deadline": None,
                "service_name": None,
                "service_type": j,
                "total_charge": {
                    "amount": res_data.get(i).get(j).get('charges'),
                    "currency": "INR"
                },
                "transit_time": None
            }
            data['technicality'].append(d)
        final_resp.append(data)
    return final_resp


ECZ_TO_VENDOR_NAME_MAPPER = {
    "delhivery": "Delhivery",
    "fedex": "FedEx",
    "ecom_express": "Ecom Express",
    "ecom_express_surface": "Ecom Express",
    "delhivery_surface": "Delhivery",
    "xpressbees": "Xpressbees",
    "dotzot": "DotZot",
    "madhur": "Madhur Courier Services",
    "customer_self_network": "Bluepaymax",
    "aramex": "Aramex",
    "ups": "UPS",
    "lets_transport": "Lets Transport", # "dotzot": "DotZot",
    "vrl": "VRL Couriers",
    "antron_express": "Antron Express",
    "ecom_shipping": "VCaN Economy",
    "india_post": "India Post EMS",
    "dhl_ecommerce": "DHL eCommerce",
    "dhl_express": "DHL Express",
    "ecom_shipping_large": "VCaN Economy",
    "delhivery_intl": "Delhivery",
    "gms_india": "GMS Worldwide Express",
    'unique5pl': 'Unique 5PL',
    'growever': 'Growever'
}


def get_ndr_resp_obj(waybill=None, ez_order_id=None, slug=None, action=None, ndr_request_exist=None, status=None, action_data=None, remark=None):
    return {
        "waybill": waybill,
        "slug": slug,
        "status": status,
        "ez_order_id": ez_order_id,
        "NDRRequestExist": ndr_request_exist,
        "remark": remark,
        "action": action,
        "action_data": action_data
    }


def compute_charged_weight(parcels=[]):
    """

    :return:
    """
    if parcels:
        return sum([i.get('weight', {}).get('value') for i in parcels])
    return 0.0

# if __name__ == "__main__":
#     from json import dumps
#     d = {
#         "123213131":{
#             "ECOM_EXPRESS_PARCEL":{
#                 "description":"test_fedex",
#                 "slug":"ecom_express",
#                 "charges":"123",
#                 "error_message":None,
#                 "info_message":None
#             }
#         },
#         "123214131":{
#             "ECOM_EXPRESS_PARCEL":{
#                 "description":"test_fedex",
#                 "slug":"ecom_express",
#                 "charges":"123",
#                 "error_message":None,
#                 "info_message":None
#             }
#         }
#     }
#     r = rate_resp(d)
#     print(dumps(r, indent=4))
