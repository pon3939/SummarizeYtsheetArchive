# -*- coding: utf-8 -*-

from datetime import datetime

from aws_lambda_powertools.utilities.typing import LambdaContext
from myLibrary import commonFunction
from myLibrary.constant import tableName
from mypy_boto3_dynamodb.client import DynamoDBClient
from mypy_boto3_dynamodb.type_defs import (
    BatchWriteItemOutputTypeDef,
    WriteRequestTypeDef,
)

"""
level_capsに登録
"""


def lambda_handler(event: dict, context: LambdaContext):
    """

    メイン処理

    Args:
        event dict: イベント
        context awslambdaric.lambda_context.LambdaContext: コンテキスト
    """

    seasonId: int = int(event["SeasonId"])
    levelCaps: list[dict[str, str]] = event["LevelCaps"]

    insertLevelCaps(levelCaps, seasonId)


def insertLevelCaps(
    levelCaps: "list[dict[str, str]]",
    seasonId: int,
):
    """レベルキャップを挿入する

    Args:
        levelCaps: list[dict[str, str]]: レベルキャップ
        seasonId: int: シーズンID
    """

    dynamoDb: DynamoDBClient = commonFunction.InitDb()

    requestItems: list[WriteRequestTypeDef] = []
    for levelCap in levelCaps:
        # JSTをGMTに変換
        startDatetimeInJst: datetime = datetime.strptime(
            f'{levelCap["startDatetime"]}+09:00', r"%Y/%m/%d%z"
        )

        requestItem: WriteRequestTypeDef = {}
        requestItem["PutRequest"] = {"Item": {}}
        item: dict = {
            "season_id": seasonId,
            "start_datetime"
            "": commonFunction.DateTimeToStrForDynamoDB(startDatetimeInJst),
            "max_exp": levelCap["maxExp"],
            "minimum_Exp": levelCap["minimumExp"],
        }
        requestItem["PutRequest"]["Item"] = (
            commonFunction.ConvertJsonToDynamoDB(item)
        )
        requestItems.append(requestItem)

    response: BatchWriteItemOutputTypeDef = dynamoDb.batch_write_item(
        RequestItems={tableName.LEVEL_CAPS: requestItems}
    )

    while response["UnprocessedItems"] != {}:
        response = dynamoDb.batch_write_item(
            RequestItems=response["UnprocessedItems"]
        )
