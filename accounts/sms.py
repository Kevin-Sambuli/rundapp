# import package
import africastalking

# Initialize SDK
# username = os.getenv('user_name', 'sandbox')
# api_key = os.getenv('api_key', 'fake')
username = "rundalis"  # use 'sandbox' for development in the test environment
api_key = "6ee159bd900a033c60ef05106c93446c2906458abfa43c83320ff6e563b62f42"  # use your sandbox app API key for development in the test environment
africastalking.initialize(username, api_key)

# Initialize a service e.g. SMS



africastalking.initialize(username, api_key)
sms = africastalking.SMS
airtime  = africastalking.Airtime
payment = africastalking.Payment


# Use the service synchronously
response = sms.send("Hello Message!", ["+254729759023"])
print(response)


# Or use it asynchronously
# def on_finish(error, response):
#     if error is not None:
#         raise error
#     print(response)


# sms.send("Hello Message!", ["+254729759023"], callback=on_finish)


class Subscription():
    def send_sms(self):
        response = sms.send("Hello Message!", ["+254729759023"])
        print(response)

    def send_airtime(self):
        phone_number = "+254729759023"
        currency_code = "KES"  # Change this to your country's code
        amount = 900
        try:
            response = airtime.send(phone_number=phone_number, amount=amount, currency_code=currency_code)
            print(response)
        except Exception as e:
            print(f"Encountered an error while sending airtime. More error details below\n {e}")



