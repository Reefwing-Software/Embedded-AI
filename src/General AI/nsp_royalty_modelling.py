# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import numpy as np
import matplotlib.pyplot as plt

# Define a range of book sales
sales_range = np.linspace(0, 5000, 1000)  # Sales from 0 to 20,000

# Define the royalty rates and advances
royalty_rates = [0.15, 0.12, 0.10]
advances = [0, 5000, 8000]

# Define the new prices and sales mix
#ebook_price = 48
#print_book_price = 60
ebook_price = 24
print_book_price = 30
ebook_ratio = 0.25
print_book_ratio = 0.75

# Update the royalty rates for e-books to 25% for all models
ebook_royalty_rate = 0.25

# Calculate the average royalty per book considering the mix of e-book and print sales
average_royalty_rate_15 = (ebook_royalty_rate * ebook_ratio) + (royalty_rates[0] * print_book_ratio)
average_royalty_rate_12 = (ebook_royalty_rate * ebook_ratio) + (royalty_rates[1] * print_book_ratio)
average_royalty_rate_10 = (ebook_royalty_rate * ebook_ratio) + (royalty_rates[2] * print_book_ratio)

# Calculate the average price per book considering the sales mix
average_book_price = ebook_price * ebook_ratio + print_book_price * print_book_ratio

# Calculate the break-even points for the advances
sales_to_payback_advance_8000 = advances[2] / (average_royalty_rate_10 * average_book_price)
sales_to_payback_advance_5000 = advances[1] / (average_royalty_rate_12 * average_book_price)

# Recalculate cumulative earnings with the updated e-book royalty rates
earnings_option_1_updated = np.maximum(0, sales_range * average_royalty_rate_15 * average_book_price)
earnings_option_2_updated = np.where(
    sales_range < sales_to_payback_advance_5000,
    5000,
    5000 + (sales_range - sales_to_payback_advance_5000) * average_royalty_rate_12 * average_book_price
)
earnings_option_3_updated = np.where(
    sales_range < sales_to_payback_advance_8000,
    8000,
    8000 + (sales_range - sales_to_payback_advance_8000) * average_royalty_rate_10 * average_book_price
)

# Recalculate cumulative earnings for both the 10% and 15% models with the updated rates
earnings_10_percent_updated = np.where(
    sales_range < sales_to_payback_advance_8000,
    8000,
    8000 + (sales_range - sales_to_payback_advance_8000) * average_royalty_rate_10 * average_book_price
)
earnings_15_percent_updated = sales_range * average_royalty_rate_15 * average_book_price

# Find the updated crossover point where the 15% model surpasses the 10% model
crossover_15_10_index_updated = np.where(earnings_15_percent_updated > earnings_10_percent_updated)[0][0]
crossover_15_10_sales_updated = sales_range[crossover_15_10_index_updated]

# Plot the updated cumulative earnings with the crossover point highlighted
plt.figure(figsize=(10, 6))
plt.plot(sales_range, earnings_option_1_updated, label='15% Royalty, $0 Advance (with 25% e-book)')
plt.plot(sales_range, earnings_option_2_updated, label='12% Royalty, $5000 Advance (with 25% e-book)')
plt.plot(sales_range, earnings_option_3_updated, label='10% Royalty, $8000 Advance (with 25% e-book)')

# Highlight the updated crossover point between the 10% and 15% models
plt.scatter(crossover_15_10_sales_updated, earnings_15_percent_updated[crossover_15_10_index_updated], color='red', label='Crossover 15% vs 10%')
plt.axvline(sales_to_payback_advance_8000, color='grey', linestyle='--', label='8000 Advance Break-even')
plt.axvline(sales_to_payback_advance_5000, color='blue', linestyle='--', label='5000 Advance Break-even')
plt.text(crossover_15_10_sales_updated, earnings_15_percent_updated[crossover_15_10_index_updated], f'{int(crossover_15_10_sales_updated)} books', verticalalignment='bottom')

plt.title('Cumulative Earnings vs. Book Sales with 25% e-Book Royalty')
plt.xlabel('Number of Books Sold')
plt.ylabel('Cumulative Earnings ($)')
plt.legend()
plt.grid(True)
plt.show()