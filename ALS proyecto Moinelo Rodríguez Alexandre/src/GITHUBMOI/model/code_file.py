import sirope

class CodeFile:
    def __init__(self, user_email, name, content, language, is_favorite=False, likes=0, is_liked=False):
        self.user_email = user_email
        self.name = name
        self.content = content
        self.language = language
        self.is_favorite = is_favorite
        self.likes = likes
        self.is_liked = is_liked

    def get_safe_id(self, srp: sirope.Sirope) -> str:
        for oid in srp.load_all_keys(CodeFile):
            stored_code_file = srp.load(oid)
            if (stored_code_file and
                    stored_code_file.user_email == self.user_email and
                    stored_code_file.name == self.name and
                    stored_code_file.content == self.content and
                    stored_code_file.language == self.language):
                return srp.safe_from_oid(oid)
        raise ValueError("OID not found for the given object")
