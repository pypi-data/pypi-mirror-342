import convomeld
from convomeld.test_data import graphs_v2, graphs_v3

graphs_v2_list, graphs_v3_list = [
    [
        graphs_v.NORMAL_GRAPH_1_1,
        graphs_v.NORMAL_GRAPH_1_2,
        graphs_v.NORMAL_GRAPH_1_3,
        graphs_v.NORMAL_GRAPH_1_1_HUMAN_STOP_EARLY,
        graphs_v.NORMAL_GRAPH_1_1_BOT_STOP_EARLY,
        graphs_v.NORMAL_GRAPH_1_1_X_1_2,
        graphs_v.NORMAL_GRAPH_1_1_X_1_2_X_1_3,
        graphs_v.NORMAL_GRAPH_2_1,
        graphs_v.NORMAL_GRAPH_2_2,
        graphs_v.NORMAL_GRAPH_2_3,
        graphs_v.NORMAL_GRAPH_2_HUMAN_STOP_EARLY_1,
        graphs_v.NORMAL_GRAPH_2_HUMAN_STOP_EARLY_2,
        graphs_v.NORMAL_GRAPH_2_HUMAN_STOP_EARLY_3,
        graphs_v.NORMAL_GRAPH_2_1_X_2_2,
        graphs_v.NORMAL_GRAPH_2_1_X_2_3,
        graphs_v.NORMAL_GRAPH_2_1_X_2_2_X_2_3,
    ]
    for graphs_v in (graphs_v2, graphs_v3)
]


def test_v2_to_v3():
    for in_graph_v2, expected_graph_v3 in zip(graphs_v2_list, graphs_v3_list):
        in_graph = convomeld.ConvoGraph.from_states_list(
            in_graph_v2, use_uuid=False, version="v2"
        )
        out_graph_v3 = in_graph.to_states_list(version="v3")
        assert out_graph_v3 == expected_graph_v3


def test_v2_to_v2():
    for in_graph_v2 in graphs_v2_list:
        in_graph = convomeld.ConvoGraph.from_states_list(
            in_graph_v2, use_uuid=False, version="v2"
        )
        out_graph_v2 = in_graph.to_states_list(version="v2")
        assert out_graph_v2 == in_graph_v2


def test_v3_to_v2():
    for expected_graph_v2, in_graph_v3 in zip(graphs_v2_list, graphs_v3_list):
        in_graph = convomeld.ConvoGraph.from_states_list(
            in_graph_v3, use_uuid=False, version="v3"
        )
        out_graph_v2 = in_graph.to_states_list(version="v2")
        assert out_graph_v2 == expected_graph_v2


def test_v3_to_v3():
    for in_graph_v3 in graphs_v3_list:
        in_graph = convomeld.ConvoGraph.from_states_list(
            in_graph_v3, use_uuid=False, version="v3"
        )
        out_graph_v3 = in_graph.to_states_list(version="v3")
        assert out_graph_v3 == in_graph_v3
