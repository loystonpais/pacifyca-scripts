from pacyfica import PacifycaSession, PacifycaSessionAloy
import os
from pprint import pprint

username = os.getenv("PACIFYCA_USERNAME")
password = os.getenv("PACIFYCA_PASSWORD")

if not username or not password:
    raise Exception("Env variables are not set")

pacifyca = PacifycaSessionAloy(username=username, password=password)

pacifyca.login()

#print(pacifyca._get_academic_periods_json())
#print(pacifyca._get_attendance_json(academic_period_id=5, student_period_id=69064))
pprint(pacifyca._get_student_details_json())
#pprint(pacifyca._get_marks_json())
pacifyca.end_session()