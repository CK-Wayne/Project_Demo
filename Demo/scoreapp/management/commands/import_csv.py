from django.core.management.base import BaseCommand
import pandas as pd
from scoreapp.models import User, Item

class Command(BaseCommand):
    help = 'Imports data from a CSV file into User and Item models'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        df = pd.read_csv(csv_file)
        
        for _, row in df.iterrows():
            # 處理 User 數據
            if not pd.isnull(row['user_id']) and not pd.isnull(row['user_anomaly_score']):
                User.objects.update_or_create(
                    user_id=int(row['user_id']),
                    defaults={'anomaly_score': row['user_anomaly_score']}
                )
        
            # 處理 Item 數據
            if not pd.isnull(row['item_id']) and not pd.isnull(row['item_anomaly_score']):
                Item.objects.update_or_create(
                    item_id=int(row['item_id']),
                    defaults={'anomaly_score': row['item_anomaly_score']}
                )
        
        self.stdout.write(self.style.SUCCESS('Successfully imported data from "%s"' % csv_file))