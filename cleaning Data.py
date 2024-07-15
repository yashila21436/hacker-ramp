import pandas as pd
from rapidfuzz import process

# Load the data, skipping the first row
file_path = 'filtered_data.csv'
data = pd.read_csv(file_path, header=1, names=['name', 'frequency'])

# Convert frequency column to integer
data['frequency'] = data['frequency'].astype(int)

# Ensure all values in the 'name' column are strings
data['name'] = data['name'].astype(str)

# Define a list of known brand names (including both lists)
known_brands = [
    'Kate Spade', 'Vineyard Vines', 'Kenneth Cole', 'Oscar de la Renta', 'David Beckham',
    'Cargo Cosmetics', 'Sugaring NYC', 'Dissh Boutique', 'Savette Handbags',
    'Louis Vuitton', 'Chanel', 'Hermès', 'L’Oréal', 'Dior', 'Sephora', 'Lancome',
    'Adidas', 'Boss', 'Nivea', 'Puma', 'Gucci', 'Prada', 'Benetton', 'Bulgari',
    'Armani', 'Zara', 'H&M', 'Cartier', 'Swatch', 'Rolex', 'Burberry', 'Nike',
    'Tiffany', 'Levi\'s', 'Gap', 'Ralph & Lauren', 'Estee', 'Avon', 'Polo',
    'Victoria\'s Secret',
    'Colourful Rebel', 'Balr.', 'Bimba Y Lola', 'Champion', 'ARMA', '8848 Altitude',
    'Amicci', 'Bonobo Jeans', 'Circle of Trust', 'Any Di', 'Celine', 'Cavallaro Napoli',
    'AlphaTauri', 'alexander mcqueen', 'Acne Studios', 'BAV TAiLOR', 'ALICE\'S LIPS',
    'Bellerose', 'COMAZO', 'COLOURS & SONS', 'Comfort Club', 'Chinese Laundry',
    'Coccinelle', 'Bally', 'Cloud9', 'Club 24', 'COUNTRY LINE', 'Cluca', 'Camper',
    'a.p.c', 'Artuyt', 'Claudie Pierlot', 'Chabo Bags', 'Australian Footwear', 'Barts',
    'CECIL', 'Charles & Keith', 'Chloé', 'A fish named Fred', 'Balenciaga', 'Converse',
    'ARMEDANGELS', 'CALIDA', 'CALVIN KLEIN', 'Cars Jeans', 'COSMOS COMFORT',
    'Burkely', 'Cast Iron', 'Bogner', 'Companeros', 'Cosel', 'Copenhagen Studios',
    'Armani Exchange', 'chaYkra', 'Bootstock', 'alpha industries', 'CKS',
    'CG – CLUB of GENTS'
]

# Create a function to check and merge brand names based on similarity
def merge_brand_names(data, known_brands, threshold=90):
    # Create a copy of the original data to avoid modifying it directly
    data_copy = data.copy()

    # Dictionary to store the combined frequencies of the brand names
    brand_frequencies = {brand: 0 for brand in known_brands}

    # Loop through each row in the data
    for index, row in data_copy.iterrows():
        name = row['name']
        frequency = row['frequency']
        matched = False

        # Check for similarity with known brands
        best_match = process.extractOne(name, known_brands)
        if best_match and best_match[1] >= threshold:
            brand_frequencies[best_match[0]] += frequency
            matched = True

        # If no match is found, keep the original name and frequency
        if not matched:
            if name in brand_frequencies:
                brand_frequencies[name] += frequency
            else:
                brand_frequencies[name] = frequency

    # Convert the brand frequencies dictionary to a DataFrame
    result_data = pd.DataFrame(list(brand_frequencies.items()), columns=['name', 'frequency'])

    return result_data

# Apply the function to merge brand names
cleaned_data = merge_brand_names(data, known_brands)

# Save the cleaned data to a new CSV file
cleaned_file_path = 'cleaned_filtered_data222.csv'
cleaned_data.to_csv(cleaned_file_path, index=False)

cleaned_file_path