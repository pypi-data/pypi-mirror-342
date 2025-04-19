from .main import RiskModel
import pandas as pd
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def assess_risk(excel_path, sheet_name=None, config_path=None):
    """
    风险评估主函数
    
    参数:
        excel_path (str): Excel文件路径
        sheet_name (str, optional): 工作表名称，默认为None（读取第一个工作表）
        config_path (str, optional): 配置文件路径，默认为None（使用默认配置）
    
    返回:
        dict: 包含风险评估结果的字典，包括：
            - results: 风险评估结果列表
            - chart_path: 图表保存路径
            - details_path: 计算详情保存路径
    """
    try:
        # 创建模型实例
        risk_model = RiskModel(config_path=config_path)
        
        # 加载数据
        risk_model.load_data(excel_path, sheet_name=sheet_name)
        
        # 计算风险
        results = risk_model.calculate_total_risk()
        
        # 保存结果到Excel
        df_results = pd.DataFrame([
            {
                '月份': result['period'],
                '总风险评分': result['total_score'],
                '风险等级': result['risk_level'],
                '风险判断依据': result['risk_basis'],
                '战略风险': result['risk_scores']['strategic'],
                '财务风险': result['risk_scores']['financial'],
                '市场风险': result['risk_scores']['market'],
                '法律信用风险': result['risk_scores']['legal_credit'],
                '事件风险': result['risk_scores']['event'],
                '信用风险': result['credit_risk'],
                '社会责任风险': result['social_risk']
            }
            for result in results
        ])
        
        # 如果有A类风险，添加触发原因
        if any('risk_reasons' in result for result in results):
            df_results['A类风险触发原因'] = [
                '\n'.join(result.get('risk_reasons', [])) 
                for result in results
            ]
        
        # 生成输出文件路径
        import os
        base_path = os.path.splitext(excel_path)[0]
        results_path = f"{base_path}_results.xlsx"
        details_path = f"{base_path}_details.xlsx"
        chart_path = f"{base_path}_chart.png"
        
        # 保存结果
        df_results.to_excel(results_path, index=False, sheet_name='风险评估结果')
        risk_model.export_calculation_details(results, details_path)
        risk_model.plot_risk_scores(results, save_path=chart_path)
        
        logger.info(f"风险评估完成！")
        logger.info(f"结果文件已保存至: {results_path}")
        logger.info(f"计算详情已保存至: {details_path}")
        logger.info(f"图表已保存至: {chart_path}")
        
        return {
            'results': results,
            'results_path': results_path,
            'details_path': details_path,
            'chart_path': chart_path
        }
        
    except Exception as e:
        logger.error(f"风险评估过程中出错: {e}")
        raise 