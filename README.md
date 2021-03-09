<h1 style="font-weight:normal"> 
  Tableau Public Metrics 
</h1>

[![Status](https://img.shields.io/badge/status-active-success.svg)]() [![GitHub Issues](https://img.shields.io/github/issues/wjsutton/tableau_public_metrics.svg)](https://github.com/wjsutton/tableau_public_metrics/issues) [![GitHub Pull Requests](https://img.shields.io/github/issues-pr/wjsutton/tableau_public_metrics.svg)](https://github.com/wjsutton/tableau_public_metrics/pulls) [![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

Calling Tableau Public APIs via an AWS Lambda function to record data from my Tableau Public Profile.

[Twitter][Twitter] :speech_balloon:&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;[LinkedIn][LinkedIn] :necktie:&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;[GitHub :octocat:][GitHub]&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;[Website][Website] :link:

<!--/div-->

<!--
Quick Link 
-->

[Twitter]:https://twitter.com/WJSutton12
[LinkedIn]:https://www.linkedin.com/in/will-sutton-14711627/
[GitHub]:https://github.com/wjsutton
[Website]:https://wjsutton.github.io/

### :a: About

I post on Tableau Public regularly and wanted to the metrics from my profile. Tableau Public has API calls that return json data making the data extract process simple. The script itself would need to run frequently so I could track my metrics over time, for this I've opted to use AWS Lambda functions to run my script and send the data to an S3 bucket.


### Set up

#### 1. Locally write a Python script that writes data to csv
[get_profile_data.py](https://github.com/wjsutton/tableau_public_metrics/blob/main/get_profile_data.py) is a scripts that queries the Tableau API and writes the data to a csv file [tableau_public_stats.csv](https://github.com/wjsutton/tableau_public_metrics/blob/main/tableau_public_stats.csv)

#### 2. Create S3 Bucket upload example file
Default configuration for S3 and upload file to S3 Bucket

#### 3. Create IAM Role
Set up an IAM to run lambda functions with the options to read and write data to an S3 Bucket
AWS service: lambda
Policies: AWSLambdaExecute, AWSLambdaRole, AmazonS3FullAccess (this may be overkill as we are just reading & writing to S3)

#### 4. Create AWS Lambda function
Change 'General configuration' to more than 3 secs  
Working from [get_profile_data.py](https://github.com/wjsutton/tableau_public_metrics/blob/main/get_profile_data.py) change the script:

- check imported libraries work, e.g. `requests` was switched for `urllib3`
- some libraries change be switched, for which we can create a Lambda layer (more on this later) and add the AWSLambda-Python38-SciPy1x layer to get access to the `numpy` library
- [lambda_func.py](https://github.com/wjsutton/tableau_public_metrics/blob/main/lambda_func.py) is an anonymised version of the script used. Note for reading the data in there are 2 options, download the file then read it or read it straight from the bucket - this script does the latter but as the download script commented out

#### 5. Create AWS Lambda Layer for pandas library
Adding a Lambda layer allows us to include additional code and libraries with our Lambda function. I followed this walkthrough, downloading the python libraries, creating a .zip file and uploading to AWS [https://medium.com/swlh/how-to-add-python-pandas-layer-to-aws-lambda-bab5ea7ced4f](https://medium.com/swlh/how-to-add-python-pandas-layer-to-aws-lambda-bab5ea7ced4f)
For reference some other AWS layers can be found here [https://github.com/mthenw/awesome-layers](https://github.com/mthenw/awesome-layers)




Materials the helped me on this project:

- [Medium - use Lambda to append daily data](https://medium.com/@haldis444/use-lambda-to-append-daily-data-to-csv-file-in-s3-2c2813bc33d0)
- [YouTube - How to download a S3 File from Lambda in Python | Step by Step Guide](https://www.youtube.com/watch?v=6LvtSmJhVRE)
- [YouTube - Upload to S3 From Lambda Tutorial | Step by Step Guide](https://www.youtube.com/watch?v=vXiZO1c5Sk0)
