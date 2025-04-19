# thsdata

# Installation

```bash
pip install --upgrade thsdata
```

# Usage

```python
from thsdata import Quote, FuquanNo, KlineDay
import datetime


def main():
    # 初始化
    quote = Quote()

    try:
        # quote.connect()
        # print(quote.about())
        start_date = datetime.datetime(2024, 1, 1)
        end_date = datetime.datetime(2025, 2, 28)
        data = quote.security_bars("USHA600519", start_date, end_date, FuquanNo, KlineDay)
        print(data)

    except Exception as e:
        print("An error occurred:", e)

    finally:
        # 断开连接
        quote.disconnect()
        print("Disconnected from the server.")


if __name__ == "__main__":
    main()

```

result:

```
2025/03/04 18:16:56 hello thsdk!
          time    close   volume    turnover     open     high      low
0   2024-01-02  1685.01  3215644  5440082500  1715.00  1718.19  1678.10
1   2024-01-03  1694.00  2022929  3411400700  1681.11  1695.22  1676.33
2   2024-01-04  1669.00  2155107  3603970100  1693.00  1693.00  1662.93
3   2024-01-05  1663.36  2024286  3373155600  1661.33  1678.66  1652.11
4   2024-01-08  1643.99  2558620  4211918600  1661.00  1662.00  1640.01
..         ...      ...      ...         ...      ...      ...      ...
273 2025-02-24  1479.07  3474373  5157907300  1488.00  1499.52  1474.00
274 2025-02-25  1454.00  2838743  4142814500  1470.01  1473.39  1452.00
275 2025-02-26  1460.01  2636609  3835949000  1455.45  1464.96  1445.00
276 2025-02-27  1485.56  4976217  7368002400  1460.02  1489.90  1454.00
277 2025-02-28  1500.79  5612895  8475738200  1485.50  1528.38  1482.00

[278 rows x 7 columns]
Disconnected from the server.
```
