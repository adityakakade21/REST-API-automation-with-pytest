import pytest

@pytest.fixture(scope="class")
def setup(request):

    url = 'https://gorest.co.in/public-api/users/'

    key = 'a2608d81deefb9d45d2ddef0f4365dc82deca66c52a74c8896ee9a20f21407b2'

    header = {'Content-Type': 'application/json'}

    request.cls.url = url
    request.cls.key = key
    request.cls.header = header

