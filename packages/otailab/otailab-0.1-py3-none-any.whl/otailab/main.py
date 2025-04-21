import networkx as nx
import matplotlib.pyplot as plt
import networkx as nx



def cpm(activities):
    """
    Perform Critical Path Method on a set of activities.
    
    Parameters:
        activities (dict): A dictionary where keys are (start, end) tuples and values are durations.

    Returns:
        results (dict): Contains EST, EFT, LST, LFT, Total Float, Free Float, Independent Float.
        graph (DiGraph): The directed graph with duration attributes.
    """
    G = nx.DiGraph()

    # Add nodes and edges with durations
    for (u, v), duration in activities.items():
        G.add_edge(u, v, duration=duration)

    # Topological sorting
    topo_order = list(nx.topological_sort(G))

    # Initialize times
    EST = {node: 0 for node in G.nodes()}
    EFT = {}
    
    # Forward pass
    for u in topo_order:
        for v in G.successors(u):
            edge_duration = G[u][v]['duration']
            EST[v] = max(EST[v], EST[u] + edge_duration)
            EFT[(u, v)] = EST[u] + edge_duration

    # Compute LFT and LST
    LFT = {node: max(EST.values()) for node in G.nodes()}
    LST = {}

    for u in reversed(topo_order):
        for v in G.successors(u):
            edge_duration = G[u][v]['duration']
            LFT[u] = min(LFT[u], LFT[v] - edge_duration)
            LST[(u, v)] = LFT[v] - edge_duration

    # Calculate floats
    total_float = {}
    free_float = {}
    independent_float = {}

    for (u, v), duration in activities.items():
        total_float[(u, v)] = LST[(u, v)] - EST[u]
        free_float[(u, v)] = EST[v] - (EST[u] + duration)
        independent_float[(u, v)] = max(0, EST[v] - LFT[u] - duration)

    results = {
        'EST': EST,
        'EFT': EFT,
        'LST': LST,
        'LFT': LFT,
        'Total Float': total_float,
        'Free Float': free_float,
        'Independent Float': independent_float
    }

    return results, G


def run_cpm_analysis(activities, cpm_function):
    """
    Runs CPM analysis on a given activity dictionary using a provided CPM function.

    Parameters:
        activities (dict): Dictionary of tasks with durations and dependencies.
        cpm_function (function): A function that accepts processed_activities and returns (results, graph).
    """

    # Preprocess activities
    processed_activities = {}
    task_mapping = {}  # Map task names to numerical IDs

    current_id = 1
    for task in activities:
        task_mapping[task] = current_id
        current_id += 1

    for task, data in activities.items():
        for dep in data['dependencies']:
            processed_activities[(task_mapping[dep], task_mapping[task])] = data['duration']

    # Run CPM function (you must define this elsewhere and pass it in)
    results, graph = cpm_function(processed_activities)

    # Reverse mapping for readability
    inv_task_mapping = {v: k for k, v in task_mapping.items()}

    # Print CPM results
    for activity, duration in processed_activities.items():
        print(f"Activity ({inv_task_mapping[activity[0]]}, {inv_task_mapping[activity[1]]}):")
        print(f" EST: {results['EST'][activity[0]]}")
        print(f" EFT: {results['EFT'][activity]}")
        print(f" LST: {results['LST'][activity]}")
        print(f" LFT: {results['LFT'][activity[1]]}")
        print(f" Total Float: {results['Total Float'][activity]}")
        print(f" Free Float: {results['Free Float'][activity]}")
        print(f" Independent Float: {results['Independent Float'][activity]}")
        print("-" * 20)

    # Draw graph with node labels
    node_labels = {node: inv_task_mapping[node] for node in graph.nodes()}
    nx.relabel_nodes(graph, node_labels, copy=False)

    pos = nx.spring_layout(graph)
    labels = nx.get_edge_attributes(graph, 'duration')

    nx.draw(graph, pos, with_labels=True, node_size=700, node_color="skyblue",
            font_size=10, font_color="black", arrowsize=20)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)

    plt.title("Project Network Diagram")
    plt.show()
