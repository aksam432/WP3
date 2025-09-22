#!/usr/bin/env python3
"""This script defines and ETL script for :
1) Extracting data from userform
2) Extracting metadata from abinitio engines (for now VASP)
3) Transforming the data to fit the canonical schema
4) Loading the data to a yaml file
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime

from pydantic import BaseModel, Field

class ModelParams(BaseModel):
    description: Optional[str]
    no_of_params: Optional[int]
    config_file_path: Optional[str]
    cutoff_radius: Optional[float] = Field(None, description="[Å]")
    rmse_train_peratomenergy: Optional[float] = Field(None, description="[eV/atom or meV/atom by policy]")
    rmse_val_peratomenergy: Optional[float] = Field(None, description="[eV/atom or meV/atom by policy]")
    rmse_train_forces: Optional[float] = Field(None, description="[eV/Å]")
    rmse_val_forces: Optional[float] = Field(None, description="[eV/Å]")

class AtomisticEngine(BaseModel):
    software: str
    version: Optional[str]
    pair_style: Optional[str]
    git_url: Optional[str]

class Model(BaseModel):
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
    scheme: Optional[str]
    grid: Optional[List[int]]
    shift: Optional[List[float]]

class Smearing(BaseModel):
    method: Optional[str]
    width: Optional[float] = Field(None, description="[eV]")

class Pseudopotential(BaseModel):
    family: Optional[str]
    version: Optional[str]
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
    final_energy_ev: Optional[float]
    content_hash: Optional[str]
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

class UserForm(BaseModel):
    # top-level optional blocks — users can submit any subset of these
    model: Optional[Model]
    datasets: Optional[Dataset]
    abinitio_metadata: Optional[AbInitioInput]


class BaseEngineExtractor(ABC):
    @abstractmethod
    def extract(self, file_path: str) -> dict:
        pass

class VaspExtractor(BaseEngineExtractor):
    def __init__(self, file_path: str):
        self.path = file_path
    def extract(self) -> dict:
        pass


class ETL:
    def __init__(self, userform_path: str):
        pass
    def _load_form(self) -> UserForm:
        pass
    def _pick_engine(self) -> BaseEngineExtractor:
        pass
    def extract(self) -> dict:
        pass

def main():
    pass


if __name__ == "__main__":
    main()

        

