def display_profile():
    # 1. Collecting User Input
    print("Please enter the following details:")
    name = input("Name: ")
    address = input("Address: ")
    birthday = input("Birthday (e.g., Month DD, YYYY): ")

    # 2. Organizing the data into a dictionary
    profile = {
        "NAME": name,
        "ADDRESS": address,
        "BIRTHDAY": birthday
    }

    # 3. Displaying the information
    print("\n" + "="*30)
    print("       USER PROFILE")
    print("="*30)
    
    for key, value in profile.items():
        # .title() makes the labels look neat
        print(f"{key:<10}: {value}")
    
    print("="*30)

# Run the function
if __name__ == "__main__":
    display_profile()
