# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import numpy as np
import matplotlib.pyplot as plt

# Define ranges for print and e-book prices
print_prices = np.linspace(50, 70, 10)  # Print book prices from $50 to $70
ebook_prices = np.linspace(40, 55, 10)  # e-book prices from $40 to $55

# Other constants
royalty_rates = [0.15, 0.12, 0.10]
advances = [0, 5000, 8000]
ebook_ratio = 0.25
print_book_ratio = 0.75
ebook_royalty_rate = 0.25
sales_range = np.linspace(0, 20000, 1000)

# Initialize a matrix to store the crossover points for different price combinations
crossover_matrix = np.zeros((len(print_prices), len(ebook_prices)))

# Perform the sensitivity analysis by varying print and e-book prices
for i, print_price in enumerate(print_prices):
    for j, ebook_price in enumerate(ebook_prices):
        # Recalculate the average book price and average royalty rates
        average_book_price = ebook_price * ebook_ratio + print_price * print_book_ratio
        average_royalty_rate_15 = (ebook_royalty_rate * ebook_ratio) + (royalty_rates[0] * print_book_ratio)
        average_royalty_rate_10 = (ebook_royalty_rate * ebook_ratio) + (royalty_rates[2] * print_book_ratio)
        
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
        
        # Store the crossover point in the matrix
        crossover_matrix[i, j] = crossover_sales

# Plot the sensitivity analysis as a contour plot
X, Y = np.meshgrid(ebook_prices, print_prices)
plt.figure(figsize=(10, 8))
contour = plt.contourf(X, Y, crossover_matrix, levels=20, cmap='viridis')
plt.colorbar(contour, label='Crossover Point (Books Sold)')
plt.title('Sensitivity of Crossover Point to Print and e-Book Prices')
plt.xlabel('e-Book Price ($)')
plt.ylabel('Print Book Price ($)')
plt.show()