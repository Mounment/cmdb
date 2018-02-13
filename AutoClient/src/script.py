#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__= 'luhj'
from src.client import AutoAgent
from src.client import AutoSalt
from src.client import AutoSSH
from config import settings

def client()
    if settings.MODE == 'agent':
        cli = AutoAgent()
    elif settings.MODE == 'ssh':
        cli = AutoSSH()
    elif settings.MODE == 'salt':
        cli = AutoSalt()
    else:
        raise Exception('资产采集模式配置错误[ssh,agent,salt]')
    cli.process()