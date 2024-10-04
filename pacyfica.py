from bs4 import BeautifulSoup
import requests
import os


class PacifycaSession:
    login_path = "/login"
   
    def __init__(self, base_url: str, username: str, password: str):
        self.url: str = base_url
        self.username = username
        self.password = password
        self.csrf_token: str | None = None
        self.session = requests.Session()
        self.is_logged_in = False

        
    @staticmethod
    def get_csrf_from_html(html: str) -> str:
        b = BeautifulSoup(html, features="html.parser")
        token = b.find("meta", {"name": "csrf-token"})["content"]
        if token is not None:
            return token
        else:
            raise Exception("couldn't get the csrf token")
        

    def _update_session(self, req) -> requests.models.Response:
        self.session = req.cookies.get("pacifyca_session")
        print("session: ", self.session)

    def request(self, method, url, **kwargs):
        return requests.request(method, url=url, cookies={"pacifyca_session": self.session}, **kwargs)
        
    def login(self, csrf_method="html"):
        # first make an initial get requeset to get the csrf token
        resp = requests.get(self.url)
        if csrf_method == "html":
            self.csrf_token = self.get_csrf_from_html(resp.text)
        else:
            raise NotImplementedError

        login_resp = self.session.request(
            "post", 
            self.url + self.login_path, 
            data=dict(_token=self.csrf_token, 
                        hash="", email=self.username, 
                        password=self.password),
            allow_redirects=False
        )

        if login_resp.status_code == 302:
            self.is_logged_in = True


class PacifycaSessionAloy(PacifycaSession):
    academic_periods_path = "/json/student-dashboard/attendance/get-attendance-academic-periods"
    settings_path = "/json/student-dashboard/attendance/get-settings"
    attendance_path = "/json/student-dashboard/attendance/get-attendance"
    url = "https://online.staloysius.edu.in/"

    def __init__(self, username, password):
        super().__init__(self.url, username, password)


    def _get_academic_periods_json(self) -> dict:
        return self.session.get(f"{self.url}/{self.academic_periods_path}").json()
    
    def _get_attendance_json(self, academic_period_id, student_period_id) -> dict:
        return self.session.get(
            f"{self.url}/{self.attendance_path}", 
            params=dict(
                academic_period_id=academic_period_id, 
                student_period_id=student_period_id)
        ).json()
    
    def end_session(self):
        self.session.close()