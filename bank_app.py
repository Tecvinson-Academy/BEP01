from email_validator import validate_email,EmailNotValidError as e
import datetime
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, date
import random
import string
import pandas as pd
import seaborn as sns
import os

date_time = datetime.now()
transaction_id = 'BEPO1'+ "".join(random.choices(string.digits, k=8))

def withdrawal_df(account_number):
    d_df = pd.read_csv("deposit_database.csv")
    balance = d_df["Balance"].iloc[0]
    amount = float(input("Enter the amount to withdraw: "))
    if amount <= balance:
        category_type = input("Enter the withrawal category: ").title()              
        otp = str(random.randint(100000, 999999))
        print(f"Your OTP is {otp} please keep safe")
        otp_check = input("Type in the OTP sent to your email: ")
        if otp_check == otp:
            if not os.path.exists("withdrawal_database.csv"):
                data = {"Transaction_id": [], "Account_number": [], "Withdrawal": [], "Expense_category": []}
                empty_df = pd.DataFrame.from_dict(data)
                updated_data = {"Transaction_id": [transaction_id], "Account_number": [account_number], "Withdrawal": [amount], "Expense_category": [category_type]}
                new_df = pd.DataFrame.from_dict(updated_data)
                withdr_df = pd.concat([empty_df, new_df], ignore_index=True)
                updated_data = withdr_df.merge(d_df, on = ["Transaction_id", "Account_number"], how = 'left')
                updated_data["Balance"] = (d_df["Balance"] - withdr_df["Withdrawal"]).cumsum()
                updated_data["Date"]= date_time.strftime('%m/%d/%Y')
                updated_data['Month'] = date_time.strftime('%b')
                updated_data['Time'] = date_time.strftime('%H:%M:%S')
                updated_data.to_csv('withdrawal_database.csv', index=False)     
                print('Withdrawal successful')   
            else: 
                df = pd.read_csv("withdrawal_database.csv")
                updated_data = {"Transaction_id": [transaction_id], "Account_number": [account_number], "Withdrawal": [amount], "Expense_category": [category_type]}
                new_df = pd.DataFrame.from_dict(updated_data)
                updated_data = new_df.merge(df, on = ["Transaction_id", "Account_number", "Withdrawal", "Expense_category"], how = 'outer')
                updated_data["Balance"] = (df["Balance"] - new_df["Withdrawal"]).cumsum()
                updated_data["Date"]= date_time.strftime('%m/%d/%Y')
                updated_data['Month'] = date_time.strftime('%b')
                updated_data['Time'] = date_time.strftime('%H:%M:%S')
                updated_data.to_csv('withdrawal_database.csv', index=False) 
                print('Withdrawal successful')
                return updated_data         
        else:
            print("Incorrect OTP. Please try again.")        
    else:
        print("Insufficient balance.")
    

def deposit_df(d_category_type, account_number):
    c_df = pd.read_csv('customer_database.csv')
    amount = float(input("Enter the amount to deposit: "))
    if amount > 0:
        categories = ["Savings", "Fixed Deposit" , "Saving"]
        for d_category_type in categories:
            if d_category_type == "Saving":
                d_category_type = d_category_type + "s"
                if not os.path.exists("deposit_database.csv"):
                    data = {"Transaction_id": [], "Account_number": [], "Deposit": [], "Deposit_type": []}
                    empty_df = pd.DataFrame.from_dict(data)
                    updated_data = {"Transaction_id": [transaction_id], "Account_number": [account_number], "Deposit": [amount], "Deposit_type": [d_category_type]}
                    new_df = pd.DataFrame.from_dict(updated_data)
                    deposit_df = pd.concat([empty_df, new_df], ignore_index=True)
                    updated_data = deposit_df.merge(c_df, on = ["Transaction_id", "Account_number", "Deposit"], how = 'left')
                    updated_data["Balance"] = (df["Balance"] + deposit_df["Deposit"]).cumsum()
                    updated_data["Date"]= date_time.strftime('%m/%d/%Y')
                    updated_data['Month'] = date_time.strftime('%b')
                    updated_data['Time'] = date_time.strftime('%H:%M:%S')
                    updated_data.to_csv('deposit_database.csv', index=False)     
                    print('Deposit successful')   
                else: 
                    df = pd.read_csv("deposit_database.csv")
                    updated_data = {"Transaction_id": [transaction_id], "Account_number": [account_number], "Deposit": [amount], "Deposit_type": [d_category_type]}
                    new_df = pd.DataFrame.from_dict(updated_data)
                    updated_data = new_df.merge(df, on = ["Transaction_id", "Account_number", "Deposit", "Deposit_type"], how = 'outer')
                    updated_data["Balance"] = (df["Balance"] + new_df["Deposit"]).cumsum()
                    updated_data["Date"]= date_time.strftime('%m/%d/%Y')
                    updated_data['Month'] = date_time.strftime('%b')
                    updated_data['Time'] = date_time.strftime('%H:%M:%S')
                    updated_data.to_csv('deposit_database.csv', index=False) 
                    print('Deposit successful') 
                return updated_data
        else:
            print('ValueError: Check your spelling. Deposit type [Savings, Fixed Deposit]')
    else:
        return f"Invalid amount. Please try again."
    return f"Your deposit of {amount} has been successfully deposited."

def analyser():
    withdraw_df = pd.read_csv('withdrawal_database.csv')
    customer_df = pd.read_csv('deposit_database.csv')
    df = pd.concat([customer_df, withdraw_df], ignore_index = True)
    df["Transaction_type"] = df.apply(lambda row:"Deposit" if pd.notna(row["Deposit"]) else "Withdrawal", axis  = 1) 
    df = df.drop(["Account Name","DOB" , "Email",  "Account_type"], axis = 1) 
    df["Description"] = df["Deposit_type"].combine_first(df["Expense_category"])
    df["Description"] = df["Description"].astype("category")
    df["Deposit"] = df["Deposit"].astype(float).fillna(0)
    df["Withdrawal"] = df["Withdrawal"].astype(float).fillna(0)
    cols = list(df.columns) 
    last_three_cols = cols[-3:]
    remaining_cols = cols[:-3]
    new_column_order = remaining_cols[:1] + last_three_cols + remaining_cols[1:]
    df = df.reindex(columns = new_column_order)
    df["Transaction_type"] = df["Transaction_type"].astype("category")
    df["Description"] = df["Description"].astype("category")
    df["Amount"] = df.apply(lambda row:row["Deposit"] if row["Deposit"] != 0 else row["Withdrawal"], axis  = 1) 
    df['Time_dep_diff'] = df['Deposit'].diff()
    df["Time_dep_diff"] = df["Time_dep_diff"].astype(float).fillna(0)
    df['Time_witd_diff'] = df['Withdrawal'].diff()
    df["Time_witd_diff"] = df["Time_witd_diff"].astype(float).fillna(0)
    df['Consecutive_dep_drops'] = df['Time_dep_diff'].rolling(window=2).apply(lambda x: all(x < 0))
    df['Consecutive_witd_drops'] = df['Time_witd_diff'].rolling(window=2).apply(lambda x: all(x < 0))
    df['Consecutive_dep_drops'] = df['Consecutive_dep_drops'].fillna(0)
    df['Consecutive_witd_drops'] = df['Consecutive_witd_drops'].fillna(0)
    df.to_csv('analyser.csv', index=False)
    return df     

def generate_recommendations():
    df = pd.read_csv("analyser.csv")
    recommendations = []
    for i, row in df.iterrows():
        if row['Time_dep_diff'] < 0:
            if row['Consecutive_dep_drops'] == 1.0:
                recommendations.append(f"Noticeable pattern: Deposits have consistently decreased over the last two months (up to {row['Time']}). Consider reviewing your spending habits and setting up a stricter budget.")
            else:
                recommendations.append(f"Alert: Deposits dropped in {row['Time']}. Consider increasing your deposits next month to meet savings goals.")
        else:
            recommendations.append(f"Good job in {row['Time']}: Deposits increased. Keep up the good work!")
        if row['Time_witd_diff'] > 0:
            if row['Consecutive_witd_drops']:
                recommendations.append(f"Noticeable pattern: Withdrawal have consistently increased over the last two withdrawals (up to {row['Time']}). Consider reviewing your spending habits and setting up a stricter budget.")
            else:
                recommendations.append(f"Alert: Your withdrawal increased in {row['Time']}. Consider reducing your withrawal next time to meet savings goals.")
        else:
            recommendations.append(f"A big shout out for you!!! Your withdrawal on  {row['Time']} reduced. Keep up the good work!")
    category_recommendations = {
    'Grocery': 'Consider setting a weekly grocery budget.',
    'Movie': 'Limit entertainment expenses to maintain savings.',
    'Restaurant': 'Eating out frequently can impact your savings.',
    'Rent': 'Ensure rent is a fixed part of your budget.',
    'Bill': 'Review utility bills regularly to avoid overspending.',
    'Uncategorized': 'Find away around saving more.',
    'Lease': 'Ensure lease is a fixed part of your budget.',
    'Travel': "Ensure travel expenses is a fixed part of your budget.",
    'Supplies':  "Ensure you make deposits after sales to balance your account.",
    'Others' : "Ensure your expense is a fixed part of your budget.",
    'Other': "Ensure your expense is a fixed part of your budget.",
    "Office Expenses": "Recommend a hybrid or remote job type for your employees. This will reduce cost.",
    'Postage': 'Recommend usage of E-mails for posting of your documents'
    }
    for word, recommendation in category_recommendations.items():
        if word in df['Description']:
            print(recommendation)
        print('No specific recommendation.')
    df['Recommendation'] = df.apply(generate_recommendations(), axis=1)
    # Generate recommendations for the customer
    recommendations = generate_recommendations()
    for rec in recommendations:
        print(rec, end = "")
def visuals():
    df = pd.read_csv("analyser.csv")
    # Create a figure and an array of axes: 2 rows, 1 column with shared y axis
    sns.set_style("darkgrid")
    fig, axes = plt.subplots(1, 2, figsize=(18, 6)) 
    plt.subplots_adjust(top=0.93)
    sns.barplot(x='Transaction_type', y='Amount', data=df, hue = "Transaction_type", ax=axes[0], ci = None)
    axes[0].set_title('Transaction Analysis')
    axes[0].set_xlabel('Time')
    axes[0].set_ylabel('Deposit Amount')
    axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=90)
    # Scatter plot 2: column1 vs column3
    sns.barplot(x = "Expense_category", y='Amount', data=df, hue = "Expense_category", ax=axes[1], ci=None)
    axes[1].set_title('Withdrawal Analysis')
    axes[1].set_xlabel('Time')
    axes[1].set_ylabel('Withdrawal Amount')
    axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=90)
    plt.tight_layout() 
    plt.show()


def validate_account_type(account_type):
    account_types = ["Salary", "Individual" , "Business"]
    if account_type in account_types:
        return account_type
    else:
        print("Invalid Account type, check your spelling")
    
def email_validation(email):
    try:
        valid_email = validate_email(email)
        email = valid_email.email
        return True
    except e:
        print("Invalid Email Format")
    
def name_validation(account_name):
       return all(char.isalpha() or char.isspace() or char=="-" for char in account_name)

def validate_dob(dob):
    import datetime
    from datetime import datetime, date
    if dob:
        current_date = date.today()
        age = current_date.year - dob.year
        for_under_age = 18 - age
        if (current_date.month, current_date.day) < (dob.month, dob.day):
            age -= 1
            if age >= 18: 
                pass    
            else:
                
                print("Your age is below 18, you'can't contnue. Thank you for chosing BEP01 banking application. Hope to see you in the next {for_under_age}")
    else:
        return f"You entered a wrong date format"    
    return dob.strftime("%Y%m%d"), age
def generate_account_number(dob):
    dob = str(dob.strftime("%Y%m%d"))
    account_number = dob + "-" + "".join(random.choices(string.digits, k=4))
    return account_number

def balance_checker(account_number):
    d_df = pd.read_csv("deposit_database.csv")
    if os.path.exists("withdrawal_database.csv"):
        w_df = pd.read_csv("withdrawal_database.csv")
        balancer_checker = d_df.merge(w_df, on = ["Transaction_id", "Balance"], how = 'outer')
        balance = balancer_checker["Balance"].iloc[0]
        print(f"\nAcccount_number: {account_number}\nBalance: {balance}")
        return f"\nAcccount_number: {account_number}\nBalance: {balance}"
    else:
        withdrawal_df(account_number)
        w_df = pd.read_csv("withdrawal_database.csv")
        balancer_checker = d_df.merge(w_df, on = ["Transaction_id", "Balance"], how = 'outer')
        subset_checker = balancer_checker[["Account_name","Account_number","Deposit", "Withdrawal", "Balance"]]
        balance = subset_checker["Balance"].iloc[0]
        print(f"\nAcccount_number: {account_number}\nBalance: {balance}")
        return f"\nAcccount_number: {account_number}\nBalance: {balance}"
def set_overdraft_limit():
    df = pd.read_csv("transaction.csv")
    otp = random.randint(100000, 999999)
    print(f"Your OTP is {otp} please keep safe")
    otp_check = int(input("Type in the OTP sent to your email: "))
    otp = int(otp)
    if otp_check == otp:
        limit = (df["Balance"].sum() * 3 /100) * -1
        overdraft_limit = limit
        print(f"Overdraft limit set to {round(overdraft_limit, 2)}")
    else:
        print("Incorrect OTP. Please try again.")
def apply_for_a_loan(account_type):
    df = pd.read_csv("wtihdrawal.csv")
    otp = random.randint(100000, 999999)
    print(f"Your OTP is {otp} please keep safe")
    otp_check = int(input("Type in the OTP sent to your email: "))
    otp = int(otp)
    if otp_check == otp:  
        amount = float(input("Enter the loan amount: "))    
        if account_type == "salary" or "business":
            print("You are eligible for a loan.")
            limit = (df["Balance"].sum() * 3 /100) * -1
            if df["Balance"].iloc[0] > limit:
                print(f"Loan approved.")
            else:
                print(f"You cannot exceed your {round(limit, 2)} ")
        else:
            print("You are not eligible for this loan.")
    else:
        print("Invalid OTP, try again")
def create_account():
    while True:
        first_name = input("First name: ").title()
        last_name = input("Last name: ").title()
        account_name = first_name + " "+ last_name
        if name_validation(account_name):
            year_of_brith = int(input("Enter your year of birth: "))
            month_of_birth = int(input("Enter your month of birth: "))
            day_of_birth = int(input("Enter your day of birth: "))
            dob = date(year_of_brith, month_of_birth, day_of_birth) 
            if validate_dob(dob):
                email = input("Enter your email: ")
                if email_validation(email):
                    account_type = input("Enter account type (salary/individual/business): ").title()
                    if validate_account_type(account_type):                     
                        initial_deposit = float(input("Enter initial deposit amount: "))
                        if initial_deposit > 5:
                            dob = str(dob.strftime("%Y%m%d"))
                            account_number = dob + "-" + "".join(random.choices(string.digits, k=4))
                            balance = initial_deposit
                            print("Account created successfully.")
                            if not os.path.exists("customer_database.csv"):
                                data = {"Transaction_id":[], "Account Name": [], "Account_number": [], "DOB":[], "Email":[],"Account_type": [], "Deposit":[]}
                                df = pd.DataFrame.from_dict(data)
                                updated_data = {"Transaction_id": [transaction_id], "Account Name": [account_name ], "Account_number": [account_number], "DOB":[dob], "Email":[email],"Account_type": [account_type], "Deposit":[initial_deposit]}
                                new_df = pd.DataFrame.from_dict(updated_data)    
                                updated_data = pd.concat([df, new_df], ignore_index=True)
                                updated_data["Date"]= date_time.strftime('%m/%d/%Y')
                                updated_data['Month'] = date_time.strftime('%b')
                                updated_data['Time'] = date_time.strftime('%H:%M:%S')
                                updated_data["Balance"] = balance
                                updated_data.to_csv('customer_database.csv', index=False)     
                                print(f"\nAccount Name: {account_name}\nAccount Number: {account_number}\nBalance: {round(balance, 2)}")    
                                return f"\nAccount Name: {account_name}\nAccount Number: {account_number}\nBalance: {round(balance, 2)}"          
                            else:
                                df = pd.read_csv("customer_database.csv")
                                updated_data = {"Transaction_id": [transaction_id], "Account Name": [account_name ], "Account_number": [account_number], "DOB":[dob], "Email":[email],"Account_type": [account_type], "Deposit":[initial_deposit]}
                                new_df = pd.DataFrame.from_dict(updated_data)    
                                updated_data = pd.concat([df, new_df], ignore_index=True)
                                updated_data["Date"]= date_time.strftime('%m/%d/%Y')
                                updated_data['Month'] = date_time.strftime('%b')
                                updated_data['Time'] = date_time.strftime('%H:%M:%S')
                                updated_data["Balance"] = balance
                                updated_data.to_csv('customer_database.csv', index=False)
                                print(f"\nAccount Name: {account_name}\nAccount Number: {account_number}\nBalance: {round(balance, 2)}")
                                return f"\nAccount Name: {account_name}\nAccount Number: {account_number}\nBalance: {round(balance, 2)}" 
                        else:
                            print("Initial deposit for account opening is $5 (min)")             
                            
            else:
                print("Invalid Date Format")
        else:
            print("Name should have only alphabets")        

def main():
    print("Welcome to BEP01 bank Application")
    while True:
        print("\n1. Create Account")
        print("2. Deposit Funds")
        print("3. Check Account Balance")
        print("4. Withdraw Funds")
        print("5. Set overdraft limit")
        print("6. Apply for Loan")
        print("7. Transaction Analysis")
        print("8. Exit")
        choice = int(input("\nEnter your choice: "))
        if choice == 1:
            account = create_account()
        elif choice in [2, 3, 4, 5, 6,7]:
            df = pd.read_csv("customer_database.csv")
            account_number = input("Enter your account number: ")
            if account_number in df["Account_number"].values:
                if choice == 2:
                    d_category_type = input('Deposit Category[Savings, Fixed Deposit]: ').title()
                    deposit_df(d_category_type, account_number)
                elif choice == 3:
                    balance_checker(account_number)
                elif choice == 4:
                    withdrawal_df(account_number)
                elif choice == 5:
                    set_overdraft_limit()
                elif choice == 6:
                    account_type = input("Enter account type (salary/individual/business): ").title()
                    if account_type == "Salary" or "Business":
                        apply_for_a_loan(account_type)
                elif choice == 7:
                    print("1. View Transaction Analysis")
                    print("2. View Recommendation")
                    transaction_choice = int(input("Enter your choice: "))
                    if transaction_choice == 1:
                        analyser()
                        visuals()
                    elif transaction_choice == 2:
                        analyser()
                        generate_recommendations()
                    else:
                        print("Select the correct option")
            else:
                print("Account number not found.")
        elif choice == 8:
            print("Thank you for using the bank application!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()