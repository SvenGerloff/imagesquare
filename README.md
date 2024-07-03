# Square Product Images

Welcome to the Square Product Images app! This app allows you to process images into a square format, centered with a white background.

## Installation

To install the necessary dependencies, follow these steps:

1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```
2. **Recommended** Create a virtual environment and activate it:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\\Scripts\\activate`
    ```
3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

There are different versions of the Streamlit app, based on the limitations of Streamlit's Community Cloud. The app **streamlit_app.py** is used for the cloud deployment.

- `app.py` -> Uses ImageMagick, but was not compatible with the cloud.
- `streamlit_app_styled.py` -> Uses the library streamlit_extras, which is also not compatible with the cloud.

### Locally
To run the app locally, use:
```bash
streamlit run streamlit_app.py
```

### Community Cloud

1. Go to [Streamlit Community Cloud](https://streamlit.io/cloud) and sign in.
2. Create a new app and link it to your GitHub repository.
3. Configure the app by selecting the main script file to run (streamlit_app.py)
4. Deploy the app and share the URL. (Hint: you can modify the URL)



