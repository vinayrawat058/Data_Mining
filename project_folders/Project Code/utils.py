import pandas as pd
import numpy as np 

def calculate_new_price_and_units(row,max_abs_inc=0.5,max_pct_inc=0.1,gc_loss=0.01):
    elasticity = row["Elasticity"]
    current_price = row["Product_Price"]
    units_sold = row["Units"]
    current_revenue = row["xRevenue"]

   # Constraints
    max_price_increase = min(max_abs_inc, max_pct_inc * current_price)  # Maximum price increase
    max_price = current_price + max_price_increase       # Maximum allowed price
    price_steps = np.arange(current_price, max_price+0.04, 0.05)  # Price steps

    best_price = current_price  # Default to current price if no better price is found
    best_units = units_sold     # Default to current units if no better price is found

    # Iterate over potential new prices
    for new_price in price_steps:
        # Calculate new units and revenue
        new_units = units_sold * (1 + elasticity * (new_price - current_price) / current_price)
        new_revenue = new_price * new_units

        # Check constraints: revenue > current_revenue, units loss ≤ 2%
        if new_revenue > current_revenue and (units_sold - new_units) / units_sold <= gc_loss:
            best_price = new_price  # Update best price if valid
            best_units = new_units  # Update corresponding units

    return pd.Series([best_price, best_units])

CITY_LIST =  ['Aguascalientes',
 'Campeche',
 'Chetumal',
 'Chihuahua',
 'Chilpancingo',
 'Ciudad Victoria',
 'Cuernavaca',
 'Cuidad de Mexico',
 'Culiacan',
 'Durango',
 'Guadalajara',
 'Guanajuato',
 'Hermosillo',
 'La Paz',
 'Merida',
 'Mexicali',
 'Monterrey',
 'Morelia',
 'Oaxaca',
 'Pachuca',
 'Puebla',
 'Saltillo',
 'San Luis Potosi',
 'Santiago',
 'Toluca',
 'Tuxtla Gutierrez',
 'Villahermosa',
 'Xalapa',
 'Zacatecas']

LOC_LIST = ['Airport', 'Commercial', 'Downtown', 'Residential']

def adjust_price(price):
    # Round to two decimal places first
    rounded_price = round(price, 2)

    # Calculate the nearest numbers ending in 9 or 5
    nearest_9 = round(rounded_price, 1) - (round(rounded_price, 1) % 1) + 0.09
    nearest_5 = round(rounded_price, 1) - (round(rounded_price, 1) % 1) + 0.05

    # Ensure they are exactly two decimal places
    nearest_9 = round(nearest_9, 2)
    nearest_5 = round(nearest_5, 2)

    # Choose the closer of the two
    if abs(rounded_price - nearest_9) < abs(rounded_price - nearest_5):
        return nearest_9
    else:
        return nearest_5

