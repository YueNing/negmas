
# if __name__ == "__main__":
import sys
sys.path.insert(0,'z:/negmas/')
sys.path.insert(0,'z:/negmas/negmas/apps/scml/src/scml')
from negmas.gui.app import app

if __name__ == "__main__":
    app.run_server(debug=True)