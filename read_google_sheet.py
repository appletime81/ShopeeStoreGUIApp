import os
import json
import tempfile
import pygsheets
import polars as pl

# import pandas as pd
from pprint import pprint

# set config
pl.Config.set_tbl_cols(1000)
pl.Config.set_tbl_rows(1000)


def auth_json():
    return {
        "type": "service_account",
        "project_id": "fifth-branch-405907",
        "private_key_id": "aa9439f37f3b5e053dd79544c1013111d205f176",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCju6Y4F84sGOa+\nKboAvuroJmD9EcWbaHiJzxsv64oJjC+G/JWkvskA/PqT6JyQqwuoDqpyawK4GV+Z\n/jGiNqPNsdvxeHOEpQUGNeXvQRzRKft4g1cJk8qoHGrit0cx0XnhN6ZCfufqLz0M\nIGobUQ2f5WcFS8fMplGeCMSWABx6BPKx6U1JRTLy9rse7VIWtUj7DX6qEr15PYU7\nSl6OMIjGu0htlEw3c8BhsRJjRtTWymUYl5LPsW2desQmQJCR9WR2fsrvAdkgQU4k\n4hWiQ2JlV5UX3oOAoaCrBvX2B4EdbM62gNapcLUhc5sNcrWDob7IEOmTwpBFHb35\ngAvnHuZJAgMBAAECgf8OXR1Cjn69H5zJJ0qfW3Wq0rMaKxT1gpS7LOVrBB7NTPRe\nbd+INF8t1wOki3jbYtCtovERAzzvKaAEF74C8l2BuLiy1lOhWgNhfW5OhEfNkavz\nRpJmz1sCpHuRUsLMJrRVLaydk28vpt/pexkpNv3FqTpVx0V1OUyvsH/j04lWqt8w\nUbejSyiA12Mxq/A1x2RuyLCd9lZPmGJicjKqWyR8qcXpXh05OmLLCfU+AmkJGdPg\nEYTr/uGxLYtMY8x8jOuQB+jCkw1V5vGs/msRpUvaGZa8GBuLfnk6KzNnfLO4KIH6\n+QMzhqMNoQ8QsaPHoeBRTpStAKN/yxckRkDKloECgYEA0mFTsEYgXdP/eAI1X1Ps\nEnX07npwalObdtOLeGQuDkj1nwqyBsr/oCcgsIhatxvBW7eimBTVAAyqUUwSy4ma\nxUQD7Cw8y61hC5ONrwWhG8w37JrXClBmQ7AOcGxMyRw1+dwExtYISWSptkMrzUpT\nsItoS5zFjXuE4LB1vQ8BW8kCgYEAxzzVYLUggfHZoqZBmd47daa1UxiG0x7N5r1F\nUiHLrEBX1S38GaNyZzryNc3+zPNtYvEaR07gkWwKEy6F9AmY9FmCUMIBnPYCmB8Z\nYpJn98hgc8DC+jclx7KUpucNkvq7msEPYPWkNaPocBxpnfSo5IlpqCKvVWkBwgD2\nm/yZdoECgYEAtAt1StuJIaOn8/W35aB13YqzllCU2no5B2Wd6+eYfsMz6euGVkfu\nowo5cLsRH7oSLcMn1I2niIZOUIsRXr2iBgbicIGfehQkhHq/+7SOn7KTfds6A+qw\nymbmxJH62PZavz3rnJtZti3/DCvKVcOxgdqc5HEDpMS8AGskKCuqVvkCgYEAlK8l\nXgJNvCvMisEf+8AJB4fdkaGgHDXE2wksjlqCMI3j/kdO96MuYTNwRg7ws+qGG2xq\nfAS1OlEyQ5ZYiQIQj2mtAq+FnKlKzlOHEjTIOfXjZP7ZgvlczGbM4LFVQ/axwo+I\n9obagN1NPT025JYM5GBX5Q3dYxP2J92oLEiaDgECgYEAmwatMuNHk/lzhXzxcwxw\nwComeZfciqiZAKWi4pMfFVRonIavWnPg6A4nGEsIXZxbE/PxXigRtv5mcYzLzxtK\ncYZ0OdTuOW8CBlehzdlEjF9hjo+RbL4pjeVR9Nur3e5im9qk5qbQzVcl3kGQdt5Q\nZl8+boW8nhr0uILLS5sQlsg=\n-----END PRIVATE KEY-----\n",
        "client_email": "google-sheet-api-by-python@fifth-branch-405907.iam.gserviceaccount.com",
        "client_id": "106206861488110401168",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/google-sheet-api-by-python%40fifth-branch-405907.iam.gserviceaccount.com",
        "universe_domain": "googleapis.com",
    }


def auth(file):
    return pygsheets.authorize(service_file=file.name)


def get_secret_key(order_no):
    # ----------------- create a temp json file ------------------
    temp_file = tempfile.NamedTemporaryFile(
        suffix=".json", dir=os.getcwd(), delete=False
    )
    json.dump(auth_json(), open(temp_file.name, "w"))
    # ------------------------------------------------------------

    # --------------------- get google auth ----------------------
    gc = auth(temp_file)
    temp_file.close()
    os.unlink(temp_file.name)
    # ------------------------------------------------------------

    # --------------------- get google sheet ---------------------
    sht = gc.open_by_url(
        "https://docs.google.com/spreadsheets/d/1pYg0cesYRxX47CdoEKN3TR_i1sfOAXiwtFTKmfKzheA"
    )
    wks_list = sht.worksheets()
    wks = wks_list[0]
    # ------------------------------------------------------------

    df = pl.DataFrame(wks.get_all_records())
    if len(order_no) > 0 and len(order_no) == 14:
        sub_df = df.filter(pl.col("Order No.").str.contains(order_no))
        print(sub_df)
        try:
            password = sub_df.item(0, 2)
            return password
        except:
            return False
    return False
