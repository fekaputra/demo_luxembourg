import morph_kgc

config = """
            [DataSource]
            mappings: mapping/mapping_file.rml.ttl
            file_path: https://semantics.id/resource/ontotrans_demo/alloy_data_simplified.csv
         """

graph = morph_kgc.materialize(config)
for s, p, o in graph:
    print(s, p, o)