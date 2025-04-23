import convomeld
from convomeld.test_data import scripts, graphs_v2, graphs_v3, BOT_NAME


VERSION = "v3"

if VERSION == 'v2':
    graphs = graphs_v2
elif VERSION == 'v3':
    graphs = graphs_v3


data = [
    # NORMAL_SCRIPT_1
    (scripts.NORMAL_SCRIPT_1_1, graphs.NORMAL_GRAPH_1_1),
    (scripts.NORMAL_SCRIPT_1_2, graphs.NORMAL_GRAPH_1_2),
    (scripts.NORMAL_SCRIPT_1_3, graphs.NORMAL_GRAPH_1_3),
    (scripts.NORMAL_SCRIPT_1_1_HUMAN_STOP_EARLY, graphs.NORMAL_GRAPH_1_1_HUMAN_STOP_EARLY),
    (scripts.NORMAL_SCRIPT_1_1_BOT_STOP_EARLY, graphs.NORMAL_GRAPH_1_1_BOT_STOP_EARLY),
    # # NORMAL_SCRIPT_2
    (scripts.NORMAL_SCRIPT_2_1, graphs.NORMAL_GRAPH_2_1),
    (scripts.NORMAL_SCRIPT_2_2, graphs.NORMAL_GRAPH_2_2),
    (scripts.NORMAL_SCRIPT_2_3, graphs.NORMAL_GRAPH_2_3),
    (scripts.NORMAL_SCRIPT_2_HUMAN_STOP_EARLY_1, graphs.NORMAL_GRAPH_2_HUMAN_STOP_EARLY_1),
    (scripts.NORMAL_SCRIPT_2_HUMAN_STOP_EARLY_2, graphs.NORMAL_GRAPH_2_HUMAN_STOP_EARLY_2),
    (scripts.NORMAL_SCRIPT_2_HUMAN_STOP_EARLY_3, graphs.NORMAL_GRAPH_2_HUMAN_STOP_EARLY_3),
]


def test_parse_scripts():
    for script, graph in data:
        parsed_graph = convomeld.script_to_graph(
            script, bot_name=BOT_NAME, version=VERSION
        )
        assert convomeld.compare_graphs(parsed_graph, graph)


def test_parse_normalization():
    for script, graph in data:
        denorm_parsed_graph = convomeld.script_to_graph(
            script, bot_name=BOT_NAME, normalized=False, version=VERSION
        )
        norm_graph = convomeld.normalize_graph(denorm_parsed_graph, output_version=VERSION)
        assert convomeld.compare_graphs(norm_graph, graph)
