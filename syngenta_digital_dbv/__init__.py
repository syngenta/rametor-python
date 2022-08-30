from syngenta_digital_dbv.postgres import PostgresVersioner
from syngenta_digital_dbv.mongo import MongoVersioner

def version(**kwargs):
    if kwargs['engine'] == 'redshift':
        redshift_versioner = PostgresVersioner(**kwargs)
        redshift_versioner.version()
    elif kwargs['engine'] == 'postgres':
        postgres_versioner = PostgresVersioner(**kwargs)
        postgres_versioner.version()
    else:
        raise Exception(f'engine {kwargs["engine"]} not supported; contribute to get it supported')
