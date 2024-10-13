# annotations.py

import pandas as pd
import os

class AnnotationHandler:
    def __init__(self, csv_file='annotations.csv'):
        self.csv_file = csv_file
        self.annotations_df = self.load_annotations()

    def load_annotations(self):
        if os.path.exists(self.csv_file):
            return pd.read_csv(self.csv_file)
        else:
            return pd.DataFrame(columns=[
                'Audio Name', 'File Location', 'Segment Number',
                'Segment Time', 'Class ID', 'Class Name'
            ])

    def save_annotation(self, audio_name, file_location, segment_number, segment_time, class_ids, class_names):
        annotation = {
            'Audio Name': audio_name,
            'File Location': file_location,
            'Segment Number': segment_number,
            'Segment Time': segment_time,
            'Class ID': ','.join(map(str, class_ids)),
            'Class Name': ','.join(class_names)
        }
        idx = self.annotations_df[
            (self.annotations_df['Audio Name'] == audio_name) &
            (self.annotations_df['Segment Number'] == segment_number)
        ].index
        if idx.size > 0:
            # Update existing annotation
            annotation_df = pd.DataFrame([annotation], index=idx)
            self.annotations_df.loc[idx] = annotation_df
        else:
            # Add new annotation using pd.concat
            new_row = pd.DataFrame([annotation])
            self.annotations_df = pd.concat([self.annotations_df, new_row], ignore_index=True)
        self.annotations_df.to_csv(self.csv_file, index=False)

    def get_annotation(self, audio_name, segment_number):
        df = self.annotations_df[
            (self.annotations_df['Audio Name'] == audio_name) &
            (self.annotations_df['Segment Number'] == segment_number)
        ]
        if not df.empty:
            return df.iloc[0]
        else:
            return None

    def get_all_annotations(self):
        return self.annotations_df.to_dict('records')

    def is_audio_annotated(self, audio_name):
        df = self.annotations_df[self.annotations_df['Audio Name'] == audio_name]
        return not df.empty