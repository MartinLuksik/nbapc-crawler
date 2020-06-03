from io import StringIO  # python3; python2: BytesIO
import boto3
import os
from azure.storage.blob import BlockBlobService


def save_to(result, season, table, season_type, save_destination):
    if save_destination == "local":
            result.to_csv('/wc/data/' + season + '_' + table + '.csv', index=False, sep=';')
            #result.to_csv('/home/martin/temp/nbapc_crawled_data/' + season + '_' + table + '_' + season_type + '.csv', index=False, sep=';')
            print('CSV was successfully saved as:' + season + '_' + table + '_' + season_type + '.csv')
    elif save_destination == "s3":
            bucket = os.environ['s3bucket']
            csv_buffer = StringIO()
            result.to_csv(csv_buffer, index=False, sep=';')
            s3 = boto3.resource('s3')
            s3.Object(bucket, 'crawled_data/' + season + '_' + table + '.csv').put(Body=csv_buffer.getvalue())
            print('CSV was successfully uploaded to s3: crawled_data/' + season + '_' + table + '.csv')
    elif save_destination == "wasb":
            wasbaccountname = os.environ['wasbaccountname']
            containername = os.environ['containername']
            wasbaccountkey = os.environ['wasbaccountkey']
            csv_buffer = StringIO()
            result.to_csv(csv_buffer, index=False, sep=';')
            block_blob_service = BlockBlobService(
                    account_name=wasbaccountname,
                    account_key=wasbaccountkey)
            block_blob_service.create_blob_from_text(containername, season + '_' + table + '.csv', csv_buffer.getvalue())
            print('CSV was successfully uploaded to Azure Storage Account container: ' + containername + '/' + season + '_' + table + '.csv')