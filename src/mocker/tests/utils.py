def mocked_requests_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code, text, reason):
            self.json_data = json_data
            self.status_code = status_code
            self.text = text
            self.reason = reason

        def json(self):
            return self.json_data

    print("mocked_requests_post args:", args)
    if args[0]:
        return MockResponse(json_data={"key": "value"}, status_code=200, text="good_text", reason="no reason")
    else:
        return MockResponse(json_data={}, status_code=404, text="error", reason="no reason")