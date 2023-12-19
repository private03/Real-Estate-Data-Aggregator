import tkinter as tk
from tkinter import filedialog
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def load_data():
    filename = filedialog.askopenfilename(title="Select CSV File", filetypes=[("CSV files", "*.csv")])
    if filename:  # If a file was selected
        df = pd.read_csv(filename)
        clean_data(df)

def clean_data(df):
    df['price'] = df['price'].replace(r'[\$,]', '', regex=True).astype(float)
    df['square_footage'] = pd.to_numeric(df['square_footage'], errors='coerce')
    df.dropna(subset=['price', 'square_footage'], inplace=True)
    plot_price_distribution(df)
    plot_price_vs_square_footage(df)

def plot_price_distribution(df):
    plt.figure(figsize=(10, 6))
    ax = sns.histplot(df['price'], kde=True)
    ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.0f}'))
    plt.title('Distribution of Property Prices')
    plt.xlabel('Price ($)')
    plt.ylabel('Count')
    plt.show()

def plot_price_vs_square_footage(df):
    # Convert price from dollars to millions of dollars
    df['price_in_millions'] = df['price'] / 1e6

    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='square_footage', y='price_in_millions')
    plt.title('Price (in millions) vs. Square Footage')
    plt.xlabel('Square Footage')
    plt.ylabel('Price (Millions $)')
    plt.show()
def main():
    # Create the main window
    root = tk.Tk()
    root.title("Data Visualization Tool")

    # Create a button to load data and plot
    load_button = tk.Button(root, text="Load Data and Plot", command=load_data)
    load_button.pack(pady=20)

    # Start the GUI event loop
    root.mainloop()

if __name__ == "__main__":
    main()
