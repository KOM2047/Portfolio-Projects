import math

# Print out descriptions of investments
print("investment - to calculate the amount of interest you'll earn on your investment")
print("bond - to calculate the amount you'll have to pay on a home loan")

# Ask user to select which calculation they want to do
# Use .lower() to ensure continuity regradless of case choice in input
calculation = input("Enter either “investment” or “bond” from the menu above to proceed: ").lower()



# if the user enters "investment"
if calculation == ("investment"):
    # Ask user to input amount being deposited
    deposit = int(input("Enter the amount being deposited: R "))
    # Ask user to input interest rate without the percentage symbol
    intrst_rate = int(input("Enter your interest rate: % "))
    # Ask how long user is investing
    years = int(input("How long is your investment: "))
    # Ask user to choose between "simple" or "compound"
    # Execute calculation regardless of input case choice
    interest = input("Choose between simple or compound interest: ").lower()
    # If interest = "simple"
    #   Calculate simple interest 
    if interest == "simple":
        simple_interest = deposit * (1 + (intrst_rate / 100) * years)
        print(round(simple_interest,2))
    # If interest = "compound"
    #   Calculate compound interest
    elif interest == "compound":
        compound_interest = deposit * math.pow((1 + (intrst_rate / 100)), years)
        print(round(compound_interest,2))

# If user enters "bond"
elif calculation == ("bond"):
    # Ask user to enter current house value
    house_value = int(input("Enter the present value of your house: "))
    # Enter the interest rate
    intrst_rate = int(input("Enter the annual interest rate: % "))
    # Enter the planned repayment term
    repay_term = int(input("Over how many months do you plan to repay the bond: "))
    # Calculate monthly interest rate
    monthly_interest = ((intrst_rate / 100) / 12)
    # Calculate monthly bond payment
    numerator = (monthly_interest * house_value)
    denominator = (1 + monthly_interest) ** (-repay_term)
    bond = numerator / denominator
    print(round(bond,2))
# If user inputs anything other than "investment" or "bond" display error message
else: 
    print("Invalid Input")
    