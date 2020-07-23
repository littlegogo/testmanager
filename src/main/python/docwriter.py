import datetime
import win32com
from win32com.client import Dispatch, constants

PLAN_DOC = f'配置项测试计划({datetime.date.today().isoformat()}).doc'
SPEC_DOC = f'配置项测试说明({datetime.date.today().isoformat()}).doc'
REPORT_DOC = f'配置项测试报告({datetime.date.today().isoformat()}).doc'

TEST_CAT_KEY = 'test_category'
TEST_PERSON_KEY = 'test_persons'
TEST_ENV_KEY = 'test_environment'
TEST_REQ_METHOD_KEY = 'qualified_method'

class DocWriter:
    """
    office word 写入工具类
    """
    def __init__(self, keys, test_cases, config, write_dir):
        self.keys = keys
        self.test_cases = test_cases
        self.config = config
        self.plan_doc_table_heads = ['序号', '测试项', '测试类别', '测试标识', '测试内容', '需求追溯', '合格方法', '记录数据',
                       '数据分析类型', '假设约束', '安全保密', '测试环境']
        # 存储文档名称
        self.plan_doc_name = write_dir + f'/{PLAN_DOC}'
        self.spec_doc_name = write_dir + f'/{SPEC_DOC}'
        self.report_doc_name = write_dir + f'/{REPORT_DOC}                               '

        # 初始化word
        self.word_app = win32com.client.gencache.EnsureDispatch('Word.Application')
        self.word_app.Visible = True
        self.word_app.DisplayAlerts = 0

        # 创建3个文档
        self.plan_doc = self.word_app.Documents.Add()
        self.spec_doc = self.word_app.Documents.Add()
        self.report_doc = self.word_app.Documents.Add()
        self.word_app.CaptionLabels.Add('表')  # 增加一个标签
        # 初始化测试计划中的测试项定义表
        self.__create_plan_table()
        self.report_doc.PageSetup.Orientation = constants.wdOrientLandscape

    def __create_plan_table(self):
        """
        创建测试计划中的测试项定义表格
        :return:
        """
        table_heading_pha = self.plan_doc.Paragraphs.Add()
        table_heading_pha.LineSpacing = 1.5*12
        table_heading_pha.Alignment = constants.wdAlignParagraphCenter
        table_heading_pha.Range.Font.Size = 12
        table_heading_pha.Range.Font.Name = '黑体'
        table_heading_pha.Range.InsertCaption("表", '', '', constants.wdCaptionPositionAbove)
        table_heading_pha.Range.InsertBefore('测试项定义')
        table_heading_pha.Range.Select()
        self.word_app.Selection.PageSetup.Orientation = constants.wdOrientLandscape
        table_pha = self.plan_doc.Paragraphs.Add()
        # 输出属性表格 共12列 外边框1.5磅
        var_table = table_pha.Range.Tables.Add(table_pha.Range, len(self.keys) + 1, 12)
        # 设置表头
        for index, value in enumerate(self.plan_doc_table_heads):
            var_table.Cell(1, index+1).Range.Text = self.plan_doc_table_heads[index]
        # 暂不设置每列的宽度
        # var_table.Columns(1).SetWidth(4*28.35, 0)  # 1cm = 28.35磅
        # var_table.Columns(2).SetWidth(4*28.35, 0)  # 1cm = 28.35磅
        # var_table.Columns(3).SetWidth(6.5*28.35, 0)  # 1cm = 28.35磅

        var_table.Borders.Enable = True
        self.__set_table_border(var_table, constants.wdLineWidth150pt, constants.wdLineWidth150pt,
                               constants.wdLineWidth150pt, constants.wdLineWidth150pt)
        # for index, var in enumerate(var_list):
        #     var_table.Cell(index + 2, 1).Range.Text = var[1]
        #     var_table.Cell(index + 2, 2).Range.Text = var[0]
        #     var_table.Cell(index + 2, 3).Range.Text = var[2]
        # var_table.Range.Select()
        var_table.Range.Font.Name = '宋体'
        var_table.Range.Font.Name = 'Times New Roman'
        var_table.Rows(1).Range.Font.Name = '黑体'
        var_table.Select()
        self.word_app.Selection.Tables(1).Rows.Alignment = constants.wdAlignRowCenter
        # 删除题注末尾的换行符
        var_table.Select()
        ref = self.word_app.Selection.Previous(constants.wdParagraph, 2)
        ref.Select()
        self.word_app.Selection.Find.Execute(FindText='^p', ReplaceWith=' ', Replace=constants.wdReplaceOne)
        table_heading_pha.Range.Font.Size = 12
        table_heading_pha.Range.Font.Name = '黑体'

    def __init_sepc_doc(self):
        """
        初始化测试说明文档
        :return:
        """
        test_case_title = self.spec_doc.Paragraphs.Add()
        test_case_title.Range.InsertBefore('测试用例')
        test_case_title.Style = self._get_title_(1)


    def __init_report_doc(self):
        """
        初始化测试报告文档
        :return:
        """
        test_result_title = self.report_doc.Paragraphs.Add()
        test_result_title.Range.InsertBefore('测试结果')
        test_result_title.Style = self._get_title_(1)


    def __set_table_border(self, table, left, top, right, bottom):
        """
        设置表格边框线宽
        :param left: 左边框宽度
        :param top: 上边框宽度
        :param right: 右边框宽度
        :param botton: 下边框宽度
        :return: 无
        """
        table.Borders(constants.wdBorderLeft).LineWidth = left
        table.Borders(constants.wdBorderTop).LineWidth = top
        table.Borders(constants.wdBorderRight).LineWidth = right
        table.Borders(constants.wdBorderBottom).LineWidth = bottom

    def __write_plan_doc_table(self, row, test_case):
        plan_doc_table = self.plan_doc.Tables(1)
        plan_doc_table.Cell(row, 1).Range.Text = str(row-1)
        plan_doc_table.Cell(row, 2).Range.Text = test_case.case_name
        plan_doc_table.Cell(row, 3).Range.Text = self.config[TEST_CAT_KEY][test_case.case_cat]
        plan_doc_table.Cell(row, 4).Range.Text = test_case.case_mark
        plan_doc_table.Cell(row, 5).Range.Text = test_case.case_content
        plan_doc_table.Cell(row, 6).Range.Text = test_case.case_req_track
        plan_doc_table.Cell(row, 7).Range.Text = self.config[TEST_REQ_METHOD_KEY][test_case.case_qualified_method]
        plan_doc_table.Cell(row, 8).Range.Text = test_case.case_data
        plan_doc_table.Cell(row, 9).Range.Text = test_case.case_data_analyse
        plan_doc_table.Cell(row, 10).Range.Text = test_case.case_constraint
        plan_doc_table.Cell(row, 11).Range.Text = test_case.case_safe_secret
        plan_doc_table.Cell(row, 12).Range.Text = self.config[TEST_ENV_KEY][test_case.case_env]

    def __write_spec_doc(self, test_case):
        # test_case = TestCase()
        # 输出用例的标题
        case_title = self.spec_doc.Paragraphs.Add()
        case_title.Range.InsertBefore(f'{test_case.case_name}({test_case.case_mark})')
        # var_heading_pha.Range.Select()
        case_title.Style = self.__get_title_(2)
        # 输出表题
        table_heading_pha = self.spec_doc.Paragraphs.Add()
        table_heading_pha.LineSpacing = 1.5*12
        table_heading_pha.Alignment = constants.wdAlignParagraphCenter
        table_heading_pha.Range.InsertCaption("表", '', '', constants.wdCaptionPositionAbove)
        table_heading_pha.Range.InsertBefore(f'{test_case.case_name}')
        # 输出表格
        table_pha = self.spec_doc.Paragraphs.Add()
        # 输出属性表格外边框1.5磅
        case_table = table_pha.Range.Tables.Add(table_pha.Range, 8+len(test_case.case_exec_procedure), 6)
        # 合并单元格并填充内容
        case_table.Cell(2, 2).Merge(case_table.Cell(2, 6))
        case_table.Cell(3, 2).Merge(case_table.Cell(3, 6))
        case_table.Cell(4, 2).Merge(case_table.Cell(4, 6))
        case_table.Cell(5, 2).Merge(case_table.Cell(5, 6))
        case_table.Cell(6, 2).Merge(case_table.Cell(6, 6))
        case_table.Cell(6, 2).Split(1, 2)
        for i in range(7, 7+len(test_case.case_exec_procedure)):
            case_table.Cell(i, 2).Merge(case_table.Cell(i, 6))
            case_table.Cell(i, 2).Split(1, 2)
            # 在合并遍历的同时设置表格内容，减少一次遍历
            case_table.Cell(i, 1).Range.Text = test_case.case_exec_procedure[i-7][0]
            case_table.Cell(i, 2).Range.Text = test_case.case_exec_procedure[i-7][1]
            case_table.Cell(i, 3).Range.Text = test_case.case_exec_procedure[i-7][2]

        case_table.Cell(7 + len(test_case.case_exec_procedure), 2).Merge(case_table.Cell(7 + len(test_case.case_exec_procedure), 6))
        case_table.Cell(8 + len(test_case.case_exec_procedure), 2).Merge(case_table.Cell(8 + len(test_case.case_exec_procedure), 6))
        # 设置表格内容
        case_table.Cell(1, 1).Range.Text = '测试用例'
        case_table.Cell(1, 3).Range.Text = '测试类别'
        case_table.Cell(1, 5).Range.Text = '需求追溯'
        case_table.Cell(2, 1).Range.Text = '测试内容'
        case_table.Cell(3, 1).Range.Text = '系统准备'
        case_table.Cell(4, 1).Range.Text = '前提约束'
        case_table.Cell(5, 1).Range.Text = '测试输入'
        case_table.Cell(6, 1).Range.Text = '序号'
        case_table.Cell(6, 2).Range.Text = '测试步骤'
        case_table.Cell(6, 3).Range.Text = '预期结果'
        case_table.Cell(7 + len(test_case.case_exec_procedure), 1).Range.Text = '评估准则'
        case_table.Cell(8 + len(test_case.case_exec_procedure), 1).Range.Text = '测试环境'

        case_table.Cell(1, 2).Range.Text = test_case.case_mark
        case_table.Cell(1, 4).Range.Text = self.config[TEST_CAT_KEY][test_case.case_cat]
        case_table.Cell(1, 6).Range.Text = test_case.case_req_track
        case_table.Cell(2, 2).Range.Text = test_case.case_content
        case_table.Cell(3, 2).Range.Text = test_case.case_sys_prepare
        case_table.Cell(4, 2).Range.Text = test_case.case_constraint
        case_table.Cell(5, 2).Range.Text = test_case.case_input
        case_table.Cell(7 + len(test_case.case_exec_procedure), 2).Range.Text = test_case.case_qualified_rule
        case_table.Cell(8 + len(test_case.case_exec_procedure), 2).Range.Text = self.config[TEST_ENV_KEY][test_case.case_env]

        # 设置表格样式及字体
        case_table.Borders.Enable = True
        self.__set_table_border(case_table, constants.wdLineWidth150pt, constants.wdLineWidth150pt,
                               constants.wdLineWidth150pt, constants.wdLineWidth150pt)
        # 先同一刷
        case_table.Range.Font.Name = '宋体'
        case_table.Range.Font.Name = 'Times New Roman'
        # 设置黑体
        case_table.Cell(1, 1).Range.Font.Name = '黑体'
        case_table.Cell(1, 3).Range.Font.Name = '黑体'
        case_table.Cell(1, 5).Range.Font.Name = '黑体'
        case_table.Cell(2, 1).Range.Font.Name = '黑体'
        case_table.Cell(3, 1).Range.Font.Name = '黑体'
        case_table.Cell(4, 1).Range.Font.Name = '黑体'
        case_table.Cell(5, 1).Range.Font.Name = '黑体'
        case_table.Cell(6, 1).Range.Font.Name = '黑体'
        case_table.Cell(6, 2).Range.Font.Name = '黑体'
        case_table.Cell(6, 3).Range.Font.Name = '黑体'
        case_table.Cell(7 + len(test_case.case_exec_procedure), 1).Range.Font.Name = '黑体'
        case_table.Cell(8 + len(test_case.case_exec_procedure), 1).Range.Font.Name = '黑体'
        # 设置文本对齐
        # case_table.Select()
        # self.word_app.Selection.Tables(1).Rows.Alignment = constants.wdAlignRowCenter
        # 删除题注末尾的换行符及表格说明字体
        case_table.Select()
        ref = self.word_app.Selection.Previous(constants.wdParagraph, 2)
        ref.Select()
        self.word_app.Selection.Find.Execute(FindText='^p', ReplaceWith=' ', Replace=constants.wdReplaceOne)
        table_heading_pha.Range.Font.Size = 12
        table_heading_pha.Range.Font.Name = '黑体'


    def __write_result(self, result_list):
        # 输出用例的标题
        result_title = self.report_doc.Paragraphs.Add()
        result_title.Range.InsertBefore('测试结果统计')
        # var_heading_pha.Range.Select()
        result_title.Style = self.__get_title_(2)
        # 输出表题
        table_heading_pha = self.report_doc.Paragraphs.Add()
        table_heading_pha.LineSpacing = 1.5*12
        table_heading_pha.Alignment = constants.wdAlignParagraphCenter
        table_heading_pha.Range.InsertCaption("表", '', '', constants.wdCaptionPositionAbove)
        table_heading_pha.Range.InsertBefore('测试结果统计')
        # 输出表格
        table_pha = self.report_doc.Paragraphs.Add()
        # 输出属性表格外边框1.5磅
        result_table = table_pha.Range.Tables.Add(table_pha.Range, 1+len(result_list), 4)

        # # 设置表格内容
        result_table.Cell(1, 1).Range.Text = '序号'
        result_table.Cell(1, 2).Range.Text = '用例名称'
        result_table.Cell(1, 3).Range.Text = '用例标识'
        result_table.Cell(1, 4).Range.Text = '测试结果'

        for index, item in enumerate(result_list):
            result_table.Cell(index + 2, 1).Range.Text = str(index + 1)
            result_table.Cell(index + 2, 2).Range.Text = item[0]
            result_table.Cell(index + 2, 3).Range.Text = item[1]
            result_table.Cell(index + 2, 4).Range.Text = '通过'

        # 设置表格样式及字体
        result_table.Borders.Enable = True
        self.__set_table_border(result_table, constants.wdLineWidth150pt, constants.wdLineWidth150pt,
                               constants.wdLineWidth150pt, constants.wdLineWidth150pt)
        # 先统一刷
        result_table.Range.Font.Name = '宋体'
        result_table.Range.Font.Name = 'Times New Roman'
        # 设置黑体
        result_table.Cell(1, 1).Range.Font.Name = '黑体'
        result_table.Cell(1, 2).Range.Font.Name = '黑体'
        result_table.Cell(1, 3).Range.Font.Name = '黑体'
        result_table.Cell(1, 4).Range.Font.Name = '黑体'
        
        # 设置文本对齐
        # case_table.Select()
        # self.word_app.Selection.Tables(1).Rows.Alignment = constants.wdAlignRowCenter
        # 删除题注末尾的换行符及表格说明字体
        result_table.Select()
        ref = self.word_app.Selection.Previous(constants.wdParagraph, 2)
        ref.Select()
        self.word_app.Selection.Find.Execute(FindText='^p', ReplaceWith=' ', Replace=constants.wdReplaceOne)
        table_heading_pha.Range.Font.Size = 12
        table_heading_pha.Range.Font.Name = '黑体'

    def __write_report_doc(self, test_case):
            # 输出用例的标题
        # test_case = TestCase()
        case_title = self.report_doc.Paragraphs.Add()
        case_title.Range.InsertBefore(f'{test_case.case_name}({test_case.case_mark})')
        # var_heading_pha.Range.Select()
        case_title.Style = self.__get_title_(2)
        # 输出表题
        table_heading_pha = self.report_doc.Paragraphs.Add()
        table_heading_pha.LineSpacing = 1.5*12
        table_heading_pha.Alignment = constants.wdAlignParagraphCenter
        table_heading_pha.Range.InsertCaption("表", '', '', constants.wdCaptionPositionAbove)
        table_heading_pha.Range.InsertBefore(f'{test_case.case_name}')
        # 输出表格
        table_pha = self.report_doc.Paragraphs.Add()
        # 输出属性表格外边框1.5磅
        case_table = table_pha.Range.Tables.Add(table_pha.Range, 10+len(test_case.case_exec_procedure), 13)
        # 合并单元格并填充内容
        # 用例标识行
        case_table.Cell(1, 2).Merge(case_table.Cell(1, 4))
        case_table.Cell(1, 4).Merge(case_table.Cell(1, 6))
        case_table.Cell(1, 6).Merge(case_table.Cell(1, 9))
        # # 测试人员行
        case_table.Cell(2, 2).Merge(case_table.Cell(2, 4))
        case_table.Cell(2, 4).Merge(case_table.Cell(2, 11))
        # # 系统准备行
        case_table.Cell(3, 2).Merge(case_table.Cell(3, 13))
        # 前提约束行
        case_table.Cell(4, 2).Merge(case_table.Cell(4, 13))
        # 测试输入行
        case_table.Cell(5, 2).Merge(case_table.Cell(5, 13))
        # 测试步骤标题行
        case_table.Cell(6, 2).Merge(case_table.Cell(6, 4))
        case_table.Cell(6, 3).Merge(case_table.Cell(6, 5))
        case_table.Cell(6, 4).Merge(case_table.Cell(6, 6))
        case_table.Cell(6, 5).Merge(case_table.Cell(6, 6))
        # 测试结果行,同步填入数据避免再次循环
        procedure_len = len(test_case.case_exec_procedure)
        for i in range(7, 7+procedure_len):
            case_table.Cell(i, 2).Merge(case_table.Cell(i, 4))
            case_table.Cell(i, 3).Merge(case_table.Cell(i, 5))
            case_table.Cell(i, 4).Merge(case_table.Cell(i, 6))
            case_table.Cell(i, 5).Merge(case_table.Cell(i, 6))

            case_table.Cell(i, 1).Range.Text = test_case.case_exec_procedure[i-7][0]
            case_table.Cell(i, 2).Range.Text = test_case.case_exec_procedure[i-7][1]
            case_table.Cell(i, 3).Range.Text = test_case.case_exec_procedure[i-7][2]
            case_table.Cell(i, 4).Range.Text = test_case.case_exec_procedure[i-7][3]
            case_table.Cell(i, 5).Range.Text = test_case.case_exec_procedure[i-7][4]
            case_table.Cell(i, 6).Range.Text = test_case.case_exec_procedure[i-7][5]
        # 测试数据行
        case_table.Cell(7 + procedure_len, 2).Merge(case_table.Cell(7 + procedure_len, 4))
        case_table.Cell(7 + procedure_len, 4).Merge(case_table.Cell(7 + procedure_len, 5))
        case_table.Cell(7 + procedure_len, 6).Merge(case_table.Cell(7 + procedure_len, 10))
        # 测试差异行
        case_table.Cell(8 + procedure_len, 2).Merge(case_table.Cell(8 + procedure_len, 13))
        # 评估准则行
        case_table.Cell(9 + procedure_len, 2).Merge(case_table.Cell(9 + procedure_len, 13))
        # 测试环境行
        case_table.Cell(10 + procedure_len, 2).Merge(case_table.Cell(10 + procedure_len, 13))

        # # 设置表格内容
        case_table.Cell(1, 1).Range.Text = '用例标识'
        case_table.Cell(1, 2).Range.Text = test_case.case_mark
        case_table.Cell(1, 3).Range.Text = '测试类别'
        case_table.Cell(1, 4).Range.Text = self.config[TEST_CAT_KEY][test_case.case_cat]
        case_table.Cell(1, 5).Range.Text = '测试时间'
        case_table.Cell(1, 6).Range.Text = test_case.test_date

        case_table.Cell(2, 1).Range.Text = '测试人员'
        case_table.Cell(2, 2).Range.Text = self.config[TEST_PERSON_KEY][test_case.test_person]
        case_table.Cell(2, 3).Range.Text = '参与人员'
        case_table.Cell(2, 4).Range.Text = test_case.test_join_person

        case_table.Cell(3, 1).Range.Text = '系统准备'
        case_table.Cell(3, 2).Range.Text = test_case.case_sys_prepare

        case_table.Cell(4, 1).Range.Text = '前提约束'
        case_table.Cell(4, 2).Range.Text = test_case.case_constraint

        case_table.Cell(5, 1).Range.Text = '测试输入'
        case_table.Cell(5, 2).Range.Text = test_case.case_input

        case_table.Cell(6, 1).Range.Text = '序号'
        case_table.Cell(6, 2).Range.Text = '测试步骤'
        case_table.Cell(6, 3).Range.Text = '预期结果'
        case_table.Cell(6, 4).Range.Text = '测试结果'
        case_table.Cell(6, 5).Range.Text = '问题描述'
        case_table.Cell(6, 6).Range.Text = '数据分析'

        case_table.Cell(7 + procedure_len, 1).Range.Text = '测试数据'
        case_table.Cell(7 + procedure_len, 2).Range.Text = test_case.case_data
        case_table.Cell(7 + procedure_len, 3).Range.Text = '问题单'
        case_table.Cell(7 + procedure_len, 4).Range.Text = test_case.case_problem_sheet
        case_table.Cell(7 + procedure_len, 5).Range.Text = '修改单'
        case_table.Cell(7 + procedure_len, 6).Range.Text = test_case.case_correct_sheet

        case_table.Cell(8 + procedure_len, 1).Range.Text = '测试差异'
        case_table.Cell(8 + procedure_len, 2).Range.Text = test_case.case_diff

        case_table.Cell(9 + procedure_len, 1).Range.Text = '评估准则'
        case_table.Cell(9 + procedure_len, 2).Range.Text = test_case.case_qualified_rule
        # 测试环境行
        case_table.Cell(10 + procedure_len, 1).Range.Text = '测试环境'
        case_table.Cell(10 + procedure_len, 2).Range.Text = self.config[TEST_ENV_KEY][test_case.case_env]


        # 设置表格样式及字体
        case_table.Borders.Enable = True
        self.__set_table_border(case_table, constants.wdLineWidth150pt, constants.wdLineWidth150pt,
                               constants.wdLineWidth150pt, constants.wdLineWidth150pt)
        # 先统一刷
        case_table.Range.Font.Name = '宋体'
        case_table.Range.Font.Name = 'Times New Roman'
        case_table.Cell(1, 1).Range.Text = '用例标识'


        # 设置黑体
        case_table.Cell(1, 1).Range.Font.Name = '黑体'
        case_table.Cell(1, 3).Range.Font.Name = '黑体'
        case_table.Cell(1, 5).Range.Font.Name = '黑体'
        case_table.Cell(2, 1).Range.Font.Name = '黑体'
        case_table.Cell(2, 3).Range.Font.Name = '黑体'
        case_table.Cell(3, 1).Range.Font.Name = '黑体'
        case_table.Cell(4, 1).Range.Font.Name = '黑体'
        case_table.Cell(5, 1).Range.Font.Name = '黑体'
        case_table.Cell(6, 1).Range.Font.Name = '黑体'
        case_table.Cell(6, 2).Range.Font.Name = '黑体'
        case_table.Cell(6, 3).Range.Font.Name = '黑体'
        case_table.Cell(6, 4).Range.Font.Name = '黑体'
        case_table.Cell(6, 5).Range.Font.Name = '黑体'
        case_table.Cell(6, 6).Range.Font.Name = '黑体'
        case_table.Cell(7 + procedure_len, 1).Range.Font.Name = '黑体'
        case_table.Cell(7 + procedure_len, 3).Range.Font.Name = '黑体'
        case_table.Cell(7 + procedure_len, 5).Range.Font.Name = '黑体'
        case_table.Cell(8 + procedure_len, 1).Range.Font.Name = '黑体'
        case_table.Cell(9 + procedure_len, 1).Range.Font.Name = '黑体'
        case_table.Cell(10 + procedure_len, 1).Range.Font.Name = '黑体'

        # 设置文本对齐
        # case_table.Select()
        # self.word_app.Selection.Tables(1).Rows.Alignment = constants.wdAlignRowCenter
        # 删除题注末尾的换行符及表格说明字体
        case_table.Select()
        ref = self.word_app.Selection.Previous(constants.wdParagraph, 2)
        ref.Select()
        self.word_app.Selection.Find.Execute(FindText='^p', ReplaceWith=' ', Replace=constants.wdReplaceOne)
        table_heading_pha.Range.Font.Size = 12
        table_heading_pha.Range.Font.Name = '黑体'

    def write_doc(self, keys, test_cases, process_progressbar):

        process_progressbar.setMaximum(len(keys))
        process_progressbar.setMinimum(0)
        result_list  = []
        try:
            for row_index, key in enumerate(keys):
                test_case = test_cases[key]
                # 写测试计划文档
                self.__write_plan_doc_table(row_index+2, test_case)
                # 写测试计划
                self.__write_spec_doc(test_case)
                # 写测试报告
                self.__write_report_doc(test_case)
                result_list.append([test_case.case_name, test_case.case_mark])
                process_progressbar.setValue(row_index+1)
            self.__write_result(result_list)            
        except Exception as e:
            print(f'write test case error{e}')

    def save_doc(self):
        self.plan_doc.SaveAs(self.plan_doc_name)
        self.spec_doc.SaveAs(self.spec_doc_name)
        self.report_doc.SaveAs(self.report_doc_name)
        self.plan_doc.Close()
        self.spec_doc.Close()
        self.report_doc.Close()
        self.word_app.Quit()

    # def open_doc(self, filename=''):
    #     d = self.word_app.Documents.Open('d:\\test.docx')
    #
    #     #  先替换
    #     for i in range(1, d.Tables.Count + 1):
    #         d.Tables(i).Select()
    #         r_table_title = self.word_app.Selection.Previous(constants.wdParagraph, 1)  # 表格标题
    #         r_table_title.Select()
    #         self.word_app.Selection.Find.Execute(FindText='表XX', ReplaceWith='', Replace=constants.wdReplaceOne)
    #         r_table_title.InsertCaption("表", '', '', constants.wdCaptionPositionAbove)
    #         d.Tables(i).Select()
    #         r_table_title = self.word_app.Selection.Previous(constants.wdParagraph, 2)  # 表格标题
    #         r_table_title.Select()
    #         self.word_app.Selection.Find.Execute(FindText='^p', ReplaceWith='', Replace=constants.wdReplaceOne)
    #         d.Tables(i).Select()
    #         r_table_title = self.word_app.Selection.Previous(constants.wdParagraph, 1)  # 表格标题
    #         r_table_title.Select()
    #         self.word_app.Selection.Font.Name = '黑体'
    #         self.word_app.Selection.Font.Size = 12
    #
    # def _fix_table(self):
    #     for i in range(1, self.doc.Tables.Count + 1):
    #         self.doc.Tables(i).Select()
    #         desc_pha = self.word_app.Selection.Previous(constants.wdParagraph, 2)  # 找到"表XX所在的段落，表格上方第2个"
    #         if desc_pha:
    #             desc_pha.Select()
    #             if self.word_app.Selection.Find.Execute(FindText='表XX'):
    #                 self.word_app.Selection.Range.InsertCrossReference(ReferenceType='表',
    #                                                                    ReferenceKind=constants.wdOnlyLabelAndNumber,
    #                                                                    ReferenceItem='{0}'.format(i),
    #                                                                    InsertAsHyperlink=True,
    #                                                                    IncludePosition=False,
    #                                                                    SeparateNumbers=False, SeparatorString=' ')
    #
    #
    def __get_title_(self, title_level):
        """
        获取标题样式
        :param title_level: 标题级别
        :return: 标题级别变量
        """
        heading_style = constants.wdStyleHeading1
        if title_level == 1:
            heading_style = constants.wdStyleHeading1
        elif title_level == 2:
            heading_style = constants.wdStyleHeading2
        elif title_level == 3:
            heading_style = constants.wdStyleHeading3
        elif title_level == 4:
            heading_style = constants.wdStyleHeading4
        elif title_level == 5:
            heading_style = constants.wdStyleHeading5
        elif title_level == 6:
            heading_style = constants.wdStyleHeading6
        elif title_level == 7:
            heading_style = constants.wdStyleHeading7
        return heading_style
    #
    # def _set_table_border(self, table, left, top, right, bottom):
    #     """
    #     设置表格边框线宽
    #     :param left: 左边框宽度
    #     :param top: 上边框宽度
    #     :param right: 右边框宽度
    #     :param botton: 下边框宽度
    #     :return: 无
    #     """
    #     table.Borders(constants.wdBorderLeft).LineWidth = left
    #     table.Borders(constants.wdBorderTop).LineWidth = top
    #     table.Borders(constants.wdBorderRight).LineWidth = right
    #     table.Borders(constants.wdBorderBottom).LineWidth = bottom
    #
    # def _write_type_title(self, type_name):
    #     """
    #     写入类型名称标题
    #     :param type_name: 类型名称
    #     :return: 无
    #     """
    #     # 创建类型名称标题对应的段落
    #     type_title = self.doc.Paragraphs.Add()  # 将类型名称作为标题
    #     type_title.Range.InsertBefore(type_name)
    #     # type_title.Range.Select()
    #     type_title.Style = self._get_title_(self.start_title)
    #
    # def _write_type_desc(self, desc):
    #     """
    #     写入类型描述
    #     :param desc: 类型描述
    #     :return: 无
    #     """
    #     # 创建类型描述对应的段落
    #     desc_pha = self.doc.Paragraphs.Add()  # 将类型名称作为标题
    #     # desc_pha.LineSpacingRule = constants.wdLineSpaceExactly
    #     desc_pha.LineSpacing = 1.5 * 12  # 设置行距1.5
    #     desc_pha.Range.Font.Name = 'Times New Roman'
    #     desc_pha.Range.Font.NameFarEast = '宋体'
    #     desc_pha.Range.Font.Size = 12  # 小四
    #
    #     desc_pha.CharacterUnitFirstLineIndent = 2  # 首行缩进2字符
    #     desc_pha.Range.InsertBefore(desc)
    #     # desc_ph.Range.Select()
    #     # desc_ph.Style = self._get_title_(self.start_title)
    #
    # def _write_var_list(self, type_name, var_list, visiable):
    #     """
    #     写入类型的成员变量
    #     :param type_name: 类型名称
    #     :param var_list: 成员变量列表
    #     :param visiable: 成员变量列表中成员的可见性
    #     :return: 无
    #     """
    #     # 输出属性标题
    #     var_heading_pha = self.doc.Paragraphs.Add()
    #     var_heading_pha.Range.InsertBefore(visiable + '属性')
    #     # var_heading_pha.Range.Select()
    #     var_heading_pha.Style = self._get_title_(self.start_title + 1)
    #     # 输出描述
    #     var_contents_pha = self.doc.Paragraphs.Add()
    #     var_contents_pha.CharacterUnitFirstLineIndent = 2  # 首行缩进2字符
    #     var_contents_pha.LineSpacing = 1.5 * 12  # 设置行距1.5
    #     var_contents_pha.Range.Font.Size = 12  # 小四
    #     var_contents_pha.Range.Font.Name = 'Times New Roman'
    #     var_contents_pha.Range.Font.NameFarEast = '宋体'
    #     if len(var_list):
    #         var_contents_pha.Range.InsertBefore(visiable + '属性如表XX所示。')
    #         # var_contents_pha.Range.InsertCrossReference(ReferenceType='表', ReferenceKind=constants.wdEntireCaption,
    #         #                                             ReferenceItem='{0}'.format(self.ref_table_index+1),
    #         #                                             InsertAsHyperlink=True, IncludePosition=False,
    #         #                                             SeparateNumbers=False, SeparatorString=' ')
    #         # 输出表题
    #         table_heading_pha = self.doc.Paragraphs.Add()
    #         table_heading_pha.LineSpacing = 1.5*12
    #         table_heading_pha.Alignment = constants.wdAlignParagraphCenter
    #         # table_heading_pha.Range.Font.Size = 12
    #         # table_heading_pha.Range.Font.Name = '黑体'
    #         table_heading_pha.Range.InsertCaption("表", '', '', constants.wdCaptionPositionAbove)
    #         table_heading_pha.Range.InsertBefore('{0}属性列表'.format(visiable))
    #         table_pha = self.doc.Paragraphs.Add()
    #         # 输出属性表格 共3列，分别为类型名称，数据类型，描述，外边框1.5磅
    #         var_table = table_pha.Range.Tables.Add(table_pha.Range, len(var_list) + 1, 3)
    #         var_table.Columns(1).SetWidth(4*28.35, 0)  # 1cm = 28.35磅
    #         var_table.Columns(2).SetWidth(4*28.35, 0)  # 1cm = 28.35磅
    #         var_table.Columns(3).SetWidth(6.5*28.35, 0)  # 1cm = 28.35磅
    #         var_table.Borders.Enable = True
    #         self._set_table_border(var_table, constants.wdLineWidth150pt, constants.wdLineWidth150pt,
    #                                constants.wdLineWidth150pt, constants.wdLineWidth150pt)
    #         var_table.Cell(1, 1).Range.Text = '属性名称'
    #         var_table.Cell(1, 2).Range.Text = '数据类型'
    #         var_table.Cell(1, 3).Range.Text = '数据描述'
    #         for index, var in enumerate(var_list):
    #             var_table.Cell(index + 2, 1).Range.Text = var[1]
    #             var_table.Cell(index + 2, 2).Range.Text = var[0]
    #             var_table.Cell(index + 2, 3).Range.Text = var[2]
    #         # var_table.Range.Select()
    #         var_table.Range.Font.Name = '宋体'
    #         var_table.Range.Font.Name = 'Times New Roman'
    #         var_table.Rows(1).Range.Font.Name = '黑体'
    #         var_table.Select()
    #         self.word_app.Selection.Tables(1).Rows.Alignment = constants.wdAlignRowCenter
    #         # 删除题注末尾的换行符
    #         var_table.Select()
    #         ref = self.word_app.Selection.Previous(constants.wdParagraph, 2)
    #         ref.Select()
    #         self.word_app.Selection.Find.Execute(FindText='^p', ReplaceWith=' ', Replace=constants.wdReplaceOne)
    #         table_heading_pha.Range.Font.Size = 12
    #         table_heading_pha.Range.Font.Name = '黑体'
    #     else:
    #         var_contents_pha.Range.InsertBefore('无。')
    #
    # def _write_fun_list(self, fun_list, visiable):
    #     """
    #     写入类型的成员函数
    #     :param fun_list: 成员函数列表
    #     :param visiable: 成员变量列表中成员的可见性
    #     :return: 无
    #     """
    #     # 输出成员函数标题
    #     fun_pha = self.doc.Paragraphs.Add()
    #     fun_pha.Range.InsertBefore(visiable + '方法')
    #     # fun_pha.Range.Select()
    #     fun_pha.Style = self._get_title_(self.start_title + 1)
    #     if len(fun_list):
    #         for index, fun in enumerate(fun_list):
    #             # 函数名作为标题
    #             fun_name = fun[1].split(' ')[0]
    #             fun_heading_pha = self.doc.Paragraphs.Add()
    #             fun_heading_pha.Range.InsertBefore(fun_name + '方法')
    #             fun_heading_pha.Style = self._get_title_(self.start_title + 2)
    #             # 输出描述
    #             fun_contents_pha = self.doc.Paragraphs.Add()
    #             fun_contents_pha.CharacterUnitFirstLineIndent = 2  # 首行缩进2字符
    #             fun_contents_pha.LineSpacing = 1.5 * 12  # 设置行距1.5
    #             fun_contents_pha.Range.Font.Size = 12  # 小四
    #             fun_contents_pha.Range.Font.Name = 'Times New Roman'
    #             fun_contents_pha.Range.Font.NameFarEast = '宋体'
    #             fun_contents_pha.Range.InsertBefore(fun_name + '方法说明如表XX所示。')
    #             # 输出表题
    #             table_heading_pha = self.doc.Paragraphs.Add()
    #             table_heading_pha.LineSpacing = 1.5 * 12
    #             table_heading_pha.Alignment = constants.wdAlignParagraphCenter
    #             # table_heading_pha.Range.Font.Size = 12
    #             # table_heading_pha.Range.Font.Name = '黑体'
    #             table_heading_pha.Range.InsertCaption("表", '', '', constants.wdCaptionPositionAbove)
    #             table_heading_pha.Range.InsertBefore('{0}方法'.format(fun_name))
    #             table_pha = self.doc.Paragraphs.Add()
    #             # 输出属性表格 4行，2列，分别为函数原型，函数描述，参数说明，返回值，流程图，外边框1.5磅
    #             fun_table = table_pha.Range.Tables.Add(table_pha.Range, 5, 2)
    #             fun_table.Borders.Enable = True
    #             self._set_table_border(fun_table, constants.wdLineWidth150pt, constants.wdLineWidth150pt,
    #                                    constants.wdLineWidth150pt, constants.wdLineWidth150pt)
    #             fun_table.Columns(1).SetWidth(3*28.35, 0)  # 1cm = 28.35磅
    #             fun_table.Columns(2).SetWidth(12*28.35, 0)  # 1cm = 28.35磅
    #             fun_table.Cell(1, 1).Range.Text = '函数原型'
    #             fun_table.Cell(2, 1).Range.Text = '函数描述'
    #             fun_table.Cell(3, 1).Range.Text = '参数说明'
    #             fun_table.Cell(4, 1).Range.Text = '返 回 值'
    #             fun_table.Cell(5, 1).Range.Text = '流 程 图'
    #             template_desc = fun[5] + '\n' if fun[5] else ''
    #             fun_table.Cell(1, 2).Range.Text = template_desc + ((fun[0] + ' ' + fun[1]) if len(fun[0]) else fun[1])  # 函数声明
    #             fun_table.Cell(2, 2).Range.Text = fun[2]  # 函数描述
    #             fun_table.Cell(3, 2).Range.Text = '\n'.join(fun[3]) if len(fun[3]) else '无'  # 参数说明
    #             fun_table.Cell(4, 2).Range.Text = fun[4] if len(fun[4]) else '无'  # 返回值说明
    #             fun_table.Cell(5, 2).Range.Text = '无'  # 流程图
    #             fun_table.Range.Font.Name = '宋体'
    #             fun_table.Range.Font.Name = 'Times New Roman'
    #             fun_table.Cell(1, 1).Range.Font.Name = '黑体'
    #             fun_table.Cell(2, 1).Range.Font.Name = '黑体'
    #             fun_table.Cell(3, 1).Range.Font.Name = '黑体'
    #             fun_table.Cell(4, 1).Range.Font.Name = '黑体'
    #             fun_table.Cell(5, 1).Range.Font.Name = '黑体'
    #             fun_table.Select()
    #             self.word_app.Selection.Tables(1).Rows.Alignment = constants.wdAlignRowCenter
    #             # 删除题注末尾的换行符
    #             fun_table.Select()
    #             ref = self.word_app.Selection.Previous(constants.wdParagraph, 2)
    #             ref.Select()
    #             self.word_app.Selection.Find.Execute(FindText='^p', ReplaceWith=' ', Replace=constants.wdReplaceOne)
    #             table_heading_pha.Range.Font.Size = 12
    #             table_heading_pha.Range.Font.Name = '黑体'
    #     else:
    #         no_fun_pha = self.doc.Paragraphs.Add()
    #         no_fun_pha.CharacterUnitFirstLineIndent = 2  # 首行缩进2字符
    #         no_fun_pha.LineSpacing = 1.5 * 12  # 设置行距1.5
    #         no_fun_pha.Range.Font.Size = 12  # 小四
    #         no_fun_pha.Range.Font.Name = '宋体'
    #         no_fun_pha.Range.InsertBefore('无。')
    #
    # def _write_typedefs(self, typedef_list):
    #     """
    #     写入类型内部的重定义类型列表
    #     :param typedef_list:重定义类型列表
    #     :return: 无
    #     """
    #     # 输出类型重定义标题
    #     typedef_pha = self.doc.Paragraphs.Add()
    #     typedef_pha.Range.InsertBefore('类型重定义')
    #     # fun_pha.Range.Select()
    #     typedef_pha.Style = self._get_title_(self.start_title + 1)
    #     if len(typedef_list):
    #         # 输出描述
    #         typedef_contents_pha = self.doc.Paragraphs.Add()
    #         typedef_contents_pha.CharacterUnitFirstLineIndent = 2  # 首行缩进2字符
    #         typedef_contents_pha.LineSpacing = 1.5 * 12  # 设置行距1.5
    #         typedef_contents_pha.Range.Font.Size = 12  # 小四
    #         typedef_contents_pha.Range.Font.Name = 'Times New Roman'
    #         typedef_contents_pha.Range.Font.NameFarEast = '宋体'
    #         typedef_contents_pha.Range.InsertBefore('类型重定义如表XX所示。')
    #         # 输出标题
    #         table_heading_pha = self.doc.Paragraphs.Add()
    #         table_heading_pha.LineSpacing = 1.5 * 12
    #         table_heading_pha.Alignment = constants.wdAlignParagraphCenter
    #         # table_heading_pha.Range.Font.Size = 12
    #         # table_heading_pha.Range.Font.Name = '黑体'
    #         table_heading_pha.Range.InsertCaption("表", '', '', constants.wdCaptionPositionAbove)
    #         table_heading_pha.Range.InsertBefore('数据类型重定义说明')
    #         table_pha = self.doc.Paragraphs.Add()
    #         # 输出属性表格 多行，2列，分别为重定义描述/重定义说明，外边框1.5磅
    #         typedef_table = table_pha.Range.Tables.Add(table_pha.Range, len(typedef_list) + 1, 2)
    #         typedef_table.Borders.Enable = True
    #         self._set_table_border(typedef_table, constants.wdLineWidth150pt, constants.wdLineWidth150pt,
    #                                constants.wdLineWidth150pt, constants.wdLineWidth150pt)
    #         typedef_table.Columns(1).SetWidth(10 * 28.35, 0)  # 1cm = 28.35磅
    #         typedef_table.Columns(2).SetWidth(5 * 28.35, 0)  # 1cm = 28.35磅
    #         typedef_table.Cell(1, 1).Range.Text = '类型定义'
    #         typedef_table.Cell(1, 2).Range.Text = '类型描述'
    #         # 填充表格内容
    #         for index, type_item in enumerate(typedef_list):
    #             typedef_table.Cell(index + 2, 1).Range.Text = type_item[0]
    #             typedef_table.Cell(index + 2, 2).Range.Text = type_item[1] if len(type_item[1]) else '无'
    #         # 设置表格字体，中文，英文，表头
    #         typedef_table.Range.Font.Name = '宋体'
    #         typedef_table.Range.Font.Name = 'Times New Roman'
    #         typedef_table.Cell(1, 1).Range.Font.Name = '黑体'
    #         typedef_table.Cell(1, 2).Range.Font.Name = '黑体'
    #         typedef_table.Select()
    #         self.word_app.Selection.Tables(1).Rows.Alignment = constants.wdAlignRowCenter
    #         # 删除题注末尾的换行符
    #         typedef_table.Select()
    #         ref = self.word_app.Selection.Previous(constants.wdParagraph, 2)
    #         ref.Select()
    #         self.word_app.Selection.Find.Execute(FindText='^p', ReplaceWith=' ', Replace=constants.wdReplaceOne)
    #         table_heading_pha.Range.Font.Size = 12
    #         table_heading_pha.Range.Font.Name = '黑体'
    #     else:
    #         no_def_pha = self.doc.Paragraphs.Add()
    #         no_def_pha.CharacterUnitFirstLineIndent = 2  # 首行缩进2字符
    #         no_def_pha.LineSpacing = 1.5 * 12  # 设置行距1.5
    #         no_def_pha.Range.Font.Size = 12  # 小四
    #         no_def_pha.Range.Font.Name = '宋体'
    #         no_def_pha.Range.InsertBefore('无。')
    #
    # def _write_enums(self, enum_list):
    #     """
    #     写入类型内部的重定义类型列表
    #     :param enum_list:枚举类型类型列表
    #     :return: 无
    #     """
    #     # 输出枚举标题
    #     enum_pha = self.doc.Paragraphs.Add()
    #     enum_pha.Range.InsertBefore('枚举值定义')
    #     enum_pha.Style = self._get_title_(self.start_title + 1)
    #     if len(enum_list):
    #         # 输出描述
    #         enum_contents_pha = self.doc.Paragraphs.Add()
    #         enum_contents_pha.CharacterUnitFirstLineIndent = 2  # 首行缩进2字符
    #         enum_contents_pha.LineSpacing = 1.5 * 12  # 设置行距1.5
    #         enum_contents_pha.Range.Font.Size = 12  # 小四
    #         enum_contents_pha.Range.Font.Name = 'Times New Roman'
    #         enum_contents_pha.Range.Font.NameFarEast = '宋体'
    #         enum_contents_pha.Range.InsertBefore('枚举值定义如表XX所示。')
    #         # 输出标题
    #         table_heading_pha = self.doc.Paragraphs.Add()
    #         table_heading_pha.LineSpacing = 1.5 * 12
    #         table_heading_pha.Alignment = constants.wdAlignParagraphCenter
    #         # table_heading_pha.Range.Font.Size = 12
    #         # table_heading_pha.Range.Font.Name = '黑体'
    #         table_heading_pha.Range.InsertCaption("表", '', '', constants.wdCaptionPositionAbove)
    #         table_heading_pha.Range.InsertBefore('枚举值定义说明')
    #         table_pha = self.doc.Paragraphs.Add()
    #         # 输出属性表格 多行，2列，分别为枚举值/枚举值说明，外边框1.5磅
    #         enum_table = table_pha.Range.Tables.Add(table_pha.Range, len(enum_list) + 1, 2)
    #         enum_table.Borders.Enable = True
    #         self._set_table_border(enum_table, constants.wdLineWidth150pt, constants.wdLineWidth150pt,
    #                                constants.wdLineWidth150pt, constants.wdLineWidth150pt)
    #         enum_table.Columns(1).SetWidth(5 * 28.35, 0)  # 1cm = 28.35磅
    #         enum_table.Columns(2).SetWidth(10 * 28.35, 0)  # 1cm = 28.35磅
    #         enum_table.Cell(1, 1).Range.Text = '枚举值'
    #         enum_table.Cell(1, 2).Range.Text = '说明'
    #         # 填充表格内容
    #         for index, type_item in enumerate(enum_list):
    #             enum_table.Cell(index + 2, 1).Range.Text = type_item[0]
    #             enum_table.Cell(index + 2, 2).Range.Text = type_item[1] if len(type_item[1]) else '无'
    #         # 设置表格字体，中文，英文，表头
    #         enum_table.Range.Font.Name = '宋体'
    #         enum_table.Range.Font.Name = 'Times New Roman'
    #         enum_table.Cell(1, 1).Range.Font.Name = '黑体'
    #         enum_table.Cell(1, 2).Range.Font.Name = '黑体'
    #         enum_table.Select()
    #         self.word_app.Selection.Tables(1).Rows.Alignment = constants.wdAlignRowCenter
    #         # 删除题注末尾的换行符
    #         enum_table.Select()
    #         ref = self.word_app.Selection.Previous(constants.wdParagraph, 2)
    #         ref.Select()
    #         self.word_app.Selection.Find.Execute(FindText='^p', ReplaceWith=' ', Replace=constants.wdReplaceOne)
    #         table_heading_pha.Range.Font.Size = 12
    #         table_heading_pha.Range.Font.Name = '黑体'
    #     else:
    #         no_def_pha = self.doc.Paragraphs.Add()
    #         no_def_pha.CharacterUnitFirstLineIndent = 2  # 首行缩进2字符
    #         no_def_pha.LineSpacing = 1.5 * 12  # 设置行距1.5
    #         no_def_pha.Range.Font.Size = 12  # 小四
    #         no_def_pha.Range.Font.Name = '宋体'
    #         no_def_pha.Range.InsertBefore('无。')
    #
    #
    # def write(self, data_type):
    #     """
    #     将data_type表示的数据类型信息写入配置文件
    #     :param data_type: 数据类型信息
    #     :return: 无
    #     """
    #     self._write_type_title(data_type.name)
    #     self._write_type_desc(data_type.desc+'。')
    #     self._write_typedefs(data_type.typedef_list)
    #     self._write_enums(data_type.enum_list)
    #     self._write_var_list(data_type.name, data_type.public_var_list, 'Public')
    #     self._write_var_list(data_type.name, data_type.protected_var_list, 'Protected')
    #     self._write_var_list(data_type.name, data_type.private_var_list, 'Private')
    #     self._write_fun_list(data_type.public_fun_list, 'Public')
    #     self._write_fun_list(data_type.protected_fun_list, 'Protected')
    #     self._write_fun_list(data_type.private_fun_list, 'Private')
    #
    # def save(self):
    #     """
    #     保存并关闭文件
    #     :return: 无
    #     """
    #     self._fix_table()
    #     self.doc.SaveAs(self.doc_name)
    #     # self.doc.Close()
    #     # self.word_app.Quit()
    #
    #
