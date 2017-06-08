import json
import logging
import os
import urllib
import xml.etree.ElementTree as ET
import subprocess

import wikitextparser as wtp
from flask import Flask, Response

name = os.environ["WIKIA_NAME"]
devnull = open(os.devnull, 'w')

app = Flask(__name__)

logger = logging.getLogger('wikia-extractor')

@app.route('/entities')
def get_entities():

    def generate():
        url = "http://s3.amazonaws.com/wikia_xml_dumps/%s/%s/%s_pages_current.xml.7z" % (name[:1], name[:2], name)
        logger.info("Downloading '%s'.." % url)
        # can't decompress 7z as stream as it requires seeks
        local_filename, headers = urllib.request.urlretrieve(url)
        logger.info("Downloaded to '%s'" % local_filename)

        logger.info("Decompressing..")
        # requires 7z executable
        cmd = ['7z', 'e', '-so', local_filename]
        proc = subprocess.Popen(cmd, stderr=devnull, stdout=subprocess.PIPE)
        first = True
        yield "["
        for event, elem in ET.iterparse(proc.stdout):
            if elem.tag == '{http://www.mediawiki.org/xml/export-0.6/}page':
                text = elem.find('{http://www.mediawiki.org/xml/export-0.6/}revision').find('{http://www.mediawiki.org/xml/export-0.6/}text').text
                parsed_text = wtp.parse(text) if text else None
                entity = {
                    "_id": elem.find('{http://www.mediawiki.org/xml/export-0.6/}id').text,
                    "title": elem.find('{http://www.mediawiki.org/xml/export-0.6/}title').text,
                    "templates": [{ "name": x.name, "arguments": [{ "name": y.name, "value": y.value} for y in x.arguments] } for x in parsed_text.templates] if parsed_text else None,
                    "wikilinks": [{ "target": x.target, "text": x.text } for x in parsed_text.wikilinks] if parsed_text else None
                }
                if not first:
                    yield ","
                yield(json.dumps(entity))
                first = False
                elem.clear()
        yield "]"
        logger.info("Decompression complete")
        os.remove(local_filename)
        logger.info("Removed file '%s'" % local_filename)

    return Response(generate(), mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

