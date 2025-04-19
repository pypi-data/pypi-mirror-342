import pytest
from unittest.mock import ANY
import asyncio
import httpx
from httpx import ReadTimeout
from pytest_httpx import HTTPXMock
from d4k_ms_base.service import Service
from d4k_ms_base.logger import application_logger

TEST_URL_1 = "http://d4k.dk/service/version"
TEST_URL_2 = f"{TEST_URL_1}/"

def test_init():
  service = Service(TEST_URL_1)
  assert service.base_url == TEST_URL_1
  assert service._client is not None
  service = Service(TEST_URL_2)
  assert service.base_url == TEST_URL_1

def test__full_url():
  service = Service(TEST_URL_1)
  assert service._full_url("status") == f"{TEST_URL_2}status"
  assert service._full_url("/status") == f"{TEST_URL_2}status"

@pytest.mark.asyncio
async def test_status(httpx_mock: HTTPXMock):
  expected = {'data': "result"}
  httpx_mock.add_response(json=expected)
  service = Service(TEST_URL_1)
  assert await service.status() == expected

@pytest.mark.asyncio
async def test_get(httpx_mock: HTTPXMock):
  expected = {'data': "result"}
  httpx_mock.add_response(json=expected)
  service = Service(TEST_URL_1)
  assert await service.get("get_endpoint") == expected

@pytest.mark.asyncio
async def test_get_error(httpx_mock: HTTPXMock):
  expected = {'error': "Service failed to respond. Error: 'Response text', status: 404"}
  httpx_mock.add_response(text="Response text", status_code=404)
  service = Service(TEST_URL_1)
  assert await service.get("get_endpoint") == expected

@pytest.mark.asyncio
async def test_get_exception(httpx_mock: HTTPXMock, caplog, mocker):
  al = mocker.patch('d4k_ms_base.logger.application_logger.exception')
  expected = {'error': "HTTPX 'GET' operation raised exception ReadTimeout"}
  httpx_mock.add_exception(httpx.ReadTimeout("Unable to read within timeout"))
  service = Service(TEST_URL_1)
  assert await service.get("get_endpoint") == expected
  args, kwargs = al.call_args_list[-1]
  assert args[0] == "HTTPX 'GET' operation raised exception ReadTimeout"
  assert isinstance(args[1], ReadTimeout) == True

@pytest.mark.asyncio
async def test_post(httpx_mock: HTTPXMock):
  httpx_mock.add_response(text='{"result": "good"}', status_code=201)
  service = Service(TEST_URL_1)
  assert await service.post("post_endpoint", data={'send': "data"}) == {"result": "good"}

@pytest.mark.asyncio
async def test_post_200(httpx_mock: HTTPXMock):
  httpx_mock.add_response(text='{"result": "good"}', status_code=200)
  service = Service(TEST_URL_1)
  assert await service.post("post_endpoint", data={'send': "data"}) == {"result": "good"}

@pytest.mark.asyncio
async def test_post_timeout(mocker):
  mock_post = mocker.patch("httpx.AsyncClient.post", return_value=httpx.Response(200,json={"status":"passed"}),)
  service = Service(TEST_URL_1)
  assert await service.post("post_endpoint", data={'send': "data"}, timeout=100) == {'status': 'passed'}
  assert mock_post.call_count == 1
  mock_post.assert_has_calls([mocker.call('http://d4k.dk/service/version/post_endpoint',json={'send': 'data'}, timeout=100)])

@pytest.mark.asyncio
async def test_post_error(httpx_mock: HTTPXMock):
  expected = {'error': "Service failed to respond. Error: 'Response text', status: 500"}
  httpx_mock.add_response(text="Response text", status_code=500)
  service = Service(TEST_URL_1)
  assert await service.post("post_endpoint", data={'send': "data"}) == expected

@pytest.mark.asyncio
async def test_post_exception(httpx_mock: HTTPXMock, caplog, mocker):
  al = mocker.patch('d4k_ms_base.logger.application_logger.exception')
  expected = {'error': "HTTPX 'POST' operation raised exception ReadTimeout"}
  httpx_mock.add_exception(httpx.ReadTimeout("Unable to read within timeout"))
  service = Service(TEST_URL_1)
  assert await service.post("post_endpoint") == expected
  args, kwargs = al.call_args_list[-1]
  assert args[0] == "HTTPX 'POST' operation raised exception ReadTimeout"
  assert isinstance(args[1], ReadTimeout) == True

@pytest.mark.asyncio
async def test_delete(httpx_mock: HTTPXMock):
  httpx_mock.add_response(text='{"result": "good"}', status_code=204)
  service = Service(TEST_URL_1)
  assert await service.delete("delete_endpoint") == {}

@pytest.mark.asyncio
async def test_delete_error(httpx_mock: HTTPXMock):
  expected = {'error': "Service failed to respond. Error: 'Response text', status: 500"}
  httpx_mock.add_response(text="Response text", status_code=500)
  service = Service(TEST_URL_1)
  assert await service.delete("delete_endpoint") == expected

@pytest.mark.asyncio
async def test_delete_exception(httpx_mock: HTTPXMock, caplog, mocker):
  al = mocker.patch('d4k_ms_base.logger.application_logger.exception')
  expected = {'error': "HTTPX 'DELETE' operation raised exception ReadTimeout"}
  httpx_mock.add_exception(httpx.ReadTimeout("Unable to read within timeout"))
  service = Service(TEST_URL_1)
  assert await service.delete("delete_endpoint") == expected
  args, kwargs = al.call_args_list[-1]
  assert args[0] == "HTTPX 'DELETE' operation raised exception ReadTimeout"
  assert isinstance(args[1], ReadTimeout) == True

@pytest.mark.asyncio
async def test_files_no_data(httpx_mock: HTTPXMock):
  httpx_mock.add_response(text='{"result": "good"}', status_code=201)
  service = Service(TEST_URL_1)
  assert await service.file_post("upload_endpoint", files={ 'x': 'data'}) == {"result": "good"}

@pytest.mark.asyncio
async def test_files_with_data(httpx_mock: HTTPXMock):
  httpx_mock.add_response(text='{"result": "good"}', status_code=201)
  service = Service(TEST_URL_1)
  assert await service.file_post("upload_endpoint", files={ 'x': 'data'}, data={'send': "data"}) == {"result": "good"}

@pytest.mark.asyncio
async def test_files_error(httpx_mock: HTTPXMock):
  expected = {'error': "Service failed to respond. Error: 'Response text', status: 500"}
  httpx_mock.add_response(text="Response text", status_code=500)
  service = Service(TEST_URL_1)
  assert await service.file_post("upload_endpoint", files={ 'x': 'data'}) == expected

@pytest.mark.asyncio
async def test_files_exception(httpx_mock: HTTPXMock, caplog, mocker):
  al = mocker.patch('d4k_ms_base.logger.application_logger.exception')
  expected = {'error': "HTTPX 'POST (file)' operation raised exception ReadTimeout"}
  httpx_mock.add_exception(httpx.ReadTimeout("Unable to read within timeout"))
  service = Service(TEST_URL_1)
  assert await service.file_post("upload_endpoint", files={ 'x': 'data'}) == expected
  args, kwargs = al.call_args_list[-1]
  assert args[0] == "HTTPX 'POST (file)' operation raised exception ReadTimeout"
  assert isinstance(args[1], ReadTimeout) == True
