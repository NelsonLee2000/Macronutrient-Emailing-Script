bodyweight = int(input("Enter Bodyweight: "))
total_calories = int(input("Enter Total Calories: "))
total_protein = int(input("Enter Total Protein: "))
fats_ratio = float(input("Enter Fats Ratio: "))
mesocycle = input("Enter Mesocycle #: ")


total_fats = bodyweight * fats_ratio
total_carbs = (total_calories - ((total_protein * 4) + (total_fats * 9)))/4

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


print(f'mesocycle: {mesocycle}\nbodyweight: {bodyweight}\ntotal calories: {total_calories}\ntotal protein: {total_protein}\nfats ratio: {fats_ratio}\ntotal fats: {total_fats}\ntotal carbs: {total_carbs}\npre and post-workout meal: {pre_and_post_wo_meals}\ntwo regular meals: {two_regular_meals}')
