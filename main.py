import os
import jinja2
import pdfkit
import logging


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


    template_loader = jinja2.FileSystemLoader("./")
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template("pdf.html")
    output_text = template.render(context)

    config = pdfkit.configuration(wkhtmltopdf="/usr/local/bin/wkhtmltopdf")


    output_filename = f"{client_name} Meso {mesocycle} {phase}.pdf"
    output_directory = f"/Users/nelsonlee/Documents/Fitness Business/Clients/{client_name}/Mesocycles/Meso {mesocycle}/"

    #if the path doesn't exist, we make a new directory
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    output_path = os.path.join(output_directory, output_filename)

    #making pdf and storing it in the output path
    pdfkit.from_string(output_text, output_path, configuration=config)

    print(f"{output_filename} was successfully created in {output_directory}")

    
except Exception as e:
    logging.exception(e)






