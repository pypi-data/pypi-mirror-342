"""
This module update the all order details into final orders collection

this module takes input standard format of dictionary

{
    "request_data"{"blah":"blah"}, type(input rquest)
    "order_id":"EZBLAH" type() --> string
    "tracking_number":blah blah, type() --> string
    "label_link":"blah", type() -->> string
    "tracking_link":"blah", type() --> string
    "slug":"blah" type() -- > string
    "charge_weight_value":"blah" type() -->> string
    "charge_weight_unit": "blah" type() --> string
    "invoice_link" : "link" type() --> string
}
"""
# uncomment
import uuid

import pytz
# from app.constants import DEFAULT_TIMEZONE, VENDOR_NAMES
from app.utils import asbool
from app.mongo import Conn
from collections import defaultdict
from datetime import datetime, timedelta
import dateutil.parser
import json
import os
import datetime as dt


DEFAULT_TIMEZONE = 'Asia/Kolkata'
VENDOR_NAMES = {}
TRACKING_SERVER_IP = os.getenv('TRACKING_URL', 'https://track.eshipz.com')
TRACKING_LINK = "{}/track?awb={}&slug={}"

BD_DEFAULT_TRACKING_LINK = "https://www.bluedart.com/web/guest/trackdartresultthirdparty?trackFor=0&trackNo={}"

class FinalOrderUpdate(object):
    """

    """
    def __init__(self, details):
        """

        :param details:
        """
        self.details_data = details

    def update_db(self):
        """

        :return:
        """
        # Fedex MPS creates multiple tracking numbers
        # check if the tracking is list or not
        is_list = False
        __awb_numbers = self.details_data.get('tracking_number')
        __tracking_number = self.details_data.get('tracking_number')

        if __awb_numbers and isinstance(__awb_numbers, list):
            is_list = True
            if self.details_data.get('docket_number'):
                __tracking_number = self.details_data.get('docket_number')
            else:
                __tracking_number = str(__awb_numbers[0]) if len(__awb_numbers) > 0 else ''

        ordinfo = defaultdict(dict)
        request_data = self.details_data.get('request_data', {}) or {}
        __utcnow = datetime.utcnow()
        # Handling for ship date, if passed via API
        shipment_date = request_data.get('shipment_date')
        shipment_date_tz = request_data.get('shipment_date_tz') or DEFAULT_TIMEZONE
        # Handling as a way to figure out when was the shipment data pushed to us, in case they pass a different shipment_date
        created_date = __utcnow
        __slug = self.details_data.get('slug') if 'offline' == request_data.get('slug') and self.details_data.get('slug') else request_data.get('slug')

        if shipment_date:
            try:
                if type(shipment_date) == str:
                    shipment_date = dateutil.parser.parse(shipment_date)
                try:
                    default_timezone = shipment_date_tz
                    local_tz = pytz.timezone(default_timezone)
                    local_sdt = local_tz.localize(shipment_date, is_dst=None)
                    shipment_date = local_sdt.astimezone(pytz.utc)
                except Exception as e:
                    pass
            except:
                shipment_date = __utcnow
        else:
            shipment_date = __utcnow


        tracking_link = BD_DEFAULT_TRACKING_LINK.format(__tracking_number) if "bluedart" == __slug else TRACKING_LINK.format(TRACKING_SERVER_IP, __tracking_number, __slug)  # self.details_data.get('tracking_link')
        if request_data.get('tracking_link'):
            tracking_link = request_data.get('tracking_link')
        gst_invoices = request_data.get('gst_invoices', []) or []
        ordinfo['date'] = shipment_date
        ordinfo['latest_checkpoint_date'] = created_date
        ordinfo['creation_date'] = created_date
        ordinfo['is_to_pay'] = self.details_data.get('is_to_pay', False) or False
        ordinfo['is_reverse'] = self.details_data.get('is_reverse') or False
        ordinfo['order_id'] = self.details_data.get('order_id')
        ordinfo['order_source'] = request_data.get('order_source', 'manual')
        ordinfo['parcel_contents'] = request_data.get('parcel_contents')
        ordinfo['service_type'] = request_data.get('service_type')
        ordinfo['paper_size'] = request_data.get('paper_size')
        ordinfo['service_options']['type'] = 'cod' if request_data.get('is_cod') else 'prepaid'
        ordinfo['service_options']['currency'] = request_data.get('collect_on_delivery', {}).get('currency')
        ordinfo['service_options']['amount'] = request_data.get('collect_on_delivery', {}).get('amount')
        ordinfo['service_options']['cod_return_label'] = None

        vendor_id = request_data.get('vendor_id')
        ordinfo.update({
            'account_info': {
                'user_id': request_data.get('api_token'),
                'vendor_id': vendor_id,
                'description': request_data.get('description')
            }
        })

        ordinfo['order_details']['sender_address'] = self._get_parsed_address('sender')
        ordinfo['order_details']['receiver_address'] = self._get_parsed_address('receiver')
        ordinfo['order_details']['return_to'] = self._get_parsed_address('return')

        '''  # Its an expensive operation to perform here
        opa_list = []
        oda_list = []
        pincode_details = Conn().pincode_settings.find_one({"user_id": request_data.get('api_token')}, {vendor_id:1,"_id":0})
        opa_pincodes = [[opa_list.append(k) for k in pin.keys()] for pin in pincode_details.get(vendor_id,{}).get('opa_pincode',[])] if pincode_details else []
        oda_pincodes = [[oda_list.append(k) for k in pin.keys()] for pin in pincode_details.get(vendor_id,{}).get('oda_pincode',[])] if pincode_details else []

        ordinfo['order_details']['sender_address']['is_opa'] = True if opa_list and self._get_parsed_address('sender').get('postal_code',"") in opa_list else False
        ordinfo['order_details']['receiver_address']['is_oda'] = True if oda_list and self._get_parsed_address('receiver').get('postal_code',"") in oda_list else False
        '''
        __parcels = request_data.get('shipment', {}).get('parcels', [{}])
        if self.details_data.get('parcels'):
            __parcels = self.details_data.get('parcels')

        # Lets convert customer Ref / Tracking Number to a single case
        customer_reference = request_data.get('customer_reference')
        consignee_reference = request_data.get('consignee_reference')
        addl_reference = request_data.get('addl_reference')
        if customer_reference:
            customer_reference = str(customer_reference).upper()
        if consignee_reference:
            consignee_reference = str(consignee_reference).upper()
        if addl_reference:
            addl_reference = str(addl_reference).upper()
        if __tracking_number:
            __tracking_number = str(__tracking_number).upper()

        ordinfo['parcels'] = __parcels
        ordinfo['awb'] = __awb_numbers if is_list else [__tracking_number]
        __label_meta = {
            "awb": __tracking_number,
            "url": self.details_data.get('label_link'),
            'master_label_count': self.details_data.get('master_label_count', 0),
            'box_count': len(__parcels),
            'package_numbers': self.details_data.get('package_numbers') or []
        }
        if self.details_data.get('package_sticker_url'):
            __label_meta.update({
                'package_sticker_url': self.details_data.get('package_sticker_url')
            })
        ordinfo['label_meta'] = __label_meta
        total_charge_amount = self.details_data.get('rate', {}).get('amount') or request_data.get('rate', {}).get('amount')
        total_charge_curr = self.details_data.get('rate', {}).get('currency') or request_data.get('rate', {}).get('currency')
        # To enable Forwarding via TrackMile
        if request_data.get('forwarding_id'):
            update_dict = {
                '$push': {
                    'forwarding_details': {
                        'forwarding_order_id': self.details_data.get('order_id'),
                        'forwarding_slug': __slug,
                        'forwarding_service_type': request_data.get('service_type'),
                        'forwarding_awb': __tracking_number,
                        'forwarding_url': self.details_data.get('label_link'),
                        'package_sticker_url': self.details_data.get('package_sticker_url'),
                        'is_active': True
                    }
                }
            }
            Conn().final_orders.update_one({'order_id': request_data.get('forwarding_id')}, update_dict)

        ordinfo['charge_weight']['value'] = self.details_data.get('charge_weight_value')
        ordinfo['charge_weight']['unit'] = self.details_data.get('charge_weight_unit')
        ordinfo['total_charge']['amount'] = total_charge_amount
        ordinfo['total_charge']['currency'] = total_charge_curr

        # Provision to Capture the Offline Carrier slug
        ordinfo['slug'] = __slug
        ordinfo['slug_details'] = self.details_data.get('slug_details')
        ordinfo['package_count'] = self._get_pkg_count()
        ordinfo['purpose'] = request_data.get('purpose')

        ordinfo['is_cod'] = request_data.get('is_cod')
        ordinfo['order_status'] = 'pickup_schedule' if self.details_data.get('pickup_meta', {}).get('pickup_request', False) else 'success'
        ordinfo['shipment_type'] = 'document' if request_data.get('is_document') else 'parcel'
        ordinfo['customer_referenc'] = str(customer_reference).upper() if customer_reference else None
        ordinfo['addl_reference'] = str(addl_reference).upper() if addl_reference else None
        ordinfo['consignee_reference'] = str(consignee_reference).upper() if consignee_reference else None
        # Arvind Fashions - start
        ordinfo['custom_fields'] = {
            'channel_code': request_data.get('channel_code'),
            'channel_desc': request_data.get('channel_desc'),
            'brand_code': request_data.get('brand_code'),
            'brand_desc': request_data.get('brand_desc'),
            'total_shipment_quantity': request_data.get('total_shipment_quantity')
        }
        # Arvind Fashions - end
        # ordinfo['invoice_number'] = resp.get('data').get('invoice_numbe')
        ordinfo['entered_weight']['unit'] = self._get_weight_unit()
        ordinfo['entered_weight']['value'] = self._get_entered_weight()
        ordinfo['invoice_details']['invoice_link'] = self.details_data.get('invoice_link')
        ordinfo['invoice_details']['invoice_number'] = request_data.get('invoice_number')
        ordinfo['invoice_details']['invoice_date'] = request_data.get("invoice_date")
        ordinfo['invoice_details']['ewaybill_number'] = request_data.get("shipment", {}).get("eWaybillNumber","")
        ordinfo['invoice_details']['amount'] = self._get_invoice_amount()
        ordinfo['invoice_details']['total_invoice_amount'] = self._get_invoice_amount(gst_invoices)
        ordinfo['invoice_details']['currency'] = self._get_invoice_currency()
        ordinfo['tracking_link'] = tracking_link
        ordinfo['meta_collection'] = self.details_data.get('meta_collection')
        ordinfo['tracking_status'] = "InfoReceived"
        ordinfo['active'] = True
        ordinfo['is_track_only'] = asbool(self.details_data.get('is_track_only'))
        ordinfo['labels_downloaded'] = False
        ordinfo['async_ops_completed'] = self.details_data.get('async_ops_completed')
        ordinfo['label_contents'] = self.details_data.get('label_contents')
        ordinfo['label_format'] = self.details_data.get('label_format') or 'pdf'
        ordinfo['pickup_meta'] = self.details_data.get('pickup_meta', {"pickup_request": False, "data": []})
        # Additional Fields to store the
        if self.details_data.get('secondary_order_id'):
            ordinfo['secondary_order_id'] = self.details_data.get('secondary_order_id')
        if "peipl" == self.details_data.get('slug'):
            ordinfo['ecz_order_id'] = self.details_data.get('ecz_order_id')
            ordinfo['secondary_order_id'] = self.details_data.get('ecz_order_id')
        ordinfo['gst_invoices'] = gst_invoices
        ordinfo['trip_id'] = request_data.get('trip_id')
        ordinfo['po_number'] = request_data.get('po_number')
        ordinfo['vendor_name'] = self.details_data.get('vendor_name', __slug)
        ordinfo['vendor_display_name'] = self.details_data.get('vendor_name', VENDOR_NAMES.get(__slug) or __slug)
        export_option = request_data.get('shipment', {}).get('export_option', {})
        invoice_date = export_option.get('invoice_date', "")

        payment_mode = {
            "mode_option": request_data.get('payment_mode', {}).get('mode_option', ''),
            "favour_name": request_data.get('payment_mode', {}).get('favour_name', '')
        }
        ordinfo["payment_mode"] = payment_mode

        if isinstance(invoice_date, dt.date):
            export_option['invoice_date'] = invoice_date.isoformat()
        ordinfo['export_option'] = export_option
        ordinfo['is_csb_v_mode'] = request_data.get('shipment', {}).get('is_csb_v_mode', False)
        ordinfo['is_qc_checked'] = request_data.get('shipment', {}).get('is_qc_checked', False)
        ordinfo['is_return_exchange'] = request_data.get('shipment', {}).get('is_return_exchange', False)
        ordinfo['exchange_shipment_id'] = request_data.get('shipment', {}).get('exchange_shipment_id')
        ordinfo['return_reason'] = request_data.get('shipment', {}).get('return_reason')

        ordinfo["is_etd_shipment"] = True if __slug in ['fedex', 'fedex_india'] and request_data.get('shipment', {}).get("etd_details") else False
        if request_data.get('shipment', {}).get("etd_details"):
            etd_details = {
                "status": "pending" if request_data.get('shipment', {}).get("etd_details", {}).get("etd_type") == "POST-SHIPMENT" else "completed",
                "cut_off_time": datetime.utcnow() + timedelta(hours=24) if request_data.get('shipment', {}).get("etd_details", {}).get("etd_type") == "POST-SHIPMENT" else '',
                "type": request_data.get('shipment', {}).get("etd_details", {}).get("etd_type"),
                "is_fedex_generated_docs": False if request_data.get('shipment', {}).get("etd_details", {}).get("allow_upload_docs") or request_data.get('shipment', {}).get("etd_details", {}).get("etd_type") == "POST-SHIPMENT" else True,
                "docs_types": [doc.get("doc_type") for doc in request_data.get('shipment', {}).get("etd_details", {}).get("docs_details")],
            }
            ordinfo["etd_details"] = etd_details

        if request_data.get('shipment', {}).get("is_appt_based_delivery"):

            appointment_delivery_details = {
                "appointment_id":request_data.get("shipment",{}).get("appointment_delivery_details",{}).get("appointment_id",'') or '',
                "appointment_date": datetime.combine(datetime.strptime(request_data.get("shipment", {}).get("appointment_delivery_details", {}).get("appointment_date", ''), "%Y/%m/%d").date(),datetime.min.time()) or '',
                "appointment_time": request_data.get("shipment",{}).get("appointment_delivery_details",{}).get("appointment_time",'') or '',
                "appointment_remarks": request_data.get("shipment",{}).get("appointment_delivery_details",{}).get("appointment_remarks",'') or ''
            }
            ordinfo["is_appointment_delivery"] = request_data.get('shipment', {}).get("is_appt_based_delivery")
            ordinfo["appointment_delivery_details"] = appointment_delivery_details

        ordinfo["sales_order_store_id"] = request_data.get("sales_order_store_id", "")
        ordinfo["special_instruction"] = request_data.get("special_instruction") or ""
        Conn().final_orders.insert_one(ordinfo)
        #
        # try:
        #     user_id = request_data.get('api_token')
        #     if user_id: # in ['6151a9c70afce07ef6bd9e25', '5f783d4d0afce06ef35745fe']:
        #         Conn().processing_requests.remove({'customer_referenc': customer_reference.upper(), 'user_id': user_id}) #request_data.get('api_token')
        #     # TODO: Make it generic, if it works fine
        # except:
        #     pass
        #
        return True

    def _get_pkg_count(self):
        """
        Return the package counts
        """
        return len(self.details_data.get('request_data').get('shipment').get('parcels'))

    def _get_entered_weight(self):
        return sum([m.get('weight', {}).get('value', 0.0) for m in self.details_data.get('request_data', {}).get('shipment', {}).get('parcels', [])])

    def _get_invoice_amount(self, gst_invoices=[]):
        """
        return the total amount for invoice 
        """
        _invoice_amount_list = []
        for invoice in gst_invoices:
            if invoice.get('invoice_value'):
                _invoice_amount_list.append(invoice.get('invoice_value'))

        if _invoice_amount_list:
            return sum(_invoice_amount_list)

        total_item_inv = sum([k.get('price', {}).get('amount', 0.0) * k.get('quantity', 1) for m in self.details_data.get('request_data', {}).get('shipment', {}).get('parcels', [{}]) for k in m.get('items') or [{}]])

        return total_item_inv

    def _get_invoice_currency(self):
        """
        return the currency type
        """
        for parcel in self.details_data.get('request_data', {}).get('shipment', {}).get("parcels"):
            if parcel.get("items", []):
                return parcel.get("items")[0].get("price", {}).get("currency")
        #
        # return (
        #     self.details_data.get('request_data', {}).get('shipment', {}).get('parcels', [{}])[0].get('items', [{}])[
        #         0].get('price', {}).get('currency'))

    def _get_weight_unit(self):
        return (self.details_data.get('request_data').get('shipment').get('parcels')[0].get('weight').get('unit'))

    def _get_parsed_address(self, request_from):
        address = {}
        if 'sender' == request_from:
            address = self.details_data.get('request_data', {}).get('shipment', {}).get('ship_from')
        if 'receiver' == request_from:
            address = self.details_data.get('request_data', {}).get('shipment', {}).get('ship_to')
        if 'return' == request_from:
            address = self.details_data.get('request_data', {}).get('shipment', {}).get('return_to')
        shipper_postal_code = address.get("postal_code")
        if not shipper_postal_code:
            address.update({
                "postal_code": "00000"
            })

        return address
