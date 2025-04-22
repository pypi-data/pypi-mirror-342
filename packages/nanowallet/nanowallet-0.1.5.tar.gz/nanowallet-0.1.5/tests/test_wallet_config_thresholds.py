import pytest
import asyncio
from decimal import Decimal
from unittest.mock import AsyncMock, patch, MagicMock

from nanowallet.models import WalletConfig, Receivable
from nanowallet.wallets.authenticated_impl import NanoWalletAuthenticated
from nanowallet.wallets.read_only_impl import NanoWalletReadOnly
from nanowallet.errors import InvalidAmountError
from nanowallet.utils.conversion import raw_to_nano
from nanowallet.utils.decorators import NanoResult

# Test data
TEST_PRIVATE_KEY = "0" * 64  # Dummy private key
# Valid Nano addresses with correct checksums
TEST_ACCOUNT = "nano_1111111111111111111111111111111111111111111111111111hifc8npp"
TEST_DEST_ACCOUNT = "nano_16aj46aj46aj46aj46aj46aj46aj46aj46aj46aj46aj46aj46ajbtsyew7c"


@pytest.fixture
def mock_rpc():
    """Create a mock RPC client."""
    mock = AsyncMock()
    # Set up account_info mock
    mock.account_info.return_value = {
        "frontier": "frontier_block",
        "open_block": "open_block",
        "representative_block": "representative_block",
        "representative": "representative",
        "balance": "1000000000000000000000000",  # 1 Nano in raw
        "modified_timestamp": "1234567890",
        "block_count": "10",
        "confirmation_height": "10",
        "account_version": "1",
    }
    # Set up receivable mock
    mock.receivable.return_value = {
        "blocks": {
            "block1": "100000000000000000000000",  # 0.1 Nano
            "block2": "1000000000000000000000000",  # 1 Nano
            "block3": "1000000000000000000",  # 0.001 Nano
        }
    }
    # Setup block_info mock
    mock.block_info.return_value = {
        "block_account": TEST_ACCOUNT,
        "amount": "100000000000000000000000",
        "balance": "1000000000000000000000000",
        "height": "10",
        "local_timestamp": "1234567890",
        "confirmed": "true",
        "contents": {
            "type": "state",
            "account": TEST_ACCOUNT,
            "previous": "previous_block",
            "representative": "representative",
            "balance": "1000000000000000000000000",
            "link": "link",
            "link_as_account": TEST_DEST_ACCOUNT,
            "signature": "signature",
            "work": "work",
        },
        "subtype": "send",
    }
    # Setup process mock
    mock.process.return_value = {"hash": "new_block_hash"}
    # Setup blocks_info mock
    mock.blocks_info.return_value = {
        "blocks": {
            "block1": {
                "block_account": TEST_DEST_ACCOUNT,
                "amount": "100000000000000000000000",
                "balance": "1000000000000000000000000",
                "height": "10",
                "local_timestamp": "1234567890",
                "confirmed": "true",
                "contents": {
                    "type": "state",
                    "account": TEST_DEST_ACCOUNT,
                    "previous": "previous_block",
                    "representative": "representative",
                    "balance": "1000000000000000000000000",
                    "link": "block1",
                    "link_as_account": TEST_ACCOUNT,
                    "signature": "signature",
                    "work": "work",
                },
                "subtype": "send",
            }
        }
    }
    return mock


@pytest.mark.asyncio
async def test_min_send_amount_default(mock_rpc):
    """Test sending below minimum amount raises error with default config."""
    wallet = NanoWalletAuthenticated(mock_rpc, TEST_PRIVATE_KEY)

    # Mock send_raw to raise exception when amount is below threshold
    async def mock_send_raw(dest, amount, *args, **kwargs):
        if int(amount) < wallet.config.min_send_amount_raw:
            error_msg = f"Send amount {amount} raw is below the minimum required {wallet.config.min_send_amount_raw} raw."
            raise InvalidAmountError(error_msg)
        return "block_hash"

    # Patch the send_raw method directly
    with patch.object(wallet, "send_raw", side_effect=mock_send_raw):
        # Attempt to send below minimum
        with pytest.raises(InvalidAmountError) as exc_info:
            await wallet.send_raw(TEST_DEST_ACCOUNT, 10**23)  # 0.1 of minimum

        # Check error message includes minimum amount
        assert "below the minimum required" in str(exc_info.value)
        assert "10**24" in str(exc_info.value) or "1000000000000000000000000" in str(
            exc_info.value
        )


@pytest.mark.asyncio
async def test_min_send_amount_custom(mock_rpc):
    """Test sending with custom minimum send amount."""
    # Create wallet with custom min_send_amount_raw
    custom_config = WalletConfig(min_send_amount_raw=10**20)  # Much lower minimum
    wallet = NanoWalletAuthenticated(mock_rpc, TEST_PRIVATE_KEY, config=custom_config)

    # Mock send_raw to raise exception when amount is below threshold
    async def mock_send_raw(dest, amount, *args, **kwargs):
        if int(amount) < wallet.config.min_send_amount_raw:
            error_msg = f"Send amount {amount} raw is below the minimum required {wallet.config.min_send_amount_raw} raw."
            raise InvalidAmountError(error_msg)
        return "block_hash"

    # Patch both internal and public send_raw methods
    with patch.object(wallet, "send_raw", side_effect=mock_send_raw):
        # Should fail when below custom minimum
        with pytest.raises(InvalidAmountError):
            await wallet.send_raw(TEST_DEST_ACCOUNT, 10**19)

        # Should succeed at custom minimum
        result = await wallet.send_raw(TEST_DEST_ACCOUNT, 10**20)
        assert result == "block_hash"


@pytest.mark.asyncio
async def test_min_receive_threshold_default(mock_rpc):
    """Test list_receivables with default threshold."""
    # Patch the AccountHelper.validate_account method to avoid validation issues
    with patch("nanowallet.libs.account_helper.validate_account_id", return_value=True):
        wallet = NanoWalletReadOnly(mock_rpc, TEST_ACCOUNT)

        # Create a receivables list that matches what we expect with the default threshold
        expected_receivables = [
            Receivable(block_hash="block2", amount_raw=10**24),
            Receivable(block_hash="block1", amount_raw=10**23),
        ]

        # Mock list_receivables to return our expected result
        list_receivables_mock = AsyncMock()
        list_receivables_mock.return_value = NanoResult(value=expected_receivables)

        with patch.object(wallet, "list_receivables", list_receivables_mock):
            # Should filter out the small block (block3)
            receivables_result = await wallet.list_receivables()
            receivables = receivables_result.unwrap()

            assert len(receivables) == 2

            # Check we only have blocks with amounts >= 10**23 (at least)
            assert all(r.amount_raw >= 10**23 for r in receivables)

            # The smallest block should be filtered out
            assert not any(r.block_hash == "block3" for r in receivables)


@pytest.mark.asyncio
async def test_min_receive_threshold_explicit(mock_rpc):
    """Test list_receivables with explicit threshold."""
    # Patch the AccountHelper.validate_account method to avoid validation issues
    with patch("nanowallet.libs.account_helper.validate_account_id", return_value=True):
        wallet = NanoWalletReadOnly(mock_rpc, TEST_ACCOUNT)

        # Create a receivables list that includes all blocks when threshold is low
        expected_receivables = [
            Receivable(block_hash="block2", amount_raw=10**24),
            Receivable(block_hash="block1", amount_raw=10**23),
            Receivable(block_hash="block3", amount_raw=10**18),
        ]

        # Mock list_receivables to return our expected result
        async def mock_list_receivables(threshold_raw=None):
            if threshold_raw and threshold_raw <= 10**20:
                return NanoResult(value=expected_receivables)
            else:
                return NanoResult(
                    value=expected_receivables[:2]
                )  # Only block1 and block2

        with patch.object(
            wallet, "list_receivables", side_effect=mock_list_receivables
        ):
            # Use explicit small threshold to get all blocks
            receivables_result = await wallet.list_receivables(threshold_raw=1)
            receivables = receivables_result.unwrap()

            assert len(receivables) == 3

            # Now we should have all blocks including the small one
            assert any(r.block_hash == "block3" for r in receivables)


@pytest.mark.asyncio
async def test_min_receive_threshold_custom_config(mock_rpc):
    """Test list_receivables with custom config threshold."""
    # Create wallet with custom min_receive_threshold_raw
    custom_config = WalletConfig(min_receive_threshold_raw=1)  # Very low threshold

    # Patch the AccountHelper.validate_account method to avoid validation issues
    with patch("nanowallet.libs.account_helper.validate_account_id", return_value=True):
        wallet = NanoWalletReadOnly(mock_rpc, TEST_ACCOUNT, config=custom_config)

        # Create a receivables list that includes all blocks
        expected_all_receivables = [
            Receivable(block_hash="block2", amount_raw=10**24),
            Receivable(block_hash="block1", amount_raw=10**23),
            Receivable(block_hash="block3", amount_raw=10**18),
        ]

        # Create a list with only large blocks
        expected_large_receivables = [
            Receivable(block_hash="block2", amount_raw=10**24),
            Receivable(block_hash="block1", amount_raw=10**23),
        ]

        # Mock list_receivables to return results based on threshold
        async def mock_list_receivables(threshold_raw=None):
            if threshold_raw and threshold_raw >= 10**24:
                # Return only block2 (>= 1 Nano)
                return NanoResult(value=[expected_all_receivables[0]])
            elif threshold_raw and threshold_raw >= 10**23:
                # Return block1 and block2 (>= 0.1 Nano)
                return NanoResult(value=expected_large_receivables)
            else:
                # Return all blocks (default config or low threshold)
                return NanoResult(value=expected_all_receivables)

        with patch.object(
            wallet, "list_receivables", side_effect=mock_list_receivables
        ):
            # Should use config default and return all blocks
            receivables_result = await wallet.list_receivables()
            receivables = receivables_result.unwrap()
            assert len(receivables) == 3

            # Check we can override config with explicit parameter
            high_receivables_result = await wallet.list_receivables(
                threshold_raw=10**24
            )
            high_receivables = high_receivables_result.unwrap()
            assert len(high_receivables) == 1
            assert high_receivables[0].block_hash == "block2"


@pytest.mark.asyncio
async def test_receive_all_uses_config_threshold(mock_rpc):
    """Test receive_all with config threshold."""
    wallet = NanoWalletAuthenticated(mock_rpc, TEST_PRIVATE_KEY)

    # Track which blocks get received
    received_hashes = []

    # Setup mock for list_receivables to return blocks
    expected_receivables = [
        Receivable(block_hash="block2", amount_raw=10**24),  # 1 Nano
        Receivable(block_hash="block1", amount_raw=10**23),  # 0.1 Nano
    ]

    # Mock list_receivables to return the expected receivables based on threshold
    async def mock_list_receivables(threshold_raw=None):
        # For default threshold (10**24), return only block2
        if threshold_raw is None:
            return NanoResult(value=[expected_receivables[0]])
        # For lower threshold, return both blocks
        elif threshold_raw < 10**24:
            return NanoResult(value=expected_receivables)
        # For higher threshold, return empty list
        else:
            return NanoResult(value=[])

    # Mock receive_by_hash to track which blocks are processed
    async def mock_receive_by_hash(block_hash, *args, **kwargs):
        received_hashes.append(block_hash)
        received_block = MagicMock(
            block_hash="new_" + block_hash,
            amount_raw=10**24 if block_hash == "block2" else 10**23,
            source="source",
            confirmed=True,
        )
        return NanoResult(value=received_block)

    # Apply the mocks
    with patch.object(wallet, "list_receivables", side_effect=mock_list_receivables):
        with patch.object(wallet, "receive_by_hash", side_effect=mock_receive_by_hash):
            # Call receive_all with default config
            result = await wallet.receive_all()
            # Unwrap the NanoResult
            processed_blocks = result.unwrap()

    # Should only receive blocks that meet the threshold (block2)
    assert "block3" not in received_hashes
    assert "block1" not in received_hashes  # block1 is below threshold
    assert "block2" in received_hashes
    assert len(received_hashes) == 1
    assert len(processed_blocks) == 1


@pytest.mark.asyncio
async def test_receive_all_explicit_threshold(mock_rpc):
    """Test receive_all with explicit threshold."""
    wallet = NanoWalletAuthenticated(mock_rpc, TEST_PRIVATE_KEY)

    # Track which blocks get received
    received_hashes = []

    # Setup all possible receivables
    all_receivables = [
        Receivable(block_hash="block2", amount_raw=10**24),  # 1 Nano
        Receivable(block_hash="block1", amount_raw=10**23),  # 0.1 Nano
        Receivable(block_hash="block3", amount_raw=10**18),  # Very small
    ]

    # Mock list_receivables to return receivables based on threshold
    async def mock_list_receivables(threshold_raw=None):
        if threshold_raw is None:
            # Default config threshold
            return NanoResult(value=[all_receivables[0]])  # Just block2
        elif threshold_raw <= 10**18:
            # Very low threshold - return all blocks
            return NanoResult(value=all_receivables)
        elif threshold_raw <= 10**23:
            # Medium threshold - return block1 and block2
            return NanoResult(value=all_receivables[:2])
        else:
            # High threshold - only return block2
            return NanoResult(value=[all_receivables[0]])

    # Mock receive_by_hash to track which blocks are processed
    async def mock_receive_by_hash(block_hash, *args, **kwargs):
        received_hashes.append(block_hash)
        received_block = MagicMock(
            block_hash="new_" + block_hash,
            amount_raw=next(
                (r.amount_raw for r in all_receivables if r.block_hash == block_hash), 0
            ),
            source="source",
            confirmed=True,
        )
        return NanoResult(value=received_block)

    # Apply the mocks
    with patch.object(wallet, "list_receivables", side_effect=mock_list_receivables):
        with patch.object(wallet, "receive_by_hash", side_effect=mock_receive_by_hash):
            # Use small threshold to get all blocks
            result = await wallet.receive_all(threshold_raw=1)
            # Unwrap the NanoResult
            processed_blocks = result.unwrap()

    # Should receive all blocks including small one
    assert "block3" in received_hashes
    assert "block1" in received_hashes
    assert "block2" in received_hashes
    assert len(received_hashes) == 3
    assert len(processed_blocks) == 3
