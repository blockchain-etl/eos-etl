# The MIT License (MIT)
#
# Copyright (c) 2018 Evgeny Medvedev, evge.medvedev@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import decimal
import json

import requests

from eosetl.rpc.request import make_post_request


class EosRpc:

    def __init__(self, provider_uri, timeout=60):
        self.provider_uri = provider_uri
        self.timeout = timeout
        self.headers = {
            'accept': 'application/json',
            'content-type': 'application/json'
        }

    def call(self, endpoint, data):
        raw_response = requests.post(
            url=self.provider_uri + endpoint,
            data=json.dumps(data),
            headers=self.headers
        )

        if (raw_response.status_code != 200):
            raise Exception("Failed calling API. Error: " + raw_response.text)

        return raw_response.json(parse_float=decimal.Decimal)

    def getblockhash(self, param):
        response = self.batch([['getblockhash', param]])
        return response[0] if len(response) > 0 else None

    def getblock(self, block_num_or_id):
        return self.call('/v1/chain/get_block', {
            'block_num_or_id': block_num_or_id
        })

    def get_info(self):
        return self.call('/v1/chain/get_info', {})

    def getblockcount(self):
        response = self.batch([['getblockcount']])
        return response[0] if len(response) > 0 else None

