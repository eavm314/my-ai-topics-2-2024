from fastapi import FastAPI

app = FastAPI(title='My first api')


@app.get("/")
def root():
    return {"status": "OK", "message": "Happy student day"}


@app.get("/hello")
def hello(student: str):
    return {"message": f"Hello {student}, nice to meet you!"}


students = []


@app.post("/student", status_code=201)
def create_student(name: str, age: int):
    students.append((name, age))

@app.get("/students")
def get_students():
    return students


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("hello_api:app", reload=True, port=8008)
