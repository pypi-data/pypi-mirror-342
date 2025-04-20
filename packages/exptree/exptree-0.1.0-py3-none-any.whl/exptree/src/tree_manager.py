import uuid
import json
from datetime import datetime
from json import JSONDecodeError
import networkx as nx
from typing import Dict, Any, List, Optional, Set


class TreeManager:
    """Manages a directed graph representing experiment tracking."""

    def __init__(self) -> None:
        """Initializes TreeManager with a graph and storage path.

        Args:
            path: The directory to store graph data (default: current directory).
        """
        self.graph: nx.DiGraph = None  # Initialize graph attribute

    @staticmethod
    def get_time() -> str:
        """Returns the current time as a formatted string."""
        now = datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S")

    def create_graph(self) -> None:
        """Creates a new directed graph."""
        self.graph = nx.DiGraph()

    def create_node(self, **kwargs: Any) -> str:
        """Creates a new node in the graph.

        Args:
            **kwargs: Arbitrary key-value pairs representing node properties.

        Returns:
            The UUID of the newly created node.
        """
        node_id = str(uuid.uuid4())
        self.graph.add_node(
            node_id,
            created_at=TreeManager.get_time(),
            last_updated=TreeManager.get_time(),
            **kwargs
        )
        return node_id

    def create_edge(self, prev_node_id: str, curr_node_id: str) -> None:
        """Creates an edge between two nodes.

        Args:
            prev_node_id: The ID of the source node.
            curr_node_id: The ID of the destination node.
        """
        self.graph.add_edge(prev_node_id, curr_node_id)

    def get_node_properties(self, node_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves the properties of a node.

        Args:
            node_id: The ID of the node.

        Returns:
            A dictionary of node properties, or None if the node doesn't exist.
        """
        return self.graph.nodes.get(node_id)  # More efficient way to handle missing nodes

    def check_node_exists(self, node_id: str) -> bool:
        """Checks if a node exists in the graph.

        Args:
            node_id: The ID of the node.

        Returns:
            True if the node exists, False otherwise.
        """
        return node_id in self.graph.nodes  # Simplified existence check

    def get_id_by_name(self, name: str, view: nx.DiGraph, predecessor: Optional[str] = None) -> List[str]:
        """Retrieves node IDs matching a given name within a subgraph view.

        Args:
            name: The name of the node to search for.
            view: The subgraph view to search within.
            predecessor: Optional predecessor node ID to restrict the search.

        Returns:
            A list of matching node IDs.
        """
        ids = [node_id for node_id in view.nodes() if view.nodes[node_id]["name"] == name]
        if predecessor:
            ids = [node_id for node_id in ids if node_id in self.graph.successors(predecessor)]
        return ids

    def filter_nodes_by_type(self, node_type: str) -> nx.DiGraph:
        """Filters nodes based on their type.

        Args:
            node_type: The type of nodes to filter.

        Returns:
            A subgraph view containing only nodes of the specified type.
        """

        return nx.subgraph_view(self.graph, filter_node=lambda n: self.graph.nodes[n].get('type') == node_type)


    def check_name_exists(self, name: str, predecessor: Optional[str] = None, type: Optional[str] = None) -> bool:
        """Checks if a node with a given name exists, optionally within a specific type and predecessor.

        Args:
            name: The name to check.
            predecessor: Optional predecessor node ID.
            type: Optional node type.

        Returns:
            True if a matching node exists, False otherwise.
        """
        if type and name:
            view = self.filter_nodes_by_type(type)
            return bool(self.get_id_by_name(name, view, predecessor))
        return False

    def update_node_property(
            self, node_id: str, property_name: str, property_value: Any, add_new: bool = False
    ) -> None:
        """Updates a node's property.

        Args:
            node_id: The ID of the node.
            property_name: The name of the property.
            property_value: The new value of the property.
            add_new: Whether to add the property if it doesn't exist.
        """
        if not add_new and property_name not in self.graph.nodes.get(node_id, {}):
            raise ValueError("Incorrect property")  # Raise exception for clarity
        if node_id in self.graph.nodes:
            self.graph.nodes[node_id][property_name] = property_value
        else:
            raise ValueError("Incorrect ID")  # Raise exception for incorrect ID


    def remove(self, node_id: str) -> None:
        """Removes a node and its successors from the graph.

        Args:
            node_id: The ID of the node to remove.
        """
        for successor in list(self.graph.successors(node_id)):  # Iterate over a copy to avoid issues during removal
            self.graph.remove_node(successor)
        self.graph.remove_node(node_id)

    def get_successor(self, node_id: str) -> Set[str]:
        """Returns the successors of a node.
         Args:
            node_id (str): The ID of the node.

        Returns:
            Set[str]: A set of node IDs representing the successors of the input node.
        """
        return set(self.graph.successors(node_id))

    def get_edge_source(self, node_id: str) -> List[str]:
        """Returns the predecessors (source nodes) of a given node.

        Args:
            node_id: The ID of the node.

        Returns:
            A list of predecessor node IDs, or an empty list if the node doesn't exist.
        """
        return list(self.graph.predecessors(node_id)) if node_id in self.graph.nodes else []

    def get_name_by_id(self, node_id: str) -> Optional[str]:
        """Retrieves the name of a node by its ID.

        Args:
            node_id: The ID of the node.

        Returns:
            The name of the node, or None if the node doesn't exist or doesn't have a 'name' property.
        """
        return self.graph.nodes[node_id].get("name") if node_id in self.graph.nodes else None

    def _build_tree(self, node: str, visited: Set[str]) -> Optional[Dict[str, Any]]:
        """Recursively builds a tree-like JSON structure from the graph.

        Args:
            node: The starting node ID.
            visited: A set to keep track of visited nodes (to prevent cycles).

        Returns:
            A dictionary representing the tree structure, or None if the node is already visited.
        """
        if node in visited:
            return None

        visited.add(node)
        node_data = self.graph.nodes.get(node, {}).copy()
        node_data["ID"] = node

        children = [self._build_tree(neighbor, visited) for neighbor in self.graph.neighbors(node) if neighbor not in visited]
        children = [child for child in children if child is not None]

        if children:
            node_data["children"] = children

        return node_data

    def export_to_json(self, root: str, filename: str) -> None:
        """Exports the graph to a JSON file in a tree-like structure.

        Args:
            root: The root node ID for the tree.
            filename: The name of the JSON file to export to.
        """
        tree_data = self._build_tree(root, set())

        with open(filename, "w") as f:
            json.dump(tree_data, f, indent=4)

    def load_from_json(self, filename: str) -> None:
        """Loads a graph from a JSON file.

        Args:
            filename: The name of the JSON file to load from.
        """

        # Create a new graph
        self.graph = nx.DiGraph()

        try:
            # Load JSON data
            with open(filename, "r") as f:
                tree_data = json.load(f)
        except (FileNotFoundError, JSONDecodeError) as e:
            print(f"error {e}")

        try:
            # Recursively add nodes and edges from the JSON structure
            self._build_graph_from_json(tree_data)
        except Exception as e:
            print("Failed loading experiment tree!!")

        print("Imported the experiment tree successfully")

    def _build_graph_from_json(self, node_data: Dict[str, Any]) -> None:
        """Recursively builds the graph from a JSON tree structure.

        Args:
            node_data: A dictionary representing a node and its children.
        """

        # Extract the node ID
        node_id = node_data.pop("ID")

        # Add the node with its attributes
        attributes = {k: v for k, v in node_data.items() if k != "children"}
        self.graph.add_node(node_id, **attributes)

        # Process children if they exist
        if "children" in node_data:
            for child in node_data["children"]:
                child_id = child["ID"]
                # Add an edge from the current node to the child
                self.graph.add_edge(node_id, child_id)
                # Recursively process the child
                self._build_graph_from_json(child)

    def delete_property(self, node_id, property_key):
        """Deletes a specific property from a node.

        Args:
            node_id (str): ID of the node to modify
            property_key (str): Key of the property to delete

        Returns:
            bool: True if deletion was successful, False if node_id doesn't exist
                  or property doesn't exist on the node

        Raises:
            ValueError: If trying to delete a required property ('name', 'type')
        """
        # Check if node exists
        if not self.graph.has_node(node_id):
            print(f"Node with ID {node_id} not found")
            return False

        # Prevent deletion of essential properties
        if property_key in ['name', 'type']:
            raise ValueError(f"Cannot delete required property '{property_key}'")

        # Check if property exists on the node
        if property_key not in self.graph.nodes[node_id]:
            return False

        # Delete the property
        del self.graph.nodes[node_id][property_key]
        return True
