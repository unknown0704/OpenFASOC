import warnings
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from common.get_ngspice_version import check_ngspice_version
            
def classify_sim_error(template_file, result_file, compare_files) -> str:
    """Used to propogate out how close the generated simulations results are 
    from the results in the stored template files

    Args:
    - 'template_file' (string): The stored template file
    - 'result_file' (string): The result file generated by the simulations
    - 'compare_files' (function): The simulation file comparison function imported from a specific generator's tools/ directory
    Returns:
    - str: The kind of alert
        - 'red' alert for very large difference in generated and template results (> max allowable error)
        - 'amber' alert if the difference lies within the allowable range (min allowable error < . < max allowable error)
        - 'green' if ok (< min allowable error)
    """
   
    ngspice_check_flag = check_ngspice_version()
    alerts = { 0: 'green', 1: 'amber', 2: 'red' }
    
    
    if ngspice_check_flag:
        if compare_files(template_file, result_file) == 0:
            return alerts[0]
        elif compare_files(template_file, result_file) == 1:
            warnings.warn('Simulation results do not match, but ngspice version matches!')
            return alerts[1]
        else:
            return alerts[2]
        
    elif ngspice_check_flag == 0:
        warnings.warn('NGSPICE version does not match!')
        if compare_files(template_file, result_file) == 0:
            return alerts[0]
        elif compare_files(template_file, result_file) == 1:
            warnings.warn('Simulation results do not match!')
            return alerts[1]
        else:
            return alerts[2]
