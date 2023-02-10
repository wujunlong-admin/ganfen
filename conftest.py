import pytest


@pytest.fixture(scope="function", autouse=True)
def my_fixture():
    print('-----前置-----')
    yield
    print('-----后置-----')

# 该方法主要用于处理控制台参数编码问题
def pytest_collection_modifyitems(items):
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")
