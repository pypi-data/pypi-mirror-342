import convomeld
from convomeld.constants import DATA_DIR
from convomeld.test_data import scripts_paths, graphs_v2, graphs_v3, graphs_v2_paths, graphs_v3_paths


VERSION = 'v3'

if VERSION == 'v2':
    graphs = graphs_v2
    graphs_paths = graphs_v2_paths
elif VERSION == 'v3':
    graphs = graphs_v3
    graphs_paths = graphs_v3_paths


def test_convoyaml_filepath_str():
    filepath_str = graphs_paths.NORMAL_GRAPH_1_1.as_posix()
    graph = convomeld.file_to_graph(
        filepath_str,
        use_uuid=False,
        output_version=VERSION,
    )
    assert graph == graphs.NORMAL_GRAPH_1_1


def test_script_filepath_str():
    filepath_str = scripts_paths.NORMAL_SCRIPT_1_1.as_posix()
    graph = convomeld.file_to_graph(
        filepath_str,
        use_uuid=False,
        output_version=VERSION,
    )
    assert graph == graphs.NORMAL_GRAPH_1_1


def test_convoyaml_path():
    path = graphs_paths.NORMAL_GRAPH_1_1
    graph = convomeld.file_to_graph(
        path,
        use_uuid=False,
        output_version=VERSION,
    )
    assert graph == graphs.NORMAL_GRAPH_1_1


def test_script_path():
    path = scripts_paths.NORMAL_SCRIPT_1_1
    graph = convomeld.file_to_graph(
        path,
        use_uuid=False,
        output_version=VERSION,
    )
    assert graph == graphs.NORMAL_GRAPH_1_1


def test_convoyaml_stream():
    stream = graphs_paths.NORMAL_GRAPH_1_1.open("r", encoding="utf-8")
    graph = convomeld.file_to_graph(
        stream,
        use_uuid=False,
        output_version=VERSION,
    )
    assert graph == graphs.NORMAL_GRAPH_1_1


def test_script_stream():
    stream = scripts_paths.NORMAL_SCRIPT_1_1.open("r", encoding="utf-8")
    graph = convomeld.file_to_graph(
        stream,
        use_uuid=False,
        output_version=VERSION,
    )
    assert graph == graphs.NORMAL_GRAPH_1_1


def test_convoyaml_local_url():
    filepath = graphs_paths.NORMAL_GRAPH_1_1.as_posix()
    url = "file:///" + filepath
    graph = convomeld.file_to_graph(
        url,
        use_uuid=False,
        output_version=VERSION,
    )
    assert graph == graphs.NORMAL_GRAPH_1_1


def test_script_local_url():
    filepath = scripts_paths.NORMAL_SCRIPT_1_1.as_posix()
    url = "file:///" + filepath
    graph = convomeld.file_to_graph(
        url,
        use_uuid=False,
        output_version=VERSION,
    )
    assert graph == graphs.NORMAL_GRAPH_1_1
