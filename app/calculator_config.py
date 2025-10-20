from dataclasses import dataclass
from decimal import Decimal
from numbers import Number
from pathlib import Path
import os
from typing import Optional
from dotenv import load_dotenv

from app.exceptions import ConfigurationError

load_dotenv()

def get_project_root() -> Path:
    """
    Return the root directory of the project

    """

    current_file = Path(__file__)
    return current_file.parent.parent

@dataclass
class CalculatorConfig:
    """
    Calculator configuration settings
    """
    def __init__(
            self,
            base_dir: Optional[Path] = None,
            max_history_size: Optional[int] = None,
            auto_save: Optional[bool] = None,
            precision: Optional[int] = None,
            max_input_value: Optional[Number] = None,
            default_encoding: Optional[str] = None
    ):
        """
        Initialize configuration of environment variables
        """
        project_root = get_project_root()
        self.base_dir = base_dir or Path(
            os.getenv('CALCULATOR_BASE_DIR', str(project_root))
        ).resolve()

        self.max_history_size = max_history_size or int(
            os.getenv('CALCULATOR_MAX_HISTORY_SIZE', '1000')
        )

        auto_save_env = os.getenv('CALCULATOR_AUTO_SAVE', 'true').lower()
        self.auto_save = auto_save if auto_save is not None else (
            auto_save_env == 'true' or auto_save_env == '1'
        )

        self.precision = precision or int(
            os.getenv('CALCULATOR_PRECISION', '10')
        )

        self.max_input_value = max_input_value or Decimal(
            os.getenv('CALCULATOR_MAX_INPUT_VALUE', '1e999')
        )

        self.default_encoding = default_encoding or os.getenv(
            'CALCULATOR_DEFAULT_ENCODING', 'utf-8'
        )

    @property
    def log_dir(self) -> Path:
        """
        get log path
        """
        return Path(os.getenv(
            'CALCULATOR_LOG_DIR',
            str(self.base_dir / "logs")
        )).resolve()
    
    @property
    def history_dir(self) -> Path:
        """
        get history folder path
        """
        return Path(os.getenv(
            'CALCULATOR_HISTORY_DIR',
            str(self.base_dir / "history")
        )).resolve()
    
    @property
    def history_file(self) -> Path:
        """
        get history file path
        """
        return Path(os.getenv(
            'CALCULATOR_HISTORY_FILE',
            str(self.base_dir / "calculator_history.csv")
        )).resolve()
    

    @property
    def log_file(self) -> Path:
        """
        Get log file path for log entries
        """
        return Path(os.getenv(
            'CALCULATOR_LOG_FILE',
            str(self.log_dir / "calculator.log")
        )).resolve()

    def validate(self) -> None:
        """
        Validates configuration settings

        Configuration parameters meet the required criteria.
        Raises:
            ConfigurationError: If any configuration parameter is invalid.
        """
        if self.max_history_size <= 0:
            raise ConfigurationError("max_history_size must be positive")
        if self.precision <= 0:
            raise ConfigurationError("precision must be positive")
        if self.max_input_value <= 0:
            raise ConfigurationError("max_input_value must be positive")
    
    
    
    


