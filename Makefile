run:
	python -m streamlit run main.py
install:
	python -m venv myenv
	myenv\Scripts\activate
	pip install -r requirements.txt
source:
	source myenv/bin/activate
