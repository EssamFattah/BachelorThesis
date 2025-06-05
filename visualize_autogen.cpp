#include <fstream>
#include <unordered_map>
#include <string>

void traverse(Node* curr, std::ofstream& out, std::unordered_map<Node*, int>& ids, int& id) {
    if (!curr) return;
    if (ids.find(curr) != ids.end()) return;  // avoid revisiting
    ids[curr] = id++;
    out << "    node" << ids[curr] << " [label=\"" << curr->data << "\"];\n";
    if (curr->next) {
        traverse(curr->next, out, ids, id);
        out << "    node" << ids[curr] << " -> node" << ids[curr->next] << " [label=\"next\"];\n";
    }
    if (curr->prev) {
        traverse(curr->prev, out, ids, id);
        out << "    node" << ids[curr] << " -> node" << ids[curr->prev] << " [label=\"prev\"];\n";
    }
}

void visualize(Node* root, const std::string& filename = "output_1000.dot") {
    std::ofstream out(filename);
    out << "digraph G {\n";
    out << "    node [shape=box];\n";
    out << "    rankdir=TB;\n";
    std::unordered_map<Node*, int> ids;
    int id = 0;
    traverse(root, out, ids, id);
    out << "}\n";
    out.close();
}