# from urllib3 import request
# from urllib2 import Request, urlopen
#
# values = """
#   {
#     "command": "request",
#     "data": {
#       "api_key": "mysendykey",
#       "api_username": "mysendyusername",
#       "vendor_type": 1,
#       "rider_phone": "0728561783",
#       "from": {
#         "from_name": "Green House",
#         "from_lat": -1.300577,
#         "from_long": 36.78183,
#         "from_description": ""
#       },
#       "to": {
#         "to_name": "KICC",
#         "to_lat": -1.28869,
#         "to_long": 36.823363,
#         "to_description": ""
#       },
#       "recepient": {
#         "recepient_name": "Sender Name",
#         "recepient_phone": "0709779779",
#         "recepient_email": "sendyer@gmail.com",
#         "recepient_notes": "recepient specific Notes",
#         "recepient_notify": false
#       },
#       "sender": {
#         "sender_name": "Sendyer Name",
#         "sender_phone": "0709 779 779",
#         "sender_email": "sendyer@gmail.com",
#         "sender_notes": "Sender specific notes",
#         "sender_notify": false
#       },
#       "delivery_details": {
#         "pick_up_date": "2016-04-20 12:12:12",
#         "collect_payment": {
#           "status": false,
#           "pay_method": 0,
#           "amount": 10
#         },
#         "carrier_type": 2,
#         "return": false,
#         "note": " Sample note",
#         "note_status": true,
#         "request_type": "delivery",
#         "order_type": "ondemand_delivery",
#         "ecommerce_order": false,
#         "express": false,
#         "skew": 1,
#         "package_size": [
#           {
#             "weight": 20,
#             "height": 10,
#             "width": 200,
#             "length": 30,
#             "item_name": "laptop"
#           }
#         ]
#       }
#     },
#     "request_token_id": "request_token_id"
#   }
# """
#
# headers = {
#     'Content-Type': 'application/json'
# }
# request = Request('https://apitest.sendyit.com/v1/##request', data=values, headers=headers)
#
# response_body = urlopen(request).read()
# print(response_body)
