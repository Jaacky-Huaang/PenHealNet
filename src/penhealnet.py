from pentest_module import pentest_module
from remediation_module import remediation_module
import pickle

# the vulnerability information will be stored in lod_dir = "logs1/raw.pkl"
P_agent1 = pentest_module(log_dir="logs1", reasoning_model="gpt-4-turbo", parsing_model="gpt-3.5-turbo", instructor_dir="docs1")
P_agent1.main()
IP1 = P_agent1.extract_IP()

# the vulnerability information will be stored in lod_dir = "logs2/raw.pkl"
P_agent2 = pentest_module(log_dir="logs2", reasoning_model="gpt-4-turbo", parsing_model="gpt-3.5-turbo", instructor_dir="docs2")
P_agent2.main()
IP2 = P_agent2.extract_IP()

# the new vulnerabilities will be stored in logs1/additional.pkl
P_agent1.makeup_pentest(vuln_info_path="logs2/raw.pkl")
# the new vulnerabilities will be stored in logs2/additional.pkl
P_agent2.makeup_pentest(vuln_info_path="logs1/raw.pkl")

# concatenate the vulnerabilities stored in logs1/raw.pkl and logs1/additional.pkl
with open("logs1/raw.pkl", "rb") as f:
    vuln_list1 = pickle.load(f)
with open("logs1/additional.pkl", "rb") as f:
    additional_vuln_list1 = pickle.load(f)
    vuln_list1 += additional_vuln_list1
with open("logs1/vuln_list.pkl", "wb") as f:
    pickle.dump(vuln_list1, f)

# concatenate the vulnerabilities stored in logs2/raw.pkl and logs2/additional.pkl
with open("logs2/raw.pkl", "rb") as f:
    vuln_list2 = pickle.load(f)
with open("logs2/additional.pkl", "rb") as f:
    additional_vuln_list2 = pickle.load(f)
    vuln_list2 += additional_vuln_list2
with open("logs2/vuln_list.pkl", "wb") as f:
    pickle.dump(vuln_list2, f)

R_agent1 = remediation_module(log_dir="logs1", reasoning_model="gpt-4-turbo", parsing_model="gpt-3.5-turbo")
R_agent2 = remediation_module(log_dir="logs2", reasoning_model="gpt-4-turbo", parsing_model="gpt-3.5-turbo")
R_agent1.main()
R_agent2.main()

remediation_list1 = R_agent1.main()
remediation_list2 = R_agent2.main()


# Remediation for the new vulnerabilities
additional_remediation = f"Since vulnerabilities are found in the IP address {IP1} 
you should consider adding firewall rules to block the malicious traffic using this command: 'iptables -A INPUT -s {IP1} -j DROP'"
remediation_list1.append(additional_remediation)

additional_remediation = f"Since vulnerabilities are found in the IP address {IP2} 
you should consider adding firewall rules to block the malicious traffic using this command: 'iptables -A INPUT -s {IP2} -j DROP'"
remediation_list2.append(additional_remediation)





