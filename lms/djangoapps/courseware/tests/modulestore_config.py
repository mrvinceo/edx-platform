"""
Define test configuration for modulestores.
"""
from tempfile import mkdtemp

from django.conf import settings

from xmodule.modulestore.tests.django_utils import (
    xml_store_config, mixed_store_config
)

TEST_DATA_DIR = settings.COMMON_TEST_DATA_ROOT

# This is an XML only modulestore
TEST_DATA_XML_MODULESTORE = xml_store_config(TEST_DATA_DIR)

# Map all XML course fixtures so they are accessible through
# the MixedModuleStore
MAPPINGS = {
    'edX/simple/2012_Fall': 'xml',
    'edX/toy/2012_Fall': 'xml',
    'edX/toy/TT_2012_Fall': 'xml',
    'edX/test_end/2012_Fall': 'xml',
    'edX/test_about_blob_end_date/2012_Fall': 'xml',
    'edX/graded/2012_Fall': 'xml',
    'edX/open_ended/2012_Fall': 'xml',
    'edX/due_date/2013_fall': 'xml',
    'edX/open_ended_nopath/2012_Fall': 'xml',
    'edX/detached_pages/2014': 'xml',
}
# This modulestore will provide both a mixed mongo editable modulestore, and
# an XML store with all the above courses loaded.
TEST_DATA_MIXED_XML_MODULESTORE = mixed_store_config(TEST_DATA_DIR, MAPPINGS)

# This modulestore will provide both a mixed mongo editable modulestore, and
# an XML store with just the toy course loaded.
TEST_DATA_MIXED_TOY_MODULESTORE = mixed_store_config(TEST_DATA_DIR, {'edX/toy/2012_Fall': 'xml', })

# All store requests now go through mixed
# Use this modulestore if you specifically want to test mongo and not a mocked modulestore.
# This modulestore definition below will not load any xml courses.
TEST_DATA_MONGO_MODULESTORE = mixed_store_config(mkdtemp(), {}, include_xml=False)

# Unit tests that are not specifically testing the modulestore implementation but just need course context can use a mocked modulestore.
# Use this modulestore if you do not care about the underlying implementation.
# TODO: acutally mock out the modulestore for this in a subsequent PR.
TEST_DATA_MOCK_MODULESTORE = mixed_store_config(mkdtemp(), {}, include_xml=False)
