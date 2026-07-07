# =============================================================
# Lambda: validate-order
# Description: Valida pedido recebido no fluxo Step Functions
# Author: Luciano Girao
# Date: 2025
# =============================================================

import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

REQUIRED_FIELDS = ["order_id", "customer_id", "items", "total"]


def lambda_handler(event, context):
    logger.info("Validando pedido: %s", json.dumps(event))

    # Verifica campos obrigatorios
    missing = [f for f in REQUIRED_FIELDS if f not in event]
    if missing:
        logger.error("Campos ausentes: %s", missing)
        raise ValueError(f"Pedido invalido. Campos ausentes: {missing}")

    # Valida total positivo
    if event["total"] <= 0:
        raise ValueError("Total do pedido deve ser maior que zero.")

    # Valida lista de itens nao vazia
    if not event["items"]:
        raise ValueError("Pedido deve conter pelo menos um item.")

    logger.info("Pedido %s validado com sucesso.", event["order_id"])

    return {
        "statusCode": 200,
        "order_id": event["order_id"],
        "customer_id": event["customer_id"],
        "items": event["items"],
        "total": event["total"],
        "status": "VALIDATED"
    }
