# Marconutrient PDF Emailing Script

This Python script calculates my coaching client's daily macronutrients (protein, fats, and carbohydrates), creates a pdf with the macronutrients split into 4 meals, stores the pdf in my client's file on my computer, and then emails the pdf to my client.

## Why?

As an online fitness coach, one of my tasks is to provide my clients with an updated nutrition sheet when we finish a cycle of training and dieting. For example, I may transition my client from a bulk to a cut, and this requires a change in their daily caloric intake. Usually this process is long and tedious, requiring me to insert inputs into my google sheets macrocalculator, copy the macronutrients per meal, make a new google document, paste in the macronutrients, format the google document, download the google document as a pdf, store it in the correct folder on my computer, and finally email it to my client. This process usually takes around 15 minutes.

With this script, this process now only takes 5 seconds (99.4% faster!). After inputting a couple of variables, the script will calculate the marconutirients per meal, create a well-formatted pdf with the calculated numbers,organize this pdf to my client's file on my computer, and email this pdf to my client.

## How does it work?

After the script is initialized, it will ask for 7 inputs: bodyweight in (lbs), daily calories (kcal), daily protein (g), fats ratio (0.3-0.4), mesocycle #, phase (Fat Loss, Massing, Maintenance, Deload), and client name. The script will then perform calculations to find the daily fats (g), daily carbs (g), macronutrients for 2 regular meals, and macronutrients for the pre- and post-workout meals. All the calculated numbers are rendered into a jinja2 html file, which is used to create a pdf with proper formatting and titles. The client name and mesocycle is used to determine the path of the pdf storage in my local computer. Additionally, if the path doesn't exist, the script will create a new one (useful for when we start a new mesocycle). After the creation of the pdf, the script will ask if you would like to send the pdf to the client. When prompted to send the pdf, the script will log into the SMTP (simple mail transfer protocol) server with my gmail creditials and send a formatted email with a subject, body, and pdf attachment to my client's email(fetched from a custom dictionary). Finally, the SMTP connection is closed and the script ends.