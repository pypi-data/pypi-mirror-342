
import unittest
import logging
from io import StringIO
import json
import math  # Example module to wrap
import os

# Assuming ModWrapper class is in the same file or adjust import as necessary
from modwrap import ModWrapper  # Replace your_module


class TestModWrapper(unittest.TestCase):
    """Tests for ModWrapper class."""

    def setUp(self):
        """Set up test environment."""
        self.module_to_wrap = math
        self.logger_stream = StringIO()
        self.log_handler = logging.StreamHandler(self.logger_stream)
        self.log_formatter = logging.Formatter(
            '%(levelname)s:%(name)s:%(message)s')
        self.log_handler.setFormatter(self.log_formatter)
        self.test_logger = logging.getLogger('test_logger')
        self.test_logger.addHandler(self.log_handler)
        # Capture all levels for testing
        self.test_logger.setLevel(logging.DEBUG)
        self.captured_logs = self.logger_stream  # Use the stream directly

    def tearDown(self):
        """Tear down test environment."""
        self.test_logger.removeHandler(self.log_handler)
        handlers = list(self.test_logger.handlers)[:]
        for hdlr in handlers:
            self.test_logger.removeHandler(hdlr)
            hdlr.close()
        self.logger_stream.close()

    def test_module_wrapping_and_logging(self):
        """Test basic module wrapping and function call logging."""
        wrapped_module = ModWrapper(
            self.module_to_wrap, logger=self.test_logger, log_level=logging.INFO)
        wrapped_module.sqrt(4)
        log_output = self.captured_logs.getvalue()

        self.assertIn("INFO:test_logger:\nModule Call: math.sqrt", log_output)
        self.assertIn("Positional Arg:\n---\n4", log_output)
        self.assertIn("Return Value:\n---\n2.0", log_output)

    def test_function_argument_logging(self):
        """Test logging of function arguments, including lists and dicts."""
        wrapped_module = ModWrapper(
            self.module_to_wrap, logger=self.test_logger, log_level=logging.DEBUG)
        test_list = [1, 2, 'three']
        test_dict = {'a': 1, 'b': 'two'}
        wrapped_module.gcd(test_list[0], b=test_dict)
        log_output = self.captured_logs.getvalue()

        self.assertIn("DEBUG:test_logger:\nModule Call: math.gcd", log_output)
        self.assertIn("Positional Arg:\n---\n1", log_output)
        self.assertIn(
            "Keyword Arg: b =\n---  {'a': 1, 'b': 'two'}", log_output)

    def test_json_like_string_argument_logging(self):
        """Test logging of arguments that are JSON-like strings."""
        wrapped_module = ModWrapper(
            self.module_to_wrap, logger=self.test_logger, log_level=logging.DEBUG)
        json_str_arg = '{"key": "value"}'
        list_str_arg = '[1, 2, 3]'

        wrapped_module.sin(json_str_arg)
        log_output = self.captured_logs.getvalue()
        self.assertIn(
            "Positional Arg (JSON String):\n---\n{\n    \"key\": \"value\"\n}", log_output)
        self.captured_logs.truncate(0)  # clear for next assert
        self.captured_logs.seek(0)

        wrapped_module.cos(list_str_arg)
        log_output = self.captured_logs.getvalue()
        self.assertIn(
            "Positional Arg (JSON String):\n---\n[\n    1,\n    2,\n    3\n]", log_output)

    def test_exception_logging(self):
        """Test logging of exceptions during function calls."""
        wrapped_module = ModWrapper(
            self.module_to_wrap, logger=self.test_logger, log_level=logging.INFO)
        with self.assertRaises(TypeError):
            wrapped_module.sqrt("string")  # sqrt expects number, not string
        log_output = self.captured_logs.getvalue()

        self.assertIn("ERROR:test_logger:Error in 'math.sqrt':", log_output)
        self.assertIn("TypeError: must be real number, not str", log_output)

    def test_filter_func_usage(self):
        """Test using filter_func to selectively wrap functions."""
        def filter_out_sqrt(name): return name != 'sqrt'
        wrapped_module = ModWrapper(self.module_to_wrap, logger=self.test_logger,
                                    log_level=logging.INFO, filter_func=filter_out_sqrt)

        wrapped_module.sin(0)  # Should be logged
        wrapped_module.sqrt(4)  # Should NOT be logged
        log_output = self.captured_logs.getvalue()

        self.assertIn("Module Call: math.sin", log_output)
        self.assertNotIn("Module Call: math.sqrt", log_output)

    def test_dir_and_repr_methods(self):
        """Test __dir__ and __repr__ methods for introspection."""
        wrapped_module = ModWrapper(self.module_to_wrap)
        self.assertIn('sqrt', dir(wrapped_module))
        self.assertIn('sin', dir(wrapped_module))
        self.assertTrue(repr(wrapped_module).startswith("<ModWrapper(math)>"))

    def test_log_level_debug_verbosity(self):
        """Test that DEBUG level logs more details when appropriate."""
        wrapped_module = ModWrapper(
            self.module_to_wrap, logger=self.test_logger, log_level=logging.DEBUG)
        # result is small, should log return in debug
        result = wrapped_module.pow(2, 3)
        log_output = self.captured_logs.getvalue()
        self.assertIn("Return Value:\n---\n8", log_output)
        self.captured_logs.truncate(0)
        self.captured_logs.seek(0)

        long_string_result = "A" * 200  # long result, should NOT log return in debug
        # Mock setting an attribute to get a long string back
        wrapped_module.os_name = os.name
        # Call the attribute which will call __getattribute__ and then log.
        wrapped_module.os_name
        log_output = self.captured_logs.getvalue()
        self.assertNotIn("Return Value:", log_output,
                         "Long return should not be logged in DEBUG")

    def test_no_args_kwargs_logging(self):
        """Test logging when function is called with no arguments."""
        wrapped_module = ModWrapper(
            self.module_to_wrap, logger=self.test_logger, log_level=logging.INFO)
        wrapped_module.tau  # math.tau is a constant, accessing it calls __getattr__ but no wrapping
        wrapped_module.degrees(0)  # function call with no kwargs or args

        log_output = self.captured_logs.getvalue()
        self.assertIn(
            "INFO:test_logger:\nModule Call: math.degrees", log_output)
        # Arguments block should not be present
        self.assertNotIn("Arguments:", log_output)


if __name__ == '__main__':
    unittest.main()
