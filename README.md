# Data Processing App

## Overview
This application is a simple Flask web app with three main functionalities: (i) uploading a file containing experiment metadata, (ii) processing the uploaded metadata and transform the original data stored in certain location into its RDF representation, and storing the processed data into a text file which is (iii) then available for download. 

## Setup and Installation

1. **Install Python 3**  
   Ensure you have Python 3 installed on your system.

2. **Setup Virtual Environment (Optional but recommended)**    
`python3 -m venv env source env/bin/activate` # On Windows, use: `env\Scripts\activate`

3. **Install All Required Libraries**   
`pip install -r requirements.txt`

4. **Clone the Repository**   
Clone the repository or copy the scripts into your project directory.

## Project Structure

- **main.py**: This is the main script that contains the Flask application and the endpoints for the REST APIs.
- **templates/index.html**: This file contains the HTML template for the home page, which includes a file uploader and buttons to trigger the process and store data functionalities.
- **example_data**: This folder contains a simple CSV data about alloy composition and its metadata representation in TRIG format (extended TTL). 
    - The metadata (trig) file consisting of three components: (i) DCAT part for accessing real data, (ii) mapping from original data into RDF representation - currently following [RML specification](https://w3id.org/rml/core/spec) - more about it can be seen at [RML website](https://rml.io), and (iii) EMMO ontology and instances, for completing the transformed RDF data. 

### The `main.py` script defines the following routes:

1. **/upload_data (POST)**
- Endpoint to upload a file from the local computer.
- The uploaded file is stored in the `uploads/` directory and the filename is added to a list of data to be processed.

2. **/process_data (GET)**
- Endpoint to process the uploaded `*.trig` file containing the metadata about an experiment result.
- The process will use the available metadata to transform the original data into its RDF representation.

3. **/store_data (GET)**
- The processed data is stored in a text file and this file is then sent to the browser for download as a `*.ttl`.

4. **/ (GET)**
- The home page which provides a simple UI for the application.

### Running the Application

1. Navigate to the project directory in your terminal.
2. Run the following command to start the Flask application:   
`python app.py`
3. Open a web browser and visit `http://127.0.0.1:5000/` to access the application.

### Contributing
Feel free to fork the project and make contributions.

### License
This project is open-source and available under the [MIT License](LICENSE).



<!-- # Demo Luxembourg

## How to install

* `pip install -r requirements.txt`
* `python main.py`
* Open http://127.0.0.1:5000 in your browser
* Upload [example metadata](example_data/alloy_data_simplified_meta.trig) in the  -->