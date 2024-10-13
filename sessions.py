# sessions.py

class SessionManager:
    def __init__(self, annotations_df):
        self.annotations_df = annotations_df

    def is_audio_annotated(self, audio_name):
        df = self.annotations_df[self.annotations_df['Audio Name'] == audio_name]
        return not df.empty