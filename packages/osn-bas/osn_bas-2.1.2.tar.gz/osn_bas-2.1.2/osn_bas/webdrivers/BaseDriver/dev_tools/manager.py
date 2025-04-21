import sys
import trio
import logging
import traceback
from types import TracebackType
from collections.abc import Awaitable
from selenium.webdriver.common.bidi.cdp import CdpSession, open_cdp
from selenium.webdriver.remote.bidi_connection import BidiConnection
import osn_bas.webdrivers.BaseDriver.dev_tools.domains.fetch as fetch
from contextlib import (
	AbstractAsyncContextManager,
	asynccontextmanager
)
from osn_bas.webdrivers.BaseDriver.protocols import (
	TrioWebDriverWrapperProtocol
)
from osn_bas.webdrivers.BaseDriver.dev_tools.errors import (
	CantEnterDevToolsContextError
)
from typing import (
	Any,
	AsyncGenerator,
	Callable,
	Coroutine,
	Optional,
	TYPE_CHECKING,
	cast
)
from osn_bas.webdrivers.BaseDriver.dev_tools.domains import (
	CallbacksSettings,
	Fetch,
	_special_keys
)
from osn_bas.webdrivers.BaseDriver.dev_tools._utils import (
	log_on_error,
	validate_handler_settings,
	warn_if_active
)


if TYPE_CHECKING:
	from osn_bas.webdrivers.BaseDriver.webdriver import BrowserWebDriver


class DevTools:
	"""
	Base class for handling DevTools functionalities in Selenium WebDriver.

	Provides an interface to interact with Chrome DevTools Protocol (CDP)
	for advanced browser control and monitoring. This class supports event handling
	and allows for dynamic modifications of browser behavior, such as network request interception.

	Attributes:
		_webdriver (BrowserWebDriver): The parent WebDriver instance associated with this DevTools instance.
		_bidi_connection (Optional[AbstractAsyncContextManager[BidiConnection, Any]]): Asynchronous context manager for the BiDi connection.
		_bidi_connection_object (Optional[BidiConnection]): The BiDi connection object when active.
		_bidi_devtools (Optional[Any]): The DevTools API object from the BiDi connection.
		_is_active (bool): Flag indicating if the DevTools event handler is currently active.
		_nursery (Optional[AbstractAsyncContextManager[trio.Nursery, Optional[bool]]]): Asynchronous context manager for the Trio nursery.
		_nursery_object (Optional[trio.Nursery]): The Trio nursery object when active, managing concurrent tasks.
		_exit_event (Optional[trio.Event]): Trio Event to signal exiting of DevTools event handling.
		_callbacks_settings (CallbacksSettings): Settings for configuring DevTools event callbacks.
	"""
	
	def __init__(self, parent_webdriver: "BrowserWebDriver"):
		"""
		Initializes the DevTools instance.

		Args:
			parent_webdriver (Any): The parent WebDriver instance that this DevTools instance will be associated with.
		"""
		
		self._webdriver = parent_webdriver
		self._bidi_connection: Optional[AbstractAsyncContextManager[BidiConnection, Any]] = None
		self._bidi_connection_object: Optional[BidiConnection] = None
		self._bidi_devtools: Optional[Any] = None
		self._is_active = False
		self._nursery: Optional[AbstractAsyncContextManager[trio.Nursery, Optional[bool]]] = None
		self._nursery_object: Optional[trio.Nursery] = None
		self._exit_event: Optional[trio.Event] = None
		
		self._callbacks_settings = CallbacksSettings(
				fetch=Fetch(
						use=False,
						enable_func_path="fetch.enable",
						disable_func_path="fetch.disable",
						request_paused=None
				)
		)
	
	async def _start_listeners(self, cdp_session: CdpSession):
		"""
		Starts all configured DevTools event listeners.

		This method initiates listeners for all event types configured in `_callbacks_settings` that are set to 'use'.
		It enables target discovery and starts a nursery task to process new targets, then iterates through each event type and name to start individual listeners.

		Args:
			cdp_session (CdpSession): The CDP session object to use for starting listeners.

		Raises:
			WrongHandlerSettingsTypeError: If the handler_settings is not a dictionary.
			WrongHandlerSettingsError: If the handler_settings does not contain exactly one of the required keys.
		"""
		
		try:
			await cdp_session.execute(self._get_devtools_object("target.set_discover_targets")(True))
			self._nursery_object.start_soon(self._process_new_targets, cdp_session)
		
			for domain_name, domain_config in self._callbacks_settings.items():
				if domain_config["use"]:
					if domain_config.get("enable_func_path", None) is not None:
						await cdp_session.execute(self._get_devtools_object(domain_config["enable_func_path"])())
		
					for event_name, event_config in domain_config.items():
						if event_name not in _special_keys and event_config is not None:
							handler_type = validate_handler_settings(event_config)
		
							if handler_type == "class":
								self._nursery_object.start_soon(self._run_event_listener, cdp_session, domain_name, event_name)
		
			await trio.sleep(0.0)
		except (trio.Cancelled, trio.EndOfChannel):
			pass
	
	async def _process_new_targets(self, cdp_session: CdpSession):
		"""
		Processes new browser targets as they are created.

		Listens for 'target.TargetCreated' events, which are emitted when new targets (like tabs or windows) are created in the browser.
		For each new target, it starts a new nursery task to handle events for that target.

		Args:
			cdp_session (CdpSession): The CDP session object to listen for target creation events.
		"""
		
		receiver_channel: trio.MemoryReceiveChannel = cdp_session.listen(self._get_devtools_object("target.TargetCreated"))
		
		while True:
			try:
				event = await receiver_channel.receive()
		
				if event.target_info.type_ == "page":
					self._nursery_object.start_soon(self._handle_new_target, event.target_info.target_id)
			except (trio.Cancelled, trio.EndOfChannel):
				break
			except (Exception,):
				exception_type, exception_value, exception_traceback = sys.exc_info()
				error = "".join(
						traceback.format_exception(exception_type, exception_value, exception_traceback)
				)
		
				logging.log(logging.ERROR, error)
	
	async def _handle_new_target(self, target_id: str):
		"""
		Handles events for a newly created browser target.

		Manages a new CDP session for a given target ID. It uses `_new_session_manager` to open a session for the target,
		starts event listeners for this new session, and waits for a cancellation event before closing the session.

		Args:
			target_id (str): The ID of the new browser target to handle.
		"""
		
		try:
			async with self._new_session_manager(target_id) as new_session:
				await self._start_listeners(new_session)
				await self._exit_event.wait()
		except (trio.Cancelled, trio.EndOfChannel):
			pass
	
	def _get_devtools_object(self, path: str) -> Any:
		"""
		Navigates and retrieves a specific object within the DevTools API structure.

		Using a dot-separated path, this method traverses the nested DevTools API objects to retrieve a target object.
		For example, a path like "fetch.enable" would access `self._bidi_devtools.fetch.enable`.

		Args:
			path (str): A dot-separated string representing the path to the desired DevTools API object.

		Returns:
			Any: The DevTools API object located at the specified path.
		"""
		
		object_ = self._bidi_devtools
		
		for path_part in path.split("."):
			object_ = getattr(object_, path_part)
		
		return object_
	
	def _get_handler_to_use(self, event_type: str, event_name: str) -> Optional[
		Callable[
			[CdpSession, fetch.RequestPausedHandlerSettings, Any],
			Coroutine[None, None, Any]
		]
	]:
		"""
		Retrieves the appropriate handler function for a given DevTools event.

		Based on the event type and name, this method returns the corresponding handler function
		defined within the DevTools class. It's used to dynamically dispatch events to their respective handlers.

		Args:
			event_type (str): The type of DevTools event (e.g., "fetch").
			event_name (str): The name of the specific event handler within the event type (e.g., "request_paused").

		Returns:
			Optional[Callable[[CdpSession, fetch.RequestPausedHandlerSettings, Any], Coroutine[None, None, Any]]]: The handler function if found, otherwise None.
		"""
		
		return getattr(self, f"_handle_{event_type}_{event_name}", None)
	
	async def _run_event_listener(self, cdp_session: CdpSession, event_type: str, event_name: str):
		"""
		Runs an asynchronous event listener loop for a specific DevTools event.

		Sets up a listener on the provided CDP session for the specified event type and name.
		It retrieves the associated handler settings and the handler function from internal state.
		It then continuously receives events from the CDP session's channel and passes them
		to the handler function for processing. The loop continues until cancelled or
		the channel is closed. Exceptions during event processing are caught and logged.

		Args:
			cdp_session (CdpSession): The Chrome DevTools Protocol session object to listen to events from.
			event_type (str): The domain of the DevTools event (e.g., "fetch", "log", "network").
			event_name (str): The specific name of the event within the domain (e.g., "requestPaused", "entryAdded").
		"""
		
		handler_settings = self._callbacks_settings[event_type][event_name]
		handler = self._get_handler_to_use(event_type, event_name)
		
		class_to_use = self._get_devtools_object(handler_settings["class_to_use_path"])
		receiver_channel: trio.MemoryReceiveChannel = cdp_session.listen(class_to_use, buffer_size=handler_settings["listen_buffer_size"])
		
		while True:
			try:
				event = await receiver_channel.receive()
		
				if handler:
					self._nursery_object.start_soon(handler, cdp_session, handler_settings, event)
			except (trio.Cancelled, trio.EndOfChannel):
				break
			except (Exception,):
				exception_type, exception_value, exception_traceback = sys.exc_info()
				error = "".join(
						traceback.format_exception(exception_type, exception_value, exception_traceback)
				)
		
				logging.log(logging.ERROR, error)
	
	@property
	def _websocket_url(self) -> Optional[str]:
		"""
		Retrieves the WebSocket URL for DevTools from the WebDriver.

		This method attempts to get the WebSocket URL from the WebDriver capabilities or by directly querying the CDP details.
		The WebSocket URL is necessary to establish a connection to the browser's DevTools.

		Returns:
			Optional[str]: The WebSocket URL for DevTools, or None if it cannot be retrieved.
		"""
		
		driver = self._webdriver.driver
		
		if driver is None:
			return None
		
		if driver.caps.get("se:cdp"):
			return driver.caps.get("se:cdp")
		
		return driver._get_cdp_details()[1]
	
	@asynccontextmanager
	async def _new_session_manager(self, target_id: str) -> AsyncGenerator[CdpSession, None]:
		"""
		Manages a new CDP session for a specific target, using async context management.

		This context manager opens a new CDP session for a given target ID and ensures that the session is properly closed after use.
		It's used to handle the lifecycle of CDP sessions for different browser targets.

		Args:
			target_id (str): The ID of the browser target for which to open a new CDP session.

		Returns:
			AsyncGenerator[CdpSession, None]: An asynchronous generator that yields a CdpSession object, allowing for operations within the session context.
		"""
		
		async with open_cdp(self._websocket_url) as new_connection:
			async with new_connection.open_session(target_id) as new_session:
				yield new_session
	
	async def __aenter__(self) -> TrioWebDriverWrapperProtocol:
		"""
		Asynchronously enters the DevTools event handling context.

		This method is called when entering an `async with` block with a DevTools instance.
		It initializes the BiDi connection, starts a Trio nursery to manage event listeners,
		and then starts listening for DevTools events.

		Returns:
			TrioWebDriverWrapperProtocol: Returns a wrapped WebDriver object that can be used to interact with the browser
				 while DevTools event handling is active.

		Raises:
			CantEnterDevToolsContextError: If the WebDriver driver is not initialized, indicating that a browser session has not been started yet.

		Usage
		______
		async with driver.dev_tools as driver_wrapper:
			# DevTools event handling is active within this block
			await driver_wrapper.set_request_paused_handler(...)
			await driver.search_url("example.com")
		# DevTools event handling is deactivated after exiting the block
		"""
		
		if self._webdriver.driver is None:
			raise CantEnterDevToolsContextError("Driver is not initialized")
		
		self._bidi_connection: AbstractAsyncContextManager[BidiConnection, Any] = self._webdriver.driver.bidi_connection()
		self._bidi_connection_object = await self._bidi_connection.__aenter__()
		self._bidi_devtools = self._bidi_connection_object.devtools
		
		self._nursery = trio.open_nursery()
		self._nursery_object = await self._nursery.__aenter__()
		
		await self._start_listeners(self._bidi_connection_object.session)
		
		self._is_active = True
		self._exit_event = trio.Event()
		
		return cast(TrioWebDriverWrapperProtocol, self._webdriver.to_wrapper())
	
	async def __aexit__(
			self,
			exc_type: Optional[type],
			exc_val: Optional[BaseException],
			exc_tb: Optional[TracebackType]
	):
		"""
		Asynchronously exits the DevTools event handling context.

		This method is called when exiting an `async with` block with a DevTools instance.
		It ensures that all event listeners are cancelled, the Trio nursery is closed,
		and the BiDi connection is properly shut down.

		Args:
			exc_type (Optional[type]): The exception type, if any, that caused the context to be exited.
			exc_val (Optional[BaseException]): The exception value, if any.
			exc_tb (Optional[traceback.TracebackType]): The exception traceback, if any.
		"""
		
		@log_on_error
		def _close_nursery_object():
			"""Closes the Trio nursery object and cancels all tasks within it."""
			
			if self._nursery_object is not None:
				self._nursery_object.cancel_scope.cancel()
		
		@log_on_error
		async def _close_nursery():
			"""Asynchronously exits the Trio nursery context manager."""
			
			if self._nursery is not None:
				await self._nursery.__aexit__(exc_type, exc_val, exc_tb)
		
		@log_on_error
		async def _close_bidi_connection():
			"""Asynchronously exits the BiDi connection context manager."""
			
			if self._bidi_connection is not None:
				await self._bidi_connection.__aexit__(exc_type, exc_val, exc_tb)
		
		@log_on_error
		def _activate_exit_event():
			"""Sets the exit event to signal listeners to stop."""
			
			if self._exit_event is not None:
				self._exit_event.set()
		
		if self._is_active:
			_activate_exit_event()
			self._exit_event = None
		
			_close_nursery_object()
			self._nursery_object = None
		
			await _close_nursery()
			self._nursery = None
		
			await _close_bidi_connection()
			self._bidi_connection = None
			self._bidi_connection_object = None
			self._bidi_devtools = None
		
			self._is_active = False
	
	async def _handle_fetch_request_paused(
			self,
			cdp_session: CdpSession,
			handler_settings: fetch.RequestPausedHandlerSettings,
			event: Any
	):
		"""
		Processes a 'fetch.requestPaused' event received from the DevTools Protocol.

		This internal method is executed by the event listener loop whenever a 'fetch.requestPaused'
		event occurs and is routed to this handler. It applies the configured `post_data_handler`
		and `headers_handler` from the `handler_settings` to modify the request, handling cases
		where the handlers might return awaitable results. Finally, it instructs the browser
		to continue the request with the (potentially) modified parameters using `fetch.continue_request`.
		Errors occurring during the handler execution or the continue request are caught
		and passed to the `on_error` callable defined in the handler settings.

		Args:
			cdp_session (CdpSession): The CDP session object used to communicate with the browser's DevTools.
			handler_settings (fetch.RequestPausedHandlerSettings): Configuration settings for this specific
				'requestPaused' handler, including the callable handlers and the error handler.
			event (Any): The 'fetch.requestPaused' event object containing details about the paused request.
						 Expected to be an instance of the class specified by `handler_settings["class_to_use_path"]`.
		"""
		
		post_data_result = handler_settings["post_data_handler"](handler_settings, event)
		headers_result = handler_settings["headers_handler"](handler_settings, self._get_devtools_object("fetch.HeaderEntry"), event)
		
		try:
			await cdp_session.execute(
					self._get_devtools_object("fetch.continue_request")(
							request_id=event.request_id,
							url=event.request.url,
							method=event.request.method,
							post_data=post_data_result
							if not isinstance(post_data_result, Awaitable)
							else await post_data_result,
							headers=headers_result
							if not isinstance(headers_result, Awaitable)
							else await headers_result,
					)
			)
		except (Exception,) as error:
			handler_settings["on_error"](self, event, error)
	
	@property
	def is_active(self) -> bool:
		"""
		Checks if DevTools is currently active.

		Returns:
			bool: True if DevTools event handler context manager is active, False otherwise.
		"""
		
		return self._is_active
	
	@warn_if_active
	def _remove_handler_settings(self, event_type: str, event_name: str):
		"""
		Removes specific handler settings for a given DevTools event.

		This method is used internally to clean up configurations when a handler is no longer needed.
		It sets the handler settings for a specific event name under an event type to None and updates the 'use' flag for that event type.

		Args:
			event_type (str): The type of DevTools event domain (e.g., "fetch").
			event_name (str): The name of the specific event handler within the event type (e.g., "request_paused").
		"""
		
		self._callbacks_settings[event_type][event_name] = None
		self._callbacks_settings[event_type]["use"] = len(
				[
					key
					for key, value in self._callbacks_settings[event_type].items()
					if key not in ["use", "enable_func_path", "disable_func_path"]
					and value is not None
				]
		) != 0
	
	def remove_request_paused_handler_settings(self):
		"""
		Removes the settings for the request paused handler specifically for fetch events.

		This method disables the interception and modification of network requests that were set up using `set_request_paused_handler`.
		It calls `_remove_handler_settings` specifically for the 'fetch' event type and 'request_paused' event name.
		"""
		
		self._remove_handler_settings(event_type="fetch", event_name="request_paused")
	
	@warn_if_active
	def _set_handler_settings(
			self,
			event_type: str,
			event_name: str,
			settings_type: type,
			**kwargs: Any
	):
		"""
		Sets handler settings for a specific DevTools event.

		This internal method configures the settings for handling a specific DevTools event. It updates the `_callbacks_settings`
		with the provided settings, including the settings type and any keyword arguments, and marks the event type as 'in use'.

		Args:
			event_type (str): The type of DevTools event domain (e.g., "fetch").
			event_name (str): The name of the specific event handler within the event type (e.g., "request_paused").
			settings_type (type): The class type for the settings object, used for instantiation.
			**kwargs (Any): Keyword arguments to be passed to the settings_type constructor.
		"""
		
		self._callbacks_settings[event_type]["use"] = True
		self._callbacks_settings[event_type][event_name] = settings_type(**kwargs)
	
	def set_request_paused_handler(
			self,
			listen_buffer_size: int = 50,
			post_data_instances: Optional[Any] = None,
			headers_instances: Optional[dict[str, fetch.HeaderInstance]] = None,
			post_data_handler: Optional[fetch.post_data_handler_type] = None,
			headers_handler: Optional[fetch.headers_handler_type] = None
	):
		"""
		Sets up a handler for 'fetch.requestPaused' DevTools events to intercept and modify network requests.

		Configures the Chrome DevTools Protocol's Fetch domain to intercept network requests
		that the browser is about to send. When a request is paused, the configured handler
		settings and custom handler functions are used to potentially inspect or modify
		the request's post data and headers before allowing the request to continue.

		Args:
			listen_buffer_size (int): The size of the buffer for the Trio channel that will
				listen for incoming 'fetch.requestPaused' events. Defaults to 50.
			post_data_instances (Optional[Any]): Optional data structure(s) used to match against
				the request's post data. If provided, the handler might only process requests
				whose post data matches one of these instances, depending on the custom handler logic.
				Defaults to None (no post data matching required by settings).
			headers_instances (Optional[Dict[str, fetch.HeaderInstance]]): Optional dictionary defining
				header modifications based on predefined instructions. Keys are header names, and
				values are `HeaderInstance` objects specifying how to modify the header (e.g., set, remove).
				These instances are passed to the `headers_handler`. Defaults to None (no instance-based header modifications).
			post_data_handler (Optional[fetch.post_data_handler_type]): A custom callable (function or method)
				to process and modify the request's post data. This function receives the handler settings
				and the event object. If None, `fetch.default_post_data_handler` is used. Defaults to None.
			headers_handler (Optional[fetch.headers_handler_type]): A custom callable (function or method)
				to process and modify the request's headers. This function receives the handler settings,
				the DevTools header entry class, and the event object. If None, `fetch.default_headers_handler`
				is used. Defaults to None.
		"""
		
		self._set_handler_settings(
				event_type="fetch",
				event_name="request_paused",
				settings_type=fetch.RequestPausedHandlerSettings,
				class_to_use_path="fetch.RequestPaused",
				listen_buffer_size=listen_buffer_size,
				post_data_instances=post_data_instances,
				headers_instances=headers_instances,
				post_data_handler=fetch.default_post_data_handler
				if post_data_handler is None
				else post_data_handler,
				headers_handler=fetch.default_headers_handler
				if headers_handler is None
				else headers_handler,
				on_error=fetch.default_on_error
		)
