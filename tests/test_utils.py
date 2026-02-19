from http import HTTPStatus
from unittest.mock import Mock, patch

import pytest
from src.controllers.utils import eleva_quadrado, requires_role


@pytest.mark.parametrize("test_input,expected", [(2, 4), (10, 100), (3, 9), (1.4,1.9599999999999997)])
def test_eleva_quadrado_sucesso(test_input, expected):
    resultado = eleva_quadrado(test_input)
    assert resultado == expected

@pytest.mark.parametrize("test_input,exc_class, msg",
    [
        ('a', TypeError, "unsupported operand type(s) for ** or pow(): 'str' and 'int'"),
        (None, TypeError, "unsupported operand type(s) for ** or pow(): 'NoneType' and 'int'"),
    ]
)
def test_eleva_quadrado_falha(test_input,exc_class, msg):
    with pytest.raises(exc_class) as exc:
        eleva_quadrado(test_input)
    assert str(exc.value) == msg

def test_requires_role_sucess():
    mock_user = Mock()
    mock_user.role.name = 'admin'
    mock_get_jwt_identity = patch('src.controllers.utils.get_jwt_identity')
    mock_db_get_or_404 = patch('src.controllers.utils.db.session.get', return_value=mock_user)

    mock_get_jwt_identity.start()
    mock_db_get_or_404.start()

    decorated_function = requires_role('admin')(lambda: 'Sucess')

    result = decorated_function()

    assert result == 'Sucess'

    mock_get_jwt_identity.stop()
    mock_db_get_or_404.stop()

def test_requires_role_fail():
    mock_user = Mock()
    mock_user.role.name = 'normal'
    mock_get_jwt_identity = patch('src.controllers.utils.get_jwt_identity')
    mock_db_get_or_404 = patch('src.controllers.utils.db.session.get', return_value=mock_user)

    mock_get_jwt_identity.start()
    mock_db_get_or_404.start()

    decorated_function = requires_role('admin')(lambda: 'Sucess')


    result = decorated_function()
    assert result == ({'message': 'Required role: admin'}, HTTPStatus.FORBIDDEN)

    mock_get_jwt_identity.stop()
    mock_db_get_or_404.stop()