# coding: utf-8
"""
This scripts uses the Article Meta API to harvest all SciELO Network Documents
They are stored into a zip file.
This processing always harvest the entire database to garantee that all the
documents are up to date.
"""
import os
import logging
import zipfile
import datetime

import requests
import argparse

logger = logging.getLogger(__name__)

ARTICLEMETA = 'http://articlemeta.scielo.org/api/v1/'

trans_acronym = {'scl': 'bra'}


def load_documents(xml_format='xmlwos'):
    offset = 0
    while True:
        url = '%sarticle/identifiers?offset=%s' % (ARTICLEMETA, str(offset))
        logger.debug('Loading url: %s', url)
        identifiers = requests.get(url).json()

        if len(identifiers['objects']) == 0:
            raise StopIteration

        for identifier in identifiers['objects']:
            code = identifier['code']
            collection = identifier['collection']
            url_document = '%sarticle?code=%s&format=%s' % (ARTICLEMETA, code, xml_format)
            logger.debug('Loading url: %s', url_document)
            document = requests.get(url_document)
            yield ('%s_%s' % (collection, code), document.text)

        offset += 1000


def getschema():

    try:
        xsd = requests.get('https://raw.githubusercontent.com/scieloorg/articles_meta/master/tests/xsd/scielo_sci/ThomsonReuters_publishing.xsd').text
        logger.debug('Schema download')
        return xsd
    except:
        logger.error('Schema download fail')


def dumpdata(*args, **xargs):
    zip_name = xargs['file_name']
    xml_format = xargs['xml_format']

    logger.info('Creating zip file: %s', zip_name)
    logger.info('XML Format: %s', xml_format)
    with zipfile.ZipFile(zip_name, 'w', compression=zipfile.ZIP_DEFLATED, allowZip64=True) as thezip:
        for document in load_documents(xml_format=xml_format):
            collection = trans_acronym[document[0][0:3]] if document[0][0:3] in trans_acronym else document[0][0:3]
            issn = document[0][5:14]
            pid = document[0][5:]
            xml_file_name = '{0}/{1}/{2}.xml'.format(collection, issn, pid)
            thezip.writestr(xml_file_name, bytes(document[1].encode('utf-8')))

        readmef = open(os.path.dirname(__file__)+'/templates/dumparticle_readme.txt', 'r').read()
        readme = '{0}\r\n* Documents updated at: {1}\r\n'.format(readmef, datetime.datetime.now().isoformat())

        thezip.writestr("README.txt", bytes(readme))

        if xml_format == 'xmlwos':
            xsd = getschema()
            if xsd:
                thezip.writestr("schema/ThomsonReuters_publishing.xsd", bytes(xsd))

    logging.info('Zip created: %s', zip_name)


def _config_logging(logging_level='INFO', logging_file=None):

    allowed_levels = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    logger.setLevel(allowed_levels.get(logging_level, 'INFO'))

    if logging_file:
        hl = logging.FileHandler(logging_file, mode='a')
    else:
        hl = logging.StreamHandler()

    hl.setFormatter(formatter)
    hl.setLevel(allowed_levels.get(logging_level, 'INFO'))

    logger.addHandler(hl)

    return logger


def main():

    parser = argparse.ArgumentParser(
        description="Dump SciELO Network metadata"
    )

    parser.add_argument(
        '--zip_file',
        '-f',
        default='/tmp/dumpdata.zip',
        help='Full path to the zip file that will receive the documents'
    )

    parser.add_argument(
        '--xml_format',
        '-x',
        default='xmlwos',
        choices=['xmlwos', 'xmlrsps'],
        help='XML output format'
    )

    parser.add_argument(
        '--logging_file',
        '-o',
        default='/tmp/dumpdata.log',
        help='Full path to the log file'
    )

    parser.add_argument(
        '--logging_level',
        '-l',
        default='DEBUG',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Logggin level'
    )

    args = parser.parse_args()

    _config_logging(args.logging_level, args.logging_file)

    dumpdata(
        file_name=args.zip_file,
        xml_format=args.xml_format
    )
