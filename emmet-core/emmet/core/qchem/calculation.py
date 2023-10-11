"""Core definitions of a QChem calculation document."""

# mypy: ignore-errors

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import numpy as np
from pydantic import field_validator, BaseModel, Field, ConfigDict
from datetime import datetime
from pymatgen.io.qchem.inputs import QCInput
from pymatgen.io.qchem.outputs import QCOutput
from collections import OrderedDict
import re

from emmet.core.qchem.calc_types import (
    LevelOfTheory,
    CalcType,
    TaskType,
    level_of_theory,
    calc_type,
    task_type,
)

from emmet.core.qchem.task import QChemStatus

__author__ = "Rishabh D. Guha <rdguha@lbl.gov>"
logger = logging.getLogger(__name__)

# class QChemObject(ValueEnum):
# Not sure but can we have something like GRAD and HESS
# as QChem data objects


class CalculationInput(BaseModel):
    """
    Document defining QChem calculation inputs.
    """

    initial_molecule: Optional[Dict[str, Any]] = Field(
        None, description="input molecule geometry before the QChem calculation"
    )

    # parameters: Dict[str, Any] = Field(
    #     None, description = "Parameters from a previous QChem calculation."
    # )

    charge: int = Field(None, description="The charge of the input molecule")

    rem: Optional[Dict[str, Any]] = Field(
        None,
        description="The rem dict of the input file which has all the input parameters",
    )

    job_type: str = Field(
        None, description="The type of QChem calculation being performed"
    )

    opt: Optional[Dict[str, Any]] = Field(
        None,
        description="A dictionary of opt section. For instance atom constraints and fixed atoms. Go to QCInput definition for more details.",
    )

    pcm: Optional[Dict[str, Any]] = Field(
        None, description="A dictionary for the PCM solvent details if used"
    )

    solvent: Optional[Dict[str, Any]] = Field(
        None,
        description="The solvent parameters used if the PCM solvent model has been employed",
    )

    smx: Optional[Dict[str, Any]] = Field(
        None,
        description="A dictionary for the solvent parameters if the SMD solvent method has been employed",
    )

    vdw_mode: str = Field(
        None,
        description="Either atomic or sequential. Used when custon van der Waals radii are used to construct pcm cavity",
    )

    van_der_waals: Optional[Dict[str, Any]] = Field(
        None, description="The dictionary of the custom van der Waals radii if used"
    )

    scan_variables: Optional[Dict[str, Any]] = Field(
        None,
        description="The dictionary of scan variables for torsions or bond stretches",
    )

    tags: Union[Dict[str, Any], str] = Field(
        None, description="Any tags associated with the QChem calculation."
    )

    @classmethod
    def from_qcinput(cls, qcinput: QCInput) -> "CalculationInput":
        """
        Create a QChem input document from a QCInout object.

        Parameters
        ----------
        qcinput
            A QCInput object.

        Returns
        --------
        CalculationInput
            The input document.
        """
        print("the molecule \n")
        print(qcinput.molecule.as_dict())

        return cls(
            initial_molecule=qcinput.molecule.as_dict(),
            charge=int(qcinput.molecule.as_dict()["charge"])
            if qcinput.molecule.as_dict()
            else None,
            rem=qcinput.rem,
            job_type=qcinput.rem.get("job_type", None),
            opt=qcinput.opt,
            pcm=qcinput.pcm,
            solvent=qcinput.solvent,
            smx=qcinput.smx,
            vdw_mode=qcinput.vdw_mode,
            scan_variables=qcinput.scan,
            van_der_waals=qcinput.van_der_waals,
        )


class CalculationOutput(BaseModel):
    """Document defining QChem calculation outputs."""

    optimized_molecule: Optional[Dict[str, Any]] = Field(
        None,
        description="optimized geometry of the molecule after calculation in case of opt, optimization or ts",
    )

    mulliken: Optional[Union[List, Dict[str, Any]]] = Field(
        None, description="Calculate Mulliken charges on the atoms"
    )

    esp: Optional[Union[List, Dict[str, Any]]] = Field(
        None,
        description="Calculated charges on the atoms if esp calculation has been performed",
    )

    resp: Optional[Union[List, Dict[str, Any]]] = Field(
        None,
        description="Calculated charges on the atoms if resp calculation has been performed",
    )

    nbo_data: Optional[Dict[str, Any]] = Field(
        None, description="NBO data if analysis has been performed."
    )

    frequencies: Optional[Dict[str, Any]] = Field(
        None,
        description="Calculated frequency modes if the job type is freq or frequency",
    )

    frequency_modes: Union[List, str] = Field(
        None, description="The list of calculated frequency mode vectors"
    )

    final_energy: Optional[Union[str, float]] = Field(
        None,
        description="The final energy of the molecule after the calculation is complete",
    )

    enthalpy: Optional[Union[str, float]] = Field(
        None,
        description="The total enthalpy correction if a frequency calculation has been performed",
    )

    entropy: Optional[Union[str, float]] = Field(
        None,
        description="The total entropy of the system if a frequency calculation has been performed",
    )

    scan_energies: Optional[Dict[str, Any]] = Field(
        None,
        description="A dictionary of the scan energies with their respective parameters",
    )

    scan_geometries: Optional[Dict[str, Any]] = Field(
        None, description="optimized geometry of the molecules after the geometric scan"
    )

    scan_molecules: Optional[Dict[str, Any]] = Field(
        None,
        description="The constructed pymatgen molecules from the optimized scan geometries",
    )

    pcm_gradients: Optional[Union[Dict[str, Any], np.ndarray]] = Field(
        None,
        description="The parsed total gradients after adding the PCM contributions.",
    )

    @field_validator("pcm_gradients", mode="before")
    @classmethod
    def validate_pcm_gradients(cls, v):
        if v is not None and not isinstance(v, np.ndarray):
            raise ValueError("pcm_gradients must be a numpy array or None.")
        return v

    cds_gradients: Optional[Union[Dict[str, Any], np.ndarray]] = Field(
        None, description="The parsed CDS gradients."
    )

    @field_validator("cds_gradients", mode="before")
    @classmethod
    def validate_cds_gradients(cls, v):
        if v is not None and not isinstance(v, np.ndarray):
            raise ValueError("cds_gradients must be a numpy array or None.")
        return v

    dipoles: Optional[Dict[str, Any]] = Field(
        None, description="The associated dipoles for Mulliken/RESP/ESP charges"
    )

    gap_info: Optional[Dict[str, Any]] = Field(
        None, description="The Kohn-Sham HOMO-LUMO gaps and associated Eigenvalues"
    )

    @classmethod
    def from_qcoutput(cls, qcoutput: QCOutput) -> "CalculationOutput":
        """
        Create a QChem output document from a QCOutput object.

        Parameters
        ----------
        qcoutput
            A QCOutput object.

        Returns
        --------
        CalculationOutput
            The output document.
        """

        return cls(
            optimized_molecule=qcoutput.data.get(
                "molecule_from_optimized_geometry", {}
            ),
            mulliken=qcoutput.data.get(["Mulliken"][-1], []),
            esp=qcoutput.data.get(["ESP"][-1], []),
            resp=qcoutput.data.get(["RESP"][-1], []),
            nbo_data=qcoutput.data.get("nbo_data", {}),
            frequencies=qcoutput.data.get("frequencies", {}),
            frequency_modes=qcoutput.data.get("frequency_mode_vectors", []),
            final_energy=qcoutput.data.get("final_energy", None),
            enthalpy=qcoutput.data.get("enthalpy", None),
            entropy=qcoutput.data.get("entropy", None),
            scan_energies=qcoutput.data.get("scan_energies", {}),
            scan_geometries=qcoutput.data.get("optimized_geometries", {}),
            scan_molecules=qcoutput.data.get("molecules_from_optimized_geometries", {}),
            pcm_gradients=qcoutput.data.get(["pcm_gradients"][0], None),
            cds_gradients=qcoutput.data.get(["CDS_gradients"][0], None),
            dipoles=qcoutput.data.get("dipoles", None),
            gap_info=qcoutput.data.get("gap_info", None),
        )

    model_config = ConfigDict(arbitrary_types_allowed=True)
    # TODO What can be done for the trajectories, also how will walltime and cputime be reconciled


class Calculation(BaseModel):
    """Full QChem calculation inputs and outputs."""

    dir_name: str = Field(None, description="The directory for this QChem calculation")
    qchem_version: str = Field(
        None, description="QChem version used to perform the current calculation"
    )
    has_qchem_completed: Union[QChemStatus, bool] = Field(
        None, description="Whether QChem calculated the calculation successfully"
    )
    input: CalculationInput = Field(
        None, description="QChem input settings for the calculation"
    )
    output: CalculationOutput = Field(
        None, description="The QChem calculation output document"
    )
    completed_at: str = Field(
        None, description="Timestamp for when the calculation was completed"
    )
    task_name: str = Field(
        None,
        description="Name of task given by custodian (e.g. opt1, opt2, freq1, freq2)",
    )
    output_file_paths: Dict[str, Union[str, Path, Dict[str, Path]]] = Field(
        None,
        description="Paths (relative to dir_name) of the QChem output files associated with this calculation",
    )
    level_of_theory: LevelOfTheory = Field(
        None,
        description="Levels of theory used for the QChem calculation: For instance, B97-D/6-31g*",
    )
    task_type: TaskType = Field(
        None,
        description="Calculation task type like Single Point, Geometry Optimization. Frequency...",
    )
    calc_type: CalcType = Field(
        None,
        description="Combination dict of LOT + TaskType: B97-D/6-31g*/VACUUM Geometry Optimization",
    )

    @classmethod
    def from_qchem_files(
        cls,
        dir_name: Union[Path, str],
        task_name: str,
        qcinput_file: Union[Path, str],
        qcoutput_file: Union[Path, str],
        store_energy_trajectory: bool = False,
        qcinput_kwargs: Optional[Dict] = None,
        qcoutput_kwargs: Optional[Dict] = None,
    ) -> "Calculation":
        """
        Create a QChem calculation document from a directory and file paths.

        Parameters
        ----------
        dir_name
            The directory containing the QChem calculation outputs.
        task_name
            The task name.
        qcinput_file
            Path to the .in/qin file, relative to dir_name.
        qcoutput_file
            Path to the .out/.qout file, relative to dir_name.
        store_energy_trajectory
            Whether to store the energy trajectory during a QChem calculation #TODO: Revisit this- False for now.
        qcinput_kwargs
            Additional keyword arguments that will be passed to the qcinput file
        qcoutput_kwargs
            Additional keyword arguments that will be passed to the qcoutput file

        Returns
        -------
        Calculation
            A QChem calculation document.
        """

        dir_name = Path(dir_name)
        qcinput_file = dir_name / qcinput_file
        qcoutput_file = dir_name / qcoutput_file

        output_file_paths = _find_qchem_files(dir_name)

        qcinput_kwargs = qcinput_kwargs if qcinput_kwargs else {}
        qcinput = QCInput.from_file(qcinput_file, **qcinput_kwargs)
        print(qcinput)

        qcoutput_kwargs = qcoutput_kwargs if qcoutput_kwargs else {}
        qcoutput = QCOutput(qcoutput_file, **qcoutput_kwargs)

        completed_at = str(datetime.fromtimestamp(qcoutput_file.stat().st_mtime))

        input_doc = CalculationInput.from_qcinput(qcinput)
        output_doc = CalculationOutput.from_qcoutput(qcoutput)

        has_qchem_completed = (
            QChemStatus.SUCCESS
            if qcoutput.data.get("completion", [])
            else QChemStatus.FAILED
        )

        if store_energy_trajectory:
            print("Still have to figure the energy trajectory")

        return cls(
            dir_name=str(dir_name),
            task_name=task_name,
            qchem_version=qcoutput.data["version"],
            has_qchem_completed=has_qchem_completed,
            completed_at=completed_at,
            input=input_doc,
            output=output_doc,
            output_file_paths={
                k.lower(): Path(v)
                if isinstance(v, str)
                else {k2: Path(v2) for k2, v2 in v.items()}
                for k, v in output_file_paths.items()
            },
            level_of_theory=level_of_theory(input_doc.rem),
            task_type=task_type(input_doc.dict()),
            calc_type=calc_type(input_doc.dict()),
        )


def _find_qchem_files(
    path: Union[str, Path],
) -> Dict[str, Any]:
    """
    Find QChem files in a directory.

    Only the mol.qout file (or alternatively files
    with the task name as an extension, e.g., mol.qout.opt_0.gz, mol.qout.freq_1.gz, or something like this...)
    will be returned.

    Parameters
    ----------
    path
        Path to a directory to search.

    Returns
    -------
    Dict[str, Any]
        The filenames of the calculation outputs for each QChem task, given as a ordered dictionary of::

            {
                task_name:{
                    "qchem_out_file": qcrun_filename,
                },
                ...
            }
    If there is only 1 qout file task_name will be "standard" otherwise it will be the extension name like "opt_0"
    """
    path = Path(path)
    task_files = OrderedDict()
    print(Path)

    in_file_pattern = re.compile(r"^(?P<in_task_name>mol\.qin(?:\..+)?)\.gz$")
    print(in_file_pattern)

    for file in path.iterdir():
        if file.is_file():
            print(file.name)
            in_match = in_file_pattern.match(file.name)
            print(in_match)
            # out_match = out_file_pattern.match(file.name)
            if in_match:
                # print(in_task_name)
                in_task_name = in_match.group("in_task_name").replace("mol.qin.", "")
                print(in_task_name)
                # out_task_name = out_match.group('out_task_name').replace("mol.qout", "") #Remove mol.qout
                if in_task_name == "orig":
                    task_files[in_task_name] = {"orig_input_file": file}
                elif in_task_name == "mol.qin":
                    task_files["standard"] = {
                        "qchem_in_file": file,
                        "qchem_out_file": Path("mol.qout.gz"),
                    }
                else:
                    try:
                        task_files[in_task_name] = {
                            "qchem_in_file": file,
                            "qchem_out_file": Path("mol.qout." + in_task_name + ".gz"),
                        }
                    except FileNotFoundError:
                        task_files[in_task_name] = {
                            "qchem_in_file": file,
                            "qchem_out_file": "No qout files exist for this in file",
                        }

    return task_files
