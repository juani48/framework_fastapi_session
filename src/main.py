from web import app
import uvicorn

if __name__ == "__main__":
	# Ejecutar con: python -m src.main
	# uvicorn main:app --reload
	uvicorn.run("src.web:app", host="127.0.0.1", port=8000, reload=False)