import uvicorn

if __name__ == "__main__":
    print("Iniciando servidor...")
    print("Entra desde tu navegador a http://localhost:8000")
    print("Para que otros entren desde la red local, usa la IP de esta máquina.")

    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
