import pytest
from epoch_viz.viz import *
import os

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(CUR_DIR, "run")

def test_universal_constant():
    assert m == 9.10938356e-31
    assert e == 1.60217662e-19
    assert c == 299792458
    assert pi == np.pi
    assert epsilon == 8.85418781e-12
    assert kb == 1.38064852e-23
    assert na == 6.02214076e23

def test_init_checks_errors():
    with pytest.raises(ValueError):
        EpochViz("not_a_directory")
    
    with pytest.raises(EmptyDirectoryError):
        EpochViz(os.path.join(CUR_DIR, "empty_dir"))

    with pytest.raises(InputFileNotFoundError):
        EpochViz(os.path.join(CUR_DIR, "no_input_deck"))

    with pytest.raises(NoSdfFilesError):
        EpochViz(os.path.join(CUR_DIR, "no_sdf_files"))

    
def test_init_checks():
    ez = EpochViz(DATA_DIR)
    assert ez.directory == DATA_DIR
    assert ez.files == sorted(glob.glob(os.path.join(DATA_DIR, "*.sdf")))

def test_find_available_data():
    ez = EpochViz(DATA_DIR)
    assert ez._EpochViz__find_available_data() == [
        "Ex",
        "Ey",
        "Ez",
        "Bx",
        "By",
        "Bz",
        "Px",
        "Py",
        "Pz",
        "rho",
        "Ne",
        "N",
    ]

    assert ez.available_data == [
        "Ex",
        "Ey",
        "Ez",
        "Bx",
        "By",
        "Bz",
        "Px",
        "Py",
        "Pz",
        "rho",
        "Ne",
        "N",
    ]

def test_deck_info():
    ez = EpochViz(DATA_DIR)
    deck_info = {
        "LAMBD": 1e-6,
        "LAS_TIME": 20,
        "T_MAX": 40,
        "DT": 1e-16,
        "A0": 1,
        "FACTOR": 3,
        "NX": 8000,
        "X_MIN": -20,
        "X_MAX": 10,
        "THICKNESS": 1,
        "PPC": 100,
        "START": 0,
    }
    cal_info = ez._EpochViz__get_input_deck_info()
    #assert approximate values:
    for key in deck_info.keys():
        assert deck_info[key] == pytest.approx(cal_info[key]), f"deck_info has wrong value for {key}"
        assert deck_info[key] == pytest.approx(ez.deck_info[key]), f"deck_info inside ez has wrong value for {key}"

def test_info_is_loaded():
    ez = EpochViz(DATA_DIR)
    assert ez._EpochViz__everything_calculated == True, "Everything should be calculated after init"

def test_node_to_space():
    ez = EpochViz(DATA_DIR)
    assert ez._EpochViz__space_node_to_space(0) == 0
    assert ez._EpochViz__space_node_to_space(4000) == 15
    assert ez._EpochViz__space_node_to_space(8000) == ez.deck_info["X_MAX"] - ez.deck_info["X_MIN"]

def test_space_to_node():
    ez = EpochViz(DATA_DIR)
    assert ez._EpochViz__space_to_space_node(0) == 0
    assert ez._EpochViz__space_to_space_node(15) == 4000
    assert ez._EpochViz__space_to_space_node(ez.deck_info["X_MAX"] - ez.deck_info["X_MIN"]) == 8000

def test_time_node_to_time():
    ez = EpochViz(DATA_DIR)
    assert ez._EpochViz__time_node_to_time(0) == 0
    assert ez._EpochViz__time_node_to_time(len(ez.files)) == ez.deck_info["T_MAX"]
    assert ez._EpochViz__time_node_to_time(len(ez.files)/4) == ez.deck_info["T_MAX"]/4

def test_time_to_time_node():
    ez = EpochViz(DATA_DIR)
    assert ez._EpochViz__time_to_time_node(0) == 0
    assert ez._EpochViz__time_to_time_node(ez.deck_info["T_MAX"]) == len(ez.files)

def test_get_data_errors():
    ez = EpochViz(DATA_DIR)
    with pytest.raises(DataNotFoundError):
        ez.get_data("not_a_data")
    
    with pytest.raises(InvalidTimeError):
        ez.get_data("Ex", time_node=10000)

def test_get_data_not_normalize():
    ez = EpochViz(DATA_DIR)
    ey = ez.get_data("Ey", time_node=100)
    assert ey.shape == (ez.deck_info["NX"], )
    assert max(ey) > 1e10
    N = ez.get_data("N", normalize=False, time_node=100)
    assert N.shape == (ez.deck_info["NX"], )
    assert max(N) >= ez.calculated_parameters["ne"]

def test_get_data_normalize():
    ez = EpochViz(DATA_DIR)
    ey = ez.get_data("Ey", normalize=True, time_node=100)
    assert ey.shape == (ez.deck_info["NX"], )
    assert max(ey) == 1
    N = ez.get_data("N", normalize=True, time_node=100)
    assert N.shape == (ez.deck_info["NX"], )
    assert max(N) >= ez.deck_info["FACTOR"]

def test_get_correct_time_range_error():
    ez = EpochViz(DATA_DIR)
    with pytest.raises(InvalidTimeError):
        ez._EpochViz__get_correct_time_range((100, 0), are_nodes = True), "Reversed tuple should raise an error"
    with pytest.raises(InvalidTimeError):
        ez._EpochViz__get_correct_time_range((100, 0), are_nodes = False), "Reversed tuple should raise an error"
    with pytest.raises(TypeError):
        ez._EpochViz__get_correct_time_range([100, 200, 2.0], are_nodes = True), "Should raise an error if dtypes are different"

def test_get_correct_time_range_nodes():
    ez = EpochViz(DATA_DIR)
    assert ez._EpochViz__get_correct_time_range((0, 100), are_nodes = True) == (0, 100), "Tuple should be returned as is"
    assert ez._EpochViz__get_correct_time_range(100, are_nodes = True) == [100], "Integers should be converted to list"
    assert ez._EpochViz__get_correct_time_range(10000, are_nodes = True) == [len(ez.files)-1], "Integers should be converted to list and clipped"
    assert ez._EpochViz__get_correct_time_range((0, 10000), are_nodes = True) == (0, len(ez.files)), "Greater than max should be converted to max"
    assert ez._EpochViz__get_correct_time_range((-100, 100), are_nodes = True) == (0, 100), "Less than min should be converted to min"
    assert ez._EpochViz__get_correct_time_range((-100, 10000), are_nodes = True) == (0, len(ez.files)), "Less than min and greater than max should be converted to min and max"
    
    assert ez._EpochViz__get_correct_time_range(2.0, are_nodes = True) == [ez._EpochViz__time_to_time_node(2.0)], "Float should be converted to time node and list"
    assert ez._EpochViz__get_correct_time_range([2.0, 4.0], are_nodes = True) == [ez._EpochViz__time_to_time_node(2.0), ez._EpochViz__time_to_time_node(4.0)], "list of floats should be converted to list of time nodes"
    assert ez._EpochViz__get_correct_time_range([100, 200, 300], are_nodes = True) == [100, 200, 300], "list of ints should be returned as is"

def test_get_correct_time_range_time():
    ez = EpochViz(DATA_DIR)
    assert ez._EpochViz__get_correct_time_range((0, 10), are_nodes = False) == (0, ez._EpochViz__time_to_time_node(10)), "Should be converted to nodes"
    assert ez._EpochViz__get_correct_time_range((0, 100), are_nodes = False) == (0, len(ez.files)), "Should be converted to nodes and should be clipped to max"
    assert ez._EpochViz__get_correct_time_range((-10, 100), are_nodes = False) == (0, len(ez.files)), "Should be converted to nodes and should be clipped to max and min"

def test_get_correct_space_range_error():
    ez = EpochViz(DATA_DIR)
    with pytest.raises(InvalidSpaceError):
        ez._EpochViz__get_correct_space_range((100, 0), are_nodes = True), "Reversed tuple should raise an error"
    with pytest.raises(InvalidSpaceError):
        ez._EpochViz__get_correct_space_range((100, 0), are_nodes = False), "Reversed tuple should raise an error"
    with pytest.raises(TypeError):
        ez._EpochViz__get_correct_space_range([100, 200, 2.0], are_nodes = True), "Should raise an error if dtypes are different"


def test_get_correct_space_range_nodes():
    ez = EpochViz(DATA_DIR)
    assert ez._EpochViz__get_correct_space_range((0, 100), are_nodes = True) == (0, 100), "Tuple should be returned as is"
    assert ez._EpochViz__get_correct_space_range(100, are_nodes = True) == [100], "Integers should be converted to list"
    assert ez._EpochViz__get_correct_space_range(10000, are_nodes = True) == [ez.deck_info["NX"]-1], "Integers should be converted to list and clipped"
    assert ez._EpochViz__get_correct_space_range((0, 10000), are_nodes = True) == (0, ez.deck_info["NX"]), "Greater than max should be converted to max"
    assert ez._EpochViz__get_correct_space_range((-100, 100), are_nodes = True) == (0, 100), "Less than min should be converted to min"
    assert ez._EpochViz__get_correct_space_range((-100, 10000), are_nodes = True) == (0, ez.deck_info["NX"]), "Less than min and greater than max should be converted to min and max"
    
    assert ez._EpochViz__get_correct_space_range(2.0, are_nodes = True) == [ez._EpochViz__space_to_space_node(2.0)], "Float should be converted to space node and list"
    assert ez._EpochViz__get_correct_space_range([2.0, 4.0], are_nodes = True) == [ez._EpochViz__space_to_space_node(2.0), ez._EpochViz__space_to_space_node(4.0)], "list of floats should be converted to list of space nodes"
    assert ez._EpochViz__get_correct_space_range([100, 200, 300], are_nodes = True) == [100, 200, 300], "list of ints should be returned as is"