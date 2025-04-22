"""
# Public Fault Tree Analyser: utilities.py

Mathematical utility methods.

**Copyright 2025 Conway.**
Licensed under the GNU General Public License v3.0 (GPL-3.0-only).
This is free software with NO WARRANTY etc. etc., see LICENSE.
"""


def find_cycles(adjacency_dict: dict):
    """
    Find cycles of a directed graph via three-state (clean, infected, dead) depth-first search.
    """
    infection_cycles = set()
    infection_chain = []

    clean_nodes = set(adjacency_dict.keys())
    infected_nodes = set()
    # dead_nodes need not be tracked

    def infect(node):
        clean_nodes.discard(node)
        infected_nodes.add(node)
        infection_chain.append(node)

        for child_node in sorted(adjacency_dict[node]):
            if child_node in infected_nodes:  # cycle discovered
                child_index = infection_chain.index(child_node)
                infection_cycles.add(tuple(infection_chain[child_index:]))

            elif child_node in clean_nodes:  # clean child to be infected
                infect(child_node)

        infected_nodes.discard(node)  # infected node dies
        infection_chain.pop()

    while clean_nodes:
        first_clean_node = min(clean_nodes)
        infect(first_clean_node)

    return infection_cycles
