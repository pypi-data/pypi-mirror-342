from main import RiskModel
import pandas as pd

def main():
    # 创建模型实例
    risk_model = RiskModel(config_path='config.yaml')  # 或者 RiskModel() 使用默认配置
    
    try:
        # 加载数据（假设Excel文件格式为：第一列是指标名称，后续列为各月份数据）
        risk_model.load_data('test.xlsx', sheet_name='Sheet3')

        # 计算所有月份的风险
        results = risk_model.calculate_total_risk()
        
        # 输出结果
        print("\n=== 风险评估结果 ===")
        for result in results:
            print(f"\n期间: {result['period']}月")
            print(f"总风险评分: {result['total_score']:.2f}")
            print(f"风险等级: {result['risk_level']}")
            if result.get('risk_basis') == 'threshold':
                print("【A类风险】触发原因：")
                for reason in result['risk_reasons']:
                    print(f"  - {reason}")
            print("各项风险评分:")
            for risk_type, score in result['risk_scores'].items():
                print(f"  {risk_type}: {score:.2f}")
            print(f"  信用风险: {result['credit_risk']:.2f}")
            print(f"  社会责任风险: {result['social_risk']:.2f}")
        
        # 将结果保存到Excel文件
        # 创建结果DataFrame
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
        if any(result.get('risk_basis') == 'threshold' for result in results):
            df_results['A类风险触发原因'] = [
                '\n'.join(result.get('risk_reasons', [])) if result.get('risk_basis') == 'threshold' else ''
                for result in results
            ]
        
        # 保存到Excel
        excel_path = 'risk_assessment_results.xlsx'
        df_results.to_excel(excel_path, index=False, sheet_name='风险评估结果')
        print(f"\n结果已保存至: {excel_path}")
        
        # 导出计算详情到Excel
        details_path = 'risk_calculation_details.xlsx'
        risk_model.export_calculation_details(results, details_path)
        print(f"计算详情已保存至: {details_path}")
        
        # 绘制并保存风险评分柱状图
        chart_path = 'risk_assessment_chart.png'
        risk_model.plot_risk_scores(results, save_path=chart_path)
        print(f"图表已保存至: {chart_path}")
            
    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    main() 