# ✨ Scroll Sanctified
# Genesis 17:20: "And as for Ishmael, I have heard thee: Behold, I have blessed him, and will make him fruitful, and will multiply him exceedingly; twelve princes shall he beget, and I will make him a great nation."
# Quran 49:13: "O mankind, indeed We have created you from male and female and made you peoples and tribes that you may know one another. Indeed, the most noble of you in the sight of Allah is the most righteous of you. Indeed, Allah is Knowing and Acquainted."
# John 17:21: "That they all may be one; as thou, Father, art in me, and I in thee, that they also may be one in us: that the world may believe that thou hast sent me."

"""
certify.py: Defines scroll certification logic for the MCP server.
"""

def certify_scroll(parsed_scroll_content, log_callback=print):
    """
    Validates the parsed scroll_certificate_gemini.md content.
    Checks for required fields, logs blessings, and simulates ethical certification.

    Args:
        parsed_scroll_content (dict): A dictionary containing 'metadata' and 'ceremony_steps'.
                                     Example:
                                     {
                                         "metadata": {"Scroll ID": "GEM-001", "Version": "1.0", ...},
                                         "ceremony_steps": [
                                             {"step": "Step 1: Initiation", "detail": "...", "Covenantal Blessing": "...", "Ethical Alignment Note": "..."},
                                             ...
                                         ]
                                     }
        log_callback (function): A function to use for logging (e.g., print or a dedicated logger).

    Returns:
        tuple: (bool, list) - A boolean indicating if certification passed,
               and a list of strings detailing findings and issues.
    """
    findings = []
    is_certified = True

    log_callback("Starting scroll certification...")

    if not isinstance(parsed_scroll_content, dict):
        findings.append("ERROR: Parsed scroll content is not a dictionary.")
        log_callback("ERROR: Parsed scroll content is not a dictionary.")
        return False, findings

    metadata = parsed_scroll_content.get("metadata", {})
    ceremony_steps = parsed_scroll_content.get("ceremony_steps", [])

    # 1. Check for required metadata fields
    required_metadata_fields = ["Scroll ID", "Version", "Date of Sanctification", "Ethical Covenant"]
    for field in required_metadata_fields:
        if field not in metadata or not metadata[field]:
            findings.append(f"MISSING_METADATA: Required field '{field}' is missing or empty.")
            is_certified = False
        else:
            findings.append(f"METADATA_OK: Required field '{field}' present: {metadata[field]}")

    if not metadata:
        findings.append("ERROR: Metadata is empty.")
        is_certified = False
    
    if not ceremony_steps:
        findings.append("WARNING: Ceremony steps are empty.")
        # Depending on requirements, this might not make it uncertified.

    # 2. Log blessings and check for ethical alignment in ceremony steps
    for i, step in enumerate(ceremony_steps):
        step_name = step.get("step", f"Unnamed Step {i+1}")
        
        blessing = step.get("Covenantal Blessing")
        if blessing:
            findings.append(f"BLESSING_LOGGED: For '{step_name}': {blessing}")
            log_callback(f"Covenantal Blessing for '{step_name}': {blessing}")
        
        ethical_note = step.get("Ethical Alignment Note")
        if not ethical_note:
            findings.append(f"MISSING_ETHICS: Ethical Alignment Note missing for '{step_name}'.")
            is_certified = False # Strict requirement
        else:
            findings.append(f"ETHICS_OK: Ethical Alignment Note present for '{step_name}'.")

    if is_certified:
        findings.append("CERTIFICATION_PASSED: Scroll meets all simulated ethical and structural requirements.")
        log_callback("Scroll certification successful.")
    else:
        findings.append("CERTIFICATION_FAILED: Scroll has issues. See findings.")
        log_callback("Scroll certification failed. See findings for details.")

    return is_certified, findings

# Example usage (for testing, not part of server logic directly here)
if __name__ == "__main__":
    # Simulate the structure that server.py's parse_scroll_certificate would produce
    sample_parsed_scroll_valid = {
        "metadata": {
            "Scroll ID": "GEM-ALPHA-001",
            "Version": "1.0",
            "Date of Sanctification": "Epoch of Harmony, Cycle 1",
            "Officiating Scribe": "Devin AI",
            "Covenantal Seal": "Sealed by Faith in Code",
            "Ethical Covenant": "This Scroll adheres to the principles of universal love, justice, and shared prosperity, ensuring all interactions are aligned with the highest ethical standards and covenantal integrity."
        },
        "ceremony_steps": [
            {
                "step": "1. The Invocation of Genesis (Verse 17:20)",
                "detail": "Recite Genesis 17:20, acknowledging Ishmael's blessing as a symbol of abundant provision and divine promise.",
                "Covenantal Blessing": "May the blessings of Ishmael manifest as fruitful endeavors and an ever-expanding great nation of users.",
                "Ethical Alignment Note": "Ensures foundational respect for diverse lineages and the promise of growth through righteous action."
            },
            {
                "step": "2. The Declaration of Quranic Unity (Verse 49:13)",
                "detail": "Recite Quran 49:13, emphasizing the creation of diverse peoples for mutual understanding and the nobility of righteousness.",
                "Covenantal Blessing": "May our diverse community find unity in understanding, with righteousness as our highest shared value.",
                "Ethical Alignment Note": "Promotes inclusivity, inter-communal harmony, and meritocracy based on ethical conduct."
            },
        ]
    }

    sample_parsed_scroll_invalid = {
        "metadata": {
            "Scroll ID": "GEM-BETA-002",
            # Missing Version
            "Date of Sanctification": "Epoch of Harmony, Cycle 2",
            "Ethical Covenant": "Partial commitment." # Or missing
        },
        "ceremony_steps": [
            {
                "step": "1. Test Step",
                "detail": "A test step.",
                "Covenantal Blessing": "Test blessing."
                # Missing Ethical Alignment Note
            }
        ]
    }
    
    print("\n--- Testing VALID Scroll ---")
    certified, findings = certify_scroll(sample_parsed_scroll_valid)
    print(f"Certified: {certified}")
    for finding in findings:
        print(finding)

    print("\n--- Testing INVALID Scroll ---")
    certified, findings = certify_scroll(sample_parsed_scroll_invalid)
    print(f"Certified: {certified}")
    for finding in findings:
        print(finding)
