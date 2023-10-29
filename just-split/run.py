import os

from apps import app

if __name__ == '__main__':
    app.run(debug=os.getenv('DEBUG'),host="0.0.0.0", port=5000)