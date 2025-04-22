# MERIT: Monitoring, Evaluation, Reporting, Inspection, Testing

MERIT is a comprehensive framework for evaluating and testing AI systems, particularly those powered by Large Language Models (LLMs). It provides tools for test set generation, evaluation, and reporting to help you build more reliable and effective AI applications.

## Recent Improvements

The latest version includes several improvements to enhance robustness and usability:

- **Better Input Handling**: Automatically extracts content from Input objects
- **Improved Error Handling**: More robust error handling for embedding similarities
- **Enhanced Model Compatibility**: Support for both 'model' and 'generation_model' parameters
- **Dependency Checks**: Graceful fallbacks when optional dependencies are not available
- **Comprehensive Documentation**: Clear examples showing how to handle different input types
- **Type Checking and Validation**: Robust type checking for API parameters
- **Improved Test Set Loading**: Better error handling and validation for test sets
- **Progress Reporting**: Visual feedback for long-running operations
- **Utility Functions**: Common operations extracted into reusable utility functions

## Overview

Modern AI systems, especially those built with LLMs, require robust evaluation and testing frameworks to ensure they meet quality standards and perform as expected. MERIT addresses this need with a modular, extensible architecture that supports:

- **Test Set Generation**: Create diverse, representative test sets from your knowledge base
- **Evaluation**: Assess system performance using a variety of metrics
- **Reporting**: Generate detailed reports with visualizations
- **API Integration**: Connect with popular LLM providers

## Core Features

### Test Set Generation

MERIT provides powerful tools for generating test sets from your knowledge base:

- **Example-guided generation**: Create test inputs that match the style and patterns of your examples
- **Document-based generation**: Generate test inputs based on document content
- **Reference answer generation**: Automatically create reference answers for evaluation
- **Distribution strategies**: Control how test inputs are distributed across your knowledge base

```python
from merit.knowledge import KnowledgeBase
from merit.testset_generation import TestSetGenerator
from merit.api.gemini_client import GeminiClient
from merit.core.utils import extract_content

# Initialize client and knowledge base
client = GeminiClient(api_key="your-api-key")

kb = KnowledgeBase(data=your_documents, client=client)

# Create test set generator
generator = TestSetGenerator(knowledge_base=kb)

# Generate test set
test_set = generator.generate(
    num_items=50,
    distribution_strategy="representative"  
)

test_set.save("test_set.json")

from merit.core.models import TestSet
loaded_test_set = TestSet.load("test_set.json")
```

### Evaluation

MERIT includes a comprehensive evaluation system with metrics for assessing different aspects of your AI system:

- **RAG-specific metrics**: Correctness, Faithfulness, Relevance, Context Precision, Context Recall
- **General quality metrics**: Coherence, Fluency
- **Customizable evaluation**: Add your own metrics or use the built-in ones

```python
from merit.evaluation.evaluators import RAGEvaluator, evaluate_rag
from merit.metrics.rag import CorrectnessMetric, FaithfulnessMetric, RelevanceMetric
from merit.core.models import Input, Response

# Initialize metrics
metrics = [
    CorrectnessMetric(llm_client=client),
    FaithfulnessMetric(llm_client=client),
    RelevanceMetric(llm_client=client)
]

def my_rag_system(query):
    # Handle both string queries and Input objects
    if hasattr(query, 'content'):
        query_text = query.content
    else:
        query_text = str(query)
        
    # Search knowledge base (now handles Input objects automatically)
    search_results = kb.search(query, k=3)
    
    # Process results and generate response
    # ...
    
    # Return response (can be string, Response object, or tuple with context)
    return Response(content="This is a response to: " + query_text)

# Method 1: Using the RAGEvaluator class
evaluator = RAGEvaluator(
    test_set=test_set,
    metrics=metrics,
    knowledge_base=kb,
    llm_client=client
)
report1 = evaluator.evaluate(my_rag_system)

# Method 2: Using the evaluate_rag function (with improved documentation)
report2 = evaluate_rag(
    answer_fn=my_rag_system,
    testset=test_set,
    knowledge_base=kb,
    llm_client=client,
    metrics=metrics
)

# Save report with HTML visualization
report1.save("evaluation_report.json", generate_html=True)
```

### API Integration

MERIT provides a flexible API client system that supports various LLM providers:

- **OpenAI client**: Connect to OpenAI's API for text generation and embeddings
- **Generic client**: Extend to support other providers
- **Adaptive throttling**: Automatically adjust request rates to avoid rate limits
- **Retry mechanism**: Handle transient errors gracefully

```python
from merit.api.gemini_client import GeminiClient

# Initialize client (supports both 'model' and 'generation_model' parameters)
client = GeminiClient(
    api_key="your-api-key",
    model="gemini-1.5-pro",  # You can use 'model' instead of 'generation_model'
    embedding_model="embedding-001"
)

# Generate text with type checking and validation
response = client.generate_text(
    prompt="What is MERIT?",
    temperature=0.7,  # Will be validated to be between 0.0 and 1.0
    max_tokens=500
)

# Get embeddings (handles both string and Input objects)
from merit.core.utils import extract_content
from merit.core.models import Input

# Works with strings
embeddings1 = client.get_embeddings(["MERIT is a framework for evaluating AI systems"])

# Works with Input objects
input_obj = Input(content="MERIT is a framework for evaluating AI systems")
embeddings2 = client.get_embeddings([input_obj])
```

## Installation

Install MERIT using pip:

```bash
pip install merit-ai
```

For development:

```bash
# Install with development dependencies
pip install merit-ai[dev]
```

## Roadmap

MERIT is under active development with the following roadmap:

### Current Release (0.1.3)
- Test set generation
- Evaluation framework with RAG metrics
- API client system
- HTML report generation
- **Monitoring system**: Real-time monitoring of AI system performance

### Upcoming Features
- **Advanced metrics**: Additional metrics for specialized evaluation scenarios
- **UI components**: Interactive dashboards for monitoring and evaluation
- **Integration with popular frameworks**: Direct integration with LangChain, LlamaIndex, etc.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
