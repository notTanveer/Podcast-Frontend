# Podcast Frontend
This is the frontend of the Podcast Website which generates a summary of podcast with the help of RSS feed.

---

## Getting Started

1. Clone the repository to your local machine:
   ```sh
   git clone https://github.com/notTanveer/Podcast-Frontend.git
   cd Podcast-Frontend
2. Install the required Python packages. You can use a virtual environment or your preferred package manager:
    ```sh
    pip install -r requirements.txt

3. Run the streamlit app:
   ```sh
   streamlit run app.py

4. The app will open in your browser. You can interact with the app to view existing podcast details and process new podcast feeds

## Dependencies

- Python 3.6+
- Streamlit
- Modal (for cloud function invocation)

## Cloud Function

The app utilizes a cloud function called `process_podcast` to process podcast feed URLs and retrieve podcast information. This function is available in the "corise-podcast-project" project.

## Credits

This app was created by Tanveer Ansari. It uses Streamlit for the web interface and Modal for cloud function invocation.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
