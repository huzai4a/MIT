# 2023-07-11

# gets user input for each needed value (no error checks)
annual_salary = float(input("Enter your starting annual salary: "))
portion_saved = float(input("Enter the percent of your salary to save, as a decimal: "))
total_cost = float(input("Enter the cost of your dream home: "))

# initializing necessary variables
portion_down_payment = 0.25*total_cost
current_savings = 0
months = 0

# loops through adding months until sufficient savings
while current_savings < portion_down_payment:
    return_on_investment = current_savings*0.04/12
    current_savings += annual_salary/12*portion_saved + return_on_investment
    months += 1

# prints the number of months before down payment can be made
print("Number of months:", months)