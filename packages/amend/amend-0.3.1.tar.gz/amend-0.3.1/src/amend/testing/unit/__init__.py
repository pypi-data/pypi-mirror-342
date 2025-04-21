import unittest

from amend.testing.unit.built_in import (
    TestAmendImmutableBinary,
    TestAmendImmutableDataSet,
    TestAmendInteger,
    TestAmendMutableBinary,
    TestAmendMutableDataMapping,
    TestAmendMutableDataSet,
    TestAmendRealNumber,
    TestAmendText,
)
from amend.testing.unit.standard import (
    TestAmendDate,
    TestAmendDateAndTime,
    TestAmendDirectory,
    TestAmendFile,
    TestAmendTemporalOffset,
    TestAmendTime,
)
from amend.testing.unit.utilities import (
    TestImmutableMappingAcquisition,
    TestLeastCommonMultiplierSearch,
    TestLengthNormalizationOfImmutableBinary,
    TestLengthNormalizationOfImmutableSequence,
    TestLengthNormalizationOfMutableBinary,
    TestLengthNormalizationOfMutableSequence,
    TestLengthNormalizationOfText,
    TestLengthNormalizationStrategyDetermination,
)

if __name__ == "__main__":
    unittest.main()
