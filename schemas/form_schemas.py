from typing import List, Optional

from pydantic import BaseModel, Field

from models.question import QuestionTypeEnum


class NewQuestion(BaseModel):
    index: int
    type: QuestionTypeEnum
    name: str
    description: Optional[str] = Field(default="")
    options: Optional[List[str]] = Field(default=[])
    correctAnswers: Optional[List[str]] = Field(default=[])


class NewForm(BaseModel):
    title: str
    questions: List[NewQuestion]
    id: Optional[int] = Field(default=None)
    isOpen: Optional[bool] = True


class NewFormRequest(BaseModel):
    test: NewForm


class AnswerToSubmit(BaseModel):
    questionIndex: int
    answers: List[str]


class SubmitedAnswer(BaseModel):
    questionIndex: int
    isRight: bool


class AnswerSchema(BaseModel):
    text: str
    is_correct: bool
    number_in_question: int


class QuestionSchema(BaseModel):
    text: str
    description: Optional[str]
    type: QuestionTypeEnum
    number_in_test: int
    answers: List[AnswerSchema]


class TestIsOpen(BaseModel):
    isOpen: bool
