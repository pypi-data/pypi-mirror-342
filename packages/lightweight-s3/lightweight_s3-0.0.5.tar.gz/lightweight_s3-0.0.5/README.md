from ctypes import pythonapi

            ___       __    __                _       __    __         _____
           / (_)___ _/ /_  / /__      _____  (_)___ _/ /_  / /_   ____|__  /
          / / / __ `/ __ \/ __/ | /| / / _ \/ / __ `/ __ \/ __/  / ___//_ < 
         / / / /_/ / / / / /_ | |/ |/ /  __/ / /_/ / / / / /_   (__  )__/ / 
        /_/_/\__, /_/ /_/\__/ |__/|__/\___/_/\__, /_/ /_/\__/  /____/____/  
            /____/                          /____/                          

# lightweight-s3
Ultra-lightweight S3 client. Memory leakage not implemented yet (unlike boto3)
```commandline
pip install lightweight-s3
```


## Supports:  
- sending existing files  
- sending string as zipped json (data sinks)
- Operates within a session refreshed every four hours; be sure to shut down the client when you’re done.

<details>
  <summary>Usage </summary>
Create StorageConnectionParameters:

```python 
from lightweight_s3 import StorageConnectionParameters

storage_connection_parameters = StorageConnectionParameters(
    backblaze_access_key_id='access_key_id',
    backblaze_secret_access_key='secret_access_key',
    backblaze_endpoint_url='endpoint_url',
    backblaze_bucket_name='bucket_name'
)
```
Or just put em into the .env file. Load the .env using load_dotenv()  
StorageConnectionParameters() will read all of parameters in format:  

```
BACKBLAZE_ACCESS_KEY_ID=  
BACKBLAZE_SECRET_ACCESS_KEY=  
BACKBLAZE_ENDPOINT_URL=  
BACKBLAZE_BUCKET_NAME=  
```
or
```
AZURE_BLOB_PARAMETERS_WITH_KEY=  
AZURE_CONTAINER_NAME=
```
then:
```python
load_dotenv(env_path)
storage_connection_parameters = StorageConnectionParameters()
```


```python
s3_client = S3Client(storage_connection_parameters)

s3_client.upload_existing_file(file_path='C:/JohnnySins/Documents/SomeFile.csv')

s3_client.upload_zipped_jsoned_string(
    data='{some_sophisticated_data....}',
    file_name='some_csv_name.csv'
)

s3_client.shutdown()
```


</details>

<details>
  <summary>Sample Main </summary>
And the final sample main.py would look like:

```python
from lightweight_s3 import S3Client, StorageConnectionParameters


if __name__ == '__main__ ':

    storage_connection_parameters = StorageConnectionParameters(
        backblaze_access_key_id='access_key_id',
        backblaze_secret_access_key='secret_access_key',
        backblaze_endpoint_url='endpoint_url',
        backblaze_bucket_name='bucket_name'
    )

    """
    Or just put em into the .env file. Load the .env using:
    
            load_dotenv(env_path)
    
    and then read it using:
    
            storage_connection_parameters = StorageConnectionParameters()
    """

    s3_client = S3Client(storage_connection_parameters)

    s3_client.upload_existing_file(file_path='C:/JohnnySins/Documents/SomeFile.csv')

    s3_client.upload_zipped_jsoned_string(
        data='some_sophisticated_data....',
        file_name='some_csv_name.csv'
    )

    s3_client.shutdown()

```


