import pytest
from exptree.src.tree import *

# Assuming src.exp_view and src.run_view are UI elements, mocking them for testing
class MockExperimentView:
    def __init__(self, data):
        self.data = data

class MockRunView:
    def __init__(self, data):
        self.data = data


from exptree import src as exp_ui, src as run_ui

exp_ui.ExperimentView = MockExperimentView # type: ignore
run_ui.RunView = MockRunView # type: ignore


def test_set_project():
    set_project(name="Project A")
    with pytest.raises(ValueError):
        set_project(name="Project A")  # Duplicate project name

def test_set_experiment():
    set_project(name="Test Project")
    set_experiment(name="Experiment A")
    assert manager.check_name_exists("Experiment A", edges["project"], "experiment")
    with pytest.raises(ValueError):
        set_experiment(name="Experiment A") # Duplicate experiment name


def test_start_run():
    set_project(name="Test Project for run")
    set_experiment(name="Test Experiment for run")
    start_run(name="Run A")
    with pytest.raises(ValueError):
        start_run(name="Run A")  # Duplicate run name

def test_stop_run():
    set_project(name="Test Project for stop")
    set_experiment(name="Test Experiment for stop")
    start_run(name="Run Stop")
    stop_run()
    start_run(name="Run B")
    stop_run("Run B")
    with pytest.raises(ValueError):
        stop_run("Nonexistent Run")
    with pytest.raises(Exception):
        stop_run("Run B")


def test_log_hyperparameters():
    set_project(name="Test Project for hyperparameters")
    set_experiment(name="Test Experiment for hyperparameters")
    start_run(name="Run hyperparameters")
    log_hyperparameters(name="lr", value=0.01, run_name="Run hyperparameters")
    log_hyperparameters(name="batch_size", value=32, run_name="Run hyperparameters")
    log_hyperparameters(name="lr", value=0.001, run_name="Run hyperparameters") # Update existing hyperparameter
    with pytest.raises(ValueError):
        log_hyperparameters(value=0.01)  # Missing name
    with pytest.raises(ValueError):
        log_hyperparameters(name="lr")  # Missing value


def test_log_metrics():
    set_project(name="Test Project for metrics")
    set_experiment(name="Test Experiment for metrics")
    start_run(name="Run metrics")
    log_metrics(name="accuracy", value=0.95)
    log_metrics(name="loss", value=0.2, run_name="Run metrics")
    log_metrics(name="accuracy", value=0.98, run_name="Run metrics")
    with pytest.raises(ValueError):
        log_metrics(value=0.95)  # Missing name
    with pytest.raises(ValueError):
        log_metrics(name="accuracy")  # Missing value


def test_log_artifacts():
    set_project(name="Test Project for artifacts")
    set_experiment(name="Test Experiment for artifacts")
    start_run(name="Run artifacts")
    log_artifacts(name="model", artifact_type="model", value="path/to/model")
    log_artifacts(name="plot", artifact_type="image", value="path/to/plot", run_name="Run artifacts")
    log_artifacts(name="model", artifact_type="model", value="new/path", run_name="Run artifacts")
    with pytest.raises(ValueError):
        log_artifacts(artifact_type="model", value="path/to/model")  # Missing name
    with pytest.raises(ValueError):
        log_artifacts(name="model", value="path/to/model")  # Missing artifact_type

def test_get_best_run():
    set_project(name="Project Best run")
    set_experiment(name="Experiment Best run")
    start_run(name="Run 1")
    log_metrics(name="accuracy", value=0.8)
    start_run(name="Run 2")
    log_metrics(name="accuracy", value=0.9)
    best_run = get_best_run("Experiment Best run", "accuracy", "maximize")
    assert best_run["name"][0] == "Run 2"
    best_run_min = get_best_run(
        "Experiment Best run", "accuracy", "minimize"
    )  # Testing minimize objective
    assert best_run_min["name"][0] == "Run 1"
    empty_df = get_best_run("Experiment Best run", "unknown_metric") # Test with unknown metric
    assert empty_df.empty


def test_list_experiments():
    set_project(name="List Project A")
    set_experiment(name="Experiment List 1")
    set_experiment(name="Experiment List 2")
    experiments_df = list_experiments(as_dataframe=True)
    assert len(experiments_df) == 2
    experiments_list = list_experiments()
    assert len(experiments_list) == 2

def test_list_runs():
    set_project(name="List Project B")
    set_experiment(name="Experiment List Runs")
    start_run(name="Run List 1")
    start_run(name="Run List 2")
    runs_df = list_runs(as_dataframe=True)
    assert len(runs_df) == 2
    runs_list = list_runs()
    assert len(runs_list) == 2

def test_get_runs():
    set_project(name="Project Get Runs")
    set_experiment(name="Experiment Get Runs")
    start_run(name="Run Get Runs 1")
    log_metrics(name="accuracy", value=0.85)
    log_hyperparameters(name="lr", value=0.001)
    start_run(name="Run Get Runs 2")
    log_metrics(name="accuracy", value=0.92)
    log_hyperparameters(name="lr", value=0.0001)
    runs_data = get_runs("Experiment Get Runs")
    assert len(runs_data) == 2
    assert "Run Get Runs 1" in runs_data
    assert "Run Get Runs 2" in runs_data

def test_show():
    set_project(name="Show Project")
    set_experiment(name="Show Experiment")
    start_run(name="Show Run 1")
    log_metrics(name="accuracy", value=0.75)
    start_run(name="Show Run 2")
    log_metrics(name="accuracy", value=0.88)
    view_experiments() # Test showing all experiments
    view_runs(experiment_name="Show Experiment") # Test showing a specific experiment
    view_runs(experiment_name="Nonexistent Experiment") # Test with a non-existent experiment name