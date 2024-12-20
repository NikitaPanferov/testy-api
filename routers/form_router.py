from typing import Annotated, List

from fastapi import APIRouter, Depends
from starlette import status

from schemas.form_schemas import NewFormRequest, AnswerToSubmit, NewForm, TestIsOpen
from services.form_service import FormService, form_service
from services.user_service import current_user

router = APIRouter(
    prefix='/api/test',
    tags=['test'],
)


@router.get('/{test_id}/')
async def get_test_by_id(test_id: int, user: current_user, tests_service: Annotated[FormService, Depends(form_service)]):
    return await tests_service.get_form_by_id(test_id, user.id)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_test(user: current_user, tests_service: Annotated[FormService, Depends(form_service)], new_test: NewFormRequest):
    test_id = await tests_service.create_form(new_test.test, user.id)
    return {'id': test_id}


@router.get('/')
async def get_user_tests(user: current_user, tests_service: Annotated[FormService, Depends(form_service)]):
    return await tests_service.get_users_forms(user.id)


@router.post('/{test_id}/')
async def submit_test(tests_service: Annotated[FormService, Depends(form_service)], test_id: int, answers: List[AnswerToSubmit], user: current_user):
    return await tests_service.submit_form(test_id, answers, user.id)


@router.delete('/{test_id}/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_test(user: current_user, test_id: int, tests_service: Annotated[FormService, Depends(form_service)]):
    await tests_service.delete_form(test_id, user.id)


@router.put('/', status_code=status.HTTP_200_OK)
async def update_test(user: current_user, test: NewForm, tests_service: Annotated[FormService, Depends(form_service)]):
    test_id = await tests_service.update_form(test, user.id)
    return {'id': test_id}


@router.post('/{test_id}/set_is_open/', status_code=status.HTTP_200_OK)
async def set_is_open(user: current_user, test_id: int, data: TestIsOpen, tests_service: Annotated[FormService, Depends(form_service)]):
    await tests_service.set_is_open(test_id, user.id, data.isOpen)
