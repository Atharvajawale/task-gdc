import boto3
import pymysql
import os

def read_from_s3(bucket, key):
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket=bucket, Key=key)
    data = obj['Body'].read().decode('utf-8')
    return data

def push_to_rds(data, rds_endpoint, db_name, username, password):
    connection = pymysql.connect(
        host=rds_endpoint,
        user=username,
        password=password,
        database=db_name
    )
    cursor = connection.cursor()
    query = "INSERT INTO your_table (column) VALUES (%s)"
    cursor.execute(query, (data,))
    connection.commit()
    cursor.close()
    connection.close()

def push_to_glue(data, glue_database, table_name):
    glue = boto3.client('glue')
    response = glue.create_table(
        DatabaseName=glue_database,
        TableInput={
            'Name': table_name,
            'StorageDescriptor': {
                'Columns': [
                    {
                        'Name': 'column',
                        'Type': 'string'
                    }
                ],
                'Location': 's3://your-bucket/your-prefix/'
            }
        }
    )
    return response

def main():
    bucket = os.getenv('S3_BUCKET')
    key = os.getenv('S3_KEY')
    rds_endpoint = os.getenv('RDS_ENDPOINT')
    db_name = os.getenv('DB_NAME')
    username = os.getenv('DB_USERNAME')
    password = os.getenv('DB_PASSWORD')
    glue_database = os.getenv('GLUE_DATABASE')
    table_name = os.getenv('TABLE_NAME')
    
    data = read_from_s3(bucket, key)
    
    try:
        push_to_rds(data, rds_endpoint, db_name, username, password)
    except Exception as e:
        print("Failed to push to RDS, pushing to Glue Database instead.")
        push_to_glue(data, glue_database, table_name)

if __name__ == "__main__":
    main()
