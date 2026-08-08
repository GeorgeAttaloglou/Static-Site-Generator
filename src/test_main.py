import os
import shutil
import tempfile
import unittest

from main import copy_dir_to_public


class TestCopyDirToPublic(unittest.TestCase):
    """
    copy_dir_to_public() operates on hardcoded relative paths ('static'
    and 'public'), so each test runs inside its own temporary directory
    that we chdir into, to avoid touching the real project files and to
    keep tests isolated from each other.
    """

    def setUp(self):
        self._orig_cwd = os.getcwd()
        self._tmp_dir = tempfile.mkdtemp()
        os.chdir(self._tmp_dir)

    def tearDown(self):
        os.chdir(self._orig_cwd)
        shutil.rmtree(self._tmp_dir, ignore_errors=True)

    def _make_static(self, files: dict):
        """files: {relative_path: content}. Creates 'static/' plus any
        needed subdirectories and writes each file's content."""
        os.makedirs('static', exist_ok=True)
        for rel_path, content in files.items():
            full_path = os.path.join('static', rel_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w') as f:
                f.write(content)

    def _list_files(self, top: str) -> set:
        found = set()
        for root, _dirs, files in os.walk(top):
            for f in files:
                rel = os.path.relpath(os.path.join(root, f), top)
                found.add(rel)
        return found

    def test_raises_if_source_missing(self):
        # Neither 'static' nor 'public' exist at all.
        with self.assertRaises(Exception):
            copy_dir_to_public()

    def test_raises_if_source_missing_even_when_destination_exists(self):
        os.makedirs('public')
        with self.assertRaises(Exception):
            copy_dir_to_public()

    def test_creates_public_when_it_does_not_exist_yet(self):
        # Regression test: this is the state of a fresh checkout before
        # the very first build. The old code raised
        # "Error: Invalid destination directory" here, which meant the
        # script could never succeed on its first run.
        self._make_static({'index.html': '<html></html>'})
        self.assertFalse(os.path.exists('public'))

        copy_dir_to_public()

        self.assertTrue(os.path.exists('public'))
        with open('public/index.html') as f:
            self.assertEqual(f.read(), '<html></html>')

    def test_removes_stale_files_from_existing_public(self):
        self._make_static({'index.html': 'new content'})
        os.makedirs('public')
        with open('public/stale.txt', 'w') as f:
            f.write('should be removed')

        copy_dir_to_public()

        self.assertFalse(os.path.exists('public/stale.txt'))
        with open('public/index.html') as f:
            self.assertEqual(f.read(), 'new content')

    def test_copies_file_contents_correctly(self):
        self._make_static({'style.css': 'body { color: red; }'})

        copy_dir_to_public()

        with open('public/style.css') as f:
            self.assertEqual(f.read(), 'body { color: red; }')

    def test_copies_nested_directory_structure(self):
        self._make_static({
            'index.html': '<html></html>',
            'css/style.css': 'body{}',
            'images/nested/deep/logo.txt': 'fake logo bytes',
        })

        copy_dir_to_public()

        self.assertEqual(
            self._list_files('static'), self._list_files('public')
        )
        with open('public/images/nested/deep/logo.txt') as f:
            self.assertEqual(f.read(), 'fake logo bytes')

    def test_public_exactly_mirrors_static_no_extra_or_missing_files(self):
        self._make_static({
            'a.txt': '1',
            'sub/b.txt': '2',
            'sub/sub2/c.txt': '3',
        })
        os.makedirs('public')
        with open('public/leftover.txt', 'w') as f:
            f.write('old build artifact')

        copy_dir_to_public()

        self.assertEqual(
            self._list_files('static'), self._list_files('public')
        )

    def test_empty_static_directory_produces_empty_public(self):
        os.makedirs('static')

        copy_dir_to_public()

        self.assertTrue(os.path.exists('public'))
        self.assertEqual(self._list_files('public'), set())

    def test_can_run_twice_in_a_row(self):
        # A second build (e.g. running the script again after editing
        # source files) should succeed and reflect the latest content,
        # not fail because 'public' already exists from the first run.
        self._make_static({'index.html': 'version one'})
        copy_dir_to_public()

        self._make_static({'index.html': 'version two'})
        copy_dir_to_public()

        with open('public/index.html') as f:
            self.assertEqual(f.read(), 'version two')