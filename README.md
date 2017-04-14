# real-estate-price-spark
Apache Spark based price analysis (Part of Big Data Analysis project)

# Steps
## Data Extraction
From websites like - OLX, PurpleYo 
+ Technology - Python 
+ Library - Scrapy, Beautiful Soup

## Data Analysis
Apache Spark

## UI 
+ Spark Job Web UI

While a spark job is running, UI can be found at - http://`<socket-address>`
For e.g. http://192.168.1.4:4040

However, once the job is completed, one is unable to view the UI.

+ History Server

Run the shell script to start the history server. It accesses the /tmp/spark-events for Event Logs.

`/usr/local/spark/sbin/start-history-server.sh`

Every spark job executed / failed can be found at http://172.20.10.13:18080/
