#!/usr/bin/env python3
"""This script defines an ETL script for :
1) Extracting data from userform
2) Extracting metadata from abinitio engines (for now VASP)
3) Transforming the data to fit the canonical schema
4) Loading the data to a yaml file
"""
from __future__ import annotations

import argparse
import json
import re
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Iterable, Optional
from pymatgen.io.vasp.outputs import Vasprun

from model.mlip_schema import (
    AbInitioMetadata,
    Kpoints,
    Pseudopotential,
    Smearing,
)


class BaseEngineExtractor(ABC):
    @abstractmethod
    def extract(self, file_path: str) -> dict:
        pass

class VaspExtractor(BaseEngineExtractor):
    def __init__(self, file_path: str):
        self.path = file_path
    def extract(self) -> dict:
        vasprun_data = Vasprun(self.path)
        metadata ={
            "engine": "VASP",
            "version": vasprun_data.vasp_version,
            "theory_level": ["DFT+U" if vasprun_data.is_hubbard else "DFT"],
            "functional": vasprun_data.run_type ,
            "cutoff": vasprun_data.incar.get("ENCUT"),
         #   "kpoints": {
                "scheme": vasprun_data.kpoints.style.name,
                "grid": vasprun_data.kpoints.kpts[0],
                "shift": vasprun_data.kpoints.kpts_shift,
         #   },
            "smearing": {
                "method": vasprun_data.incar.get("ISMEAR"),
                "width": vasprun_data.incar.get("SIGMA")
            },
            "pseudopotential": { "element":vasprun_data.potcar_symbols               
            },
            "energy_convergence": vasprun_data.incar.get("EDIFF"),
            "force_convergence": vasprun_data.incar.get("EDIFFG")
        }
        return metadata
    

class Cp2kExtractor(BaseEngineExtractor):

    def __init__(self, input_file: str):
        self.path = input_file

    def extract(self) -> dict:

        cp2k = Cp2kInput.from_file(self.path)

        dft = cp2k["FORCE_EVAL"]["DFT"]

        xc = dft["XC"]["XC_FUNCTIONAL"]

        functional = list(xc.subsections.keys())[0]

        hubbard = None
        if "DFT_PLUS_U" in str(dft):
            hubbard = ...

        metadata = {
            "engine": "CP2K",
            "version": None,
            "theory_level": "DFT+U" if hubbard else "DFT",
            "functional": functional,
            "cutoff": dft["MGRID"]["CUTOFF"].values[0],
            "energy_convergence": dft["SCF"]["EPS_SCF"].values[0],
        }

        return metadata


def run_etl(input_yaml_path: str, vasp_xml_path: Optional[str] ) -> Dict[str, Any]:
    """ Extracts data from the userform/canonical form and vaspxml file and outputs full canonical form in dict format

    Args:
        input_path (str): path to the userform 

    Returns:
        Dict: returns full canonical form as dictionary
    """
    with open(input_yaml_path,'r') as f:
        canonical_data = yaml.load(f, Loader=yaml.SafeLoader)

    if  canonical_data["Abinitio_metadata"]:
        abm = VaspExtractor(vasp_xml_path).extract()
        canonical_data["Abinitio_metadata"] = abm                #Changes from imanol

   
    #try:
    #    doc = CanonicalForm(**canonical_data)
    #except ValidationError as e:
    #    raise SystemExit(f"[Validation] Canonical YAML invalid:\n{e}")
    """
    # If abinitio present, just validate & output
    if doc.abinitio_metadata is not None:
        out = {
            "model": to_dict(doc.model) if doc.model else None,
            "datasets": [to_dict(d) for d in (doc.datasets or [])] or None,
            "abinitio_metadata": to_dict(doc.abinitio_metadata),
        }
        return {k: v for k, v in out.items() if v is not None}

    # Otherwise, require vasprun.xml, extract & fill
    if not vasprun_xml_path:
        raise SystemExit("abinitio_metadata missing in YAML. Provide --vaspxml path to vasprun.xml.")

    abm = extract_vasp_abinitio(vasp_xml_path)
    out = {
        "model": to_dict(doc.model) if doc.model else None,
        "datasets": [to_dict(d) for d in (doc.datasets or [])] or None,
        "abinitio_metadata": abm,
    }
    return {k: v for k, v in out.items() if v is not None}
    """
    return canonical_data

def main():
    parser= argparse.ArgumentParser(description="ETL for MLIP models")
    parser.add_argument("--input", required=True, help="Path to canonical YAML file")
    parser.add_argument("--vaspxml", required=False, help="Path to vasprun.xml (used if YAML lacks abinitio_metadata)")
    args = parser.parse_args()

    result = run_etl(args.input, args.vaspxml)
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()

        

