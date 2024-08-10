# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import numpy as np
import matplotlib.pyplot as plt

# Define the original print and e-book prices
print_price = 60  # Original print book price
ebook_price = 48  # Original e-book price

# Define ranges for print to e-book sales ratios
ebook_ratios = np.linspace(0.1, 0.9, 10)  # e-book ratio from 10% to 90%
print_ratios = 1 - ebook_ratios  # Corresponding print ratios

# Other constants
royalty_rates = [0.15, 0.12, 0.10]
advances = [0, 5000, 8000]
ebook_royalty_rate = 0.25
sales_range = np.linspace(0, 20000, 1000)

# Initialize a list to store the crossover points for different ratio combinations
crossover_points_ratios = []

# Perform the sensitivity analysis by varying the print to e-book ratios
for ebook_ratio in ebook_ratios:
    print_ratio = 1 - ebook_ratio
    # Recalculate the average book price and average royalty rates
    average_book_price = ebook_price * ebook_ratio + print_price * print_ratio
    average_royalty_rate_15 = (ebook_royalty_rate * ebook_ratio) + (royalty_rates[0] * print_ratio)
    average_royalty_rate_10 = (ebook_royalty_rate * ebook_ratio) + (royalty_rates[2] * print_ratio)
    
    # Recalculate break-even point for the 10% model
    sales_to_payback_advance_8000 = advances[2] / (average_royalty_rate_10 * average_book_price)
    
    # Recalculate cumulative earnings for both the 10% and 15% models
    earnings_10_percent_sensitivity = np.where(
        sales_range < sales_to_payback_advance_8000,
        8000,
        8000 + (sales_range - sales_to_payback_advance_8000) * average_royalty_rate_10 * average_book_price
    )
    earnings_15_percent_sensitivity = sales_range * average_royalty_rate_15 * average_book_price
    
    # Find the crossover point where the 15% model surpasses the 10% model
    crossover_index = np.where(earnings_15_percent_sensitivity > earnings_10_percent_sensitivity)[0][0]
    crossover_sales = sales_range[crossover_index]
    
    # Store the crossover point for this ratio
    crossover_points_ratios.append(crossover_sales)

# Plot the sensitivity analysis as a line plot
plt.figure(figsize=(10, 6))
plt.plot(ebook_ratios, crossover_points_ratios, marker='o')
plt.axvline(0.25, color='black', linestyle='--')  # Add vertical dotted line at 0.25
plt.axvline(0.75, color='black', linestyle='--')  # Add vertical dotted line at 0.75
plt.title('Sensitivity of Crossover Point to Print-to-e-Book Sales Ratios')
plt.xlabel('e-Book Ratio')
plt.ylabel('Crossover Point (Books Sold)')
plt.grid(True)
plt.show()