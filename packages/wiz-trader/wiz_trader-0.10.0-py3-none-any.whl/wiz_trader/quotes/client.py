import asyncio
import json
import os
import logging
import random
from typing import Callable, List, Optional, Any, Dict, Iterator

import websockets
from websockets.exceptions import ConnectionClosed
from websockets.protocol import State

# Setup module-level logger with a default handler if none exists.
logger = logging.getLogger(__name__)
if not logger.handlers:
  handler = logging.StreamHandler()
  formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
  handler.setFormatter(formatter)
  logger.addHandler(handler)


class QuotesClient:
  """
  A Python SDK for connecting to the Quotes Server via WebSocket.

  Attributes:
    base_url (str): WebSocket URL of the quotes server.
    token (str): JWT token for authentication.
    log_level (str): Logging level. Options: "error", "info", "debug".
  """

  # Constants for actions
  ACTION_SUBSCRIBE = "subscribe"
  ACTION_UNSUBSCRIBE = "unsubscribe"

  def __init__(
    self, 
    base_url: Optional[str] = None, 
    token: Optional[str] = None,
    log_level: str = "error",  # default only errors
    max_message_size: int = 10 * 1024 * 1024,  # 10MB default max size
    batch_size: int = 20  # Max number of instruments to subscribe to at once
  ):
    # Configure logger based on log_level.
    valid_levels = {"error": logging.ERROR, "info": logging.INFO, "debug": logging.DEBUG}
    if log_level not in valid_levels:
      raise ValueError(f"log_level must be one of {list(valid_levels.keys())}")
    logger.setLevel(valid_levels[log_level])
    
    self.log_level = log_level
    self.max_message_size = max_message_size
    self.batch_size = batch_size
    # System env vars take precedence over .env
    self.base_url = base_url or os.environ.get("WZ__QUOTES_BASE_URL")
    self.token = token or os.environ.get("WZ__TOKEN")
    if not self.token:
      raise ValueError("JWT token must be provided as an argument or in .env (WZ__TOKEN)")
    if not self.base_url:
      raise ValueError("Base URL must be provided as an argument or in .env (WZ__QUOTES_BASE_URL)")

    # Construct the WebSocket URL.
    self.url = f"{self.base_url}?token={self.token}"
    self.ws: Optional[websockets.WebSocketClientProtocol] = None
    self.subscribed_instruments: set = set()
    self._running = False
    self._background_task = None

    # Backoff configuration for reconnection (in seconds)
    self._backoff_base = 1
    self._backoff_factor = 2
    self._backoff_max = 60

    # Callbacks
    self.on_tick: Optional[Callable[[Any, dict], None]] = None
    self.on_connect: Optional[Callable[[Any], None]] = None
    self.on_close: Optional[Callable[[Any, Optional[int], Optional[str]], None]] = None
    self.on_error: Optional[Callable[[Any, Exception], None]] = None
    
    logger.debug("Initialized QuotesClient with URL: %s", self.url)

  def _chunk_list(self, data: List[Any], chunk_size: int) -> Iterator[List[Any]]:
    """
    Split a list into smaller chunks.
    
    Args:
        data (List[Any]): The list to split.
        chunk_size (int): Maximum size of each chunk.
        
    Returns:
        Iterator[List[Any]]: Iterator of list chunks.
    """
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]

  async def _connect_with_backoff(self) -> None:
    """
    Continuously connect to the quotes server with exponential backoff.
    """
    backoff = self._backoff_base

    while self._running:
      try:
        logger.info("Connecting to %s ...", self.url)
        async with websockets.connect(self.url, max_size=self.max_message_size) as websocket:
          self.ws = websocket
          logger.info("Connected to the quotes server.")
          
          # Call the on_connect callback if provided
          if self.on_connect:
            try:
              self.on_connect(self)
            except Exception as e:
              logger.error("Error in on_connect callback: %s", e, exc_info=True)
          
          # On reconnection, re-subscribe if needed.
          if self.subscribed_instruments:
            # Split into batches to avoid message size issues
            instruments_list = list(self.subscribed_instruments)
            for batch in self._chunk_list(instruments_list, self.batch_size):
              subscribe_msg = {
                "action": self.ACTION_SUBSCRIBE,
                "instruments": batch
              }
              await self.ws.send(json.dumps(subscribe_msg))
              logger.info("Re-subscribed to batch of %d instruments", len(batch))
              # Small delay between batches to avoid overwhelming the server
              await asyncio.sleep(0.1)

          # Reset backoff after a successful connection.
          backoff = self._backoff_base

          await self._handle_messages()
      except ConnectionClosed as e:
        logger.info("Disconnected from the quotes server: %s", e)
        # Call the on_close callback if provided
        if self.on_close:
          try:
            self.on_close(self, getattr(e, 'code', None), str(e))
          except Exception as e:
            logger.error("Error in on_close callback: %s", e, exc_info=True)
      except Exception as e:
        logger.error("Connection error: %s", e, exc_info=True)
        # Call the on_error callback if provided
        if self.on_error:
          try:
            self.on_error(self, e)
          except Exception as e:
            logger.error("Error in on_error callback: %s", e, exc_info=True)

      # Don't reconnect if we're no longer running
      if not self._running:
        break
        
      # Exponential backoff before reconnecting.
      sleep_time = min(backoff, self._backoff_max)
      logger.info("Reconnecting in %s seconds...", sleep_time)
      await asyncio.sleep(sleep_time)
      backoff *= self._backoff_factor
      # Add a bit of randomness to avoid thundering herd issues.
      backoff += random.uniform(0, 1)

  async def _handle_messages(self) -> None:
    """
    Handle incoming messages and dispatch them via the on_tick callback.
    Handles newline-delimited JSON objects in a single message.
    """
    try:
      async for message in self.ws:  # type: ignore
        # Log message size for debugging large message issues
        if self.log_level == "debug" and isinstance(message, str):
          message_size = len(message.encode("utf-8"))
          if message_size > 1024 * 1024:  # Over 1MB
            logger.debug("Received large message: %d bytes", message_size)
            # Log the beginning of the message for debugging
            logger.debug("Message starts with: %s", message[:100])
        
        if isinstance(message, str):
          # Special handling for newline-delimited JSON
          if '\n' in message:
            # Split by newlines and process each JSON object separately
            for json_str in message.strip().split('\n'):
              if not json_str:
                continue
                
              try:
                tick = json.loads(json_str)
                if self.on_tick:
                  self.on_tick(self, tick)
              except json.JSONDecodeError as e:
                logger.error("Failed to parse JSON object: %s", str(e))
                logger.error("Invalid JSON: %s...", json_str[:100])
          else:
            # Single JSON object
            try:
              tick = json.loads(message)
              if self.on_tick:
                self.on_tick(self, tick)
            except json.JSONDecodeError as e:
              logger.error("Failed to parse JSON: %s", str(e))
              logger.error("Invalid JSON message: %s...", message[:100])
        else:
          logger.warning("Received non-string message: %s", type(message))
    except ConnectionClosed as e:
      logger.info("Connection closed during message handling: %s", e)
      # Let the _connect_with_backoff method handle reconnection
    except Exception as e:
      logger.error("Error processing message: %s", str(e), exc_info=True)
      # Call the on_error callback if provided
      if self.on_error:
        try:
          self.on_error(self, e)
        except Exception as e:
          logger.error("Error in on_error callback: %s", e, exc_info=True)

  async def subscribe(self, instruments: List[str]) -> None:
    """
    Subscribe to a list of instruments.

    Args:
      instruments (List[str]): List of instrument identifiers.
    """
    if self.ws and self.ws.state == State.OPEN:
      new_instruments = set(instruments) - self.subscribed_instruments
      if new_instruments:
        self.subscribed_instruments.update(new_instruments)
        
        # Split into batches to avoid message size issues
        new_instruments_list = list(new_instruments)
        for batch in self._chunk_list(new_instruments_list, self.batch_size):
          logger.info("Subscribing to batch of %d instruments", len(batch))
          message = {"action": self.ACTION_SUBSCRIBE, "instruments": batch}
          await self.ws.send(json.dumps(message))
          # Small delay between batches to avoid overwhelming the server
          await asyncio.sleep(0.1)
        
        logger.info("Completed subscription for %d new instruments", len(new_instruments))
      else:
        logger.info("Instruments already subscribed: %s", instruments)
    else:
      logger.info("Cannot subscribe: WebSocket is not connected.")
      # Still update the subscription list so we can subscribe when connected
      self.subscribed_instruments.update(set(instruments))

  async def unsubscribe(self, instruments: List[str]) -> None:
    """
    Unsubscribe from a list of instruments.

    Args:
      instruments (List[str]): List of instrument identifiers.
    """
    if self.ws and self.ws.state == State.OPEN:
      unsub_set = set(instruments)
      to_unsubscribe = unsub_set & self.subscribed_instruments
      
      if to_unsubscribe:
        self.subscribed_instruments.difference_update(to_unsubscribe)
        
        # Split into batches to avoid message size issues
        unsub_list = list(to_unsubscribe)
        for batch in self._chunk_list(unsub_list, self.batch_size):
          logger.info("Unsubscribing from batch of %d instruments", len(batch))
          message = {"action": self.ACTION_UNSUBSCRIBE, "instruments": batch}
          await self.ws.send(json.dumps(message))
          # Small delay between batches to avoid overwhelming the server
          await asyncio.sleep(0.1)
          
        logger.info("Completed unsubscription for %d instruments", len(to_unsubscribe))
      else:
        logger.info("No matching instruments found in current subscription.")
    else:
      logger.info("Cannot unsubscribe: WebSocket is not connected.")
      # Still update the subscription list
      self.subscribed_instruments.difference_update(set(instruments))

  async def close(self) -> None:
    """
    Close the WebSocket connection.
    """
    self._running = False
    if self.ws:
      await self.ws.close()
      logger.info("WebSocket connection closed.")
    
    # Cancel the background task if it exists
    if self._background_task and not self._background_task.done():
      self._background_task.cancel()
      try:
        await self._background_task
      except asyncio.CancelledError:
        pass

  def connect(self) -> None:
    """
    Connect to the websocket server in a blocking manner.
    This method handles the event loop and will not return until stop() is called.
    
    Similar to KiteTicker's connect() method, this creates and runs the event loop.
    """
    self._running = True
    
    # If there's already an event loop, use it
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        # No event loop exists, create a new one
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    try:
        # Run until completion (i.e., until stop() is called)
        loop.run_until_complete(self._connect_with_backoff())
    finally:
        if not loop.is_closed():
            # Clean up pending tasks
            pending = asyncio.all_tasks(loop)
            for task in pending:
                task.cancel()
            
            # Run until all tasks are properly canceled
            try:
                loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
            except Exception:
                pass

  def connect_async(self) -> None:
    """
    Connect to the websocket server in a non-blocking manner.
    This method starts the connection in a background task.
    """
    if self._running:
      logger.warning("Client is already running.")
      return
    
    self._running = True
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    self._background_task = asyncio.create_task(self._connect_with_backoff())
    
  def stop(self) -> None:
    """
    Stop the websocket connection.
    This is a non-blocking method that just flags the client to stop.
    """
    self._running = False
    logger.info("Client stopping. Connection will close soon.")