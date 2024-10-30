import pickle
import os
import time

from src.prompt_class import PromptStore
from src.agent_import import dynamic_import
from group_knapsack import group_knapsack
      
        
class remediation_module:

    def __init__(self, reasoning_model="gpt-4-turbo", parsing_model="gpt-3.5-turbo", log_dir="logs"):

        self.log_dir = log_dir
        
        self.advisor = dynamic_import(reasoning_model)
        self.estimator = dynamic_import(reasoning_model)
        self.extractor = dynamic_import(parsing_model)
        self.cost_evaluator = dynamic_import(reasoning_model)
        self.value_evaluator = dynamic_import(reasoning_model)
        
        self.prompts = PromptStore()
        self.history = {"penheal": [], "console": [], "user": []}

        self.all_paths = []
        self.counterfactual_prompt = ""

        print("Remediation Module initializing")
        # load the paths from the file
        log_path = self.log_dir + "/vuln_list.pkl"
        # save it in the logs folder
        with open(log_path, "rb") as f:
            self.all_paths = pickle.load(f)

    def initialize(self):
        
        (_, self.estimator_session_id) = self.estimator.send_new_message(self.prompts.estimator_prompt)
        (_, self.advisor_session_id) = self.advisor.send_new_message(self.prompts.advisor_session_init)        
        (_, self.extractor_id) = self.extractor.send_new_message(self.prompts.extractor_prompt)

    def main(self):

        # get the cve id for each path
        count = 0
        for path in self.all_paths:
            print(path.get_cve_id())
            time.sleep(1) # sleep for 1 second to avoid rate limiting
            path.summarize(self.extractor, self.extractor_id)
            path.get_info(self.estimator, self.estimator_session_id) # estimate the score for the paths not having a score, look up CVSS score for the paths having a score
            print(path.vul+" "+str(path.cvss_score))
            count += 1

        log_name = "searched.pkl"
        log_path = os.path.join(self.log_dir, log_name)
        with open(log_path, "wb") as f:
            pickle.dump(self.all_paths, f)
                    
        for path in self.all_paths:
            advice = path.get_advice(self.advisor, self.advisor_session_id)
            print("Advice: ")
            print(advice)
            path.advice_list.append(advice)
        
        log_path = "logs/advised.pkl"
        with open(log_path, "wb") as f:
            pickle.dump(self.all_paths, f)

        # load the paths from the file
        with open(log_path, "rb") as f:
            self.all_paths = pickle.load(f)

        # sort the paths based on the base score
        self.all_paths.sort(key=lambda x: x.cvss_score, reverse=True)
        print("Here is the advice for remediation in a decreasing order of severity: ")
        for path in self.all_paths:
            print(path.summary)

        # ask if the use wants to set customized rubrics
        decision = input("Do you want to set customized rubrics for the remediation? (yes/no): ")
        if "y" in decision:
            self.cost_rubrics = input("Enter the cost rubrics: ")
            self.value_rubrics = input("Enter the value rubrics: ")
        else:
            self.cost_rubrics = self.prompts.default_cost_rubrics
            self.value_rubrics = self.prompts.default_value_rubrics

        # get the budget
        decision = input("Do you want to set customized rubrics for the remediation? (yes/no): ")
        if "y" in decision:
            self.budget = int(input("Enter the budget for the remediation: "))
        else:
            self.budget = 4 * len(self.all_paths)
        
        (_, self.cost_evaluator_id) = self.cost_evaluator.send_new_message(self.prompts.cost_evaluator_prompt + self.cost_rubrics)
        (_, self.value_evaluator_id) = self.value_evaluator.send_new_message(self.prompts.value_evaluator_prompt + self.value_rubrics)

        # get the cost and value for each path
        for path in self.all_paths:
            path.get_cost(self.cost_evaluator, self.cost_evaluator_id)
            path.get_value(self.value_evaluator, self.value_evaluator_id)

        # optimize the paths based on the cost and value using knapsack
        groups = []
        for path in self.all_paths:
            cost_value_pairs = []
            for i in range(len(path.cost_list)):
                cost_value_pairs.append((path.advice_list[i], path.cost_list[i], path.value_list[i]))
            groups.append(cost_value_pairs)

        max_value, item_list = group_knapsack(groups, self.budget)
        print("The maximum value achievable is: ", max_value)
        for advice in item_list:
            print(advice)
        
        return item_list
                


if __name__ == "__main__":

    remediation_module = remediation_module(reasoning_model="gpt-4-turbo", parsing_model="gpt-3.5-turbo", log_dir="logs")
    remediation_module.main()
