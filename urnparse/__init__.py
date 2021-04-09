# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Miroslav Bauer @ CESNET.
#
# urnparse is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Python library for generating and parsing and RFC 8141 compliant uniform resource names (URN)."""

import re
from urllib.parse import parse_qs, quote, unquote, urlencode

URN_SCHEME = 'urn'
NID_PATTERN = re.compile(r'^[0-9a-z][0-9a-z-]{1,31}$', flags=re.IGNORECASE)
NSS_PCHAR = '[a-z0-9-._~]|%[a-f0-9]{2}|[!$&\'()*+,;=]|:|@'
NSS_PATTERN = re.compile(fr'^({NSS_PCHAR})({NSS_PCHAR}|/|\?)*$', re.IGNORECASE)
RQF_PATTERN = re.compile(
    r"^(?!$)(?:\?\+(?P<resolution_string>.*?))?(?:\?=(?P<query_string>.*?))?(?:#(?P<fragment>.*?))?$",
    flags=re.IGNORECASE)


def _validate_nid(value, min_len, max_len, pattern):
    strlen = len(value)
    if strlen < min_len:
        raise InvalidURNFormatError(f'{value} is shorter than {min_len}')
    elif strlen > max_len:
        raise InvalidURNFormatError(f'{value} is longer than {max_len}')

    if not re.match(pattern, value):
        raise InvalidURNFormatError(f'{value} contains invalid characters')


class NSIdentifier:
    """Namespace identifier class."""

    MIN_LENGTH = 2
    MAX_LENGTH = 32

    def __init__(self, val):
        """Initialize a Namespace identifier."""
        _validate_nid(val, self.MIN_LENGTH, self.MAX_LENGTH, NID_PATTERN)
        self.value = val

    def __repr__(self):
        """Representation of Namespace identifier."""
        return str(self.value)

    def __eq__(self, other):
        """Compare two Namespace identifiers."""
        if isinstance(other, self.__class__):
            return str(self.value) == str(other.value)
        return str(self) == str(other)


class NSSString:
    """Namespace specific string class."""

    def __init__(self, val, encoded=True):
        """Initialize a NSS String."""
        if encoded:
            if len(val) == 0 or not re.match(NSS_PATTERN, val):
                raise InvalidURNFormatError('NSS string is invalid.')

            self.encoded = val
            self._value = unquote(val)
        else:
            self.encoded = quote(val)
            self._value = val

    @property
    def decoded(self):
        """URI Decoded value of NSSString."""
        return self._value

    @property
    def parts(self):
        """Colon-separated parts of a NSSString."""
        return self._value.split(':')

    def __repr__(self):
        """Representation of NSSString."""
        return str(self.encoded)

    def __eq__(self, other):
        """Compare two NSSStrings."""
        if isinstance(other, self.__class__):
            return str(self.encoded) == str(other.encoded)
        return str(self) == str(other)


class RQFComponent:
    """RQF Component class."""

    RESOLUTION_SEPERATOR = '?+'
    QUERY_SEPERATOR = '?='
    FRAGMENT_SEPERATOR = '#'

    def __init__(self, resolution_string: str, query_string: str, fragment: str):
        """Initialize a RQF Component."""
        query_args = []
        resolution_args = []
        if query_string != '':
            query_args = {k: v[0] for k, v in parse_qs(query_string).items()}
        if resolution_string != '':
            resolution_args = {k: v[0] for k, v in parse_qs(resolution_string).items()}

        self._resolution_args = resolution_args
        self._query_args = query_args
        self._fragment = fragment

    @property
    def resolution(self) -> dict:
        """Resolution args dict."""
        return self._resolution_args

    @property
    def query(self) -> dict:
        """Query params dict."""
        return self._query_args

    @property
    def fragment(self):
        """Fragment component."""
        return self._fragment

    def __empty__(self):
        """Empty RQFComponent."""
        return len(self.resolution) == len(self.query) == len(self.fragment) == 0

    def __repr__(self):
        """Representation of RQFComponent."""
        return f'{self.RESOLUTION_SEPERATOR + urlencode(self.resolution, quote_via=quote) if len(self.resolution) else ""}' \
               f'{self.QUERY_SEPERATOR + urlencode(self.query, quote_via=quote) if len(self.query) else ""}' \
               f'{self.FRAGMENT_SEPERATOR + self.fragment if self.fragment else ""}'

    def __eq__(self, other):
        """Compare two RQFComponents."""
        return str(self) == str(other)


class URN8141:
    """
    A RFC 8141 compliant uniform resource name (URN).

    @see https://tools.ietf.org/html/rfc8141
    """

    def __init__(self, nid: NSIdentifier = None, nss: NSSString = None, rqf=None):
        """
        Initialize a RFC 8141 compliant uniform resource name.

        :param nid: The namespace identifier
        :param nss: The namespace specific string
        :param rqf: R, Q and F components of the URN
        """
        self._nid = nid
        self._nss = nss
        self._rqf = rqf

    @property
    def namespace_id(self) -> NSIdentifier:
        """Nsidentifier of the URN."""
        return self._nid

    @property
    def specific_string(self) -> NSSString:
        """Specific string part of the URN."""
        return self._nss

    @property
    def rqf_component(self) -> RQFComponent:
        """Rqfcomponent parts of the URN."""
        return self._rqf

    @classmethod
    def from_string(cls, urn_string, encoded=True):
        """Create an instance from a RFC 8141 formatted URN string.

        :param urn_string: A RFC 8141 formatted URN string
        :param encoded: URN string is urlencoded
        :raises InvalidURNFormatError
        """
        if not urn_string.startswith(URN_SCHEME) or urn_string.count(':') < 2:
            raise InvalidURNFormatError('URN string is invalid.')

        nid = urn_string.split(':')[1]
        specific_part = urn_string[(len(URN_SCHEME) + len(nid) + 2):].rstrip('#')
        eof_nss = cls._get_nss_indices(specific_part)[-1]
        nss = specific_part[:eof_nss]
        rqf = cls._parse_rqf_component(specific_part[eof_nss:])
        return cls(nid=NSIdentifier(nid), nss=NSSString(nss, encoded), rqf=rqf)

    @classmethod
    def _get_nss_indices(cls, specific_part):
        eof = len(specific_part)
        rsi = specific_part.rfind(RQFComponent.RESOLUTION_SEPERATOR)
        qsi = specific_part.rfind(RQFComponent.QUERY_SEPERATOR)
        fsi = specific_part.rfind(RQFComponent.FRAGMENT_SEPERATOR)

        if 0 < rsi < eof:
            eof = rsi
        if 0 < qsi < eof:
            eof = qsi
        if 0 < fsi < eof:
            eof = fsi

        return rsi, qsi, fsi, eof

    @classmethod
    def _parse_rqf_component(cls, rqf_string):
        if rqf_string == '':
            return RQFComponent('', '', '')

        matched = re.match(RQF_PATTERN, rqf_string)
        if not matched:
            return RQFComponent('', '', '')

        return RQFComponent(**matched.groupdict())

    def __repr__(self):
        """Representation of the URN."""
        return f'urn:{self._nid}:{self._nss}{self._rqf}'

    def __eq__(self, other):
        """Compare two URNs."""
        if isinstance(other, self.__class__):
            return self._nid == other.namespace_id and self._nss == other.specific_string
        return str(self) == str(other)


class InvalidURNFormatError(Exception):
    """Exception raised when given URN string didn't match the expected format."""
