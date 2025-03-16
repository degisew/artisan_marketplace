# artisan_marketplace
[Demo Video](https://drive.google.com/file/d/1znR4-meb7l4p-u2yoqN8uRtqw3A_SUTQ/view?usp=sharing)
## Prerequisites

Ensure the following tools are installed on your machine before proceeding:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Git](https://git-scm.com/)

## Getting Started

Follow these instructions to get the project up and running on your local machine.

### 1. Clone the Repository

```bash
git clone https://github.com/degisew/artisan_marketplace.git
cd artisan_marketplace
```

## Project Structure

```bash
├── apps/                 # Custom Apps collection
├── config/               # Project Configurations
│     └── settings/       # Project settings for dev,test, and prod environment
├── docker
│     └── dev/          
│          └── Dockerfile # Django API Dockerfile for development environment
├── docs/                 # Documentation files
├── scripts/              # Custom scripts
├── .env                  # Environment variables (you will create this)
├── compose.yaml          # Docker Compose configuration file
└── README.md             # This README file
```

### 2. Create a `.env` File

Create a `.env` file in the root of your project directory. This file will contain environment variables for the database and pgAdmin4. Here's an example `.env` file:

```bash
# pgAdmin4
PGADMIN_DEFAULT_EMAIL=admin@example.com
PGADMIN_DEFAULT_PASSWORD=<your-pgadmin-password>
```

Make sure to replace `<your-pgadmin-password>` with strong, secure values.

### 3. Build and Run the Containers

Use Docker Compose to build and spin up the containers:

```bash
docker-compose up --build
```

This command will build and run the containers for:

- **PostgreSQL** (as the database backend)
- **pgAdmin4** (to manage the PostgreSQL database)
- **Django application** (the API server)

### 4. Apply Migrations

Once you start the container, you should run the following command to apply all database migrations.

```bash
docker-compose exec api python manage.py migrate
```

This command will apply migrations and setup your database tables.

### 5. Create a superuser to access the Django admin

To create a super user, run the below command and follow the instructions.

```bash
docker-compose exec api python manage.py createsuperuser
```

for example, yu can use the following credentials:

- email: <admin@gmail.com>
- password: 1234

Once you created the super user, you can access the admin page using [http://localhost:8000/admin](http://localhost:8000/admin) and log in with the credentials.

### 6. Populate Database with seed data

I have added some seed data for product categories, user roles, data lookups, and demo users as a starter. You can populate the database by using the following command.

```bash
docker-compose exec api python manage.py loaddata role.json

docker-compose exec api python manage.py loaddata users.json

docker-compose exec api python manage.py loaddata lookup.json

docker-compose exec api python manage.py loaddata categories.json

docker-compose exec api python manage.py loaddata category_attributes.json

docker-compose exec api python manage.py loaddata product_attributes.json

docker-compose exec api python manage.py loaddata products.json
```

The above commands will populate the database with some data to work with but you can always use the **django admin** site to create data as well.

### 7. Run Tests

To run the tests, use the following command:

```bash
docker-compose exec api pytest
```

This will run all tests using the pytest test runner and also displays the test coverage in your terminal.

### 8. Access the Services

- **Django API**: Open your browser and navigate to [http://localhost:8000/api/v1/docs](http://localhost:8000/api/v1/docs) to access the Django API.

- **pgAdmin4**: Go to [http://localhost:8001](http://localhost:8001) to access pgAdmin4. Use the credentials from your `.env` file to log in.

  - **Email**: `PGADMIN_DEFAULT_EMAIL` from the `.env` file (e.g., `admin@example.com`)
  - **Password**: `PGADMIN_DEFAULT_PASSWORD` from the `.env` file

### 9. Managing PostgreSQL in pgAdmin

Once you're logged in to pgAdmin4, follow these steps to add the PostgreSQL server:

1. Click on "Add New Server".
2. Under the **General** tab, set a name for the server (e.g., `artisan DB`).
3. Under the **Connection** tab, enter the following details:
   - **Host**: `db` (this is the service name defined in the `docker-compose.yml` file)
   - **Port**: `5432`
   - **Username**: `POSTGRES_USER` from the `.env` file (e.g., `XgkJUcqxEw`)
   - **Password**: `POSTGRES_PASSWORD` from the `.env` file

Click **Save** to add the server, and you should now be able to manage the `artisan` database from pgAdmin.

## Useful Docker Commands

Here are some helpful commands to manage the Docker environment:

- **Stop all running containers**:

  ```bash
  docker-compose down
  ```

- **Rebuild and restart containers**:

  ```bash
  docker-compose up --build
  ```

- **Check logs for a specific service**:

  ```bash
  docker-compose logs <service-name>
  ```

  For example:

  ```bash
  docker-compose logs api
  ```

- **Access a running container**:

  ```bash
  docker exec -it <container_name> /bin/bash
  ```

  For example, to access the Django API container:

  ```bash
  docker exec -it <api-container-name> /bin/bash
  ```

## Troubleshooting

- **Django server not reachable**: Ensure the Django app is running on `0.0.0.0` and bound to port 8000 (this is handled by the Docker setup).
- **Database connection errors**: Verify that the database credentials in the `.env` file are correct, and that the PostgreSQL service is up and healthy.

## Volumes

The `docker-compose.yml` file defines two Docker volumes:

- `artisan_dev_db_data`: Stores the PostgreSQL database data.
- `artisan_dev_pgadmin_data`: Stores pgAdmin4 configuration data.

These volumes ensure that your data persists across container restarts.
