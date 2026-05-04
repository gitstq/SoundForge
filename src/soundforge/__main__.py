"""Allow running SoundForge as `python -m soundforge`."""

from .cli import main
import sys

sys.exit(main())
