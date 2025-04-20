from typing import Dict, List, Any, Union, Optional
from exptree.src import tree_manager
from exptree.src import exp_view as exp_ui
from exptree.src import run_view as run_ui
import pandas as pd
from collections import defaultdict

manager = tree_manager.TreeManager()
curr_node_id = None
manager.create_graph()
edges = {}


def set_project(**kwargs) -> None:
    """Creates a project node in the graph or updates edges with existing project.

    Args:
        **kwargs: Keyword arguments for project properties.
            name (str): Name of the project (required).
            description (str): Description of the project.
            created_by (str): Creator of the project.
            tags (List[str]): List of tags associated with the project.

    Raises:
        ValueError: If project name is missing.
    """
    global edges

    name = kwargs.get("name", None)
    description = kwargs.get("description", "")
    created_by = kwargs.get("created_by", "")
    tags = kwargs.get("tags", [])

    if not name:
        raise ValueError("Please provide a name for the project")

    # Check if project already exists
    view = manager.filter_nodes_by_type(node_type="project")
    curr_node_id = manager.get_id_by_name(name=name, view=view)

    if curr_node_id:
        # If project exists, update edges with existing node ID
        edges["project"] = curr_node_id[0]
        print(f"Using existing project {name} - (ID: {curr_node_id})")
    else:
        # Create new project if it doesn't exist
        curr_node_id = manager.create_node(
            name=name,
            created_by=created_by,
            description=description,
            tags=tags,
            type="project",
        )
        edges["project"] = curr_node_id
        print(f"Project {name} - (ID: {curr_node_id}) created successfully")


def set_experiment(**kwargs) -> None:
    """Creates an experiment node under the current project or updates edges with existing experiment.

    Args:
        **kwargs: Keyword arguments for experiment properties.
            name (str):  Name of the experiment (required).
            description (str): Description of the experiment.
            created_by (str): Creator of the experiment.
            tags (List[str]): List of tags for the experiment.

    Raises:
        ValueError: If experiment name is missing.
    """
    global edges
    name = kwargs.get("name", None)
    description = kwargs.get("description", "")
    created_by = kwargs.get("created_by", "")
    tags = kwargs.get("tags", [])

    if not name:
        raise ValueError("Please provide a name for the experiment")

    if "project" not in edges:
        raise ValueError("Please set a project first before setting an experiment")

    # Check if experiment already exists under the current project
    view = manager.filter_nodes_by_type(node_type="experiment")
    curr_node_id = manager.get_id_by_name(name=name, view=view, predecessor=edges["project"])

    if curr_node_id:
        # If experiment exists, update edges with existing node ID
        edges["experiment"] = curr_node_id[0]
        print(f"Using existing experiment {name} - (ID: {curr_node_id})")
    else:
        # Create new experiment if it doesn't exist
        curr_node_id = manager.create_node(
            name=name,
            created_by=created_by,
            description=description,
            tags=tags,
            type="experiment",
        )
        manager.create_edge(edges["project"], curr_node_id)
        edges["experiment"] = curr_node_id
        print(f"Experiment {name} - (ID: {curr_node_id}) created successfully")


def start_run(**kwargs) -> None:
    """Starts a run under the current experiment or updates edges with existing run.

    Args:
        **kwargs: Keyword arguments for run properties.
            name (str): Name of the run (required).
            description (str): Description of the run.
            created_by (str):  Creator of the run.
            tags (List[str]): Tags associated with the run.

    Raises:
        ValueError: If run name is missing.
    """
    global edges

    name = kwargs.get("name", None)
    description = kwargs.get("description", "")
    created_by = kwargs.get("created_by", "")
    tags = kwargs.get("tags", [])

    if not name:
        raise ValueError("Please provide a name for the run")

    if "experiment" not in edges:
        raise ValueError("Please set an experiment first before starting a run")

    if "project" not in edges:
        raise ValueError("Please set an project first before starting a run")

    # Check if run already exists under the current experiment
    view = manager.filter_nodes_by_type(node_type="run")
    curr_node_id = manager.get_id_by_name(name=name, view=view, predecessor=edges["experiment"])

    if curr_node_id:
        edges["run"] = curr_node_id[0]
        print(f"Using existing run {name} - (ID: {curr_node_id})")
        manager.delete_property(edges["run"], "end_time")
    else:
        # Create new run if it doesn't exist
        curr_node_id = manager.create_node(
            name=name,
            created_by=created_by,
            description=description,
            tags=tags,
            type="run",
        )
        manager.create_edge(edges["experiment"], curr_node_id)
        if curr_node_id:
            edges["run"] = curr_node_id
        print(f"Run {name} - (ID: {curr_node_id}) created successfully")

def stop_run(name: Optional[str] = None) -> None:
    """Stops a run by adding an end_time property.

    Args:
        name (str, optional): Name of the run to stop. If None, stops the last started run.

    Raises:
        Exception: If the specified run is already stopped.
        ValueError: If the specified run is not found.
    """
    if not name:
        try:
            if "end_time" in manager.get_node_properties(edges["run"]).keys():
                raise Exception("Run already stopped")
            manager.update_node_property(
                edges["run"],
                property_name="end_time",
                property_value=manager.get_time(),
                add_new=True,
            )
        except IndexError:  # Handles cases where no run exists
            raise ValueError("No active runs found.")
    else:
        view = manager.filter_nodes_by_type(node_type="run")
        node_id = manager.get_id_by_name(name, view, predecessor=edges["experiment"])
        if not node_id:
            raise ValueError(f"The run : {name} not found")
        else:
            if "end_time" in manager.get_node_properties(node_id[0]).keys():
                raise Exception("Run already stopped")
            manager.update_node_property(
                node_id[0],
                property_name="end_time",
                property_value=manager.get_time(),
                add_new=True,
            )
        print(f"Run {name} stopped (ID: {node_id[0]})")


def log_hyperparameters(**kwargs) -> None:
    """Logs hyperparameters for a run.

    Args:
        **kwargs: Keyword arguments for hyperparameter properties.
            name (str): Name of the hyperparameter.
            run_name (str, optional): Name of the run. If not provided, logs to the last active run.
            description (str): Description of the hyperparameter.
            created_by (str): Creator of the hyperparameter (defaults to current run's creator if available).
            tags (List[str]): List of tags.
            value (Any): Value of the hyperparameter. Can also be a dictionary of name: value pairs.

    Raises:
        ValueError: If name or value is missing (when value isn't a dictionary), or if the specified run is not found.
    """
    name = kwargs.get("name", None)
    run_name = kwargs.get("run_name", None)
    description = kwargs.get("description", "")
    try:
        created_by = kwargs.get("created_by", edges["run"])
    except IndexError:  # Handle cases where no run exists
        raise ValueError("No active run found.")
    tags = kwargs.get("tags", [])
    value = kwargs.get("value")

    if not name and not isinstance(value, dict):
        raise ValueError("Please provide a name")
    if not value:
        raise ValueError("Please provide a value")

    if not isinstance(value, dict):
        value = {name: value}

    view = manager.filter_nodes_by_type(node_type="run")
    run_id = []
    if run_name:
        run_id = manager.get_id_by_name(run_name, view, predecessor=edges["experiment"])
        if not run_id:
            raise ValueError(f"Run - {run_name} not found")

    view = manager.filter_nodes_by_type(node_type="hyperparameter")
    for (
        name,
        val,
    ) in value.items():  # Handles dictionary input for multiple hyperparameters at once
        if run_id:
            node_id = manager.get_id_by_name(name, view, predecessor=run_id[0])
        else:
            node_id = manager.get_id_by_name(name, view, predecessor=edges["run"])
        if not node_id:
            node_id = manager.create_node(
                name=name,
                created_by=created_by,
                description=description,
                tags=tags,
                value=val,
                type="hyperparameter",
            )

            manager.create_edge(edges["run"], node_id)
            print(f"'hyperparameter : {name}' logged (ID: {node_id})")
        else:  # Update hyperparameter if it already exists for the run
            manager.update_node_property(
                node_id[0],
                property_name="value",
                property_value=val,
            )
            print(f"hyperparameter : {name} updated (ID: {node_id[0]})")


def log_metrics(**kwargs) -> None:
    """Logs metrics for a run.

    Args:
        **kwargs: Keyword arguments for metric properties.
            name (str): Name of the metric.
            run_name (str, optional): Name of the run. If not provided, uses the current run.
            description (str): Description of the metric.
            created_by (str, optional): Creator of the metric (defaults to current run if available).
            tags (List[str]): List of tags for the metric.
            value (Any): Value of the metric. Can also be a dictionary of name: value pairs.

    Raises:
        ValueError: If name or value is missing (when value isn't a dictionary), or if the specified run is not found.
    """
    name = kwargs.get("name", None)
    run_name = kwargs.get("run_name", None)
    description = kwargs.get("description", "")
    try:
        created_by = kwargs.get("created_by", edges["run"])
    except KeyError:  # Handle cases where no run exists.
        raise ValueError("No active run found.")

    tags = kwargs.get("tags", [])
    value = kwargs.get("value")

    if not name and not isinstance(value, dict):
        raise ValueError("Please provide a name")
    if not value:
        raise ValueError("Please provide a value")

    view = manager.filter_nodes_by_type(node_type="run")
    run_id = []
    if run_name:
        run_id = manager.get_id_by_name(run_name, view, predecessor=edges["experiment"])
        if not run_id:
            raise ValueError(f"Run - {run_name} not found")

    if not isinstance(value, dict):
        value = {name: value}

    view = manager.filter_nodes_by_type(node_type="metrics")
    for (
        name,
        val,
    ) in (
        value.items()
    ):  # Handles dictionary input for logging multiple metrics at once.
        if run_id:
            node_id = manager.get_id_by_name(name, view, predecessor=run_id[0])
        else:
            try:
                node_id = manager.get_id_by_name(
                    name, view, predecessor=edges["run"]
                )
            except IndexError:  # Handles cases where no run exists
                raise ValueError("No active runs found.")

        if not node_id:
            node_id = manager.create_node(
                name=name,
                created_by=created_by,
                description=description,
                tags=tags,
                value=val,
                type="metric",
            )

            manager.create_edge(edges["run"], node_id)
            print(f"'metric : {name}' logged (ID: {node_id})")

        else:  # Update metric value if it already exists
            manager.update_node_property(
                node_id[0],
                property_name="value",
                property_value=val,
            )
            print(f"'metric : {name}' updated (ID: {node_id[0]})")


def log_artifacts(**kwargs) -> None:
    """Logs artifacts for a run.

    Args:
        **kwargs: Keyword arguments for artifact properties.
            name (str): Name of the artifact (required).
            run_name (str, optional): Name of the run. If not provided, uses the current run.
            description (str): Description of the artifact.
            created_by (str, optional): Creator of the artifact (defaults to current run if available).
            tags (List[str]): List of tags for the artifact.
            artifact_type (str): Type of the artifact (e.g., 'plot', 'model', 'data') (required).
            value (Any): Value or path of the artifact (required).

    Raises:
        ValueError: If name, artifact_type, or value is missing, or if the artifact_type is invalid.
    """
    name = kwargs.get("name", None)
    run_name = kwargs.get("run_name", None)
    description = kwargs.get("description", "")
    try:
        created_by = kwargs.get("created_by", edges["run"])
    except KeyError:  # Handle cases where no run exists
        raise ValueError("No active run found.")
    tags = kwargs.get("tags", [])
    artifact_type = kwargs.get("artifact_type")
    value = kwargs.get("value")

    if not name:
        raise ValueError("Please provide a name")
    if not artifact_type:
        raise ValueError("Please provide an artifact_type (plot, model, data, etc.)")
    if not value:
        raise ValueError("Please provide a path/value")

    if artifact_type not in ["image", "model", "data", "text"]:
        raise ValueError("Incorrect value for artifact type")

    view = manager.filter_nodes_by_type(
        node_type="run"
    )  # Filter for artifact nodes

    if run_name:  # Get run ID if run name is provided
        run_id = manager.get_id_by_name(run_name, view, predecessor=edges["experiment"])
        if not run_id:
            raise ValueError(f"Run - {run_name} not found")
        else:  # Get artifact node ID based on the provided run name
            node_id = manager.get_id_by_name(name, view, predecessor=run_id[0])

    else:  # Get artifact node ID based on current run
        view = manager.filter_nodes_by_type(node_type=artifact_type)
        try:
            node_id = manager.get_id_by_name(name, view, predecessor=edges["run"])
        except IndexError:  # Handles cases where no run exists
            raise ValueError("No active runs found.")

    if not node_id:  # Create new artifact node if it doesn't exist
        node_id = manager.create_node(
            name=name,
            created_by=created_by,
            description=description,
            tags=tags,
            value=value,
            type=artifact_type,
        )

        manager.create_edge(edges["run"], node_id)
        print(f"'artifact : {name}' logged (ID: {node_id})")

    else:  # Update artifact if it already exists
        manager.update_node_property(
            node_id[0],
            property_name="value",
            property_value=value,
        )
        print(f"artifact : {name} - updated (ID: {node_id[0]})")


def log_prompts(**kwargs) -> None:
    """Logs prompts for a run.

    Args:
        **kwargs: Keyword arguments for artifact properties.
            name (str): Name of the artifact (required).
            run_name (str, optional): Name of the run. If not provided, uses the current run.
            description (str): Description of the artifact.
            created_by (str, optional): Creator of the artifact (defaults to current run if available).
            tags (List[str]): List of tags for the artifact.
            value (Any): Value or path of the artifact (required).

    Raises:
        ValueError: If name, artifact_type, or value is missing, or if the artifact_type is invalid.
    """
    name = kwargs.get("name", None)
    run_name = kwargs.get("run_name", None)
    description = kwargs.get("description", "")
    try:
        created_by = kwargs.get("created_by", edges["run"])
    except KeyError:  # Handle cases where no run exists
        raise ValueError("No active run found.")
    tags = kwargs.get("tags", [])
    value = kwargs.get("value")

    if not name:
        raise ValueError("Please provide a name")
    if not value:
        raise ValueError("Please provide a prompt")

    view = manager.filter_nodes_by_type(
        node_type="run"
    )  # Filter for run nodes

    if run_name:  # Get run ID if run name is provided
        run_id = manager.get_id_by_name(run_name, view, predecessor=edges["experiment"])
        if not run_id:
            raise ValueError(f"Run - {run_name} not found")
        else:  # Get artifact node ID based on the provided run name
            node_id = manager.get_id_by_name(name, view, predecessor=run_id[0])

    else:  # Get artifact node ID based on current run
        view = manager.filter_nodes_by_type(node_type="prompt" )
        try:
            node_id = manager.get_id_by_name(name, view, predecessor=edges["run"])
        except IndexError:  # Handles cases where no run exists
            raise ValueError("No active runs found.")

    if not node_id:  # Create new artifact node if it doesn't exist
        node_id = manager.create_node(
            name=name,
            created_by=created_by,
            description=description,
            tags=tags,
            value=value,
            type="prompt",
        )

        manager.create_edge(edges["run"], node_id)
        print(f"'prompt : {name}' logged (ID: {node_id})")

    else:  # Update artifact if it already exists
        manager.update_node_property(
            node_id[0],
            property_name="value",
            property_value=value,
        )
        print(f"prompt : {name} - updated (ID: {node_id[0]})")

def get_node_id(name, type):

    if name and type:
        view = manager.filter_nodes_by_type(node_type=type)
        try:
            predecessor = {
                "project": None,
                "experiment": edges["project"],
                "run": edges["experiment"],
            }.get(
                type, None
            )  # Default to last run for other types
        except IndexError:  # Handle cases where "run" might not exist
            raise ValueError(f"No active run found for retrieving {type}")
        node_id = manager.get_id_by_name(name, view, predecessor=predecessor)
        if not node_id:
            raise ValueError(f"{name} : {type} not found")
        else:
            node_id = node_id[0]
    else:
        node_id = curr_node_id

    return node_id


def add_tags(tags, name=None, type=None):
    node_id = get_node_id(name, type) if name and type else curr_node_id

    properties = manager.get_node_properties(node_id)
    if isinstance(tags, list):
        properties["tags"].extend(tags)
    else:
        properties["tags"].append(tags)

    manager.update_node_property(
        node_id,
        property_name="tags",
        property_value=properties["tags"],
    )


def remove_tags(value, name=None, type=None):
    node_id = get_node_id(name, type) if name and type else curr_node_id
    properties = manager.get_node_properties(node_id)
    try:
        properties["tags"].remove(value)
        manager.update_node_property(
            node_id,
            property_name="tags",
            property_value=properties["tags"],
        )
    except Exception as e:
        print(e)


def update_description(description, name, type):
    node_id = get_node_id(name, type) if name and type else curr_node_id
    manager.update_node_property(
        node_id, property_name="description", property_value=description
    )


def update_name(curr_name, latest_name, type):
    node_id = get_node_id(curr_name, type) if curr_name and type else curr_node_id
    manager.update_node_property(
        node_id, property_name="name", property_value=latest_name
    )


def delete(name, type):
    global edges
    node_id = get_node_id(name, type) if name and type else curr_node_id
    print(node_id)
    manager.remove(node_id)
    if type == "project" and "project" in edges.keys():
        edges = {}
    elif type == "experiment" and "experiment" in edges.keys():
        edges.pop("experiment")
        if "run" in edges.keys():
            edges.pop("run")
    elif type == "run" and "run" in edges.keys():
        edges.pop("run")




def get(id=None):
    return manager.get_node_properties(id)


def _list_experiments(
    project: Optional[str] = None, as_dataframe: bool = False
) -> Union[pd.DataFrame, List[Dict[str, Any]]]:
    """Lists all experiments under a project."""

    project_id = get_node_id(project, "project") if project else edges["project"]
    view = manager.filter_nodes_by_type("experiment")
    experiments = [
        manager.get_node_properties(node_id)
        for node_id in view
        if manager.get_edge_source(node_id)[0] == project_id
    ]

    return pd.DataFrame(experiments) if as_dataframe else experiments


def _list_runs(
    experiment_name: Optional[str] = None, as_dataframe: bool = False
) -> Union[pd.DataFrame, List[Dict[str, Any]]]:
    """Lists all runs for the specified experiment."""

    if not experiment_name:
        if "experiment" not in edges:
            raise ValueError(
                "No current experiment set. Please use set_experiment first."
            )
        experiment_ids = [edges["experiment"]]  # Use current experiment
    else:
        view = manager.filter_nodes_by_type("experiment")
        experiment_ids = manager.get_id_by_name(experiment_name, view=view, predecessor=edges["project"])
        if not experiment_ids:
            return (
                pd.DataFrame() if as_dataframe else []
            )  # Return empty if experiment not found

    experiment_id = experiment_ids[0]
    run_view = manager.filter_nodes_by_type("run")
    runs = [
        manager.get_node_properties(node_id)
        for node_id in run_view
        if manager.get_edge_source(node_id)
        and manager.get_edge_source(node_id)[0] == experiment_id
    ]

    if as_dataframe:
        return pd.DataFrame(runs)
    else:
        return runs


def get_runs(experiment_name: Optional[str] = None) -> Dict[str, Dict[str, Any]]:
    """Retrieves all child nodes for each run in an experiment."""

    experiment_id = (
        get_node_id(experiment_name, "experiment")
        if experiment_name
        else edges["experiment"]
    )
    run_ids = manager.get_successor(experiment_id)
    tracked_data = {}

    for run_id in run_ids:
        run_name = manager.get_name_by_id(run_id)
        tracked_data[run_name] = {
            "hyperparameters": get_hyperparameters(run_name),
            "metrics": get_metrics(run_name),
            "artifact": get_artifacts(run_name),
            "prompt": get_prompts(run_name),
        }

    return tracked_data


def get_prompts(
        run_name: str, as_dataframe: bool = False
) -> Union[pd.DataFrame, List[Dict[str, Any]]]:
    """Retrieve all logged prompts for the specified run."""
    run_id = get_node_id(run_name, type="run")
    successor_nodes = manager.get_successor(run_id)
    prompts = [
        manager.get_node_properties(node_id)
        for node_id in successor_nodes
        if manager.get_node_properties(node_id)["type"] == "prompt"
    ]

    return pd.DataFrame(prompts) if as_dataframe else prompts

def get_artifacts(
    run_name: str, as_dataframe: bool = False
) -> Union[pd.DataFrame, List[Dict[str, Any]]]:
    """Retrieve all logged artifacts for the specified run."""
    run_id = get_node_id(run_name, type="run")
    successor_nodes = manager.get_successor(run_id)
    artifacts = [
        manager.get_node_properties(node_id)
        for node_id in successor_nodes
        if manager.get_node_properties(node_id)["type"] in ["image", "model", "data"]
    ]

    return pd.DataFrame(artifacts) if as_dataframe else artifacts


def get_metrics(
    run_name: str, as_dataframe: bool = False
) -> Union[pd.DataFrame, List[Dict[str, Any]]]:
    """Retrieve all logged metrics for the specified run."""
    run_id = get_node_id(run_name, type="run")
    successor_nodes = manager.get_successor(run_id)
    metrics = [
        manager.get_node_properties(node_id)
        for node_id in successor_nodes
        if manager.get_node_properties(node_id)["type"] == "metric"
    ]

    return pd.DataFrame(metrics) if as_dataframe else metrics


def get_hyperparameters(
    run_name: str, as_dataframe: bool = False
) -> Union[pd.DataFrame, List[Dict[str, Any]]]:
    """Retrieve all logged hyperparameters for the specified run."""
    run_id = get_node_id(run_name, type="run")
    successor_nodes = manager.get_successor(run_id)
    hyperparameters = [
        manager.get_node_properties(node_id)
        for node_id in successor_nodes
        if manager.get_node_properties(node_id)["type"] == "hyperparameter"
    ]

    return pd.DataFrame(hyperparameters) if as_dataframe else hyperparameters


def get_best_run(
    experiment_name: str, metric_name: str = "mae", objective: str = "minimize"
) -> pd.DataFrame:
    """Retrieves the best run based on a specified metric."""

    experiment_id = get_node_id(experiment_name, type="experiment")
    if not experiment_id:
        raise ValueError(f"Experiment '{experiment_name}' not found.")

    successor_runs = manager.get_successor(experiment_id)
    if not successor_runs:
        raise ValueError(f"No runs found for experiment '{experiment_name}'.")

    best_run = None
    best_metric_value = float("inf") if objective == "minimize" else float("-inf")

    for run_id in successor_runs:
        name = manager.get_name_by_id(run_id)
        metrics = get_metrics(name)

        if metrics:
            for metric in metrics:
                if metric_name == metric["name"]:  # Directly compare metric names
                    metric_value = float(metric["value"])

                    if (
                        objective == "minimize" and metric_value < best_metric_value
                    ) or (objective == "maximize" and metric_value > best_metric_value):
                        best_metric_value = metric_value
                        best_run = {
                            "run_id": run_id,
                            "experiment_name": experiment_name,
                            "best_metric": best_metric_value,
                            **manager.get_node_properties(run_id),
                        }
                    break  # Exit the loop after finding the metric

    if not best_run:
        return pd.DataFrame()  # Return empty dataframe

    return pd.DataFrame([best_run])


def extract_named_items(data: Dict[str, Any], item_type: str) -> Dict[str, float]:
    """Extracts items with 'name' and 'value' from a dictionary."""

    extracted_items = {}
    if (
        isinstance(data, dict)
        and item_type in data
        and isinstance(data[item_type], list)
    ):
        for item in data[item_type]:
            if isinstance(item, dict) and "name" in item and "value" in item:
                if isinstance(item["value"], (int, float)):
                    extracted_items[item["name"]] = round(float(item["value"]), 4)
                else:
                    extracted_items[item["name"]] = item["value"]
    return extracted_items


def get_experiment_data() -> Dict[str, Any]:
    """Retrieves and structures experiment data."""

    try:
        experiment_list = _list_experiments().copy()
        experiment_data_dict = {}

        for experiment in experiment_list:
            experiment_name = experiment["name"]
            experiment_data_dict[experiment_name] = experiment
            experiment_data_dict[experiment_name]["runs"] = []

            run_list = _list_runs(experiment_name=experiment_name)
            for run in run_list:
                tracked_run_data = get_runs(experiment_name=experiment_name)
                if run["name"] in tracked_run_data:
                    run["hyperparameters"] = extract_named_items(
                        tracked_run_data[run["name"]], "hyperparameters"
                    )
                    run["metrics"] = extract_named_items(
                        tracked_run_data[run["name"]], "metrics"
                    )
                    run["artifact"] = extract_named_items(
                        tracked_run_data[run["name"]], "artifact"
                    )
                    run["prompt"] = extract_named_items(
                        tracked_run_data[run["name"]], "prompt"
                    )
                    experiment_data_dict[experiment_name]["runs"].append(run)

        return experiment_data_dict
    except Exception as e:
        print(f"Error retrieving experiment data: {e}")
        return {}

def view_experiments() -> None:
    """Display experiments"""
    try:
        experiments_data = get_experiment_data()
        exp_ui.ExperimentView(experiments_data)
    except Exception as e:
        print(f"Error in rendering experiments; reason: {e}")

def view_runs(experiment_name: Optional[str] = None) -> None:
    """Displays run data for the given experiment"""
    experiments_data = get_experiment_data()
    if experiment_name in experiments_data:  # Check if experiment exists
        runs = {
            run["name"]: {k: v for k, v in run.items() if k != "name"}
            for run in experiments_data[experiment_name]["runs"]
        }
        run_ui.RunView(runs)
    else:
        print(
            f"Error: Experiment '{experiment_name}' not found."
        )  # Inform if experiment doesnt exist


def export_tree(filename: str) -> None:
    """Exports the experiment tree to a JSON file."""
    root = edges["project"]
    manager.export_to_json(root, filename)

def load_tree(filename: str) -> None:
    """Import the experiment tree from json"""
    manager.load_from_json(filename)

def get_tree_nodes_dataframe():
    """
    Creates a pandas DataFrame showing all node relationships

    Returns:
        pandas.DataFrame: DataFrame with columns for project, experiment, run, and their IDs
    """
    # Get all nodes by type
    projects = {node_id: data for node_id, data in manager.graph.nodes(data=True)
                if data.get('type') == 'project'}
    experiments = {node_id: data for node_id, data in manager.graph.nodes(data=True)
                   if data.get('type') == 'experiment'}
    runs = {node_id: data for node_id, data in manager.graph.nodes(data=True)
            if data.get('type') == 'run'}

    # Create a dictionary to store parent-child relationships
    children = defaultdict(list)

    # Build relationship map
    for edge in manager.graph.edges():
        parent, child = edge
        children[parent].append(child)

    # Lists to store hierarchical data
    paths = []

    # For each project, traverse its hierarchy
    for project_id, project_data in projects.items():
        project_name = project_data.get('name', 'Unknown')

        # If project has no experiments, add just the project
        if project_id not in children:
            paths.append({
                'project_name': project_name,
                'project_id': project_id,
                'experiment_name': None,
                'experiment_id': None,
                'run_name': None,
                'run_id': None
            })
            continue

        # For each experiment under this project
        for exp_id in children[project_id]:
            if exp_id in experiments:
                exp_name = experiments[exp_id].get('name', 'Unknown')

                # If experiment has no runs, add project-experiment
                if exp_id not in children:
                    paths.append({
                        'project_name': project_name,
                        'project_id': project_id,
                        'experiment_name': exp_name,
                        'experiment_id': exp_id,
                        'run_name': None,
                        'run_id': None
                    })
                    continue

                # For each run under this experiment
                for run_id in children[exp_id]:
                    if run_id in runs:
                        run_name = runs[run_id].get('name', 'Unknown')

                        # Add complete path
                        paths.append({
                            'project_name': project_name,
                            'project_id': project_id,
                            'experiment_name': exp_name,
                            'experiment_id': exp_id,
                            'run_name': run_name,
                            'run_id': run_id
                        })

    # Create DataFrame
    df = pd.DataFrame(paths)
    return df

def view_tree()->pd.DataFrame:
    df = get_tree_nodes_dataframe()
    return df

def get_current_experiment() -> str:
    """get current experiment"""
    return edges["experiment"]

def get_current_project() -> str:
    return edges["project"]

def get_current_run() -> str:
    return edges["run"]

