# MIT License
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

import os

import pytest

import tests.resources
from eosetl.jobs.exporters.blocks_and_transactions_item_exporter import blocks_and_transactions_item_exporter
from eosetl.streaming.stream import stream
from blockchainetl.thread_local_proxy import ThreadLocalProxy
from tests.eosetl.job.helpers import get_eos_rpc
from tests.helpers import compare_lines_ignore_order, read_file, skip_if_slow_tests_disabled

RESOURCE_GROUP = 'test_export_blocks_job'


def read_resource(resource_group, file_name):
    return tests.resources.read_resource([RESOURCE_GROUP, resource_group], file_name)


@pytest.mark.timeout(10)
@pytest.mark.parametrize("start_block, end_block, batch_size, resource_group ,provider_type", [
    (5000001, 5000002, 1, 'eos/stream_50001_50002', 'mock'),
    skip_if_slow_tests_disabled([5000001, 5000002, 1, 'eos/stream_50001_50002', 'online']),
])
def test_stream(tmpdir, start_block, end_block, batch_size, resource_group, provider_type):
    try:
        os.remove('last_synced_block.txt')
    except OSError:
        pass

    blocks_output_file = str(tmpdir.join('actual_block.json'))
    transactions_output_file = str(tmpdir.join("actual_transactions.json"))
    actions_output_file = str(tmpdir.join("actual_actions.json"))

    stream(
        eos_rpc=ThreadLocalProxy(
            lambda: get_eos_rpc(
                provider_type,
                read_resource_lambda=lambda file: read_resource(resource_group, file))),
        start_block=start_block,
        end_block=end_block,
        batch_size=batch_size,
        item_exporter=blocks_and_transactions_item_exporter(blocks_output_file, transactions_output_file, actions_output_file)
    )

    print('=====================')
    print(read_file(blocks_output_file))
    compare_lines_ignore_order(
        read_resource(resource_group, 'expected_blocks.json'), read_file(blocks_output_file)
    )

    print('=====================')
    print(read_file(transactions_output_file))
    compare_lines_ignore_order(
        read_resource(resource_group, 'expected_transactions.json'), read_file(transactions_output_file)
    )

    print('=====================')
    print(read_file(transactions_output_file))
    compare_lines_ignore_order(
        read_resource(resource_group, 'expected_actions.json'), read_file(actions_output_file)
    )

