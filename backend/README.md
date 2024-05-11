## Local Usage

1. Install the dependencies for the Poetry server:
   ```shell
   poetry install --no-root
   ```
2. Start the Poetry server:
   ```shell
   poetry run flask --app brewbucks run --host 0.0.0.0 --port 8080
   ```

## Docker Image
- Flask runs on port 80