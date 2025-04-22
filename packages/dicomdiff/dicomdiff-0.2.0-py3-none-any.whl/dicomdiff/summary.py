import pandas as pd
import pydicom
from typing import List, Optional, Dict, Set, Tuple
from dicomdiff.pseudonymizer import PPDPPseudonymizer, IDISPseudonymizer
from dicomdiff.main import compare_dicom_datasets


class InconsistentPseudoError(Exception):
    pass


def generate_pseudonymization_summary(
    file_paths: List[str],
    limit: int = 500,
    output_csv: Optional[str] = None,
    check_consistency: bool = True,
) -> pd.DataFrame:
    file_paths = file_paths[:limit]

    tag_data = initialize_tag_data()
    tag_data = process_dicom_files(file_paths, tag_data, check_consistency)
    results = create_summary_results(tag_data)

    df = pd.DataFrame(results)
    df = df.sort_values("tag")

    if output_csv:
        df.to_csv(output_csv, index=False)
        print(f"Summary saved to {output_csv}")

    return df


def initialize_tag_data() -> Dict:
    return {
        "tag_summary": {},
        "tag_methods": {},
        "seen_files": {},
        "all_tags": set(),
        "tag_existence": {},
        "pseudonymizers": {"ppdp": PPDPPseudonymizer(), "idis": IDISPseudonymizer()},
    }


def process_dicom_files(
    file_paths: List[str], tag_data: Dict, check_consistency: bool
) -> Dict:
    """Process DICOM files and collect tag information."""
    for i, file_path in enumerate(file_paths):
        print(f"Processing file {i+1}/{len(file_paths)}: {file_path}")
        try:
            # Read the original DICOM file
            original_ds = pydicom.dcmread(file_path, force=True)

            process_original_dataset(original_ds, tag_data, file_path)
            process_ppdp_pseudonymization(original_ds, tag_data, file_path)
            process_idis_pseudonymization(original_ds, tag_data, file_path)
            track_tag_files(file_path, tag_data)

        except Exception as e:
            print(f"Error processing file {file_path}: {e}")

    if check_consistency:
        try:
            check_pseudonymization_consistency(
                tag_data["tag_methods"], tag_data["seen_files"]
            )
        except InconsistentPseudoError as e:
            # Log the inconsistency but continue processing
            print(
                f"Warning: {str(e)}\nContinuing with analysis despite inconsistencies."
            )
            tag_data["consistency_warnings"] = str(e)

    return tag_data


def process_original_dataset(original_ds, tag_data, file_path):
    tag_existence = tag_data["tag_existence"]
    tag_summary = tag_data["tag_summary"]
    all_tags = tag_data["all_tags"]

    for elem in original_ds:
        tag = format_tag(elem.tag)

        if tag not in tag_existence:
            tag_existence[tag] = {}
        if file_path not in tag_existence[tag]:
            tag_existence[tag][file_path] = {
                "original": False,
                "ppdp": False,
                "idis": False,
            }
        tag_existence[tag][file_path]["original"] = True

        all_tags.add(tag)
        if tag not in tag_summary:
            tag_summary[tag] = {"name": elem.name}


def process_ppdp_pseudonymization(original_ds, tag_data, file_path):
    try:
        ppdp_pseudo = tag_data["pseudonymizers"]["ppdp"]
        ppdp_ds = ppdp_pseudo.pseudonimize(original_ds)

        track_tags_in_dataset(ppdp_ds, file_path, "ppdp", tag_data)

        ppdp_diffs = compare_dicom_datasets(original_ds, ppdp_ds)

        process_differences(
            tag_data["tag_summary"],
            ppdp_diffs,
            "PPDP",
            tag_data["tag_methods"],
            file_path,
            file_tags=set(),
            all_tags=tag_data["all_tags"],
        )
    except Exception as e:
        print(f"Error with PPDP for file {file_path}: {e}")


def process_idis_pseudonymization(original_ds, tag_data, file_path):
    try:
        idis_pseudo = tag_data["pseudonymizers"]["idis"]
        idis_ds = idis_pseudo.pseudonimize(original_ds.copy())

        original_tags = {format_tag(elem.tag) for elem in original_ds}

        track_tags_in_dataset(idis_ds, file_path, "idis", tag_data, original_tags)

        idis_diffs = compare_dicom_datasets(original_ds, idis_ds)
        process_differences(
            tag_data["tag_summary"],
            idis_diffs,
            "IDIS",
            tag_data["tag_methods"],
            file_path,
            file_tags=set(),
            all_tags=tag_data["all_tags"],
        )
    except Exception as e:
        print(f"Error with IDIS for file {file_path}: {e}")


def track_tags_in_dataset(ds, file_path, method, tag_data, original_tags=None):
    tag_existence = tag_data["tag_existence"]
    tag_summary = tag_data["tag_summary"]
    all_tags = tag_data["all_tags"]

    for elem in ds:
        tag = format_tag(elem.tag)
        if tag not in tag_existence:
            tag_existence[tag] = {}

        if file_path not in tag_existence[tag]:
            tag_existence[tag][file_path] = {
                "original": False,
                "ppdp": False,
                "idis": False,
            }
        tag_existence[tag][file_path][method] = True

        if method == "idis" and original_tags is not None and tag not in original_tags:
            if tag not in tag_summary:
                tag_summary[tag] = {"name": elem.name}
            tag_summary[tag]["IDIS"] = "Created"

        all_tags.add(tag)


def track_tag_files(file_path, tag_data):
    all_tags = tag_data["all_tags"].copy()
    seen_files = tag_data["seen_files"]

    for tag in all_tags:
        if tag not in seen_files:
            seen_files[tag] = []
        seen_files[tag].append(file_path)


def create_summary_results(tag_data) -> List[Dict]:
    results = []
    all_tags = tag_data["all_tags"]
    tag_summary = tag_data["tag_summary"]
    tag_existence = tag_data["tag_existence"]

    for tag in all_tags:
        info = tag_summary.get(tag, {})

        ppdp_status, idis_status = determine_tag_status(tag, info, tag_existence)

        result = {
            "tag": tag,
            "name": info.get("name", "Unknown"),
            "PPDP": ppdp_status,
            "IDIS": idis_status,
            "comparison": compare_methods(ppdp_status, idis_status),
        }
        results.append(result)
    return results


def determine_tag_status(tag, info, tag_existence) -> Tuple[str, str]:
    ppdp_change = info.get("PPDP")
    idis_change = info.get("IDIS")

    patterns = analyze_tag_existence_patterns(tag, tag_existence)

    ppdp_status = determine_ppdp_status(ppdp_change, patterns)

    idis_status = determine_idis_status(idis_change, patterns)

    return ppdp_status, idis_status


def analyze_tag_existence_patterns(tag, tag_existence) -> Dict:
    patterns = {
        "tag_only_in_original": False,
        "tag_only_in_ppdp": False,
        "tag_only_in_idis": False,
        "tag_in_original_and_ppdp": False,
        "tag_in_original_and_idis": False,
    }

    for existence in tag_existence.get(tag, {}).items():
        orig = existence.get("original", False)
        ppdp = existence.get("ppdp", False)
        idis = existence.get("idis", False)

        if orig and not ppdp and not idis:
            patterns["tag_only_in_original"] = True
        if not orig and ppdp and not idis:
            patterns["tag_only_in_ppdp"] = True
        if not orig and not ppdp and idis:
            patterns["tag_only_in_idis"] = True
        if orig and ppdp:
            patterns["tag_in_original_and_ppdp"] = True
        if orig and idis:
            patterns["tag_in_original_and_idis"] = True

    return patterns


def determine_ppdp_status(ppdp_change: str, patterns: Dict[str, bool]) -> str:
    """Determine the PPDP status for a tag."""
    if ppdp_change:
        # If a specific change was detected by compare_dicom_datasets, use that
        return ppdp_change
    elif patterns["tag_only_in_ppdp"]:
        # Tag was created by PPDP
        return "Created"
    elif patterns["tag_in_original_and_ppdp"]:
        # Tag exists in both with no detected changes
        return "Unchanged"
    elif patterns["tag_only_in_original"]:
        # Tag was removed by PPDP
        return "Removed"
    else:
        # Tag doesn't exist in either dataset
        return "Not Present"


def determine_idis_status(idis_change: str, patterns: Dict[str, bool]) -> str:
    """Determine the IDIS status for a tag."""
    if idis_change == "Created":
        # If explicitly tagged as Created by our logic, keep it
        return "Created"
    elif idis_change:
        # If another specific change was detected, use that
        return idis_change
    elif patterns["tag_only_in_idis"]:
        # Tag was created by IDIS
        return "Created"
    elif patterns["tag_in_original_and_idis"]:
        # Tag exists in both with no detected changes
        return "Unchanged"
    elif patterns["tag_only_in_original"]:
        # Tag was removed by IDIS
        return "Removed"
    else:
        # Tag doesn't exist in either dataset
        return "Not Present"


def format_tag(tag):
    if isinstance(tag, int):
        group = tag >> 16
        element = tag & 0xFFFF
        return f"{group:04x},{element:04x}"
    return str(tag)


def process_differences(
    tag_summary: Dict[str, Dict[str, any]],
    differences: List[Dict[str, any]],
    method: str,
    tag_methods: Dict[str, Dict[str, Dict[str, Set[str]]]] = None,
    file_path: str = None,
    file_tags: Set[str] = None,
    all_tags: Set[str] = None,
):
    for diff in differences:
        if isinstance(diff["tag"], int):
            group = diff["tag"] >> 16
            element = diff["tag"] & 0xFFFF
            tag = f"{group:04x},{element:04x}"
        else:
            tag = diff["tag"]

        if all_tags is not None:
            all_tags.add(tag)

        if tag not in tag_summary:
            tag_summary[tag] = {"name": diff["name"]}

        if not (method == "IDIS" and tag_summary[tag].get("IDIS") == "Created"):
            tag_summary[tag][method] = diff["change_type"]

        if file_tags is not None:
            file_tags.add(tag)

        if tag_methods is not None and file_path is not None:
            if tag not in tag_methods:
                tag_methods[tag] = {"PPDP": {}, "IDIS": {}}

            if diff["change_type"] not in tag_methods[tag][method]:
                tag_methods[tag][method][diff["change_type"]] = set()

            tag_methods[tag][method][diff["change_type"]].add(file_path)


def check_pseudonymization_consistency(tag_methods, files):
    inconsistencies = []

    for tag, methods in tag_methods.items():
        for method_name, change_types in methods.items():
            if isinstance(change_types, dict) and len(change_types) > 1:
                inconsistency = {
                    "tag": tag,
                    "method": method_name,
                    "change_types": list(change_types.keys()),
                    "files": {},
                }
                for change_type, files in change_types.items():
                    inconsistency["files"][change_type] = list(files)

                inconsistencies.append(inconsistency)

    if inconsistencies:
        error_msg = "Inconsistent pseudonymization detected:\n"
        for inc in inconsistencies:
            error_msg += (
                f"Tag {inc['tag']} was handled inconsistently by {inc['method']}:\n"
            )
            for change_type, files in inc["files"].items():
                file_examples = files[:3]  # Show at most 3 examples
                error_msg += (
                    f"  - {change_type}: {len(files)} files, e.g., {file_examples}\n"
                )

        raise InconsistentPseudoError(error_msg)


def compare_methods(ppdp, idis):
    strictness = {
        "Removed": 4,
        "Not Present": 3,
        "Changed": 2,
        "Created": 1,
        "Unchanged": 0,
    }

    # Handle None values
    ppdp_val = ppdp if ppdp else "Not Present"
    idis_val = idis if idis else "Not Present"

    # If both are Not Present, they're equal
    if ppdp_val == "Not Present" and idis_val == "Not Present":
        return "Both Not Present"

    # If both are Unchanged, they're equal
    if ppdp_val == "Unchanged" and idis_val == "Unchanged":
        return "Both Unchanged"

    # Not Present is treated less strict than Unchanged
    if ppdp_val == "Not Present" and idis_val == "Unchanged":
        return "IDIS is stricter"
    if ppdp_val == "Unchanged" and idis_val == "Not Present":
        return "IDIS is more lenient"

    m1_strict = strictness.get(ppdp_val, 0)
    m2_strict = strictness.get(idis_val, 0)

    if m1_strict == m2_strict:
        return "Both methods are equal"
    elif m1_strict > m2_strict:
        return "IDIS is more lenient"
    else:
        return "IDIS is stricter"


def run_summary_for_test_files(output_csv: str = "result.csv", limit: int = 750):
    import os

    test_dir = (
        "/Users/karim/Desktop/Werk/DICOM2/manifest-1617826555824/Pseudo-PHI-DICOM-Data"
    )

    file_paths = []

    for root, _, files in os.walk(test_dir):
        for file in files:
            if file.endswith(".dcm"):
                file_path = os.path.join(root, file)
                try:
                    pydicom.dcmread(file_path, force=True)
                    file_paths.append(file_path)
                    if len(file_paths) >= limit:
                        break
                except Exception as e:
                    print(f"Skipping file {file_path}: {e}")
        if len(file_paths) >= limit:
            break

    print(f"Found {len(file_paths)} DICOM files.")
    return generate_pseudonymization_summary(file_paths, limit, output_csv)


if __name__ == "__main__":
    df = run_summary_for_test_files()
    print(df)
