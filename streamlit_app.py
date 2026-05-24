import sys
import os

# add project root safely
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.main import main

if __name__ == "__main__":
    main()
