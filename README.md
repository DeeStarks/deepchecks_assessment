# Deepchecks Backend Assessment

## System Design

The system is designed to log interactions with a Large Language Model (LLM), calculate metrics on these interactions, and alert the user when certain conditions are met based on these metrics.

It follows the Hexagonal Architecture pattern, where the core business logic is decoupled from the infrastructure. The system consists of the following components:

1. **Data Ingestion**: This component is responsible for ingesting data from the LLM. The data ingestion component is implemented using a REST API that accepts POST requests with the interaction data.
2. **Data Processing**: This component is responsible for processing the interaction data and calculating metrics. The data processing component is implemented using a background worker that processes the interaction data asynchronously.

> For the purpose of this assessment, no alerting system was implemented. Instead, there is a REST API endpoint that allows the user to query the alerts logged in the database by the data processing component.

## Implementation

The system is implemented using Python and the following libraries:

1. **FastAPI**: For building the REST API for data ingestion.
2. **SQLAlchemy**: For interacting with the database.
3. **Negotium**: A personally developed library for handling background tasks. It is similar to Celery but simpler. Unlike Celery, it does not require separately running workers. Instead, it uses threads to run tasks in the main application process.

## Solution Overview

### Logging Interactions
1. Input and Output Storage:
    - Interactions are logged via the `/log` endpoint.
    - Each interaction consists of an input and output string.
2. Database Schema:
    - `Interaction`: Stores the raw input and output.
    - `Metric`: Stores metric values related to each interaction.
    - `Alert`: Stores alert details, including type and triggered value.
3. Background Task:
    - A background task processes interactions asynchronously.
    - The task calculates metrics and checks for alerts.
    - The task is triggered when an interactions CSV file is uploaded via the `/log` endpoint.

### Metric Calculation
1. Flexible Metric Calculation:
    - Implemented a base class `MetricCalculator` to allow for easy addition of new metrics.
    - Example metric `LengthMetric` calculates the length of input and output strings.
2. Calculation Flow:
    - When an interaction is logged, metrics are calculated for both the input and output.
    - Metric values are stored in the `Metric` table.

### Alerts
1. Threshold Alert:
    - **Implementation**: `ThresholdAlert` class checks if a metric value exceeds a predefined threshold.
    - **Use Case**: Trigger alerts for unusually long or short texts.
    - **Example**: Threshold set at 100 characters for `high` and 10 characters for `low`.
2. Outlier Alert:
    - **Implementation**: `OutlierAlert` class checks if a metric value is significantly different from the average.
    - **Use Case**: Detect values that deviate from the norm.
    - **Approach**:
        - Calculate the mean and standard deviation of all metric values.
        - Trigger an alert if a value is more than or less than 2 standard deviations away from the mean.
3. Storing Alerts:
    - Alerts are stored in the `Alert` table with details about the interaction and metric value that triggered the alert.

### API Endpoints
1. `POST /interactions`:
    - **Function**: Logs new interactions from a CSV file, calculates metrics, and checks for alerts.
    - **Flow**:
        - Reads the CSV file.
        - Sends the results to the background task for processing.
            - Stores the interaction in the database.
            - Calculates metrics for input and output.
            - Checks for threshold and outlier alerts.
            - Stores any triggered alerts.
        - Returns a success message.
2. `GET /alerts`:
    - **Function**: Retrieves all stored alerts.
    - **Flow**:
        - Queries the `Alert` table.
        - Returns a list of alerts with details. Allowed parameters for filtering: `interaction_id`, `interaction_type`, `alert_type`.

## Usage

> - SQLite is used as the database for this system. So, no additional setup is required for the database.
> - For the background tasks, a Redis server is required. You can run a Redis server using Docker with the following command:
>
>   ```bash
>   docker run -d -p 6379:6379 redis
>   ```

To run the system, follow these steps:

1. Copy the contents of the `.env.example` file to a new file named `.env` and set the environment variables if using different values from the example.
2. Create and activate a virtual environment using `virtualenv`, `pipenv`, or any other tool of your choice.
3. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```
4. Run the FastAPI application:

   ```bash
    uvicorn main:app --reload
    ```

The FastAPI application will start running on `http://localhost:8000`. You can access the Swagger UI at `http://localhost:8000/docs` to interact with the API.
