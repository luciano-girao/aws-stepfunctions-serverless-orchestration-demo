# =============================================================
# Lambda: send-notification
# Description: Envia notificacao SNS apos conclusao do pedido
# Author: Luciano Girao
# Date: 2025
# =============================================================

import json
import logging
import os
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

SNS_TOPIC_ARN = os.environ.get("SNS_TOPIC_ARN", "")


def lambda_handler(event, context):
    logger.info("Enviando notificacao: %s", json.dumps(event))

    order_id = event.get("order_id")
    payment_status = event.get("payment_status", "UNKNOWN")
    transaction_id = event.get("transaction_id", "N/A")
    total = event.get("total", 0)

    message = (
        f"Pedido {order_id} processado com sucesso!\n"
        f"Status do pagamento: {payment_status}\n"
        f"Transacao: {transaction_id}\n"
        f"Total: R$ {total:.2f}"
    )

    subject = f"Confirmacao de Pedido #{order_id}"

    if SNS_TOPIC_ARN:
        sns = boto3.client("sns")
        response = sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=message,
            Subject=subject
        )
        logger.info("Notificacao enviada. MessageId: %s", response["MessageId"])
    else:
        logger.warning("SNS_TOPIC_ARN nao configurado. Notificacao simulada.")
        logger.info("Mensagem: %s", message)

    return {
        "statusCode": 200,
        "order_id": order_id,
        "notification_sent": bool(SNS_TOPIC_ARN),
        "status": "COMPLETED"
    }
