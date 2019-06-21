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

import pytest

from eosetl.jobs.export_blocks_job import ExportBlocksJob
from eosetl.jobs.exporters.blocks_item_exporter import blocks_item_exporter
from tests.eosetl.job.helpers import get_eos_rpc
from blockchainetl_common.thread_local_proxy import ThreadLocalProxy

import tests.resources
from tests.helpers import compare_lines_ignore_order, read_file, skip_if_slow_tests_disabled

RESOURCE_GROUP = 'test_export_blocks_job'


def read_resource(resource_group, file_name):
    return tests.resources.read_resource([RESOURCE_GROUP, resource_group], file_name)


@pytest.mark.parametrize("start_block, end_block, batch_size, resource_group ,provider_type", [
    (1, 1, 1, 'eos/block_1', 'mock'),
    skip_if_slow_tests_disabled([1, 1, 1, 'eos/block_1', 'online']),
    skip_if_slow_tests_disabled([30000000, 30000000, 1, 'eos/block_30000000', 'online']),
])
def test_export_blocks_job(tmpdir, start_block, end_block, batch_size, resource_group, provider_type):
    blocks_output_file = str(tmpdir.join('actual_block.json'))
    transactions_output_file = str(tmpdir.join("actual_transactions.json"))
    actions_output_file = str(tmpdir.join("actual_actions.json"))

    job = ExportBlocksJob(
        start_block=start_block,
        end_block=end_block,
        batch_size=batch_size,
        eos_rpc=ThreadLocalProxy(
            lambda: get_eos_rpc(
                provider_type,
                read_resource_lambda=lambda file: read_resource(resource_group, file))),
        max_workers=5,
        item_exporter=blocks_item_exporter(blocks_output_file, transactions_output_file, actions_output_file),
        export_blocks=blocks_output_file is not None,
        export_transactions=transactions_output_file is not None,
        export_actions=actions_output_file is not None)
    job.run()

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
    print(read_file(actions_output_file))
    compare_lines_ignore_order(
        read_resource(resource_group, 'expected_actions.json'), read_file(actions_output_file)
    )
