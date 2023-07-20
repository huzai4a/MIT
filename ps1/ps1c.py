# 2023-07-12

# gets user input for each needed value (no error checks)
annual_salary_orig = float(input("Enter your starting annual salary: "))
total_cost = 1000000 # float(input("Enter the cost of your dream home: "))

# initializing necessary variables
return_percent = 0.04
semi_annual_raise = 0.07
down_payment_percent = 0.25
portion_down_payment = down_payment_percent*total_cost
current_savings = 0

# if the full base salary is less than the down payment its impossible  
if (annual_salary_orig*3) < portion_down_payment: 
    print("It is not possible to pay the down payment in three years.")
else:
    # initializing variables for bisection search
    epsilon = 100
    num_bisects = 0
    low = 0
    # 10000 = 100%
    high = 10000
    # stored as an integer through int division
    # rate_int/10000 = rate decimal (9999 -> 0.9999 -> 99.99%)
    rate_int = (high + low)//2

    while abs(current_savings - portion_down_payment) > epsilon:
        # resets savings, months and salary every time the search repeats
        current_savings = 0
        months = 0
        annual_salary = annual_salary_orig

        # loops through adding months until sufficient savings
        while months <= 36:
            return_on_investment = current_savings*return_percent/12
            # this is where the rate takes effect
            current_savings += annual_salary/12*(rate_int/10000) + return_on_investment
            months += 1

            # if the month count is a factor of 6 get a raise
            if ((months%6) == 0):
                annual_salary *= (1 + semi_annual_raise)
        
        # add to bisection counter
        num_bisects += 1

        # if difference is admissable, the rate is found
        if abs(current_savings - portion_down_payment) < epsilon:
            break
        # otherwise if savings are lower than down payment, rate_int must be higher
        elif current_savings < portion_down_payment:
            low = rate_int
        # otherwise savings are high, rate_int must be lower
        else:
            high = rate_int

        # find the new rate_int to try
        rate_int = (low + high)//2
    

    # prints the best savings rate for inputted income
    print("Best savings rate:", rate_int/10000)
    # prints the number of steps taken during search
    print("Steps in bisections search:", num_bisects)

    # print("savings:", current_savings)
    # print("down payment:", portion_down_payment)