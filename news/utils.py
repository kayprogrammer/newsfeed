from django.utils import timezone
import math

class Util:
    @classmethod
    def sweet_timestamp(date):
        now = timezone.now()
        
        diff = now - date

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds
            
            if seconds < 60:
                return "Just now"
            

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)
            return str(minutes) + " m ago"


        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)
            return str(hours) + " h ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
            return str(days) + " d ago"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)
            return str(months) + " mo ago"


        if diff.days >= 365:
            years= math.floor(diff.days/365)
            return str(years) + " y ago"