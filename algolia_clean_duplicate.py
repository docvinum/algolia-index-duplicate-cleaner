import algoliasearch
from algoliasearch.search_client import SearchClient
from datetime import datetime
import json
import os

def get_user_input(prompt):
    while True:
        user_input = input(prompt)
        if user_input.strip():
            return user_input
        else:
            print("Input cannot be empty. Please try again.")

# Prompt the user for necessary Algolia account information
application_id = get_user_input("Enter your Algolia Application ID: ")
admin_api_key = get_user_input("Enter your Algolia Admin API Key: ")

# Initialize the Algolia client and index
client = None
algolia_index = None
while True:
    try:
        if not client:
            client = SearchClient.create(application_id, admin_api_key)
        index_name = get_user_input("Enter the name of your Algolia index: ")
        algolia_index = client.init_index(index_name)
        # Test retrieval to confirm if the index is valid
        algolia_index.search('')
        break
    except algoliasearch.exceptions.RequestException as e:
        print("An error occurred: ", e)
        print("Please enter a valid index name.")

# Retrieve data from the index
records = algolia_index.browse_objects({'query': ''})

# Sort and identify duplicates
sorted_records = {}
duplicates = []

for record in records:
    url = record['url']
    date_scraping_str = record['date_scraping']
    date_scraping = datetime.strptime(date_scraping_str, "%m/%d/%Y, %H:%M:%S")
    
    if url in sorted_records and date_scraping <= datetime.strptime(sorted_records[url]['date_scraping'], "%m/%d/%Y, %H:%M:%S"):
        duplicates.append(record)
    elif url in sorted_records:
        duplicates.append(sorted_records[url])
        sorted_records[url] = record
    else:
        sorted_records[url] = record

# Display the number of duplicates found
print(f"{len(duplicates)} duplicates found.")

# Ask user if they want to see the first 10 duplicates
see_duplicates = get_user_input("Do you want to see the first 10 duplicates? (yes/no): ").lower()
index = 0

while see_duplicates == 'yes' and index < len(duplicates):
    # Display next 10 duplicates
    for dup in duplicates[index:index+10]:
        print("-\nobjectID: {}\nURL: {}\nTitle: {}\nDate Scraping: {}\n-".format(
            dup['objectID'], dup['url'], dup.get('title', 'N/A'), dup['date_scraping']))
    index += 10

    # Ask user if they want to see the next 10 duplicates
    if index < len(duplicates):
        see_next = get_user_input(f"Do you want to see the next 10 duplicates? ({index} shown so far) (yes/no): ").lower()
        if see_next != 'yes':
            break

# Offer to save a copy of the index and the duplicates to JSON
save_choice = input("Do you want to save a copy of the index and duplicates to JSON? (yes/no): ")
if save_choice.lower() == 'yes':
    if not os.path.exists('algolia_backup'):
        os.makedirs('algolia_backup')
    with open('algolia_backup/index_backup.json', 'w') as f_index:
        json.dump(list(records), f_index)
    with open('algolia_backup/duplicates_backup.json', 'w') as f_duplicates:
        json.dump(duplicates, f_duplicates)
    print("Backups saved in the 'algolia_backup' folder.")

# Confirm before deleting duplicates
confirm_delete = input("Do you want to delete the duplicates from the index? (yes/no): ")
if confirm_delete.lower() == 'yes':
    duplicates_object_ids = [dup['objectID'] for dup in duplicates]
    algolia_index.delete_objects(duplicates_object_ids)
    print("Duplicates have been deleted from the index.")
else:
    print("No changes have been made to the index.")
