# The MIT License (MIT)
#
# Copyright (c) 2018 Evgeny Medvedev, evge.medvedev@gmail.com, Vasiliy Bondarenko vabondarenko@gmail.com
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

from eosetl.rpc.request import make_post_request


class EosRpc:

    def __init__(self, provider_uri, timeout=60):
        self.provider_uri = provider_uri
        self.timeout = timeout

    def call(self, endpoint, data):
        text = json.dumps(data)
        request_data = text.encode('utf-8')

        raw_response = make_post_request(
            self.provider_uri + endpoint,
            request_data,
            timeout=self.timeout
        )

        response = self._decode_rpc_response(raw_response)
        return response

    def _decode_rpc_response(self, response):
        # Errors are ignored because the EOS node returns invalid response that can't be decoded with utf-8
        # https://github.com/blockchain-etl/eos-etl/issues/10
        response_text = response.decode('utf-8', errors='ignore')
        return json.loads(response_text, parse_float=decimal.Decimal)

    def getblock(self, block_num_or_id):
        return self.call('/v1/chain/get_block', {
            'block_num_or_id': block_num_or_id
        })

    def get_info(self):
        return self.call('/v1/chain/get_info', {})
