import convomeld
from convomeld.test_data import graphs_v2, graphs_v3


VERSION = 'v3'

if VERSION == 'v2':
    data = graphs_v2
elif VERSION == 'v3':
    data = graphs_v3


def test_compare_identical():
    assert convomeld.compare_graphs(data.NORMAL_GRAPH_1_1, data.NORMAL_GRAPH_1_1)
    assert convomeld.compare_graphs(data.NORMAL_GRAPH_1_2, data.NORMAL_GRAPH_1_2)
    assert convomeld.compare_graphs(data.NORMAL_GRAPH_1_3, data.NORMAL_GRAPH_1_3)
    assert convomeld.compare_graphs(
        data.NORMAL_GRAPH_1_1_BOT_STOP_EARLY, data.NORMAL_GRAPH_1_1_BOT_STOP_EARLY
    )
    assert convomeld.compare_graphs(
        data.NORMAL_GRAPH_1_1_HUMAN_STOP_EARLY,
        data.NORMAL_GRAPH_1_1_HUMAN_STOP_EARLY,
    )
    assert convomeld.compare_graphs(
        data.NORMAL_GRAPH_1_1_X_1_2_X_1_3, data.NORMAL_GRAPH_1_1_X_1_2_X_1_3
    )
    assert convomeld.compare_graphs(data.NORMAL_GRAPH_2_1, data.NORMAL_GRAPH_2_1)
    assert convomeld.compare_graphs(data.NORMAL_GRAPH_2_2, data.NORMAL_GRAPH_2_2)
    assert convomeld.compare_graphs(data.NORMAL_GRAPH_2_3, data.NORMAL_GRAPH_2_3)
    assert convomeld.compare_graphs(
        data.NORMAL_GRAPH_2_1_X_2_2_X_2_3, data.NORMAL_GRAPH_2_1_X_2_2_X_2_3
    )


def test_compare_different():
    assert not convomeld.compare_graphs(
        data.NORMAL_GRAPH_1_1, data.NORMAL_GRAPH_1_2
    )
    assert not convomeld.compare_graphs(
        data.NORMAL_GRAPH_1_1, data.NORMAL_GRAPH_1_3
    )
    assert not convomeld.compare_graphs(
        data.NORMAL_GRAPH_1_2, data.NORMAL_GRAPH_1_3
    )
    assert not convomeld.compare_graphs(
        data.NORMAL_GRAPH_1_2, data.NORMAL_GRAPH_1_1
    )
    assert not convomeld.compare_graphs(
        data.NORMAL_GRAPH_1_3, data.NORMAL_GRAPH_1_1
    )
    assert not convomeld.compare_graphs(
        data.NORMAL_GRAPH_1_3, data.NORMAL_GRAPH_1_2
    )
    assert not convomeld.compare_graphs(
        data.NORMAL_GRAPH_2_1, data.NORMAL_GRAPH_2_2
    )
    assert not convomeld.compare_graphs(
        data.NORMAL_GRAPH_2_1, data.NORMAL_GRAPH_2_2
    )
    assert not convomeld.compare_graphs(
        data.NORMAL_GRAPH_2_2, data.NORMAL_GRAPH_2_3
    )
    assert not convomeld.compare_graphs(
        data.NORMAL_GRAPH_2_2, data.NORMAL_GRAPH_2_1
    )
    assert not convomeld.compare_graphs(
        data.NORMAL_GRAPH_2_3, data.NORMAL_GRAPH_2_1
    )
    assert not convomeld.compare_graphs(
        data.NORMAL_GRAPH_2_3, data.NORMAL_GRAPH_2_2
    )
