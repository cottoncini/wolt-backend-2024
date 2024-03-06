# wolt-backend-2024
Assignment for Wolt backend internship 2024

## Rationale
I completed the assignment in Python, using FastAPI due to its feature set and ease of use compared to, e.g., Flask.
I adopted the folder structure of a conventional backend app despite its simplicity, with the single POST endpoint in `app/routers` and a dummy GET root endpoint in `app/main.py`.

Constants needed to compute the delivery fee are placed in a separate module `app/constants.py`.
In a production environment, I expect the module import to be replaced by some suitable container, populated from a database or the environment at runtime.

Cart data model, fee functions and related tests are built under the assumption that the inputs `cart_value`, `delivery_distance` and `number_of_items` are always positive.

## Installation
All dependencies are listed in `requirements.txt` and can be installed in a new virtual environment as follows:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage
The app can be run with any ASGI HTTP server.
For example the server `uvicorn` can be setup by running:
```bash
pip install uvicorn
uvicorn app.main:app
```
`curl` can be used to send a sample API request to the `/delivery-fee` endpoint.
Sending the cart provided with the original prompt:
```bash
curl -H "Content-Type: application/json" -d '{"time": "2024-01-15T13:00:00Z", "cart_value": 790, "delivery_distance": 2235, "number_of_items": 4}' http://localhost:8000/delivery-fee
```
will return:
```json
{"delivery_fee":710}
```

## Testing
The full test suite can be run as follows:
```bash
pytest
```
