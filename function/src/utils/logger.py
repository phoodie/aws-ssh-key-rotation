import logging
import json
from typing import Any, Dict

class StepLogger(logging.Logger):
   def __init__(self, name):
       super().__init__(name)
       self._step = None
   
   @property 
   def step(self):
       return self._step
       
   @step.setter
   def step(self, value):
       self._step = value

class JsonFormatter(logging.Formatter):
   def format(self, record: logging.LogRecord) -> str:
       # Extract message if it's a dict
       msg = record.msg if isinstance(record.msg, dict) else {'msg': record.getMessage()}

       # Get logger step value
       logger_step = getattr(record.module_logger, 'step', None) if hasattr(record, 'module_logger') else None
       
       # Build log entry
       log_data = {
           'level': record.levelname.lower(),
           'time': int(record.created * 1000),
           'step': logger_step,
           **msg
       }

       # Remove None values
       log_data = {k: v for k, v in log_data.items() if v is not None}

       if record.exc_info:
           log_data['error'] = self.formatException(record.exc_info)

       return json.dumps(log_data)

# Register custom logger
logging.setLoggerClass(StepLogger)

# Single logger instance
logger = logging.getLogger('ssh-rotation')
handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
logger.handlers.clear()
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Prevent duplicate logs
logger.propagate = False
logging.getLogger().handlers.clear()