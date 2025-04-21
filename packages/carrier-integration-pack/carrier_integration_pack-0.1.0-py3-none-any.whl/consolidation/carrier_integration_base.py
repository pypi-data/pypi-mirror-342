from abc import ABC, abstractmethod
from app.consolidation import aslist_cronly, render_shipping_label_html, pdf_merge_from_byte
from app.consolidation import cred_check_error_msg, cred_check_success_msg
import time
import json
import requests

class CarrierIntegration(ABC):

    CARRIER_LOGO = None
    CARRIER_SLUG = None
    CARRIER_TC = None
    

    def __init__(self, **kw):
        pass

    @staticmethod
    def piece_count_map(parcels=[]):
        """
        :param parcels:
        :return:
        """
        dims_map = {}
        for box in parcels:
            _dim = box.get('dimension', {})
            _wt = sum([i.get('weight').get('value') for i in box.get('items')])
            lbhw = '%s|%s|%s|%s' % (_dim.get('length'), _dim.get('width'), _dim.get('height'), _wt)
            _parcel_count = dims_map.get(lbhw) or 0
            dims_map[lbhw] = _parcel_count + 1

        return dims_map

    @abstractmethod
    def get_box_details(self, parcels):
        """

        :param parcels:
        :return:
        """
        # Length~Width~Heigh~PCS~Weight~bulk/Not bulk
        dimensions = []
        total_weight = []
        for parcel_dim, parcel_count in self.piece_count_map(parcels).items():
            _dim = parcel_dim.split('|')
            _l = _dim[0]
            _b = _dim[1]
            _h = _dim[2]
            _wt = _dim[3]

            dimensions.append({
                "no_of_boxes": parcel_count,
                "box_height": _h,
                "box_length": _l,
                "box_breadth": _b
            })
            total_weight.append(float(str(_wt)) or 0)

        return dimensions, float(str(sum(total_weight)))

    @abstractmethod
    def _custom_label(self, input_data):
        """
        On the lines of Delhivery Surface
        # TODO: Hell lot of duplicate code. Needs serious attention
        input
        {
            "barcodes":
            "order_id":
            "shipper_address":
            "reciever_address":
            "parcel":""
            "is_cod":
            "cod_amt"
            "awb"
            "service_name"
            "invoice_no"
        }
        """
        label_data = []
        _slug = self.CARRIER_SLUG
        # input_data = kw.get('input', {})
        # Looks like we are passing a list of AWBs here
        awb_list = aslist_cronly(input_data.get('awb'))
        docket_number = input_data.get('docket_number')
        total_weight = input_data.get('total_weight')
        source_code = input_data.get('source_code')
        source_location = input_data.get('source_location')
        destination_code = input_data.get('destination_code')
        destination_location = input_data.get('destination_location')
        qr_content = input_data.get('barcodes')

        # QR Code Format
        # <AWB no. with piece no.> | <Total pieces in AWB> | <Total weight of AWB> | <Source Hub> | <Source Service Center> | <Destination Hub> | <Destination Service Center>
        parcels = input_data.get('parcel') or []
        number_of_pkgs = len(parcels)

        raw_pdf = render_shipping_label_html(vendor_name=_slug.replace('_', " ").title(), vendor_service='', vendor_logo=self.CARRIER_LOGO, vendor_tos=self.CARRIER_TC, input_data=input_data, is_master_label=True, awb=docket_number, label_copy='Parent', barcode_format='code39', )
        label_data.append(raw_pdf)
        for awb in awb_list[1:]:
            raw_pdf = render_shipping_label_html(vendor_name=_slug.replace('_', " ").title(), vendor_service='', vendor_logo=self.CARRIER_LOGO, vendor_tos=self.CARRIER_TC, input_data=input_data, is_master_label=False, awb=awb, label_copy='Child', barcode_format='code39', )
            label_data.append(raw_pdf)

        order_id = input_data.get('order_id')
        link = pdf_merge_from_byte(label_data, str(order_id), str(input_data.get('docket_number') or ''))
        print('--------->', link)
        return link

    # @abstractmethod
    # def fetch_quotes(self, request_data, vendor_id, vendor_config, retry=0):
    #     pass

    # @abstractmethod
    # def create_pickup(self) :
    #     pass
    
    @abstractmethod
    def generate_label(self, retry=0):
        pass

    # @abstractmethod
    # def cancel_shipment(self):
    #     pass