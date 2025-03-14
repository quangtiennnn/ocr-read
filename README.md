# My Python API

This project is a simple API built with Flask that demonstrates how to manage environment variables and set up a basic structure for an API.

## Project Structure

```
my-python-api
├── src
│   ├── app.py
│   ├── controllers
│   │   └── __init__.py
│   ├── routes
│   │   └── __init__.py
│   └── models
│       └── __init__.py
├── .env
├── requirements.txt
└── README.md
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd my-python-api
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the root directory and add your API key:
   ```
   API_KEY=your_api_key_here
   ```

## Usage

To run the application, execute the following command:
```
python src/app.py
```

The API will be available at `http://localhost:5000`.

## Contributing

Feel free to submit issues or pull requests for improvements or bug fixes.