import configparser
import os

fileDir = os.getcwd() + '\\config.ini'
global config

if not os.path.exists(fileDir):
    with open(fileDir, mode='w+') as f:
        f.write('')
print(fileDir)
config = configparser.ConfigParser()
config.read(filenames=fileDir)


def getIniValue(key: str, section: str, default):
    if config.has_option(option=key, section=section):
        return config.get(section=section, option=key)
    return default


def setIniValue(key: str, section: str, value):
    if config.has_section(section=section):
        config.set(section=section, option=key, value=value)
    else:
        config.add_section(section=section)
        config.set(section=section, option=key, value=value)
    with open(fileDir, 'w+') as file:
        config.write(file)


# 重新读取
def reloadConfig():
    config.read(filenames=fileDir)
    return config


def text_between(text: str, begin: str, end: str) -> str:
    start = text.index(begin) + len(begin)
    end = text.index(end, start)
    return text[start:end]


def writeSaleRecord(my_account, buy_account, plt, tradeId, time):
    """

    :param time:  确认报价的时间
    :param tradeId:  steam报价id
    :param plt:  平台名
    :param my_account:  自己的账号
    :param buy_account: 买家的账号
    :return:
    """
    text = f"{my_account}----{buy_account}----{plt}----{tradeId}----{time}\r\n"
    with open(os.getcwd() + '\\saleRecord.txt', 'a+') as f:
        f.write(text)
        f.flush()
