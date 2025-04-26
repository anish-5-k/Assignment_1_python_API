from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

app = FastAPI()
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

app = FastAPI()

# Simulated DB
assignments_db = []
assignment_id_counter = 1

class AssignmentRequest(BaseModel):
    teacher_id: int
    student_id: int
    lesson_id: int

class AssignmentResponse(BaseModel):
    assignment_id: int
    teacher_id: int
    student_id: int
    lesson_id: int
    status: str
    assigned_at: str
    completed_at: Optional[str] = None

# 1. Assign a lesson to a student
@app.post("/api/assignments", response_model=AssignmentResponse)
def assign_lesson(data: AssignmentRequest):
    global assignment_id_counter
    assignment = {
        "assignment_id": assignment_id_counter,
        "teacher_id": data.teacher_id,
        "student_id": data.student_id,
        "lesson_id": data.lesson_id,
        "status": "incomplete",
        "assigned_at": datetime.utcnow().isoformat(),
        "completed_at": None
    }
    assignments_db.append(assignment)
    assignment_id_counter += 1
    return assignment

# 2. Get a student's incomplete assignments
@app.get("/api/students/{student_id}/assignments", response_model=List[AssignmentResponse])
def get_incomplete_assignments(student_id: int, status: Optional[str] = "incomplete"):
    results = [a for a in assignments_db if a["student_id"] == student_id and a["status"] == status]
    return results

# 3. Student marks an assignment as complete
@app.patch("/api/assignments/{assignment_id}/complete", response_model=AssignmentResponse)
def complete_assignment(assignment_id: int):
    for assignment in assignments_db:
        if assignment["assignment_id"] == assignment_id:
            if assignment["status"] == "complete":
                raise HTTPException(status_code=400, detail="Assignment already completed")
            assignment["status"] = "complete"
            assignment["completed_at"] = datetime.utcnow().isoformat()
            return assignment
    raise HTTPException(status_code=404, detail="Assignment not found")

# 4. Teacher views all assignments they've made
@app.get("/api/teachers/{teacher_id}/assignments", response_model=List[AssignmentResponse])
def get_teacher_assignments(teacher_id: int):
    results = [a for a in assignments_db if a["teacher_id"] == teacher_id]
    return results

# Simulated DB
assignments_db = []
assignment_id_counter = 1

class AssignmentRequest(BaseModel):
    teacher_id: int
    student_id: int
    lesson_id: int

class AssignmentResponse(BaseModel):
    assignment_id: int
    teacher_id: int
    student_id: int
    lesson_id: int
    status: str
    assigned_at: str

@app.post("/api/assignments", response_model=AssignmentResponse)
def assign_lesson(data: AssignmentRequest):
    global assignment_id_counter
    assignment = {
        "assignment_id": assignment_id_counter,
        "teacher_id": data.teacher_id,
        "student_id": data.student_id,
        "lesson_id": data.lesson_id,
        "status": "incomplete",
        "assigned_at": datetime.utcnow().isoformat()
    }
    assignments_db.append(assignment)
    assignment_id_counter += 1
    return assignment
