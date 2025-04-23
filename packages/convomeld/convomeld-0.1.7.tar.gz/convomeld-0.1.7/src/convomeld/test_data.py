import yaml
from convomeld.constants import DATA_DIR


def get_script_path(filename):
    return DATA_DIR / "test" / "scripts" / filename


def get_graph_path(version, subfolder, filename):
    return DATA_DIR / "test" / "graphs" / version / subfolder / filename


def read_script(script_path):
    with script_path.open() as stream:
        return [line.rstrip() for line in stream]


def read_graph(graph_path):
    with graph_path.open() as stream:
        return yaml.safe_load(stream)


BOT_NAME = "teacher"


# Scripts
class ScriptsTestData:
    class Paths:
        def __init__(self):
            self.NORMAL_SCRIPT_1_1 = get_script_path("count_by_one_1_1.txt")
            self.NORMAL_SCRIPT_1_2 = get_script_path("count_by_one_1_2.txt")
            self.NORMAL_SCRIPT_1_3 = get_script_path("count_by_one_1_3.txt")
            self.NORMAL_SCRIPT_1_1_HUMAN_STOP_EARLY = get_script_path(
                "count_by_one_1_1_student_stop_early.txt"
            )
            self.NORMAL_SCRIPT_1_1_BOT_STOP_EARLY = get_script_path(
                "count_by_one_1_1_teacher_stop_early.txt"
            )
            self.NORMAL_SCRIPT_2_1 = get_script_path("count_by_one_2_1.txt")
            self.NORMAL_SCRIPT_2_2 = get_script_path("count_by_one_2_2.txt")
            self.NORMAL_SCRIPT_2_3 = get_script_path("count_by_one_2_3.txt")
            self.NORMAL_SCRIPT_2_HUMAN_STOP_EARLY_1 = get_script_path(
                "count_by_one_2_student_stop_early_1.txt"
            )
            self.NORMAL_SCRIPT_2_HUMAN_STOP_EARLY_2 = get_script_path(
                "count_by_one_2_student_stop_early_2.txt"
            )
            self.NORMAL_SCRIPT_2_HUMAN_STOP_EARLY_3 = get_script_path(
                "count_by_one_2_student_stop_early_3.txt"
            )

    class Scripts:
        def __init__(self, paths):
            self.NORMAL_SCRIPT_1_1 = read_script(paths.NORMAL_SCRIPT_1_1)
            self.NORMAL_SCRIPT_1_2 = read_script(paths.NORMAL_SCRIPT_1_2)
            self.NORMAL_SCRIPT_1_3 = read_script(paths.NORMAL_SCRIPT_1_3)
            self.NORMAL_SCRIPT_1_1_HUMAN_STOP_EARLY = read_script(
                paths.NORMAL_SCRIPT_1_1_HUMAN_STOP_EARLY
            )
            self.NORMAL_SCRIPT_1_1_BOT_STOP_EARLY = read_script(
                paths.NORMAL_SCRIPT_1_1_BOT_STOP_EARLY
            )
            self.NORMAL_SCRIPT_2_1 = read_script(paths.NORMAL_SCRIPT_2_1)
            self.NORMAL_SCRIPT_2_2 = read_script(paths.NORMAL_SCRIPT_2_2)
            self.NORMAL_SCRIPT_2_3 = read_script(paths.NORMAL_SCRIPT_2_3)
            self.NORMAL_SCRIPT_2_HUMAN_STOP_EARLY_1 = read_script(
                paths.NORMAL_SCRIPT_2_HUMAN_STOP_EARLY_1
            )
            self.NORMAL_SCRIPT_2_HUMAN_STOP_EARLY_2 = read_script(
                paths.NORMAL_SCRIPT_2_HUMAN_STOP_EARLY_2
            )
            self.NORMAL_SCRIPT_2_HUMAN_STOP_EARLY_3 = read_script(
                paths.NORMAL_SCRIPT_2_HUMAN_STOP_EARLY_3
            )

    def __init__(self):
        self.paths = ScriptsTestData.Paths()
        self.scripts = ScriptsTestData.Scripts(self.paths)


scripts_data = ScriptsTestData()
scripts = scripts_data.scripts
scripts_paths = scripts_data.paths


if __name__ == "__main__":
    from convomeld.graph import ConvoGraph

    def build_parsed_graph(out_filename, script):
        graph = ConvoGraph.from_script_lines(
            script, base_author=BOT_NAME, use_uuid=False
        )
        path = (
            DATA_DIR / "test" / "graphs" / "{v}" / "parsed" / out_filename
        ).as_posix()
        graph.to_yaml(path.format(v="v2"), "v2")
        graph.to_yaml(path.format(v="v3"), "v3")

    def build_parsed_graphs():
        scripts = scripts_data.scripts

        # count_by_one_1
        build_parsed_graph("count_by_one_1_1", scripts.NORMAL_SCRIPT_1_1)
        build_parsed_graph("count_by_one_1_2", scripts.NORMAL_SCRIPT_1_2)
        build_parsed_graph("count_by_one_1_3", scripts.NORMAL_SCRIPT_1_3)
        build_parsed_graph(
            "count_by_one_1_1_student_stop_early",
            scripts.NORMAL_SCRIPT_1_1_HUMAN_STOP_EARLY,
        )
        build_parsed_graph(
            "count_by_one_1_1_teacher_stop_early",
            scripts.NORMAL_SCRIPT_1_1_BOT_STOP_EARLY,
        )
        # count_by_one_2
        build_parsed_graph("count_by_one_2_1", scripts.NORMAL_SCRIPT_2_1)
        build_parsed_graph("count_by_one_2_2", scripts.NORMAL_SCRIPT_2_2)
        build_parsed_graph("count_by_one_2_3", scripts.NORMAL_SCRIPT_2_3)
        build_parsed_graph(
            "count_by_one_2_student_stop_early_1",
            scripts.NORMAL_SCRIPT_2_HUMAN_STOP_EARLY_1,
        )
        build_parsed_graph(
            "count_by_one_2_student_stop_early_2",
            scripts.NORMAL_SCRIPT_2_HUMAN_STOP_EARLY_2,
        )
        build_parsed_graph(
            "count_by_one_2_student_stop_early_3",
            scripts.NORMAL_SCRIPT_2_HUMAN_STOP_EARLY_3,
        )

    build_parsed_graphs()


class ParsedGraphsTestData:
    class Paths:
        def __init__(self, version):
            # count_by_one_1
            self.NORMAL_GRAPH_1_1 = get_graph_path(
                version, "parsed", "count_by_one_1_1.yml"
            )
            self.NORMAL_GRAPH_1_2 = get_graph_path(
                version, "parsed", "count_by_one_1_2.yml"
            )
            self.NORMAL_GRAPH_1_3 = get_graph_path(
                version, "parsed", "count_by_one_1_3.yml"
            )
            self.NORMAL_GRAPH_1_1_HUMAN_STOP_EARLY = get_graph_path(
                version, "parsed", "count_by_one_1_1_student_stop_early.yml"
            )
            self.NORMAL_GRAPH_1_1_BOT_STOP_EARLY = get_graph_path(
                version, "parsed", "count_by_one_1_1_teacher_stop_early.yml"
            )
            # count_by_one_2
            self.NORMAL_GRAPH_2_1 = get_graph_path(
                version, "parsed", "count_by_one_2_1.yml"
            )
            self.NORMAL_GRAPH_2_2 = get_graph_path(
                version, "parsed", "count_by_one_2_2.yml"
            )
            self.NORMAL_GRAPH_2_3 = get_graph_path(
                version, "parsed", "count_by_one_2_3.yml"
            )
            self.NORMAL_GRAPH_2_HUMAN_STOP_EARLY_1 = get_graph_path(
                version, "parsed", "count_by_one_2_student_stop_early_1.yml"
            )
            self.NORMAL_GRAPH_2_HUMAN_STOP_EARLY_2 = get_graph_path(
                version, "parsed", "count_by_one_2_student_stop_early_2.yml"
            )
            self.NORMAL_GRAPH_2_HUMAN_STOP_EARLY_3 = get_graph_path(
                version, "parsed", "count_by_one_2_student_stop_early_3.yml"
            )

    class Graphs:
        def __init__(self, paths):
            # count_by_one_1
            self.NORMAL_GRAPH_1_1 = read_graph(paths.NORMAL_GRAPH_1_1)
            self.NORMAL_GRAPH_1_2 = read_graph(paths.NORMAL_GRAPH_1_2)
            self.NORMAL_GRAPH_1_3 = read_graph(paths.NORMAL_GRAPH_1_3)
            self.NORMAL_GRAPH_1_1_HUMAN_STOP_EARLY = read_graph(
                paths.NORMAL_GRAPH_1_1_HUMAN_STOP_EARLY
            )
            self.NORMAL_GRAPH_1_1_BOT_STOP_EARLY = read_graph(
                paths.NORMAL_GRAPH_1_1_BOT_STOP_EARLY
            )
            # count_by_one_2
            self.NORMAL_GRAPH_2_1 = read_graph(paths.NORMAL_GRAPH_2_1)
            self.NORMAL_GRAPH_2_2 = read_graph(paths.NORMAL_GRAPH_2_2)
            self.NORMAL_GRAPH_2_3 = read_graph(paths.NORMAL_GRAPH_2_3)
            self.NORMAL_GRAPH_2_HUMAN_STOP_EARLY_1 = read_graph(
                paths.NORMAL_GRAPH_2_HUMAN_STOP_EARLY_1
            )
            self.NORMAL_GRAPH_2_HUMAN_STOP_EARLY_2 = read_graph(
                paths.NORMAL_GRAPH_2_HUMAN_STOP_EARLY_2
            )
            self.NORMAL_GRAPH_2_HUMAN_STOP_EARLY_3 = read_graph(
                paths.NORMAL_GRAPH_2_HUMAN_STOP_EARLY_3
            )

    def __init__(self, version):
        self.paths = ParsedGraphsTestData.Paths(version)
        self.graphs = ParsedGraphsTestData.Graphs(self.paths)


parsed_graphs_v2_data = ParsedGraphsTestData("v2")
parsed_graphs_v3_data = ParsedGraphsTestData("v3")


if __name__ == "__main__":
    # Merge graphs
    def build_merged_graph(out_filename, version, *graphs):
        base_graph = None

        for graph in graphs:
            if base_graph is None:
                base_graph = ConvoGraph.from_states_list(
                    graph, use_uuid=False, version=version
                )
            else:
                base_graph = base_graph.merge_graph(
                    ConvoGraph.from_states_list(graph, use_uuid=False, version=version)
                )

        path = (
            DATA_DIR / "test" / "graphs" / version / "merged" / out_filename
        ).as_posix()
        base_graph.to_yaml(path, version)

    def build_merged_graphs():
        parsed_graphs_versions = {
            "v2": parsed_graphs_v2_data.graphs,
            "v3": parsed_graphs_v3_data.graphs,
        }

        for version, parsed_graphs in parsed_graphs_versions.items():
            # count_by_one_1
            build_merged_graph(
                "count_by_one_1_1+1_2",
                version,
                parsed_graphs.NORMAL_GRAPH_1_1,
                parsed_graphs.NORMAL_GRAPH_1_2,
            )
            build_merged_graph(
                "count_by_one_1_1+1_2+1_3",
                version,
                parsed_graphs.NORMAL_GRAPH_1_1,
                parsed_graphs.NORMAL_GRAPH_1_2,
                parsed_graphs.NORMAL_GRAPH_1_3,
            )
            # count_by_one_2
            build_merged_graph(
                "count_by_one_2_1+2_2",
                version,
                parsed_graphs.NORMAL_GRAPH_2_1,
                parsed_graphs.NORMAL_GRAPH_2_2,
            )
            build_merged_graph(
                "count_by_one_2_1+2_3",
                version,
                parsed_graphs.NORMAL_GRAPH_2_1,
                parsed_graphs.NORMAL_GRAPH_2_3,
            )
            build_merged_graph(
                "count_by_one_2_2+2_3",
                version,
                parsed_graphs.NORMAL_GRAPH_2_2,
                parsed_graphs.NORMAL_GRAPH_2_3,
            )
            build_merged_graph(
                "count_by_one_2_1+2_2+2_3",
                version,
                parsed_graphs.NORMAL_GRAPH_2_1,
                parsed_graphs.NORMAL_GRAPH_2_2,
                parsed_graphs.NORMAL_GRAPH_2_3,
            )

    build_merged_graphs()


class MergedGraphsTestData:
    class Paths:
        def __init__(self, version):
            # count_by_one_1
            self.NORMAL_GRAPH_1_1_X_1_2 = get_graph_path(
                version, "merged", "count_by_one_1_1+1_2.yml"
            )
            self.NORMAL_GRAPH_1_1_X_1_2_X_1_3 = get_graph_path(
                version, "merged", "count_by_one_1_1+1_2+1_3.yml"
            )
            # count_by_one_2
            self.NORMAL_GRAPH_2_1_X_2_2 = get_graph_path(
                version, "merged", "count_by_one_2_1+2_2.yml"
            )
            self.NORMAL_GRAPH_2_1_X_2_3 = get_graph_path(
                version, "merged", "count_by_one_2_1+2_3.yml"
            )
            self.NORMAL_GRAPH_2_2_X_2_3 = get_graph_path(
                version, "merged", "count_by_one_2_2+2_3.yml"
            )
            self.NORMAL_GRAPH_2_1_X_2_2_X_2_3 = get_graph_path(
                version, "merged", "count_by_one_2_1+2_2+2_3.yml"
            )

    class Graphs:
        def __init__(self, paths):
            # count_by_one_1
            self.NORMAL_GRAPH_1_1_X_1_2 = read_graph(paths.NORMAL_GRAPH_1_1_X_1_2)
            self.NORMAL_GRAPH_1_1_X_1_2_X_1_3 = read_graph(
                paths.NORMAL_GRAPH_1_1_X_1_2_X_1_3
            )
            # count_by_one_2
            self.NORMAL_GRAPH_2_1_X_2_2 = read_graph(paths.NORMAL_GRAPH_2_1_X_2_2)
            self.NORMAL_GRAPH_2_1_X_2_3 = read_graph(paths.NORMAL_GRAPH_2_1_X_2_3)
            self.NORMAL_GRAPH_2_2_X_2_3 = read_graph(paths.NORMAL_GRAPH_2_2_X_2_3)
            self.NORMAL_GRAPH_2_1_X_2_2_X_2_3 = read_graph(
                paths.NORMAL_GRAPH_2_1_X_2_2_X_2_3
            )

    def __init__(self, version):
        self.paths = MergedGraphsTestData.Paths(version)
        self.graphs = MergedGraphsTestData.Graphs(self.paths)


merged_graphs_v2_data = MergedGraphsTestData("v2")
merged_graphs_v3_data = MergedGraphsTestData("v3")


class GraphsTestData:
    class Paths:
        def __init__(self, parsed_paths, merged_paths):
            # parsed graphs
            self.NORMAL_GRAPH_1_1 = parsed_paths.NORMAL_GRAPH_1_1
            self.NORMAL_GRAPH_1_2 = parsed_paths.NORMAL_GRAPH_1_2
            self.NORMAL_GRAPH_1_3 = parsed_paths.NORMAL_GRAPH_1_3
            self.NORMAL_GRAPH_1_1_HUMAN_STOP_EARLY = (
                parsed_paths.NORMAL_GRAPH_1_1_HUMAN_STOP_EARLY
            )
            self.NORMAL_GRAPH_1_1_BOT_STOP_EARLY = (
                parsed_paths.NORMAL_GRAPH_1_1_BOT_STOP_EARLY
            )
            self.NORMAL_GRAPH_2_1 = parsed_paths.NORMAL_GRAPH_2_1
            self.NORMAL_GRAPH_2_2 = parsed_paths.NORMAL_GRAPH_2_2
            self.NORMAL_GRAPH_2_3 = parsed_paths.NORMAL_GRAPH_2_3
            self.NORMAL_GRAPH_2_HUMAN_STOP_EARLY_1 = (
                parsed_paths.NORMAL_GRAPH_2_HUMAN_STOP_EARLY_1
            )
            self.NORMAL_GRAPH_2_HUMAN_STOP_EARLY_2 = (
                parsed_paths.NORMAL_GRAPH_2_HUMAN_STOP_EARLY_2
            )
            self.NORMAL_GRAPH_2_HUMAN_STOP_EARLY_3 = (
                parsed_paths.NORMAL_GRAPH_2_HUMAN_STOP_EARLY_3
            )
            # merged graphs
            self.NORMAL_GRAPH_1_1_X_1_2 = merged_paths.NORMAL_GRAPH_1_1_X_1_2
            self.NORMAL_GRAPH_1_1_X_1_2_X_1_3 = (
                merged_paths.NORMAL_GRAPH_1_1_X_1_2_X_1_3
            )
            self.NORMAL_GRAPH_2_1_X_2_2 = merged_paths.NORMAL_GRAPH_2_1_X_2_2
            self.NORMAL_GRAPH_2_1_X_2_3 = merged_paths.NORMAL_GRAPH_2_1_X_2_3
            self.NORMAL_GRAPH_2_2_X_2_3 = merged_paths.NORMAL_GRAPH_2_2_X_2_3
            self.NORMAL_GRAPH_2_1_X_2_2_X_2_3 = (
                merged_paths.NORMAL_GRAPH_2_1_X_2_2_X_2_3
            )

    class Graphs:
        def __init__(self, parsed_graphs, merged_graphs):
            # parsed graphs
            self.NORMAL_GRAPH_1_1 = parsed_graphs.NORMAL_GRAPH_1_1
            self.NORMAL_GRAPH_1_2 = parsed_graphs.NORMAL_GRAPH_1_2
            self.NORMAL_GRAPH_1_3 = parsed_graphs.NORMAL_GRAPH_1_3
            self.NORMAL_GRAPH_1_1_HUMAN_STOP_EARLY = (
                parsed_graphs.NORMAL_GRAPH_1_1_HUMAN_STOP_EARLY
            )
            self.NORMAL_GRAPH_1_1_BOT_STOP_EARLY = (
                parsed_graphs.NORMAL_GRAPH_1_1_BOT_STOP_EARLY
            )
            self.NORMAL_GRAPH_2_1 = parsed_graphs.NORMAL_GRAPH_2_1
            self.NORMAL_GRAPH_2_2 = parsed_graphs.NORMAL_GRAPH_2_2
            self.NORMAL_GRAPH_2_3 = parsed_graphs.NORMAL_GRAPH_2_3
            self.NORMAL_GRAPH_2_HUMAN_STOP_EARLY_1 = (
                parsed_graphs.NORMAL_GRAPH_2_HUMAN_STOP_EARLY_1
            )
            self.NORMAL_GRAPH_2_HUMAN_STOP_EARLY_2 = (
                parsed_graphs.NORMAL_GRAPH_2_HUMAN_STOP_EARLY_2
            )
            self.NORMAL_GRAPH_2_HUMAN_STOP_EARLY_3 = (
                parsed_graphs.NORMAL_GRAPH_2_HUMAN_STOP_EARLY_3
            )
            # merged graphs
            self.NORMAL_GRAPH_1_1_X_1_2 = merged_graphs.NORMAL_GRAPH_1_1_X_1_2
            self.NORMAL_GRAPH_1_1_X_1_2_X_1_3 = (
                merged_graphs.NORMAL_GRAPH_1_1_X_1_2_X_1_3
            )
            self.NORMAL_GRAPH_2_1_X_2_2 = merged_graphs.NORMAL_GRAPH_2_1_X_2_2
            self.NORMAL_GRAPH_2_1_X_2_3 = merged_graphs.NORMAL_GRAPH_2_1_X_2_3
            self.NORMAL_GRAPH_2_2_X_2_3 = merged_graphs.NORMAL_GRAPH_2_2_X_2_3
            self.NORMAL_GRAPH_2_1_X_2_2_X_2_3 = (
                merged_graphs.NORMAL_GRAPH_2_1_X_2_2_X_2_3
            )

    def __init__(self, parsed_graphs_data, parsed_merged_data):
        self.paths = GraphsTestData.Paths(
            parsed_graphs_data.paths, parsed_merged_data.paths
        )
        self.graphs = GraphsTestData.Graphs(
            parsed_graphs_data.graphs, parsed_merged_data.graphs
        )


graphs_v2_data = GraphsTestData(parsed_graphs_v2_data, merged_graphs_v2_data)
graphs_v3_data = GraphsTestData(parsed_graphs_v3_data, merged_graphs_v3_data)
graphs_v2 = graphs_v2_data.graphs
graphs_v3 = graphs_v3_data.graphs
graphs_v2_paths = graphs_v2_data.paths
graphs_v3_paths = graphs_v3_data.paths
