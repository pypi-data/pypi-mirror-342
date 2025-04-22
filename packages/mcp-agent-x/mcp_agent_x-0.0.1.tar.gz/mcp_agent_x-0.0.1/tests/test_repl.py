"""
Tests for the REPL module.
"""

import tempfile
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, mock

from langchain.schema import AIMessage, HumanMessage, SystemMessage

from mcpx.repl import AgentREPL


class TestAgentREPLHistory(IsolatedAsyncioTestCase):
    """Tests for the AgentREPL class focusing on conversation history handling."""

    def setUp(self):
        """Set up test environment."""
        # Create temporary directory
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_data_dir = Path(self.temp_dir.name)
        self.test_history_file = self.test_data_dir / "history.json"
        self.test_commands_file = self.test_data_dir / "default_commands.txt"

        # Create mock agent
        self.mock_agent = mock.MagicMock()
        self.mock_agent._agent = mock.MagicMock()
        self.mock_agent._agent.run = mock.AsyncMock()
        self.mock_agent.initialize = mock.AsyncMock()
        self.mock_agent.close = mock.AsyncMock()
        self.mock_agent.set_system_message = mock.MagicMock()

        # Create mock console
        self.mock_console = mock.MagicMock()

        # Patch history file path
        self.history_file_patch = mock.patch(
            "mcpx.repl.HISTORY_FILE", self.test_history_file
        )
        self.history_file_patch.start()

        # Patch load_history and save_history
        self.load_history_patch = mock.patch("mcpx.repl.load_history")
        self.mock_load_history = self.load_history_patch.start()
        self.mock_load_history.return_value = {"conversations": {}}

        self.save_history_patch = mock.patch("mcpx.repl.save_history")
        self.mock_save_history = self.save_history_patch.start()

        # Patch Rich console
        self.console_patch = mock.patch(
            "mcpx.repl.Console", return_value=self.mock_console
        )
        self.console_patch.start()

        # Patch prompt session
        self.mock_session = mock.MagicMock()
        self.mock_session.prompt_async = mock.AsyncMock()
        self.session_patch = mock.patch(
            "mcpx.repl.PromptSession", return_value=self.mock_session
        )
        self.session_patch.start()

        # Patch signal handlers
        self.signal_patch = mock.patch("mcpx.repl.signal.signal")
        self.signal_patch.start()

        # System prompt for testing
        self.system_prompt = "Test system prompt"

    def tearDown(self):
        """Clean up after tests."""
        # Stop patches
        self.history_file_patch.stop()
        self.console_patch.stop()
        self.session_patch.stop()
        self.signal_patch.stop()
        self.load_history_patch.stop()
        self.save_history_patch.stop()

        # Remove temp directory
        self.temp_dir.cleanup()

    async def test_load_conversation_empty(self):
        """Test loading conversation when history is empty."""
        # Set up mock to return empty conversations
        self.mock_load_history.return_value = {"conversations": {}}

        # Create REPL
        repl = AgentREPL(
            self.mock_agent, system_prompt=self.system_prompt, session_id="test"
        )

        # Check that system message was added
        self.assertEqual(1, len(repl.messages))
        self.assertIsInstance(repl.messages[0], SystemMessage)
        self.assertEqual(self.system_prompt, repl.messages[0].content)

    async def test_load_conversation_existing(self):
        """Test loading conversation when history exists."""
        # Set up mock to return a conversation
        self.mock_load_history.return_value = {
            "conversations": {
                "test": [
                    {"type": "system", "content": self.system_prompt},
                    {"type": "human", "content": "Human message"},
                    {"type": "ai", "content": "AI message"},
                ]
            }
        }

        # Create REPL
        repl = AgentREPL(
            self.mock_agent, system_prompt=self.system_prompt, session_id="test"
        )

        # Check that messages were loaded
        self.assertEqual(3, len(repl.messages))
        self.assertIsInstance(repl.messages[0], SystemMessage)
        self.assertIsInstance(repl.messages[1], HumanMessage)
        self.assertIsInstance(repl.messages[2], AIMessage)

    async def test_save_conversation(self):
        """Test saving conversation."""
        # Set up mock to return empty conversations
        self.mock_load_history.return_value = {"conversations": {}}

        # Create REPL
        repl = AgentREPL(
            self.mock_agent, system_prompt=self.system_prompt, session_id="test"
        )

        # Add messages
        repl.messages.append(HumanMessage(content="Human message"))
        repl.messages.append(AIMessage(content="AI message"))

        # Save conversation
        repl._save_conversation()

        # Check that save_history was called with the correct arguments
        self.mock_save_history.assert_called_once()
        saved_data = self.mock_save_history.call_args[0][0]
        self.assertIn("conversations", saved_data)
        self.assertIn("test", saved_data["conversations"])
        self.assertEqual(3, len(saved_data["conversations"]["test"]))

    async def test_handles_list_format_conversation(self):
        """Test that the REPL can handle the legacy list format for conversations."""
        # Set up mock to return a conversation in list format
        self.mock_load_history.return_value = {
            "conversations": [
                {"type": "system", "content": self.system_prompt},
                {"type": "human", "content": "Human message"},
                {"type": "ai", "content": "AI message"},
            ]
        }

        # Create REPL
        repl = AgentREPL(
            self.mock_agent, system_prompt=self.system_prompt, session_id="test"
        )

        # Check that messages were loaded from the list format
        self.assertEqual(3, len(repl.messages))
        self.assertIsInstance(repl.messages[0], SystemMessage)
        self.assertIsInstance(repl.messages[1], HumanMessage)
        self.assertIsInstance(repl.messages[2], AIMessage)

    async def test_handles_corrupted_history(self):
        """Test that the REPL gracefully handles corrupted history files."""
        # Set up mock to raise an exception
        self.mock_load_history.side_effect = Exception("Corrupted data")

        # Create REPL - this should not raise an exception
        repl = AgentREPL(
            self.mock_agent, system_prompt=self.system_prompt, session_id="test"
        )

        # Check that system message was added
        self.assertEqual(1, len(repl.messages))
        self.assertIsInstance(repl.messages[0], SystemMessage)

    async def test_conversation_round_trip(self):
        """Test a full round trip of loading, adding messages, and saving."""
        # Set up mock to return initial history
        self.mock_load_history.return_value = {
            "conversations": {
                "test": [{"type": "system", "content": self.system_prompt}]
            }
        }

        # Create REPL
        repl = AgentREPL(
            self.mock_agent, system_prompt=self.system_prompt, session_id="test"
        )

        # Check initial message
        self.assertEqual(1, len(repl.messages))

        # Add messages
        repl.messages.append(HumanMessage(content="First question"))
        repl.messages.append(AIMessage(content="First answer"))

        # Save conversation
        repl._save_conversation()

        # Set up mock to return the updated conversation
        self.mock_load_history.return_value = {
            "conversations": {
                "test": [
                    {"type": "system", "content": self.system_prompt},
                    {"type": "human", "content": "First question"},
                    {"type": "ai", "content": "First answer"},
                ]
            }
        }

        # Create a new REPL (should load the saved conversation)
        repl2 = AgentREPL(
            self.mock_agent, system_prompt=self.system_prompt, session_id="test"
        )

        # Check that all messages were loaded
        self.assertEqual(3, len(repl2.messages))
        self.assertIsInstance(repl2.messages[0], SystemMessage)
        self.assertIsInstance(repl2.messages[1], HumanMessage)
        self.assertIsInstance(repl2.messages[2], AIMessage)
        self.assertEqual("First question", repl2.messages[1].content)
        self.assertEqual("First answer", repl2.messages[2].content)

    @mock.patch("mcpx.repl.FileHistory")
    async def test_file_history_initialization(self, mock_file_history):
        """Test that the FileHistory is correctly initialized."""
        # Create REPL
        AgentREPL(self.mock_agent, system_prompt=self.system_prompt, session_id="test")

        # Check that FileHistory was created with correct path
        mock_file_history.assert_called_once()
        file_path = mock_file_history.call_args[0][0]
        self.assertIn("test_commands.txt", file_path)
