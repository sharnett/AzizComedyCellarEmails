def send_me_email(date):
    import smtplib, string

    SUBJECT = "Aziz in the house!"
    TO = "srharnett@gmail.com"
    FROM = "srharnett@gmail.com"
    text = "He's comin to town! Be there be there be there! Clear you schedule on %s" % date
    BODY = string.join((
        "From: %s" % FROM,
        "To: %s" % TO,
        "Subject: %s" % SUBJECT ,
        "",
        text
        ), "\r\n")
    server = smtplib.SMTP("localhost")
    server.sendmail(FROM, [TO], BODY)
    server.quit()
