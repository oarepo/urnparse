# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Miroslav Bauer @ CESNET.
#
# urnparse is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""URNparse tests."""
import pytest

from urnparse import NSIdentifier, InvalidURNFormatError, NSSString, RQFComponent, URN8141


def test_ns_identifier():
    ni = NSIdentifier('test')
    assert ni.value == 'test'
    assert str(ni) == 'test'

    with pytest.raises(InvalidURNFormatError):
        NSIdentifier('test/abc')

    ne = NSIdentifier('test2')
    assert ni != ne


def test_nss_string():
    nss = NSSString('example.org:resource:test%20space')
    assert nss.encoded == 'example.org:resource:test%20space'
    assert nss.value == 'example.org:resource:test space'

    nss2 = NSSString('example.org:resource:test space', encoded=False)
    assert nss.encoded == 'example.org:resource:test%20space'
    assert nss.value == 'example.org:resource:test space'


def test_rqf_component():
    rqf = RQFComponent('', 'a=a%20test&b=b%20test', 'example.org')
    assert len(rqf.query) == 2
    assert 'a' in rqf.query.keys()
    assert rqf.query['a'] == 'a test'

    assert rqf.fragment == 'example.org'
    assert str(rqf) == '?=a=a%20test&b=b%20test#example.org'


def test_urn():
    urn = URN8141.from_string('urn:tests:example:attributes:123?=key=value%3Asubvalue#example.org')
    assert urn is None