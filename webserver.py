from flask import Flask, render_template, url_for, request, redirect
import smtplib
from email.message import EmailMessage

app = Flask(__name__)


@app.route('/')
def index():
    print(url_for('static', filename='faviconblack.ico'))
    return render_template("index.html")


@app.route('/thankyou.html')
def thankyou():
    print(url_for('static', filename='faviconblack.ico'))
    return render_template("thankyou.html")


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        data = request.form.to_dict()

        clientname = data['name']
        clientemail = data['email']
        clientmessage = data['message']

        formtoclienthtml = f"""
                                <!DOCTYPE html>
                                <html>
                                  <head>
                                    <base target="_top">
                                  </head>
                                  <body style="background-color: ghostwhite;">
                                    <h1 style="background-color:lightgray; color:darkolivegreen;">Thank you for contacting!</h1>
                                        <h3>Dear {clientname},</h3>
                                        <text>
                                            Thank you for your interest!
                                            <br> 
                                            <br> Your message was received and I'll do my best to get in touch, shortly!
                                            <br>
                                            <br> Best regards,
                                            <br> <b>Bardócz Zoltán</b>
                                            <br> CEO Arhimachete Srl
                                            <br> Tel, Whatsapp: +40756539555
                                            <br> www.arhimachete.com
                                        </text>
                                  </body>
                                </html>
                            """

        email = EmailMessage()
        email['from'] = "Arhimachete Office"
        email['to'] = clientemail
        email['subject'] = '🙏 Thank you!'

        email.set_content("Thank you for contacting me")
        email.add_alternative(formtoclienthtml, subtype='html')

        with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login('office@arhimachete.com', 'hogdwxxcgmfnodsm')
            smtp.send_message(email)
            print('all good boss, email confirmation sent to client!')
            smtp.quit()

            formtoofficehtml = f"""
                                    <!DOCTYPE html>
                                        <html>
                                            <head>
                                                <base target="_top">
                                            </head>
                                            <body style="background-color: ghostwhite;">
                                            <h1 style="background-color:lightgray; color:darkolivegreen;">{clientname} submitted your form!</h1>
                                                <h3>{clientemail}</h3>
                                                <text>
                                                    <br> {clientmessage}
                                                    <br>
                                                    <br> OFFICE
                                                    <br>
                                                </text>
                                            </body>
                                        </html>
                                """

        email = EmailMessage()
        email['from'] = "Arhimachete Office"
        email['to'] = 'office@arhimachete.com'
        email['subject'] = '💥 Alert! Contact Form Submitted 💥'

        email.set_content('Alert! Contact form submitted!')
        email.add_alternative(formtoofficehtml, subtype='html')

        with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login('office@arhimachete.com', 'hogdwxxcgmfnodsm')
            smtp.send_message(email)
            print('all good boss, email confirmation sent to office!')
            smtp.quit()

        data.clear()

        return redirect("thankyou.html")
    else:
        return 'something went wrong, try again!'
