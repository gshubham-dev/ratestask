## Ratestask API

## Introduction

The Ratestask API is an implementation of the [Xeneta ratestask](https://github.com/xeneta/ratestask) project.

## Setup Instructions

### I. Initial Setup: Docker

You can execute the provided Dockerfile by running:

```bash
docker build -t ratestask .
```

This will create a container with the name *ratestask*, which you can
start in the following way:

```bash
docker run -p 0.0.0.0:5432:5432 --name ratestask ratestask
```

You can connect to the exposed Postgres instance on the Docker host IP address,
usually *127.0.0.1* or *172.17.0.1*. It is started with the default user `postgres` and `ratestask` password.

```bash
PGPASSWORD=ratestask psql -h 127.0.0.1 -U postgres
```

alternatively, use `docker exec` if you do not have `psql` installed:

```bash
docker exec -e PGPASSWORD=ratestask -it ratestask psql -U postgres
```
### II. Application Setup to run application

Once your Docker container is running and you have verified that PostgreSQL is accessible, follow below steps to set up and run the Flask application:

#### 1. Clone the Repository

```bash
git clone https://github.com/gshubham-dev/ratestask.git
cd ratestask
```

#### 2. Create a Virtual Environment
Create a virtual environment to manage dependencies:

`macOS/Linux:`

```bash
source venv/bin/activate
```

` Windows:`

```bash
venv\Scripts\activate
```

#### 3. Install Dependencies
Install the required Python packages using `pip`:

```bash
pip install -r requirements.txt
```

#### 4. Run the Application
Start the Flask application:

```bash
flask run
```
or
```bash
python run.py
```


#### 5. Access the API

You can access the API using the following URL:

* http://127.0.0.1:5000
* 
### Fetching Rates

#### Example 1:

Example requests:

1. Using region codes:
   ```bash
   curl --location 'http://127.0.0.1:5000/rates?date_from=2016-01-01&date_to=2016-01-10&origin=china_main&destination=north_europe_main'
   ```

2. Using port codes:
   ```bash
   curl --location 'http://127.0.0.1:5000/rates?date_from=2016-01-10&date_to=2017-01-11&origin=CNSGH&destination=IEDUB'
   ```

## Tests

To run the unit tests, execute the following command:

```bash
pytest
```

## <p style='color:green'>🎯 Key Design Decisions.</p>

### 1. Average Price Calculation:
- The **average price** between the origin and destination ports can result in several decimal places. To ensure clarity, the price is **rounded** to **two** **decimal** places, balancing precision with readability, rather than rounding to a whole number.

### 2. Handling Invalid Origin and Destination:
- Instead of returning an **error** for **invalid** origin or destination inputs, the solution returns an **empty** **response**. This design choice enhances user experience by allowing easy correction of input errors while ensuring smooth operation without compromising data integrity.

### 3. Handling of Missing Days in Price Calculation:
- The `calculate_average_prices` method calculates average prices for days that have corresponding records in the **prices** table. If a specific day within the requested date range lacks any records, that day will not be included in the final results. This ensures that the average price calculation only reflects days where at **least** **one** **price** record exists, following written SQL's behavior.

## Total Time Spent
The development of this project was accomplished in an estimated duration of 4 hours 20 min.
Thank You !!