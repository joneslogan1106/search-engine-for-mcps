# search-engine-for-mcps
This repo will kinda be like a google for finding Open-MCP servers, which have tools for different LLM(s) which can make them interactive.
It will be a search engine for Open-MCP servers, allowing users to find and interact with various tools and applications built on the MCP framework.
NOTE: The flask app must be ran from the project root, In the backend, You can cache everything, but searching from the command line will not work, because it is implemented for the flask app.
## Features
- Search for Open-MCP servers by name, description, or tags.
- View details about each server, including available tools and applications.
- Interact with tools directly from the search results.
- Bookmark favorite servers for quick access.
- User-friendly interface for easy navigation and search.
## Technologies Used
- Frontend: Flask, HTML, CSS, JavaScript
- Backend: Python, Flask
## Installation
1. Clone the repository:
    ```bash
    git clone
    pip install -r requirements.txt
    ```
2. Navigate to the project directory:
    ```bash
    cd search-engine-for-mcps
    ```
3. Run the Flask application:
    ```bash
    python app.py
    ```
4. Open your web browser and go to `http://localhost:5000` to access the search engine.
## Usage
- Use the search bar to find Open-MCP servers by entering keywords related to the server name, description, or tags.
- Click on a server to view its details and available tools.
- Interact with tools directly from the server details page.
- Bookmark your favorite servers for easy access later.
## Contributing
Contributions are welcome! If you have suggestions for improvements or new features, please open an issue or submit a pull request.
1. Fork the repository.
2. Create a new branch for your feature or bug fix:
    ```bash
    git checkout -b feature/your-feature-name
    ```
3. Make your changes and commit them
    ```bash
    git commit -m "Add your changes here"
    ```
4. Push to the branch:
    ```bash
    git push origin feature/your-feature-name
    ```
5. Open a pull request to the main branch of the original repository.
## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
## Acknowledgements
- Thanks to the Open-MCP community for their contributions and support.
- Inspired by the need for a centralized platform to discover and interact with Open-MCP servers.