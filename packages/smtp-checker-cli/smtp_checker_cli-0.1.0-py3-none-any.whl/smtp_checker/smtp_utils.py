import smtplib

def check_smtp_connection(host, port, security, username=None, password=None, from_email=None, to_email=None):
    try:
        if security == "ssl":
            server = smtplib.SMTP_SSL(host, port, timeout=10)
        else:
            server = smtplib.SMTP(host, port, timeout=10)
            server.ehlo()
            if security == "tls":
                server.starttls()
        
        server.ehlo()

        if username and password:
            server.login(username, password)

        if from_email and to_email:
            message = "Subject: SMTP Checker\n\nTest email from smtp-checker-cli."
            server.sendmail(from_email, to_email, message)

        server.quit()
        return "Success: SMTP connection and email sent!"
    except Exception as e:
        return f"Error: {str(e)}"
