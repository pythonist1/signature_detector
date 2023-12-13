from sqlalchemy import MetaData, Table, Column, String, Integer, Boolean, DateTime


metadata = MetaData()


SignatureDetectingResult = Table(
    'signature_detecting_result', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('reference', String),
    Column('detected_quantity', Integer),
    Column('is_detected', Boolean),
    Column('request_time', DateTime)
)
