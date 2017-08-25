import requests
import json
import logging
from app import app

class SaltAPI():

    def __init__(self, **kwargs):
        self.token = None

        self.salt_host = app.config["SALT_HOST"]
        self.salt_username = app.config["SALT_USER"]
        self.salt_password = app.config["SALT_PASSWORD"]
        ###NEEED TO FIX SO THAT IT USES SSL!!!!!!!!!!!!!
        self.verify_ssl_cert = kwargs.get("verify_ssl_cert", False)

    def login(self):
        req = requests.post(self.salt_host + "/login", data={"eauth": "pam", "username": self.salt_username, "password": self.salt_password}, headers={"Accept": "application/json"}, verify=self.verify_ssl_cert, timeout=5.0)
        if req.status_code != 200:
            print(req.text)
            print(req.status_code)
            print("Signing into salt failed")
        logging.debug("Salt login response: %s - %s", req.status_code, req.text)
        if req.status_code != 200:
            print("Signing into salt failed")
        resp = req.json()
        self.token = resp["return"][0]["token"]
        return self.token

    def logout(self):
        req = requests.post(self.salt_host +"/logout", headers=self._get_headers(), verify = self.verify_ssl_cert)
        return 1

    def _get_headers(self):
        return {"Accept": "application/json", "X-Auth-Token": self.token}

    def checkComms(self):
        req = requests.get(self.salt_host, verify = self.verify_ssl_cert)
        code = req.status_code
        resp = 0
        if code == 200:
            resp = 1 #200 = connection good
        return resp

    def is_minion_reachable(self, minion_id):
        req = requests.post(self.salt_host, data={"client": "local", "tgt": minion_id, "fun": "test.ping"}, headers=self._get_headers(), verify=self.verify_ssl_cert)
        logging.debug("Salt ping response: %s - %s", req.status_code, req.text)
        resp = req.json()

        #if ping succeeds, resp== {'return': [{'minion_name':True}]}
        #if ping fails, resp=={'return':[{}]}

        if resp["return"][0].get(minion_id, None):   #returns true if the minion name can be found in the responce
            return resp["return"][0][minion_id]
        else:
            return False

    def get_minion_grains(self, minion_id):
        #the minion must be online for grains to be checked
        #function will fail if minion is offline
        req = requests.get(self.salt_host + "/minions/" + minion_id, headers=self._get_headers(), verify=self.verify_ssl_cert)
        resp = req.json()
        data = resp["return"][0]
        data2 = data[minion_id]
        return data2


# testing
if __name__ == '__main__':
    api=SaltAPI()
    api.login()
    minion = "rtc-es"
    print(api.is_minion_reachable(minion))
    api.logout()
    print(api.is_minion_reachable(minion))
    print(api.get_minion_grains(minion))
