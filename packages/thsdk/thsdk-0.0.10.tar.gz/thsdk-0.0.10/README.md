# thsdk

# Installation

```bash
pip install --upgrade thsdk
```

# Usage

```python
from thsdk import THS, Adjust, Interval


def main():
    # 初始化
    ths = THS()
    # ths.about()

    try:
        # 连接到行情服务器
        login_reply = ths.connect()
        if login_reply.err_code != 0:
            print(f"登录错误:{login_reply.err_code}, 信息:{login_reply.err_message}")
            return
        else:
            print("Connected to the server.")

        # 查询历史所有日k数据
        # results = ths.download("USHA600519")
        # 查询历史100条日k数据
        # results = ths.download("USHA600519", count=100)
        # 查询历史20240101 - 202050101 日k数据
        results = ths.download("USHA600519", start=20240101, end=20250101)
        # 查询历史100条日k数据 前复权
        # results = ths.download("USHA600519", count=100, adjust=Adjust.FORWARD)
        # 查询历史100跳1分钟k数据
        # results = ths.download("USHA600519", count=100, interval=Interval.MIN_1)

        print(results)

        print("查询成功 数量:", len(results))

    except Exception as e:
        print("An error occurred:", e)

    finally:
        # 断开连接
        ths.disconnect()
        print("Disconnected from the server.")
        # print(ths.about())
        ths.about()


if __name__ == "__main__":
    main()

```

## Result:

```
Connected to the server.
         time    close   volume    turnover     open     high      low
0   2024-01-02  1685.01  3215644  5440082500  1715.00  1718.19  1678.10
1   2024-01-03  1694.00  2022929  3411400700  1681.11  1695.22  1676.33
2   2024-01-04  1669.00  2155107  3603970100  1693.00  1693.00  1662.93
3   2024-01-05  1663.36  2024286  3373155600  1661.33  1678.66  1652.11
4   2024-01-08  1643.99  2558620  4211918600  1661.00  1662.00  1640.01
..         ...      ...      ...         ...      ...      ...      ...
237 2024-12-25  1530.00  1712339  2621061900  1538.80  1538.80  1526.10
238 2024-12-26  1527.79  1828651  2798840000  1534.00  1538.78  1523.00
239 2024-12-27  1528.97  2075932  3170191400  1528.90  1536.00  1519.50
240 2024-12-30  1525.00  2512982  3849542600  1533.97  1543.96  1525.00
241 2024-12-31  1524.00  3935445  6033540400  1525.40  1545.00  1522.01

[242 rows x 7 columns]
查询成功 数量: 242
Disconnected from the server.
```

```python
from thsdk import THS, Adjust, Interval
import pandas as pd


def main():
    # 初始化
    ths = THS()
    # ths.about()

    try:
        # 连接到行情服务器
        login_reply = ths.connect()
        if login_reply.err_code != 0:
            print(f"登录错误:{login_reply.err_code}, 信息:{login_reply.err_message}")
            return
        else:
            print("Connected to the server.")

        # 获取历史日级别数据
        reply = ths.security_bars("USHA600519", 20240101, 20250420, Adjust.NONE, Interval.DAY)

        if reply.err_code != 0:
            print(f"查询错误:{reply.err_code}, 信息:{reply.err_message}")
            return

        resp = reply.resp
        df = pd.DataFrame(resp.data)
        print(df)

        print("查询成功 数量:", len(resp.data))

    except Exception as e:
        print("An error occurred:", e)

    finally:
        # 断开连接
        ths.disconnect()
        print("Disconnected from the server.")
        # print(ths.about())
        ths.about()


if __name__ == "__main__":
    main()

```

## Result:

```
Connected to the server.
          time    close   volume    turnover     open     high      low
0   2024-01-02  1685.01  3215644  5440082500  1715.00  1718.19  1678.10
1   2024-01-03  1694.00  2022929  3411400700  1681.11  1695.22  1676.33
2   2024-01-04  1669.00  2155107  3603970100  1693.00  1693.00  1662.93
3   2024-01-05  1663.36  2024286  3373155600  1661.33  1678.66  1652.11
4   2024-01-08  1643.99  2558620  4211918600  1661.00  1662.00  1640.01
..         ...      ...      ...         ...      ...      ...      ...
307 2025-04-14  1551.99  2171144  3379425600  1560.97  1566.00  1551.53
308 2025-04-15  1558.00  2148928  3339942700  1552.00  1565.00  1545.00
309 2025-04-16  1559.17  3115605  4834880600  1552.00  1576.00  1537.00
310 2025-04-17  1570.00  2384605  3733925000  1554.00  1576.50  1549.99
311 2025-04-18  1565.94  2029848  3179974300  1566.00  1575.00  1556.00

[312 rows x 7 columns]
查询成功 数量: 312
Disconnected from the server.
```

```python
from thsdk import BkTHS
import pandas as pd


def main():
    # 初始化
    ths = BkTHS()
    # ths.about()

    try:
        # 连接到行情服务器
        login_reply = ths.connect()
        if login_reply.err_code != 0:
            print(f"登录错误:{login_reply.err_code}, 信息:{login_reply.err_message}")
            return
        else:
            print("Connected to the server.")

        # 获取历史日级别数据
        reply = ths.get_block_data(0xCE5F)
        if reply.err_code != 0:
            print(f"查询错误:{reply.err_code}, 信息:{reply.err_message}")
            return

        resp = reply.resp
        df = pd.DataFrame(resp.data)
        print(df)

        print("查询成功 数量:", len(resp.data))

    except Exception as e:
        print("An error occurred:", e)

    finally:
        # 断开连接
        ths.disconnect()
        print("Disconnected from the server.")
        # print(ths.about())
        ths.about()


if __name__ == "__main__":
    main()

```

## result:

```
Connected to the server.
          code   name
0   URFI881165     综合
1   URFI881171  自动化设备
2   URFI881118   专用设备
3   URFI881141     中药
4   URFI881157     证券
..         ...    ...
85  URFI881138   包装印刷
86  URFI881121    半导体
87  URFI881131   白色家电
88  URFI881273     白酒
89  URFI881271   IT服务

[90 rows x 2 columns]
查询成功 数量: 90
Disconnected from the server.
```