"""
Tests for the configuration management module.
"""

import json
import tempfile
from pathlib import Path
from unittest import TestCase, mock

from mcpx.config import (
    ensure_config_exists,
    load_history,
    save_history,
)


class TestConfig(TestCase):
    """Tests for the configuration management functionality."""

    def setUp(self):
        """Set up test environment."""
        # Create temporary directories for config and data
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_config_dir = Path(self.temp_dir.name) / "config"
        self.test_data_dir = Path(self.temp_dir.name) / "data"
        self.test_defaults_dir = Path(self.temp_dir.name) / "defaults"
        self.test_config_file = self.test_config_dir / "config.json"
        self.test_system_prompt_file = self.test_config_dir / "system_prompt.md"
        self.test_history_file = self.test_data_dir / "history.json"

        # Create directories
        self.test_config_dir.mkdir(parents=True, exist_ok=True)
        self.test_data_dir.mkdir(parents=True, exist_ok=True)
        self.test_defaults_dir.mkdir(parents=True, exist_ok=True)

        # Create default files
        with open(self.test_defaults_dir / "config.json", "w") as f:
            json.dump({"conversations": {}}, f)
        with open(self.test_defaults_dir / "system_prompt.md", "w") as f:
            f.write("Test system prompt")

        # Set up patches
        self.config_dir_patch = mock.patch(
            "mcpx.config.CONFIG_DIR", self.test_config_dir
        )
        self.data_dir_patch = mock.patch("mcpx.config.DATA_DIR", self.test_data_dir)
        self.defaults_dir_patch = mock.patch(
            "mcpx.config.DEFAULTS_DIR", self.test_defaults_dir
        )
        self.config_file_patch = mock.patch(
            "mcpx.config.CONFIG_FILE", self.test_config_file
        )
        self.system_prompt_file_patch = mock.patch(
            "mcpx.config.SYSTEM_PROMPT_FILE", self.test_system_prompt_file
        )
        self.history_file_patch = mock.patch(
            "mcpx.config.HISTORY_FILE", self.test_history_file
        )

        # Start patches
        self.config_dir_patch.start()
        self.data_dir_patch.start()
        self.defaults_dir_patch.start()
        self.config_file_patch.start()
        self.system_prompt_file_patch.start()
        self.history_file_patch.start()

    def tearDown(self):
        """Clean up after tests."""
        # Stop patches
        self.config_dir_patch.stop()
        self.data_dir_patch.stop()
        self.defaults_dir_patch.stop()
        self.config_file_patch.stop()
        self.system_prompt_file_patch.stop()
        self.history_file_patch.stop()

        # Remove temp directory
        self.temp_dir.cleanup()

    def test_ensure_config_exists(self):
        """Test that ensure_config_exists creates the necessary files and directories."""
        # Ensure config exists
        ensure_config_exists()

        # Check that directories were created
        self.assertTrue(self.test_config_dir.exists())
        self.assertTrue(self.test_data_dir.exists())

        # Check that history file was created with correct structure
        self.assertTrue(self.test_history_file.exists())
        with open(self.test_history_file) as f:
            history_data = json.load(f)
            self.assertIn("conversations", history_data)
            self.assertIsInstance(history_data["conversations"], dict)

    def test_load_history_creates_default_on_error(self):
        """Test that load_history creates a default history file on error."""
        # Write invalid JSON to history file
        with open(self.test_history_file, "w") as f:
            f.write("invalid json")

        # Load history
        history_data = load_history()

        # Check that history data has correct structure
        self.assertIn("conversations", history_data)
        self.assertIsInstance(history_data["conversations"], dict)

        # Check that history file was fixed
        with open(self.test_history_file) as f:
            new_history_data = json.load(f)
            self.assertIn("conversations", new_history_data)
            self.assertIsInstance(new_history_data["conversations"], dict)

    def test_load_history_handles_empty_conversations(self):
        """Test that load_history handles an empty conversations list."""
        # Write history file with empty conversations list
        with open(self.test_history_file, "w") as f:
            json.dump({"conversations": []}, f)

        # Load history
        history_data = load_history()

        # Check that history data has correct structure
        self.assertIn("conversations", history_data)
        # Empty list should be preserved for backward compatibility
        self.assertIsInstance(history_data["conversations"], list)

    def test_save_and_load_history(self):
        """Test that save_history and load_history work together correctly."""
        # Create test history data
        test_history = {
            "conversations": {
                "test_session": [
                    {"type": "system", "content": "System message"},
                    {"type": "human", "content": "Human message"},
                    {"type": "ai", "content": "AI message"},
                ]
            }
        }

        # Save history
        save_history(test_history)

        # Load history
        loaded_history = load_history()

        # Check that loaded history matches test history
        self.assertEqual(test_history, loaded_history)
        self.assertIn("conversations", loaded_history)
        self.assertIn("test_session", loaded_history["conversations"])
        self.assertEqual(3, len(loaded_history["conversations"]["test_session"]))

    def test_history_backup_on_corruption(self):
        """Test that corrupted history files are backed up."""
        # Write a valid history file first
        valid_history = {"conversations": {"session1": []}}
        with open(self.test_history_file, "w") as f:
            json.dump(valid_history, f)

        # Corrupt the file
        with open(self.test_history_file, "w") as f:
            f.write("corrupted data")

        # Load history (this should create a backup)
        load_history()

        # Check that backup file exists
        backup_file = self.test_history_file.with_suffix(".json.bak")
        self.assertTrue(backup_file.exists())

        # Check that backup contains the corrupted data
        with open(backup_file) as f:
            backup_content = f.read()
            self.assertEqual("corrupted data", backup_content)
