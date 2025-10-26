from typing import Dict, Tuple

from baml_client import b


def scrub_document(text: str) -> Tuple[str, Dict[str, str]]:
    # Extract PII from the document
    result = b.ExtractPII(text)

    # Create a mapping of real values to scrubbed placeholders
    scrubbed_text = text
    pii_mapping = {}

    # Process each PII item and replace with a placeholder
    for pii_item in result.privateData:
        pii_type = pii_item.dataType.upper()
        placeholder = f"[{pii_type}_{pii_item.index}]"

        # Store the mapping for reference
        pii_mapping[placeholder] = pii_item.value

        # Replace the PII with the placeholder
        scrubbed_text = scrubbed_text.replace(pii_item.value, placeholder)

    return scrubbed_text, pii_mapping


def restore_document(scrubbed_text: str, pii_mapping: Dict[str, str]) -> str:
    """Restore the original text using the PII mapping."""
    restored_text = scrubbed_text
    for placeholder, original_value in pii_mapping.items():
        restored_text = restored_text.replace(placeholder, original_value)
    return restored_text


# Example usage
document = """
John Smith works at Tech Corp.
You can reach him at john.smith@techcorp.com
or call 555-0123 during business hours.
His employee ID is TC-12345.
"""

# Scrub the document
scrubbed_text, pii_mapping = scrub_document(document)

print("Original Document:")
print(document)
print("\nScrubbed Document:")
print(scrubbed_text)
print("\nPII Mapping:")
for placeholder, original in pii_mapping.items():
    print(f"{placeholder}: {original}")

# If needed, restore the original document
restored_text = restore_document(scrubbed_text, pii_mapping)
print("\nRestored Document:")
print(restored_text)
