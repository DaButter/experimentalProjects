import requests

# Set up the email message
sender = "sender@guerrillamail.com"
recipient = "floby132@gmail.com"
subject = "Test email"
body = "This is a test email sent from Guerilla Mail."
message = {
    "from": sender,
    "to": recipient,
    "subject": subject,
    "text": body
}

# Send the email using the Guerilla Mail API
api_key = "YOUR_API_KEY"
api_url = f"https://api.guerrillamail.com/ajax.php?f=mail.set_email_user&email_user={api_key}"
response = requests.post(api_url, data=message)

# Check the response status code
if response.status_code == 200:
    print("Email sent successfully!")
else:
    print("Failed to send email:", response.text)
