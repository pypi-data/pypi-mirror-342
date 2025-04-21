CARRIER_SLUG = 'airwayscourier'
CARRIER_LOGO = 'https://airwayscourier.co.in/images/airways-logo.gif'            #gif format
CARRIER_TC = 'https://airwayscourier.co.in/about-airways-profile.aspx'

ENDPOINTS = {
    'live': {
        'auth': 'https://airwayscourier.co.in/api/v1/authenticate',
        'booking': 'https://airwayscourier.co.in/api/v1/booking',
        'cancellation': 'https://airwayscourier.co.in/api/v1/Cancelbooking?WaybillNo={tracking_number}',
        'serviceability': 'https://airwayscourier.co.in/api/v1/getPinDetails?PinNo={pincode}'
    },
    'staging': {
        'auth': 'https://airwayscourier.co.in/api/v1/authenticate',
        'booking': 'https://airwayscourier.co.in/api/v1/booking',
        'cancellation': 'https://airwayscourier.co.in/api/v1/Cancelbooking?WaybillNo={tracking_number}',
        'serviceability': 'https://airwayscourier.co.in/api/v1/getPinDetails?PinNo={pincode}'
    }
}

airwayscourier_vendor_config = {
    'username' : 'MD03',
    'password' : 'MD03@123',
    'account_type' : 'test',
    "risk_surcharge" : "CLIENT",                    #---> values {CLIENT, COMPANY, NONE}
    'service_type' : 'AIR, SURFACE, EXPRESS'
}