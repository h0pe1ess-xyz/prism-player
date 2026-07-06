import ast
import sys

def remove_functions(source_file, func_names, output_file):
    with open(source_file, 'r') as f:
        source_lines = f.readlines()
    
    with open(source_file, 'r') as f:
        tree = ast.parse(f.read())

    # Find the line ranges of functions to delete
    ranges_to_delete = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in func_names:
            start = node.lineno - 1
            end = node.end_lineno
            ranges_to_delete.append((start, end))
            
    # Sort in reverse order so deleting from bottom doesn't shift indices of top
    ranges_to_delete.sort(key=lambda x: x[0], reverse=True)
    
    for start, end in ranges_to_delete:
        del source_lines[start:end]

    with open(output_file, 'w') as f:
        f.writelines(source_lines)

if __name__ == '__main__':
    funcs = sys.argv[2].split(',')
    remove_functions(sys.argv[1], funcs, sys.argv[3])
