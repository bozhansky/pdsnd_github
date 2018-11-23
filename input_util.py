#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 13:17:22 2018

@author: bostjan
"""

def get_user_input(message, data_list, errormsg):
    """
    An utility function to obtain user specific input value
    Args:
        (str) message - an information message for a particular request
    Returns:
        (str) user_data - requested data from user
    """

    while True:
        user_data = input(message).lower()
        if user_data in data_list:
            break
        elif user_data == 'all':
            break
        else:
            print(errormsg)
            print()
    return user_data
