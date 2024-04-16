import streamlit as st
import base64
from bson import ObjectId
from backend_v11 import insert_property, search_property, update_property, delete_property
from PIL import Image
import bcrypt
from io import BytesIO
from pymongo import MongoClient
import pandas as pd
import json
import io


# Constants for the states list and file types for images
STATES_LIST = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware",
    "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky",
    "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri",
    "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York",
    "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island",
    "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington",
    "West Virginia", "Wisconsin", "Wyoming"
]
ACCEPTED_IMAGE_TYPES = ['jpg', 'png']


# MongoDB connection setup
MONGO_URI = 'mongodb+srv://nguyenlamvu88:Keepyou0ut99!!@cluster0.ymo3tge.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(MONGO_URI)

# Database and collection names
db = client['authentication']
users_collection = db['login_info']


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def insert_new_user(username, hashed_password):
    try:
        existing_user = users_collection.find_one({"username": username})
        if existing_user:
            st.error("Username already exists. Please choose a different username.")
            return False

        result = users_collection.insert_one({"username": username, "hashed_password": hashed_password})
        if result.inserted_id:
            return True
        else:
            st.error("Failed to insert new user.")
            return False
    except Exception as e:
        st.error(f"Exception occurred while registering user: {e}")
        return False


def login_ui():
    st.sidebar.subheader("Login")
    username = st.sidebar.text_input("Username", key="login_username")
    password = st.sidebar.text_input("Password", type="password", key="login_password")
    if st.sidebar.button("Login"):
        user_info = users_collection.find_one({"username": username})
        if user_info and bcrypt.checkpw(password.encode('utf-8'), user_info['hashed_password']):
            st.session_state["authenticated"] = True
            st.sidebar.success("You are logged in.")
            st.experimental_rerun()
        else:
            st.sidebar.error("Incorrect username or password.")


def registration_ui():
    st.sidebar.subheader("Register New Account")
    with st.sidebar.form("registration_form"):
        new_username = st.text_input("New Username", key="new_username_reg")
        new_password = st.text_input("New Password", type="password", key="new_password_reg")
        submit_button = st.form_submit_button("Register")

        if submit_button:
            if new_username and new_password:
                hashed_password = hash_password(new_password)
                if insert_new_user(new_username, hashed_password):
                    st.sidebar.success("User registered successfully.")
                else:
                    st.sidebar.error("Registration failed. Username might already exist.")
            else:
                st.sidebar.error("Username and password cannot be empty.")


def image_to_base64(image_path):
    """
    Convert an image file to a base64 string.
    """
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    except Exception as e:
        st.error(f"Error reading image file: {e}")
        return None


def display_logo(url: str):
    """
    Display the company logo and title in the Streamlit app using an image URL.
    """
    # Use the URL directly in the img src attribute
    logo_html = f"<img src='{url}' class='img-fluid' width='350'>"
    st.markdown(f"""
        <div style="display: flex; align-items: center;">
            {logo_html}
            <h1 style="margin: 0 0 0 50px;">Majestic Real Estate Management</h1>
        </div>
        <div class="space"></div>
        """, unsafe_allow_html=True)


def convert_image_to_base64(uploaded_image, size=(600, 400)):
    """
    Convert an uploaded image to a base64 string for storage.
    """
    try:
        # Extract file extension from filename and normalize to uppercase
        filename = uploaded_image.name
        file_extension = filename.split(".")[-1].lower()  # Ensure extension is in lowercase
        if file_extension not in ['jpg', 'png']:
            raise ValueError("Invalid file type")

        # Open the uploaded image with PIL
        image = Image.open(uploaded_image)

        # Resize the image
        resized_image = image.resize(size)

        # Save the resized image to a buffer, specifying format explicitly
        buffer = BytesIO()
        format = 'JPEG' if file_extension == 'jpg' else file_extension.upper()
        resized_image.save(buffer, format=format)  # Use explicit format
        buffer.seek(0)

        # Convert the image in the buffer to a base64 string
        b64_encoded = base64.b64encode(buffer.read()).decode()

        return f"data:image/{file_extension};base64,{b64_encoded}"
    except Exception as e:
        st.error(f"An error occurred while converting image to base64: {e}")
        return None


def display_image_in_base64(base64_string):
    st.markdown(
        f"<img src='{base64_string}' class='img-fluid'>", unsafe_allow_html=True
    )


def add_property_ui():
    """
    UI for adding a new property.
    """
    st.subheader("🏡 Add a New Property")
    with st.form(key='add_property_form'):
        col1, col2 = st.columns(2)
        with col1:
            address = st.text_input("Address")
            city = st.text_input("City")
            state = st.selectbox("State", STATES_LIST)
            zip_code = st.text_input("ZIP Code")
        with col2:
            price = st.number_input("Price ($)", min_value=0, value=150000, step=50000, format="%d")
            bedrooms = st.number_input("Bedrooms", min_value=0, value=3, step=1)
            bathrooms = st.number_input("Bathrooms", min_value=0.0, value=2.0, step=0.5)
            square_footage = st.number_input("Square Footage", min_value=0, value=1000, step=100)
        property_type = st.selectbox("Type", ["Sale", "Rent"])
        date_listed = st.date_input("Date Listed")
        description = st.text_area("Description")
        uploaded_images = st.file_uploader("Upload Property Images", accept_multiple_files=True,
                                           type=ACCEPTED_IMAGE_TYPES)
        submit_button = st.form_submit_button(label='Add Property')

        if submit_button:
            image_strings = [convert_image_to_base64(image) for image in uploaded_images] if uploaded_images else []
            property_data = {
                "address": address,
                "city": city,
                "state": state,
                "zip_code": int(zip_code) if zip_code.isdigit() else 0,
                "price": price,
                "bedrooms": bedrooms,
                "bathrooms": bathrooms,
                "square_footage": square_footage,
                "type": property_type.lower(),
                "date_listed": str(date_listed),
                "description": description,
                "images": image_strings
            }
            try:
                success = insert_property(property_data)
                if success:
                    st.success("Property added successfully!")
                else:
                    st.error("Failed to add property. Please check the input data.")
            except Exception as e:
                st.error(f"An error occurred: {e}")


# Custom JSON Encoder to handle MongoDB ObjectId
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)  # Convert ObjectId to string
        return json.JSONEncoder.default(self, o)


def display_image(data):
    """Display an image from a URL or base64 string."""
    if isinstance(data, str):
        if data.startswith('http'):  # URL
            st.image(data, use_column_width=True)
        elif data.startswith('data:image'):  # Base64
            base64_str = data.split(',')[1]
            image_data = base64.b64decode(base64_str)
            image = Image.open(io.BytesIO(image_data))
            st.image(image, use_column_width=True)


def search_property_ui():
    st.subheader("🔍 Search for Properties")
    with st.form("search_form"):
        city = st.text_input("City", help="partial match allowed, case-insensitive")
        state = st.text_input("State", help="partial match allowed, case-insensitive")
        property_type = st.text_input("Type", help="sale or rent, case-insensitive")
        address = st.text_input("Address", help="partial match allowed, case-insensitive")
        custom_id = st.text_input("Custom ID")
        sort_by_price = st.selectbox("Sort by Price", ["None", "Ascending", "Descending"], index=0)

        submit = st.form_submit_button("Search")

    if submit:
        sort_option = 'asc' if sort_by_price == "Ascending" else 'desc' if sort_by_price == "Descending" else None
        search_results = search_property(city=city, state=state, property_type=property_type.lower(), address=address, custom_id=custom_id, sort_by_price=sort_option)
        unique_properties = {prop['custom_id']: prop for prop in search_results}
        unique_search_results = list(unique_properties.values())

        if unique_search_results:
            st.success(f"Found {len(unique_search_results)} unique properties.")
            for property in unique_search_results:
                with st.expander(f"{property.get('address', 'No Address Provided')}"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.markdown(f"**Property ID:** `{property.get('custom_id')}`")
                        st.markdown(f"**City:** {property.get('city', 'N/A')}")
                        st.markdown(f"**State:** {property.get('state', 'N/A')}")
                    with col2:
                        st.markdown(f"**Price:** `${property.get('price', 'N/A')}`", unsafe_allow_html=True)
                        st.markdown(f"**Bedrooms:** {property.get('bedrooms', 'N/A')}")
                        st.markdown(f"**Bathrooms:** {property.get('bathrooms', 'N/A')}")
                    with col3:
                        st.markdown(f"**Square Footage:** {property.get('square_footage', 'N/A')}")
                        st.markdown(f"**Type:** {property.get('type', 'N/A')}")
                        st.markdown(f"**Listed Date:** {property.get('date_listed', 'N/A')}")

                    st.markdown(f"**Description:** {property.get('description', 'N/A')}")
                    images = property.get('images', [])
                    if images:
                        for img in images:
                            display_image(img)

            # Global download buttons for all search results
            json_data = json.dumps(unique_search_results, indent=4, cls=JSONEncoder).encode('utf-8')
            df = pd.DataFrame(unique_search_results).drop(columns=['images'], errors='ignore')
            csv_data = df.to_csv(index=False).encode('utf-8')

            st.download_button("Download JSON", json_data, "search_results.json", "application/json", key='download-json')
            st.download_button("Download CSV", csv_data, "search_results.csv", "text/csv", key='download-csv')
        else:
            st.warning("No properties found matching the criteria.")


def update_property_ui():
    """
    UI for updating property details with all input fields displayed.
    """
    st.subheader("✏️ Update Property Details")

    with st.form(key='update_property_form'):
        custom_id = st.text_input("Property Custom ID")

        # Display input fields for all updateable properties
        price = st.number_input("New Price ($)", format="%d", step=25000, key="price")  # Step enforces integer increments
        bedrooms = st.number_input("New Bedrooms", format="%d", step=1, key="bedrooms")  # Step enforces integer increments
        bathrooms = st.number_input("New Bathrooms", format="%f", step=0.5, key="bathrooms")  # Bathrooms can often be a float
        square_footage = st.number_input("New Square Footage", format="%d", step=100, key="square_footage")  # Step enforces integer increments
        listed_date = st.date_input("New Listed Date", key="listed_date")
        prop_type = st.selectbox("New Type", ["Sale", "Rent"], key="type")
        description = st.text_input("New Description", key="description")

        submit_update = st.form_submit_button(label='Update Property')

        if submit_update:
            # Collect updates into a dictionary, ignoring empty fields
            update_data = {}
            if price > 0: update_data['price'] = price
            if bedrooms > 0: update_data['bedrooms'] = bedrooms
            if bathrooms > 0: update_data['bathrooms'] = bathrooms
            if square_footage > 0: update_data['square_footage'] = square_footage
            if listed_date: update_data['listed_date'] = listed_date.strftime("%Y-%m-%d")
            if prop_type: update_data['type'] = prop_type.lower()
            if description: update_data['description'] = description

            # Ensure there's at least one field to update
            if update_data:
                success = update_property(custom_id, update_data)
                if success:
                    st.success("Property updated successfully!")
                else:
                    st.error("Failed to update property. Please check the input data and Custom ID.")
            else:
                st.error("No updates specified. Please fill in at least one field to update.")


def delete_property_ui():
    """
    UI for deleting a property.
    """
    st.subheader("🗑️ Delete a Property")
    with st.form(key='delete_property_form'):
        custom_id = st.text_input("Property Custom ID to Delete")
        submit_delete = st.form_submit_button(label='Delete Property')

        if submit_delete:
            confirm_delete = st.checkbox("I confirm that I want to delete this property", value=False)
            if confirm_delete:
                success = delete_property(custom_id)
                if success:
                    st.success("Property deleted successfully!")
                else:
                    st.error("Failed to delete property. Please check the Custom ID.")
            else:
                st.warning("Please confirm the deletion.")


def logout_ui():
    if st.sidebar.button('Logout'):
        # Clear all items in the session state
        keys = list(st.session_state.keys())
        for key in keys:
            del st.session_state[key]
        st.sidebar.success("You have been logged out.")
        st.experimental_rerun()  # Rerun the app to reflect logged out state


def main():
    # Safely check if the user is authenticated, defaulting to False if the key doesn't exist
    is_authenticated = st.session_state.get("authenticated", False)

    logo_url = "https://nguyenlamvu88.github.io/dsci551_data_base_management_system/landing_page_image.png"
    display_logo(logo_url)

    if is_authenticated:
        # User is authenticated, show property management operations
        st.sidebar.title("🏠 Property Management")
        operation = st.sidebar.selectbox("Choose Operation",
                                         ["Add Property", "Search Property", "Update Property", "Delete Property"])

        # Save the current operation to session state
        st.session_state['current_operation'] = operation

        if operation == "Add Property":
            add_property_ui()
        elif operation == "Search Property":
            search_results = search_property_ui()  # Modify this function to return search results
            st.session_state['search_results'] = search_results  # Store search results in session state
        elif operation == "Update Property":
            update_property_ui()
        elif operation == "Delete Property":
            delete_property_ui()

        logout_ui()  # Call the logout UI function

    else:
        # User is not authenticated, show login and optionally registration UI
        login_ui()

        registration_ui()


if __name__ == "__main__":
    main()
