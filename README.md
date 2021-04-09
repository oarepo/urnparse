# urnparse
Python library for generating and parsing [RFC 8141]( https://tools.ietf.org/html/rfc8141) compliant uniform
resource names (URN).

## Installation

To use this library in your project, install it with pip

```shell
pip install urnparse
```

## Usage

### Create URN object from URN RFC 8141 formatted string
To validate a given URN string against the RFC 8141 specification and construct
an URN object from it, use the `URN8141.from_string()` method:

```python
from urnparse import URN8141

urn_string = 'urn:example:example.org:resources:'+\
             'example%20resource?+res1=a'+\
             '?=param1=test&param2=test2#example.org'

urn = URN8141.from_string(urn_string)
````

You can then access the specific URN components:
```python
print(urn.namespace_id)
# example
print(urn.specific_string.decoded)
# example.org:resources:example resource
print(urn.specific_string.parts)
# ['example.org', 'resources', 'example resource']
print(urn.rqf_component.resolution)
# {'res1': 'a'}
print(urn.rqf_component.query)
# {'param1': 'test', 'param2': 'test2'}
print(urn.rqf_component.fragment)
# example.org
```

#### Create URN string from component objects 
To create an RFC 8141 formatted URN string for a certain resource, construct the URN
object from the following components:

````python
from urnparse import URN8141, NSIdentifier, NSSString, RQFComponent

nid = NSIdentifier('example')
nss = NSSString('example.org:resources:example%20resource', encoded=True)
rqf = RQFComponent(resolution_string='res1=a',
                   query_string='param1=test&param2=test2',
                   fragment='example.org')

urn = URN8141(nid=nid, nss=nss, rqf=rqf)

print(urn)
# urn:example:example.org:resources:example%20resource?+res1=a?=param1=test&param2=test2#example.org
````

