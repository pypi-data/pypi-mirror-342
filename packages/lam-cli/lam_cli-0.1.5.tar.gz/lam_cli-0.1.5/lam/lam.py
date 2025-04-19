#!/usr/bin/env python3

import json
import logging
import os
import re
import shutil
import socket
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, Union

import click
import psutil
from logtail import LogtailHandler
from posthog import Posthog

# Initialize analytics and logging
posthog = Posthog(project_api_key='phc_wfeHFG0p5yZIdBpjVYy00o5x1HbEpggdMzIuFYgNPSK', 
                  host='https://app.posthog.com')

# Configure logging with UTC timezone
logging.Formatter.converter = lambda *args: datetime.now(timezone.utc).timetuple()
logging.basicConfig(level=logging.DEBUG, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger('urllib3').setLevel(logging.WARNING)  # Suppress urllib3 logs

handler = LogtailHandler(source_token="TYz3WrrvC8ehYjXdAEGGyiDp")
logger.addHandler(handler)

class LAMError(Exception):
    """Base exception for LAM errors"""
    pass

class UserError(LAMError):
    """Errors caused by user input"""
    pass

class SystemError(LAMError):
    """Errors caused by system issues"""
    pass

class ResourceLimitError(LAMError):
    """Errors caused by resource limits"""
    pass

def check_resource_limits(modules_dir: Optional[Path] = None) -> None:
    """Check system resource availability"""
    logger.debug("Checking system resource limits")
    disk = shutil.disk_usage(tempfile.gettempdir())
    if disk.free < 100 * 1024 * 1024:  # 100MB minimum
        logger.critical("Insufficient disk space: %dMB free", disk.free // (1024*1024))
        raise ResourceLimitError("Insufficient disk space")
    
    if modules_dir and modules_dir.exists():
        modules_size = sum(
            os.path.getsize(os.path.join(dirpath, filename))
            for dirpath, _, filenames in os.walk(modules_dir)
            for filename in filenames
        )
        if modules_size > 500 * 1024 * 1024:
            logger.warning("Cleaning oversized modules directory (%dMB)", modules_size//(1024*1024))
            shutil.rmtree(modules_dir)
            modules_dir.mkdir(exist_ok=True)

class Stats:
    """Track execution statistics"""
    def __init__(self):
        self.start_time = datetime.now()
        self.memory_start = self.get_memory_usage()
    
    def get_memory_usage(self):
        process = psutil.Process()
        return process.memory_info().rss
    
    def finalize(self):
        return {
            'duration_ms': (datetime.now() - self.start_time).total_seconds() * 1000,
            'memory_used_mb': (self.get_memory_usage() - self.memory_start) / (1024 * 1024),
            'timestamp': datetime.now().isoformat()
        }

class EngineType(Enum):
    JQ = "jq"
    JAVASCRIPT = "js"
    PYTHON = "py"

class ProcessingError(Exception):
    """Custom exception for processing errors"""
    pass

class Engine:
    """Base class for execution engines"""
    def __init__(self, workspace_id: str, flow_id: str, execution_id: str):
        self.workspace_id = workspace_id
        self.flow_id = flow_id
        self.execution_id = execution_id
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    def get_log_file(self) -> str:
        return f"lam_run_{self.workspace_id}_{self.flow_id}_{self.execution_id}_{self.timestamp}.log"

    def get_result_file(self) -> str:
        return f"lam_result_{self.workspace_id}_{self.flow_id}_{self.execution_id}_{self.timestamp}.json"

    def track_event(self, event_name: str, properties: Dict[str, Any]) -> None:
        """Track events with PostHog"""
        try:
            distinct_id = f"{os.getuid()}_{socket.gethostname()}_{self.workspace_id}_{self.flow_id}"
            properties |= {
                'workspace_id': self.workspace_id,
                'flow_id': self.flow_id,
                'engine': self.__class__.__name__,
            }
            posthog.capture(distinct_id=distinct_id, event=event_name, properties=properties)
        except Exception as e:
            logger.error(f"Error tracking event: {e}")

class JQEngine(Engine):
    """JQ execution engine"""
    def validate_environment(self) -> bool:
        logger.debug("Validating JQ environment")
        return shutil.which("jq") is not None

    def execute(self, program_file: str, input_data: str) -> Tuple[Union[Dict, str], Optional[str]]:
        logger.info(f"Executing JQ script: {program_file}")
        
        try:
            with open(program_file, 'r') as file:
                jq_script = ''.join(line for line in file if not line.strip().startswith('#'))
                logger.debug("Loaded JQ script: %d characters", len(jq_script))

            process = subprocess.Popen(
                ["jq", "-c", jq_script],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            logger.debug("Starting JQ process PID %d", process.pid)
            output, error = process.communicate(input=input_data)
            
            if error:
                logger.error("JQ error output: %s", error.strip())
                raise ProcessingError(error)
                
            # Handle output
            try:
                output_lines = [line.strip() for line in output.splitlines() if line.strip()]
                logger.debug(f"Found {len(output_lines)} JSON objects in output")
                
                if len(output_lines) > 1:
                    parsed = [json.loads(line) for line in output_lines]
                    logger.info(f"Processed {len(parsed)} JSON objects")
                    return {"lam.result": parsed}, None
                elif len(output_lines) == 1:
                    result = json.loads(output_lines[0])
                    logger.info("Processed single JSON object")
                    return result, None
                else:
                    logger.info("No JSON objects in output")
                    return {"lam.error": "No JSON objects in output"}, "No JSON objects in output"
                    
            except json.JSONDecodeError as e:
                return {"lam.result": output}, None
                
        except Exception as e:
            logger.exception("JQ execution failed")
            self.track_event('lam.jq.error', {'error': str(e)})
            return {"lam.error": str(e)}, str(e)

class BunEngine(Engine):
    """Bun JavaScript execution engine with enhanced logging"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.modules_dir = Path(tempfile.gettempdir()) / "lam_modules"
        self.modules_dir.mkdir(exist_ok=True)
        self._setup_shared_modules()
        
        self.runtime_template = '''
        const logs = [];
        const originalLog = console.log;
        const originalError = console.error;
        const originalWarn = console.warn;
        
        console.log = (...args) => logs.push({ type: 'log', message: args.map(String).join(' ') });
        console.error = (...args) => {
            originalError(...args);  // Keep error output for debugging
            logs.push({ type: 'error', message: args.map(String).join(' ') });
        };
        console.warn = (...args) => logs.push({ type: 'warn', message: args.map(String).join(' ') });
        
        // Keep original stdout for result output
        const writeResult = (obj) => {
            console.error("Writing result:", JSON.stringify(obj, null, 2));
            originalLog(JSON.stringify(obj));
        };
        
        const _ = require('lodash');
        const { format, parseISO } = require('date-fns');
        
        module.exports = {
            _,
            format,
            parseISO,
            logs,
            writeResult
        };
        '''

    def _setup_shared_modules(self):
        """Setup shared node_modules once"""
        if not (self.modules_dir / "node_modules").exists():
            logger.info("Initializing shared modules directory")
            package_json = {
                "dependencies": {
                    "lodash": "^4.17.21",
                    "date-fns": "^2.30.0"
                }
            }
            with open(self.modules_dir / "package.json", "w") as f:
                json.dump(package_json, f, indent=2)

            try:
                logger.debug("Installing shared dependencies")
                result = subprocess.run(
                    [self.get_bun_path(), "install"],
                    cwd=self.modules_dir,
                    check=True,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                logger.debug("Dependency install output: %s", result.stdout)
            except subprocess.CalledProcessError as e:
                logger.error("Dependency install failed: %s", e.stderr)
                raise ProcessingError(f"Environment setup failed: {e.stderr}") from e

    def create_wrapper(self, input_data: str, user_script: str) -> str:
        """Create the wrapper script with proper escaping"""
        return f'''
        const {{ _, format, parseISO, logs, writeResult }} = require('./runtime.js');

        // Utility function to handle circular references in JSON.stringify
        function safeStringify(obj) {{
            const seen = new WeakSet();
            return JSON.stringify(obj, (key, value) => {{
                if (typeof value === 'object' && value !== null) {{
                    if (seen.has(value)) {{
                        return '[Circular Reference]';
                    }}
                    seen.add(value);
                }}
                return value;
            }}, 2);
        }}

        // Validate transform function
        function validateTransform(fn) {{
            if (typeof fn !== 'function') {{
                throw new Error('Transform must be a function');
            }}
            if (fn.length !== 1) {{
                throw new Error('Transform function must accept exactly one argument (input)');
            }}
        }}

        // Execute transform immediately
        try {{
            // Parse input safely
            let input;
            try {{
                input = JSON.parse({json.dumps(input_data)});
            }} catch (e) {{
                throw new Error(`Failed to parse input data: ${{e.message}}`);
            }}

            // Get transform function
            let transform;
            try {{
                transform = {user_script};
            }} catch (e) {{
                throw new Error(`Failed to parse transform function: ${{e.message}}`);
            }}

            // Validate transform
            validateTransform(transform);

            // Execute transform
            const result = transform(input);

            // Output result after transform
            writeResult({{
                result,
                logs
            }});
        }} catch (error) {{
            console.error(JSON.stringify({{
                error: error.message,
                stack: error.stack?.split('\\n') || [],
                type: error.constructor.name
            }}));
            process.exit(1);
        }}
        '''
    
    def setup_environment(self, temp_dir: Path) -> None:
        """Set up the JavaScript environment with runtime"""
        # Write runtime file only
        runtime_path = temp_dir / "runtime.js"
        with open(runtime_path, "w") as f:
            f.write(self.runtime_template)
        logger.debug("Runtime file written to: %s", runtime_path)
        
        # Symlink node_modules from shared directory
        os.symlink(self.modules_dir / "node_modules", temp_dir / "node_modules")
        logger.debug("node_modules symlinked from: %s", self.modules_dir / "node_modules")

    def validate_environment(self) -> bool:
        # Check multiple locations for bun
        possible_locations = [
            "bun",  # System PATH
            os.path.join(os.path.dirname(sys.executable), "bun"),  # venv/bin
            os.path.join(os.path.dirname(os.path.dirname(sys.executable)), "bin", "bun")  # venv/bin (alternative)
        ]
        
        return any(shutil.which(loc) is not None for loc in possible_locations)

    def get_bun_path(self) -> str:
        """Get the appropriate bun executable path"""
        possible_locations = [
            "bun",
            os.path.join(os.path.dirname(sys.executable), "bun"),
            os.path.join(os.path.dirname(os.path.dirname(sys.executable)), "bin", "bun")
        ]
        
        for loc in possible_locations:
            if shutil.which(loc):
                return shutil.which(loc)
        
        raise EnvironmentError("Bun not found in environment")

    def execute(self, program_file: str, input_data: str) -> Tuple[Union[Dict, str], Optional[str]]:
        logger.info(f"Executing Bun script: {program_file}")
        stats = Stats()

        try:
            check_resource_limits(self.modules_dir)

            with tempfile.TemporaryDirectory() as temp_dir:
                temp_dir = Path(temp_dir)
                self.setup_environment(temp_dir)

                # Read user script
                with open(program_file, 'r') as f:
                    user_script = f.read()
                    logger.debug("Loaded user script: %d characters", len(user_script))

                # Create wrapper script
                wrapper = self.create_wrapper(input_data, user_script)
                script_path = temp_dir / "script.js"
                with open(script_path, 'w') as f:
                    f.write(wrapper)
                logger.debug("Generated wrapper script: %s", script_path)

                # Execute with Bun
                process = subprocess.Popen(
                    [
                        self.get_bun_path(),
                        "run",
                        "--no-fetch",
                        "--smol",
                        "--silent",
                        str(script_path)
                    ],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    cwd=temp_dir
                )
                logger.info("Started Bun process PID %d", process.pid)

                try:
                    output, error = process.communicate(timeout=5)
                    logger.debug("Process completed with code %d", process.returncode)
                except subprocess.TimeoutExpired as e:
                    logger.warning("Process timeout after 5 seconds")
                    process.kill()
                    return {"lam.error": "Script execution timed out"}, "Execution timed out after 5 seconds"

                # Handle process errors
                if process.returncode != 0:
                    try:
                        # Try to parse structured error from stderr
                        error_data = json.loads(error.strip())
                        error_msg = error_data.get('error', 'Unknown error')
                        stack = error_data.get('stack', [])
                        
                        # Format error message
                        error_details = {
                            "lam.error": error_msg,
                            "stack_trace": stack
                        }
                        return error_details, error_msg
                        
                    except json.JSONDecodeError:
                        # Fallback to raw error output
                        error_msg = error.strip() or "Unknown error"
                        return {"lam.error": error_msg}, error_msg

                # Handle successful output
                try:
                    output_data = json.loads(output)
                    
                    # Process JavaScript logs (if any)
                    if 'logs' in output_data:
                        for log_entry in output_data.get('logs', []):
                            if log_entry['type'] == 'error':
                                logger.error("[JS] %s", log_entry['message'])
                            else:
                                logger.debug("[JS] %s", log_entry['message'])
                    
                    result = output_data.get('result', {})
                    return result, None

                except json.JSONDecodeError as e:
                    logger.error("Failed to parse output: %s", str(e))
                    return {
                        "lam.error": "Invalid JSON output",
                        "raw_output": output.strip()
                    }, "Output format error"

        except Exception as e:
            logger.exception("Execution failed")
            return {
                "lam.error": str(e),
                "type": e.__class__.__name__
            }, str(e)

class PythonEngine(Engine):
    """Python execution engine with improved sandboxing for security"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.modules_dir = Path(tempfile.gettempdir()) / "lam_python_modules"
        self.modules_dir.mkdir(exist_ok=True)
        # Define allowed modules that can be safely imported
        self.allowed_modules = {
            "json", "datetime", "math", "statistics", "collections", 
            "itertools", "functools", "re", "copy", "decimal",
            "csv", "io", "dataclasses", "typing", "enum"
        }
        
    def validate_environment(self) -> bool:
        logger.debug("Validating Python environment")
        return sys.executable is not None
        
    def create_safe_globals(self) -> dict:
        """Create a restricted globals dictionary for safer execution"""
        safe_globals = {
            "__builtins__": {
                # Safe builtins only
                "abs": abs, "all": all, "any": any, "bool": bool,
                "chr": chr, "dict": dict, "dir": dir, "divmod": divmod,
                "enumerate": enumerate, "filter": filter, "float": float,
                "format": format, "frozenset": frozenset, "hash": hash,
                "hex": hex, "int": int, "isinstance": isinstance,
                "issubclass": issubclass, "iter": iter, "len": len,
                "list": list, "map": map, "max": max, "min": min,
                "next": next, "oct": oct, "ord": ord, "pow": pow,
                "print": print, "range": range, "repr": repr,
                "reversed": reversed, "round": round, "set": set,
                "slice": slice, "sorted": sorted, "str": str, "sum": sum,
                "tuple": tuple, "type": type, "zip": zip,
                # Add Exception types for error handling
                "Exception": Exception, "ValueError": ValueError,
                "TypeError": TypeError, "KeyError": KeyError,
                "IndexError": IndexError
            },
            # Pre-import safe modules
            "json": json,
            "datetime": datetime,
            "math": __import__("math"),
            "statistics": __import__("statistics"),
            "collections": __import__("collections"),
            "itertools": __import__("itertools"),
            "functools": __import__("functools"),
            "re": __import__("re")
        }
        return safe_globals

    def check_for_dangerous_code(self, code: str) -> Optional[str]:
        """Check for potentially dangerous patterns in the code"""
        dangerous_patterns = [
            (r"__import__\s*\(", "Use of __import__ is not allowed"),
            (r"eval\s*\(", "Use of eval() is not allowed"),
            (r"exec\s*\(", "Use of exec() is not allowed"),
            (r"globals\s*\(", "Access to globals() is not allowed"),
            (r"locals\s*\(", "Access to locals() is not allowed"),
            (r"getattr\s*\(", "Use of getattr() is not allowed"),
            (r"setattr\s*\(", "Use of setattr() is not allowed"),
            (r"delattr\s*\(", "Use of delattr() is not allowed"),
            (r"compile\s*\(", "Use of compile() is not allowed"),
            (r"open\s*\(", "Use of open() is not allowed"),
            (r"__subclasses__", "Access to __subclasses__ is not allowed"),
            (r"subprocess", "Access to subprocess module is not allowed"),
            (r"sys\.", "Access to sys module is not allowed"),
            (r"os\.", "Access to os module is not allowed"),
            (r"shutil", "Access to shutil module is not allowed"),
            (r"pathlib", "Access to pathlib module is not allowed"),
            (r"importlib", "Access to importlib module is not allowed"),
            (r"builtins", "Access to builtins module is not allowed"),
            (r"_thread", "Access to _thread module is not allowed"),
            (r"ctypes", "Access to ctypes module is not allowed"),
            (r"socket", "Access to socket module is not allowed"),
            (r"pickle", "Access to pickle module is not allowed"),
            (r"multiprocessing", "Access to multiprocessing module is not allowed"),
            (r"__\w+__", "Access to dunder attributes may not be allowed")
        ]
        
        for pattern, message in dangerous_patterns:
            if re.search(pattern, code):
                return message
        
        # Check for imports outside of allowed modules
        import_pattern = r"import\s+(\w+)|from\s+(\w+)\s+import"
        for match in re.finditer(import_pattern, code):
            module = match.group(1) or match.group(2)
            if module and module not in self.allowed_modules:
                return f"Import of '{module}' is not allowed, only these modules are permitted: {', '.join(sorted(self.allowed_modules))}"
        
        return None

    def create_wrapper(self, input_data: str, user_script: str) -> str:
        """Create the wrapper script with proper escaping and sandboxing"""
        # Perform safety checks before creating wrapper
        safety_issue = self.check_for_dangerous_code(user_script)
        if safety_issue:
            # Return a wrapper that will immediately exit with the safety error
            return f'''
import json
import sys

sys.stdout.write(json.dumps({{
    "error": "Security violation detected: {safety_issue}",
    "stack": []
}}))
sys.exit(1)
'''

        return f'''
import json
import sys
import traceback
from datetime import datetime
import re
import math
import statistics
import collections
import itertools
import functools

# Resource limiting
import resource
import signal

# Set resource limits
def set_resource_limits():
    # 5 seconds CPU time
    resource.setrlimit(resource.RLIMIT_CPU, (5, 5))
    
    # 100MB memory limit
    memory_limit = 100 * 1024 * 1024  # 100MB in bytes
    resource.setrlimit(resource.RLIMIT_AS, (memory_limit, memory_limit))
    
    # Set timeout handler
    def timeout_handler(signum, frame):
        sys.stderr.write(json.dumps({{
            "error": "Execution timed out (5 seconds)",
            "stack": []
        }}))
        sys.exit(1)
    
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(5)  # 5 second timeout

try:
    set_resource_limits()
except Exception as e:
    # Continue if resource limiting is not available (e.g., on Windows)
    pass

# Setup basic logging
logs = []

class LogCapture:
    def __init__(self, log_type):
        self.log_type = log_type
        
    def write(self, message):
        if message.strip():
            logs.append({{"type": self.log_type, "message": message.strip()}})
        return len(message)
        
    def flush(self):
        pass

# Custom safer importer
class RestrictedImporter:
    def __init__(self, allowed_modules):
        self.allowed_modules = allowed_modules
        
    def __call__(self, name, *args, **kwargs):
        if name in self.allowed_modules:
            return __import__(name, *args, **kwargs)
        else:
            raise ImportError(f"Import of '{{name}}' is not allowed for security reasons. " +
                             f"Allowed modules: {{', '.join(sorted(self.allowed_modules))}}")

# Capture stdout and stderr
original_stdout = sys.stdout
original_stderr = sys.stderr
sys.stdout = LogCapture("log")
sys.stderr = LogCapture("error")

# Parse input data
try:
    input_data = json.loads(r"""{input_data}""")
except json.JSONDecodeError as e:
    original_stderr.write(json.dumps({{"error": f"Failed to parse input data: {{e}}"}}))
    sys.exit(1)

# Create safe environment
safe_globals = {{
    "__builtins__": {{
        # Safe builtins only
        "abs": abs, "all": all, "any": any, "bool": bool,
        "chr": chr, "dict": dict, "divmod": divmod,
        "enumerate": enumerate, "filter": filter, "float": float,
        "format": format, "frozenset": frozenset, "hash": hash,
        "hex": hex, "int": int, "isinstance": isinstance,
        "issubclass": issubclass, "iter": iter, "len": len,
        "list": list, "map": map, "max": max, "min": min,
        "next": next, "oct": oct, "ord": ord, "pow": pow,
        "print": print, "range": range, "repr": repr,
        "reversed": reversed, "round": round, "set": set,
        "slice": slice, "sorted": sorted, "str": str, "sum": sum,
        "tuple": tuple, "type": type, "zip": zip,
        # Exception types for error handling
        "Exception": Exception, "ValueError": ValueError,
        "TypeError": TypeError, "KeyError": KeyError,
        "IndexError": IndexError,
        # Add a safe import function
        "__import__": RestrictedImporter({{
            "json", "datetime", "math", "statistics", "collections", 
            "itertools", "functools", "re", "copy", "decimal",
            "csv", "io", "dataclasses", "typing", "enum"
        }})
    }},
    # Pre-import safe modules
    "json": json,
    "datetime": datetime,
    "math": math,
    "statistics": statistics,
    "collections": collections,
    "itertools": itertools,
    "functools": functools,
    "re": re
}}

safe_locals = {{"input_data": input_data}}

# Define transform function from user script in a safe context
try:
    compiled_code = compile(r"""{user_script}""", "<user_script>", "exec")
    exec(compiled_code, safe_globals, safe_locals)
    
    # Validate transform function exists and has correct signature
    if 'transform' not in safe_locals:
        original_stderr.write(json.dumps({{"error": "No transform function defined"}}))
        sys.exit(1)
        
    if not callable(safe_locals['transform']):
        original_stderr.write(json.dumps({{"error": "transform must be a function"}}))
        sys.exit(1)
        
    transform_fn = safe_locals['transform']
    
except Exception as e:
    original_stderr.write(json.dumps({{
        "error": str(e),
        "stack": traceback.format_exc().split('\\n')
    }}))
    sys.exit(1)

# Execute transform with input data
try:
    # Cancel the alarm if we reach here (we have our own timeout)
    try:
        signal.alarm(0)
    except:
        pass
        
    result = transform_fn(input_data)
    
    # Basic validation of output (to prevent non-serializable data)
    try:
        json.dumps(result)
    except TypeError as e:
        raise TypeError(f"Transform result is not JSON serializable: {{e}}")
    
    # Write result to original stdout
    original_stdout.write(json.dumps({{"result": result, "logs": logs}}))
    
except Exception as e:
    original_stderr.write(json.dumps({{
        "error": str(e),
        "stack": traceback.format_exc().split('\\n')
    }}))
    sys.exit(1)
finally:
    # Restore stdout and stderr
    sys.stdout = original_stdout
    sys.stderr = original_stderr
'''

    def execute(self, program_file: str, input_data: str) -> Tuple[Union[Dict, str], Optional[str]]:
        logger.info(f"Executing Python script: {program_file}")
        stats = Stats()

        try:
            check_resource_limits(self.modules_dir)

            with tempfile.TemporaryDirectory() as temp_dir:
                temp_dir = Path(temp_dir)
                
                # Read user script
                with open(program_file, 'r') as f:
                    user_script = f.read()
                    logger.debug("Loaded user Python script: %d characters", len(user_script))
                
                # Check for dangerous code
                safety_issue = self.check_for_dangerous_code(user_script)
                if safety_issue:
                    logger.warning(f"Security violation detected in script: {safety_issue}")
                    return {
                        "lam.error": f"Security violation: {safety_issue}",
                        "type": "SecurityError"
                    }, f"Security violation: {safety_issue}"

                # Create wrapper script
                wrapper = self.create_wrapper(input_data, user_script)
                script_path = temp_dir / "script.py"
                with open(script_path, 'w') as f:
                    f.write(wrapper)
                logger.debug("Generated Python wrapper script: %s", script_path)

                # Execute with Python in isolated environment
                process = subprocess.Popen(
                    [
                        sys.executable,
                        "-I",  # Isolated mode, ignores environment variables/site packages
                        str(script_path)
                    ],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    cwd=temp_dir,
                    # Prevent access to system environment variables
                    env={"PATH": os.environ.get("PATH", "")}
                )
                logger.info("Started Python process PID %d", process.pid)

                try:
                    output, error = process.communicate(timeout=5)
                    logger.debug("Process completed with code %d", process.returncode)
                except subprocess.TimeoutExpired as e:
                    logger.warning("Process timeout after 5 seconds")
                    process.kill()
                    return {"lam.error": "Script execution timed out"}, "Execution timed out after 5 seconds"

                # Handle process errors
                if process.returncode != 0:
                    try:
                        # Try to parse structured error from stderr
                        error_data = json.loads(error.strip())
                        error_msg = error_data.get('error', 'Unknown error')
                        stack = error_data.get('stack', [])
                        
                        # Format error message
                        error_details = {
                            "lam.error": error_msg,
                            "stack_trace": stack
                        }
                        return error_details, error_msg
                        
                    except json.JSONDecodeError:
                        # Fallback to raw error output
                        error_msg = error.strip() or "Unknown error"
                        return {"lam.error": error_msg}, error_msg

                # Handle successful output
                try:
                    output_data = json.loads(output)
                    
                    # Process Python logs (if any)
                    if 'logs' in output_data:
                        for log_entry in output_data.get('logs', []):
                            if log_entry['type'] == 'error':
                                logger.error("[Python] %s", log_entry['message'])
                            else:
                                logger.debug("[Python] %s", log_entry['message'])
                    
                    result = output_data.get('result', {})
                    return result, None

                except json.JSONDecodeError as e:
                    logger.error("Failed to parse output: %s", str(e))
                    return {
                        "lam.error": "Invalid JSON output",
                        "raw_output": output.strip()
                    }, "Output format error"

        except Exception as e:
            logger.exception("Execution failed")
            return {
                "lam.error": str(e),
                "type": e.__class__.__name__
            }, str(e)

def get_engine(engine_type: str, workspace_id: str, flow_id: str, execution_id: str) -> Engine:
    """Factory function to get the appropriate execution engine"""
    engines = {
        EngineType.JQ.value: JQEngine,
        EngineType.JAVASCRIPT.value: BunEngine,
        EngineType.PYTHON.value: PythonEngine
    }
    
    engine_class = engines.get(engine_type)
    if not engine_class:
        raise ValueError(f"Unsupported engine type: {engine_type}")
    
    engine = engine_class(workspace_id, flow_id, execution_id)
    if not engine.validate_environment():
        raise EnvironmentError(f"Required dependencies not found for {engine_type}")
    
    return engine

def process_input(input: str) -> Tuple[str, Optional[str]]:
    """Process and validate input data"""
    if os.path.isfile(input):
        logger.debug("Loading input from file: %s", input)
        with open(input, 'r') as file:
            return file.read(), None
            
    try:
        json.loads(input)
        logger.debug("Validated inline JSON input")
        return input, None
    except json.JSONDecodeError as e:
        logger.error("Invalid JSON input: %s", str(e))
        return None, str(e)

@click.group()
def lam():
    """LAM - Laminar Data Transformation Tool"""
    pass

@lam.command()
@click.argument('program_file', type=click.Path(exists=True))
@click.argument('input', type=str)
@click.option('--language', type=click.Choice(['jq', 'js', 'py']), default='jq',
              help='Script language (default: jq)')
@click.option('--workspace_id', default="local", help="Workspace ID")
@click.option('--flow_id', default="local", help="Flow ID")
@click.option('--execution_id', default="local", help="Execution ID")
@click.option('--as-json', is_flag=True, default=True, help="Output as JSON")
def run(program_file: str, input: str, language: str, workspace_id: str, 
        flow_id: str, execution_id: str, as_json: bool):
    """Execute a LAM transformation script"""
    stats = Stats()
    
    try:
        engine = get_engine(language, workspace_id, flow_id, execution_id)
    except (ValueError, EnvironmentError) as e:
        click.echo({"lam.error": str(e)}, err=True)
        return

    log_file = engine.get_log_file()
    result_file = engine.get_result_file()
    
    file_handler = logging.FileHandler(log_file, 'w')
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(file_handler)
    
    logger.info("Starting LAM execution with %s engine", language)
    engine.track_event('lam.run.start', {
        'language': language,
        'program_file': program_file
    })

    try:
        input_data, error = process_input(input)
        if error:
            raise ProcessingError(f"Invalid input: {error}")

        result, error = engine.execute(program_file, input_data)
        
        stats_data = stats.finalize()
        logger.info("Execution stats: duration=%.2fms, memory=%.2fMB",
                   stats_data['duration_ms'], stats_data['memory_used_mb'])
        
        if error:
            click.echo({"lam.error": error}, err=True)
            engine.track_event('lam.run.error', {'error': error, **stats_data})
        else:
            output = json.dumps(result, indent=4) if as_json else result
            click.echo(output)
            engine.track_event('lam.run.success', stats_data)
            
        if isinstance(result, list):
            result = {"lam.result": result}
        
        with open(result_file, 'w') as f:
            json.dump(result, f, indent=4)
            
    except Exception as e:
        stats_data = stats.finalize()
        logger.error("Execution failed: %s", str(e))
        logger.error("Final stats: duration=%.2fms, memory=%.2fMB",
                    stats_data['duration_ms'], stats_data['memory_used_mb'])
        click.echo({"lam.error": str(e)}, err=True)
        engine.track_event('lam.run.error', {'error': str(e), **stats_data})
        
    finally:
        logger.info("Execution complete")
        logger.removeHandler(file_handler)

if __name__ == '__main__':
    lam()
