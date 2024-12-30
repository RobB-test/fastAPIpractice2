import boto3

#Initialize the s3 client
s3 = boto3.client("s3")

#Name of S3 bucket
bucket_name = "robbrown271276-generalbucket"

#File path in s3
file_key = "index.html"

#Download file to temp location
s3.download_file(bucket_name, file_key, "tmp.html")

#Read and print file contents
with open("tmp.html", "r") as file:
    contents = file.read()
    print(contents)
