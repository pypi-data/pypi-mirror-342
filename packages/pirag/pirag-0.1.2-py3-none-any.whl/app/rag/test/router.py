from argparse import Namespace
from ragas import evaluate
from ragas.metrics import (
    answer_relevancy,
    faithfulness,
    context_precision,
    context_recall,
)

def route(args: Namespace):
    
    result = evaluate(
        
    )
    print(args)
