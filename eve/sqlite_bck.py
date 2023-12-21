import datetime
import os
import string
import tarfile
import shutil
import boto                          # you need to install "boto" == 'sudo pip install boto'
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from datetime import timedelta
import sqlite3

#
aws_access_key = 'AKIAUKEOSGO3I34O4KUU'
aws_secret_key = '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'
aws_bucket = 'eve-db'                    # s3 bucket name
aws_folder = 'eve-db-folder'                     # folder name inside bucket


path='tmp/backup_db/'
db="wg.sqlite3"

con = sqlite3.connect('wg.sqlite3')
bck = sqlite3.connect(f'{path}backup.db')
with bck:
    con.backup(bck)
bck.close()
con.close()
       #
#configuring filepath and tar file name
today = str(datetime.date.today())
archieve_name = db
db_path = db
archieve_path = path + archieve_name + "_" + today
#

print('[FILE] Creating archive for ' + db)
shutil.make_archive(archieve_path, 'gztar', path)
print('Completed archiving database')
full_archive_file_path = archieve_path + ".tar.gz"
full_archive_name = archieve_name + ".tar.gz"
print(full_archive_file_path)
print(full_archive_name)

s3 = boto.s3.connect_to_region('eu-central-1',
       aws_access_key_id=aws_access_key,
       aws_secret_access_key=aws_secret_key,
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
shutil.rmtree(path)
os.mkdir(path)
print('Removed backup of Local database')