# =============================================================
# Lambda: process-payment
# Description: Processa pagamento de pedido validado
# Author: Luciano Girao
# Date: 2025
# =============================================================

import json
import logging
import random
import uuid

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logger.info("Processando pagamento: %s", json.dumps(event))

    order_id = event.get("order_id")
    total = event.get("total")

    if not order_id or total is None:
        raise ValueError("order_id e total sao obrigatorios.")

    # Simula processamento de pagamento (mock)
    # Em producao, integraria com Stripe, PagSeguro, etc.
    success = random.random() > 0.1  # 90% de aprovacao simulada

    transaction_id = str(uuid.uuid4())

    if success:
        logger.info("Pagamento aprovado. Transacao: %s", transaction_id)
        return {
            "statusCode": 200,
            "order_id": order_id,
            "transaction_id": transaction_id,
            "total": total,
            "payment_status": "APPROVED"
        }
    else:
        logger.warning("Pagamento recusado para pedido: %s", order_id)
        raise Exception(f"Pagamento recusado para pedido {order_id}. Tente novamente.")
