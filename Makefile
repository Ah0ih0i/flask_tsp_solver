all: install

bootstrap:

	echo "Installing Pip"
	sudo apt-get install python-pip
	echo "Installing virtualenv"
	sudo pip install virtualenv

venv:

	virtualenv venv

install: venv

	echo "Installing packages from requirements.txt"
	venv/bin/pip install -r requirements.txt

run:

	venv/bin/python run.py

clean:

	rm *.pyc