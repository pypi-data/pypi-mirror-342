import copy
import datetime
import os
import textwrap
import threading

import pdfkit
from jinja2 import Environment, FileSystemLoader

from app.consolidation.utilization.pdf_merger import pdf_merge_from_byte
from app.consolidation.utilization.utils import get_vendor_label_setting

WKHTML_PATH =  r"C:\wkhtmltopdf\bin\wkhtmltopdf.exe"
ZPL_LABEL_FORMATS = ['89x60_zpl', '100x100_zpl', '70x65_zpl']

EZ_CUSTOM_LABELS = {}
COLLECTABLE_PAYMENT_MODES = {}
PAYMENT_MODE_COLLECTABLE_TEXT = {}
link = os.getenv('PIPE') if os.getenv('PIPE') else bytes(WKHTML_PATH, 'UTF8')
_CONFIG = pdfkit.configuration(wkhtmltopdf=link)
_LABEL_PATH = os.path.dirname(os.path.realpath(__file__))


def get_country_name():
    return {}


class ExceptionDuringLabelCancellation(Exception):

    def __init__(self, message):
        super().__init__(message)
        self.msg = message


def cred_check_success_msg(slug=''):
    """

    Returns:

    """
    return {
        "meta": {
            "status": "success",
            "code": 200,
            "message": "The %s API Credentials are valid !" % slug.upper(),
            "details": None

        },
        "data": {}
    }


def cred_check_error_msg(slug='', message=''):
    return {
        "meta": {
            "status": "error",
            "code": 400,
            "message": "The %s API Credentials are not valid - %s!" % (slug.upper(), message or ''),
            "details": None
        },
        "data": {}
    }


def trigger_service_failure(msg, slug, vendor_id, desc):
    """

    :param msg:
    :param slug:
    :param vendor_id:
    :param desc:
    :return:
    """
    return {
        "code": 400,
        "slug": slug,
        "vendor_id": vendor_id,
        "description": desc,
        "technicality": [{
            "error_message": msg,
            "transit_time": None,
            "detailed_charges": [],
            "total_charge": {
                "amount": None,
                "currency": None
            },
            "service_type": None,
            "charge_weight": {
                "value": None,
                "unit": None
            },
            "service_name": None,
            "info_message": None,
            "booking_cut_off": None,
            "delivery_date": None,
            "pickup_deadline": None
        }]
    }


def no_service_message(slug, description, pincode, vendor_id, message=None):
    """

    :param slug:
    :param description:
    :param pincode:
    :param vendor_id:
    :return:
    """
    err_msg = "{} ({}) Either Service is not available or Pincode {} Not In The Uploaded Pincode List.".format(slug, description, pincode)
    offline_service_resp = {
        'code': 400,
        'vendor_id': vendor_id,
        'description': description,
        'slug': slug,
        'error_message': message or err_msg,
        'technicality': [copy.deepcopy(TECHNICALLITY)]
    }
    return offline_service_resp


CANCELLATION_RESP = {
    "meta": {
        "code": 200,
        "status": "success",
        "message": "OK",
        "details": [
            "The Shipment is successfully cancelled on eShipz. Kindly reach out to your carrier partner for operational follow-up."]
    },
    "data": {}
}

PICKUP_CANCELLATION_RESP = {
    "meta": {
        "code": 200,
        "status": "success",
        "message": "OK",
        "details": [
            "The Pickup is successfully cancelled on eShipz. Kindly reach out to your carrier partner for operational follow-up."]
    },
    "data": {}
}

CANCELLATION_SUCCESS_DEFAULT = {
    "meta": {
        "code": 200,
        "status": "success",
        "message": "OK",
        "details": ["The Shipment is successfully cancelled"]
    },
    "data": {}
}

CANCELLATION_FAILURE_DEFAULT = {
    "meta": {
        "code": 200,
        "status": "success",
        "message": "OK",
        "details": [
            "The Shipment cancellation failed. Kindly reach out to your carrier partner for operational follow-up."]
    },
    "data": {}
}

CANCELLATION_FAILURE_ERROR = {
    "meta": {
        "code": 400,
        "status": "failure",
        "message": "ERROR",
        "details": [
            "The Shipment cancellation failed. Kindly reach out to your carrier partner for operational follow-up."]
    },
    "data": {}
}

PICKUP_RESP = {
    'meta': 200,
    'message': 'The pickup would happen as per your SLAs with the carrier partner',
    'data': {
        'status_code': 200,
        'status': 'SUCCESS'
    }
}

_UNSUCCESS_MSG = "Pincode Is Not Serviceability."
_SUCCESS_MSG = "Pincode is Serviceable."

def pickup_response(is_success, message):
    return {
    'meta': 200,
    'message': 'The pickup would happen as per your SLAs with the carrier partner',
    'data': {
        'status_code': 200 if is_success else 400,
        'status': message or "SUCCESS" 
    }
}


def __generate_label_contents(label_size, label_format, html_template, options):
    """

    :param label_size:
    :return:
    """
    if 'pdf' == label_format:
        return pdfkit.from_string(html_template, False, configuration=_CONFIG, options=options)
    else:
        return html_template


def update_label_settings_params(user_id, slug, vendor_id):
    """

    :param user_id:
    :param slug:
    :param vendor_id:
    :param label_settings:
    :return:
    """
    _label_setting = get_vendor_label_setting(user_id, slug, vendor_id)
    _vendor_label_settings = _label_setting.get("accounts", {}).get(slug, {}).get(vendor_id, {})
    label_setting = _vendor_label_settings.get('label_setting', EZ_CUSTOM_LABELS.get('LABEL_CUSTOM_DEFAULT'))
    shipper_logo = _vendor_label_settings.get('logo', '')
    product_mask = _vendor_label_settings.get('product_mask', '')
    label_msg = _vendor_label_settings.get('label_msg', '')
    hide_rto_details = _vendor_label_settings.get('hide_rto_details', False)
    hide_shipper_details = _vendor_label_settings.get('hide_shipper_details', False)
    hide_invoice_value = _vendor_label_settings.get('hide_invoice_value', False)
    hide_shipper_name = _vendor_label_settings.get('hide_shipper_name', False)
    hide_shipper_company = _vendor_label_settings.get('hide_shipper_company', False)
    hide_shipper_address = _vendor_label_settings.get('hide_shipper_address', False)
    hide_sku_variant = _vendor_label_settings.get('hide_sku_variant', False)
    hide_receiver_phone = _vendor_label_settings.get('hide_receiver_phone', False)

    return {
        "label_setting": label_setting,
        "shipper_logo": shipper_logo,
        "product_mask": product_mask,
        "label_msg": label_msg,
        "hide_shipper_name": hide_shipper_name,
        "hide_shipper_company": hide_shipper_company,
        "hide_shipper_address": hide_shipper_address,
        "hide_shipper_details": hide_shipper_details,
        "hide_rto_details": hide_rto_details,
        "hide_invoice_value": hide_invoice_value,
        "hide_receiver_phone": hide_receiver_phone,
        "hide_sku_variant": hide_sku_variant
    }


def render_shipping_label_html(vendor_name, vendor_service, vendor_logo, vendor_tos, input_data, is_master_label, barcode_format='code39', awb=None, label_path=None, custom_label_html=None, label_copy='Master', pdf_options=None, child_label_number=0, capture_dims=False, volumetric_threshold=None, qr_content=None, package_series_range='', carrier_payment_mode=None):
    """

    :param vendor_name:
    :param vendor_service:
    :param vendor_logo:
    :param vendor_tos:
    :param input_data:
    :return:
    """
    from app.utils import datetimeformat

    lock = threading.Lock()
    with lock:
        options = {
            'page-size': 'A5',
            'margin-top': '2',
            'margin-right': '2',
            'margin-left': '2',
            'margin-bottom': '2'
        }
        app_env = 'staging' if 'staging' == os.environ.get('WING') else 'prod'
        regular_label_flow = True
        # number_of_pkgs = len(input_data.get('parcel'))
        reciever_address = input_data.get('reciever_address', {})
        shipper_address = input_data.get('shipper_address', {})
        rto_address = input_data.get('rto_address', {})
        service_name = vendor_service if vendor_service not in ['', None] else input_data.get('service_name', '')
        awb = awb or input_data.get('awb')
        # Gati Specific
        docket_number = input_data.get('docket_number')
        service_name = service_name.replace('_', ' ')

        #
        template_folder_path = label_path or _LABEL_PATH
        j2_env = Environment(loader=FileSystemLoader(template_folder_path), trim_blocks=True)
        j2_env.filters['datetimeformat'] = datetimeformat

        tw = textwrap.TextWrapper(width=12)

        address_shipper_wrap = tw.wrap(" ".join([input_data.get('shipper_address', {}).get('street1') or '',
                                                 input_data.get('shipper_address', {}).get('street2') or '',
                                                 input_data.get('shipper_address', {}).get('street3') or '']))
        address_consinee_wrap = tw.wrap(" ".join([input_data.get('reciever_address', {}).get('street1') or '',
                                                  input_data.get('reciever_address', {}).get('street2') or '',
                                                  input_data.get('reciever_address', {}).get('street3') or '']))
        label_setting = input_data.get('label_setting')
        label_html = 'label.html'
        label_format = 'pdf'

        if label_setting == EZ_CUSTOM_LABELS.get('LABEL_CUSTOM_INVOICE_PLUS_LBL_LANDSCAPE'):
            options = {
                'page-size': 'A5',
                'margin-top': '2',
                'margin-right': '2',
                'margin-left': '2',
                'margin-bottom': '2'
                # 'margin': '2px'
            }
            label_html = 'format1.html'
            label_format = 'pdf'
        elif label_setting == EZ_CUSTOM_LABELS.get('LABEL_CUSTOM_INVOICE_PLUS_LBL_POTRAIT'):
            options = {
                'page-size': 'A5',
                'margin-top': '2',
                'margin-right': '2',
                'margin-left': '2',
                'margin-bottom': '2'
                # 'margin': '2px'
            }
            label_html = 'format2.html'
            label_format = 'pdf'
        elif label_setting == EZ_CUSTOM_LABELS.get('LABEL_CUSTOM_4x6'):
            options = {
                'page-height': '148mm',
                'page-width': '105mm',
                'orientation': 'portrait',
                'margin-top': '1',
                'margin-right': '1',
                'margin-left': '1',
                'margin-bottom': '1'
            }
            label_html = 'thermal_4_6.html'
            label_format = 'pdf'
        elif label_setting == EZ_CUSTOM_LABELS.get('LABEL_CUSTOM_4x3'):
            options = {
                'page-height': '60mm',
                'page-width': '89mm',
                'orientation': 'portrait',
                'margin-top': '1',
                'margin-right': '1',
                'margin-left': '1',
                'margin-bottom': '1'
            }
            label_html = 'sticker_label_pdf_4_3.html'
            label_format = 'pdf'
        elif label_setting == EZ_CUSTOM_LABELS.get('LABEL_CUSTOM_4x3_B2B_POD_LABEL'):
            options = {
                'page-height': '60mm',
                'page-width': '89mm',
                'orientation': 'portrait',
                'margin-top': '1',
                'margin-right': '1',
                'margin-left': '1',
                'margin-bottom': '1'
            }
            label_html = 'sticker_label_pdf_4_3.html'
            label_format = 'pdf'
        elif label_setting == EZ_CUSTOM_LABELS.get('LABEL_CUSTOM_B2B_DOCKET'):
            options = {
                'page-height': '297mm',
                'page-width': '210mm',
                'orientation': 'portrait',
                'margin-top': '1',
                'margin-right': '1',
                'margin-left': '1',
                'margin-bottom': '1'
            }
            label_html = 'b2bdocket.html'
            label_format = 'pdf'
        # print(label_setting)
        shipper_complete_address = textwrap.wrap(' '.join(list(set([shipper_address.get('street1', "") or '',
                                                                    shipper_address.get('street2', "") or '',
                                                                    shipper_address.get('street3', "") or '']))).replace(',,', ','), 70, break_long_words=False)

        receiver_complete_address = textwrap.wrap(' '.join(list(set([reciever_address.get('street1', "") or '',
                                                                     reciever_address.get('street2', "") or '',
                                                                     reciever_address.get('street3', "") or '']))).replace(',,', ','), 70, break_long_words=False)

        return_address = " ".join(list(set([rto_address.get('contact_name', '') or '' + ",",
                                            rto_address.get('company_name', " ") or '' + ",",
                                            rto_address.get('street1', " ") or '',
                                            rto_address.get('street2', " ") or '',
                                            rto_address.get('street3', " ") or '' + " ,",
                                            rto_address.get('city', "") or '' + "-",
                                            rto_address.get('postal_code', '') or '',
                                            rto_address.get('state', "") or '', ])))

        _wgtz = []
        _dimz = []
        dims_map = {}
        total_act_wt = sum([i.get('weight', {}).get('value') for i in input_data.get('parcel')]) if is_master_label else \
            input_data.get('parcel')[child_label_number].get('weight', {}).get('value')
        total_vol_wt = total_act_wt
        if capture_dims:
            total_vol_wt = 0.0
            for box in input_data.get('parcel', []):
                _vol_wt = 0.0
                _dim = box.get('dimension', {})
                try:
                    if volumetric_threshold is not None and type(volumetric_threshold) is str and volumetric_threshold.isnumeric() and float(volumetric_threshold) > 0:
                        _vol_wt = round((
                                                _dim.get('length') * _dim.get('width') * _dim.get('height')) / float(volumetric_threshold), 2)
                except Exception as e:
                    _vol_wt = 0.0

                total_vol_wt += _vol_wt
                _dim.update({
                    'vol_wt': _vol_wt
                })
                _dimz.append(_dim)
                _wt = sum([i.get('weight', {}).get('value') or 0 for i in box.get('items') or []])
                lbh = '%s|%s|%s|%s' % (_dim.get('length'), _dim.get('width'), _dim.get('height'), str(_wt))
                _parcel_count = dims_map.get(lbh) or 0
                dims_map[lbh] = _parcel_count + 1
                _wgtz.append(_wt)
        # print(custom_label_html, label_path)
        gst_invoices = input_data.get('gst_invoices') or []

        ewaybill_numbers = []
        invoice_numbers = []
        _invoice_amount_list = []

        if input_data.get('ewaybill_number'):
            ewaybill_numbers.append(input_data.get('ewaybill_number') or '')
        if not gst_invoices and (input_data.get('invoice') or input_data.get('invoice_number')):
            invoice_numbers.append(input_data.get('invoice') or input_data.get('invoice_number') or '')

        # {'invoice_value': 2222.0, 'ewaybill_number': '', 'invoice_date': '', 'invoice_number': '2222', 'ewaybill_date': ''}
        for invoice in gst_invoices:
            if invoice.get('invoice_number'):
                invoice_numbers.append(invoice.get('invoice_number'))
            if invoice.get('ewaybill_number'):
                ewaybill_numbers.append(invoice.get('ewaybill_number'))
            if invoice.get('invoice_value'):
                _invoice_amount_list.append(invoice.get('invoice_value'))

        currency = "INR"
        for parcel in input_data.get("parcel", []):
            if parcel.get("items", []):
                currency = parcel.get("items")[0].get("price", {}).get("currency")
                break

        # tmp fix for LogicERP to use the gst_invoices list for total invoice amount
        if _invoice_amount_list:
            total_inv_val = sum(_invoice_amount_list)
        else:
            total_inv_val = sum([ix.get('price').get('amount') * ix.get('quantity') for x in input_data.get('parcel')
                                 for ix in x.get('items') or []])

        html_master = ''
        mode_option = 'cash'
        try:
            mode_option = input_data.get('payment_mode', {}).get('mode_option') or 'cash'
        except Exception as e:
            mode_option = 'cash'
        favor_of_name = ''
        # tmp for carriers that dont want Pre-Paid on the label
        payment_mode = 'prepaid' if not input_data.get('is_cod') else mode_option
        if carrier_payment_mode and PAYMENT_MODE_COLLECTABLE_TEXT.get(carrier_payment_mode):
            payment_mode = carrier_payment_mode
        payment_mode_text = PAYMENT_MODE_COLLECTABLE_TEXT.get(payment_mode)
        if mode_option in COLLECTABLE_PAYMENT_MODES and payment_mode not in ['prepaid', 'tbb']:
            payment_mode_text = '%s %s %s' % (
            payment_mode_text or '', str(input_data.get('cod_amt')) if payment_mode not in ['fod_dod', 'fod'] else '',
            str(input_data.get("cod_currency", "INR")) if payment_mode not in ['fod_dod', 'fod'] else '')
            if 'cash' != mode_option:
                favor_of_name = "In Favor Of: {}".format(input_data.get('payment_mode', {}).get('favour_name') or '') if mode_option in COLLECTABLE_PAYMENT_MODES and input_data.get('payment_mode', {}).get('favour_name') else ""

        try:
            label_html_tmpl = custom_label_html or label_html
            html_master = j2_env.get_template(label_html_tmpl).render(app_env=app_env, hide=not is_master_label,  # This should be deprecated once removed from all labels
                is_child_label=not is_master_label, is_to_pay=input_data.get('is_to_pay'), date=datetime.datetime.now().strftime("%d/%m/%Y"), b_datetime=datetime.datetime.utcnow(), awb=awb, favour_name=favor_of_name, weight=total_act_wt, consinee_pincode=reciever_address.get('postal_code'), consinee_name=reciever_address.get('contact_name'), consinee_company_name=reciever_address.get('company_name'), consinee_address=address_consinee_wrap, consinee_city_pincode=reciever_address.get('postal_code'), consinee_city_address=reciever_address.get('city'), consinee_state=reciever_address.get('state'), consinee_country=get_country_name(reciever_address.get('country')), consinee_phone=reciever_address.get('phone'), consinee_gst=reciever_address.get('tax_id'), consinee_address_lines=receiver_complete_address, invoice_no=','.join(filter(None, list(set(invoice_numbers)))), cust_ref=input_data.get('cust_ref'), shipper_name=shipper_address.get('contact_name'), shipper_company_name=shipper_address.get('company_name'), shipper_address=address_shipper_wrap, shipper_city_address=shipper_address.get('city'), shipper_city_pincode=shipper_address.get('postal_code'), shipper_country=get_country_name(shipper_address.get('country')), shipper_state=shipper_address.get('state'), shipper_phone=shipper_address.get('phone'), shipper_gst=shipper_address.get('tax_id'), shipper_address_lines=shipper_complete_address,  # b_code=generate_barcode(input_data.get('awb')),
                is_doc=input_data.get('is_doc'), sort_code="", pkg_count=len(input_data.get('parcel')) if is_master_label else "{} of {}".format(child_label_number + 1, len(input_data.get('parcel'))), t_number=awb, source_code=input_data.get("source_code") or '', source_location=input_data.get("source_location") or '', destination_code=input_data.get("destination_code") if input_data.get("destination_code") else "", destination_location=input_data.get("destination_location") if input_data.get("destination_code") else " ", content=input_data.get('content'), value=total_inv_val, value_currency=currency, order_id=input_data.get('order_id'), payment_mod=payment_mode_text, cod_amt=str(input_data.get('cod_amt')) + " " + input_data.get("cod_currency", "INR") if input_data.get('is_cod') else "", vendor_name=vendor_name.upper() if vendor_name else '', logo=vendor_logo if vendor_logo else '', service_name=service_name, tos_link=vendor_tos, customer_code=input_data.get('customer_code'), return_address=return_address, shipper_logo=input_data.get('shipper_logo', ''), items=[
                    i for x in input_data.get('parcel') for i in x.get('items') or []], pkg_dimension=
                input_data.get('parcel')[child_label_number].get('dimension'), pkg_case_number=
                input_data.get('parcel', [{}])[
                    child_label_number].get('box_no') or '' if not is_master_label else '', product_mask=input_data.get('product_mask', ''), label_msg=input_data.get('label_msg', ''), special_instruction=input_data.get('special_instruction'), ewb=','.join(filter(None, list(set(ewaybill_numbers)))), pkg_dimensions=_dimz, pkg_weights=_wgtz, total_vol_wt=total_vol_wt, dims_map=dims_map, hide_invoice_value=input_data.get('hide_invoice_value', False), hide_receiver_phone=input_data.get('hide_receiver_phone', False), hide_rto_details=input_data.get('hide_rto_details', False), hide_shipper_details=input_data.get('hide_shipper_details', False), hide_shipper_name=input_data.get('hide_shipper_name', False), hide_shipper_company=input_data.get('hide_shipper_company', False), hide_shipper_address=input_data.get('hide_shipper_address', False), hide_sku_variant=input_data.get('hide_sku_variant', False), total_inv_val=total_inv_val, show_payment_mode=regular_label_flow, barcode_format=barcode_format, copy_type=label_copy.title() if label_copy else '', gst_invoices=gst_invoices, docket_number=docket_number or '', qr_content=qr_content, package_series_range=package_series_range)

        except Exception as e:
            print("############ Error #############")
            print(str(e))
            print("############ End Error #############")
        print(html_master)
        return pdfkit.from_string(html_master, False, configuration=_CONFIG, options=pdf_options or options)


def aslist_cronly(value):
    if isinstance(value, (str,)):
        value = filter(None, [x.strip() for x in value.splitlines()])
    return list(value)


TECHNICALLITY = {
    "error_message": None,
    "transit_time": None,
    "detailed_charges": [],
    "total_charge": {
        "amount": None,
        "currency": None
    },
    "service_type": None,
    "charge_weight": {
        "value": "",
        "unit": "KG"
    },
    "service_name": None,
    "info_message": None,
    "booking_cut_off": None,
    "delivery_date": None,
    "pickup_deadline": None
}
