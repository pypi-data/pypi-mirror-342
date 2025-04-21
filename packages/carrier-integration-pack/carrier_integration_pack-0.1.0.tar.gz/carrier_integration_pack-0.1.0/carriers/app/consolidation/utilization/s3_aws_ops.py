import boto
from boto.s3.key import Key

AWS_KEYS = {
    'dev': {
        'AWS_ACCESS_KEY_ID': 'AKIAIL6KEIHTV6KUHSCA',
        'AWS_SECRET_ACCESS_KEY': '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',
        'END_POINT': 'ap-south-1',
        'S3_HOST': 's3.ap-south-1.amazonaws.com',
        'BUCKET_NAME': 'eazyship'
    },
    'prod': {
        'AWS_ACCESS_KEY_ID': '',
        'AWS_SECRET_ACCESS_KEY': '',
        'END_POINT': '',
        'S3_HOST': '',
        'BUCKET_NAME': ''
    }
}


def SimpleStorageS3(file, id, tracking_number, order_id):
    print("SIMPLE STORAGE", id, tracking_number)

    upload_filename = 'eshipz' + '/' + str(order_id) + '/' + tracking_number

    aws_key = AWS_KEYS.get('dev', {})

    s3 = boto.s3.connect_to_region(
        aws_key['END_POINT'], aws_access_key_id=aws_key['AWS_ACCESS_KEY_ID'], aws_secret_access_key=aws_key[
            'AWS_SECRET_ACCESS_KEY'], host=aws_key['S3_HOST'])
    bucket = s3.get_bucket(aws_key['BUCKET_NAME'])
    k = Key(bucket)
    k.key = upload_filename + '.pdf'
    k.set_contents_from_string(file)
    k.set_acl('public-read')
    url = k.generate_url(expires_in=0, query_auth=False)
    return url


if __name__ == "__main__":
    file = "test test test"
    id = "test1221312"
    tracking_number = "234628376"
    print(SimpleStorageS3(file, id, tracking_number))
