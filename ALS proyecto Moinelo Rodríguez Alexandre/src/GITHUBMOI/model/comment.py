import sirope

class Comment:
    def __init__(self, user_email, code_file_id, content):
        self.user_email = user_email
        self.code_file_id = code_file_id
        self.content = content

    def to_dict(self):
        return {
            "user_email": self.user_email,
            "code_file_id": self.code_file_id,
            "content": self.content
        }
