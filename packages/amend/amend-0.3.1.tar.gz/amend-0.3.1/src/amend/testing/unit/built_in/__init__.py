import unittest

from amend.testing.unit.built_in.mappings import TestAmendMutableDataMapping
from amend.testing.unit.built_in.numbers import (
    TestAmendInteger,
    TestAmendRealNumber,
)
from amend.testing.unit.built_in.sequences import (
    TestAmendImmutableBinary,
    TestAmendMutableBinary,
    TestAmendText,
)
from amend.testing.unit.built_in.sets import (
    TestAmendImmutableDataSet,
    TestAmendMutableDataSet,
)

if __name__ == "__main__":
    unittest.main()
