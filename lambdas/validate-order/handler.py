"""
validate-order/handler.py
Função Lambda - Valida os dados de entrada de um pedido
Parte do fluxo: aws-stepfunctions-serverless-orchestration-demo
Autor: Luciano Girão | github.com/luciano-girao
"""

import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

REQUIRED_FIELDS = ["orderId", "customer", "amount", "items"]


def lambda_handler(event, context):
    """
    Valida os campos obrigatórios de um pedido.
    Input esperado: { orderId, customer, amount, items }
    """
    logger.info("ValidateOrder iniciado. Evento: %s", json.dumps(event))

    # Verifica campos obrigatórios
    missing_fields = [
        field for field in REQUIRED_FIELDS if field not in event
    ]

    if missing_fields:
        error_msg = f"Campos obrigatórios ausentes: {missing_fields}"
        logger.error(error_msg)
        raise ValueError(error_msg)

    # Valida que o valor do pedido é positivo
    if not isinstance(event["amount"], (int, float)) or event["amount"] <= 0:
        raise ValueError("O campo 'amount' deve ser um número positivo.")

    # Valida que o pedido tem ao menos 1 item
    if not isinstance(event["items"], list) or len(event["items"]) == 0:
        raise ValueError("O pedido deve conter ao menos 1 item.")

    logger.info("Pedido %s validado com sucesso.", event["orderId"])

    return {
        "status": "VALIDATED",
        "orderId": event["orderId"],
        "customer": event["customer"],
        "amount": event["amount"],
        "items": event["items"],
        "itemCount": len(event["items"])
    }
