import clang.cindex
clang.cindex.Config.set_library_file("/usr/local/opt/llvm/lib/libclang.dylib")

import clang.cindex
clang.cindex.Config.set_library_file("/usr/local/opt/llvm/lib/libclang.dylib")

def parse_file(filename: str, target_class: str):
    index = clang.cindex.Index.create()

    args = [ # compiler arguments
        "-std=c++17",
        "-I/usr/local/include",
        "-I/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/usr/include/c++/v1",
        "-I/Library/Developer/CommandLineTools/usr/lib/clang/15.0.0/include",
        "-I/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/usr/include",
        "-I/Library/Developer/CommandLineTools/usr/include",
    ]

    pointer_fields = []
    non_pointer_fields = []
    label_field = ""

    try:
        tu = index.parse(filename, args=args)
    except clang.cindex.TranslationUnitLoadError:
        print(f"Failed to parse {filename}.")
        return None, [], ""

    for cursor in tu.cursor.get_children():
        if cursor.kind == clang.cindex.CursorKind.CLASS_DECL and cursor.spelling == target_class:
            print(f"Found class: {target_class}")

            for field in cursor.get_children():
                if field.kind == clang.cindex.CursorKind.FIELD_DECL:
                    field_type = field.type.spelling
                    print(f"  -> {field.spelling} : {field_type}")
                    if "*" in field_type:
                        pointer_fields.append(field.spelling)
                    else:
                        non_pointer_fields.append(field.spelling)

            # Pick any field as label
            if non_pointer_fields:
                label_field = non_pointer_fields[0]
            elif pointer_fields:
                label_field = pointer_fields[0]

            return target_class, pointer_fields, label_field

    print(f"Class '{target_class}' not found in {filename}.")
    return None, [], ""






def generate_visualize_cpp(class_name, pointer_fields, filename, label_field = "data"):

    print(f"Generating tree-friendly visualize_autogen.cpp for class '{class_name}'")

    lines = [
        "#include <fstream>",
        "#include <unordered_map>",
        "#include <string>",
        "",
        f"void traverse({class_name}* curr, std::ofstream& out, std::unordered_map<{class_name}*, int>& ids, int& id) {{",
        "    if (!curr) return;",
        "    if (ids.find(curr) != ids.end()) return;  // avoid revisiting",
        "    ids[curr] = id++;",
        f"    out << \"    node\" << ids[curr] << \" [label=\\\"\" << curr->{label_field} << \"\\\"];\\n\";",
    ]

    for field in pointer_fields:
        lines.append(f"    if (curr->{field}) {{")
        lines.append(f"        traverse(curr->{field}, out, ids, id);")
        lines.append(f"        out << \"    node\" << ids[curr] << \" -> node\" << ids[curr->{field}] << \" [label=\\\"{field}\\\"];\\n\";")
        lines.append("    }")

    lines.append("}")

    lines += [
        "",
        f"void visualize({class_name}* root, const std::string& filename) {{",
        "    std::ofstream out(filename);",
        "    out << \"digraph G {\\n\";",
        "    out << \"    node [shape=box];\\n\";",
        "    out << \"    rankdir=TB;\\n\";",  # top-down layout for trees
        f"    std::unordered_map<{class_name}*, int> ids;",
        "    int id = 0;",
        "    traverse(root, out, ids, id);",
        "    out << \"}\\n\";",
        "    out.close();",
        "}"
    ]

    with open("visualize_autogen.cpp", "w") as f:
        f.write("\n".join(lines))

    print(f"Generated visualize_autogen.cpp for class '{class_name}'")
    print(label_field)


source_file = "linklist.cpp"        
class_name = "Node"             

parsed_class, pointer_fields, label_field = parse_file(source_file, class_name)

generate_visualize_cpp(class_name, pointer_fields, source_file)
print(label_field + " label")