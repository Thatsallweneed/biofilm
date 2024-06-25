import smtplib

email = "updatesofaccess@gmail.com"
receiver_email = "sherlocksk859@gmail.com"

subject = "INVITATION FOR party"
message = "hello sam lets have a party on wenesday"

text = f"Subject: {subject}\n\n{message}"

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(email, 'vatfbntjznrvgjli')  # Replace 'yourpassword' with your actual password
server.sendmail(email, receiver_email, text)
print(f"Email has been sent to - {receiver_email}")
