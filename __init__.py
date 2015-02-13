from core.configuration import ConfigurationObject
name = "WaterBalanceModel"
identifier = "gov.usgs.WaterBalanceModel"
version = '0.0.1'

def packagedependencies():
    return ['edu.utah.sci.vistrials.matplotlib']

configuration = \
    ConfigurationObject(output_dir = r'C:\temp\WaterBalanceModule_workspace',
                        r_path = r'..\\..\\Central_R\R-2.14.1\bin',
                        maxent_path = r'..\\..\\Central_Maxent',
                        cur_session_folder = r'C:\temp\WaterBalanceModule_workspace',
                        cur_processing_mode = "multiple cores asynchronously",
                        verbose = "True")