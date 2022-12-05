# OverseerApi

### Environment variables  
- **OVERSEER_API_CONFIG_PATH** \
  file path to config file
- **MONGO_HOST** \
  url to MongoDB
- **RABBIT_HOST** \
  url to RabbitMQ

By default swagger should be available at http://localhost:9000/api/overseer/v1/
To initialize MongoDB from mongodb-dump: docker exec -i <docker-container-name> /usr/bin/mongorestore --username root --password root --authenticationDatabase admin --db overseer /dump/overseer