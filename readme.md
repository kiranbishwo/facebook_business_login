# Facebook Business Login

This project is a web application that integrates Facebook Business Login using Flask. It provides a simple interface for users to log in using their Facebook credentials.

## Installation

### Prerequisites

- Python 3.9 or higher
- Virtual environment (optional but recommended)
- facebook app credencial (FACEBOOK_APP_ID,FACEBOOK_APP_SECRET)

### Steps

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/facebook_business_login.git
    cd facebook_business_login
    ```

2. Create a virtual environment (optional but recommended):

    ```sh
    python -m venv venv
    ```

3. Activate the virtual environment:

    - On Windows:

        ```sh
        .\venv\Scripts\activate
        ```

    - On macOS/Linux:

        ```sh
        source venv/bin/activate
        ```

4. Install the required dependencies:

    ```sh
    pip install -r requirements.txt
    ```

5. Run the application:

    ```sh
    python app.py
    ```

6. Open your browser and navigate to `http://127.0.0.1:5000` to see the application in action.

## About

This project uses the following technologies:

- **Flask**: A lightweight WSGI web application framework.
- **Jinja2**: A fast, expressive, extensible templating engine for Python.
- **Facebook SDK**: For integrating Facebook login functionality.

### Project Structure
