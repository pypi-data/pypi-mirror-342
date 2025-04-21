CARRIER_SLUG = 'blitz'
CARRIER_LOGO = 'https://www.blitznow.in/assets/images/logo/blitz.svg'
CARRIER_TC = 'https://www.blitznow.in/Terms+of+Service.pdf'  ##pdf

ENDPOINTS = {
    'staging': {
        'auth': 'https://xenc2tehd4.execute-api.us-east-2.amazonaws.com/v1/auth',
        'booking': 'https://nu7c3e0ewj.execute-api.us-east-2.amazonaws.com/v1/waybill/',
        'cancellation': 'https://oyvm2iv4xj.execute-api.us-east-2.amazonaws.com/v1/orin/api/cancel/',
        'serviceability': 'https://oyvm2iv4xj.execute-api.ap-south-1.amazonaws.com/v1/inventory/inventory/estimatedDateSrcPincode/',
    },
    'live': {
        'auth': 'https://oyvm2iv4xj.execute-api.ap-south-1.amazonaws.com/v1/auth',
        'booking': 'https://xv24xrhpxa.execute-api.ap-south-1.amazonaws.com/v1/waybill/',
        'cancellation': 'https://oyvm2iv4xj.execute-api.ap-south-1.amazonaws.com/v1/orin/api/cancel/',
        'serviceability': 'https://oyvm2iv4xj.execute-api.ap-south-1.amazonaws.com/v1/inventory/inventory/estimatedDateSrcPincode/',
    }
}
blitz_vendor_config = {
    'service_type': "air,surface",  # no service types as per carrier so adding default for  serviceability
    'account_type': 'live',
    'username': 'SPLsv9jJC2Zm',
    'password': 'B,PaFYnE58~Jd',
    'use_carrier_label': True
}
