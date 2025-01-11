# Use the official PostgreSQL image
FROM postgres:latest

# Set environment variables for PostgreSQL
ENV POSTGRES_USER=admin
ENV POSTGRES_PASSWORD=
ENV POSTGRES_DB=mydatabase

# Expose the default PostgreSQL port
EXPOSE 5432