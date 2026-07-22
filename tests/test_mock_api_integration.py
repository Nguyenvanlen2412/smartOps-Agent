"""End-to-end contract tests: run the real mock_api FastAPI app in a background
thread and drive it through the actual tool implementations (real HTTP calls,
real Pydantic (de)serialization) instead of mocked httpx responses. This is what
catches drift between a tool's expectations and the backend's actual response
shape -- e.g. it caught agent/tools/transaction_tool.py reading fields
(customer, transaction_date, amount) that mock_api never returns.
"""

import os
import socket
import threading
import time

import pytest
import uvicorn

from mock_api.main import app
from agent.tools.order_tool import OrderTool
from agent.tools.ticket_tool import TicketTool
from agent.tools.email_tool import EmailTool
from agent.tools.transaction_tool import check_transaction_status


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture(scope="module")
def live_api_base_url():
    port = _free_port()
    base_url = f"http://127.0.0.1:{port}"
    config = uvicorn.Config(app, host="127.0.0.1", port=port, log_level="warning")
    server = uvicorn.Server(config)
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()

    deadline = time.monotonic() + 10
    while not server.started and time.monotonic() < deadline:
        time.sleep(0.05)
    assert server.started, "mock_api server failed to start within 10s"

    original = {
        "API_BASE_URL": os.environ.get("API_BASE_URL"),
        "MOCK_API_BASE_URL": os.environ.get("MOCK_API_BASE_URL"),
    }
    os.environ["API_BASE_URL"] = base_url
    os.environ["MOCK_API_BASE_URL"] = base_url

    yield base_url

    server.should_exit = True
    thread.join(timeout=5)
    for key, value in original.items():
        if value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = value


class TestOrderToolAgainstLiveApi:

    def test_known_order(self, live_api_base_url):
        tool = OrderTool()
        result = tool._run("VN1024")
        assert "Nguyen Van An" in result
        assert "Status: In Transit" in result

    def test_unknown_order(self, live_api_base_url):
        tool = OrderTool()
        result = tool._run("VN0000")
        assert "couldn't find any information for Order ID 'VN0000'" in result


class TestTicketToolAgainstLiveApi:

    def test_create_ticket(self, live_api_base_url):
        tool = TicketTool()
        result = tool._run(user_id="U00421", issue="Item arrived damaged")
        assert result.startswith("Support ticket TKT-")
        assert result.endswith("for user U00421.")


class TestEmailToolAgainstLiveApi:

    def test_known_user(self, live_api_base_url):
        tool = EmailTool()
        result = tool._run("user_id=U00421; subject=Ticket update; content=We are on it.")
        assert "Email sent to Nguyen Van An (van.an@gmail.com)" in result

    def test_unknown_user(self, live_api_base_url):
        tool = EmailTool()
        result = tool._run("user_id=U99999; subject=Hi; content=Test")
        assert result == "Could not send email: user not found."


class TestTransactionToolAgainstLiveApi:

    def test_known_transaction(self, live_api_base_url):
        result = check_transaction_status("TXN-20250518-00421")
        assert "User ID: U00421" in result
        assert "Status: Success" in result
        assert "Payment Method: VNPay QR" in result
        assert "Amount (VND): 9490000" in result
        assert "Linked Order: VN1024" in result

    def test_unknown_transaction(self, live_api_base_url):
        result = check_transaction_status("TXN-DOES-NOT-EXIST")
        assert "couldn't find any information for Transaction ID 'TXN-DOES-NOT-EXIST'" in result
