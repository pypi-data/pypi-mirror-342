import pandas as pd
import yaml
from typing import Dict, Optional, List
import logging
import matplotlib.pyplot as plt
import numpy as np

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RiskModel:
    """
    风险评估模型类
    
    这个类提供了完整的风险评估功能，包括数据加载、风险计算、结果导出和可视化。
    
    参数:
        config_path (str, optional): 配置文件路径，包含权重和计算参数。默认为None。
    
    属性:
        df (pandas.DataFrame): 存储输入数据的DataFrame
        weights (dict): 各类风险的权重配置
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        初始化风险评估模型
        Args:
            config_path: 配置文件路径（可选）
        """
        self.df = None
        # 定义各风险类型内部计算的权重
        self.internal_weights = {
            'strategic': {
                'fa1': 0.1,  # 业务集中度1
                'fa2': 0.1,  # 业务集中度2
                'fa3': 0.3,  # 主业毛利率
                'fa4': 0.1,  # 研发投入增速
                'fa5': 0.4   # 主营业务亏损金额
            },
            'financial': {
                'fb1': 0.3,  # 资产负债率
                'fb2': 0.2,  # 带息负债比率
                'fb3': 0.25, # 经营净现金流占比
                'fb4': 0.25  # 现金流与投资收益占利息比
            },
            'market': {
                'fc1': 0.1,  # 预付账款占比
                'fc2': 0.1,  # 预收账款占比
                'fc3': 0.15, # 应付账款占比
                'fc4': 0.15, # 应收账款占比
                'fc5': 0.1,  # 坏账准备率
                'fc6': 0.2,  # 存货占比
                'fc7': 0.2   # 毛利润占比
            },
            'legal_credit': {
                'fd1': 0.3,  # 诉讼案件比例
                'fd2': 0.35, # 主执行金额占比
                'fd3': 0.35  # 被执行金额占比
            },
            'event': {
                'fe1': 1,  # 销号率
                'fe2': 1,  # 影响金额消减率
                'fe3': 1,  # 降损率
                'fe4': 1,  # 处置化解率
                'fe5': 1   # 计提覆盖率
            }
        }
        
        logger.info("风险评估模型初始化完成")


    def load_data(self, file_path: str, sheet_name: Optional[str] = None) -> None:
        """
        加载Excel数据文件
        
        参数:
            file_path (str): Excel文件路径
            sheet_name (str, optional): 工作表名称，默认为None（读取第一个工作表）
        
        异常:
            FileNotFoundError: 当文件不存在时抛出
            ValueError: 当数据格式不正确时抛出
        
        示例:
            >>> model.load_data('data.xlsx')
            >>> model.load_data('data.xlsx', sheet_name='Sheet1')
        """
        try:
            # 读取原始数据
            raw_df = pd.read_excel(file_path, sheet_name=sheet_name)
            
            # 将第一列设置为索引
            self.df = raw_df.set_index(raw_df.columns[0])
            
            # 转置数据，使月份成为索引
            self.df = self.df.transpose()
            
            # 将所有数值列转换为float类型
            for column in self.df.columns:
                try:
                    self.df[column] = pd.to_numeric(self.df[column], errors='coerce')
                except Exception as e:
                    logger.warning(f"列 '{column}' 转换为数值类型时出错: {e}")
            
            # 验证数据完整性
            self._validate_data()
            logger.info(f"成功加载数据，共{len(self.df)}行")
        except Exception as e:
            logger.error(f"数据加载失败: {e}")
            raise

    def _validate_data(self) -> None:
        """验证数据完整性"""
        required_columns = [
            '主营业务收入', '营业总收入', '主营业务利润总额', '利润总额', '主营业务毛利润',
            '研发（R&D）经费投入的本年累计数', '研发（R&D）经费投入的上年同期数',
            '主营业务成本', '主营业务相关费用',
            '负债总额', '资产总额', '带息负债总额', '经营净现金流',
            '货币资金', '投资收益', '财务费用中的利息费用', '资本化利息支出',
            '预付账款', '预收账款', '资产总额', '应收账款', '应付账款', '净资产',
            '坏账准备金额', '存货', '毛利润',
            '企业当年新发生司法诉讼案件的数量', '上一年司法案件数量', '近一年主执行金额', '近一年被执行金额',
            '已销号个数', '年初事件个数', '新增事件个数',
            '已销号事件影响金额', '年初事件影响金额', '新增事件影响金额',
            '未销号事件兜底保障金额', '未销号事件追损挽损金额',
            '未销号事件影响金额', '未销号事件累计计提减值金额',
            '主业毛利率行业中等值', '企业科技创新考核目标任务值', '资产负债率行业中等值',
            '带息负债比率行业中等值', '预付账款占比行业平均值', '预收账款行业平均值',
            '应付账款行业平均值', '应收账款行业平均值', '存货行业平均值', '毛利率行业平均值',
            '严重失信企业数量', '品牌风险企业数量', '行政处罚企业数量', '高危企业发生重大事故次数',
            '高危企业发生较大事故同责及以上事故次数', '高危企业发生较大事故次责事故次数',
            '高危企业发生一般责任事故次数',
            '非高危企业发生较大事故同责及其以上事故次数', '非高危企业发生较大事故次责事故次数',
            '非高危企业发生一般责任事故次数',
            '较大生态环境事件', '一般生态环境事件',
            '高危企业发生特别重大生产安全事故次数', '非高危企业发生特别重大生产安全事故次数',
            '企业发生重大及以上生态环境事件次数', '带息负债率行业较差值', '货币资金', '财务费用中的利息费用'
        ]

        # 检查所有必需的指标是否都在数据中
        missing_columns = [col for col in required_columns if col not in self.df.columns]
        if missing_columns:
            raise ValueError(f"缺少必要的指标: {', '.join(missing_columns)}")
            
        # 检查是否有空值或非数值
        for col in required_columns:
            if col in self.df.columns:
                null_values = self.df[col].isnull().sum()
                if null_values > 0:
                    logger.warning(f"列 '{col}' 中存在 {null_values} 个空值")
                non_numeric = self.df[col].apply(lambda x: not pd.api.types.is_numeric_dtype(type(x))).sum()
                if non_numeric > 0:
                    logger.warning(f"列 '{col}' 中存在 {non_numeric} 个非数值类型的数据")

    def _safe_divide(self, numerator: float, denominator: float, default_value: float = 0.0) -> float:
        """
        安全除法，处理除以零的情况
        Args:
            numerator: 分子
            denominator: 分母
            default_value: 当分母为0时返回的默认值
        Returns:
            除法结果或默认值
        """
        try:
            if abs(denominator) < 1e-10:  # 处理接近0的情况
                return default_value
            return numerator / denominator
        except Exception:
            return default_value

    def piecewise_function(self, x, segments, **kwargs):
        """
        实现分段函数的求值
        Args:
            x: 自变量的值
            segments: 一个列表，每个元素是一个二元组 (condition, func)
            kwargs: 其他参数
        Returns:
            满足条件的那一段对应的函数计算结果
        """
        for cond, func in segments:
            if cond(x, **kwargs):
                return func(x, **kwargs)
        raise ValueError(f"没有找到满足 x = {x} 的条件。")

    def _get_monthly_value(self, column: str, row_idx: int) -> float:
        """
        获取指定列的月度值（如果是累计值则计算增量）
        Args:
            column: 列名
            row_idx: 行索引
        Returns:
            月度值
        """
        current_value = self.df[column].iloc[row_idx]
        if row_idx == 0:  # 第一个月直接返回当前值
            return current_value
        previous_value = self.df[column].iloc[row_idx - 1]
        return current_value - previous_value

    def _calculate_strategic_risk(self, row_idx: int) -> float:
        """计算战略风险分数"""
        # monthly_main_revenue = self._get_monthly_value('主营业务收入', row_idx)
        # monthly_total_revenue = self._get_monthly_value('总营业收入', row_idx)

        # 战略风险
        # 企业主营业务收入占企业营业总收入的比重
        concentration1 = self._safe_divide(
            self.df['主营业务收入'].iloc[row_idx],
            self.df['营业总收入'].iloc[row_idx]
        )

        # 定义分段函数
        segment1 = [
            (lambda x, **kwargs: x >= 0.85, lambda x, **kwargs: 0),
            (lambda x, **kwargs: x < 0.85, lambda x, **kwargs: min(15, 100 * (0.85 - x)))
        ]
        fa1 = self.piecewise_function(concentration1, segment1)
        # 企业主营业务利润总额占企业利润总额的比重
        concentration2 = self._safe_divide(
            self.df['主营业务利润总额'].iloc[row_idx],
            self.df['利润总额'].iloc[row_idx]
        )
        segment2 = [
            (lambda x, **kwargs: x >= 0.85, lambda x, **kwargs: 0),
            (lambda x, **kwargs: x < 0.85, lambda x, **kwargs: min(15, 300 * (0.85 - x)))
        ]
        fa2 = self.piecewise_function(concentration2, segment2)
        # 主营业务毛利润占主营业务收入的比重
        gross_margin = self._safe_divide(
            self.df['主营业务毛利润'].iloc[row_idx],
            self.df['主营业务收入'].iloc[row_idx]
        )
        segment3 = [
            (lambda x, **kwargs: x >= self.df['主业毛利率行业中等值'].iloc[row_idx], lambda x, **kwargs: 0),
            (lambda x, **kwargs: x < self.df['主业毛利率行业中等值'].iloc[row_idx],
             lambda x, **kwargs: min(15, 500 * (self.df['主业毛利率行业中等值'].iloc[row_idx] - x)))
        ]
        fa3 = self.piecewise_function(gross_margin, segment3)
        # 企业研发投入增速
        r_and_d_intensity = self._safe_divide(
            self.df['研发（R&D）经费投入的本年累计数'].iloc[row_idx],
            self.df['研发（R&D）经费投入的上年同期数'].iloc[row_idx]
        )
        segment4 = [
            (lambda x, **kwargs: x >= self.df['企业科技创新考核目标任务值'].iloc[row_idx], lambda x, **kwargs: 0),
            (lambda x, **kwargs: x < self.df['企业科技创新考核目标任务值'].iloc[row_idx],
             lambda x, **kwargs: min(15, 300 * ( self.df['企业科技创新考核目标任务值'].iloc[row_idx] -x)))
        ]
        fa4 = self.piecewise_function(r_and_d_intensity, segment4)
        # 企业主营业务亏损金额
        loss_amount = (self.df['主营业务收入'].iloc[row_idx] -
                       (self.df['主营业务成本'].iloc[row_idx] + self.df['主营业务相关费用'].iloc[row_idx]))
        segment5 = [
            (lambda x, **kwargs: x > 0, lambda x, **kwargs: 0),
            (lambda x, **kwargs: x == 0, lambda x, **kwargs: 3),
            (lambda x, **kwargs: x < 0, lambda x, **kwargs: min(15, 3 + 3 * abs(x) / 5000))
        ]
        fa5 = self.piecewise_function(loss_amount, segment5)

        # 使用内部权重计算战略风险总分
        weights = self.internal_weights['strategic']
        return (fa1 * weights['fa1'] + fa2 * weights['fa2'] + fa3 * weights['fa3'] + 
                fa4 * weights['fa4'] + fa5 * weights['fa5'])

    def _calculate_financial_risk(self, row_idx: int) -> float:
        """计算财务风险分数"""
        # 计算各项指标
        # 资产负债率
        debt_ratio = self._safe_divide(
            self.df['负债总额'].iloc[row_idx],
            self.df['资产总额'].iloc[row_idx]
        )
        segment6 = [
            (lambda x, **kwargs: x <= self.df['资产负债率行业中等值'].iloc[row_idx], lambda x, **kwargs: 0),
            (lambda x, **kwargs: x > self.df['资产负债率行业中等值'].iloc[row_idx],
             lambda x, **kwargs: min(30, 500 * (x - self.df['资产负债率行业中等值'].iloc[row_idx])))
        ]
        fb1 = self.piecewise_function(debt_ratio, segment6)
        # 带息负债比率
        interest_bearing_debt_ratio = self._safe_divide(
            self.df['带息负债总额'].iloc[row_idx],
            self.df['负债总额'].iloc[row_idx]
        )
        segment7 = [
            (lambda x, **kwargs: x <= self.df['带息负债比率行业中等值'].iloc[row_idx], lambda x, **kwargs: 0),
            (lambda x, **kwargs: x > self.df['带息负债比率行业中等值'].iloc[row_idx],
             lambda x, **kwargs: min(30, 500 * (x - self.df['带息负债比率行业中等值'].iloc[row_idx])))
        ]
        fb2 = self.piecewise_function(interest_bearing_debt_ratio, segment7)
        # 经营净现金流占货币资金的比重
        operating_cash_flow = self._safe_divide(self.df['经营净现金流'].iloc[row_idx],
                                                self.df['货币资金'].iloc[row_idx])
        segment8 = [
            (lambda x, **kwargs: x > 0, lambda x, **kwargs: 0),
            (lambda x, **kwargs: x <= 0, lambda x, **kwargs: min(30, 100 * abs(x)))
        ]
        fb3 = self.piecewise_function(operating_cash_flow, segment8)
        # （经营净现金流+投资分红等收益）占利息支出的比重
        inventory_ratio = self._safe_divide(
            self.df['经营净现金流'].iloc[row_idx] + self.df['投资收益'].iloc[row_idx],
            self.df['财务费用中的利息费用'].iloc[row_idx] + self.df['资本化利息支出'].iloc[row_idx]
        )
        segment9 = [
            (lambda x, **kwargs: x >= 1, lambda x, **kwargs: 0),
            (lambda x, **kwargs: x < 1, lambda x, **kwargs: min(30, 700 * abs(x - 1)))
        ]
        fb4 = self.piecewise_function(inventory_ratio, segment9)

        # 使用内部权重计算财务风险总分
        weights = self.internal_weights['financial']
        return (fb1 * weights['fb1'] + fb2 * weights['fb2'] + 
                fb3 * weights['fb3'] + fb4 * weights['fb4'])

    def _calculate_market_risk(self, row_idx: int) -> float:
        """计算市场风险分数"""
        # 市场风险C
        # 预付账款占营业总收入的比重
        prepaid_ratio = self._safe_divide(
            self.df['预付账款'].iloc[row_idx],
            self.df['营业总收入'].iloc[row_idx]
        )
        segment10 = [
            (lambda x, **kwargs: x <= self.df['预付账款占比行业平均值'].iloc[row_idx], lambda x, **kwargs: 0),
            (lambda x, **kwargs: x > self.df['预付账款占比行业平均值'].iloc[row_idx],
             lambda x, **kwargs: min(25, 300 * abs(x - self.df['预付账款占比行业平均值'].iloc[row_idx])))
        ]
        fc1 = self.piecewise_function(prepaid_ratio, segment10)
        # 预收账款占资产总额的比重
        pre_received_ratio = self._safe_divide(
            self.df['预收账款'].iloc[row_idx],
            self.df['资产总额'].iloc[row_idx]
        )
        segment11 = [
            (lambda x, **kwargs: x <= self.df['预收账款行业平均值'].iloc[row_idx], lambda x, **kwargs: 0),
            (lambda x, **kwargs: x > self.df['预收账款行业平均值'].iloc[row_idx],
             lambda x, **kwargs: min(25, 200 * abs(x - self.df['预收账款行业平均值'].iloc[row_idx])))
        ]
        fc2 = self.piecewise_function(pre_received_ratio, segment11)
        # 应付账款占营业总收入的比值
        accounts_payable_ratio = self._safe_divide(
            self.df['应付账款'].iloc[row_idx],
            self.df['营业总收入'].iloc[row_idx]
        )
        segment12 = [
            (lambda x, **kwargs: x <= self.df['应付账款行业平均值'].iloc[row_idx], lambda x, **kwargs: 0),
            (lambda x, **kwargs: x > self.df['应付账款行业平均值'].iloc[row_idx],
             lambda x, **kwargs: min(25, 200 * abs(x - self.df['应付账款行业平均值'].iloc[row_idx])))
        ]
        fc3 = self.piecewise_function(accounts_payable_ratio, segment12)
        # 应收账款占净资产的比重
        receivables_ratio = self._safe_divide(
            self.df['应收账款'].iloc[row_idx],
            self.df['净资产'].iloc[row_idx]
        )
        segment13 = [
            (lambda x, **kwargs: x <= self.df['应收账款行业平均值'].iloc[row_idx], lambda x, **kwargs: 0),
            (lambda x, **kwargs: x > self.df['应收账款行业平均值'].iloc[row_idx],
             lambda x, **kwargs: min(25, 200 * abs(x - self.df['应收账款行业平均值'].iloc[row_idx])))
        ]
        fc4 = self.piecewise_function(receivables_ratio, segment13)
        # 应收账款坏账准备率
        receivables_bad_debt_ratio = self._safe_divide(
            self.df['坏账准备金额'].iloc[row_idx],
            self.df['应收账款'].iloc[row_idx] + self.df['坏账准备金额'].iloc[row_idx]
        )
        segment14 = [
            (lambda x, **kwargs: x >= 0.5, lambda x, **kwargs: 0),
            (lambda x, **kwargs: x < 0.5, lambda x, **kwargs: min(25, 100 * abs(x - 0.5)))
        ]
        fc5 = self.piecewise_function(receivables_bad_debt_ratio, segment14)
        # 存货占净资产的比重
        inventory_ratio = self._safe_divide(
            self.df['存货'].iloc[row_idx],
            self.df['净资产'].iloc[row_idx]
        )
        segment15 = [
            (lambda x, **kwargs: x <= self.df['存货行业平均值'].iloc[row_idx], lambda x, **kwargs: 0),
            (lambda x, **kwargs: x > self.df['存货行业平均值'].iloc[row_idx],
             lambda x, **kwargs: min(25, 200 * abs(x - self.df['存货行业平均值'].iloc[row_idx])))
        ]
        fc6 = self.piecewise_function(inventory_ratio, segment15)
        # 毛利润占营业总收入的比重
        margin_ratio = self._safe_divide(
            self.df['毛利润'].iloc[row_idx],
            self.df['营业总收入'].iloc[row_idx]
        )
        segment16 = [
            (lambda x, **kwargs: x >= self.df['毛利率行业平均值'].iloc[row_idx], lambda x, **kwargs: 0),
            (lambda x, **kwargs: x < self.df['毛利率行业平均值'].iloc[row_idx],
             lambda x, **kwargs: min(25, 500 * abs(x - self.df['毛利率行业平均值'].iloc[row_idx])))
        ]
        fc7 = self.piecewise_function(margin_ratio, segment16)

        # 使用内部权重计算市场风险总分
        weights = self.internal_weights['market']
        return (fc1 * weights['fc1'] + fc2 * weights['fc2'] + fc3 * weights['fc3'] + 
                fc4 * weights['fc4'] + fc5 * weights['fc5'] + fc6 * weights['fc6'] + 
                fc7 * weights['fc7'])

    def _calculate_legal_credit_risk(self, row_idx: int) -> float:
        """计算法律风险分数"""
        # 法律风险
        # 企业涉及司法诉讼案件的数量
        litigation_cases = self._safe_divide(
            self.df['企业当年新发生司法诉讼案件的数量'].iloc[row_idx],
            self.df['上一年司法案件数量'].iloc[row_idx]
        )
        segment17 = [
            (lambda x, **kwargs: x <= 1, lambda x, **kwargs: 0),
            (lambda x, **kwargs: x > 1, lambda x, **kwargs: min(10, 100 * abs(x - 1)))
        ]
        fd1 = self.piecewise_function(litigation_cases, segment17)
        # 主执行金额占净资产的比重
        execution_amount_ratio = self._safe_divide(
            self.df['近一年主执行金额'].iloc[row_idx],
            self.df['净资产'].iloc[row_idx]
        )
        segment18 = [
            (lambda x, **kwargs: x <= 0, lambda x, **kwargs: 0),
            (lambda x, **kwargs: x > 0, lambda x, **kwargs: min(10, 10000 * abs(x)))
        ]
        fd2 = self.piecewise_function(execution_amount_ratio, segment18)
        # 被执行金额占净资产的比重
        executed_amount_ratio = self._safe_divide(
            self.df['近一年被执行金额'].iloc[row_idx],
            self.df['净资产'].iloc[row_idx]
        )
        segment19 = [
            (lambda x, **kwargs: x <= 0, lambda x, **kwargs: 0),
            (lambda x, **kwargs: x > 0, lambda x, **kwargs: min(10, 10000 * x))
        ]
        fd3 = self.piecewise_function(executed_amount_ratio, segment19)

        # 使用内部权重计算法律风险总分
        weights = self.internal_weights['legal_credit']
        return (fd1 * weights['fd1'] + fd2 * weights['fd2'] + fd3 * weights['fd3'])

    def _calculate_event_risk(self, row_idx: int) -> float:
        """计算事件风险分数"""
        # 事件风险
        # 销号率
        cancellation_rate = self._safe_divide(
            self.df['已销号个数'].iloc[row_idx],
            self.df['年初事件个数'].iloc[row_idx] + self.df['新增事件个数'].iloc[row_idx]
        )
        segment20 = [
            (lambda x, **kwargs: x >= 0.5, lambda x, **kwargs: 0),
            (lambda x, **kwargs: (x >= 0.3) and (x < 0.5), lambda x, **kwargs: 1),
            (lambda x, **kwargs: (x >= 0.2) and (x < 0.3), lambda x, **kwargs: 2),
            (lambda x, **kwargs: x < 0.2, lambda x, **kwargs: 4)
        ]
        fe1 = self.piecewise_function(cancellation_rate, segment20)
        # 影响金额消减率
        reduction_rate = self._safe_divide(
            self.df['已销号事件影响金额'].iloc[row_idx],
            self.df['年初事件影响金额'].iloc[row_idx] + self.df['新增事件影响金额'].iloc[row_idx]
        )
        segment21 = [
            (lambda x, **kwargs: x >= 0.5, lambda x, **kwargs: 0),
            (lambda x, **kwargs: (x >= 0.3) and (x < 0.5), lambda x, **kwargs: 1),
            (lambda x, **kwargs: (x >= 0.2) and (x < 0.3), lambda x, **kwargs: 2),
            (lambda x, **kwargs: x < 0.2, lambda x, **kwargs: 4)
        ]
        fe2 = self.piecewise_function(reduction_rate, segment21)
        # 降损率
        loss_rate = self._safe_divide(
            self.df['未销号事件兜底保障金额'].iloc[row_idx] + self.df['未销号事件追损挽损金额'].iloc[row_idx],
            self.df['未销号事件影响金额'].iloc[row_idx]
        )
        segment22 = [
            (lambda x, **kwargs: x >= 0.5, lambda x, **kwargs: 0),
            (lambda x, **kwargs: (x >= 0.3) and (x < 0.5), lambda x, **kwargs: 1),
            (lambda x, **kwargs: (x >= 0.2) and (x < 0.3), lambda x, **kwargs: 2),
            (lambda x, **kwargs: x < 0.2, lambda x, **kwargs: 4)
        ]
        fe3 = self.piecewise_function(loss_rate, segment22)
        # 处置化解率
        disposal_resolution_rate = self._safe_divide(
            self.df['已销号事件影响金额'].iloc[row_idx] + self.df['未销号事件兜底保障金额'].iloc[row_idx] + self.df['未销号事件追损挽损金额'].iloc[row_idx] + self.df['未销号事件累计计提减值金额'].iloc[row_idx],
            self.df['年初事件影响金额'].iloc[row_idx] +
            self.df['新增事件影响金额'].iloc[row_idx]
        )
        segment23 = [
            (lambda x, **kwargs: x >= 0.6, lambda x, **kwargs: 0),
            (lambda x, **kwargs: (x >= 0.4) and (x < 0.6), lambda x, **kwargs: 1),
            (lambda x, **kwargs: (x >= 0.2) and (x < 0.4), lambda x, **kwargs: 2),
            (lambda x, **kwargs: x < 0.2, lambda x, **kwargs: 4)
        ]
        fe4 = self.piecewise_function(disposal_resolution_rate, segment23)
        # 计提覆盖率
        provision_coverage_rate = self._safe_divide(
            self.df['未销号事件累计计提减值金额'].iloc[row_idx] ,
            self.df['未销号事件影响金额'].iloc[row_idx] - self.df['未销号事件兜底保障金额'].iloc[row_idx] -
            self.df['未销号事件追损挽损金额'].iloc[row_idx]
        )
        segment24 = [
            (lambda x, **kwargs: x >= 0.5, lambda x, **kwargs: 0),
            (lambda x, **kwargs: (x >= 0.3) and (x < 0.5), lambda x, **kwargs: 1),
            (lambda x, **kwargs: (x >= 0.2) and (x < 0.3), lambda x, **kwargs: 2),
            (lambda x, **kwargs: x < 0.2, lambda x, **kwargs: 4)
        ]
        fe5 = self.piecewise_function(provision_coverage_rate, segment24)

        # 使用内部权重计算事件风险总分
        weights = self.internal_weights['event']
        return (fe1 * weights['fe1'] + fe2 * weights['fe2'] + fe3 * weights['fe3'] + 
                fe4 * weights['fe4'] + fe5 * weights['fe5'])

    def _calculate_risk_score(self, row_idx: int) -> Dict[str, float]:
        """
        计算信用风险和社会责任风险分数
        Args:
            row_idx: 行索引
        Returns:
            包含信用风险和社会责任风险的字典
        """
        # 计算信用风险（M1）
        credit_risk = 5 * (self.df['严重失信企业数量'].iloc[row_idx] + self.df['品牌风险企业数量'].iloc[row_idx] +
                           self.df['行政处罚企业数量'].iloc[row_idx])

        # 计算社会责任风险（G）
        # 高危企业和非高危企业发生生产安全事故
        X1 = 10 * self.df['高危企业发生重大事故次数'].iloc[row_idx] + 6 * \
             self.df['高危企业发生较大事故同责及以上事故次数'].iloc[row_idx] \
             + 3 * self.df['高危企业发生较大事故次责事故次数'].iloc[row_idx] + 1 * \
             self.df['高危企业发生一般责任事故次数'].iloc[row_idx]
        Y1 = 10 * self.df['非高危企业发生较大事故同责及其以上事故次数'].iloc[row_idx] + 5 * \
             self.df['非高危企业发生较大事故次责事故次数'].iloc[row_idx] \
             + 2 * self.df['非高危企业发生一般责任事故次数'].iloc[row_idx]
        # 所有企业发生生态环境事件
        Z1 = 10 * self.df['较大生态环境事件'].iloc[row_idx] + 5 * self.df['一般生态环境事件'].iloc[row_idx]
        social_risk = X1 + Y1 + Z1

        print(f"第{row_idx}行数据的信用风险评分为：{credit_risk}")
        print(f"第{row_idx}行数据的社会责任风险评分为：{social_risk}")

        return {
            'credit_risk': credit_risk,
            'social_risk': social_risk
        }

    @staticmethod
    def _get_risk_level(score: float) -> Dict[str, str]:
        """
        根据分数确定风险等级
        Args:
            score: 风险评分
        Returns:
            包含风险等级和判断依据的字典
        """
        if score >= 90:
            return {"level": "高风险", "basis": "score"}
        elif score >= 70:
            return {"level": "中高风险", "basis": "score"}
        elif score >= 60:
            return {"level": "中低风险", "basis": "score"}
        else:
            return {"level": "低风险", "basis": "score"}

    def _check_threshold_risk(self, row_idx: int) -> Dict[str, any]:
        """
        检查是否触发阈值风险（第一层风险判断）
        Args:
            row_idx: 行索引
        Returns:
            包含是否高风险及原因的字典
        """

        # 定义阈值风险判断条件
        threshold_conditions = {
            '主业亏损金额': {
                'value': (self.df['主营业务收入'].iloc[row_idx] -
                    (self.df['主营业务成本'].iloc[row_idx] + self.df['主营业务相关费用'].iloc[row_idx])
                ),
                'threshold': 20000,
                'condition': lambda x, t: x > t
            },
            '资产负债率': {
                'value': self._safe_divide(
                    self.df['负债总额'].iloc[row_idx],
                    self.df['资产总额'].iloc[row_idx]
                ),
                'threshold': 0.9,
                'condition': lambda x, t: x > t
            },
            '带息负债率': {
                'value': self._safe_divide(
                    self.df['带息负债总额'].iloc[row_idx],
                    self.df['负债总额'].iloc[row_idx]
                ),
                'threshold': float(self.df['带息负债率行业较差值'].iloc[row_idx]) if not pd.isna(self.df['带息负债率行业较差值'].iloc[row_idx]) else 0.0,
                'condition': lambda x, t: x > t
            },
            '高危企业发生特别重大生产安全事故': {
                'value': float(self.df['高危企业发生特别重大生产安全事故次数'].iloc[row_idx]) if not pd.isna(self.df['高危企业发生特别重大生产安全事故次数'].iloc[row_idx]) else 0.0,
                'threshold': 0,
                'condition': lambda x, t: x > t
            },
            '非高危企业发生特别重大生产安全事故': {
                'value': float(self.df['非高危企业发生特别重大生产安全事故次数'].iloc[row_idx]) if not pd.isna(self.df['非高危企业发生特别重大生产安全事故次数'].iloc[row_idx]) else 0.0,
                'threshold': 0,
                'condition': lambda x, t: x > t
            },
            '企业发生重大及以上生态环境事件': {
                'value': float(self.df['企业发生重大及以上生态环境事件次数'].iloc[row_idx]) if not pd.isna(self.df['企业发生重大及以上生态环境事件次数'].iloc[row_idx]) else 0.0,
                'threshold': 0,
                'condition': lambda x, t: x > t
            },
            '经营净现金流占货币资金的比重': {
                'value': self._safe_divide(
                    self.df['经营净现金流'].iloc[row_idx],
                    self.df['货币资金'].iloc[row_idx]
                ),
                'threshold': -0.3,
                'condition': lambda x, t: x < t
            }
        }

        # 检查是否触发任何阈值条件
        triggered_conditions = []
        for indicator, config in threshold_conditions.items():
            if config['condition'](config['value'], config['threshold']):
                triggered_conditions.append(f"{indicator}={config['value']:.2f}")

        if triggered_conditions:
            return {
                "is_high_risk": True,
                "level": "高风险",
                "basis": "threshold",
                "reasons": triggered_conditions
            }
        
        return {"is_high_risk": False}

    def _calculate_risk_for_row(self, row_idx: int) -> Dict[str, float]:
        """
        计算单行数据的风险评分
        Args:
            row_idx: 行索引
        Returns:
            包含各项风险分数的字典
        """
        try:
            # 计算基础风险分数
            risk_scores = {
                'strategic': self._calculate_strategic_risk(row_idx),
                'financial': self._calculate_financial_risk(row_idx),
                'market': self._calculate_market_risk(row_idx),
                'legal_credit': self._calculate_legal_credit_risk(row_idx),
                'event': self._calculate_event_risk(row_idx)
            }
            
            return risk_scores
            
        except Exception as e:
            logger.error(f"计算第{row_idx}行风险评分时出错: {e}")
            raise

    def calculate_total_risk(self) -> List[Dict]:
        """
        计算所有行的风险评分
        
        返回:
            List[Dict]: 包含每行风险评分的列表，每个字典包含：
                - period: 期间（如月份）
                - total_score: 总风险评分
                - risk_scores: 各项风险评分
                - risk_level: 风险等级
                - risk_basis: 风险判断依据
        
        异常:
            ValueError: 当数据未加载时抛出
        
        示例:
            >>> results = model.calculate_total_risk()
            >>> for result in results:
            ...     print(f"期间: {result['period']}, 总评分: {result['total_score']}")
        """
        if self.df is None:
            raise ValueError("请先加载数据")

        results = []
        for idx in range(len(self.df)):
            try:
                # 获取当前行的索引值（可能是日期或其他标识）
                row_index = self.df.index[idx]
                
                # 首先检查是否触发阈值风险（第一层判断）
                threshold_risk = self._check_threshold_risk(idx)
                
                # 计算当前行的风险评分
                risk_scores = self._calculate_risk_for_row(idx)
                
                # 计算信用风险和社会责任风险
                additional_risks = self._calculate_risk_score(idx)
                
                # 计算总分（直接累加各项风险分数，不使用权重）
                total_score = sum(score for _, score in risk_scores.items()) + \
                             additional_risks['social_risk'] + additional_risks['credit_risk']
                
                # 确定风险等级（优先使用阈值判断结果）
                if threshold_risk["is_high_risk"]:
                    risk_level = threshold_risk
                else:
                    risk_level = self._get_risk_level(total_score)
                
                # 组织结果
                result = {
                    'period': row_index,  # 期间（如月份）
                    'total_score': total_score,
                    'risk_scores': risk_scores,
                    'credit_risk': additional_risks['credit_risk'],
                    'social_risk': additional_risks['social_risk'],
                    'risk_level': risk_level["level"],
                    'risk_basis': risk_level["basis"]
                }
                
                # 如果是阈值触发的高风险，添加具体原因
                if threshold_risk["is_high_risk"]:
                    result['risk_reasons'] = threshold_risk["reasons"]
                
                results.append(result)
                
            except Exception as e:
                logger.error(f"处理第{idx}行数据时出错: {e}")
                continue
        
        return results

    def plot_risk_scores(self, results: List[Dict], save_path: Optional[str] = None) -> None:
        """
        绘制风险评分柱状图
        
        参数:
            results (List[Dict]): 风险评分结果列表
            save_path (str, optional): 图表保存路径，如果为None则显示图表
        
        示例:
            >>> model.plot_risk_scores(results)  # 显示图表
            >>> model.plot_risk_scores(results, 'risk_chart.png')  # 保存图表
        """
        try:
            # 准备数据
            periods = [str(result['period']) for result in results]
            
            # 风险类型
            risk_types_mapping = {
                'strategic': '战略风险',
                'financial': '财务风险',
                'market': '市场风险',
                'legal_credit': '法律风险',
                'event': '事件风险'
            }
            
            risk_types = {
                'total': '总体风险',
                'credit_risk': '信用风险',
                'social_risk': '社会责任风险',
                **risk_types_mapping
            }

            # 设置中文字体
            plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
            plt.rcParams['axes.unicode_minus'] = False    # 用来正常显示负号

            # 创建图表
            fig, ax = plt.subplots(figsize=(15, 8))
            
            # 准备数据
            total_scores = [result['total_score'] for result in results]
            credit_risks = [result['credit_risk'] for result in results]
            social_risks = [result['social_risk'] for result in results]
            risk_scores = {
                risk_type: [result['risk_scores'][risk_type] for result in results]
                for risk_type in risk_types_mapping.keys()
            }

            # 设置柱状图宽度和位置
            bar_width = 0.08  # 减小柱子宽度
            spacing = 0.02   # 添加间距
            index = np.arange(len(periods))
            
            # 设置颜色
            risk_colors = {
                'financial': '#FF0000',    # 财务风险-红色
                'strategic': '#FFA500',    # 战略风险-橙色
                'market': '#FFD700',       # 市场风险-金色
                'legal_credit': '#006400', # 法律风险-深绿色
                'event': '#7CFC00',        # 事件风险-草绿色
                'credit_risk': '#FF69B4',  # 信用风险-粉色
                'social_risk': '#9370DB'   # 社会责任风险-紫色
            }
            
            # 计算总体风险柱状图的位置
            total_pos = index - 2 * (bar_width + spacing)
            
            # 绘制总分柱状图（深蓝色）
            bars_total = ax.bar(total_pos, total_scores, 
                              bar_width, label=risk_types['total'], 
                              color='#1976D2', alpha=0.9)
            
            # 在总分柱子上方添加风险等级标签
            for bar, result in zip(bars_total, results):
                height = bar.get_height()
                label_text = f'{height:.1f}\n{result["risk_level"]}'
                if "risk_reasons" in result:
                    label_text += "\n(阈值触发)"
                ax.text(bar.get_x() + bar_width/2., height,
                       label_text,
                       ha='center', va='bottom', fontsize=8)

            # 绘制信用风险柱状图（粉色）
            credit_pos = index - 1 * (bar_width + spacing)
            bars_credit = ax.bar(credit_pos, credit_risks,
                               bar_width, label=risk_types['credit_risk'],
                               color=risk_colors['credit_risk'], alpha=0.9)
            
            # 在信用风险柱子上方添加数值标签
            for bar in bars_credit:
                height = bar.get_height()
                ax.text(bar.get_x() + bar_width/2., height,
                       f'{height:.1f}', ha='center', va='bottom', fontsize=8)
            
            # 绘制社会责任风险柱状图（紫色）
            social_pos = index - 0 * (bar_width + spacing)
            bars_social = ax.bar(social_pos, social_risks,
                               bar_width, label=risk_types['social_risk'],
                               color=risk_colors['social_risk'], alpha=0.9)
            
            # 在社会责任风险柱子上方添加数值标签
            for bar in bars_social:
                height = bar.get_height()
                ax.text(bar.get_x() + bar_width/2., height,
                       f'{height:.1f}', ha='center', va='bottom', fontsize=8)

            # 绘制分项风险评分柱状图
            for i, risk_type in enumerate(risk_types_mapping.keys()):
                scores = risk_scores[risk_type]
                pos = index + (i + 1) * (bar_width + spacing)
                bars = ax.bar(pos, scores, bar_width, 
                           label=f'{risk_types_mapping[risk_type]}', 
                            color=risk_colors[risk_type], alpha=0.9)
                
                # 添加分数标签
                for bar, score in zip(bars, scores):
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar_width/2., height,
                           f'{score:.1f}', ha='center', va='bottom', fontsize=8)

            # 设置x轴刻度和标签
            ax.set_xticks(index + bar_width * 0.5)
            ax.set_xticklabels(periods, rotation=45)
            
            # 设置标题和轴标签
            ax.set_title('风险评分分析', fontsize=16, pad=20)
            ax.set_xlabel('期间', fontsize=12, labelpad=10)
            ax.set_ylabel('风险评分', fontsize=12, labelpad=10)
            
            # 显示图例
            ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
                    fancybox=True, shadow=True, ncol=4, fontsize=10)
            
            # 添加网格线
            ax.grid(axis='y', linestyle='--', alpha=0.7)
            
            # 调整y轴范围，确保所有柱状图都能显示
            max_height = max(max(total_scores), max(credit_risks), max(social_risks))
            for scores in risk_scores.values():
                max_height = max(max_height, max(scores))
            
            ax.set_ylim(0, max_height * 1.2)  # 增加20%的空间用于显示标签
            
            # 添加水平辅助线表示风险等级
            risk_thresholds = {
                "高风险": 90,
                "中高风险": 70,
                "中低风险": 60
            }
            
            for level, threshold in risk_thresholds.items():
                ax.axhline(y=threshold, linestyle='-', color='r' if level == "高风险" else 
                         'orange' if level == "中高风险" else 'g', alpha=0.5)
                ax.text(index[0] - 0.5, threshold + 1, f"{level}阈值: {threshold}", 
                       fontsize=8, va='bottom')
            
            # 调整布局
            plt.tight_layout()
            
            # 保存或显示图表
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                logger.info(f"图表已保存至: {save_path}")
            else:
                plt.show()
                
            # 关闭图表
            plt.close()

        except Exception as e:
            logger.error(f"绘制风险评分图表时出错: {e}")
            raise

    def export_calculation_details(self, results: List[Dict], output_path: str) -> None:
        """
        将所有风险评估指标及计算过程导出到Excel
        
        参数:
            results (List[Dict]): 风险评分结果列表
            output_path (str): 输出Excel文件路径
        
        示例:
            >>> model.export_calculation_details(results, 'calculation_details.xlsx')
        """
        try:
            # 创建Excel写入对象
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                # 准备基础数据
                base_data = {}
                for col in self.df.columns:
                    base_data[col] = self.df[col].tolist()
                base_data['期间'] = self.df.index.tolist()
                
                # 导出原始数据
                pd.DataFrame(base_data).to_excel(writer, sheet_name='原始数据', index=False)
                
                # 导出战略风险指标计算明细
                strategic_details = {
                    '期间': self.df.index.tolist(),
                    '主营业务收入': self.df['主营业务收入'].tolist(),
                    '营业总收入': self.df['营业总收入'].tolist(),
                    '业务集中度1': [self._safe_divide(self.df['主营业务收入'].iloc[i], self.df['营业总收入'].iloc[i]) for i in range(len(self.df))],
                    '业务集中度1得分(fa1)': [min(15, 100 * (0.85 - self._safe_divide(self.df['主营业务收入'].iloc[i], self.df['营业总收入'].iloc[i]))) if self._safe_divide(self.df['主营业务收入'].iloc[i], self.df['营业总收入'].iloc[i]) < 0.85 else 0 for i in range(len(self.df))],
                    '主营业务利润总额': self.df['主营业务利润总额'].tolist(),
                    '利润总额': self.df['利润总额'].tolist(),
                    '业务集中度2': [self._safe_divide(self.df['主营业务利润总额'].iloc[i], self.df['利润总额'].iloc[i]) for i in range(len(self.df))],
                    '业务集中度2得分(fa2)': [min(15, 300 * (0.85 - self._safe_divide(self.df['主营业务利润总额'].iloc[i], self.df['利润总额'].iloc[i]))) if self._safe_divide(self.df['主营业务利润总额'].iloc[i], self.df['利润总额'].iloc[i]) < 0.85 else 0 for i in range(len(self.df))],
                    '主营业务毛利润': self.df['主营业务毛利润'].tolist(),
                    '主业毛利率': [self._safe_divide(self.df['主营业务毛利润'].iloc[i], self.df['主营业务收入'].iloc[i]) for i in range(len(self.df))],
                    '主业毛利率行业中等值': self.df['主业毛利率行业中等值'].tolist(),
                    '主业毛利率得分(fa3)': [min(15, 500 * (self.df['主业毛利率行业中等值'].iloc[i] - self._safe_divide(self.df['主营业务毛利润'].iloc[i], self.df['主营业务收入'].iloc[i]))) if self._safe_divide(self.df['主营业务毛利润'].iloc[i], self.df['主营业务收入'].iloc[i]) < self.df['主业毛利率行业中等值'].iloc[i] else 0 for i in range(len(self.df))],
                    '研发经费投入本年累计数': self.df['研发（R&D）经费投入的本年累计数'].tolist(),
                    '研发经费投入上年同期数': self.df['研发（R&D）经费投入的上年同期数'].tolist(),
                    '研发投入增速': [self._safe_divide(self.df['研发（R&D）经费投入的本年累计数'].iloc[i], self.df['研发（R&D）经费投入的上年同期数'].iloc[i]) for i in range(len(self.df))],
                    '科技创新考核目标任务值': self.df['企业科技创新考核目标任务值'].tolist(),
                    '研发投入增速得分(fa4)': [min(15, 300 * (self.df['企业科技创新考核目标任务值'].iloc[i] - self._safe_divide(self.df['研发（R&D）经费投入的本年累计数'].iloc[i], self.df['研发（R&D）经费投入的上年同期数'].iloc[i]))) if self._safe_divide(self.df['研发（R&D）经费投入的本年累计数'].iloc[i], self.df['研发（R&D）经费投入的上年同期数'].iloc[i]) < self.df['企业科技创新考核目标任务值'].iloc[i] else 0 for i in range(len(self.df))],
                    '主营业务成本': self.df['主营业务成本'].tolist(),
                    '主营业务相关费用': self.df['主营业务相关费用'].tolist(),
                    '主营业务亏损金额': [(self.df['主营业务收入'].iloc[i] - (self.df['主营业务成本'].iloc[i] + self.df['主营业务相关费用'].iloc[i])) for i in range(len(self.df))],
                    '主营业务亏损得分(fa5)': [min(15, 3 + 3 * abs(self.df['主营业务收入'].iloc[i] - (self.df['主营业务成本'].iloc[i] + self.df['主营业务相关费用'].iloc[i])) / 5000) if (self.df['主营业务收入'].iloc[i] - (self.df['主营业务成本'].iloc[i] + self.df['主营业务相关费用'].iloc[i])) < 0 else (3 if (self.df['主营业务收入'].iloc[i] - (self.df['主营业务成本'].iloc[i] + self.df['主营业务相关费用'].iloc[i])) == 0 else 0) for i in range(len(self.df))],
                    '战略风险权重': [f'fa1({self.internal_weights["strategic"]["fa1"]}) + fa2({self.internal_weights["strategic"]["fa2"]}) + fa3({self.internal_weights["strategic"]["fa3"]}) + fa4({self.internal_weights["strategic"]["fa4"]}) + fa5({self.internal_weights["strategic"]["fa5"]})' for _ in range(len(self.df))],
                    '战略风险总分': [result['risk_scores']['strategic'] for result in results]
                }
                pd.DataFrame(strategic_details).to_excel(writer, sheet_name='战略风险', index=False)
                
                # 导出财务风险指标计算明细
                financial_details = {
                    '期间': self.df.index.tolist(),
                    '负债总额': self.df['负债总额'].tolist(),
                    '资产总额': self.df['资产总额'].tolist(),
                    '资产负债率': [self._safe_divide(self.df['负债总额'].iloc[i], self.df['资产总额'].iloc[i]) for i in range(len(self.df))],
                    '资产负债率行业中等值': self.df['资产负债率行业中等值'].tolist(),
                    '资产负债率得分(fb1)': [min(30, 500 * (self._safe_divide(self.df['负债总额'].iloc[i], self.df['资产总额'].iloc[i]) - self.df['资产负债率行业中等值'].iloc[i])) if self._safe_divide(self.df['负债总额'].iloc[i], self.df['资产总额'].iloc[i]) > self.df['资产负债率行业中等值'].iloc[i] else 0 for i in range(len(self.df))],
                    '带息负债总额': self.df['带息负债总额'].tolist(),
                    '带息负债比率': [self._safe_divide(self.df['带息负债总额'].iloc[i], self.df['负债总额'].iloc[i]) for i in range(len(self.df))],
                    '带息负债比率行业中等值': self.df['带息负债比率行业中等值'].tolist(),
                    '带息负债比率得分(fb2)': [min(30, 500 * (self._safe_divide(self.df['带息负债总额'].iloc[i], self.df['负债总额'].iloc[i]) - self.df['带息负债比率行业中等值'].iloc[i])) if self._safe_divide(self.df['带息负债总额'].iloc[i], self.df['负债总额'].iloc[i]) > self.df['带息负债比率行业中等值'].iloc[i] else 0 for i in range(len(self.df))],
                    '经营净现金流': self.df['经营净现金流'].tolist(),
                    '货币资金': self.df['货币资金'].tolist(),
                    '经营净现金流占比': [self._safe_divide(self.df['经营净现金流'].iloc[i], self.df['货币资金'].iloc[i]) for i in range(len(self.df))],
                    '经营净现金流占比得分(fb3)': [min(30, 100 * abs(self._safe_divide(self.df['经营净现金流'].iloc[i], self.df['货币资金'].iloc[i]))) if self._safe_divide(self.df['经营净现金流'].iloc[i], self.df['货币资金'].iloc[i]) <= 0 else 0 for i in range(len(self.df))],
                    '投资收益': self.df['投资收益'].tolist(),
                    '利息费用': self.df['财务费用中的利息费用'].tolist(),
                    '资本化利息支出': self.df['资本化利息支出'].tolist(),
                    '现金流与投资收益之和': [self.df['经营净现金流'].iloc[i] + self.df['投资收益'].iloc[i] for i in range(len(self.df))],
                    '利息费用总和': [self.df['财务费用中的利息费用'].iloc[i] + self.df['资本化利息支出'].iloc[i] for i in range(len(self.df))],
                    '现金流与投资收益占利息比': [self._safe_divide(self.df['经营净现金流'].iloc[i] + self.df['投资收益'].iloc[i], self.df['财务费用中的利息费用'].iloc[i] + self.df['资本化利息支出'].iloc[i]) for i in range(len(self.df))],
                    '现金流与投资收益占利息比得分(fb4)': [min(30, 700 * abs(self._safe_divide(self.df['经营净现金流'].iloc[i] + self.df['投资收益'].iloc[i], self.df['财务费用中的利息费用'].iloc[i] + self.df['资本化利息支出'].iloc[i]) - 1)) if self._safe_divide(self.df['经营净现金流'].iloc[i] + self.df['投资收益'].iloc[i], self.df['财务费用中的利息费用'].iloc[i] + self.df['资本化利息支出'].iloc[i]) < 1 else 0 for i in range(len(self.df))],
                    '财务风险权重': [f'fb1({self.internal_weights["financial"]["fb1"]}) + fb2({self.internal_weights["financial"]["fb2"]}) + fb3({self.internal_weights["financial"]["fb3"]}) + fb4({self.internal_weights["financial"]["fb4"]})' for _ in range(len(self.df))],
                    '财务风险总分': [result['risk_scores']['financial'] for result in results]
                }
                pd.DataFrame(financial_details).to_excel(writer, sheet_name='财务风险', index=False)
                
                # 导出市场风险指标计算明细
                market_details = {
                    '期间': self.df.index.tolist(),
                    '预付账款': self.df['预付账款'].tolist(),
                    '预付账款占营业总收入比重': [self._safe_divide(self.df['预付账款'].iloc[i], self.df['营业总收入'].iloc[i]) for i in range(len(self.df))],
                    '预付账款占比行业平均值': self.df['预付账款占比行业平均值'].tolist(),
                    '预付账款占比得分(fc1)': [min(25, 300 * abs(self._safe_divide(self.df['预付账款'].iloc[i], self.df['营业总收入'].iloc[i]) - self.df['预付账款占比行业平均值'].iloc[i])) if self._safe_divide(self.df['预付账款'].iloc[i], self.df['营业总收入'].iloc[i]) > self.df['预付账款占比行业平均值'].iloc[i] else 0 for i in range(len(self.df))],
                    '预收账款': self.df['预收账款'].tolist(),
                    '预收账款占资产总额比重': [self._safe_divide(self.df['预收账款'].iloc[i], self.df['资产总额'].iloc[i]) for i in range(len(self.df))],
                    '预收账款行业平均值': self.df['预收账款行业平均值'].tolist(),
                    '预收账款占比得分(fc2)': [min(25, 200 * abs(self._safe_divide(self.df['预收账款'].iloc[i], self.df['资产总额'].iloc[i]) - self.df['预收账款行业平均值'].iloc[i])) if self._safe_divide(self.df['预收账款'].iloc[i], self.df['资产总额'].iloc[i]) > self.df['预收账款行业平均值'].iloc[i] else 0 for i in range(len(self.df))],
                    '应付账款': self.df['应付账款'].tolist(),
                    '应付账款占营业总收入比重': [self._safe_divide(self.df['应付账款'].iloc[i], self.df['营业总收入'].iloc[i]) for i in range(len(self.df))],
                    '应付账款行业平均值': self.df['应付账款行业平均值'].tolist(),
                    '应付账款占比得分(fc3)': [min(25, 200 * abs(self._safe_divide(self.df['应付账款'].iloc[i], self.df['营业总收入'].iloc[i]) - self.df['应付账款行业平均值'].iloc[i])) if self._safe_divide(self.df['应付账款'].iloc[i], self.df['营业总收入'].iloc[i]) > self.df['应付账款行业平均值'].iloc[i] else 0 for i in range(len(self.df))],
                    '应收账款': self.df['应收账款'].tolist(),
                    '净资产': self.df['净资产'].tolist(),
                    '应收账款占净资产比重': [self._safe_divide(self.df['应收账款'].iloc[i], self.df['净资产'].iloc[i]) for i in range(len(self.df))],
                    '应收账款行业平均值': self.df['应收账款行业平均值'].tolist(),
                    '应收账款占比得分(fc4)': [min(25, 200 * abs(self._safe_divide(self.df['应收账款'].iloc[i], self.df['净资产'].iloc[i]) - self.df['应收账款行业平均值'].iloc[i])) if self._safe_divide(self.df['应收账款'].iloc[i], self.df['净资产'].iloc[i]) > self.df['应收账款行业平均值'].iloc[i] else 0 for i in range(len(self.df))],
                    '坏账准备金额': self.df['坏账准备金额'].tolist(),
                    '坏账准备率': [self._safe_divide(self.df['坏账准备金额'].iloc[i], self.df['应收账款'].iloc[i] + self.df['坏账准备金额'].iloc[i]) for i in range(len(self.df))],
                    '坏账准备率得分(fc5)': [min(25, 100 * abs(self._safe_divide(self.df['坏账准备金额'].iloc[i], self.df['应收账款'].iloc[i] + self.df['坏账准备金额'].iloc[i]) - 0.5)) if self._safe_divide(self.df['坏账准备金额'].iloc[i], self.df['应收账款'].iloc[i] + self.df['坏账准备金额'].iloc[i]) < 0.5 else 0 for i in range(len(self.df))],
                    '存货': self.df['存货'].tolist(),
                    '存货占净资产比重': [self._safe_divide(self.df['存货'].iloc[i], self.df['净资产'].iloc[i]) for i in range(len(self.df))],
                    '存货行业平均值': self.df['存货行业平均值'].tolist(),
                    '存货占比得分(fc6)': [min(25, 200 * abs(self._safe_divide(self.df['存货'].iloc[i], self.df['净资产'].iloc[i]) - self.df['存货行业平均值'].iloc[i])) if self._safe_divide(self.df['存货'].iloc[i], self.df['净资产'].iloc[i]) > self.df['存货行业平均值'].iloc[i] else 0 for i in range(len(self.df))],
                    '毛利润': self.df['毛利润'].tolist(),
                    '毛利润占营业总收入比重': [self._safe_divide(self.df['毛利润'].iloc[i], self.df['营业总收入'].iloc[i]) for i in range(len(self.df))],
                    '毛利率行业平均值': self.df['毛利率行业平均值'].tolist(),
                    '毛利润占比得分(fc7)': [min(25, 500 * abs(self._safe_divide(self.df['毛利润'].iloc[i], self.df['营业总收入'].iloc[i]) - self.df['毛利率行业平均值'].iloc[i])) if self._safe_divide(self.df['毛利润'].iloc[i], self.df['营业总收入'].iloc[i]) < self.df['毛利率行业平均值'].iloc[i] else 0 for i in range(len(self.df))],
                    '市场风险权重': [f'fc1({self.internal_weights["market"]["fc1"]}) + fc2({self.internal_weights["market"]["fc2"]}) + fc3({self.internal_weights["market"]["fc3"]}) + fc4({self.internal_weights["market"]["fc4"]}) + fc5({self.internal_weights["market"]["fc5"]}) + fc6({self.internal_weights["market"]["fc6"]}) + fc7({self.internal_weights["market"]["fc7"]})' for _ in range(len(self.df))],
                    '市场风险总分': [result['risk_scores']['market'] for result in results]
                }
                pd.DataFrame(market_details).to_excel(writer, sheet_name='市场风险', index=False)
                
                # 导出法律信用风险指标计算明细
                legal_credit_details = {
                    '期间': self.df.index.tolist(),
                    '当年新发生司法诉讼案件数量': self.df['企业当年新发生司法诉讼案件的数量'].tolist(),
                    '上一年司法案件数量': self.df['上一年司法案件数量'].tolist(),
                    '诉讼案件比例': [self._safe_divide(self.df['企业当年新发生司法诉讼案件的数量'].iloc[i], self.df['上一年司法案件数量'].iloc[i]) for i in range(len(self.df))],
                    '诉讼案件比例得分(fd1)': [min(10, 100 * abs(self._safe_divide(self.df['企业当年新发生司法诉讼案件的数量'].iloc[i], self.df['上一年司法案件数量'].iloc[i]) - 1)) if self._safe_divide(self.df['企业当年新发生司法诉讼案件的数量'].iloc[i], self.df['上一年司法案件数量'].iloc[i]) > 1 else 0 for i in range(len(self.df))],
                    '近一年主执行金额': self.df['近一年主执行金额'].tolist(),
                    '净资产': self.df['净资产'].tolist(),
                    '主执行金额占净资产比重': [self._safe_divide(self.df['近一年主执行金额'].iloc[i], self.df['净资产'].iloc[i]) for i in range(len(self.df))],
                    '主执行金额占比得分(fd2)': [min(10, 10000 * abs(self._safe_divide(self.df['近一年主执行金额'].iloc[i], self.df['净资产'].iloc[i]))) if self._safe_divide(self.df['近一年主执行金额'].iloc[i], self.df['净资产'].iloc[i]) > 0 else 0 for i in range(len(self.df))],
                    '近一年被执行金额': self.df['近一年被执行金额'].tolist(),
                    '被执行金额占净资产比重': [self._safe_divide(self.df['近一年被执行金额'].iloc[i], self.df['净资产'].iloc[i]) for i in range(len(self.df))],
                    '被执行金额占比得分(fd3)': [min(10, 10000 * self._safe_divide(self.df['近一年被执行金额'].iloc[i], self.df['净资产'].iloc[i])) if self._safe_divide(self.df['近一年被执行金额'].iloc[i], self.df['净资产'].iloc[i]) > 0 else 0 for i in range(len(self.df))],
                    '法律风险权重': [f'fd1({self.internal_weights["legal_credit"]["fd1"]}) + fd2({self.internal_weights["legal_credit"]["fd2"]}) + fd3({self.internal_weights["legal_credit"]["fd3"]})' for _ in range(len(self.df))],
                    '法律信用风险总分': [result['risk_scores']['legal_credit'] for result in results]
                }
                pd.DataFrame(legal_credit_details).to_excel(writer, sheet_name='法律风险', index=False)
                
                # 导出事件风险指标计算明细
                event_details = {
                    '期间': self.df.index.tolist(),
                    '已销号个数': self.df['已销号个数'].tolist(),
                    '年初事件个数': self.df['年初事件个数'].tolist(),
                    '新增事件个数': self.df['新增事件个数'].tolist(),
                    '销号率': [self._safe_divide(self.df['已销号个数'].iloc[i], self.df['年初事件个数'].iloc[i] + self.df['新增事件个数'].iloc[i]) for i in range(len(self.df))],
                    '销号率得分(fe1)': [0 if self._safe_divide(self.df['已销号个数'].iloc[i], self.df['年初事件个数'].iloc[i] + self.df['新增事件个数'].iloc[i]) >= 0.5 else (1 if self._safe_divide(self.df['已销号个数'].iloc[i], self.df['年初事件个数'].iloc[i] + self.df['新增事件个数'].iloc[i]) >= 0.3 else (2 if self._safe_divide(self.df['已销号个数'].iloc[i], self.df['年初事件个数'].iloc[i] + self.df['新增事件个数'].iloc[i]) >= 0.2 else 4)) for i in range(len(self.df))],
                    '已销号事件影响金额': self.df['已销号事件影响金额'].tolist(),
                    '年初事件影响金额': self.df['年初事件影响金额'].tolist(),
                    '新增事件影响金额': self.df['新增事件影响金额'].tolist(),
                    '影响金额消减率': [self._safe_divide(self.df['已销号事件影响金额'].iloc[i], self.df['年初事件影响金额'].iloc[i] + self.df['新增事件影响金额'].iloc[i]) for i in range(len(self.df))],
                    '影响金额消减率得分(fe2)': [0 if self._safe_divide(self.df['已销号事件影响金额'].iloc[i], self.df['年初事件影响金额'].iloc[i] + self.df['新增事件影响金额'].iloc[i]) >= 0.5 else (1 if self._safe_divide(self.df['已销号事件影响金额'].iloc[i], self.df['年初事件影响金额'].iloc[i] + self.df['新增事件影响金额'].iloc[i]) >= 0.3 else (2 if self._safe_divide(self.df['已销号事件影响金额'].iloc[i], self.df['年初事件影响金额'].iloc[i] + self.df['新增事件影响金额'].iloc[i]) >= 0.2 else 4)) for i in range(len(self.df))],
                    '未销号事件兜底保障金额': self.df['未销号事件兜底保障金额'].tolist(),
                    '未销号事件追损挽损金额': self.df['未销号事件追损挽损金额'].tolist(),
                    '未销号事件影响金额': self.df['未销号事件影响金额'].tolist(),
                    '降损率': [self._safe_divide(self.df['未销号事件兜底保障金额'].iloc[i] + self.df['未销号事件追损挽损金额'].iloc[i], self.df['未销号事件影响金额'].iloc[i]) for i in range(len(self.df))],
                    '降损率得分(fe3)': [0 if self._safe_divide(self.df['未销号事件兜底保障金额'].iloc[i] + self.df['未销号事件追损挽损金额'].iloc[i], self.df['未销号事件影响金额'].iloc[i]) >= 0.5 else (1 if self._safe_divide(self.df['未销号事件兜底保障金额'].iloc[i] + self.df['未销号事件追损挽损金额'].iloc[i], self.df['未销号事件影响金额'].iloc[i]) >= 0.3 else (2 if self._safe_divide(self.df['未销号事件兜底保障金额'].iloc[i] + self.df['未销号事件追损挽损金额'].iloc[i], self.df['未销号事件影响金额'].iloc[i]) >= 0.2 else 4)) for i in range(len(self.df))],
                    '处置化解率分子': [self.df['已销号事件影响金额'].iloc[i] + self.df['未销号事件兜底保障金额'].iloc[i] + self.df['未销号事件追损挽损金额'].iloc[i] + self.df['未销号事件累计计提减值金额'].iloc[i] for i in range(len(self.df))],
                    '处置化解率分母': [self.df['年初事件影响金额'].iloc[i] + self.df['新增事件影响金额'].iloc[i] for i in range(len(self.df))],
                    '处置化解率': [self._safe_divide(self.df['已销号事件影响金额'].iloc[i] + self.df['未销号事件兜底保障金额'].iloc[i] + self.df['未销号事件追损挽损金额'].iloc[i] + self.df['未销号事件累计计提减值金额'].iloc[i], self.df['年初事件影响金额'].iloc[i] + self.df['新增事件影响金额'].iloc[i]) for i in range(len(self.df))],
                    '处置化解率得分(fe4)': [0 if self._safe_divide(self.df['已销号事件影响金额'].iloc[i] + self.df['未销号事件兜底保障金额'].iloc[i] + self.df['未销号事件追损挽损金额'].iloc[i] + self.df['未销号事件累计计提减值金额'].iloc[i], self.df['年初事件影响金额'].iloc[i] + self.df['新增事件影响金额'].iloc[i]) >= 0.6 else (1 if self._safe_divide(self.df['已销号事件影响金额'].iloc[i] + self.df['未销号事件兜底保障金额'].iloc[i] + self.df['未销号事件追损挽损金额'].iloc[i] + self.df['未销号事件累计计提减值金额'].iloc[i], self.df['年初事件影响金额'].iloc[i] + self.df['新增事件影响金额'].iloc[i]) >= 0.4 else (2 if self._safe_divide(self.df['已销号事件影响金额'].iloc[i] + self.df['未销号事件兜底保障金额'].iloc[i] + self.df['未销号事件追损挽损金额'].iloc[i] + self.df['未销号事件累计计提减值金额'].iloc[i], self.df['年初事件影响金额'].iloc[i] + self.df['新增事件影响金额'].iloc[i]) >= 0.2 else 4)) for i in range(len(self.df))],
                    '未销号事件累计计提减值金额': self.df['未销号事件累计计提减值金额'].tolist(),
                    '计提覆盖率分子': [self.df['未销号事件累计计提减值金额'].iloc[i] for i in range(len(self.df))],
                    '计提覆盖率分母': [self.df['未销号事件影响金额'].iloc[i] - self.df['未销号事件兜底保障金额'].iloc[i] - self.df['未销号事件追损挽损金额'].iloc[i] for i in range(len(self.df))],
                    '计提覆盖率': [self._safe_divide(self.df['未销号事件累计计提减值金额'].iloc[i], self.df['未销号事件影响金额'].iloc[i] - self.df['未销号事件兜底保障金额'].iloc[i] - self.df['未销号事件追损挽损金额'].iloc[i]) for i in range(len(self.df))],
                    '计提覆盖率得分(fe5)': [0 if self._safe_divide(self.df['未销号事件累计计提减值金额'].iloc[i], self.df['未销号事件影响金额'].iloc[i] - self.df['未销号事件兜底保障金额'].iloc[i] - self.df['未销号事件追损挽损金额'].iloc[i]) >= 0.5 else (1 if self._safe_divide(self.df['未销号事件累计计提减值金额'].iloc[i], self.df['未销号事件影响金额'].iloc[i] - self.df['未销号事件兜底保障金额'].iloc[i] - self.df['未销号事件追损挽损金额'].iloc[i]) >= 0.3 else (2 if self._safe_divide(self.df['未销号事件累计计提减值金额'].iloc[i], self.df['未销号事件影响金额'].iloc[i] - self.df['未销号事件兜底保障金额'].iloc[i] - self.df['未销号事件追损挽损金额'].iloc[i]) >= 0.2 else 4)) for i in range(len(self.df))],
                    '事件风险权重': [f'fe1({self.internal_weights["event"]["fe1"]}) + fe2({self.internal_weights["event"]["fe2"]}) + fe3({self.internal_weights["event"]["fe3"]}) + fe4({self.internal_weights["event"]["fe4"]}) + fe5({self.internal_weights["event"]["fe5"]})' for _ in range(len(self.df))],
                    '事件风险总分': [result['risk_scores']['event'] for result in results]
                }
                pd.DataFrame(event_details).to_excel(writer, sheet_name='事件风险', index=False)
                
                # 导出信用风险和社会责任风险指标计算明细
                additional_risks = {
                    '期间': self.df.index.tolist(),
                    '严重失信企业数量': self.df['严重失信企业数量'].tolist(),
                    '品牌风险企业数量': self.df['品牌风险企业数量'].tolist(),
                    '行政处罚企业数量': self.df['行政处罚企业数量'].tolist(),
                    '信用风险计算公式': ['5 * (严重失信企业数量 + 品牌风险企业数量 + 行政处罚企业数量)' for _ in range(len(self.df))],
                    '信用风险分数': [result['credit_risk'] for result in results],
                    '高危企业发生重大事故次数': self.df['高危企业发生重大事故次数'].tolist(),
                    '高危企业发生较大事故同责及以上事故次数': self.df['高危企业发生较大事故同责及以上事故次数'].tolist(),
                    '高危企业发生较大事故次责事故次数': self.df['高危企业发生较大事故次责事故次数'].tolist(),
                    '高危企业发生一般责任事故次数': self.df['高危企业发生一般责任事故次数'].tolist(),
                    '非高危企业发生较大事故同责及其以上事故次数': self.df['非高危企业发生较大事故同责及其以上事故次数'].tolist(),
                    '非高危企业发生较大事故次责事故次数': self.df['非高危企业发生较大事故次责事故次数'].tolist(),
                    '非高危企业发生一般责任事故次数': self.df['非高危企业发生一般责任事故次数'].tolist(),
                    '高危企业安全事故得分(X1)': [10 * self.df['高危企业发生重大事故次数'].iloc[i] + 6 * self.df['高危企业发生较大事故同责及以上事故次数'].iloc[i] + 3 * self.df['高危企业发生较大事故次责事故次数'].iloc[i] + 1 * self.df['高危企业发生一般责任事故次数'].iloc[i] for i in range(len(self.df))],
                    '非高危企业安全事故得分(Y1)': [10 * self.df['非高危企业发生较大事故同责及其以上事故次数'].iloc[i] + 5 * self.df['非高危企业发生较大事故次责事故次数'].iloc[i] + 2 * self.df['非高危企业发生一般责任事故次数'].iloc[i] for i in range(len(self.df))],
                    '较大生态环境事件': self.df['较大生态环境事件'].tolist(),
                    '一般生态环境事件': self.df['一般生态环境事件'].tolist(),
                    '生态环境事件得分(Z1)': [10 * self.df['较大生态环境事件'].iloc[i] + 5 * self.df['一般生态环境事件'].iloc[i] for i in range(len(self.df))],
                    '社会责任风险计算公式': ['X1 + Y1 + Z1' for _ in range(len(self.df))],
                    '社会责任风险分数': [result['social_risk'] for result in results]
                }
                pd.DataFrame(additional_risks).to_excel(writer, sheet_name='信用与社会责任风险', index=False)
                
                # 导出阈值风险指标计算明细
                threshold_risks = {
                    '期间': self.df.index.tolist(),
                    '主营业务收入': self.df['主营业务收入'].tolist(),
                    '主营业务成本': self.df['主营业务成本'].tolist(),
                    '主营业务相关费用': self.df['主营业务相关费用'].tolist(),
                    '主业亏损金额': [(self.df['主营业务收入'].iloc[i] - (self.df['主营业务成本'].iloc[i] + self.df['主营业务相关费用'].iloc[i])) for i in range(len(self.df))],
                    '主业亏损阈值': [20000 for _ in range(len(self.df))],
                    '主业亏损状态': [((self.df['主营业务收入'].iloc[i] - (self.df['主营业务成本'].iloc[i] + self.df['主营业务相关费用'].iloc[i])) > 20000) for i in range(len(self.df))],
                    '资产负债率': [self._safe_divide(self.df['负债总额'].iloc[i], self.df['资产总额'].iloc[i]) for i in range(len(self.df))],
                    '资产负债率阈值': [0.9 for _ in range(len(self.df))],
                    '资产负债率状态': [(self._safe_divide(self.df['负债总额'].iloc[i], self.df['资产总额'].iloc[i]) > 0.9) for i in range(len(self.df))],
                    '带息负债率': [self._safe_divide(self.df['带息负债总额'].iloc[i], self.df['负债总额'].iloc[i]) for i in range(len(self.df))],
                    '带息负债率行业较差值': [float(self.df['带息负债率行业较差值'].iloc[i]) if not pd.isna(self.df['带息负债率行业较差值'].iloc[i]) else 0.0 for i in range(len(self.df))],
                    '带息负债率状态': [(self._safe_divide(self.df['带息负债总额'].iloc[i], self.df['负债总额'].iloc[i]) > float(self.df['带息负债率行业较差值'].iloc[i]) if not pd.isna(self.df['带息负债率行业较差值'].iloc[i]) else 0.0) for i in range(len(self.df))],
                    '高危企业发生特别重大生产安全事故次数': [float(self.df['高危企业发生特别重大生产安全事故次数'].iloc[i]) if not pd.isna(self.df['高危企业发生特别重大生产安全事故次数'].iloc[i]) else 0.0 for i in range(len(self.df))],
                    '特别重大事故阈值': [0 for _ in range(len(self.df))],
                    '特别重大事故状态': [(float(self.df['高危企业发生特别重大生产安全事故次数'].iloc[i]) if not pd.isna(self.df['高危企业发生特别重大生产安全事故次数'].iloc[i]) else 0.0) > 0 for i in range(len(self.df))],
                    '阈值触发状态': ['触发' if any([
                        ((self.df['主营业务收入'].iloc[i] - (self.df['主营业务成本'].iloc[i] + self.df['主营业务相关费用'].iloc[i])) > 20000),
                        (self._safe_divide(self.df['负债总额'].iloc[i], self.df['资产总额'].iloc[i]) > 0.9),
                        (self._safe_divide(self.df['带息负债总额'].iloc[i], self.df['负债总额'].iloc[i]) > float(self.df['带息负债率行业较差值'].iloc[i]) if not pd.isna(self.df['带息负债率行业较差值'].iloc[i]) else 0.0),
                        ((float(self.df['高危企业发生特别重大生产安全事故次数'].iloc[i]) if not pd.isna(self.df['高危企业发生特别重大生产安全事故次数'].iloc[i]) else 0.0) > 0)
                    ]) else '未触发' for i in range(len(self.df))],
                    '阈值判断结果': ['高风险' if any([
                        ((self.df['主营业务收入'].iloc[i] - (self.df['主营业务成本'].iloc[i] + self.df['主营业务相关费用'].iloc[i])) > 20000),
                        (self._safe_divide(self.df['负债总额'].iloc[i], self.df['资产总额'].iloc[i]) > 0.9),
                        (self._safe_divide(self.df['带息负债总额'].iloc[i], self.df['负债总额'].iloc[i]) > float(self.df['带息负债率行业较差值'].iloc[i]) if not pd.isna(self.df['带息负债率行业较差值'].iloc[i]) else 0.0),
                        ((float(self.df['高危企业发生特别重大生产安全事故次数'].iloc[i]) if not pd.isna(self.df['高危企业发生特别重大生产安全事故次数'].iloc[i]) else 0.0) > 0)
                    ]) else '未触发高风险' for i in range(len(self.df))]
                }
                pd.DataFrame(threshold_risks).to_excel(writer, sheet_name='阈值风险', index=False)
                
                # 导出总风险评分
                total_risk = {
                    '期间': self.df.index.tolist(),
                    '战略风险分数': [result['risk_scores']['strategic'] for result in results],
                    '财务风险分数': [result['risk_scores']['financial'] for result in results],
                    '市场风险分数': [result['risk_scores']['market'] for result in results],
                    '法律信用风险分数': [result['risk_scores']['legal_credit'] for result in results],
                    '事件风险分数': [result['risk_scores']['event'] for result in results],
                    '信用风险分数': [result['credit_risk'] for result in results],
                    '社会责任风险分数': [result['social_risk'] for result in results],
                    '总风险分数': [result['total_score'] for result in results],
                    '总风险计算方式': ['直接相加各项风险分数：战略风险分数 + 财务风险分数 + 市场风险分数 + 法律信用风险分数 + 事件风险分数 + 信用风险分数 + 社会责任风险分数' for _ in range(len(self.df))],
                    '风险等级': [result['risk_level'] for result in results],
                    '判断依据': [result['risk_basis'] for result in results],
                    '阈值判断结果': ['高风险' if any([
                         ((self.df['主营业务收入'].iloc[i] - (self.df['主营业务成本'].iloc[i] + self.df['主营业务相关费用'].iloc[i])) > 20000),
                         (self._safe_divide(self.df['负债总额'].iloc[i], self.df['资产总额'].iloc[i]) > 0.9),
                         (self._safe_divide(self.df['带息负债总额'].iloc[i], self.df['负债总额'].iloc[i]) > float(self.df['带息负债率行业较差值'].iloc[i]) if not pd.isna(self.df['带息负债率行业较差值'].iloc[i]) else 0.0),
                         ((float(self.df['高危企业发生特别重大生产安全事故次数'].iloc[i]) if not pd.isna(self.df['高危企业发生特别重大生产安全事故次数'].iloc[i]) else 0.0) > 0)
                     ]) else '未触发高风险' for i in range(len(self.df))]
                }
                pd.DataFrame(total_risk).to_excel(writer, sheet_name='总风险', index=False)

                logger.info(f"计算明细已导出至 {output_path}")
                return output_path
        except Exception as e:
            logger.error(f"导出计算详情时出错: {e}")
            raise

