from pathlib import Path
import pytest

@pytest.fixture(scope="session")
def test_dir():
    return Path(__file__).parent.parent.parent.joinpath("test_files").resolve()

def assert_schemas_equal(test_schema, valid_schema):
    """
    Recursively test all items in valid_schema are present and equal in test_schema.

    While test_schema can be a pydantic schema or dictionary, the valid schema must
    be a (nested) dictionary. This function automatically handles accessing the
    attributes of classes in the test_schema.

    Args:
        test_schema: A pydantic schema or dictionary of the schema.
        valid_schema: A (nested) dictionary specifying the key and values that must be
            present in test_schema. This is what the generated test_schema will be tested against
    """
    from pydantic import BaseModel

    if isinstance(valid_schema, dict):
        for key, sub_valid_schema in valid_schema.items():
            if isinstance(key, str) and hasattr(test_schema, key):
                sub_test_schema = getattr(test_schema, key)
            elif not isinstance(test_schema, BaseModel):
                sub_test_schema = test_schema[key]
            else:
                raise ValueError(f"{type(test_schema)} does not have field: {key}")
            return assert_schemas_equal(sub_test_schema, sub_valid_schema)

    elif isinstance(valid_schema, list):
        for i, sub_valid_schema in enumerate(valid_schema):
            return assert_schemas_equal(test_schema[i], sub_valid_schema)

    elif isinstance(valid_schema, float):
        assert test_schema == pytest.approx(valid_schema)
    else:
        assert test_schema == valid_schema

class SchemaTestData:
    """Dummy class to be used to contain all test data information"""

class SinglePointTest(SchemaTestData):
    
    folder = "qchem_sp_test"
    task_files = {
        "standard": {
            "input_file": "mol.qin.gz",
            "output_file": "mol.qout.gz",
        }
    }

    objects = {"standard": []}
    task_doc = {
    "calcs_reversed": [
        {
            "output": {
                "mulliken": {"O": -0.713178, "H": 0.357278, "H": 0.355900},
                "resp": {"O": -0.872759, "H": 0.436379, "H": 0.436379},
                "final_energy": -76.4493700739,
            },
            "input": {
                "charge": 0,
                "rem": {
                    "job_type": "sp",
                    "basis": "def2-qzvppd",
                    "max_scf_cycles": "100",
                    "gen_scfman": "true",
                    "xc_grid": "3",
                    "thresh": "14",
                    "s2thresh": "16",
                    "scf_algorithm": "diis",
                    "resp_charges": "true",
                    "symmetry": "false",
                    "sym_ignore": "true",
                    "method": "wb97mv",
                    "solvent_method": "smd",
                    "ideriv": "1",
                },
                "job_type": "sp",
            },
        }
    ],
    "input": {
        "molecule": {
            '@module': 'pymatgen.core.structure',
            '@class': 'Molecule',
            'charge': 0,
            'spin_multiplicity': 1,
            'sites': [
                {
                    'name': 'O',
                    'species': [{'element': 'O', 'occu': 1}],
                    'xyz': [-0.80595, 2.22952, -0.01914],
                    'properties': {},
                    'label': 'O'
                    },
                {
                    'name': 'H',
                    'species': [{'element': 'H', 'occu': 1}],
                    'xyz': [0.18338, 2.20176, 0.01351],
                    'properties': {},
                    'label': 'H'
                    },
                {
                    'name': 'H',
                    'species': [{'element': 'H', 'occu': 1}],
                    'xyz': [-1.09531, 1.61602, 0.70231],
                    'properties': {},
                    'label': 'H'
                }
            ]},
        "lev_theory": "wB97M-V/def2-QZVPPD/SMD",
        "task_type": "Single Point",
    },
    "output": {
        "mulliken": {"O": -0.713178, "H": 0.357278, "H": 0.355900},
        "resp": {"O": -0.872759, "H": 0.436379, "H": 0.436379},
        "final_energy": -76.4493700739,
    },
    "custodian": [
        {"job": {
            "@module": "custodian.qchem.jobs",
            "@class": "QCJob",
            "@version": "2022.5.26",
            "qchem_command": [
                "qchem"
            ],
            "max_cores": "40",
            "multimode": "openmp",
            "input_file": "mol.qin",
            "output_file": "mol.qout",
            "qclog_file": "mol.qclog",
            "suffix": "",
            "calc_loc": "/tmp",
            "nboexe": "null",
            "save_scratch": "false",
            "backup": "true"
             },
        "corrections": [],
        }
        ],
    }
        
class OptimizationTest(SchemaTestData):
    
    folder = "qchem_opt_test"
    task_files = {
        "standard": {
            "input_file": "mol.qin.gz",
            "output_file": "mol.qout.gz",
        }
    }

    objects = {"standard": []}
    task_doc = {
    "calcs_reversed": [
        {
            "output": {
                "optimized_molecule": {
                        '@module': 'pymatgen.core.structure',
                        '@class': 'Molecule',
                        'charge': 0,
                        'spin_multiplicity': 1,
                        'sites': [
                            {
                                'name': 'O',
                                'species': [{'element': 'O', 'occu': 1}],
                                'xyz': [-0.80086, 2.22483, -0.01362],
                                'properties': {},
                                'label': 'O'
                                },
                            {
                                'name': 'H',
                                'species': [{'element': 'H', 'occu': 1}],
                                'xyz': [0.16379, 2.19629, 0.01994],
                                'properties': {},
                                'label': 'H'
                                },
                            {
                                'name': 'H',
                                'species': [{'element': 'H', 'occu': 1}],
                                'xyz': [-1.08081, 1.62618, 0.69036],
                                'properties': {},
                                'label': 'H'
                            }
                        ]},
                "mulliken": {"O": -0.373491, "H": 0.186964, "H": 0.186527},
                "resp": {"O": -0.895220, "H": 0.447610, "H": 0.447610},
                "final_energy": -76.358341626913,
            },
            "input": {
                "charge": 0,
                "rem": {
                    "job_type": "sp",
                    "basis": "def2-qzvppd",
                    "max_scf_cycles": "100",
                    "gen_scfman": "true",
                    "xc_grid": "3",
                    "thresh": "14",
                    "s2thresh": "16",
                    "scf_algorithm": "diis",
                    "resp_charges": "true",
                    "symmetry": "false",
                    "sym_ignore": "true",
                    "method": "wb97mv",
                    "solvent_method": "smd",
                    "ideriv": "1",
                },
                "job_type": "sp",
            },
        }
    ],
    "input": {
        "molecule": {
            '@module': 'pymatgen.core.structure',
            '@class': 'Molecule',
            'charge': 0,
            'spin_multiplicity': 1,
            'sites': [
                {
                    'name': 'O',
                    'species': [{'element': 'O', 'occu': 1}],
                    'xyz': [-0.80595, 2.22952, -0.01914],
                    'properties': {},
                    'label': 'O'
                    },
                {
                    'name': 'H',
                    'species': [{'element': 'H', 'occu': 1}],
                    'xyz': [0.18338, 2.20176, 0.01351],
                    'properties': {},
                    'label': 'H'
                    },
                {
                    'name': 'H',
                    'species': [{'element': 'H', 'occu': 1}],
                    'xyz': [-1.09531, 1.61602, 0.70231],
                    'properties': {},
                    'label': 'H'
                }
            ]},
        "lev_theory": "wB97M-V/def2-SVPD/SMD",
        "task_type": "Geometry Optimization",
    },
    "output": {
        "optimized_molecule": {
            '@module': 'pymatgen.core.structure',
            '@class': 'Molecule',
            'charge': 0,
            'spin_multiplicity': 1,
            'sites': [
                {
                    'name': 'O',
                    'species': [{'element': 'O', 'occu': 1}],
                    'xyz': [-0.80086, 2.22483, -0.01362],
                    'properties': {},
                    'label': 'O'
                    },
                {
                    'name': 'H',
                    'species': [{'element': 'H', 'occu': 1}],
                    'xyz': [0.16379, 2.19629, 0.01994],
                    'properties': {},
                    'label': 'H'
                    },
                {
                    'name': 'H',
                    'species': [{'element': 'H', 'occu': 1}],
                    'xyz': [-1.08081, 1.62618, 0.69036],
                    'properties': {},
                    'label': 'H'
                }
                ]},
        "mulliken": {"O": -0.373491, "H": 0.186964, "H": 0.186527},
        "resp": {"O": -0.895220, "H": 0.447610, "H": 0.447610},
        "final_energy": -76.358341626913,
    },
    "custodian": [
        {"job": {
            "@module": "custodian.qchem.jobs",
            "@class": "QCJob",
            "@version": "2022.5.26",
            "qchem_command": [
                "qchem"
            ],
            "max_cores": "40",
            "multimode": "openmp",
            "input_file": "mol.qin",
            "output_file": "mol.qout",
            "qclog_file": "mol.qclog",
            "suffix": "",
            "calc_loc": "/tmp",
            "nboexe": "null",
            "save_scratch": "false",
            "backup": "true"
             },
        "corrections": [],
        }
        ],
    }

objects = {cls.__name__: cls for cls in SchemaTestData.__subclasses__()}

def get_test_object(object_name):
    """Get the schema test data object from the class name."""
    return objects[object_name]

    

        
