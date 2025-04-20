import os
import tempfile
import shutil
import pytest
from file_query_text.main import parse_query, QueryVisitor, execute_query


@pytest.fixture
def test_dir():
    """Create a temporary directory structure with test files."""
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()

    # Create a nested directory structure
    community_dir = os.path.join(temp_dir, "community")
    os.makedirs(community_dir)

    loaders_dir = os.path.join(community_dir, "loaders")
    os.makedirs(loaders_dir)

    # Create test files
    with open(os.path.join(loaders_dir, "recursive_url_loader.py"), "w") as f:
        f.write("# Test file")

    with open(os.path.join(loaders_dir, "other_loader.py"), "w") as f:
        f.write("# Test file")

    with open(os.path.join(community_dir, "recursive_other.py"), "w") as f:
        f.write("# Test file")

    with open(os.path.join(temp_dir, "unrelated.py"), "w") as f:
        f.write("# Test file")

    # Provide the directory to the test
    yield temp_dir

    # Clean up after the test
    shutil.rmtree(temp_dir)


def test_single_condition(test_dir):
    """Test that single conditions work correctly."""
    query_str = f"SELECT * FROM '{test_dir}' WHERE extension = 'py'"
    parsed = parse_query(query_str)
    visitor = QueryVisitor()
    visitor.visit(parsed)
    results = execute_query(visitor.select, visitor.from_dirs, visitor.where)

    # Should find all 4 .py files
    assert len(results) == 4


def test_two_and_conditions(test_dir):
    """Test that two AND conditions work correctly."""
    query_str = f"SELECT * FROM '{test_dir}' WHERE path LIKE '%community%' AND extension = 'py'"
    parsed = parse_query(query_str)
    visitor = QueryVisitor()
    visitor.visit(parsed)
    results = execute_query(visitor.select, visitor.from_dirs, visitor.where)

    # Should find 3 files in the community directory
    assert len(results) == 3

    # Verify all results have community in the path
    for file_path in results:
        assert "community" in file_path


def test_three_and_conditions(test_dir):
    """Test that three AND conditions work correctly with our fix."""
    query_str = f"SELECT * FROM '{test_dir}' WHERE path LIKE '%community%' AND path LIKE '%loaders%' AND name LIKE 'recursive%'"
    parsed = parse_query(query_str)
    visitor = QueryVisitor()
    visitor.visit(parsed)
    results = execute_query(visitor.select, visitor.from_dirs, visitor.where)

    # Should find the recursive_url_loader.py file
    expected_file = os.path.join(test_dir, "community", "loaders", "recursive_url_loader.py")

    assert len(results) == 1
    assert "recursive_url_loader.py" in results[0]


def test_complex_query_similar_to_user_example(test_dir):
    """Test a query similar to the one in the user's example."""
    query_str = f"SELECT * FROM '{test_dir}' WHERE path LIKE '%community%' AND name LIKE '%recursive%' AND extension = 'py'"
    parsed = parse_query(query_str)
    visitor = QueryVisitor()
    visitor.visit(parsed)
    results = execute_query(visitor.select, visitor.from_dirs, visitor.where)

    # Should find recursive_url_loader.py and recursive_other.py
    expected_count = 2
    expected_files = [
        os.path.join(test_dir, "community", "loaders", "recursive_url_loader.py"),
        os.path.join(test_dir, "community", "recursive_other.py")
    ]

    assert len(results) == expected_count

    # Check that all expected files are in results (regardless of order)
    for expected_file in expected_files:
        assert any(os.path.samefile(expected_file, result) for result in results)
