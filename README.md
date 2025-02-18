# French Cadastre API

This project consists of developing an API that allows users to retrieve information from the French cadastre. The API supports multiple queries for retrieving data related to the cadastral system.

## Project Overview

The goal of this project is to build an API that can answer several queries related to the French cadastre, such as retrieving property boundaries, cadastral data, and other relevant geographic and legal information. 

## Technologies

- **Backend**: Python (Flask or FastAPI)
- **Database**: PostgreSQL (with PostGIS for geospatial data)
- **Data Sources**: French cadastral data (available via public sources)

## Features

- **Retrieve cadastral data**: Access property boundaries, details of land plots, and associated metadata.
- **Multiple query options**: Supports various queries to fetch data about specific regions, communes, and cadastral identifiers.
- **Geospatial data**: Built with geospatial capabilities to handle map-based data.

## Installation

### Requirements

Make sure to have the following installed:

- Python 3.7+
- PostgreSQL with PostGIS enabled

### Setup

Clone the repository:

```bash
git clone https://github.com/tanguylegrand2/projet_info_2a.git
cd projet_info_2a
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Set up the database and import cadastral data as described in the provided documentation files.

## Running the API

Start the API by running the following command:

```bash
python app.py
```

The API will be available at `http://localhost:5000` by default.

## API Endpoints

- **GET /cadastre**: Retrieve cadastral information.
- **GET /commune/{id}**: Fetch data for a specific commune.
- **GET /region/{id}**: Retrieve data for a specific region.

## Testing the API

To test the API, you can use tools like [Postman](https://www.postman.com/) or cURL to make GET requests to the available endpoints.

## Future Improvements

- **Advanced search**: Allow more complex queries such as filtering by date, owner, or building type.
- **Data visualization**: Integrate with mapping tools (e.g., Leaflet) to visually display cadastral data.
- **Authentication**: Add user authentication and role-based access control for sensitive data.


