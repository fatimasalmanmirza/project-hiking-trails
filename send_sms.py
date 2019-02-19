# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client
import os
 
# Your Account Sid and Auth Token from twilio.com/console
account_sid = os.environ["account_sid"]
auth_token = os.environ["auth_token"]
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Hi, here is our recommendation of Hike trails for your weekend",
                     from_='+13347317307',
                     to='+14159106112'
                 )

print(message.sid)


# POST https://api.twilio.com/2010-04-01/Accounts/{TestAccountSid}/Messages

# +13347317307

# Account Sid

# AC6ee6806642a619b8e5e11983cf52b26f

# Auth Token
# cc391ab8ef49943b9bcc61d0bb6431d2