# cython: boundscheck=False
# cython: wraparound=False

import binascii

cdef object hexlify = binascii.hexlify
del binascii


cpdef unicode cchecksum(
    str norm_address_no_0x, 
    const unsigned char[::1] address_hash_hex_no_0x,
):
    """
    Computes the checksummed version of an Ethereum address.

    This function takes a normalized Ethereum address (without the '0x' prefix) and its corresponding
    hash (also without the '0x' prefix) and returns the checksummed address as per the Ethereum
    Improvement Proposal 55 (EIP-55).

    Args:
        norm_address_no_0x: The normalized Ethereum address without the '0x' prefix.
        address_hash_hex_no_0x: The hash of the address, also without the '0x' prefix.

    Returns:
        The checksummed Ethereum address with the '0x' prefix.

    Examples:
        >>> cchecksum("b47e3cd837ddf8e4c57f05d70ab865de6e193bbb", "abcdef1234567890abcdef1234567890abcdef12")
        '0xB47E3Cd837DdF8E4C57F05D70Ab865De6E193BbB'

        >>> cchecksum("0000000000000000000000000000000000000000", "1234567890abcdef1234567890abcdef12345678")
        '0x0000000000000000000000000000000000000000'

    See Also:
        - :func:`eth_utils.to_checksum_address`: A utility function for converting addresses to their checksummed form.
    """
    cdef int i, address_char
        
    # Declare memoryviews for fixed-length data
    cdef const unsigned char[::1] norm_address_mv = norm_address_no_0x.encode('ascii')
    
    # Create a buffer for our result
    # 2 for "0x" prefix and 40 for the address itself
    cdef unsigned char[42] buffer = b'0x' + bytearray(40)
    
    with nogil:
        # Handle character casing based on the hash value
        for i in range(40):
            
            if address_hash_hex_no_0x[i] < 56:
                # '0' to '7' have ASCII values 48 to 55
                buffer[i + 2] = norm_address_no_0x[i]
                
            else:
                address_char = norm_address_no_0x[i]
                # This checks if `address_char` falls in the ASCII range for lowercase hexadecimal
                # characters ('a' to 'f'), which correspond to ASCII values 97 to 102. If it does,
                # the character is capitalized.
                buffer[i + 2] = address_char - 32 if 97 <= address_char <= 102 else address_char

    # It is faster to decode a buffer with a known size ie buffer[:42]
    return buffer[:42].decode('ascii')


cpdef unicode to_normalized_address_no_0x(value: Union[AnyAddress, str, bytes]):
    """
    Converts an address to its normalized hexadecimal representation without the '0x' prefix.

    This function ensures that the address is in a consistent lowercase hexadecimal
    format, which is useful for further processing or validation.

    Args:
        value: The address to be normalized.

    Raises:
        ValueError: If the input address is not in a recognized format.
        TypeError: If the input is not a string, bytes, or any address type.

    Examples:
        >>> to_normalized_address("0xB47E3CD837DDF8E4C57F05D70AB865DE6E193BBB")
        '0xb47e3cd837ddf8e4c57f05d70ab865de6e193bbb'

        >>> to_normalized_address(b'\xb4~<\xd87\xdd\xf8\xe4\xc5\x7f\x05\xd7\n\xb8e\xden\x19;\xbb')
        '0xb47e3cd837ddf8e4c57f05d70ab865de6e193bbb'

    See Also:
        - :func:`eth_utils.to_normalized_address` for the standard implementation.
    """
    cdef unicode hex_address_no_0x
    
    if isinstance(value, str):
        hex_address_no_0x = value
        hex_address_no_0x = hex_address_no_0x.lower()
        if hex_address_no_0x.startswith("0x"):
            hex_address_no_0x = hex_address_no_0x[2:]

        # if `hex_address_no_0x` has content, validate all characters are valid hex chars:
        if hex_address_no_0x:
            try:
                validate_hex_chars(hex_address_no_0x, value)
            except ValueError as e:
                raise ValueError("when sending a str, it must be a hex string. " f"Got: {repr(value)}") from e.__cause__

    elif isinstance(value, (bytes, bytearray)):
        hex_address_no_0x = (<bytes>hexlify(value)).decode("ascii")
        hex_address_no_0x = hex_address_no_0x.lower()

    else:
        raise TypeError(
            f"Unsupported type: '{repr(type(value))}'. Must be one of: bool, str, bytes, bytearray or int."
        )

    validate_hex_address(hex_address_no_0x, value)
    return hex_address_no_0x


cdef inline void validate_hex_address(unicode hex_address_no_0x, object original_value):
    if len(hex_address_no_0x) != 40:
        raise ValueError(
            f"Unknown format {repr(original_value)}, attempted to normalize to '0x{hex_address_no_0x}'"
        )
    validate_hex_chars(hex_address_no_0x, original_value)

    
cdef inline void validate_hex_chars(unicode string, object original_value):
    # NOTE: `string` should already be lowercase when passed in
    cdef char c
    for c in string:
        if c == 48:  # 0
            pass
        elif c == 49:  # 1
            pass
        elif c == 50:  # 2
            pass
        elif c == 51:  # 3
            pass
        elif c == 52:  # 4
            pass
        elif c == 53:  # 5
            pass
        elif c == 54:  # 6
            pass
        elif c == 55:  # 7
            pass
        elif c == 56:  # 8
            pass
        elif c == 57:  # 9
            pass
        elif c == 97:  # a
            pass
        elif c == 98:  # b
            pass
        elif c == 99:  # c
            pass
        elif c == 100:  # d
            pass
        elif c == 101:  # e
            pass
        elif c == 102:  # f
            pass
        else:
            raise ValueError(
                f"Unknown format {repr(original_value)}, attempted to normalize to '0x{string}'"
            )
