class topics(object):
    def __init__(self):
        # name for the topic. Sequenced.
        self.names =    [   "1_L_ARM_EL_Y_POSITION_STATE",  
                            "2_L_ARM_GRIP_L_POSITION_STATE", 
                            "3_L_ARM_GRIP_POSITION_STATE",
                            "4_L_ARM_SH_P1_POSITION_STATE", 
                            "5_L_ARM_SH_P2_POSITION_STATE", 
                            "6_L_ARM_SH_R_POSITION_STATE", 
                            "7_L_ARM_WR_P_POSITION_STATE",
                            "8_L_ARM_WR_R_POSITION_STATE",
                            "9_L_ARM_WR_Y_POSITION_STATE",
                        ]
        # list of all publisher topics
        self.pubList =  [   
                            '/thormang3/l_arm_el_y_position/command',  # -1.3 to 1.3
                            '/thormang3/l_arm_grip_1_position/command', # 0 to 1.2
                            '/thormang3/l_arm_grip_position/command', # 0 to 1.1
                            '/thormang3/l_arm_sh_p1_position/command', # -1.6 to 1.6
                            '/thormang3/l_arm_sh_p2_position/command', # -1.6 to 1.6
                            '/thormang3/l_arm_sh_r_position/command', # -1.6 to 1.6
                            '/thormang3/l_arm_wr_p_position/command', # -1.4 to 1.4
                            '/thormang3/l_arm_wr_r_position/command', # -2.8 to 2.8
                            '/thormang3/l_arm_wr_y_position/command' # 1.4 to 1.4
                        ]
        # list of all subscriber topics
        self.subList =  [   
                            '/thormang3/l_arm_el_y_position/state',  
                            '/thormang3/l_arm_grip_1_position/state',
                            '/thormang3/l_arm_grip_position/state',
                            '/thormang3/l_arm_sh_p1_position/state',
                            '/thormang3/l_arm_sh_p2_position/state',
                            '/thormang3/l_arm_sh_r_position/state',
                            '/thormang3/l_arm_wr_p_position/state',
                            '/thormang3/l_arm_wr_r_position/state',
                            '/thormang3/l_arm_wr_y_position/state'
                        ]
        # movement
        self.movement1 =  [
                                [-0.5, -0.5, -0.5, -0.5, 0, 0, 0], 
                                [0.0, 0.0, 0.7, 0.7, 0.7, 0.7, 0],  
                                [0.0, 0.0, 0.7, 0.7, 0.7, 0.7, 0],  
                                [-0.5, -0.18, -0.18, -0.5, 0, 0, 0],
                                [0, 0, 0.0, 0.0, 0.0, 0.0, 0], 
                                [1.5, 1.5, 1.5, 1.5, 0, 0, 0],
                                [0, 0, 0.0, 0.0, 0.0, -1.0, -1.0], 
                                [1.5, 1.5, 1.5, 1.5, 0, 0, 0], 
                                [0, 0, 0.0, 0.0, 0, 0, 0], 
                            ]           


