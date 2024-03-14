import os
import jinja2
import pdfkit
import logging
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
from client_emails import client_emails

load_dotenv()


try:
    bodyweight = int(input("Enter Bodyweight (lbs): "))
    total_calories = int(input("Enter Total Calories (kcal): "))
    total_protein = int(input("Enter Total Protein (g): "))
    fats_ratio = float(input("Enter Fats Ratio (0.3-0.4): "))
    mesocycle = input("Enter Mesocycle #: ")
    phase = input("Enter Phase(Fat Loss, Massing, Maintenance, Deload): ")
    client_name = input("Enter Client Name (firstname  lastname): ")

    #calculations from inputs
    total_fats = round(bodyweight * fats_ratio)
    total_carbs = round((total_calories - ((total_protein * 4) + (total_fats * 9)))/4)


    #Using total macros to split into 2 types of meals
    pre_and_post_wo_meals = {
        "protein" : round(total_protein/4),
        "fats" : round(total_fats*0.15),
        "carbs" : round(total_carbs*0.3)
    }

    two_regular_meals = {
        "protein": round(total_protein/4),
        "fats": round((total_fats - 2*(pre_and_post_wo_meals["fats"]))/2),
        "carbs": round((total_carbs - 2*(pre_and_post_wo_meals["carbs"]))/2)
    }

    #context is given to jinja 2 environment render
    context = {
        "bodyweight" : bodyweight,
        "total_calories" : total_calories,
        "total_protein" : total_protein,
        "fats_ratio" : fats_ratio,
        "mesocycle" : mesocycle,
        "phase" : phase,
        "total_fats" : total_fats,
        "total_carbs" : total_carbs,
        "pre_and_post_wo_meals" : pre_and_post_wo_meals,
        "two_regular_meals" : two_regular_meals,
        "client_name" : client_name
    }

    #html to pdf set-up
    template_loader = jinja2.FileSystemLoader("./")
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template("pdf.html")
    output_text = template.render(context)

    config = pdfkit.configuration(wkhtmltopdf="/usr/local/bin/wkhtmltopdf")

    #custom filenames and directory path
    output_filename = f"{client_name} Meso {mesocycle} {phase}.pdf"
    output_directory = f"/Users/nelsonlee/Documents/Fitness Business/Clients/{client_name}/Mesocycles/Meso {mesocycle}/"

    #if the path doesn't exist, we make a new directory
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    output_path = os.path.join(output_directory, output_filename)

    #making pdf and storing it in the output path
    pdfkit.from_string(output_text, output_path, configuration=config)

    print(f"{output_filename} was successfully created in {output_directory}")

    send_email_y_n = input("Send email with pdf? (y/n)")



    #start of email sending code
    if send_email_y_n == "y":

        #port number and server set-up
        smtp_port = 587
        smtp_server = "smtp.gmail.com"

        email_from = "nelsonleex@gmail.com"
        email_to = client_emails[client_name]

        pw = os.getenv("pw")

        subject = f"Mesocycle {mesocycle} Nutrition Sheet "
        
        #body of the email
        body = f"""
Attached below is your nutrition sheet for mesocycle {mesocycle}


Best,

Nelson Lee
        """

        #creating MIME object, defining parts of the email
        msg = MIMEMultipart()
        msg["From"] = f"Nelson Lee <{email_from}>"
        msg["To"] = email_to
        msg["Subject"] = subject

        #attaching the body of the message
        msg.attach(MIMEText(body, "plain"))

        #define the file to attach
        attachment_filename = output_path

        #open the file as binary (rb)
        attachment = open(attachment_filename, "rb")

        #encode as base 64
        attachment_package = MIMEBase('application', 'octet-stream')
        attachment_package.set_payload((attachment).read())
        encoders.encode_base64(attachment_package)
        attachment_package.add_header("Content-Disposition", "attachment; filename= " + attachment_filename)
        msg.attach(attachment_package)

        #set to string
        text = msg.as_string()

        
        try:
            #connecting to server
            print("Trying to connect to server")
            TIE_server = smtplib.SMTP(smtp_server, smtp_port)
            TIE_server.starttls()
            TIE_server.login(email_from, pw)
            print("Login successful, connected to server")

            #sending email
            print(f"Sending email to: {email_to}")
            TIE_server.sendmail(email_from, email_to, text)
            print(f"Email successfully sent to: {email_to}")
            print("email sent, ending script")
        except Exception  as e:
            print(str(e))
        finally:
            TIE_server.quit()
    else:
        print("no problem, ending script")

except Exception as e:
    logging.exception(e)






