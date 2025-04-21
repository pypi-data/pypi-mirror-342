import pytest
from dfh.core import DigestFusionHasher
from dfh.exceptions import InvalidSplitRatioError

def test_hash_and_verify_success():
    hasher = DigestFusionHasher()
    content = b'test-content'
    signature = b'super-secret'

    result = hasher.hash(content, signature)
    final_hash = result['final_hash']
    split_ratio = result['split_ratio']

    assert hasher.verify(content, signature, split_ratio, final_hash)


def test_verify_invalid_split_ratio():
    hasher = DigestFusionHasher()
    content = b'test-content'
    signature = b'super-secret'
    fake_hash = '1234deadbeef'

    with pytest.raises(InvalidSplitRatioError):
        hasher.verify(content, signature, 0.1, fake_hash)
