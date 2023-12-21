import datetime
import os
import string
import tarfile
import shutil
import boto                          # you need to install "boto" == 'sudo pip install boto'
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from datetime import timedelta

# Configuration inlcudes of AWS credentials, db.sqlite3 file and local backup path
# note: first you need to store this script where your db.sqlite3 db is located
# Then you can run the script "python sqlite_bck.py

aws_access_key = 'AKIAUKEOSGO3I34O4KUU'
aws_secret_key = 'xcyCapBFF+TjcYMqFfIrtiIqcSKORwmdnPBl2Sxo'
aws_bucket = 'eve-db'                    # s3 bucket name
aws_folder = 'eve-db-folder'                     # folder name inside bucket

## create directory inside /tmp and backup the database
os.system("mkdir /tmp/backup_db")
path='tmp/backup_db/'
db="wg.sqlite3"

cmd= "sqlite3 wg.sqlite3 .dump > '"+path+"''"+db+"'"
os.system(cmd)

#configuring filepath and tar file name
today = str(datetime.date.today())
archieve_name = db
db_path = db
archieve_path = path + archieve_name

print('[FILE] Creating archive for ' + db)
shutil.make_archive(archieve_path, 'gztar', path)
print('Completed archiving database')
full_archive_file_path = archieve_path + ".tar.gz"
full_archive_name = archieve_name + ".tar.gz"

# import pdb; pdb.set_trace()


# Establish S3 Connection
# s3 = S3Connection(aws_access_key, aws_secret_key)
s3 = boto.s3.connect_to_region('eu-central-1',
       aws_access_key_id=aws_access_key,
       aws_secret_access_key=aws_secret_key,
       # is_secure=True,               # uncomment if you are not using ssl
       calling_format = boto.s3.connection.OrdinaryCallingFormat(),
       )

bucket = s3.get_bucket(aws_bucket)

# Send files to S3
print ('[S3] Uploading file archive ' + full_archive_name + '...')
k = Key(bucket)
k.key = aws_folder + '/' + today + '/' + full_archive_name
print(k.key)
k.set_contents_from_filename(full_archive_file_path)
k.set_acl("public-read")

print('[S3] Clearing previous file archive ' + full_archive_name + '...')
# shutil.rmtree(path)
print('Removed backup of Local database')