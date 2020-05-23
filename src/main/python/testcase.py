import datetime
import json
import copy
# import util
# from testcasecodec import TestCaseDecoder


class TestCaseEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, TestCase):
            dic = {}
            for key, value in o.__dict__.items():
                dic[str(key)]=value
            return dic
        return json.JSONEncoder.default(self, o)


def assign_case(a, b):
    a = copy.deepcopy(b)

class TestCaseDecoder(json.JSONDecoder):
    def decode(self, s):
        dic = super().decode(s)
        return TestCase(
            case_id=dic['case_id'],
            case_name=dic['case_name'],
            case_cat=dic['case_cat'],
            case_mark=dic['case_mark'],
            case_content=dic['case_content'],
            case_req_track=dic['case_req_track'],
            case_qualified_method=dic['case_qualified_method'],
            case_record_data=dic['case_record_data'],
            case_data_analyse=dic['case_data_analyse'],
            case_constraint=dic['case_constraint'],
            case_input=dic['case_input'],
            case_safe_secret=dic['case_safe_secret'],
            case_env=dic['case_env'],
            case_sys_prepare=dic['case_sys_prepare'],
            case_exec_procedure=dic['case_exec_procedure'],
            case_data=dic['case_data'],
            case_problem_sheet=dic['case_problem_sheet'],
            case_correct_sheet=dic['case_correct_sheet'],
            case_diff=dic['case_diff'],
            case_qualified_rule=dic['case_qualified_rule'],
            test_person=dic['test_person'],
            test_join_person=dic['test_join_person'],
            test_date=dic['test_date'],
        )


class TestCase:
    def __init__(self,**kwargs):
        # 以下是测试项定义相关内容，包含部分测试用例和测试报告中的内容
        self.case_id = kwargs['case_id'] if 'case_id' in kwargs else '无'
        self.case_name = kwargs['case_name'] if 'case_name' in kwargs else '无'
        self.case_cat = kwargs['case_cat'] if 'case_cat' in kwargs else 0
        self.case_mark = kwargs['case_mark'] if 'case_mark'in kwargs else '无'
        self.case_content = kwargs['case_content'] if 'case_content'in kwargs else '无'
        self.case_req_track = kwargs['case_req_track'] if 'case_req_track'in kwargs else '无'
        self.case_qualified_method = kwargs['case_qualified_method'] if 'case_qualified_method'in kwargs else 0
        self.case_record_data = kwargs['case_record_data'] if 'case_record_data'in kwargs else '无'
        self.case_data_analyse = kwargs['case_data_analyse'] if 'case_data_analyse'in kwargs else '无'
        self.case_constraint = kwargs['case_constraint'] if 'case_constraint'in kwargs else '无'
        self.case_input = kwargs['case_input'] if 'case_input' in kwargs else '无'
        self.case_safe_secret = kwargs['case_safe_secret'] if 'case_safe_secret'in kwargs else '无'
        self.case_env = kwargs['case_env'] if 'case_env'in kwargs else 0
        self.case_sys_prepare = kwargs['case_sys_prepare'] if 'case_sys_prepare'in kwargs else '无'
        self.case_exec_procedure = kwargs['case_exec_procedure'] if 'case_exec_procedure'in kwargs else []
        self.case_data = kwargs['case_data'] if 'case_data'in kwargs else '无'
        self.case_problem_sheet = kwargs['case_problem_sheet'] if 'case_problem_sheet'in kwargs else '无'
        self.case_correct_sheet = kwargs['case_correct_sheet'] if 'case_correct_sheet'in kwargs else '无'
        self.case_diff = kwargs['case_diff'] if 'case_diff'in kwargs else '无'
        self.case_qualified_rule = kwargs['case_qualified_rule'] if 'case_qualified_rule'in kwargs else '实际结果于预期结果一致'
        self.test_person = kwargs['test_person'] if 'test_person'in kwargs else 0
        self.test_join_person = kwargs['test_join_person'] if 'test_join_person'in kwargs else '无'
        self.test_date = kwargs['test_date'] if 'test_date'in kwargs else datetime.date.today().isoformat()

    def save_to_file(self, file_name):
        try:
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(json.dumps(self, cls=TestCaseEncoder, ensure_ascii=False, indent=2))
        except Exception as e:
            print('保存json文件异常' + str(e))

    def __repr__(self):
        return json.dumps(self, indent=4, ensure_ascii=False,cls=TestCaseEncoder)

    def load_from_file(self, file_name):
        try:
            with open(file_name, 'r', encoding='utf-8') as file:
                load_case = json.load(file, encoding='utf-8', cls=TestCaseDecoder)
                self.case_id = load_case.case_id
                self.case_name = load_case.case_name
                self.case_cat = load_case.case_cat
                self.case_mark = load_case.case_mark
                self.case_content = load_case.case_content
                self.case_req_track = load_case.case_req_track
                self.case_qualified_method = load_case.case_qualified_method
                self.case_record_data = load_case.case_record_data
                self.case_data_analyse = load_case.case_data_analyse
                self.case_constraint = load_case.case_constraint
                self.case_safe_secret = load_case.case_safe_secret
                self.case_env = load_case.case_env
                self.case_sys_prepare = load_case.case_sys_prepare
                self.case_exec_procedure = load_case.case_exec_procedure
                self.case_data = load_case.case_data
                self.case_problem_sheet = load_case.case_problem_sheet
                self.case_correct_sheet = load_case.case_correct_sheet
                self.case_diff = load_case.case_diff
                self.case_qualified_rule = load_case.case_qualified_rule
                self.test_person = load_case.test_person
                self.test_join_person = load_case.test_join_person
                self.test_date = load_case.test_date
        except Exception as e:
            print(f'从{file_name}创建对象失败' + str(e))
            return None