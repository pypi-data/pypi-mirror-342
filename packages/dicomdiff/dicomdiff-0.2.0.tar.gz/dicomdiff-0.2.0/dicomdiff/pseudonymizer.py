import pydicom
import os
import csv
from copy import deepcopy
from idiscore.core import Core, Profile
from idiscore.defaults import get_dicom_rule_sets


class Pseudonymizer:
    def pseudonimize(self, ds: pydicom.Dataset) -> pydicom.Dataset:
        """Pseudonymize the given DICOM dataset."""

        raise NotImplementedError("Pseudonymization logic not implemented.")


class PPDPPseudonymizer(Pseudonymizer):
    def pseudonimize(self, ds: pydicom.Dataset) -> pydicom.Dataset:
        """Pseudonymize the given DICOM dataset using PPDP."""

        original_root_dir = (
            "/Users/karim/Desktop/Werk/DICOM2/"
            "manifest-1617826555824/Pseudo-PHI-DICOM-Data"
        )

        ppdp_dir = (
            "/Users/karim/Desktop/Werk/DICOM Deidentified"
            "/manifest-1617826161202/Pseudo-PHI-DICOM-Data"
        )

        mapping_csv = "/Users/karim/Desktop/linked_paths5.csv"

        # Get full path of the input dataset
        ds_path = getattr(ds, "filename", None)
        if ds_path is None:
            raise ValueError("Dataset has no associated filename (ds.filename is None)")

        ds_path = os.path.normcase(os.path.abspath(ds_path))
        original_root_dir = os.path.normcase(os.path.abspath(original_root_dir))

        if not ds_path.startswith(original_root_dir):
            raise ValueError(
                f"{ds_path} is not under the expected root directory {original_root_dir}"
            )

        path_to_deid_path = {}
        with open(mapping_csv, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                orig_path = (
                    row["path_original"]
                    .strip()
                    .lstrip("./")
                    .replace("\r", "")
                    .replace("\n", "")
                )
                abs_orig_path = os.path.normcase(
                    os.path.abspath(os.path.join(original_root_dir, orig_path))
                )
                deid_path = row["path_deidentified"].strip()
                path_to_deid_path[abs_orig_path] = deid_path

        if ds_path not in path_to_deid_path:
            raise ValueError(f"File path {ds_path} not found in PPDP mapping")

        deid_rel_path = path_to_deid_path[ds_path]
        deid_full_path = os.path.join(ppdp_dir, deid_rel_path)

        if not os.path.exists(deid_full_path):
            raise FileNotFoundError(
                f"Mapped pseudonymized file does not exist: {deid_full_path}"
            )

        return pydicom.dcmread(deid_full_path)


class IDISPseudonymizer(Pseudonymizer):
    def pseudonimize(self, ds: pydicom.Dataset) -> pydicom.Dataset:
        """Pseudonymize the given DICOM dataset using IDIS."""

        sets = get_dicom_rule_sets()
        profile = Profile(rule_sets=[sets.basic_profile])
        core = Core(profile)
        ds_copy = deepcopy(ds)
        pseudonymized_ds = core.deidentify(ds_copy)
        return pseudonymized_ds
