# Property Management System

## Overview

This comprehensive Property Management System is designed for efficient handling of property listings through a robust backend and an intuitive frontend. The backend, developed in Python, interacts with MongoDB to manage property data. The frontend, powered by Streamlit, offers a user-friendly web interface for streamlined property management tasks.

## Accessing the Web Application

The Property Management System web application can be accessed through the link: [Property Management System Web Application](https://dsci551databasemanagementsystem-kieuh8yc2yx9czf5nah4b9.streamlit.app/). This allows for direct interaction with the system via a web browser.

## Backend (Python) – `backend_v11.py`

### Features Include:

- **Database Initialization**: Prepares the database by creating necessary indexes to optimize query performance.
- **Property Insertion**: Allows for the insertion of new property listings into the database, with input validation to ensure data integrity.
- **Property Searching**: Supports searching for properties based on criteria such as city, state, type, and custom identifiers, with optional sorting by price.
- **Property Updating**: Enables updating existing property listings by specifying the property's custom identifier and the fields to be updated.
- **Property Deletion**: Allows for the deletion of property listings from the database using the property's custom identifier.
- **Export Functionality**: Provides the ability to export search results into CSV or JSON formats for external use or analysis.
- **Interactive Mode**: Offers an interactive mode for insert, search, update, and delete operations, guiding users through the process with prompts.

### Usage Instructions
#### Change to the directory where `backend_v11.py` is saved and run the following commands:

#### Command-Line Interface Example
- **Initialize Database**: `python backend_v11.py --init`
- **Insert a Property**: `python backend_v11.py --operation insert --address "456 University Dr" --city "Irvine" --state "California" --zip_code 92612 --price 1500000 --bedrooms 3 --bathrooms 2.5 --square_footage 2000 --type "sale" --date_listed "2024-02-15" --description "Spacious family home" --images "image1.jpg" "image2.jpg" "image3.jpg"`
- **Search for Properties**: `python backend_v11.py --operation search --city "Irvine" --type "sale"`
- **Update a Property**: `python backend_v11.py --operation update --custom_id "CAL-IRVI-456" --updates "bedrooms=4" "bathrooms=2.5" "price=675000"`
- **Delete a Property**: `python backend_v11.py --operation delete --custom_id "CAL-IRVI-456"`

#### Interactive Interface Example

- **Interactive Insert**: `python backend_v11.py --operation interactive_insert`
- **Interactive Search**: `python backend_v11.py --operation interactive_search`
- **Interactive Update**: `python backend_v11.py --operation interactive_update`
- **Interactive Delete**: `python backend_v11.py --operation interactive_delete`

#### Function Descriptions

#### Database and Initialization Functions
- **`check_connection`**: Ensures MongoDB connectivity.
- **`initialize_indexes`**: Sets up indexes for improved query performance.

#### Property Management Functions
- **`create_custom_id`**, **`get_database`**: Manage property identification and database allocation.
- **`validate_property_data`**: Confirms property data matches schema requirements.
- **`property_already_exists`**, **`duplicate_property`**, **`insert_property`**, **`search_property`**, **`update_property`**, **`delete_property`**: Facilitate CRUD operations on property listings.

#### Export Functions
- **`export_to_csv`**, **`export_to_json`**: Allow for exporting property data to CSV or JSON formats.

#### Utility and Helper Functions
- **`prompt_for_property_data`** through **`delete_property_interactive`**: Support interactive command-line operations for property management.

## Frontend (Streamlit) – `frontend_v11.py`

### Usage Instructions

Change to the directory where `frontend_v11.py` is saved and run the frontend application by executing:

`streamlit run frontend_v11.py`

### Function Descriptions

#### Authentication Functions
- **`hash_password`**, **`insert_new_user`**: Handle user password security and registration.
- **`login_ui`**, **`registration_ui`**: Render and manage login and registration interfaces.

#### Image Handling Functions
- **`image_to_base64`**, **`convert_image_to_base64`**: Convert and process images for web display.
- **`display_image_in_base64`**: Show property images within the web application.

#### UI Components
- **`display_logo`**: Presents the system's logo and branding.
- **`add_property_ui`**, **`search_property_ui`**, **`update_property_ui`**, **`delete_property_ui`**: Offer web-based forms and interfaces for managing property listings.

#### Export to CSV or JSON
- **`Download CSV` & `Download JSON` buttons**: Allow user to download search results in JSON or CSV format.
