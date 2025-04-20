#!/usr/bin/env python3

"""Tests for the ReadFile subtool."""

import os
import unittest

from codemcp.testing import MCPEndToEndTestCase


class ReadFileTest(MCPEndToEndTestCase):
    """Test the ReadFile subtool."""

    async def test_read_file(self):
        """Test the ReadFile subtool."""
        # Create a test file
        test_file_path = os.path.join(self.temp_dir.name, "test_file.txt")
        test_content = "Test content\nLine 2\nLine 3"
        with open(test_file_path, "w") as f:
            f.write(test_content)

        async with self.create_client_session() as session:
            # Get a valid chat_id
            chat_id = await self.get_chat_id(session)

            # Call the ReadFile tool with the chat_id
            result_text = await self.call_tool_assert_success(
                session,
                "codemcp",
                {"subtool": "ReadFile", "path": test_file_path, "chat_id": chat_id},
            )

            # Verify the result includes our file content (ignoring line numbers)
            for line in test_content.splitlines():
                self.assertIn(line, result_text)

    async def test_read_file_with_offset_limit(self):
        """Test the ReadFile subtool with offset and limit."""
        # Create a test file with multiple lines
        test_file_path = os.path.join(self.temp_dir.name, "multi_line.txt")
        lines = ["Line 1", "Line 2", "Line 3", "Line 4", "Line 5"]
        with open(test_file_path, "w") as f:
            f.write("\n".join(lines))

        async with self.create_client_session() as session:
            # Get a valid chat_id
            chat_id = await self.get_chat_id(session)

            # Call the ReadFile tool with offset and limit and the chat_id
            result_text = await self.call_tool_assert_success(
                session,
                "codemcp",
                {
                    "subtool": "ReadFile",
                    "path": test_file_path,
                    "offset": 2,  # Start from line 2
                    "limit": 2,  # Read 2 lines
                    "chat_id": chat_id,
                },
            )

            # Verify we got exactly lines 2-3
            self.assertIn("Line 2", result_text)
            self.assertIn("Line 3", result_text)
            self.assertNotIn("Line 1", result_text)
            self.assertNotIn("Line 4", result_text)


if __name__ == "__main__":
    unittest.main()
