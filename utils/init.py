#!/usr/bin/python3
# -*- coding: utf-8 -*-
# 初始化运行环境及配置


import configparser


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
    conf.set('AUTH_CFG', 'AUTHORIZATION_HEADER', header)

    method = default_input("? Authorization method (Bearer)", "Bearer")
    conf.set('AUTH_CFG', 'AUTHORIZATION_METHOD', method)

    algorithms = default_input("? Algorithms (HS256)", "HS256")
    conf.set('AUTH_CFG', 'ALGORITHMS', algorithms)

    key = input("? Secret key: ")
    conf.set('AUTH_CFG', 'SECRET_KEY', key)

    client = input("? Client id: ")
    conf.set('AUTH_CFG', 'CLIENT_ID', client)

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

    passwd = input("? Password: ")
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


def init():
    create_auth_cfg()
    create_database_cfg()
