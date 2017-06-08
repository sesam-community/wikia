# wikia-extractor
Reads XML backup dumps from wikias and extracts some data.

[![Build Status](https://travis-ci.org/sesam-community/wikia.svg?branch=master)](https://travis-ci.org/sesam-community/wikia)

Wikia dumps data on request to Amazon S3. See links at bottom of the [special page](http://muppet.wikia.com/wiki/Special:Statistics).

An example of system config: 

```json
[{
  "_id": "my-wikia",
  "type": "system:microservice",
  "docker": {
    "environment": {
      "WIKIA_NAME": "muppet"
    },
    "image": "sesamcommunity/wikia:latest",
    "port": 5000
  }
},
{
  "_id": "my-muppet-reader",
  "type": "pipe",
  "source": {
    "type": "json",
    "system": "my-wikia",
    "url": "/entities"
  }
}]
```
