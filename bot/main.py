"""Entrypoint wrapper for production deployments expecting /bot/main.py."""
from pathlib import Path
import importlib.util

root_bot = Path(__file__).resolve().parents[1] / "bot.py"
spec = importlib.util.spec_from_file_location("root_bot_module", root_bot)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)

if __name__ == '__main__':
    module.main()
