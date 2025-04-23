import convomeld
from convomeld.test_data import scripts, graphs_v2, graphs_v3, BOT_NAME
from itertools import permutations


VERSION = 'v3'

if VERSION == 'v2':
    data = graphs_v2
elif VERSION == 'v3':
    data = graphs_v3


def test_merge_identical_graphs():
    # NORMAL_GRAPH_1
    graphs_1 = [
        data.NORMAL_GRAPH_1_1,
        data.NORMAL_GRAPH_1_2,
        data.NORMAL_GRAPH_1_3,
        data.NORMAL_GRAPH_1_1_HUMAN_STOP_EARLY,
        data.NORMAL_GRAPH_1_1_BOT_STOP_EARLY,
    ]
    # NORMAL_GRAPH_2
    graphs_2 = [
        data.NORMAL_GRAPH_2_1,
        data.NORMAL_GRAPH_2_2,
        data.NORMAL_GRAPH_2_3,
        data.NORMAL_GRAPH_2_HUMAN_STOP_EARLY_1,
        data.NORMAL_GRAPH_2_HUMAN_STOP_EARLY_2,
        data.NORMAL_GRAPH_2_HUMAN_STOP_EARLY_3,
    ]

    for graph in graphs_1 + graphs_2:
        assert convomeld.compare_graphs(convomeld.merge_graphs(graph, graph), graph)


def test_merge_normal_compatible_graphs():
    # NORMAL_GRAPH_1
    # merge 2 graphs
    graphs_1_1 = [
        data.NORMAL_GRAPH_1_1,
        data.NORMAL_GRAPH_1_2,
    ], data.NORMAL_GRAPH_1_1_X_1_2
    # merge 3 graphs
    graphs_1_2 = [
        data.NORMAL_GRAPH_1_1,
        data.NORMAL_GRAPH_1_2,
        data.NORMAL_GRAPH_1_3,
    ], data.NORMAL_GRAPH_1_1_X_1_2_X_1_3
    # NORMAL_GRAPH_2
    # merge 2 graphs
    graphs_2_1 = [
        data.NORMAL_GRAPH_2_1,
        data.NORMAL_GRAPH_2_2,
    ], data.NORMAL_GRAPH_2_1_X_2_2
    graphs_2_2 = [
        data.NORMAL_GRAPH_2_1,
        data.NORMAL_GRAPH_2_3,
    ], data.NORMAL_GRAPH_2_1_X_2_3
    graphs_2_3 = [
        data.NORMAL_GRAPH_2_2,
        data.NORMAL_GRAPH_2_3,
    ], data.NORMAL_GRAPH_2_2_X_2_3
    # merge 3 graphs
    graphs_2_4 = [
        data.NORMAL_GRAPH_2_1,
        data.NORMAL_GRAPH_2_2,
        data.NORMAL_GRAPH_2_3,
    ], data.NORMAL_GRAPH_2_1_X_2_2_X_2_3

    all_graphs = [
        graphs_1_1,
        graphs_1_2,
        graphs_2_1,
        graphs_2_2,
        graphs_2_3,
        graphs_2_4,
    ]

    for src_graphs, res_graph in all_graphs:
        for graphs in permutations(src_graphs):
            assert convomeld.compare_graphs(
                convomeld.merge_graphs(*graphs), res_graph
            )


def test_merge_normal_and_stop_early_graphs():
    # NORMAL_GRAPH_1
    graphs_1 = [
        data.NORMAL_GRAPH_1_1,
        data.NORMAL_GRAPH_1_1_HUMAN_STOP_EARLY,
        data.NORMAL_GRAPH_1_1_BOT_STOP_EARLY,
    ]
    # NORMAL_GRAPH_2
    graphs_2 = [
        data.NORMAL_GRAPH_2_1_X_2_2_X_2_3,
        data.NORMAL_GRAPH_2_HUMAN_STOP_EARLY_1,
        data.NORMAL_GRAPH_2_HUMAN_STOP_EARLY_2,
        data.NORMAL_GRAPH_2_HUMAN_STOP_EARLY_3,
    ]

    all_graphs = [graphs_1, graphs_2]

    for src_graphs in all_graphs:
        res_graph = src_graphs[0]
        for graphs in permutations(src_graphs):
            assert convomeld.compare_graphs(
                convomeld.merge_graphs(*graphs), res_graph
            )


def test_merge_denormalized_compatible_graphs():
    # NORMAL_GRAPH_1
    # merge 2 graphs
    data_1_1 = [
        scripts.NORMAL_SCRIPT_1_1,
        scripts.NORMAL_SCRIPT_1_2,
    ], data.NORMAL_GRAPH_1_1_X_1_2
    # merge 3 graphs
    data_1_2 = [
        scripts.NORMAL_SCRIPT_1_1,
        scripts.NORMAL_SCRIPT_1_2,
        scripts.NORMAL_SCRIPT_1_3,
    ], data.NORMAL_GRAPH_1_1_X_1_2_X_1_3
    # NORMAL_GRAPH_2
    # merge 2 graphs
    data_2_1 = [
        scripts.NORMAL_SCRIPT_2_1,
        scripts.NORMAL_SCRIPT_2_2,
    ], data.NORMAL_GRAPH_2_1_X_2_2
    data_2_2 = [
        scripts.NORMAL_SCRIPT_2_1,
        scripts.NORMAL_SCRIPT_2_3,
    ], data.NORMAL_GRAPH_2_1_X_2_3
    data_2_3 = [
        scripts.NORMAL_SCRIPT_2_2,
        scripts.NORMAL_SCRIPT_2_3,
    ], data.NORMAL_GRAPH_2_2_X_2_3
    # merge 3 graphs
    data_2_4 = [
        scripts.NORMAL_SCRIPT_2_1,
        scripts.NORMAL_SCRIPT_2_2,
        scripts.NORMAL_SCRIPT_2_3,
    ], data.NORMAL_GRAPH_2_1_X_2_2_X_2_3

    all_data = [
        data_1_1,
        data_1_2,
        data_2_1,
        data_2_2,
        data_2_3,
        data_2_4,
    ]

    for src_scripts, res_graph in all_data:
        graphs = [
            convomeld.script_to_graph(script, bot_name=BOT_NAME, normalized=False, version=VERSION)
            for script in src_scripts
        ]
        assert convomeld.compare_graphs(
            convomeld.merge_graphs(*graphs), res_graph
        )
