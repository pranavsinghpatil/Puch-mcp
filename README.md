# Tarri Food puch 🍲

A web application for exploring and discovering delicious recipes from the Indian subcontinent. Get recommendations based on your taste!

## Features

*   Browse through a wide variety of recipes.
*   Get detailed information for each recipe, including ingredients and instructions.
*   Smart recipe recommendations.
*   Find recipes popular in your locality.

## Getting Started

### Prerequisites

*   Python 3.11+
*   pip

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/Puch-mcp.git
    cd Puch-mcp
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv .tarri
    source .tarri/bin/activate  # On Windows, use `.tarri\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Prepare the data:**
    The initial dataset needs to be processed. Make sure `raw.csv` is present in the `app/data` directory.
    ```bash
    python app/data/data_prep.py
    ```
    This will create the `recipes.csv` file used by the application.

5.  **Run the application:**
    ```bash
    uvicorn app.main:app --reload
    ```
    The application will be available at `http://127.0.0.1:8000`.

## API Endpoints

The following endpoints are available:

*   `GET /`: Welcome message.
*   `GET /recipes`: Get a list of all recipes.
*   `GET /recipes/{recipe_id}`: Get details for a specific recipe.
*   `GET /recommend/{recipe_id}`: Get recipe recommendations based on a given recipe.
*   `GET /locality/{locality_name}`: Get recipes popular in a specific locality.

## Project Structure

```
desi-food-puch/
├── app/
│   ├── controllers/      # Business logic for handling requests
│   ├── data/             # Data files and data preparation script
│   ├── routes/           # API route definitions
│   ├── services/         # Services for business logic (e.g., recommendations)
│   ├── tests/            # Application tests
│   ├── utils/            # Utility functions
│   └── main.py           # Main FastAPI application entry point
├── .tarri/               # Python virtual environment
├── alt/                  # Alternative backend implementation (Node.js)
├── requirements.txt      # Python dependencies
├── .gitignore
└── README.md
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
