import os
import base64

from models import db, Donor, Donation  # noqa F403
from peewee import *  # noqa F403
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


try:
    db.connect()
    db.drop_tables([Donor, Donation])  # noqa F403
    db.create_tables([Donor, Donation])  # noqa F403
    logger.info('Drop and create tables.')
except Exception as e:
    logger.info(e)
finally:
    db.close()


def add_people():

    FIRST_NAME = 0
    LAST_NAME = 1

    donors = [
        ('George', 'Kim'),
        ('Don', 'Juan'),
        ('Michael', 'Jordan'),
        ('Mark', 'Mcgwire'),
        ('Ben', 'Kenobe')
    ]

    try:
        db.connect()
        for donor in donors:
            code = base64.b32encode(os.urandom(8)).decode().strip('=')
            with db.transaction():
                n = Donor.create(  # noqa F403
                    code=code,
                    first_name=donor[FIRST_NAME],
                    last_name=donor[LAST_NAME])
                n.save()

        logger.info('People added.')

    except Exception as e:
        logger.info(e)

    finally:
        logger.info('database closes')
        db.close()


def add_donations():

    DONATION_AMT = 0
    LAST_NAME = 1

    donations = [
        (75.0, 'Kim'),
        (7750.0, 'Juan'),
        (1250.0, 'Juan'),
        (4712.0, 'Juan'),
        (375.0, 'Jordan'),
        (758.0, 'Jordan'),
        (885.0, 'Mcgwire'),
        (71.0, 'Mcgwire'),
        (369.0, 'Mcgwire'),
        (111.0, 'Kenobe'),
        (475.0, 'Kenobe'),
        (411.0, 'Kenobe')
    ]

    try:
        db.connect()
        for donation in donations:
            with db.transaction():
                n = Donation.create(  # noqa F403
                    donation=donation[DONATION_AMT],
                    donor=donation[LAST_NAME])
                n.save()

        logger.info('Donations added.')

    except Exception as e:
        logger.info(e)

    finally:
        logger.info('database closes')
        db.close()


def query_donors():
    try:
        db.connect()
        query = (Donor  # noqa F403
                 .select(Donor, Donation)  # noqa F403
                 .join(Donation, JOIN.INNER))  # noqa F403

        for row in query:
            logger.info(f'{row.last_name} {row.donation.donation}')
    except Exception as e:
        logger.info(e)

    finally:
        logger.info('database closes')
        db.close()


def check_donor(key):
    try:
        db.connect()
        query = (Donor  # noqa F403
                 .select(Donor, Donation)  # noqa F403
                 .join(Donation, JOIN.INNER)  # noqa F403
                 .where(Donor.last_name == key))  # noqa F403

        if query.exists():
            return True

    except Exception as e:
        logger.info(e)

    finally:
        logger.info('database closes')
        db.close()


if __name__ == '__main__':
    add_people()
    add_donations()
