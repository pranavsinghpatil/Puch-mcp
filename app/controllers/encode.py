import base64

phone = input("Enter your phone number: ")  # 10-15 digits, with country code
token = base64.b64encode(phone.encode()).decode()
print(token)  # 'OTE5ODc2NTQzMjEw'