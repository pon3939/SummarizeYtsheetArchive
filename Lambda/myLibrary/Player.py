from dataclasses import dataclass, field
from datetime import datetime

from myLibrary.PlayerCharacter import PlayerCharacter
from pytz import timezone

# -*- coding: utf-8 -*-


"""
PL
"""


@dataclass
class Player:
    """
    PL
    """

    Name: str
    UpdateTime: str
    MaxExp: int
    MinimumExp: int

    # DBから取得したJSON
    CharacterJsons: list[dict]

    Characters: list[PlayerCharacter] = field(default_factory=list)

    def __post_init__(self) -> None:
        """
        コンストラクタの後の処理
        """
        if len(self.CharacterJsons) == 0:
            # JSONからデコードされた場合など
            return

        # 更新日時をスプレッドシートが理解できる形式に変換
        utc: datetime = datetime.fromisoformat(self.UpdateTime)
        jst: datetime = utc.astimezone(timezone("Asia/Tokyo"))
        self.UpdateTime = jst.strftime("%Y/%m/%d %H:%M:%S")

        self.Characters = list(
            map(
                lambda x: PlayerCharacter(
                    Json=x,
                    PlayerName=self.Name,
                    MaxExp=self.MaxExp,
                    MinimumExp=self.MinimumExp,
                ),
                self.CharacterJsons,
            )
        )

        # 不要なので削除
        self.MaxExp = 0
        self.MinimumExp = 0
        self.CharacterJsons = []
