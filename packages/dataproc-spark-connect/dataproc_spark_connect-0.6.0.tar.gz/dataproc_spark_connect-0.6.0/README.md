# Dataproc Spark Connect Client

A wrapper of the Apache [Spark Connect](https://spark.apache.org/spark-connect/) client with
additional functionalities that allow applications to communicate with a remote Dataproc
Spark cluster using the Spark Connect protocol without requiring additional steps.

## Install

```console
pip install dataproc_spark_connect
```

## Uninstall

```console
pip uninstall dataproc_spark_connect
```

## Setup
This client requires permissions to manage [Dataproc sessions and session templates](https://cloud.google.com/dataproc-serverless/docs/concepts/iam).
If you are running the client outside of Google Cloud, you must set following environment variables:

* GOOGLE_CLOUD_PROJECT - The Google Cloud project you use to run Spark workloads
* GOOGLE_CLOUD_REGION - The Compute Engine [region](https://cloud.google.com/compute/docs/regions-zones#available) where you run the Spark workload.
* GOOGLE_APPLICATION_CREDENTIALS - Your [Application Credentials](https://cloud.google.com/docs/authentication/provide-credentials-adc)
* DATAPROC_SPARK_CONNECT_SESSION_DEFAULT_CONFIG (Optional) - The config location, such as `tests/integration/resources/session.textproto`

## Usage

1. Install the latest version of Dataproc Python client and Dataproc Spark Connect modules:

   ```console
   pip install google_cloud_dataproc --force-reinstall
   pip install dataproc_spark_connect --force-reinstall
   ```

2. Add the required import into your PySpark application or notebook:

   ```python
   from google.cloud.dataproc_spark_connect import DataprocSparkSession
   ```

3. There are two ways to create a spark session,

   1. Start a Spark session using properties defined in `DATAPROC_SPARK_CONNECT_SESSION_DEFAULT_CONFIG`:

      ```python
      spark = DataprocSparkSession.builder.getOrCreate()
      ```

   2. Start a Spark session with the following code instead of using a config file:

      ```python
      from google.cloud.dataproc_v1 import SparkConnectConfig
      from google.cloud.dataproc_v1 import Session
      dataproc_session_config = Session()
      dataproc_session_config.spark_connect_session = SparkConnectConfig()
      dataproc_session_config.environment_config.execution_config.subnetwork_uri = "<subnet>"
      dataproc_session_config.runtime_config.version = '3.0'
      spark = DataprocSparkSession.builder.dataprocSessionConfig(dataproc_session_config).getOrCreate()
      ```

## Billing
As this client runs the spark workload on Dataproc, your project will be billed as per [Dataproc Serverless Pricing](https://cloud.google.com/dataproc-serverless/pricing).
This will happen even if you are running the client from a non-GCE instance.

## Contributing
### Building and Deploying SDK

1. Install the requirements in virtual environment.

      ```console
      pip install -r requirements-dev.txt
      ```

2. Build the code.

      ```console
      python setup.py sdist bdist_wheel
      ```

3. Copy the generated `.whl` file to Cloud Storage. Use the version specified in the `setup.py` file.

      ```sh
      VERSION=<version>
      gsutil cp dist/dataproc_spark_connect-${VERSION}-py2.py3-none-any.whl gs://<your_bucket_name>
      ```

4. Download the new SDK on Vertex, then uninstall the old version and install the new one.

      ```sh
      %%bash
      export VERSION=<version>
      gsutil cp gs://<your_bucket_name>/dataproc_spark_connect-${VERSION}-py2.py3-none-any.whl .
      yes | pip uninstall dataproc_spark_connect
      pip install dataproc_spark_connect-${VERSION}-py2.py3-none-any.whl
      ```
