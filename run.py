# create this app as a package
from flaskblog import create_app
# app variable need to exist in __init__.py file under flaskblog folder

app = create_app()

if __name__ == '__main__':
	app.run(debug=True)   #as long as import, app run debug mode

