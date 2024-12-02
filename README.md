# NASA CME and GST Data Processing

This project retrieves, processes, and merges data on Coronal Mass Ejections (CMEs) and Geomagnetic Storms (GSTs) from NASA's DONKI API. The final merged dataset includes time-difference calculations and is exported for further analysis.

---

## Project Overview

The workflow involves the following key steps:
1. **Retrieve CME and GST Data**:
   - Fetch data using GET requests to NASA's API with specified date ranges and API key.
   - Convert the JSON response into Pandas DataFrames for analysis.

2. **Data Cleaning**:
   - Explode nested data (`linkedEvents`) into individual rows.
   - Extract `activityID` from nested dictionaries.
   - Remove missing values and filter relevant rows.

3. **Data Transformation**:
   - Convert columns to appropriate data types (e.g., `datetime`).
   - Rename columns for clarity.
   - Filter data based on specific criteria (e.g., retain GSTs linked to CMEs).

4. **Merge Data**:
   - Merge the cleaned CME and GST DataFrames using relevant keys.
   - Calculate time differences between CME and GST events.

5. **Export Data**:
   - Save the final cleaned and merged dataset to a CSV file for future use.

---

## How to Use

### Prerequisites
Ensure you have the following installed:
- Python 3.x
- Pandas
- Requests

### Setup
1. Clone the repository or copy the code files.
2. Install the required Python libraries:
   ```bash
   pip install pandas requests
3. Replace the placeholder DEMO_KEY with your NASA API key in the code.

Run the script files in order:
1. Retrieve CME Data
python cme_data_processing.py

2. Retrieve GST Data:
python gst_data_processing.py

3. Merge and Export Data:
python merge_export_data.py


###Retrieving Data
The code constructs query URLs for CME and GST data based on the base URL, date ranges, and API key.
The JSON responses are previewed and converted into Pandas DataFrames.

###Cleaning Data
Exploding Nested Data: The linkedEvents column, containing nested lists of dictionaries, is expanded into individual rows.
Extracting IDs: A helper function extract_activityID_from_dict is used to extract activityID values safely.
Filtering and Removing Missing Data: Rows with missing or irrelevant data are removed to retain only meaningful observations.

###Transforming Data
Columns are converted to appropriate data types, including datetime.
New columns are created, such as CME_ActivityID and timeDiff.
Columns are renamed for clarity (startTime to startTime_CME, etc.).

###Merging Data
The CME and GST DataFrames are merged using keys like GST_ActivityID and CME_ActivityID.
Time differences between events are calculated.

###Exporting Data
The final merged dataset is exported to a CSV file for further analysis.
Key Functions and Features
extract_activityID_from_dict: A utility function to safely extract activityID from dictionaries, handling errors gracefully.

###Dynamic Filtering: Rows are filtered based on the presence of specific keywords (e.g., 'CME').

Time Difference Calculation: Calculates the time difference (in seconds) between CME and GST start times.

Example Output
Final Merged DataFrame:

gstID	startTime_GST	CME_ActivityID	cmeID	startTime_CME	timeDiff
2022-01-01T00:00:00-GST-001	2022-01-01 00:00:00	CME-001	CME-001	2022-01-01 00:00:00	3600.0
Exported CSV:

File Name: merged_cme_gst_data.csv
Contains the merged and cleaned dataset for further analysis.

