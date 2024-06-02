import requests

def get_balance(address):
    """
    获取指定Tron地址的TRX和USDT余额。

    参数:
        address (str): Tron地址。

    返回:
        tuple: TRX余额和USDT余额。
    """
    url = f"https://apilist.tronscanapi.com/api/accountv2?address={address}"

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"获取地址 {address} 的余额失败。错误: {e}")
        return None, None

    data = response.json()
    trx_balance = None
    usdt_balance = None

    for token in data.get("withPriceTokens", []):
        if token.get("tokenAbbr") == "trx":
            trx_balance = token.get("amount")
        elif token.get("tokenAbbr") == "USDT":
            usdt_balance = int(token.get("balance")) / 10**6  # 使用"balance"字段并转换为实际数量

    print(f"地址 {address} 的TRX余额 - {trx_balance}，USDT余额 - {usdt_balance}")
    return trx_balance, usdt_balance


def write_to_file(address, usdt_balance):
    """
    如果USDT余额大于1，将地址和余额写入文件中。

    参数:
        address (str): Tron地址。
        usdt_balance (float): USDT余额。
    """
    if usdt_balance is not None and usdt_balance > 1:
        try:
            with open("有金额.txt", "a") as balance_file:
                balance_file.write(f"地址: {address}, USDT余额: {usdt_balance}\n")
                print(f"已将数据写入文件：地址 - {address}，USDT余额 - {usdt_balance}")
        except IOError as e:
            print(f"写入文件失败: {e}")


def main():
    addresses_file = "1.txt"
    try:
        with open(addresses_file, "r") as f:
            addresses = f.read().splitlines()
    except IOError as e:
        print(f"从文件读取地址失败: {e}")
        return

    for address in addresses:
        trx_balance, usdt_balance = get_balance(address)
        if trx_balance is not None and usdt_balance is not None:
            write_to_file(address, usdt_balance)


if __name__ == "__main__":
    main()
