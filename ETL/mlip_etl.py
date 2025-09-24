#!/usr/bin/env python3
"""This script defines and ETL script for :
1) Extracting data from userform
2) Extracting metadata from abinitio engines (for now VASP)
3) Transforming the data to fit the canonical schema
4) Loading the data to a yaml file
"""
from __future__ import annotations
import argparse
from abc import ABC, abstractmethod
from datetime import datetime
from pymatgen.io.vasp  import Vasprun


from pydantic import BaseModel, Field

class ModelParams(BaseModel):
    """ Validation of parameters relate to base model
    """
    description: Optional[str]
    no_of_params: Optional[int]
    config_file_path: Optional[str]
    cutoff_radius: Optional[float] = Field(None, description="[Å]")
    rmse_train_peratomenergy: Optional[float] = Field(None, description="[meV/atom ]")
    rmse_val_peratomenergy: Optional[float] = Field(None, description="[meV/atom ]")
    rmse_train_forces: Optional[float] = Field(None, description="[meV/Å]")
    rmse_val_forces: Optional[float] = Field(None, description="[meV/Å]")

class AtomisticEngine(BaseModel):
    """ Validation of parameters related to  MD engine used to run the model
    """
    software:Optional[str]
    version: Optional[str]
    pair_style: Optional[str]
    git_url: Optional[str]

class Model(BaseModel):
    """ Validation of parameters related to MLIP model
    """
    title: str
    description: Optional[str]
    elements: Union[str, List[str]]
    no_of_elements: Optional[int]
    model_type: str
    pretrained_variant: Optional[str]
    training_strategy: str
    software_version: str
    git_url: Optional[str]
    DOI: Optional[str]
    model_params: Optional[ModelParams]
    diadem_project: Optional[str]
    prediction: List[str]
    targeted_system: Optional[str]
    target_properties: Optional[str]
    atomistic_engines: Optional[AtomisticEngine]
    date_of_creation: datetime = Field(default_factory=datetime.utcnow)




class Kpoints(BaseModel):
    """ Kpoints information
    """
    scheme: Optional[str]
    grid: Optional[List[int]]
    shift: Optional[List[float]]

class Smearing(BaseModel):
    """ smearing details
    """
    method: Optional[str]
    width: Optional[float] = Field(None, description="[eV]")

class Pseudopotential(BaseModel):
    """ Validation of pseudopotential 
    """
    elements: Optional[List[str]]

class AbInitioMetadata(BaseModel):
    engine: str
    version: Optional[str]
    theory_level: Optional[str]
    functional: Optional[str]
    cutoff: Optional[float] = Field(None, description="[eV]")
    kpoints: Optional[Kpoints]
    smearing: Optional[Smearing]
    pseudopotential: Optional[Pseudopotential]
    energy_convergence: Optional[float] = Field(None, description="[eV]")
    force_convergence: Optional[float] = Field(None, description="[eV/Å]")
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Dataset(BaseModel):
    name: str
    description: Optional[str]
    type: str = Field(..., description="Training_set | Validation_set | Test_set")
    source: str
    target_system: Optional[str]
    no_of_structures: Optional[int]
    elements: Union[str, List[str]]
    temperature_min: Optional[float]
    temperature_max: Optional[float]
    pressure_min: Optional[float]
    pressure_max: Optional[float]
    created_at: datetime = Field(default_factory=datetime.utcnow)

class CanonicalForm(BaseModel):
    """ Composition of userform data
    """
  
    model: Optional[Model]
    datasets: [Dataset]
    abinitio_metadata: Optional[AbInitioInput]


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


def run_etl(input_path: str, vasp_xml_path: str ) -> Dict:
    """ Extracts data from the userform/canonical form and vaspxml file and outputs full canonical form in dict format

    Args:
        input_path (str): path to the userform 

    Returns:
        Dict: returns full canonical form as dictionary
    """
    pass

def main():
    parser= argparse.ArgumentParser(description="ETL for MLIP models")
    parser.add_argument('--vaspxml', type=str, required=True, help="Path to vasprun.xml file")

    args= parser.parse_args()
    vasp_extractor= VaspExtractor(args.vaspxml)
    vasp_metadata= vasp_extractor.extract()
    print(vasp_metadata)

if __name__ == "__main__":
    main()

        

