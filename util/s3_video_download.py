""" This file is used to download course videos from S3 bucket. """
import boto3
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('--csv-file', type=str, required=True)

class S3VideoDownload:
    """ This class is used to download course videos from S3 bucket. """

    def __init__(self, csv_file):
        """ Initialize the class. """
        self.csv_file_name = csv_file
        self.s3_client = boto3.client('s3')
        self.bucket_name = 'edx-video-bucket'
        self.file_prefix = 'prod-edx/unprocessed/'
        self.files_dict = {}

    def check_file_exists(self, video_id):
        """ Check if file exists in S3 bucket. """
        try:
            self.s3_client.get_object(Bucket=self.bucket_name, Key=self.file_prefix + video_id)
            return True
        except Exception as e:
            print(e)
            return False

    def csv_to_dict(self, ):
        """ Convert csv file to dictionary. """
        with open(self.csv_file_name, 'r') as csv_file:
            for line in csv_file:
                line = line.strip()
                video_id, course_id, video_title, video_source = line.split(',')
                if self.check_file_exists(video_id):
                    self.files_dict[video_id] = {
                        'course_id': course_id,
                        'video_title': video_title,
                        'video_source': video_source
                    }
                else:
                    print(f"File does not exist: \n \
                        video_id: {video_id} \n \
                        course_id: {course_id} \n \
                        video_title: {video_title}")

    def download_videos(self):
        """ Download videos from S3 bucket. """
        for video_id, video_info in self.files_dict.items():
            self.s3_client.download_file(self.bucket_name, self.file_prefix + video_id, video_id)
            print(f"Downloaded: {video_id}")

    def run(self):
        """ Run the class. """
        self.csv_to_dict()
        self.download_videos()


if __name__ == '__main__':
    args = parser.parse_args()
    s3_video_download = S3VideoDownload(args.csv_file)
    s3_video_download.run()