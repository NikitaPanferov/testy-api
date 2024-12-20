from typing import List

from fastapi import HTTPException
from starlette import status

from models import db
from models.question import QuestionTypeEnum
from repositories.abc_repositories import AbstractFormRepository
from repositories.sqlalchemy.form_repository import FormRepository
from schemas.form_schemas import NewForm, QuestionSchema, AnswerSchema, NewQuestion, AnswerToSubmit, SubmitedAnswer


class FormService:
    def __init__(self, form_repo: AbstractFormRepository):
        self.form_repo = form_repo

    async def get_form_by_id(self, test_id: int, user_id: int):
        orm_form = await self.form_repo.get_test_by_id(test_id)
        if not orm_form:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'form with id {test_id} not found'
            )
        await self.__is_open_test(user_id, orm_form.id)
        return self.__orm_to_pydantic([orm_form])[0]

    async def create_form(self, form: NewForm, user_id: int):
        title = form.title
        questions = self.__modify_pydantic(form.questions)
        return await self.form_repo.create_test(title, user_id, questions, False)

    async def get_users_forms(self, user_id: int):
        orm_forms = await self.form_repo.get_tests_by_user_id(user_id)
        return self.__orm_to_pydantic(orm_forms)

    async def submit_form(self, form_id: int, answers: List[AnswerToSubmit], user_id: int):
        await self.__is_open_test(user_id, form_id)
        right_answers = await self.form_repo.get_right_answers(form_id)
        return [SubmitedAnswer(
            questionIndex=answer.questionIndex,
            isRight=set(right_answers[answer.questionIndex]) == set(map(lambda x: x.lower().strip(), answer.answers))
        ) for answer in answers]

    async def delete_form(self, form_id, user_id):
        await self.__is_users_form(user_id, form_id)
        await self.form_repo.delete_form(form_id)

    async def update_form(self, form: NewForm, user_id):
        await self.__is_users_form(user_id, form.id)
        questions = self.__modify_pydantic(form.questions)
        return await self.form_repo.update_test(form.id, form.title, questions)

    async def set_is_open(self, test_id: int, user_id: int, is_open: bool):
        await self.__is_users_form(user_id, test_id)
        return await self.form_repo.set_is_open(test_id, is_open)

    async def __is_users_form(self, user_id: int, form_id: int):
        user = await self.form_repo.get_user_by_test_id(form_id)
        if user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
            )

    async def __is_open_test(self, user_id: int, test_id: int):
        orm_test = await self.form_repo.get_test_by_id(test_id)
        if orm_test.user_id != user_id and not orm_test.is_open:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='test is closed')

    @staticmethod
    def __orm_to_pydantic(orm_forms):
        forms = []
        for orm_form in orm_forms:
            questions = []
            for question in orm_form.questions:
                options = []
                if question.type != QuestionTypeEnum.answer:
                    options = [ans.text for ans in question.answers]

                questions.append(NewQuestion(
                    index=question.number_in_test,
                    type=question.type,
                    name=question.text,
                    description=question.description,
                    options=options,
                ))
            forms.append(NewForm(
                title=orm_form.title,
                questions=questions,
                id=orm_form.id,
                isOpen=orm_form.is_open,
            ))
        return forms

    @staticmethod
    def __modify_pydantic(questions):
        ques = []
        for q in questions:
            if q.type == QuestionTypeEnum.answer:
                answers = [AnswerSchema(text=q.correctAnswers[0], is_correct=True, number_in_question=0)]
            else:
                answers = [AnswerSchema(
                    text=a.lower().strip(),
                    is_correct=a in q.correctAnswers,
                    number_in_question=i + 1,
                ) for i, a in enumerate(q.options)]

            ques.append(QuestionSchema(
                text=q.name,
                description=q.description,
                type=q.type,
                number_in_test=q.index,
                answers=answers
            ))
        return ques


def form_service():
    return FormService(FormRepository(db.session_factory))
