from api.app import create_app
from api.config.config import config_dict

<<<<<<< HEAD
# app = create_app(config=config_dict['prod'])
=======
>>>>>>> 20516bdc5ec9b4448244fdb4d9c39ba79f78a175
app = create_app()

if __name__=="__main__":
    app.run(debug=True)