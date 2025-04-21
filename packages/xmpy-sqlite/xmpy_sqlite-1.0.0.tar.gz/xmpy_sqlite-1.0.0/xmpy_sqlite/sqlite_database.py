from datetime import datetime
from typing import List

from peewee import (
    AutoField,
    CharField,
    DateTimeField,
    FloatField, IntegerField,
    Model,
    SqliteDatabase as PeeweeSqliteDatabase,
    ModelSelect,
    ModelDelete,
    chunked,
    fn
)

from xmpy.包_交易核心.模块_常数 import 类_交易所,类_周期
from xmpy.包_交易核心.模块_对象 import 类_K线数据,类_行情数据
from xmpy.包_交易核心.模块_工具 import 获取文件路径
from xmpy.包_交易核心.模块_基础数据库 import (
    类_基础数据库,
    类_K线概览,
    数据库时区,
    类_Tick概览,
    转换时区
)

path: str = str(获取文件路径("database.db"))
db: PeeweeSqliteDatabase = PeeweeSqliteDatabase(path)


class DbBarData(Model):
    """K线数据表映射对象"""

    id: AutoField = AutoField()

    symbol: str = CharField()
    exchange: str = CharField()
    datetime: datetime = DateTimeField()
    interval: str = CharField()

    volume: float = FloatField()
    turnover: float = FloatField()
    open_interest: float = FloatField()
    open_price: float = FloatField()
    high_price: float = FloatField()
    low_price: float = FloatField()
    close_price: float = FloatField()

    class Meta:
        database: PeeweeSqliteDatabase = db
        indexes: tuple = ((("symbol", "exchange", "interval", "datetime"), True),)


class DbTickData(Model):
    """TICK数据表映射对象"""

    id: AutoField = AutoField()

    symbol: str = CharField()
    exchange: str = CharField()
    datetime: datetime = DateTimeField()

    name: str = CharField()
    volume: float = FloatField()
    turnover: float = FloatField()
    open_interest: float = FloatField()
    last_price: float = FloatField()
    last_volume: float = FloatField()
    limit_up: float = FloatField()
    limit_down: float = FloatField()

    open_price: float = FloatField()
    high_price: float = FloatField()
    low_price: float = FloatField()
    pre_close: float = FloatField()

    bid_price_1: float = FloatField()
    bid_price_2: float = FloatField(null=True)
    bid_price_3: float = FloatField(null=True)
    bid_price_4: float = FloatField(null=True)
    bid_price_5: float = FloatField(null=True)

    ask_price_1: float = FloatField()
    ask_price_2: float = FloatField(null=True)
    ask_price_3: float = FloatField(null=True)
    ask_price_4: float = FloatField(null=True)
    ask_price_5: float = FloatField(null=True)

    bid_volume_1: float = FloatField()
    bid_volume_2: float = FloatField(null=True)
    bid_volume_3: float = FloatField(null=True)
    bid_volume_4: float = FloatField(null=True)
    bid_volume_5: float = FloatField(null=True)

    ask_volume_1: float = FloatField()
    ask_volume_2: float = FloatField(null=True)
    ask_volume_3: float = FloatField(null=True)
    ask_volume_4: float = FloatField(null=True)
    ask_volume_5: float = FloatField(null=True)

    localtime: datetime = DateTimeField(null=True)

    class Meta:
        database: PeeweeSqliteDatabase = db
        indexes: tuple = ((("symbol", "exchange", "datetime"), True),)


class DbBarOverview(Model):
    """K线汇总数据表映射对象"""

    id: AutoField = AutoField()

    symbol: str = CharField()
    exchange: str = CharField()
    interval: str = CharField()
    count: int = IntegerField()
    start: datetime = DateTimeField()
    end: datetime = DateTimeField()

    class Meta:
        database: PeeweeSqliteDatabase = db
        indexes: tuple = ((("symbol", "exchange", "interval"), True),)


class DbTickOverview(Model):
    """Tick汇总数据表映射对象"""

    id: AutoField = AutoField()

    symbol: str = CharField()
    exchange: str = CharField()
    count: int = IntegerField()
    start: datetime = DateTimeField()
    end: datetime = DateTimeField()

    class Meta:
        database: PeeweeSqliteDatabase = db
        indexes: tuple = ((("symbol", "exchange"), True),)


class SqliteDatabase(类_基础数据库):
    """SQLite数据库接口"""

    def __init__(self) -> None:
        """"""
        self.db: PeeweeSqliteDatabase = db
        self.db.connect()
        self.db.create_tables([DbBarData, DbTickData, DbBarOverview, DbTickOverview])

    def 保存K线数据(self, bars: List[类_K线数据], stream: bool = False) -> bool:
        """保存K线数据"""
        # 读取主键参数
        bar: 类_K线数据 = bars[0]
        symbol: str = bar.symbol
        exchange: 类_交易所 = bar.exchange
        interval: 类_周期 = bar.interval

        # 将BarData数据转换为字典，并调整时区
        data: list = []

        for bar in bars:
            bar.datetime = 转换时区(bar.datetime)

            d: dict = bar.__dict__
            d["exchange"] = d["exchange"].value
            d["interval"] = d["interval"].value
            d.pop("gateway_name")
            d.pop("vt_symbol")
            data.append(d)

        # 使用upsert操作将数据更新到数据库中
        with self.db.atomic():
            for c in chunked(data, 50):
                DbBarData.insert_many(c).on_conflict_replace().execute()

        # 更新K线汇总数据
        overview: DbBarOverview = DbBarOverview.get_or_none(
            DbBarOverview.symbol == symbol,
            DbBarOverview.exchange == exchange.value,
            DbBarOverview.interval == interval.value,
        )

        if not overview:
            overview = DbBarOverview()
            overview.symbol = symbol
            overview.exchange = exchange.value
            overview.interval = interval.value
            overview.start = bars[0].datetime
            overview.end = bars[-1].datetime
            overview.count = len(bars)
        elif stream:
            overview.end = bars[-1].datetime
            overview.count += len(bars)
        else:
            overview.start = min(bars[0].datetime, overview.start)
            overview.end = max(bars[-1].datetime, overview.end)

            s: ModelSelect = DbBarData.select().where(
                (DbBarData.symbol == symbol)
                & (DbBarData.exchange == exchange.value)
                & (DbBarData.interval == interval.value)
            )
            overview.count = s.count()

        overview.save()

        return True

    def 保存Tick数据(self, ticks: List[类_行情数据], stream: bool = False) -> bool:
        """保存TICK数据"""
        # 读取主键参数
        tick: 类_行情数据 = ticks[0]
        symbol: str = tick.symbol
        exchange: 类_交易所 = tick.exchange

        # 将TickData数据转换为字典，并调整时区
        data: list = []

        for tick in ticks:
            tick.datetime = 转换时区(tick.datetime)

            d: dict = tick.__dict__
            d["exchange"] = d["exchange"].value
            d.pop("gateway_name")
            d.pop("vt_symbol")
            data.append(d)

        # 使用upsert操作将数据更新到数据库中
        with self.db.atomic():
            for c in chunked(data, 10):
                DbTickData.insert_many(c).on_conflict_replace().execute()

        # 更新Tick汇总数据
        overview: DbTickOverview = DbTickOverview.get_or_none(
            DbTickOverview.symbol == symbol,
            DbTickOverview.exchange == exchange.value,
        )

        if not overview:
            overview: DbTickOverview = DbTickOverview()
            overview.symbol = symbol
            overview.exchange = exchange.value
            overview.start = ticks[0].datetime
            overview.end = ticks[-1].datetime
            overview.count = len(ticks)
        elif stream:
            overview.end = ticks[-1].datetime
            overview.count += len(ticks)
        else:
            overview.start = min(ticks[0].datetime, overview.start)
            overview.end = max(ticks[-1].datetime, overview.end)

            s: ModelSelect = DbTickData.select().where(
                (DbTickData.symbol == symbol)
                & (DbTickData.exchange == exchange.value)
            )
            overview.count = s.count()

        overview.save()

        return True

    def 加载K线数据(
        self,
        symbol: str,
        exchange: 类_交易所,
        interval: 类_周期,
        start: datetime,
        end: datetime
    ) -> List[类_K线数据]:
        """读取K线数据"""
        s: ModelSelect = (
            DbBarData.select().where(
                (DbBarData.symbol == symbol)
                & (DbBarData.exchange == exchange.value)
                & (DbBarData.interval == interval.value)
                & (DbBarData.datetime >= start)
                & (DbBarData.datetime <= end)
            ).order_by(DbBarData.datetime)
        )

        bars: List[类_K线数据] = []
        for db_bar in s:
            bar: 类_K线数据 = 类_K线数据(
                symbol=db_bar.symbol,
                exchange=类_交易所(db_bar.exchange),
                datetime=datetime.fromtimestamp(db_bar.datetime.timestamp(), 数据库时区),
                interval=类_周期(db_bar.interval),
                volume=db_bar.volume,
                turnover=db_bar.turnover,
                open_interest=db_bar.open_interest,
                open_price=db_bar.open_price,
                high_price=db_bar.high_price,
                low_price=db_bar.low_price,
                close_price=db_bar.close_price,
                gateway_name="DB"
            )
            bars.append(bar)

        return bars

    def 加载Tick数据(
        self,
        symbol: str,
        exchange: 类_交易所,
        start: datetime,
        end: datetime
    ) -> List[类_行情数据]:
        """读取TICK数据"""
        s: ModelSelect = (
            DbTickData.select().where(
                (DbTickData.symbol == symbol)
                & (DbTickData.exchange == exchange.value)
                & (DbTickData.datetime >= start)
                & (DbTickData.datetime <= end)
            ).order_by(DbTickData.datetime)
        )

        ticks: List[类_行情数据] = []
        for db_tick in s:
            tick: 类_行情数据 = 类_行情数据(
                symbol=db_tick.symbol,
                exchange=类_交易所(db_tick.exchange),
                datetime=datetime.fromtimestamp(db_tick.datetime.timestamp(), 数据库时区),
                name=db_tick.name,
                volume=db_tick.volume,
                turnover=db_tick.turnover,
                open_interest=db_tick.open_interest,
                last_price=db_tick.last_price,
                last_volume=db_tick.last_volume,
                limit_up=db_tick.limit_up,
                limit_down=db_tick.limit_down,
                open_price=db_tick.open_price,
                high_price=db_tick.high_price,
                low_price=db_tick.low_price,
                pre_close=db_tick.pre_close,
                bid_price_1=db_tick.bid_price_1,
                bid_price_2=db_tick.bid_price_2,
                bid_price_3=db_tick.bid_price_3,
                bid_price_4=db_tick.bid_price_4,
                bid_price_5=db_tick.bid_price_5,
                ask_price_1=db_tick.ask_price_1,
                ask_price_2=db_tick.ask_price_2,
                ask_price_3=db_tick.ask_price_3,
                ask_price_4=db_tick.ask_price_4,
                ask_price_5=db_tick.ask_price_5,
                bid_volume_1=db_tick.bid_volume_1,
                bid_volume_2=db_tick.bid_volume_2,
                bid_volume_3=db_tick.bid_volume_3,
                bid_volume_4=db_tick.bid_volume_4,
                bid_volume_5=db_tick.bid_volume_5,
                ask_volume_1=db_tick.ask_volume_1,
                ask_volume_2=db_tick.ask_volume_2,
                ask_volume_3=db_tick.ask_volume_3,
                ask_volume_4=db_tick.ask_volume_4,
                ask_volume_5=db_tick.ask_volume_5,
                localtime=db_tick.localtime,
                gateway_name="DB"
            )
            ticks.append(tick)

        return ticks

    def 删除K线数据(
        self,
        symbol: str,
        exchange: 类_交易所,
        interval: 类_周期
    ) -> int:
        """删除K线数据"""
        d: ModelDelete = DbBarData.delete().where(
            (DbBarData.symbol == symbol)
            & (DbBarData.exchange == exchange.value)
            & (DbBarData.interval == interval.value)
        )
        count: int = d.execute()

        # 删除K线汇总数据
        d2: ModelDelete = DbBarOverview.delete().where(
            (DbBarOverview.symbol == symbol)
            & (DbBarOverview.exchange == exchange.value)
            & (DbBarOverview.interval == interval.value)
        )
        d2.execute()

        return count

    def 删除Tick数据(
        self,
        symbol: str,
        exchange: 类_交易所
    ) -> int:
        """删除TICK数据"""
        d: ModelDelete = DbTickData.delete().where(
            (DbTickData.symbol == symbol)
            & (DbTickData.exchange == exchange.value)
        )
        count: int = d.execute()

        # 删除Tick汇总数据
        d2: ModelDelete = DbTickOverview.delete().where(
            (DbTickOverview.symbol == symbol)
            & (DbTickOverview.exchange == exchange.value)
        )
        d2.execute()

        return count

    def 获取K线概览(self) -> List[类_K线概览]:
        """查询数据库中的K线汇总信息"""
        # 如果已有K线，但缺失汇总信息，则执行初始化
        data_count: int = DbBarData.select().count()
        overview_count: int = DbBarOverview.select().count()
        if data_count and not overview_count:
            self.init_bar_overview()

        s: ModelSelect = DbBarOverview.select()
        overviews: List[类_K线概览] = []
        for overview in s:
            overview.exchange = 类_交易所(overview.exchange)
            overview.interval = 类_周期(overview.interval)
            overviews.append(overview)
        return overviews

    def 获取Tick概览(self) -> List[类_Tick概览]:
        """查询数据库中的Tick汇总信息"""
        s: ModelSelect = DbTickOverview.select()
        overviews: list = []
        for overview in s:
            overview.exchange = 类_交易所(overview.exchange)
            overviews.append(overview)
        return overviews

    def init_bar_overview(self) -> None:
        """初始化数据库中的K线汇总信息"""
        s: ModelSelect = (
            DbBarData.select(
                DbBarData.symbol,
                DbBarData.exchange,
                DbBarData.interval,
                fn.COUNT(DbBarData.id).alias("count")
            ).group_by(
                DbBarData.symbol,
                DbBarData.exchange,
                DbBarData.interval
            )
        )

        for data in s:
            overview: DbBarOverview = DbBarOverview()
            overview.symbol = data.symbol
            overview.exchange = data.exchange
            overview.interval = data.interval
            overview.count = data.count

            start_bar: DbBarData = (
                DbBarData.select()
                .where(
                    (DbBarData.symbol == data.symbol)
                    & (DbBarData.exchange == data.exchange)
                    & (DbBarData.interval == data.interval)
                )
                .order_by(DbBarData.datetime.asc())
                .first()
            )
            overview.start = start_bar.datetime

            end_bar: DbBarData = (
                DbBarData.select()
                .where(
                    (DbBarData.symbol == data.symbol)
                    & (DbBarData.exchange == data.exchange)
                    & (DbBarData.interval == data.interval)
                )
                .order_by(DbBarData.datetime.desc())
                .first()
            )
            overview.end = end_bar.datetime

            overview.save()
