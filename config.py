class Language:
    def __init__(self):
        self.language = 'en-US'

    def __str__(self):
        return self.language

    def change(self, lang):
        assert isinstance(lang, str)
        self.language = lang

language = Language()

settings = {
    'TOKEN': 'Nzk2NjkyNjEyMjQ5NjgxOTMw.X_bn0A.gh3PdwFkOgk74dQfFnHERHLCx3Y',
    'NAME_BOT': 'DBOT',
    'ID': '796692612249681930',
    'PREFIX': '-'
}