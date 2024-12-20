from typing import Optional, List

from sqlalchemy import select, delete
from sqlalchemy.orm import joinedload, selectinload

from models import Question, Answer, Form, User, UsersAnswer
from repositories.abc_repositories import AbstractFormRepository
from schemas.form_schemas import QuestionSchema


class FormRepository(AbstractFormRepository):
    def __init__(self, db_session_factory):
        self.db_session_factory = db_session_factory

    async def get_tests_by_user_id(self, user_id: int) -> Optional[List[Form]]:
        async with self.db_session_factory() as session:
            result = await session.execute(
                select(Form)
                .options(joinedload(Form.questions).joinedload(Question.answers))
                .join(Form.user)  # Ассоциация с User
                .where(User.id == user_id)
            )
            return result.unique().scalars().all()

    async def create_test(self, title: str, user_id: int, questions: List[QuestionSchema], is_open: bool) -> int:
        async with self.db_session_factory() as session:
            async with session.begin():
                test = Form(title=title, user_id=user_id, is_open=is_open)
                session.add(test)
                await session.flush()
                await self.__create_questions(questions, session, test.id)
                await session.commit()
        return test.id

    @staticmethod
    async def __create_questions(questions: List[QuestionSchema], session, test_id):
        for q in questions:
            question = Question(
                text=q.text,
                description=q.description,
                type=q.type.value,
                number_in_test=q.number_in_test,
                test_id=test_id,
            )
            session.add(question)
            await session.flush()
            for a in q.answers:
                answer = Answer(
                    text=a.text,
                    is_correct=a.is_correct,
                    number_in_question=a.number_in_question,
                    question_id=question.id
                )
                session.add(answer)

    async def get_test_by_id(self, test_id: int) -> Optional[Form]:
        async with self.db_session_factory() as session:
            result = await session.execute(
                select(Form).where(Form.id == test_id).options(joinedload(Form.questions).joinedload(Question.answers))
            )
            return result.scalars().first()

    async def get_right_answers(self, test_id: int):
        async with self.db_session_factory() as session:
            result = await session.execute(
                select(Form.id, Question.number_in_test, Answer.text).
                join(Question, Form.id == Question.test_id).
                join(Answer, Question.id == Answer.question_id).
                filter(Form.id == test_id, Answer.is_correct.is_(True))
            )
            res = {}
            for _, num, ans in result.all():
                res.setdefault(num, []).append(ans)

            return res

    async def delete_form(self, test_id: int):
        async with self.db_session_factory() as session:
            test = await session.get(Form, test_id)
            if test is not None:
                # Удалить тест и каскадно все связанные объекты
                await session.delete(test)
                # Зафиксировать изменения в базе данных
                await session.commit()

    async def get_user_by_test_id(self, test_id: int) -> User:
        async with self.db_session_factory() as session:
            result = await session.execute(
                select(User)
                .join(User.forms)
                .options(selectinload(User.forms))
                .where(Form.id == test_id)
            )
            return result.unique().scalars().first()

    async def update_test(self, test_id: int, test_title: str, questions: List[QuestionSchema]):
        async with self.db_session_factory() as session:
            question_ids = await session.execute(
                select(Question).where(Question.test_id == test_id)
            )
            question_ids = [q.id for q in question_ids.scalars().all()]

            # Удалить все ответы, связанные с этими вопросами
            await session.execute(
                delete(Answer).where(Answer.question_id.in_(question_ids))
            )

            # Удалить все вопросы этого теста
            await session.execute(
                delete(Question).where(Question.test_id == test_id)
            )

            test = (await session.execute(
                select(Form).where(Form.id == test_id)
            )).scalars().first()

            test.title = test_title
            session.add(test)
            await self.__create_questions(questions, session, test_id)
            await session.commit()
            return test.id

    async def set_is_open(self, test_id: int, is_open: bool) -> int:
        async with self.db_session_factory() as session:
            test = (await session.execute(
                select(Form).where(Form.id == test_id)
            )).scalars().first()
            test.is_open = is_open
            await session.commit()
            return test.id

    async def create_users_answers(self, user_id, answers):
        async with self.db_session_factory() as session:
            for answer in answers:
                session.add(
                    UsersAnswer(
                        question_id=answer.get('question_id'),
                        is_correct=answer.get('is_correct'),
                    )
                )
            await session.commit()
