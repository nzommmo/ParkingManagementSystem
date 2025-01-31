# Generated by Django 5.1.5 on 2025-01-31 19:06

from django.db import migrations, models
from django.db.models import F
from django.db.models.functions import Extract

class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0009_alter_ticket_assigned_to'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='stay_duration',
            field=models.DurationField(null=True, blank=True),
        ),
        migrations.RunSQL(
            sql="""
            CREATE TRIGGER update_ticket_stay_duration
            AFTER UPDATE OF end_time ON tickets_ticket
            FOR EACH ROW
            BEGIN
                UPDATE tickets_ticket 
                SET stay_duration = 
                    CASE 
                        WHEN NEW.end_time IS NOT NULL 
                        THEN (julianday(NEW.end_time) - julianday(NEW.start_time)) * 86400.0
                        ELSE NULL 
                    END
                WHERE rowid = NEW.rowid;
            END;
            """,
            reverse_sql="DROP TRIGGER IF EXISTS update_ticket_stay_duration;"
        ),
        migrations.RunSQL(
            sql="""
            CREATE TRIGGER update_ticket_stay_duration_insert
            AFTER INSERT ON tickets_ticket
            FOR EACH ROW
            BEGIN
                UPDATE tickets_ticket 
                SET stay_duration = 
                    CASE 
                        WHEN NEW.end_time IS NOT NULL 
                        THEN (julianday(NEW.end_time) - julianday(NEW.start_time)) * 86400.0
                        ELSE NULL 
                    END
                WHERE rowid = NEW.rowid;
            END;
            """,
            reverse_sql="DROP TRIGGER IF EXISTS update_ticket_stay_duration_insert;"
        )
    ]