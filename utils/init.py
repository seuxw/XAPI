#!/usr/bin/python3
# -*- coding: utf-8 -*-
# 初始化运行环境及配置


import configparser
import getpass


def default_input(content, default):
    res = input(content)
    return res if res else default


def create_auth_cfg():
    """创建 auth 配置文件."""
    print("\nStart create auth config file")
    CONFIG_FILE = "./auth/auth.cfg"
    conf = configparser.ConfigParser()
    conf.add_section('AUTH_CFG')

    header = default_input(
        "? Authorization header (Authorization)", "Authorization")
    conf.set('AUTH_CFG', 'authorization_header', header)

    method = default_input("? Authorization method (Bearer)", "Bearer")
    conf.set('AUTH_CFG', 'authorization_method', method)

    algorithms = default_input("? Algorithms (HS256)", "HS256")
    conf.set('AUTH_CFG', 'algorithms', algorithms)

    key = getpass.getpass("* Secret key: ")
    conf.set('AUTH_CFG', 'secret_key', key)

    client = input("? Client id: ")
    conf.set('AUTH_CFG', 'client_id', client)

    conf.write(open(CONFIG_FILE, 'w'))
    print("Finish create auth config file\n")


def create_database_cfg():
    """创建 database 配置文件."""
    print("Start create database config file")
    CONFIG_FILE = "./database/database.cfg"
    conf = configparser.ConfigParser()
    conf.add_section('DATABASE_INFO')

    host = default_input("? Host (localhost)", "localhost")
    conf.set('DATABASE_INFO', 'host', host)

    port = default_input("? Port (3306)", "3306")
    conf.set('DATABASE_INFO', 'port', port)

    user = default_input("? User (root)", "root")
    conf.set('DATABASE_INFO', 'user', user)

    passwd = getpass.getpass("* Password: ")
    conf.set('DATABASE_INFO', 'passwd', passwd)

    db = input("? Database: ")
    conf.set('DATABASE_INFO', 'db', db)

    charset = default_input("? Charset (utf8)", "utf8")
    conf.set('DATABASE_INFO', 'charset', charset)

    max_connections = default_input("? Max connections (5)", "5")
    conf.set('DATABASE_INFO', 'max_connections', max_connections)

    idle_seconds = default_input("? Idle seconds (600)", "600")
    conf.set('DATABASE_INFO', 'idle_seconds', idle_seconds)

    wait_connection_timeout = default_input(
        "? Wait connection timeout (3)", "3")
    conf.set('DATABASE_INFO', 'wait_connection_timeout',
             wait_connection_timeout)

    conf.write(open(CONFIG_FILE, 'w'))
    print("Finish create database config file\n")


def create_paocao_cfg():
    """创建跑操爬虫配置文件."""
    print("\nStart create spider paocao config file")
    CONFIG_FILE = "./utils/spider_paocao_cookie/paocao.cfg"
    conf = configparser.ConfigParser()
    conf.add_section('CARD_INFO')

    cardno = input("? 一卡通号: ")
    conf.set('CARD_INFO', 'cardno', cardno)

    cardpswd = getpass.getpass("* 一卡通密码: ")
    conf.set('CARD_INFO', 'cardpswd', cardpswd)

    conf.write(open(CONFIG_FILE, 'w'))
    print("Finish create spider paocao config file\n")


def create_redis_cfg():
    """创建 Redis 配置文件."""
    print("\nStart create Redis config file")
    CONFIG_FILE = "./database/redis.cfg"
    conf = configparser.ConfigParser()
    conf.add_section('REDIS_INFO')

    host = default_input("? Host (localhost)", "localhost")
    conf.set('REDIS_INFO', 'host', host)

    port = default_input("? Port (6379)", "6379")
    conf.set('REDIS_INFO', 'port', port)

    db = input("? Db: ")
    conf.set('REDIS_INFO', 'db', db)

    conf.write(open(CONFIG_FILE, 'w'))
    print("Finish create spider paocao config file\n")


def init():
    create_auth_cfg()
    # create_database_cfg()
    # create_paocao_cfg()
