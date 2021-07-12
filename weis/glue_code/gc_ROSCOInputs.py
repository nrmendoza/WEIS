def assign_ROSCO_values(wt_opt, modeling_options, control):
    # ROSCO tuning parameters
    rosco_init_options = modeling_options['ROSCO']

    # Pitch regulation
    wt_opt['tune_rosco_ivc.PC_omega']      = rosco_init_options['omega_pc']
    wt_opt['tune_rosco_ivc.PC_zeta']       = rosco_init_options['zeta_pc']
    if not (len(rosco_init_options['omega_pc']) == \
        len(rosco_init_options['zeta_pc']) == \
        len(rosco_init_options['U_pc'])):
        raise Exception('omega_pc, zeta_pc, and U_pc must have the same number of elements in the modeling options')

    # Torque control
    wt_opt['tune_rosco_ivc.VS_omega']      = rosco_init_options['omega_vs']
    wt_opt['tune_rosco_ivc.VS_zeta']       = rosco_init_options['zeta_vs']
    
    # Flap control params
    if modeling_options['ROSCO']['Flp_Mode'] > 0:
        try:
            wt_opt['tune_rosco_ivc.Flp_omega']      = control['dac']['Flp_omega']
            wt_opt['tune_rosco_ivc.Flp_zeta']       = control['dac']['Flp_zeta']
        except:
            raise Exception('If Flp_Mode > 0, you must set Flp_omega, Flp_zeta in the modeling options')

    if 'IPC' in control.keys():
        wt_opt['tune_rosco_ivc.IPC_KI']      = control['IPC']['IPC_gain_1P']
    # # other optional parameters
    wt_opt['tune_rosco_ivc.max_pitch']     = rosco_init_options['max_pitch']
    wt_opt['tune_rosco_ivc.min_pitch']     = rosco_init_options['min_pitch']
    wt_opt['tune_rosco_ivc.vs_minspd']     = rosco_init_options['vs_minspd']
    wt_opt['tune_rosco_ivc.ss_vsgain']     = rosco_init_options['ss_vsgain']
    wt_opt['tune_rosco_ivc.ss_pcgain']     = rosco_init_options['ss_pcgain']
    wt_opt['tune_rosco_ivc.ps_percent']    = rosco_init_options['ps_percent']
    
    if modeling_options['ROSCO']['Fl_Mode']:
        try:
            wt_opt['tune_rosco_ivc.twr_freq']      = rosco_init_options['twr_freq']
            wt_opt['tune_rosco_ivc.ptfm_freq']     = rosco_init_options['ptfm_freq']
            if 'Kp_float' in rosco_init_options:
                wt_opt['tune_rosco_ivc.Kp_float']      = rosco_init_options['Kp_float']
        except:
            raise Exception('If Fl_Mode > 0, you must set twr_freq and ptfm_freq in modeling options')
        
    # Check for proper Flp_Mode, print warning
    if modeling_options['WISDEM']['RotorSE']['n_tab'] > 1 and modeling_options['ROSCO']['Flp_Mode'] == 0:
            raise Exception('A distributed aerodynamic control device is specified in the geometry yaml, but Flp_Mode is zero in the modeling options.')
    if modeling_options['WISDEM']['RotorSE']['n_tab'] == 1 and modeling_options['ROSCO']['Flp_Mode'] > 0:
            raise Exception('Flp_Mode is non zero in the modeling options, but no distributed aerodynamic control device is specified in the geometry yaml.')

    return wt_opt
