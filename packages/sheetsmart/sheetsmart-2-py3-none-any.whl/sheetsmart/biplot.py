import os
import pandas as pd
import matplotlib.pyplot as plt
import sheetsmart
sheetsmart.in_pkg()
def biplot():
    os.makedirs("data", exist_ok=True)
    
    filename = input("Enter the filename to analyze: ").lower() + ".csv"
    filepath = os.path.join("data", filename)
    
    if not os.path.exists(filepath):
        print("Error: File does not exist! Check the name of the file or use sheetsmart.write() to create a table.")
        return
    
    df = pd.read_csv(filepath)
    df.columns = [col.lower() for col in df.columns]  # Convert column names to lowercase
    
    while True:
        column_name = input("Enter the column name to analyze: ").strip().lower()
        
        if column_name in df.columns:
            break
        
        # Suggest a possible correct column name
        suggestions = [col for col in df.columns if column_name in col or col in column_name]
        suggestion_text = f" You may refer '{suggestions[0]}'?" if suggestions else ""
        print(f"Error: Column '{column_name}' not found in '{filename}'.{suggestion_text}")
    
    df.reset_index(inplace=True)  # Ensure index is used for x-axis (ID)
    
    plt.figure(figsize=(10, 6))
    plt.scatter(df['index'], df[column_name], label='Scatter Plot', color='blue', alpha=0.6)
    plt.plot(df['index'], df[column_name], linestyle='-', color='red', label='Line Plot')
    
    plt.xlabel("ID")
    plt.ylabel(column_name.capitalize())
    plt.title(f"Biplot(by SheetSmart) of {column_name.capitalize()} vs ID")
    plt.legend()
    plt.grid(True)
    plt.show()
