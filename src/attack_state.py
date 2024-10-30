import requests
from cvss import CVSS3
class attackState:
    def __init__(self, attack_plan = "", target = "", prev_command = "", prev_result = ""):
        self.attack_plan = attack_plan
        self.target = target
        self.prev_command = prev_command
        self.prev_result = prev_result

    def __str__(self):
        return f"command: {self.prev_command}, result: {self.prev_result}"

class attackPath:
    def __init__(self, state_list = []):
        self.path = state_list
        # Join the attack_plan  of each state in the state_list
        self.summary = ""
        self.vul = ""
        self.description = ""
        self.vector_string = ""
        self.cvss_score = 0
        self.severity = ""
        self.exploitability_score = 0
        self.impact_score = 0
        self.cve_id = ""
        self.advice_list = []
        self.cost_list = []
        self.value_list = []


    def __str__(self):
        res = f"The target of this attack is: {self.path[0].target}\n"
        for index, state in enumerate(self.path):
            res += f"Step {index + 1}: {str(state)}\n"
        return res

    def get_vul(self,summarizer, session_id):
        prefix = "Please specify the vulnerability used in the path in one line (e.g., CVE-2021-1234 and the name of the backdoor used). \
        If the CVE ID is not available, please write CVE-NA. "
        vul = summarizer.send_message(prefix + str(self), session_id)
        self.vul = vul.split(":")[1].strip()
        return vul
    
    def get_cve_id(self):
        # in this form: CVE-2011-2523 vsFTPd version 2.3.4 backdoor
        self.cve_id = self.vul.split(" ")[0].strip()
        return self.cve_id

    def get_info(self, estimator, session_id):
        if "NA" in self.cve_id:
            res = self.estimate_score(estimator, session_id)
            return res
        else:
            url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={self.cve_id}"
            response = requests.get(url)
            print("response: ", response)
            if response.status_code == 200:
                response = response.json()
                info = response["vulnerabilities"][0]["cve"]
                if info["metrics"].get("cvssMetricV31", None):
                    metrics = info["metrics"]["cvssMetricV31"][0]

                    cvssData = metrics["cvssData"]
                    vector_string = cvssData["vectorString"]
                    cvss_score = cvssData["baseScore"]
                    severity = cvssData["baseSeverity"]
                elif info["metrics"].get("cvssMetricV3", None):
                    metrics = info["metrics"]["cvssMetricV3"][0]

                    cvssData = metrics["cvssData"]
                    vector_string = cvssData["vectorString"]
                    cvss_score = cvssData["baseScore"]
                    severity = cvssData["baseSeverity"]
                else:
                    metrics = info["metrics"]["cvssMetricV2"][0]
                    
                    cvssData = metrics["cvssData"]
                    vector_string = cvssData["vectorString"]
                    cvss_score = cvssData["baseScore"]
                    severity = metrics["baseSeverity"]

                exploitability_score = metrics["exploitabilityScore"]
                impact_score = metrics["impactScore"]
                

                for des in info["descriptions"]:
                    if des["lang"] == "en":
                        description = des["value"]
                
                self.description = description
                self.vector_string = vector_string
                self.cvss_score = cvss_score
                self.severity = severity
                self.exploitability_score = exploitability_score
                self.impact_score = impact_score
                return description, vector_string, cvss_score, severity, exploitability_score, impact_score
                
            else:
                return "Failed to retrieve data from NVD."

    def get_advice(self, advisor, advisor_session_id):
        info = f"Description: {self.description}\nBase Score: {self.cvss_score}\n"
        info += f"Here is the summary of the path used to exploit the vulnerability: {self.summary}"
        info += "Please give me some advice on remediation."
        self.advice = advisor.send_message(info, advisor_session_id)
        return self.advice

    def get_all_info(self):
        self.get_vul()
        self.get_cve_id()
        self.get_info()
        self.summarize()
        self.get_advice()

    def get_command_list(self):
        command_list = []
        for state in self.path:
            if state.prev_command:
                command_list.append(state.prev_command)
        return command_list

    def summarize(self, summarizer, session_id):
        # summarize the path
        prefix = "Here is the path for you to summarize: "
        summary = summarizer.send_message(prefix + str(self), session_id)
        self.summary = summary
        return summary
    
    def estimate_score(self, estimator, session_id):
        res = estimator.send_message(self.summary, session_id)
        # get the cvss score using the descriptor
        self.cvss_score = float(CVSS3(res)[0])
        return res

    def get_cost(self, cost_evaluator, cost_evaluator_id):
        content = f"Please evaluate the cost of the following advice: {self.advice}"
        content += f"\nThe background of the attack is: {self.summary}"
        res = cost_evaluator.send_message(content, cost_evaluator_id)
        for advice in range(self.advice_list):
            res = cost_evaluator.send_message(advice, cost_evaluator_id)
            self.cost_list.append(float(res))
        return res
    
    def get_value(self, value_evaluator, value_evaluator_id):
        content = f"Please evaluate the value of the following advice: {self.advice}"
        content += f"\nThe background of the attack is: {self.summary}"
        res = value_evaluator.send_message(content, value_evaluator_id)
        for advice in range(self.advice_list):
            res = value_evaluator.send_message(advice, value_evaluator_id)
            self.value_list.append(float(res))
        return res

