# aws-stepfunctions-serverless-orchestration-demo

> Demo de orquestração serverless com AWS Step Functions, Lambda e serviços AWS.

![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Step Functions](https://img.shields.io/badge/Step_Functions-FF4F8B?style=for-the-badge&logo=amazonaws&logoColor=white)
![Lambda](https://img.shields.io/badge/Lambda-FF9900?style=for-the-badge&logo=awslambda&logoColor=white)

---

## 📌 Sobre o projeto

Demonstração prática de **orquestração serverless** utilizando AWS Step Functions para coordenar funções Lambda em um fluxo de trabalho event-driven. O projeto simula um processo de aprovação de pedidos com estados de sucesso, falha e retentativas.

Ideal para estudar **arquitetura serverless**, **orquestração de serviços** e **boas práticas de Step Functions**.

---

## 📂 Estrutura do repositório

```
aws-stepfunctions-serverless-orchestration-demo/
├── statemachine/
│   └── order-flow.asl.json          # Definição da State Machine (Amazon States Language)
├── lambdas/
│   ├── validate-order/
│   │   └── handler.py                 # Valida dados do pedido
│   ├── process-payment/
│   │   └── handler.py                 # Processa pagamento (simulação)
│   └── send-notification/
│       └── handler.py                 # Envia notificação final
├── docs/
│   └── architecture.png             # Diagrama da arquitetura
└── README.md
```

---

## 🔄 Fluxo da State Machine

```
[Inicio]
    |
    v
[ValidateOrder] --> FALHA --> [HandleError] --> [END - Falha]
    |
  SUCESSO
    |
    v
[ProcessPayment] --> ERRO --> [Retry x3] --> [HandleError]
    |
  SUCESSO
    |
    v
[SendNotification]
    |
    v
[END - Sucesso]
```

---

## 📝 Definição da State Machine (ASL)

```json
{
  "Comment": "Fluxo de aprovação de pedido serverless",
  "StartAt": "ValidateOrder",
  "States": {
    "ValidateOrder": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:REGION:ACCOUNT:function:validate-order",
      "Next": "ProcessPayment",
      "Catch": [{
        "ErrorEquals": ["States.ALL"],
        "Next": "HandleError"
      }]
    },
    "ProcessPayment": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:REGION:ACCOUNT:function:process-payment",
      "Retry": [{
        "ErrorEquals": ["States.TaskFailed"],
        "IntervalSeconds": 2,
        "MaxAttempts": 3
      }],
      "Next": "SendNotification"
    },
    "SendNotification": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:REGION:ACCOUNT:function:send-notification",
      "End": true
    },
    "HandleError": {
      "Type": "Fail",
      "Error": "OrderFailed",
      "Cause": "Erro no processamento do pedido"
    }
  }
}
```

---

## 🚀 Como executar

1. **Deploy das funções Lambda** via AWS Console ou CLI
2. **Criar a State Machine** no AWS Step Functions colando o JSON acima
3. **Substituir** `REGION` e `ACCOUNT` pelos seus valores
4. **Iniciar execução** com o payload de teste:

```json
{
  "orderId": "ORD-001",
  "customer": "Luciano",
  "amount": 150.00,
  "items": ["produto-a", "produto-b"]
}
```

---

## 📚 O que aprendi com esse projeto

- Modelagem de fluxos com Amazon States Language (ASL)
- Tratamento de erros com `Catch` e `Retry` em Step Functions
- Arquitetura event-driven e orquestração vs. coreografia
- Integração entre Step Functions e funções Lambda
- Boas práticas de serverless na AWS

---

## 👤 Autor

**Luciano Henrique Morais Girão**  
[LinkedIn](https://www.linkedin.com/in/lucianogirao) • [GitHub](https://github.com/lucianowtp1-stack)
