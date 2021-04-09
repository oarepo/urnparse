#!/usr/bin/env sh
# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Miroslav Bauer @ CESNET.
#
# urnparse is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

pydocstyle urnparse tests && \
isort -c urnparse && \
check-manifest && \
pytest
