"""
Logging utility module for Treebeard.

This module provides logging context management functionality,
allowing creation and management of trace contexts.
"""
import asyncio
import inspect
import os
import re
import threading
import traceback
import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any, Type

from .internal_utils.fallback_logger import fallback_logger, sdk_logger
from .context import LoggingContext
from .core import Treebeard
from .constants import COMPACT_TRACEBACK_KEY, TRACE_COMPLETE_ERROR_MARKER, TRACE_COMPLETE_SUCCESS_MARKER, TRACE_ID_KEY, MESSAGE_KEY, LEVEL_KEY, FILE_KEY, LINE_KEY, TRACE_START_MARKER, TRACEBACK_KEY, TRACE_NAME_KEY

import logging

dev_logger = logging.getLogger("dev")

masked_terms = {
    'password', 'pass', 'pw', 'secret', 'api_key', 'access_token', 'refresh_token',
    'token', 'key', 'auth', 'credentials', 'credential', 'private_key', 'public_key',
    'ssh_key', 'certificate', 'cert', 'signature', 'sign', 'hash', 'salt', 'nonce',
    'session_id', 'session', 'cookie', 'jwt', 'bearer', 'oauth', 'oauth2', 'openid',
    'client_id', 'client_secret', 'consumer_key', 'consumer_secret', 'aws_access_key',
    'aws_secret_key', 'aws_session_token', 'azure_key', 'gcp_key', 'api_secret',
    'encryption_key', 'decryption_key', 'master_key', 'root_key', 'admin_key',
    'database_password', 'db_password', 'db_pass', 'redis_password', 'redis_pass',
    'mongodb_password', 'mongodb_pass', 'postgres_password', 'postgres_pass',
    'mysql_password', 'mysql_pass', 'oracle_password', 'oracle_pass'
}

pattern = re.compile(
    r"(?P<db>[a-z\+]+)://(?P<user>[a-zA-Z0-9_-]+):(?P<pw>[a-zA-Z0-9_]+)@(?P<host>[\.a-zA-Z0-9_-]+):(?P<port>\d+)"
)


class Log:
    """Logging utility class for managing trace contexts."""

    @staticmethod
    def start(name: Optional[str] = None, data: Optional[Dict] = None, **kwargs) -> str:
        """Start a new logging context with the given name.

        If a context already exists, it will be cleared before creating
        the new one.

        Args:
            name: The name of the logging context

        Returns:
            The generated trace ID
        """
        # Clear any existing context
        try:
            Log.end()

            # Generate new trace ID
            trace_id = f"T{uuid.uuid4().hex}"

            # Set up new context
            LoggingContext.set(TRACE_ID_KEY, trace_id)

            if name:
                LoggingContext.set(TRACE_NAME_KEY, name)

            Log.info(TRACE_START_MARKER, data, **kwargs)

            return trace_id
        except Exception as e:
            sdk_logger.error(
                f"Error in Log.start : {str(e)}: {traceback.format_exc()}")
            return None

    @staticmethod
    def end() -> None:
        try:
            """End the current logging context by clearing all context data."""
            LoggingContext.clear()
        except Exception as e:
            sdk_logger.error(
                f"Error in Log.end : {str(e)}: {traceback.format_exc()}")

    @staticmethod
    def complete_success() -> None:
        """Mark the completion of a successful trace."""
        try:
            Log.info(TRACE_COMPLETE_SUCCESS_MARKER)
            Log.end()
        except Exception as e:
            sdk_logger.error(
                f"Error in Log.complete_success : {str(e)}: {traceback.format_exc()}")

    @staticmethod
    def complete_error(data: Optional[Dict] = None, **kwargs) -> None:
        """Mark the completion of an error trace."""
        try:
            Log.error(TRACE_COMPLETE_ERROR_MARKER, data, **kwargs)
            Log.end()
        except Exception as e:
            sdk_logger.error(
                f"Error in Log.complete_error : {str(e)}: {traceback.format_exc()}")

    @staticmethod
    def _prepare_log_data(message: str, data: Optional[Dict] = None, **kwargs) -> Dict[str, Any]:
        """Prepare log data by merging context, provided data and kwargs.

        Args:
            message: The log message
            data: Optional dictionary of metadata
            **kwargs: Additional metadata as keyword arguments

        Returns:
            Dict containing the complete log entry
        """
        try:
            filename = None
            line_number = None
            locals_dict = {}
            frame_info = inspect.stack()

            # don't take a frame from the SDK wrapper
            for frame_info in inspect.stack():
                frame_file = frame_info.filename
                if "treebeardhq" not in frame_file:
                    filename = frame_file
                    line_number = frame_info.lineno
                    locals_dict = Log.extract_relevant_locals(
                        frame_info.frame.f_locals)
                    break

            # Start with the context data
            log_data = LoggingContext.get_all()

            # Add the message
            log_data[MESSAGE_KEY] = message
            log_data['f_locals'] = locals_dict

            if not log_data.get(TRACE_ID_KEY):
                trace_id = Log.start()
                log_data[TRACE_ID_KEY] = trace_id

            # Merge explicit data dict if provided
            if data is not None:
                log_data.update(data)

            # Merge kwargs
            if kwargs:
                log_data.update(kwargs)

            # Create a new dictionary to avoid modifying in place
            processed_data = {}
            processed_data[FILE_KEY] = filename
            processed_data[LINE_KEY] = line_number

            for key, value in log_data.items():

                if value is None:
                    continue

                if isinstance(value, Exception):
                    if value.__traceback__ is not None:
                        processed_data[TRACEBACK_KEY] = '\n'.join(traceback.format_exception(
                            type(value), value, value.__traceback__))
                        tb = value.__traceback__
                        while tb.tb_next:  # walk to the last frame
                            tb = tb.tb_next

                        processed_data[FILE_KEY] = tb.tb_frame.f_code.co_filename
                        processed_data[LINE_KEY] = tb.tb_lineno

                    else:
                        processed_data[TRACEBACK_KEY] = str(value)

                # Handle datetime objects
                elif isinstance(value, datetime):
                    processed_data[key] = int(value.timestamp())
                # Handle dictionaries
                elif isinstance(value, dict):
                    Log.recurse_and_collect_dict(value, processed_data, key)
                # Handle objects
                elif isinstance(value, object) and not isinstance(value, (int, float, str, bool, type(None))):
                    for attr_name in dir(value):
                        if not attr_name.startswith("_"):
                            try:
                                attr_value = getattr(value, attr_name)
                                if isinstance(attr_value, (int, float, str, bool, type(None))):
                                    if attr_value is None:
                                        processed_data[f"{key}_{attr_name}"] = "None"
                                    # Mask password-related keys
                                    elif any(pw_key in attr_name.lower() for pw_key in masked_terms):
                                        processed_data[f"{key}_{attr_name}"] = '*****'
                                    else:
                                        processed_data[f"{key}_{attr_name}"] = attr_value
                            except:
                                continue
                # Keep all primitive types as is
                else:
                    # Mask password-related keys
                    if any(pw_key in key.lower() for pw_key in masked_terms):
                        processed_data[key] = '*****'
                    else:
                        processed_data[key] = value

            return processed_data
        except Exception as e:

            sdk_logger.error(
                f"Error in Log._prepare_log_data : {str(e)}: {traceback.format_exc()}")
            return {}

    @staticmethod
    def trace(message: str, data: Optional[Dict] = None, **kwargs) -> None:
        """Log a trace message.

        Args:
            message: The log message
            data: Optional dictionary of metadata
            **kwargs: Additional metadata as keyword arguments
        """
        try:
            log_data = Log._prepare_log_data(message, data, **kwargs)
            log_data[LEVEL_KEY] = 'trace'
            Treebeard().add(log_data)
        except Exception as e:
            sdk_logger.error(
                f"Error in Log.trace : {str(e)}: {traceback.format_exc()}")

    @staticmethod
    def debug(message: str, data: Optional[Dict] = None, **kwargs) -> None:
        """Log a debug message.

        Args:
            message: The log message
            data: Optional dictionary of metadata
            **kwargs: Additional metadata as keyword arguments
        """
        try:
            log_data = Log._prepare_log_data(message, data, **kwargs)
            log_data[LEVEL_KEY] = 'debug'
            Treebeard().add(log_data)
        except Exception as e:
            sdk_logger.error(
                f"Error in Log.debug : {str(e)}: {traceback.format_exc()}")

    @staticmethod
    def info(message: str, data: Optional[Dict] = None, **kwargs) -> None:
        """Log an info message.

        Args:
            message: The log message
            data: Optional dictionary of metadata
            **kwargs: Additional metadata as keyword arguments
        """
        try:
            log_data = Log._prepare_log_data(message, data, **kwargs)
            log_data[LEVEL_KEY] = 'info'
            Treebeard().add(log_data)
        except Exception as e:
            sdk_logger.error(
                f"Error in Log.info : {str(e)}: {traceback.format_exc()}")

    @staticmethod
    def warning(message: str, data: Optional[Dict] = None, **kwargs) -> None:
        """Log a warning message.

        Args:
            message: The log message
            data: Optional dictionary of metadata
            **kwargs: Additional metadata as keyword arguments
        """
        try:
            log_data = Log._prepare_log_data(message, data, **kwargs)
            log_data[LEVEL_KEY] = 'warning'
            Treebeard().add(log_data)
        except Exception as e:
            sdk_logger.error(
                f"Error in Log.warning : {str(e)}: {traceback.format_exc()}")

    @staticmethod
    def warn(message: str, data: Optional[Dict] = None, **kwargs) -> None:
        """alias for warning

        Args:
            message: The log message
            data: Optional dictionary of metadata
            **kwargs: Additional metadata as keyword arguments
        """
        try:
            Log.warning(message, data, **kwargs)
        except Exception as e:
            sdk_logger.error(
                f"Error in Log.warn : {str(e)}: {traceback.format_exc()}")

    @staticmethod
    def error(message: str, data: Optional[Dict] = None, **kwargs) -> None:
        """Log an error message.

        Args:
            message: The log message
            data: Optional dictionary of metadata
            **kwargs: Additional metadata as keyword arguments
        """
        try:
            log_data = Log._prepare_log_data(message, data, **kwargs)
            log_data[LEVEL_KEY] = 'error'
            Treebeard().add(log_data)
        except Exception as e:
            sdk_logger.error(
                f"Error in Log.error : {str(e)}: {traceback.format_exc()}")

    @staticmethod
    def critical(message: str, data: Optional[Dict] = None, **kwargs) -> None:
        """Log a critical message.

        Args:
            message: The log message
            data: Optional dictionary of metadata
            **kwargs: Additional metadata as keyword arguments
        """
        try:
            log_data = Log._prepare_log_data(message, data, **kwargs)
            log_data[LEVEL_KEY] = 'critical'
            Treebeard().add(log_data)
        except Exception as e:
            sdk_logger.error(
                f"Error in Log.critical : {str(e)}: {traceback.format_exc()}")

    @classmethod
    def _handle_exception(cls, exc_type: Type[BaseException], exc_value: BaseException, exc_traceback: Any) -> None:
        """Handle unhandled exceptions in the main thread.

        Args:
            exc_type: The type of the exception
            exc_value: The exception instance
            exc_traceback: The traceback object
        """
        try:

            # Log the exception
            Log.error(
                "Unhandled exception in main thread",
                error=exc_value,
            )

            # Clear the context after logging
            LoggingContext.clear()

            # Call the original exception handler
            if Treebeard._original_excepthook is not None:
                Treebeard._original_excepthook(
                    exc_type, exc_value, exc_traceback)

        except Exception as e:
            Log.error("Handled exception in SDK", error=e)

    @classmethod
    def _handle_threading_exception(cls, args: threading.ExceptHookArgs) -> None:
        """Handle unhandled exceptions in threads.

        Args:
            args: The exception hook arguments containing exception info
        """
        try:

            # Log the exception
            Log.error(
                "Unhandled exception in thread",
                thread_name=args.thread.name,
                thread_id=args.thread.ident,
                error=args.exc_value,

            )

            # Clear the context after logging
            LoggingContext.clear()

        # Call the original exception handler
            if Treebeard._original_threading_excepthook is not None:
                Treebeard._original_threading_excepthook(args)
        except Exception:
            Log.error("Handled exception in SDK")

    @classmethod
    def _handle_async_exception(cls, loop: asyncio.AbstractEventLoop, context: dict) -> None:
        """Handle unhandled exceptions in async contexts.

        Args:
            loop: The event loop where the exception occurred
            context: Dictionary containing exception information
        """
        try:
            exception = context.get('exception')

            if exception:
                # Log the exception
                Log.error(
                    "Unhandled exception in async context",
                    error=exception,

                    future=context.get('future'),
                    task=context.get('task'),
                    message=context.get('message'),

                )
            else:
                # Log the error message if no exception is present
                Log.error(
                    "Error in async context",
                    message=context.get('message'),
                    future=context.get('future'),
                    task=context.get('task'),
                )

            # Clear the context after logging
            LoggingContext.clear()

        # Call the original exception handler
            if Treebeard._original_loop_exception_handler is not None:
                Treebeard._original_loop_exception_handler(loop, context)
        except Exception:
            Log.error("Handled exception in SDK")

    @staticmethod
    def recurse_and_collect_dict(data: dict, collector: Dict[str, Any], prefix: str = "") -> Dict[str, Any]:
        """
        Recursively flattens a nested dictionary into a flat dictionary with keys
        representing the path to each value using underscores. Lists are stored as their count.

        Args:
            data: The dictionary to traverse.
            collector: The flat dictionary to populate.
            prefix: The current key prefix for nesting.

        Returns:
            The updated collector dictionary.
        """
        for key, value in data.items():
            full_key = f"{prefix}_{key}" if prefix else key

            if isinstance(value, dict):
                Log.recurse_and_collect_dict(value, collector, full_key)
            elif isinstance(value, list):
                collector[f"{full_key}_count"] = len(value)
            elif isinstance(value, (str, int, float, bool, type(None))):
                if value is None:
                    collector[full_key] = "None"
                elif any(pw_key in full_key.lower() for pw_key in masked_terms):
                    collector[full_key] = '*****'
                elif "url" in full_key.lower():
                    collector[full_key] = pattern.sub(mask_pw, value)
            # Optionally handle other types here (e.g. sets, tuples)

        return collector

    def extract_relevant_locals(locals_dict):
        result = {}
        for key, value in locals_dict.items():
            if key.startswith("__"):
                continue  # skip dunder
            if isinstance(value, (type(inspect), type(os))):  # skip modules
                continue
            if callable(value):
                continue  # skip functions and classes
            try:
                repr(value)
            except Exception:
                continue  # skip unrepr-able objects
            result[key] = value
        return result


Treebeard.register(Log._handle_exception,
                   Log._handle_threading_exception, Log._handle_async_exception)


def mask_pw(match):
    return f"{match.group('db')}://{match.group('user')}:*****@{match.group('host')}:{match.group('port')}"
