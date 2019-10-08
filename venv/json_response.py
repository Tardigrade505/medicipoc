import json


class JsonResponse:
    def __init__(self, status_code, headers, body):
        self.status_code = status_code
        self.headers = headers
        self.body = body

    def to_json(self):
        return {"statusCode": self.status_code, "headers": self.headers, "body": json.dumps(self.body)}
