import sys
import os
import time
from pathlib import Path

# --- Test Setup: Add src directory to sys.path ---
# This allows importing 'whatsapp' as if it were installed
# Note: This is specific to this testing approach. Standard test runners
# might handle this differently (e.g., pytest with src layout).
try:
    # Resolve the project root directory (assuming tests/ is one level down from root)
    project_root = Path(__file__).resolve().parent.parent
    src_path = project_root / "src"
    if str(src_path) not in sys.path:
        print(f"Adding {src_path} to sys.path for testing.")
        sys.path.insert(0, str(src_path))
except Exception as e:
    print(f"Error adjusting sys.path: {e}. Imports might fail.", file=sys.stderr)
    sys.exit(1)  # Exit if path setup fails

# --- Now import the package ---
# Imports should work now because src/ is in sys.path
try:
    from whatsapp_bridge import (
        WhatsappClient,
        WhatsappPkgError,
        BridgeError,
        __version__,
    )

    print(f"Imported whatsapp_bridge version {__version__}")
except ImportError as e:
    print(
        f"Failed to import whatsapp_bridge after adjusting sys.path: {e}",
        file=sys.stderr,
    )
    print(f"Current sys.path: {sys.path}", file=sys.stderr)
    sys.exit(1)

# --- Main Test Logic (Adapted from Usage.py) ---


def run_test():
    """Runs the integration test steps."""
    client = None  # Initialize client to None for finally block
    print("\n>>> Initializing WhatsApp Bridge Client for Test...")
    try:
        # Initialize with auto_setup and auto_connect for a full test
        # Consider making these False for more granular unit tests later
        client = WhatsappClient(auto_setup=True, auto_connect=True)
        print("Client initialized and bridge connected successfully.")

    except (WhatsappPkgError, BridgeError) as e:
        print(f"TEST FAILED: Failed to initialize client: {e}", file=sys.stderr)
        # No cleanup needed here as client likely didn't fully initialize or connect
        return  # Exit the test function on failure
    except KeyboardInterrupt:
        print("\nTest interrupted during initialization.")
        # Attempt cleanup if client object exists
        if client and hasattr(client, "disconnect"):
            print("Attempting disconnect...")
            client.disconnect()
        return  # Exit test

    # --- Sending Messages Test ---
    print(f"\n>>> Sending Test Message...")
    try:
        # IMPORTANT: Replace with a valid JID or phone number for testing
        # Using a placeholder that likely won't work unless configured
        test_recipient = os.getenv(
            "WHATSAPP_TEST_RECIPIENT", "1234567890@s.whatsapp.net"
        )  # Example JID
        print(f"   Recipient: {test_recipient}")

        # Construct a unique message for testing
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        test_message = (
            f"Automated test message from whatsapp_bridge v{__version__} at {timestamp}"
        )

        if client.send_message(test_recipient, test_message):
            print("Test message sent successfully (API success).")
        else:
            print(
                "TEST FAILED: Failed to send test message (API failure).",
                file=sys.stderr,
            )
            # Decide if test should continue or stop here

        # --- Sending Media Test (Optional) ---
        # --- Sending Media Test (Optional) ---
        # Uncomment and provide a valid path to test media sending
        # test_media_path = "path/to/your/test_image.jpg"
        # if os.path.exists(test_media_path):
        #    print(f"\n>>> Sending Test Media File {test_media_path}...")
        #    if client.send_media(test_recipient, test_media_path, caption="Test Media"):
        #        print("   Test media sent successfully (API success).")
        #    else:
        #        print(f"TEST FAILED: Failed to send test media {test_media_path} (API failure).", file=sys.stderr)
        # else:
        #    print(f"Skipping media test: File not found at {test_media_path}")

    except BridgeError as e:
        print(
            f"TEST FAILED: Bridge Error during sending: {e}. Cannot perform action.",
            file=sys.stderr,
        )
    except Exception as e:
        print(
            f"TEST FAILED: An unexpected error occurred during sending: {e}",
            file=sys.stderr,
        )

    # --- Receiving New Messages Test (Polling Example) ---
    # This part is harder to automate reliably without a dedicated test account
    # or mocking. Running a short poll as a basic check.
    print("\n>>> Checking for New Messages (Short Poll)...")
    try:
        # Check only once or twice for the test
        for i in range(2):
            print(f"\n[{time.strftime('%H:%M:%S')}] Polling attempt {i+1}...")
            # Access bridge manager via client attribute (assuming it's public or semi-public)
            # Note: Accessing _bridge_manager is using an internal detail, might change.
            if not client._bridge_manager.check_if_alive():
                print("TEST FAILED: Bridge process died unexpectedly.", file=sys.stderr)
                break

            new_messages = client.get_new_messages(
                download_media=True
            )  # Test with auto-download

            if new_messages:
                print(f"   Received {len(new_messages)} New Message(s):")
                for msg in new_messages:
                    local_timestamp_str = (
                        msg["timestamp"].astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
                    )
                    sender = msg.get(
                        "sender", "Unknown"
                    )  # Handle potential missing sender
                    content = msg.get("content", "")
                    media_info = ""
                    if msg.get("media_type"):
                        media_info = (
                            f" [{msg['media_type']}: {msg.get('filename', 'N/A')}]"
                        )
                        local_path = msg.get("local_media_path")
                        if local_path:
                            if "FAILED" in local_path or "ERROR" in local_path:
                                media_info += f" (Download Status: {local_path})"
                            else:
                                media_info += (
                                    f" (Downloaded: {os.path.basename(local_path)})"
                                )

                    print(
                        f"     [{local_timestamp_str}] From: {sender} Chat: {msg.get('chat_jid', 'Unknown')}"
                    )
                    print(f"       Content: '{content}'{media_info}")
            else:
                print("   No new messages found during this poll.")

            if i < 1:
                wait_time = 5
                print(f"Waiting {wait_time} seconds before next poll...")
                time.sleep(wait_time)

    except KeyboardInterrupt:
        print("\nTest polling interrupted.")
    except BridgeError as e:
        print(f"\nTEST FAILED: Bridge Error during polling: {e}", file=sys.stderr)
    except Exception as e:
        print(f"\nTEST FAILED: Unexpected error during polling: {e}", file=sys.stderr)
    finally:
        # --- Test Cleanup ---
        print("\n>>> Test Finished: Disconnecting Bridge...")
        if client and hasattr(client, "disconnect"):
            client.disconnect()
        else:
            print("Client object not available for disconnect.")


# --- Script Execution ---
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print(" Starting WhatsApp Bridge Integration Test ".center(60))
    print("=" * 60)
    run_test()
    print("\n" + "=" * 60)
    print(" Test Script Completed ".center(60))
    print("=" * 60)
