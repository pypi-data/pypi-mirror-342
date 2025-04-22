from dfh.exceptions import InvalidSplitRatioError
class DigestFusionHasher:
    """
    Digest Fusion Hasher
    
    A secure hashing system that combines content and signature digests
    using a randomized split ratio technique for enhanced security.

    Methods:
        hash(content, signature) -> dict:
            Generates a fused hash and returns the final hash along with the used split ratio.
        
            verify(content, signature, split_ratio, expected_hash) -> bool:
                Verifies if given content and signature match the expected hash using provided split ratio.
    """

    def __init__(self):
        # Initizalization logic if needed
        pass


    def hash(self, content: bytes, signature: bytes) -> dict:
        """
        Generates a secure hash by fusing the content and signature digests with a randomized split ratio.

        Args:
            content (bytes): The main content to be hashed.
            signature (bytes): The secret signature used for added randomness.

        Returns:
            dict: A dictionary containing:
                - 'final_hash' (str): The resulting final hash as a hexadecimal string.
                - 'split_ratio' (float): The randomly generated split ratio used during fusion.
        """
        
        from hashlib import sha3_512
        from random import uniform as random_uniform

        content_digest = sha3_512(content).digest()
        signature_digest = sha3_512(signature).digest()
        
        split_ratio = random_uniform(0.30, 0.70)

        content_split_point = int(len(content_digest) * split_ratio)
        signature_split_point = len(signature_digest) - content_split_point

        fused_digest = content_digest[:content_split_point] + signature_digest[signature_split_point:]

        final_digest = sha3_512(fused_digest).hexdigest()

        return {
            'final_hash': final_digest,
            'split_ratio': split_ratio
        }


    def verify (self, content: bytes, signature:bytes, split_ratio: float, expected_hash: str) -> bool:
        """
        Verifies if the provided content and signature match the expected hash using the given split ratio.
        
        Args:
            content (bytes): The main content to verify
            signature (bytes): The secret signature that was used originally.
            split_ratio (float): The split ratio that was used during hash generation.
            expected_hash (str): The expected final hash to match against.

        Raises:
            InvalidSplitRatioError: If the provided split ratio is outside the allowed range (0.30 - 0.70).
        
        Returns:
            bool: True if the generated hash matches the expected hash, False otherwise.
        """

        if not (0.30 <= split_ratio <= 0.70):
            
            raise InvalidSplitRatioError(f'Split-Ratio needs to be between 0.30 and 0.70')

        from hashlib import sha3_512

        content_digest = sha3_512(content).digest()
        signature_digest = sha3_512(signature).digest()

        content_split_point = int(len(content_digest) * split_ratio)
        signature_split_point = len(signature_digest) - content_split_point

        fused_digest = content_digest[:content_split_point] + signature_digest[signature_split_point:]

        final_digest = sha3_512(fused_digest).hexdigest()

        return final_digest == expected_hash
