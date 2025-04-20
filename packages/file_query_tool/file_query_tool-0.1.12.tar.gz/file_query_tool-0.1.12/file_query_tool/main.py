import os
import sys
from file_query_tool.grammar import query  # Import the fixed grammar
import file_query_tool.gitignore_parser as gitignore_parser
import os.path
import re


def parse_query(query_str):
    try:
        # Increase recursion limit temporarily to handle complex queries
        old_limit = sys.getrecursionlimit()
        sys.setrecursionlimit(2000)

        parsed = query.parseString(query_str, parseAll=True)

        # Restore original recursion limit
        sys.setrecursionlimit(old_limit)
        return parsed
    except Exception as e:
        print(f"Parse error: {e}")
        return None

class QueryVisitor:
    def __init__(self):
        self.select = []
        self.from_dirs = []
        self.where = None

    def visit(self, parsed_query):
        self.select = parsed_query.get("select", ["*"])
        self.from_dirs = parsed_query.get("from_dirs", [])
        self.where = parsed_query.get("where", None)

def execute_query(select, from_dirs, where_conditions, respect_gitignore=True, show_hidden=False):
    matched_files = []

    # Set up gitignore matching if requested
    gitignore_matchers = {}

    # Increase recursion limit to handle deeply nested expressions
    old_limit = sys.getrecursionlimit()
    sys.setrecursionlimit(2000)

    try:
        for directory in from_dirs:
            if not os.path.exists(directory):
                continue

            # Initialize gitignore matcher for this directory
            if respect_gitignore:
                # Find the repository root (where .git directory is)
                repo_root = directory
                while repo_root != os.path.dirname(repo_root):  # Stop at filesystem root
                    if os.path.exists(os.path.join(repo_root, '.git')):
                        break
                    repo_root = os.path.dirname(repo_root)

                # If we found a git repo, check for .gitignore
                gitignore_path = os.path.join(repo_root, '.gitignore')
                if os.path.exists(gitignore_path):
                    if repo_root not in gitignore_matchers:
                        try:
                            gitignore_matchers[repo_root] = gitignore_parser.parse_gitignore(gitignore_path)
                        except Exception as e:
                            print(f"Warning: Error parsing .gitignore at {gitignore_path}: {e}")

            for root, _, files in os.walk(directory):
                for filename in files:
                    file_path = os.path.join(root, filename)

                    # Skip hidden files or files in hidden directories unless explicitly requested
                    if not show_hidden:
                        # Check if file name starts with dot
                        if os.path.basename(file_path).startswith('.'):
                            continue

                        # Check if any parent directory starts with dot
                        rel_path = os.path.relpath(file_path, directory)
                        path_parts = rel_path.split(os.sep)
                        if any(part.startswith('.') for part in path_parts[:-1]):  # Check all except the filename
                            continue

                    # Check if file is ignored by gitignore rules
                    if respect_gitignore:
                        # Find which repo this file belongs to
                        file_repo_root = None
                        for repo_root in gitignore_matchers:
                            if file_path.startswith(repo_root):
                                file_repo_root = repo_root
                                break

                        # Skip if file is ignored by gitignore
                        if file_repo_root and gitignore_matchers[file_repo_root](file_path):
                            continue

                    if evaluate_conditions(file_path, where_conditions):
                        matched_files.append(file_path)
    finally:
        # Restore original recursion limit
        sys.setrecursionlimit(old_limit)

    return matched_files

def evaluate_conditions(file_path, condition):
    if not condition:
        return True

    # Debug current file being evaluated
    print(f"DEBUG Evaluating file: {file_path}")

    # Get the relative path for comparison
    cwd = os.getcwd()
    try:
        relative_path = os.path.relpath(file_path, cwd)
    except ValueError:
        # Handle case when on different drives (Windows)
        relative_path = file_path

    def get_file_attr(attr_name):
        if attr_name == "extension":
            return os.path.splitext(file_path)[1][1:]
        if attr_name == "name":
            return os.path.basename(file_path)
        if attr_name == "size":
            return os.path.getsize(file_path)
        if attr_name == "path":
            return relative_path  # Use relative path instead of absolute
        # Add more attributes as needed
        return None

    # Evaluation function for expressions
    def eval_expr(expr):
        # Debug output
        print(f"DEBUG Evaluating: {expr}")
        result = None

        if not isinstance(expr, list):
            return expr  # For simple terms like 'AND', 'OR'

        # Parenthesized groups may come as a list within a list
        if len(expr) == 1 and isinstance(expr[0], list):
            result = eval_expr(expr[0])
            print(f"DEBUG Parenthesized result: {result}")
            return result

        # Handle complex OR chains
        # If we have more than 3 elements and alternating 'OR's, evaluate the chain
        if len(expr) > 3 and all(expr[i] == 'OR' for i in range(1, len(expr), 2)):
            # This is an OR chain like [cond1, 'OR', cond2, 'OR', cond3, ...]
            for i in range(0, len(expr), 2):
                if eval_expr(expr[i]):
                    print(f"DEBUG OR chain: condition at index {i} is True => True")
                    return True
            print(f"DEBUG OR chain: all conditions are False => False")
            return False

        # Handle complex AND chains
        # If we have more than 3 elements and alternating 'AND's, evaluate the chain
        if len(expr) > 3 and all(expr[i] == 'AND' for i in range(1, len(expr), 2)):
            # This is an AND chain like [cond1, 'AND', cond2, 'AND', cond3, ...]
            for i in range(0, len(expr), 2):
                # Short-circuit if any condition is False
                if not eval_expr(expr[i]):
                    print(f"DEBUG AND chain: condition at index {i} is False => False")
                    return False
            print(f"DEBUG AND chain: all conditions are True => True")
            return True

        if len(expr) == 3:
            # Handle three types of expressions:

            # 1. Basic condition: [attr, op, value]
            if isinstance(expr[0], str) and isinstance(expr[1], str):
                attr_name = expr[0]
                attr_val = get_file_attr(attr_name)
                op = expr[1]
                val = expr[2].strip("'") if isinstance(expr[2], str) else expr[2]  # Remove quotes if string

                if op == "=" or op == "==": result = str(attr_val) == val
                if op == "!=" or op == "<>": result = str(attr_val) != val
                if op == "<": result = attr_val is not None and int(attr_val) < int(val)
                if op == "<=": result = attr_val is not None and int(attr_val) <= int(val)
                if op == ">": result = attr_val is not None and int(attr_val) > int(val)
                if op == ">=": result = attr_val is not None and int(attr_val) >= int(val)
                if op.upper() == "LIKE":
                    result = check_like_condition(attr_val, val)

                print(f"DEBUG Basic condition: {expr[0]} {expr[1]} {expr[2]} => {result}")
                return result

            # 2. Logical operations from infixNotation: [left, op, right]
            elif expr[1] == "AND":
                left = eval_expr(expr[0])
                # Short-circuit if left is False
                if not left:
                    print(f"DEBUG AND short-circuit: {left} AND ... => False")
                    return False
                right = eval_expr(expr[2])
                result = left and right
                print(f"DEBUG AND: {left} AND {right} => {result}")
                return result
            elif expr[1] == "OR":
                left = eval_expr(expr[0])
                # Short-circuit if left is True
                if left:
                    print(f"DEBUG OR short-circuit: {left} OR ... => True")
                    return True
                right = eval_expr(expr[2])
                result = left or right
                print(f"DEBUG OR: {left} OR {right} => {result}")
                return result

        # 3. NOT operation: ['NOT', expr]
        elif len(expr) == 2 and expr[0] == "NOT":
            inner_result = eval_expr(expr[1])
            result = not inner_result
            print(f"DEBUG NOT: NOT {inner_result} => {result}")
            return result

        # 4. Special case for NOT LIKE: [attr, 'NOT', 'LIKE', value]
        elif len(expr) == 4 and expr[1] == "NOT" and expr[2] == "LIKE":
            attr_name = expr[0]
            attr_val = get_file_attr(attr_name)
            val = expr[3].strip("'") if isinstance(expr[3], str) else expr[3]

            if attr_val is None:
                result = True  # If attribute doesn't exist, NOT LIKE is True
            else:
                result = not check_like_condition(attr_val, val)

            print(f"DEBUG NOT LIKE: {attr_name} NOT LIKE {val} => {result}")
            return result

        print(f"DEBUG Unhandled expression: {expr} => False")
        return False

    # Helper function to check LIKE conditions with proper pattern matching
    def check_like_condition(attr_val, val):
        if attr_val is None:
            return False
        # Convert SQL LIKE pattern (with % wildcards) to regex pattern
        # Escape any regex special characters in the pattern except %
        pattern = re.escape(val).replace('\\%', '%')  # Unescape % after escaping everything else
        pattern = pattern.replace("%", ".*")
        pattern = f"^{pattern}$"  # Anchor pattern to match whole string
        return bool(re.search(pattern, str(attr_val), re.IGNORECASE))

    return eval_expr(condition.asList())

# Function to get all attributes for a file
def get_file_attributes(file_path):
    """Get all available attributes for a file."""
    cwd = os.getcwd()
    try:
        # Make path relative to current directory
        rel_path = os.path.relpath(file_path, cwd)
    except ValueError:
        # Handle case when on different drives (Windows)
        rel_path = file_path

    attributes = {
        "extension": os.path.splitext(file_path)[1][1:],
        "name": os.path.basename(file_path),
        "size": os.path.getsize(file_path),
        "path": rel_path,  # Use relative path for consistency
    }
    return attributes

# Example usage
if __name__ == "__main__":
    # Get project root directory for demonstration
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    src_dir = os.path.join(project_root, "src")
    tests_dir = os.path.join(project_root, "tests")
    query_str = f"SELECT * FROM '{src_dir}', '{tests_dir}' WHERE extension == 'py'"
    parsed = parse_query(query_str)
    if parsed:
        visitor = QueryVisitor()
        visitor.visit(parsed)
        results = execute_query(visitor.select, visitor.from_dirs, visitor.where)
        print("Matching files:")
        for file in results:
            # Skip files in .venv directory
            if ".venv" not in file:
                print(file)
