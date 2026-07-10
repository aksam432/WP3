"""Simplified Pydantic models for the MLIP ETL schema.

The models  avoid aliases and database-managed audit fields while
retaining the main schema constraints.
"""

from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field


Element = Literal[
    "H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne",
    "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar", "K", "Ca",
    "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn",
    "Ga", "Ge", "As", "Se", "Br", "Kr", "Rb", "Sr", "Y", "Zr",
    "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn",
    "Sb", "Te", "I", "Xe", "Cs", "Ba", "La", "Ce", "Pr", "Nd",
    "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb",
    "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg",
    "Tl", "Pb", "Bi", "Po", "At", "Rn", "Fr", "Ra", "Ac", "Th",
    "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm",
    "Md", "No", "Lr", "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds",
    "Rg", "Cn", "Nh", "Fl", "Mc", "Lv", "Ts", "Og",
]

ModelArchitecture = Literal[
    "DeepMD",
    "HDNNP",
    "ANI",
    "GAP",
    "SOAP",
    "MTP",
    "ACE",
    "NequIP",
    "Allegro",
    "M3GNet",
    "CHGNet",
    "SevenNet",
    "OrbNet",
    "MACE",
    "GRACE",
    "PET",
    "Custom",
]

TrainingStrategy = Literal["scratch", "fine-tune", "unknown"]
Prediction = Literal["E", "F", "S", "C"]
TargetSystem = Literal["organic", "materials", "liquids", "mixed"]
DatasetType = Literal["training", "validation", "test"]
TheoryLevel = Literal["DFT", "DFT+U"]
BenchmarkProtocolType = Literal["RDF", "Phonon"]

DiademProject = Literal[
    "2FAST",
    "FastNano",
    "ADAM",
    "A-DREAM",
    "AMETHYST",
    "DIAMS",
    "Highway2-Mat",
    "MOF Learning",
    "RUBIS",
    "MicroElec",
    "ARTEMIS",
    "ATHERM_COAT",
    "PHOTONIA",
    "FAST-IN FUELS",
]


class ModelParams(BaseModel):
    """Parameters and validation metrics associated with an MLIP model."""

    description: Optional[str] = None
    no_of_params: Optional[int] = Field(default=None, ge=0)
    config_file_path: Optional[str] = None
    cutoff_radius: Optional[float] = Field(
        default=None,
        gt=0,
        description="[Å]",
    )
    rmse_train_peratomenergy: Optional[float] = Field(
        default=None,
        ge=0,
        description="[meV/atom]",
    )
    rmse_val_peratomenergy: Optional[float] = Field(
        default=None,
        ge=0,
        description="[meV/atom]",
    )
    rmse_train_forces: Optional[float] = Field(
        default=None,
        ge=0,
        description="[meV/Å]",
    )
    rmse_val_forces: Optional[float] = Field(
        default=None,
        ge=0,
        description="[meV/Å]",
    )


class AtomisticEngine(BaseModel):
    """Atomistic or molecular-dynamics engine used with the model."""

    software: str
    version: Optional[str] = None
    pair_style: Optional[str] = None
    git_url: Optional[str] = None


class Model(BaseModel):
    """Validation of metadata related to an MLIP model."""

    title: str = Field(min_length=1)
    description: Optional[str] = None

    elements: List[Element] = Field(min_length=1, max_length=118)
    no_of_elements: Optional[int] = Field(default=None, ge=1, le=118)

    model_architecture: ModelArchitecture
    pretrained_variant: Optional[str] = None
    training_strategy: TrainingStrategy

    software_version: Optional[str] = None
    git_url: Optional[str] = None
    doi: Optional[str] = None

    model_params: Optional[ModelParams] = None
    diadem_project: Optional[DiademProject] = None

    prediction: List[Prediction] = Field(min_length=1, max_length=4)
    targeted_system: Optional[TargetSystem] = None
    target_properties: Optional[List[str]] = Field(default=None, max_length=10)

    atomistic_engines: Optional[List[AtomisticEngine]] = Field(
        default=None,
        max_length=10,
    )


class Kpoints(BaseModel):
    """K-point sampling information."""

    scheme: Optional[str] = None
    grid: Optional[List[int]] = Field(default=None, min_length=3, max_length=3)
    shift: Optional[List[float]] = Field(default=None, min_length=3, max_length=3)


class Smearing(BaseModel):
    """Electronic smearing details."""

    method: Optional[Union[str, int]] = None
    width: Optional[float] = Field(default=None, ge=0, description="[eV]")


class Pseudopotential(BaseModel):
    """Pseudopotential information."""

    elements: Optional[List[str]] = None
    functional: Optional[str] = None


class AbInitioMetadata(BaseModel):
    """Metadata extracted from an ab-initio calculation."""

    engine: str
    version: Optional[str] = None
    theory_level: Optional[TheoryLevel] = None
    functional: Optional[str] = None
    hubbard_u: Optional[float] = Field(default=None, ge=0, description="[eV]")
    cutoff: Optional[float] = Field(default=None, gt=0, description="[eV]")

    kpoints: Optional[Kpoints] = None
    smearing: Optional[Smearing] = None
    pseudopotential: Optional[Pseudopotential] = None

    energy_convergence: Optional[float] = Field(
        default=None,
        gt=0,
        description="[eV]",
    )
    force_convergence: Optional[float] = Field(
        default=None,
        description="[eV/Å]",
    )


class Dataset(BaseModel):
    """Validation of dataset metadata."""

    name: str = Field(min_length=1)
    description: Optional[str] = None
    type: DatasetType

    source: str = Field(min_length=1)
    target_system: Optional[TargetSystem] = None

    no_of_structures: Optional[int] = Field(default=None, ge=0)
    elements: List[Element] = Field(min_length=1, max_length=118)

    temperature_min: Optional[float] = Field(default=None, ge=0, description="[K]")
    temperature_max: Optional[float] = Field(default=None, ge=0, description="[K]")
    pressure_min: Optional[float] = Field(default=None, description="[GPa]")
    pressure_max: Optional[float] = Field(default=None, description="[GPa]")


class Benchmark(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    protocol_engine: Optional[str] = None
    protocol_type: Optional[BenchmarkProtocolType] = None
    protocol_params: Optional[Dict[str, Any]] = None
    log_file: Optional[str] = None


class Test(BaseModel):
    model_id: Optional[str] = None
    benchmark_id: Optional[str] = None
    result: Optional[bool] = None
    visibility: Optional[bool] = None
    log_file: Optional[str] = None


class CanonicalForm(BaseModel):
    """Composition of user form and extracted metadata."""

    model: Optional[Model] = None
    datasets: Optional[List[Dataset]] = None
    abinitio_metadata: Optional[AbInitioMetadata] = None
    benchmarks: Optional[List[Benchmark]] = None
    tests: Optional[List[Test]] = None