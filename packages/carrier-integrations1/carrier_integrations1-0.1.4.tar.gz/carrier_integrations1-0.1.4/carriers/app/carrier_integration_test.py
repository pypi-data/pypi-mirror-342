
import json

# from app.consolidation.franchexpress.franchexpress import FranchExpressIntegration
# from app.consolidation.india_post.india_post import IndiaPostIntegration
from app.consolidation.blitz.blitz import BlitzIntegration
# from app.consolidation.xpressbees_b2b_cargo.xpressbees_cargo import XpressbeesB2BCargoIntegration
#from app.consolidation.aramex_rest.aramex import AramexIntegration
#from app.consolidation.aramex_rest.aramex import fetch_token_map
#from app.consolidation.ekart_b2b.ekart_b2b import Ekart_B2B_Integration
from app.consolidation.airwayscourier.airwayscourier import AirwaysCourierIntegration

# from app.consolidation.FedEx.FedEx import FedExIntegration
# from app.consolidation.sampark.sampark import SamparkIntegration
# from app.consolidation.scorpion.scorpion import ScorpionIntegration

# from app.consolidation.pidge.pidge import PidgeIntegration

# from app.consolidation.ithinklogistics.ithinklogistics import ithinklogisticsIntegration
# from app.consolidation.ecomexpress_b2b.ecomexpress_b2b import ECOMExpressB2BIntegration

# from app.consolidation.xpressbees_wallet.xpressbees_wallet import XpressbeesWalletIntegration

AWB_REVERSE_REQUEST = json.loads('''

{
  "billing": {
    "paid_by": "shipper"
  },
  "vendor_id": "7983392038",
  "description": "Bluedart RVP Creds",
  "slug": "bluedart",
  "purpose": "commercial",
  "order_source": "manual",
  "parcel_contents": "test bookings",
  "is_document": false,
  "service_type": "eTailPrePaidAir",
  "charged_weight": {
    "unit": "KG",
    "value": 67
  },
  "customer_reference": "SYSTEST8798",
  "invoice_number": "123",
  "invoice_date": "15/02/2022",
  "is_cod": false,
  "collect_on_delivery": {
    "amount": 0,
    "currency": "INR"
  },
  "shipment": {
    "is_reverse": true,
    "is_qc_checked": true,
    "is_return_exchange": false,
    "return_reason": "Wrong Product Received",
    "ship_from": {
      "contact_name": "Test",
      "company_name": "Test Shipper",
      "street1": "Shipper Address one line 1",
      "street2": "Address line 2",
      "city": "Bangalore",
      "state": "KA",
      "postal_code": "400099",
      "phone": "9999999999",
      "email": "test@test.123",
      "tax_id": "29AAHCP6046M1ZT",
      "country": "IN",
      "type": "residential",
      "lat": "",
      "lng": "",
      "what3words": "",
      "id": ""
    },
    "ship_to": {
      "contact_name": "Test Receiver",
      "company_name": "Test Receiver company",
      "street1": "Reciver address 1",
      "street2": "Address 2",
      "city": "Mumbai",
      "state": "MH",
      "postal_code": "400011",
      "phone": "9999999999",
      "country": "IN",
      "type": "business",
      "lat": "",
      "lng": "",
      "what3words": "",
      "id": ""
    },
    "return_to": {
      "contact_name": "Test",
      "company_name": "Test Shipper",
      "street1": "Shipper Address one line 1",
      "street2": "Address line 2",
      "city": "Bangalore",
      "state": "KA",
      "postal_code": "560011",
      "phone": "9999999999",
      "email": "test@test.123",
      "tax_id": "29AAHCP6046M1ZT",
      "country": "IN",
      "type": "residential",
      "lat": "",
      "lng": "",
      "what3words": "",
      "id": ""
    },
    "is_to_pay": false,
    "parcels": [
      {
        "description": "PVC - QR code sticker_1000",
        "box_type": "custom",
        "quantity": 1,
        "weight": {
          "value": 4.6,
          "unit": "kg"
        },
        "dimension": {
          "width": 23,
          "height": 15,
          "length": 26,
          "unit": "cm"
        },
        "items": [
          {
            "reference": "item_id_1",
            "description": "PVC - QR code sticker_1000",
            "origin_country": "IN",
            "sku": "sku121",
            "hs_code": "",
            "variant": "",
            "quantity": 1,
            "price": {
              "amount": 10.9,
              "currency": "INR"
            },
            "weight": {
              "value": 4.6,
              "unit": "kg"
            },
            "item_qc_details": {
              "item_url": "https://www.bluedart.com/image/layout_set_logo?img_id=1414225&t=1727174533219",
              "item_quantity": 1,
              "item_size": "",
              "item_variant": "",
              "comments": "",
              "questions": [
                {
                  "question_id": "100",
                  "question_description": "Does the description match?",
                  "question_value": "Yes",
                  "expected_answer": "Y"
                },
                {
                  "question_id": "101",
                  "question_description": "Does the Product match the image shown?",
                  "question_value": "Yes",
                  "expected_answer": "Y"
                },
                {
                  "question_id": "102",
                  "question_description": "Does the Colour match?",
                  "question_value": "Yes",
                  "expected_answer": "Y"
                },
                {
                  "question_id": "103",
                  "question_description": "Does the Size Match?",
                  "question_value": "Yes",
                  "expected_answer": "Y"
                },
                {
                  "question_id": "104",
                  "question_description": "Does the Brand Match?",
                  "question_value": "Yes",
                  "expected_answer": "Y"
                },
                {
                  "question_id": "105",
                  "question_description": "Does the SKU Code Match?",
                  "question_value": "Yes",
                  "expected_answer": "Y"
                }
              ]
            }
          }
        ]
      }
    ]
  },
  "gst_invoices": [
    {
      "invoice_number": "100001",
      "invoice_date": "2021-08-10T18:30:00.000Z",
      "invoice_value": 500,
      "ewaybill_number": "123456789012",
      "ewaybill_date": ""
    }
  ]
}
                                 ''')

AWB_INPUT_REQUEST = json.loads('''
{
  "billing": {
    "paid_by": "shipper"
  },
  "vendor_id": "2642784902",
  "description": "DHL international",
  "slug": "dhl_india",
  "purpose": "commercial",
  "order_source": "shopify",
  "parcel_contents": "Crayons",
  "is_document": false,
  "service_type": "Road Cargo",
  "rate": {
    "amount": "919.960",
    "currency": "INR"
  },
  "charged_weight": {
    "unit": "KG",
    "value": 0.25
  },
  "customer_reference": "test_clonez123123123912312",
  "invoice_number": "1234543",
  "invoice_date": "28/01/2021",
  "is_cod": false,
  "collect_on_delivery": {
    "amount": 10,
    "currency": "USD"
  },
  "shipment": {
    "docket_number" : "113192478",
    "is_csb_v_mode": true,
    "eWaybillNumber": "",
    "ship_from": {
      "contact_name": "shipper contact_name ",
      "company_name": "shipper company name",
      "street1": "shipper street1 ",
      "city": "Bangalore",
      "state": "Karnataka",
      "postal_code": "201317",
      "country": "IN",
      "type": "residential",
      "phone": "7338466335",
      "street2": "shipper street2",
      "tax_id": "27AAACB0446L2ZR",
      "street3": "shipper street3",
      "fax": "",
      "email": "shipper@gmail.com",
      "alias_name": "Banglore_3",
      "is_primary": true,
      "id": "CR022350"
    },
    "ship_to": {
      "city": "Delhi",
      "company_name": "consignee company",
      "contact_name": "consignee contact name",
      "country": "IN", 
      "email": "consignee@gmail.com",
      "fax": "",
      "phone": "7338466335",
      "postal_code": "560015",
      "state": "Delhi",
      "street1": "consignee street1",
      "street2": "consignee street2",
      "street3": "consignee street3",
      "tax_id": "consTAX",
      "type": "residential",
      "id": "CN000081"
    },
    "return_to": {
      "contact_name": "return contact name",
      "company_name": "return comapany name",
      "street1": "return to street1",
      "city": "Banglore",
      "state": "Karnataka",
      "postal_code": "560015",
      "country": "IN",
      "type": "residential",
      "phone": "8888888888",
      "street2": "return to street2",
      "tax_id": "RETURNTOTAX",
      "street3": "return to street3",
      "fax": "",
      "email": "returnmail.com",
      "alias_name": "Banglore_3",
      "is_primary": true
    },
    "is_reverse": true,
    "is_qc_checked": true,
    "is_to_pay": false,                
    "parcels": [
      {
        "awb" : "test_clonez123123123912312126627",
        "description": "MEDIUM BOX",
        "box_type": "custom",
        "weight": {
          "value": 0.25,
          "unit": "kg"
        },
        "dimension": {
          "width": 10,
          "height": 10,
          "length": 10,
          "unit": "cm"
        },
        "items": [
          {
            "piece_no": 1,
            "description": "Crayons",
            "origin_country": "IN",
            "commodity_type": "Others",
            "is_meis": false,
            "hs_code": "12345678",
            "invoice_rate_per_item": 200,
            "fob_value": "200",
            "total_amount": 200,
            "sku": "125gh6y-48nj45frf-748hfn-7rhfj-48fh",
            "quantity": 1,
            "ship_piece_cess": "",
            "ship_piece_taxable_value": "200",
            "ship_piece_igst": "30",
            "ship_piece_igst_percentage" : "18",
            "item_qc_details": {
              "item_url": "https://www.bluedart.com/image/layout_set_logo?img_id=1414225&t=1727174533219",
              "item_quantity": 1,
              "item_size": "",
              "item_variant": "",
              "comments": "",
              "questions": [
                {
                  "question_id": "100",
                  "question_description": "Does the description match?",
                  "question_value": "Yes",
                  "expected_answer": "Y"
                },
                {
                  "question_id": "101",
                  "question_description": "Does the Product match the image shown?",
                  "question_value": "Yes",
                  "expected_answer": "Y"
                },
                {
                  "question_id": "102",
                  "question_description": "Does the Colour match?",
                  "question_value": "Yes",
                  "expected_answer": "Y"
                },
                {
                  "question_id": "103",
                  "question_description": "Does the Size Match?",
                  "question_value": "Yes",
                  "expected_answer": "Y"
                },
                {
                  "question_id": "104",
                  "question_description": "Does the Brand Match?",
                  "question_value": "Yes",
                  "expected_answer": "Y"
                },
                {
                  "question_id": "105",
                  "question_description": "Does the SKU Code Match?",
                  "question_value": "Yes",
                  "expected_answer": "Y"
                }
              ]
            },
            "price": {
              "amount": 200,
              "currency": "INR"
            },
            "weight": {
              "value": 0.125,
              "unit": "kg"
            }
          }       
        ],
        
        "quantity": 2
      }
    ],                                     
    "is_appt_based_delivery":false,
    "appointment_delivery_details":{"appointment_date":"2024/03/08","appointment_time":"16:55","appointment_remarks":""},
    "export_option": {
      "terms_of_sale": "FOB",
      "ad_code": "12345678901234",
      "gst_amount": "100",
      "invoice_date": "28/01/2021",
      "is_gst_invoice": true,
      "is_bond": true,
      "iec_number": "qwertyuiop",
      "is_ecom_seller": true,
      "is_meis": false
    }
  },

  "gst_invoices": [
    {
      "invoice_number": "100001",
      "invoice_date": "2021-08-10T18:30:00.000Z",
      "invoice_value": 200,
      "ewaybill_number": "123456789012",
      "ewaybill_date": ""
    },
    {
      "invoice_number": "100002",
      "invoice_date": "2021-08-10T18:30:00.000Z",
      "invoice_value": 200,
      "ewaybill_number": "123456789013",
      "ewaybill_date": ""
    },
                               {
      "invoice_number": "100003",
      "invoice_date": "2021-08-10T18:30:00.000Z",
      "invoice_value": 200,
      "ewaybill_number": "123456789012",
      "ewaybill_date": ""
    },
    {
      "invoice_number": "100004",
      "invoice_date": "2021-08-10T18:30:00.000Z",
      "invoice_value": 200,
      "ewaybill_number": "123456789013",
      "ewaybill_date": ""
    },
                               {
      "invoice_number": "100005",
      "invoice_date": "2021-08-10T18:30:00.000Z",
      "invoice_value": 200,
      "ewaybill_number": "123456789013",
      "ewaybill_date": ""
    }
   
  ]
}
''')

AC_AWB_INPUT_REQUEST = json.loads('''
{
  "billing": {
    "paid_by": "shipper"
  },
  "vendor_id": "3803500874",
  "user_id" : "5cebc9d47a621400091ab864",                                  
  "description": "DHL international",
  "slug": "fedex",
  "purpose": "commercial",
  "order_source": "shopify",
  "parcel_contents": "Crayons",
  "is_document": false,
  "service_type": "FEDEX_INTERNATIONAL_PRIORITY_EXPRESS",
  "rate": {
    "amount": "919.960",
    "currency": "INR"
  },
  "charged_weight": {
    "unit": "KG",
    "value": 0.25
  },
  "customer_reference": "TEST1324_clone1222",
  "invoice_number": "1234543",
  "invoice_date": "28/01/2021",
  "is_cod": false,
  "collect_on_delivery": {
    "amount": 20,
    "currency": "USD"
  },
  "shipment": {
    "docket_number" : "EZ100011319IN",
    "is_csb_v_mode": true,
    "eWaybillNumber": "",
    "ship_from": {
      "contact_name": "Customer Care",
      "company_name": "Warehouse Exam",
      "street1": "Pickup Warehouse 1 ",
      "city": "Mumbai",
      "state": "MH",
      "postal_code": "400001",
      "country": "IN",
      "type": "residential",
      "phone": "8888888888",
      "street2": "",
      "tax_id": "ABCDEFGHJ",
      "street3": "",
      "fax": "",
      "email": "demo@gmail.com",
      "alias_name": "Banglore_3",
      "is_primary": true,
      "id": "CR022350"
    },
    "ship_to": {
      "city": "Bangalore",
      "company_name": "name of the company",
      "contact_name": "ram",
      "country": "US", 
      "email": "t0054502@gmail.com",
      "fax": "",
      "phone": "6666666666",
      "postal_code": "38017",
      "state": "TN",
      "street1": "test booking do not ship the 1",
      "street2": "",
      "street3": "",
      "tax_id": "12asdfr1234f4g5",
      "type": "residential",
      "id": "CN000081"
    },
    "return_to": {
      "contact_name": "Customer Care",
      "company_name": "Warehouse Exam",
      "street1": "# 73  nilay address line 1",
      "city": "Banglore",
      "state": "Karnataka",
      "postal_code": "110001",
      "country": "IN",
      "type": "residential",
      "phone": "8888888888",
      "street2": "sampige road not",
      "tax_id": "ABCDEFGHJ",
      "street3": "landmark : behind fire station bat3",
      "fax": "",
      "email": "demo@gmail.com",
      "alias_name": "Banglore_3",
      "is_primary": true
    },
    "is_reverse": true,
    "is_to_pay": false,
    "parcels": [
      {
        "description": "MEDIUM BOX",
        "box_type": "custom",
        "weight": {
          "value": 2,
          "unit": "kg"
        },
        "dimension": {
          "width": 10,
          "height": 10,
          "length": 10,
          "unit": "cm"
        },
        "items": [
          {
            "piece_no": 1,
            "description": "Crayons",
            "origin_country": "IN",
            "commodity_type": "Others",
            "is_meis": false,
            "hs_code": "12345678",
            "invoice_rate_per_item": 200,
            "fob_value": "200",
            "total_amount": 200,
            "sku": "125gh6y-48nj45frf-748hfn-7rhfj-48fh",
            "quantity": 1,
            "ship_piece_cess": "",
            "ship_piece_taxable_value": "200",
            "ship_piece_igst": "30",
            "ship_piece_igst_percentage" : "18",
            "price": {
              "amount": 200,
              "currency": "USD"
            },
            "weight": {
              "value": 1,
              "unit": "kg"
            }
          }  ,
           {
            "piece_no": 1,
            "description": "Crayons",
            "origin_country": "IN",
            "commodity_type": "Others",
            "is_meis": false,
            "hs_code": "12345678",
            "invoice_rate_per_item": 200,
            "fob_value": "200",
            "total_amount": 200,
            "sku": "125gh6y-48nj45frf-748hfn-7rhfj-48fh",
            "quantity": 1,
            "ship_piece_cess": "",
            "ship_piece_taxable_value": "200",
            "ship_piece_igst": "30",
            "ship_piece_igst_percentage" : "18",
            "price": {
              "amount": 200,
              "currency": "USD"
            },
            "weight": {
              "value": 0.125,
              "unit": "kg"
            }
          }             
        ],
        "awb": "",
        "quantity": 2
      }
    ],
    "export_option": {
      "terms_of_sale": "FOB",
      "ad_code": "12345678901234",
      "gst_amount": "100",
      "invoice_date": "28/01/2021",
      "is_gst_invoice": true,
      "is_bond": true,
      "iec_number": "qwertyuiop",
      "is_ecom_seller": true,
      "is_meis": false
    }
  },
  "gst_invoices": [
    {
      "invoice_number": "100001",
      "invoice_date": "2021-08-10T18:30:00.000Z",
      "invoice_value": 500,
      "ewaybill_number": "123456789012",
      "ewaybill_date": ""
    },
    {
      "invoice_number": "100002",
      "invoice_date": "2021-08-10T18:30:00.000Z",
      "invoice_value": 500,
      "ewaybill_number": "123456789013",
      "ewaybill_date": ""
    }
  ]
}
''')

Blitz_AWB_INPUT_REQUEST = json.loads('''
{
  "billing": {
    "paid_by": "shipper"
  },
  "vendor_id": "9212052189",
  "description": "BlueDart",
  "slug": "bluedart",
  "purpose": "commercial",
  "order_source": "api",
  "parcel_contents": "test bookings",
  "is_document": false,
  "service_type": "eTailPrePaidAir",
  "charged_weight": {
    "unit": "KG",
    "value": 67
  },
  "rate": {
    "amount": "919.960",
    "currency": "INR"
  },
                                     
  "customer_reference": "skjcnuuirtclso",
  "invoice_number": "123",
  "invoice_date": "15/02/2022",
  "is_cod": true,
  "collect_on_delivery": {
    "amount": 150,
    "currency": "INR"
  },
  "shipment": {
    "ship_from": {
      "contact_name": "Test1234er",
      "company_name": "Test Shipper",
      "street1": "Shipper Address one line 1",
      "street2": "Address line 2",
      "city": "Bangalore",
      "state": "KA",
      "postal_code": "122001",
      "phone": "9999999999",
      "email": "test@test.123",
      "tax_id": "29AAHCP6046M1ZT",
      "country": "IN",
      "type": "residential"
    },
    "ship_to": {
      "contact_name": "Test Receiver",
      "company_name": "Test Receiver company",
      "street1": "Reciver address 1",
      "street2": "Address 2",
      "city": "Mumbai",
      "state": "MH",
      "postal_code": "122001",
      "phone": "9999999999",
      "country": "IN",
      "type": "business"
    },
    "return_to": {
      "contact_name": "Test",
      "company_name": "Test Shipper",
      "street1": "Shipper Address one line 1",
      "street2": "Address line 2",
      "city": "Bangalore",
      "state": "KA",
      "postal_code": "560011",
      "phone": "9999999999",
      "email": "test@test.123",
      "tax_id": "29AAHCP6046M1ZT",
      "country": "IN",
      "type": "residential"
    },
    "is_reverse": false,
    "is_to_pay": false,
    "parcels": [
    {
        "description": "PVC - QR code sticker_1000",
        "box_type": "custom",
         "quantity": 1,
        "weight": {
          "value": 4.6,
          "unit": "kg"
        },
        "dimension": {
          "width": 23,
          "height": 15,
          "length": 26,
          "unit": "cm"
        },
        "items": [
          {
            "description": "PVC - QR code sticker_1000",
            "origin_country": "IN",
           
             "sku": "",
            "hs_code": "",
            "variant": "",
           
            "quantity": 1,
           
            "price": {
              "amount": 10.9,
              "currency": "INR"
            },
            "weight": {
              "value": 4.6,
              "unit": "kg"
            }
          }
        ]
      }
    ]
  },
  "gst_invoices": [
    {
      "invoice_number": "100001",
      "invoice_date": "2021-08-10T18:30:00.000Z",
      "invoice_value": 500,
      "ewaybill_number": null,
      "ewaybill_date": ""
    }
  ]
}
                                     ''')

AWB_INPUT_REQUEST_CARGO = json.loads('''
{
    "billing": {
        "paid_by": "shipper"
    },
    "vendor_id": "V0010",
    "description": "EXC1381",
    "slug": "bluedart",
    "purpose": "commercial",
    "order_source": "api",
    "parcel_contents": "DEAD ALRIGHT Unisex Cargo - 32",
    "is_document": false,
    "service_type": "Air",
    "mode": "Road",
    "payment_mode" : {
                    "mode_option" : ""
                       },
    "rate": {
        "amount": 0,
        "currency": "INR"
    },
    "charged_weight": {
        "unit": "KG",
        "value": 0.4
    },
    "customer_reference": "pa5599999959059EEEE8165a411ee",
    "invoice_number": "",
    "invoice_date": "2024-12-24",
    "is_cod": false,
    "collect_on_delivery": {
        "amount": 0,
        "currency": "INR"
    },
    "shipment": {
        "docket_number" : "716719827788976648",
        "ship_from": {
            "contact_name": "July",
            "company_name": "ocean co. pvt ltd",
            "street1": "#67 dummy address line test order 1",
            "city": "Ahmedabad",
            "state": "Gujarat",
            "postal_code": "421111",
            "country": "IN",
            "type": "residential",
            "phone": "7338466335",
            "street2": "donot ship the shipment one two t 2",
            "tax_id": "",
            "street3": "",
            "fax": "",
            "email": "ocean@no.com",
            "alias_name": "Banglore_2",
            "is_primary": true
        },
        "ship_to": {
            "contact_name": "charger",
            "company_name": "cement ",
            "street1": "HMT park sampige road siddaramnagar",
            "city": "Ahmedabad",
            "state": "Gujarat",
            "postal_code": "360009",
            "country": "IN",
            "type": "residential",
            "phone": "7338466321",
            "street2": "test booking not for shipping",
            "tax_id": "",
            "street3": "",
            "fax": "",
            "email": "paper@gmail.com",
            "id": "Mysore_2",
            "is_primary": true
        },
        "return_to": {
            "contact_name": "July",
            "company_name": "ocean co. pvt ltd",
            "street1": "#67 dummy address line test order 1",
            "city": "Pune",
            "state": "Maharashtra",
            "postal_code": "421111",
            "country": "IN",
            "type": "residential",
            "phone": "7338466335",
            "street2": "donot ship the shipment one two t 2",
            "tax_id": "",
            "street3": "",
            "fax": "",
            "email": "ocean@no.com",
            "id": "Banglore_2",
            "is_primary": true
        },
        "is_reverse": true,
        "is_qc_checked": true,
        "return_reason": "Damaged",
        "is_to_pay": false,
        "parcels": [
            {
                "reference": "pa5599999959720rcel_20212",
                "description": "BOX",
                "box_type": "custom",
                "weight": {"value": 1, "unit": "kg"},
                "dimension": {"width": 2, "height": 1, "length": 2, "unit": "cm"},
                "quantity": 1,
                "items": [
          {
            "description": "parcel521",
            "origin_country": "IN",
           
             "sku": "",
            "hs_code": "",
            "variant": "",
           
            "quantity": 1,
           
            "price": {
              "amount": 10.9,
              "currency": "INR"
            },
            "weight": {
              "value": 4.6,
              "unit": "kg"
            }
          }
        ]
            },
            {
                "reference": "pa5599999959720rcel_20213",
                "description": "BOX",
                "box_type": "custom",
                "weight": {"value": 1, "unit": "kg"},
                "dimension": {"width": 6, "height": 4, "length": 4, "unit": "cm"},
                "quantity": 1,
                "items": [
          {
            "description": "parcel_21_23",
            "origin_country": "IN",
           
             "sku": "",
            "hs_code": "",
            "variant": "",
           
            "quantity": 1,
           
            "price": {
              "amount": 10.9,
              "currency": "INR"
            },
            "weight": {
              "value": 4.6,
              "unit": "kg"
            }
          }
        ]
            },
            {
                "reference": "pa5599999959720rcel_202114",
                "description": "BOX",
                "box_type": "custom",
                "weight": {"value": 1, "unit": "kg"},
                "dimension": {"width": 1, "height": 3, "length": 1, "unit": "cm"},
                "quantity": 1,
                                     "items": [
          {
            "description": "p131",
            "origin_country": "IN",
           
             "sku": "",
            "hs_code": "",
            "variant": "",
           
            "quantity": 1,
           
            "price": {
              "amount": 10.9,
              "currency": "INR"
            },
            "weight": {
              "value": 4.6,
              "unit": "kg"
            }
          }
        ]
            },
            {
                "reference": "pa5599999959720rcel_20215",
                "description": "BOX",
                "box_type": "custom",
                "weight": {"value": 1, "unit": "kg"},
                "dimension": {"width": 1, "height": 4, "length": 4, "unit": "cm"},
                "quantity": 1,
                                     "items": [
          {
            "description": "P141",
            "origin_country": "IN",
           
             "sku": "",
            "hs_code": "",
            "variant": "",
           
            "quantity": 1,
           
            "price": {
              "amount": 10.9,
              "currency": "INR"
            },
            "weight": {
              "value": 4.6,
              "unit": "kg"
            }
          }
        ]
            },
            {
                "reference": "pa5599999959720rcel_20216",
                "description": "BOX",
                "box_type": "custom",
                "weight": {"value": 1, "unit": "kg"},
                "dimension": {"width": 6, "height": 4, "length": 4, "unit": "cm"},
                "quantity": 1
            },
            {
                "reference": "pa5599999959720rcel_20217",
                "description": "BOX",
                "box_type": "custom",
                "weight": {"value": 1, "unit": "kg"},
                "dimension": {"width": 6, "height": 4, "length": 4, "unit": "cm"},
                "quantity": 1
            },
            {
                "reference": "pa5599999959720rcel_20218",
                "description": "BOX",
                "box_type": "custom",
                "weight": {"value": 1, "unit": "kg"},
                "dimension": {"width": 6, "height": 4, "length": 4, "unit": "cm"},
                "quantity": 1
            },
            {
                "reference": "pa5599999959720rcel_20219",
                "description": "BOX",
                "box_type": "custom",
                "weight": {"value": 1, "unit": "kg"},
                "dimension": {"width": 6, "height": 4, "length": 4, "unit": "cm"},
                "quantity": 1
            },
            {
                "reference": "pa5599999959720rcel_202199",
                "description": "BOX",
                "box_type": "custom",
                "weight": {"value": 1, "unit": "kg"},
                "dimension": {"width": 6, "height": 4, "length": 4, "unit": "cm"},
                "quantity": 1
            },
            {
                "reference": "pa5599999959720rcel_202198",
                "description": "BOX",
                "box_type": "custom",
                "weight": {"value": 1, "unit": "kg"},
                "dimension": {"width": 6, "height": 4, "length": 4, "unit": "cm"},
                "quantity": 1
            },
            {
                "reference": "pa5599999959720rcel_202177",
                "description": "BOX",
                "box_type": "custom",
                "weight": {"value": 1, "unit": "kg"},
                "dimension": {"width": 6, "height": 4, "length": 4, "unit": "cm"},
                "quantity": 1
            },
            {
                "reference": "pa5599999959720rcel_202155",
                "description": "BOX",
                "box_type": "custom",
                "weight": {"value": 1, "unit": "kg"},
                "dimension": {"width": 6, "height": 4, "length": 4, "unit": "cm"},
                "quantity": 1,
                                     "items": [
          {
            "description": "PVC - QR code sticker_1000",
            "origin_country": "IN",
           
             "sku": "",
            "hs_code": "",
            "variant": "",
           
            "quantity": 1,
           
            "price": {
              "amount": 10.9,
              "currency": "INR"
            },
            "weight": {
              "value": 4.6,
              "unit": "kg"
            }
          }
        ]
            }
        ]
    },
    "gst_invoices": [
        {
            "invoice_number": "100001",
            "invoice_date": "2021-08-10T18:30:00.000Z",
            "invoice_value": 500,
            "ewaybill_number": "123456789012",
            "ewaybill_date": ""
        },
         {
            "invoice_number": "100002",
            "invoice_date": "2021-08-10T18:30:00.000Z",
            "invoice_value": 500,
            "ewaybill_number": "123456789012",
            "ewaybill_date": ""
        }
    ]
}
''')

AWB_INPUT_REQUEST_TEST = json.loads('''
{
  "billing": {
    "paid_by": "shipper"
  },
  "vendor_id": "1587778508",
  "description": "BUSYBEES LOGISTICS SOLUTIONS PVT LT",
  "slug": "xpressbees_b2b_cargo",
  "return_carrier_response": true,
  "purpose": "commercial",
  "order_source": "api",
  "parcel_contents": ",Aavante Bar 3200D Pro Premium Black ",
  "is_document": false,
  "service_type": "Surface",
  "charged_weight": {
    "unit": "",
    "value": 0
  },
  "customer_reference": "6100004750",
  "invoice_number": "",
  "invoice_date": "",
  "is_cod": false,
  "collect_on_delivery": {
    "amount": 0,
    "currency": ""
  },
  "shipment": {
  
    "ship_from": {
      "contact_name": "Imagine Marketing Ltd- B2B FC",
      "company_name": "Imagine Marketing Ltd- B2B FC",
      "street1": ".",
      "street2": "",
      "city": "THANE",
      "state": "Maharashtra",
      "postal_code": "421101",
      "phone": "9860409903",
      "email": "akshaypatil@imaginemarketingindia.com",
      "tax_id": "27AADCI3821M1ZF",
      "country": "IN",
      "type": "business"
    },
    "ship_to": {
      "contact_name": "Imagine Marketing Ltd. - B2B Tajnag",
      "company_name": "Imagine Marketing Ltd. - B2B Tajnag",
      "street1": ".",
      "street2": "",
      "city": "GURUGRAM",
      "state": "Haryana",
      "postal_code": "122506",
      "phone": "8287514077",
      "email": "hanish.singh@imaginemarketingindia.com",
      "tax_id": "06AADCI3821M1ZJ",
      "country": "IN",
      "type": "business"
    },
    "return_to": {
      "contact_name": "Imagine Marketing Ltd- B2B FC",
      "company_name": "Imagine Marketing Ltd- B2B FC",
      "street1": ".",
      "street2": "",
      "city": "THANE",
      "state": "Maharashtra",
      "postal_code": "421101",
      "phone": "9860409903",
      "email": "akshaypatil@imaginemarketingindia.com",
      "tax_id": "27AADCI3821M1ZF",
      "country": "IN",
      "type": "business"
    },
    "is_reverse": false,
    "is_to_pay": false,
    "parcels": [
      {
        "description": "Aavante Bar 3200D Pro Premium Black ",
        "box_type": "custom",
        "quantity": 300,
        "weight": {
          "value": 7.78,
          "unit": "KG"
        },
        "dimension": {
          "width": 45,
          "height": 25,
          "length": 95,
          "unit": "CM"
        },
        "items": [
          {
            "description": "Aavante Bar 3200D Pro Premium Black ",
            "origin_country": "IN",
            "sku": "",
            "hs_code": "",
            "variant": "",
            "quantity": 300,
            "price": {
              "amount": 291.72,
              "currency": "INR"
            },
            "weight": {
              "value": 7.78,
              "unit": "KG"
            }
          }
        ]
      }
    ]
  },
  "gst_invoices": [
    {
      "invoice_number": "9272604411",
      "invoice_date": "09/04/2025",
      "invoice_value": 2917176,
      "ewaybill_number": "271010273256",
      "ewaybill_date": "2025-04-09 14:48:00"
    }
  ]
}
                                    '''                        
                                    )


SERVICE_INPUT_REQUEST = {}
Cancel_order = {
	"order_id" :["EZ128421398"],
    "api_token" : "5cebc9d47a621400091ab864"
}

pickup_order = {"vendor_id": "5828567225", "pick_datetime": "", "order_id": ["EZ37767"], "slug": "bluedart"}

if __name__ == '__main__':
   
    
    sfx = BlitzIntegration(input=Blitz_AWB_INPUT_REQUEST)
    print(sfx.generate_label())

    # sfx = AirwaysCourierIntegration(input=AWB_INPUT_REQUEST)
    # print(sfx.generate_label())

    # sfx = BlitzIntegration(input=Cancel_order)
    # print(sfx.cancel_shipment())

  #   flash_config ={
  #   'description' :'',
  #   'token' : 'd7bec8f736ef52e64bc2c63b45f13749f93d6aa2',
  #   'service_type' : 'surface',
  #   'account_type' : 'test'
  # }
  #   vendor_id =34
  #   sfx = BlitzIntegration(input=Blitz_AWB_INPUT_REQUEST)
  #   print(sfx.fetch_quotes(Blitz_AWB_INPUT_REQUEST, vendor_id, flash_config))

