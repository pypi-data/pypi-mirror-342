"""
Tests for session functionality.
"""

import os
import sys
import unittest
from unittest.mock import MagicMock

# Add parent directory to path to import proapi
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from proapi.session import Session, SessionManager, MemorySessionBackend, FileSessionBackend, session_middleware
from proapi.server import Request, Response


class TestSession(unittest.TestCase):
    """Test the Session class."""

    def test_session_init(self):
        """Test session initialization."""
        session = Session("test-id", {"key": "value"})
        self.assertEqual(session.session_id, "test-id")
        self.assertEqual(session.data, {"key": "value"})
        self.assertFalse(session.modified)
        self.assertFalse(session.new)

    def test_session_getitem(self):
        """Test session __getitem__."""
        session = Session("test-id", {"key": "value"})
        self.assertEqual(session["key"], "value")
        self.assertIsNone(session["nonexistent"])

    def test_session_setitem(self):
        """Test session __setitem__."""
        session = Session("test-id")
        session["key"] = "value"
        self.assertEqual(session.data, {"key": "value"})
        self.assertTrue(session.modified)

    def test_session_delitem(self):
        """Test session __delitem__."""
        session = Session("test-id", {"key": "value"})
        del session["key"]
        self.assertEqual(session.data, {})
        self.assertTrue(session.modified)

    def test_session_contains(self):
        """Test session __contains__."""
        session = Session("test-id", {"key": "value"})
        self.assertIn("key", session)
        self.assertNotIn("nonexistent", session)

    def test_session_get(self):
        """Test session get."""
        session = Session("test-id", {"key": "value"})
        self.assertEqual(session.get("key"), "value")
        self.assertEqual(session.get("nonexistent"), None)
        self.assertEqual(session.get("nonexistent", "default"), "default")

    def test_session_pop(self):
        """Test session pop."""
        session = Session("test-id", {"key": "value"})
        self.assertEqual(session.pop("key"), "value")
        self.assertEqual(session.data, {})
        self.assertTrue(session.modified)
        self.assertEqual(session.pop("nonexistent", "default"), "default")

    def test_session_clear(self):
        """Test session clear."""
        session = Session("test-id", {"key1": "value1", "key2": "value2"})
        session.clear()
        self.assertEqual(session.data, {})
        self.assertTrue(session.modified)

    def test_session_update(self):
        """Test session update."""
        session = Session("test-id", {"key1": "value1"})
        session.update({"key2": "value2", "key3": "value3"})
        self.assertEqual(session.data, {"key1": "value1", "key2": "value2", "key3": "value3"})
        self.assertTrue(session.modified)


class TestMemorySessionBackend(unittest.TestCase):
    """Test the MemorySessionBackend class."""

    def test_memory_backend_init(self):
        """Test memory backend initialization."""
        backend = MemorySessionBackend()
        self.assertEqual(backend.sessions, {})
        self.assertEqual(backend.expiry_times, {})
        self.assertEqual(backend.max_age, 3600)

    def test_memory_backend_save_get(self):
        """Test memory backend save and get."""
        backend = MemorySessionBackend()
        backend.save("test-id", {"key": "value"})
        self.assertEqual(backend.get("test-id"), {"key": "value"})

    def test_memory_backend_delete(self):
        """Test memory backend delete."""
        backend = MemorySessionBackend()
        backend.save("test-id", {"key": "value"})
        backend.delete("test-id")
        self.assertIsNone(backend.get("test-id"))


class TestFileSessionBackend(unittest.TestCase):
    """Test the FileSessionBackend class."""

    def setUp(self):
        """Set up the test."""
        self.test_dir = "test_sessions"
        self.backend = FileSessionBackend(directory=self.test_dir)

    def tearDown(self):
        """Clean up after the test."""
        import shutil
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_file_backend_init(self):
        """Test file backend initialization."""
        self.assertEqual(self.backend.directory, self.test_dir)
        self.assertEqual(self.backend.max_age, 3600)
        self.assertTrue(os.path.exists(self.test_dir))

    def test_file_backend_save_get(self):
        """Test file backend save and get."""
        self.backend.save("test-id", {"key": "value"})
        self.assertEqual(self.backend.get("test-id"), {"key": "value"})

    def test_file_backend_delete(self):
        """Test file backend delete."""
        self.backend.save("test-id", {"key": "value"})
        self.backend.delete("test-id")
        self.assertIsNone(self.backend.get("test-id"))


class TestSessionManager(unittest.TestCase):
    """Test the SessionManager class."""

    def setUp(self):
        """Set up the test."""
        self.secret_key = "test-secret-key"
        self.manager = SessionManager(secret_key=self.secret_key)

    def test_session_manager_init(self):
        """Test session manager initialization."""
        self.assertEqual(self.manager.secret_key, self.secret_key)
        self.assertEqual(self.manager.cookie_name, "session")
        self.assertEqual(self.manager.max_age, 3600)
        self.assertEqual(self.manager.path, "/")
        self.assertIsNone(self.manager.domain)
        self.assertFalse(self.manager.secure)
        self.assertTrue(self.manager.http_only)
        self.assertEqual(self.manager.same_site, "Lax")
        self.assertEqual(self.manager.backend.__class__.__name__, "MemorySessionBackend")

    def test_session_manager_generate_validate_session_id(self):
        """Test session ID generation and validation."""
        session_id = self.manager._generate_session_id()
        self.assertTrue(self.manager._validate_session_id(session_id))
        self.assertFalse(self.manager._validate_session_id("invalid-id"))
        self.assertFalse(self.manager._validate_session_id("invalid-id.invalid-signature"))

    def test_session_manager_get_session(self):
        """Test get_session."""
        # Create a mock request with no session cookie
        request = MagicMock()
        request.headers = {}
        
        # Get a new session
        session = self.manager.get_session(request)
        self.assertTrue(session.new)
        
        # Create a mock request with a valid session cookie
        request = MagicMock()
        session_id = self.manager._generate_session_id()
        request.headers = {"Cookie": f"session={session_id}"}
        
        # Save session data
        self.manager.backend.save(session_id, {"key": "value"})
        
        # Get the session
        session = self.manager.get_session(request)
        self.assertFalse(session.new)
        self.assertEqual(session.session_id, session_id)
        self.assertEqual(session.data, {"key": "value"})

    def test_session_manager_save_session(self):
        """Test save_session."""
        # Create a session
        session = Session("test-id", {"key": "value"}, new=True)
        
        # Create a response
        response = Response(body="Test")
        
        # Save the session
        self.manager.save_session(session, response)
        
        # Check that the session was saved
        self.assertIn("Set-Cookie", response.headers)
        self.assertTrue(response.headers["Set-Cookie"].startswith("session="))

    def test_session_manager_delete_session(self):
        """Test delete_session."""
        # Create a session
        session = Session("test-id", {"key": "value"})
        
        # Save the session
        self.manager.backend.save(session.session_id, session.data)
        
        # Create a response
        response = Response(body="Test")
        
        # Delete the session
        self.manager.delete_session(session, response)
        
        # Check that the session was deleted
        self.assertIsNone(self.manager.backend.get(session.session_id))
        self.assertIn("Set-Cookie", response.headers)
        self.assertTrue("Max-Age=0" in response.headers["Set-Cookie"])


class TestSessionMiddleware(unittest.TestCase):
    """Test the session middleware."""

    def setUp(self):
        """Set up the test."""
        self.secret_key = "test-secret-key"
        self.manager = SessionManager(secret_key=self.secret_key)
        self.middleware = session_middleware(self.manager)

    def test_session_middleware(self):
        """Test session middleware."""
        # Create a mock request
        request = MagicMock()
        request.headers = {}
        
        # Apply middleware
        processed_request = self.middleware(request)
        
        # Check that session was added to request
        self.assertTrue(hasattr(processed_request, "session"))
        self.assertTrue(hasattr(processed_request, "save_session"))
        
        # Check that session is a Session object
        self.assertEqual(processed_request.session.__class__.__name__, "Session")
        
        # Check that save_session is a callable
        self.assertTrue(callable(processed_request.save_session))


if __name__ == "__main__":
    unittest.main()
