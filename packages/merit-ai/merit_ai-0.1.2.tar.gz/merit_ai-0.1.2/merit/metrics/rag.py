"""
MERIT RAG Metrics

This module provides metrics for evaluating RAG (Retrieval-Augmented Generation) systems.
"""

from datetime import datetime
from .prompts import (
    CORRECTNESS_EVALUATION_PROMPT,
    FAITHFULNESS_EVALUATION_PROMPT,
    RELEVANCE_EVALUATION_PROMPT,
    COHERENCE_EVALUATION_PROMPT,
    FLUENCY_EVALUATION_PROMPT,
    CONTEXT_PRECISION_WITH_REFERENCE_PROMPT,
    CONTEXT_PRECISION_WITHOUT_REFERENCE_PROMPT,
    RESPONSE_RELEVANCY_EVALUATION_PROMPT,
    CONTEXT_RECALL_REFERENCE_CLAIMS_PROMPT,
    CLAIM_VERIFICATION_PROMPT
)
from .base import MetricContext, MetricCategory, register_metric
from ..core.logging import get_logger

logger = get_logger(__name__)

from .llm_measured import LLMMeasuredBaseMetric

class CorrectnessMetric(LLMMeasuredBaseMetric):
    """Metric for evaluating the correctness of an answer."""
    name = "Correctness"
    description = "Measures how accurate and correct the answer is"
    greater_is_better = True
    context = MetricContext.EVALUATION
    category = MetricCategory.QUALITY
    
    def __init__(self, llm_client=None, agent_description=None, include_raw_response=False):
        """
        Initialize the correctness metric.
        
        Args:
            llm_client: The LLM client
            agent_description: Description of the agent
            include_raw_response: Whether to include the raw LLM response in the output
        """
        self.agent_description = agent_description or "This agent is a chatbot that answers input from users."
        super().__init__(prompt=CORRECTNESS_EVALUATION_PROMPT, llm_client=llm_client, include_raw_response=include_raw_response)
    
    def _format_prompt(self, prompt, test_item, response):
        """
        Format the prompt with test item and response data.
        
        Args:
            prompt: The prompt template
            test_item: The test item
            response: The response
            
        Returns:
            str: The formatted prompt
        """
        # Get answer text
        answer_text = response.content if hasattr(response, "content") else str(response)
        
        # Try to get document content from different sources
        document_content = ""
        if hasattr(test_item, "document") and hasattr(test_item.document, "content"):
            document_content = test_item.document.content
        elif hasattr(test_item, "document_content"):
            document_content = test_item.document_content
        elif isinstance(test_item, dict) and "document_content" in test_item:
            document_content = test_item["document_content"]
        
        # Format the prompt
        try:
            return prompt.safe_format(
                document_content=document_content,
                input=test_item.input if hasattr(test_item, "input") else "",
                reference_answer=test_item.reference_answer if hasattr(test_item, "reference_answer") else "",
                model_answer=answer_text
            )
        except Exception as e:
            logger.warning(f"Error formatting correctness prompt: {e}")
            return str(prompt)
    
    
    def _get_custom_measurements(self, llm_response, test_item, response, result, llm_custom_measurements=None):
        """
        Get custom measurements based on the LLM response.
        
        Args:
            llm_response: The raw response from the LLM
            test_item: The test item
            response: The response
            result: The processed result dictionary
            llm_custom_measurements: Custom measurements provided by the LLM, if any
            
        Returns:
            dict or None: Custom measurements to add to the result
        """
        # Extract errors if present in the LLM response
        try:
            from ..core.utils import parse_json
            json_output = parse_json(llm_response, return_type="object")
            errors = json_output.get("errors", [])
            if errors:
                return {"errors": errors}
        except Exception:
            pass
        return None
    
class FaithfulnessMetric(LLMMeasuredBaseMetric):
    """
    Metric for evaluating the faithfulness of an answer to the retrieved documents.
    
    This metric measures how factually consistent a response is with the retrieved context.
    It ranges from 0 to 1, with higher scores indicating better consistency.
    
    A response is considered faithful if all its claims can be supported by the retrieved context.
    
    To calculate this:
    1. Identify all the claims in the response.
    2. Check each claim to see if it can be inferred from the retrieved context.
    3. Compute the faithfulness score using the formula: 
       Number of claims supported by the context / Total number of claims
    
    This implementation uses a two-step approach:
    1. First LLM call identifies claims in the response
    2. Separate LLM calls check each claim against the context
    """
    name = "Faithfulness"
    description = "Measures how factually consistent a response is with the retrieved context"
    greater_is_better = True
    context = MetricContext.EVALUATION
    category = MetricCategory.QUALITY
    
    def __init__(self, llm_client=None, include_raw_response=False, similarity_threshold=0.7):
        """
        Initialize the faithfulness metric.
        
        Args:
            llm_client: The LLM client
            include_raw_response: Whether to include the raw LLM response in the output
            similarity_threshold: Threshold for embedding similarity (default: 0.7)
        """
        super().__init__(prompt=FAITHFULNESS_EVALUATION_PROMPT, llm_client=llm_client, include_raw_response=include_raw_response)
        self.similarity_threshold = similarity_threshold
        self.verification_prompt = CLAIM_VERIFICATION_PROMPT
    
    def __call__(self, test_item, response, client_llm_callable=None, prompt=None):
        """
        Calculate the faithfulness metric.
        
        This overrides the base __call__ method to implement the two-step approach:
        1. First LLM call identifies claims in the response
        2. Separate LLM calls check each claim against the context
        
        Args:
            test_item: The test item containing input and reference
            response: The response from the system
            client_llm_callable: Optional callable to override the stored LLM client
            prompt: Optional prompt to override the stored prompt
            
        Returns:
            Dict: The metric result
        """
        # Use provided callable or stored client
        llm_callable = client_llm_callable or (self._llm_client.generate_text if self._llm_client else None)
        if not llm_callable:
            raise ValueError("No LLM client provided for metric calculation")
        
        # Use provided prompt or stored prompt
        used_prompt = prompt or self.prompt
        
        # Step 1: Identify claims in the response
        claims, total_claims_count = self._identify_claims(test_item, response, llm_callable, used_prompt)
        
        if not claims:
            logger.warning("No claims identified in the response")
            return {
                "value": 0.0,
                "explanation": "No claims identified in the response",
                "claims": [],
                "supported_claims_count": 0,
                "total_claims_count": 0,
                "metric_name": self.name,
                "timestamp": datetime.now().isoformat()
            }
        
        # Get document content
        document_content = self._get_document_content(test_item, response)
        
        if not document_content:
            logger.warning("No document content available for claim verification")
            return {
                "value": 0.0,
                "explanation": "No document content available for claim verification",
                "claims": claims,
                "supported_claims_count": 0,
                "total_claims_count": total_claims_count,
                "metric_name": self.name,
                "timestamp": datetime.now().isoformat()
            }
        
        # Step 2: Verify each claim against the context
        verified_claims, supported_claims_count = self._verify_claims(
            claims, document_content, llm_callable
        )
        
        # Step 3: Calculate embedding similarities (if available)
        embedding_results = self._calculate_embedding_similarities(
            claims, document_content
        )
        
        # Step 4: Calculate faithfulness score
        if total_claims_count > 0:
            faithfulness_score = supported_claims_count / total_claims_count
        else:
            faithfulness_score = 0.0
        
        # Create explanation
        explanation = f"Faithfulness score: {faithfulness_score:.2f} ({supported_claims_count}/{total_claims_count} claims supported)"
        
        # Build result
        result = {
            "value": faithfulness_score,
            "explanation": explanation,
            "claims": verified_claims,
            "supported_claims_count": supported_claims_count,
            "total_claims_count": total_claims_count,
            "metric_name": self.name,
            "timestamp": datetime.now().isoformat()
        }
        
        # Add embedding results if available
        if embedding_results:
            result["custom_measurements"] = embedding_results
        
        return result
    
    def _identify_claims(self, test_item, response, llm_callable, prompt):
        """
        Identify claims in the response using LLM.
        
        Args:
            test_item: The test item
            response: The response
            llm_callable: The LLM callable
            prompt: The prompt to use
            
        Returns:
            Tuple[List[str], int]: List of claims and total claims count
        """
        # Get answer text
        answer_text = response.content if hasattr(response, "content") else str(response)
        
        # Format the prompt
        try:
            formatted_prompt = prompt.safe_format(
                model_answer=answer_text
            )
        except Exception as e:
            logger.warning(f"Error formatting faithfulness prompt: {e}")
            return [], 0
        
        # Call LLM to identify claims
        llm_response = llm_callable(formatted_prompt)
        
        # Process response
        try:
            from ..core.utils import parse_json
            json_output = parse_json(llm_response, return_type="object")
            
            # Extract claims
            raw_claims = json_output.get("claims", [])
            
            # Deduplicate claims
            claims = self._deduplicate_claims(raw_claims)
            
            # Use the deduplicated count or the provided count, whichever is smaller
            llm_count = json_output.get("total_claims_count", len(raw_claims))
            total_claims_count = min(llm_count, len(claims))
            
            logger.info(f"Identified {len(raw_claims)} claims, deduplicated to {len(claims)}")
            
            return claims, total_claims_count
            
        except Exception as e:
            logger.warning(f"Failed to parse LLM response for claim identification: {e}")
            return [], 0
    
    def _deduplicate_claims(self, claims):
        """
        Deduplicate claims by normalizing and removing duplicates.
        
        Args:
            claims: List of claims
            
        Returns:
            List[str]: Deduplicated list of claims
        """
        if not claims:
            return []
        
        # Normalize claims (lowercase, remove extra whitespace)
        normalized_claims = {}
        
        for claim in claims:
            if not claim or not isinstance(claim, str):
                continue
                
            # Normalize: lowercase, remove extra whitespace
            normalized = " ".join(claim.lower().split())
            
            # Only add if not already present (keep original case)
            if normalized not in normalized_claims:
                normalized_claims[normalized] = claim
        
        # Return deduplicated claims (original case)
        return list(normalized_claims.values())
    
    def _verify_claims(self, claims, document_content, llm_callable):
        """
        Verify each claim against the context using separate LLM calls.
        
        Args:
            claims: List of claims to verify
            document_content: The document content
            llm_callable: The LLM callable
            
        Returns:
            Tuple[List[Dict], int]: List of verified claims with their support status and count of supported claims
        """
        verified_claims = []
        supported_claims_count = 0
        
        for claim in claims:
            # Format the verification prompt
            try:
                formatted_prompt = self.verification_prompt.safe_format(
                    document_content=document_content,
                    claim=claim
                )
            except Exception as e:
                logger.warning(f"Error formatting verification prompt: {e}")
                verified_claims.append({
                    "claim": claim,
                    "supported": False,
                    "explanation": f"Error formatting verification prompt: {e}"
                })
                continue
            
            # Call LLM to verify claim
            llm_response = llm_callable(formatted_prompt)
            
            # Process response
            try:
                from ..core.utils import parse_json
                json_output = parse_json(llm_response, return_type="object")
                
                # Extract verification result
                is_supported = json_output.get("supported", False)
                explanation = json_output.get("explanation", "")
                
                verified_claims.append({
                    "claim": claim,
                    "supported": is_supported,
                    "explanation": explanation
                })
                
                if is_supported:
                    supported_claims_count += 1
                
            except Exception as e:
                logger.warning(f"Failed to parse LLM response for claim verification: {e}")
                verified_claims.append({
                    "claim": claim,
                    "supported": False,
                    "explanation": f"Failed to parse LLM response: {e}"
                })
        
        return verified_claims, supported_claims_count
    
    def _get_document_content(self, test_item, response):
        """
        Get document content from test item or response.
        
        Args:
            test_item: The test item
            response: The response
            
        Returns:
            str: The document content
        """
        # Try to get documents from different sources
        if hasattr(response, "documents") and response.documents:
            return response.documents[0]
        elif hasattr(test_item, "document") and hasattr(test_item.document, "content"):
            return test_item.document.content
        elif hasattr(test_item, "document_content"):
            return test_item.document_content
        elif isinstance(test_item, dict) and "document_content" in test_item:
            return test_item["document_content"]
        
        return ""
    
    def _calculate_embedding_similarities(self, claims, document_content):
        """
        Calculate embedding similarity for each claim.
        
        Args:
            claims: List of claims
            document_content: The document content
            
        Returns:
            dict or None: Embedding similarity results
        """
        # Check if we have access to embeddings
        if not (self._llm_client and hasattr(self._llm_client, "get_embeddings")):
            return None
        
        similarity_scores = []
        embedding_supported_claims = []
        
        try:
            from ..core.utils import cosine_similarity
            
            # Get document embedding
            doc_embedding = self._llm_client.get_embeddings(document_content)[0]
            
            # Calculate similarity for each claim
            for claim in claims:
                claim_text = claim if isinstance(claim, str) else claim.get("claim", "")
                if not claim_text:
                    continue
                
                # Get claim embedding
                claim_embedding = self._llm_client.get_embeddings(claim_text)[0]
                
                # Calculate similarity
                similarity = cosine_similarity(claim_embedding, doc_embedding)
                
                # Determine if supported by embedding similarity
                is_supported_by_embedding = similarity >= self.similarity_threshold
                
                # Add to results
                similarity_scores.append({
                    "claim": claim_text,
                    "similarity": similarity,
                    "supported_by_embedding": is_supported_by_embedding
                })
                
                if is_supported_by_embedding:
                    embedding_supported_claims.append(claim_text)
            
            # Calculate embedding-based faithfulness score
            embedding_faithfulness = len(embedding_supported_claims) / len(claims) if claims else 0.0
            
            return {
                "embedding_similarities": similarity_scores,
                "embedding_supported_claims": embedding_supported_claims,
                "embedding_faithfulness": embedding_faithfulness
            }
            
        except Exception as e:
            logger.warning(f"Error calculating embedding similarities: {e}")
            return None

class RelevanceMetric(LLMMeasuredBaseMetric):
    """
    Metric for evaluating the relevance of an answer to the input.
    
    This metric measures how well the answer addresses the input.
    """
    name = "Relevance"
    description = "Measures how relevant the answer is to the input"
    greater_is_better = True
    context = MetricContext.EVALUATION
    category = MetricCategory.QUALITY
    
    def __init__(self, llm_client=None, include_raw_response=False):
        """
        Initialize the relevance metric.
        
        Args:
            llm_client: The LLM client
            include_raw_response: Whether to include the raw LLM response in the output
        """
        super().__init__(prompt=RELEVANCE_EVALUATION_PROMPT, llm_client=llm_client, include_raw_response=include_raw_response)
    
    def _format_prompt(self, prompt, test_item, response):
        """
        Format the prompt with test item and response data.
        
        Args:
            prompt: The prompt template
            test_item: The test item
            response: The response
            
        Returns:
            str: The formatted prompt
        """
        # Get answer text
        answer_text = response.content if hasattr(response, "content") else str(response)
        
        # Format the prompt
        try:
            return prompt.safe_format(
                input=test_item.input if hasattr(test_item, "input") else "",
                model_answer=answer_text
            )
        except Exception as e:
            logger.warning(f"Error formatting relevance prompt: {e}")
            return str(prompt)
    

class CoherenceMetric(LLMMeasuredBaseMetric):
    """
    Metric for evaluating the coherence of an answer.
    
    This metric measures how well-structured and logical the answer is.
    """
    name = "Coherence"
    description = "Measures how coherent, well-structured, and logical the answer is"
    greater_is_better = True
    context = MetricContext.EVALUATION
    category = MetricCategory.QUALITY
    
    def __init__(self, llm_client=None, include_raw_response=False):
        """
        Initialize the coherence metric.
        
        Args:
            llm_client: The LLM client
            include_raw_response: Whether to include the raw LLM response in the output
        """
        super().__init__(prompt=COHERENCE_EVALUATION_PROMPT, llm_client=llm_client, include_raw_response=include_raw_response)
    
    def _format_prompt(self, prompt, test_item, response):
        """
        Format the prompt with test item and response data.
        
        Args:
            prompt: The prompt template
            test_item: The test item
            response: The response
            
        Returns:
            str: The formatted prompt
        """
        # Get answer text
        answer_text = response.content if hasattr(response, "content") else str(response)
        
        # Format the prompt
        try:
            return prompt.safe_format(
                model_answer=answer_text
            )
        except Exception as e:
            logger.warning(f"Error formatting coherence prompt: {e}")
            return str(prompt)
    

class FluencyMetric(LLMMeasuredBaseMetric):
    """
    Metric for evaluating the fluency of an answer.
    
    This metric measures how grammatically correct and natural the answer is.
    """
    name = "Fluency"
    description = "Measures how grammatically correct and natural the answer is"
    greater_is_better = True
    context = MetricContext.EVALUATION
    category = MetricCategory.QUALITY
    
    def __init__(self, llm_client=None, include_raw_response=False):
        """
        Initialize the fluency metric.
        
        Args:
            llm_client: The LLM client
            include_raw_response: Whether to include the raw LLM response in the output
        """
        super().__init__(prompt=FLUENCY_EVALUATION_PROMPT, llm_client=llm_client, include_raw_response=include_raw_response)
    
    def _format_prompt(self, prompt, test_item, response):
        """
        Format the prompt with test item and response data.
        
        Args:
            prompt: The prompt template
            test_item: The test item
            response: The response
            
        Returns:
            str: The formatted prompt
        """
        # Get answer text
        answer_text = response.content if hasattr(response, "content") else str(response)
        
        # Format the prompt
        try:
            return prompt.safe_format(
                model_answer=answer_text
            )
        except Exception as e:
            logger.warning(f"Error formatting fluency prompt: {e}")
            return str(prompt)
    
    
    def _get_custom_measurements(self, llm_response, test_item, response, result, llm_custom_measurements=None):
        """
        Get custom measurements based on the LLM response.
        
        Args:
            llm_response: The raw response from the LLM
            test_item: The test item
            response: The response
            result: The processed result dictionary
            llm_custom_measurements: Custom measurements provided by the LLM, if any
            
        Returns:
            dict or None: Custom measurements to add to the result
        """
        # Extract errors if present in the LLM response
        try:
            from ..core.utils import parse_json
            json_output = parse_json(llm_response, return_type="object")
            errors = json_output.get("errors", [])
            if errors:
                return {"errors": errors}
        except Exception:
            pass
        return None
    
class ContextPrecisionMetric(LLMMeasuredBaseMetric):
    """
    Metric for evaluating the precision of retrieved contexts.
    
    This metric measures the proportion of relevant chunks in the retrieved contexts.
    It can operate in different modes:
    1. LLM-based with reference answer
    2. LLM-based without reference (comparing to response)
    3. Non-LLM-based with reference contexts (using similarity measures)
    
    The mode is determined by the parameters provided during initialization and call.
    """
    name = "ContextPrecision"
    description = "Measures the precision of retrieved contexts"
    greater_is_better = True
    context = MetricContext.EVALUATION
    category = MetricCategory.QUALITY
    
    def __init__(
        self,
        llm_client=None,
        use_llm=True,
        similarity_threshold=0.7,
        similarity_measure="cosine",
        include_raw_response=False,
        prompt=None
    ):
        """
        Initialize the context precision metric.
        
        Args:
            llm_client: The LLM client to use for evaluation
            use_llm: Whether to use LLM for relevance determination
            similarity_threshold: Threshold for non-LLM similarity
            similarity_measure: Similarity measure to use for non-LLM comparison
            include_raw_response: Whether to include raw LLM response
            prompt: Custom prompt to use for LLM evaluation
        """
        # Initialize with default prompt (will be selected in _format_prompt based on parameters)
        super().__init__(prompt=prompt, llm_client=llm_client, include_raw_response=include_raw_response)
        
        self.use_llm = use_llm
        self.similarity_threshold = similarity_threshold
        self.similarity_measure = similarity_measure
    
    def __call__(self, test_item, response, client_llm_callable=None, prompt=None):
        """
        Calculate the context precision.
        
        Args:
            test_item: The test item containing input and reference
            response: The response from the system
            client_llm_callable: Optional callable to override the stored LLM client
            prompt: Optional prompt to override the stored prompt
            
        Returns:
            Dict: The metric result
        """
        # Determine if we have reference answer or contexts
        has_reference_answer = (hasattr(test_item, "reference_answer") and test_item.reference_answer is not None)
        has_reference_contexts = (hasattr(test_item, "reference_contexts") and test_item.reference_contexts is not None)
        
        # Get retrieved contexts
        retrieved_contexts = []
        if hasattr(response, "documents") and response.documents:
            retrieved_contexts = response.documents
        elif hasattr(response, "contexts") and response.contexts:
            retrieved_contexts = response.contexts
        
        if not retrieved_contexts:
            logger.warning("No retrieved contexts found for context precision evaluation")
            return {
                "value": 0.0,
                "explanation": "No retrieved contexts found",
                "metric_name": self.name,
                "timestamp": datetime.now().isoformat()
            }
        
        # Choose evaluation method based on parameters and available data
        if self.use_llm:
            # Use LLM-based evaluation
            if has_reference_answer:
                return self._evaluate_with_llm(test_item, response, retrieved_contexts, 
                                              use_reference=True, client_llm_callable=client_llm_callable, prompt=prompt)
            else:
                return self._evaluate_with_llm(test_item, response, retrieved_contexts, 
                                              use_reference=False, client_llm_callable=client_llm_callable, prompt=prompt)
        else:
            # Use non-LLM evaluation
            if has_reference_contexts:
                return self._evaluate_with_similarity(test_item, response, retrieved_contexts)
            else:
                logger.warning("Non-LLM evaluation requires reference contexts")
                return {
                    "value": 0.0,
                    "explanation": "Non-LLM evaluation requires reference contexts",
                    "metric_name": self.name,
                    "timestamp": datetime.now().isoformat()
                }
    
    def _evaluate_with_llm(self, test_item, response, retrieved_contexts, use_reference=True, client_llm_callable=None, prompt=None):
        """
        Evaluate context precision using LLM.
        
        Args:
            test_item: The test item
            response: The response
            retrieved_contexts: The retrieved contexts
            use_reference: Whether to use reference answer
            client_llm_callable: Optional callable to override the stored LLM client
            prompt: Optional prompt to override the stored prompt
            
        Returns:
            Dict: The metric result
        """
        # Use provided callable or stored client
        llm_callable = client_llm_callable or (self._llm_client.generate_text if self._llm_client else None)
        if not llm_callable:
            raise ValueError("No LLM client provided for metric calculation")
        
        # Select appropriate prompt
        used_prompt = prompt or self.prompt
        if used_prompt is None:
            if use_reference:
                used_prompt = CONTEXT_PRECISION_WITH_REFERENCE_PROMPT
            else:
                used_prompt = CONTEXT_PRECISION_WITHOUT_REFERENCE_PROMPT
        
        # Evaluate each context
        relevance_scores = []
        relevant_contexts = []
        irrelevant_contexts = []
        explanations = []
        
        for i, context in enumerate(retrieved_contexts):
            # Format prompt for this context
            formatted_prompt = self._format_context_prompt(
                used_prompt, 
                test_item, 
                response, 
                context, 
                use_reference
            )
            
            # Call LLM
            llm_response = llm_callable(formatted_prompt)
            
            # Process response
            try:
                from ..core.utils import parse_json
                result = parse_json(llm_response, return_type="object")
                
                # Extract relevance information
                is_relevant = result.get("is_relevant", False)
                relevance_score = float(result.get("relevance_score", 0.0))
                explanation = result.get("explanation", "")
                
                relevance_scores.append(relevance_score)
                explanations.append(f"Context {i+1}: {explanation}")
                
                if is_relevant:
                    relevant_contexts.append(context)
                else:
                    irrelevant_contexts.append(context)
                
            except Exception as e:
                logger.error(f"Error processing LLM response for context {i+1}: {str(e)}")
                relevance_scores.append(0.0)
                explanations.append(f"Context {i+1}: Error processing LLM response")
        
        # Calculate overall precision
        if not relevance_scores:
            precision = 0.0
        else:
            precision = sum(relevance_scores) / len(relevance_scores)
        
        # Create result
        result = {
            "value": precision,
            "explanation": "\n".join(explanations),
            "relevant_contexts_count": len(relevant_contexts),
            "irrelevant_contexts_count": len(irrelevant_contexts),
            "context_scores": relevance_scores,
            "metric_name": self.name,
            "timestamp": datetime.now().isoformat()
        }
        
        if self._include_raw_response:
            result["raw_llm_response"] = llm_response
        
        return result
    
    def _evaluate_with_similarity(self, test_item, response, retrieved_contexts):
        """
        Evaluate context precision using similarity measures.
        
        Args:
            test_item: The test item
            response: The response
            retrieved_contexts: The retrieved contexts
            
        Returns:
            Dict: The metric result
        """
        # Get reference contexts
        reference_contexts = []
        if hasattr(test_item, "reference_contexts") and test_item.reference_contexts:
            reference_contexts = test_item.reference_contexts
        else:
            logger.warning("No reference contexts found for non-LLM context precision evaluation")
            return {
                "value": 0.0,
                "explanation": "No reference contexts found",
                "metric_name": self.name,
                "timestamp": datetime.now().isoformat()
            }
        
        # Calculate similarity for each retrieved context
        relevance_scores = []
        relevant_contexts = []
        irrelevant_contexts = []
        explanations = []
        
        for i, retrieved_context in enumerate(retrieved_contexts):
            # Find best matching reference context
            best_similarity = 0.0
            best_reference = None
            
            for ref_context in reference_contexts:
                similarity = self._calculate_similarity(retrieved_context, ref_context)
                if similarity > best_similarity:
                    best_similarity = similarity
                    best_reference = ref_context
            
            # Determine if relevant based on similarity threshold
            is_relevant = best_similarity >= self.similarity_threshold
            
            relevance_scores.append(best_similarity)
            explanation = f"Context {i+1}: Similarity {best_similarity:.2f} (threshold: {self.similarity_threshold})"
            explanations.append(explanation)
            
            if is_relevant:
                relevant_contexts.append(retrieved_context)
            else:
                irrelevant_contexts.append(retrieved_context)
        
        # Calculate overall precision
        if not relevance_scores:
            precision = 0.0
        else:
            precision = sum(relevance_scores) / len(relevance_scores)
        
        # Create result
        result = {
            "value": precision,
            "explanation": "\n".join(explanations),
            "relevant_contexts_count": len(relevant_contexts),
            "irrelevant_contexts_count": len(irrelevant_contexts),
            "context_scores": relevance_scores,
            "metric_name": self.name,
            "timestamp": datetime.now().isoformat()
        }
        
        return result
    
    def _format_context_prompt(self, prompt, test_item, response, context, use_reference):
        """
        Format the prompt for a specific context.
        
        Args:
            prompt: The prompt template
            test_item: The test item
            response: The response
            context: The context to evaluate
            use_reference: Whether to use reference answer
            
        Returns:
            str: The formatted prompt
        """
        # Get input text
        input_text = ""
        if hasattr(test_item, "input"):
            if hasattr(test_item.input, "content"):
                input_text = test_item.input.content
            else:
                input_text = str(test_item.input)
        
        # Get response text
        response_text = ""
        if hasattr(response, "content"):
            response_text = response.content
        else:
            response_text = str(response)
        
        # Get reference answer text
        reference_text = ""
        if hasattr(test_item, "reference_answer"):
            if hasattr(test_item.reference_answer, "content"):
                reference_text = test_item.reference_answer.content
            else:
                reference_text = str(test_item.reference_answer)
        
        # Get context text
        context_text = context
        if hasattr(context, "content"):
            context_text = context.content
        
        # Format the prompt
        try:
            if use_reference:
                return prompt.safe_format(
                    user_input=input_text,
                    reference_answer=reference_text,
                    retrieved_context=context_text
                )
            else:
                return prompt.safe_format(
                    user_input=input_text,
                    system_response=response_text,
                    retrieved_context=context_text
                )
        except Exception as e:
            logger.warning(f"Error formatting context precision prompt: {e}")
            return str(prompt)
    
    def _calculate_similarity(self, text1, text2):
        """
        Calculate similarity between two texts.
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            float: Similarity score
        """
        # Extract text content if needed
        if hasattr(text1, "content"):
            text1 = text1.content
        if hasattr(text2, "content"):
            text2 = text2.content
        
        # Convert to string if needed
        text1 = str(text1)
        text2 = str(text2)
        
        # Use appropriate similarity measure
        if self.similarity_measure == "cosine":
            from ..core.utils import cosine_similarity
            
            # If we have embeddings from the client, use them
            if self._llm_client and hasattr(self._llm_client, "get_embeddings"):
                try:
                    emb1 = self._llm_client.get_embeddings(text1)[0]
                    emb2 = self._llm_client.get_embeddings(text2)[0]
                    return cosine_similarity(emb1, emb2)
                except Exception as e:
                    logger.warning(f"Error getting embeddings: {e}")
            
            # Fallback to simple token overlap
            tokens1 = set(text1.lower().split())
            tokens2 = set(text2.lower().split())
            
            if not tokens1 or not tokens2:
                return 0.0
            
            intersection = tokens1.intersection(tokens2)
            union = tokens1.union(tokens2)
            
            return len(intersection) / len(union)
        
        elif self.similarity_measure == "jaccard":
            # Simple Jaccard similarity
            tokens1 = set(text1.lower().split())
            tokens2 = set(text2.lower().split())
            
            if not tokens1 or not tokens2:
                return 0.0
            
            intersection = tokens1.intersection(tokens2)
            union = tokens1.union(tokens2)
            
            return len(intersection) / len(union)
        
        else:
            logger.warning(f"Unknown similarity measure: {self.similarity_measure}")
            return 0.0

class ContextRecallMetric(LLMMeasuredBaseMetric):
    """
    Metric for evaluating the recall of retrieved contexts.
    
    This metric measures how many of the relevant documents were successfully retrieved.
    It can operate in different modes:
    1. LLM-based: Uses reference answer as a proxy for reference contexts
       - Breaks down reference into claims
       - Checks if each claim can be attributed to the retrieved contexts
    2. Non-LLM-based: Uses reference contexts directly
       - Uses string comparison metrics to identify if a retrieved context is relevant
    
    The mode is determined by the parameters provided during initialization.
    """
    name = "ContextRecall"
    description = "Measures how many of the relevant documents were successfully retrieved"
    greater_is_better = True
    context = MetricContext.EVALUATION
    category = MetricCategory.QUALITY
    
    def __init__(
        self,
        llm_client=None,
        use_llm=True,
        similarity_threshold=0.7,
        similarity_measure="cosine",
        include_raw_response=False,
        prompt=None
    ):
        """
        Initialize the context recall metric.
        
        Args:
            llm_client: The LLM client to use for evaluation
            use_llm: Whether to use LLM for relevance determination
            similarity_threshold: Threshold for non-LLM similarity
            similarity_measure: Similarity measure to use for non-LLM comparison
            include_raw_response: Whether to include raw LLM response
            prompt: Custom prompt to use for LLM evaluation
        """
        # Initialize with default prompt
        super().__init__(prompt=prompt, llm_client=llm_client, include_raw_response=include_raw_response)
        
        self.use_llm = use_llm
        self.similarity_threshold = similarity_threshold
        self.similarity_measure = similarity_measure
        self.verification_prompt = CLAIM_VERIFICATION_PROMPT
    
    def __call__(self, test_item, response, client_llm_callable=None, prompt=None):
        """
        Calculate the context recall.
        
        Args:
            test_item: The test item containing input and reference
            response: The response from the system
            client_llm_callable: Optional callable to override the stored LLM client
            prompt: Optional prompt to override the stored prompt
            
        Returns:
            Dict: The metric result
        """
        # Determine if we have reference answer or contexts
        has_reference_answer = (hasattr(test_item, "reference_answer") and test_item.reference_answer is not None)
        has_reference_contexts = (hasattr(test_item, "reference_contexts") and test_item.reference_contexts is not None)
        
        # Get retrieved contexts
        retrieved_contexts = []
        if hasattr(response, "documents") and response.documents:
            retrieved_contexts = response.documents
        elif hasattr(response, "contexts") and response.contexts:
            retrieved_contexts = response.contexts
        
        if not retrieved_contexts:
            logger.warning("No retrieved contexts found for context recall evaluation")
            return {
                "value": 0.0,
                "explanation": "No retrieved contexts found",
                "metric_name": self.name,
                "timestamp": datetime.now().isoformat()
            }
        
        # Choose evaluation method based on parameters and available data
        if self.use_llm:
            # Use LLM-based evaluation
            if has_reference_answer:
                return self._evaluate_with_llm(test_item, response, retrieved_contexts, 
                                              client_llm_callable=client_llm_callable, prompt=prompt)
            else:
                logger.warning("LLM-based evaluation requires reference answer")
                return {
                    "value": 0.0,
                    "explanation": "LLM-based evaluation requires reference answer",
                    "metric_name": self.name,
                    "timestamp": datetime.now().isoformat()
                }
        else:
            # Use non-LLM evaluation
            if has_reference_contexts:
                return self._evaluate_with_similarity(test_item, response, retrieved_contexts)
            else:
                logger.warning("Non-LLM evaluation requires reference contexts")
                return {
                    "value": 0.0,
                    "explanation": "Non-LLM evaluation requires reference contexts",
                    "metric_name": self.name,
                    "timestamp": datetime.now().isoformat()
                }
    
    def _evaluate_with_llm(self, test_item, response, retrieved_contexts, client_llm_callable=None, prompt=None):
        """
        Evaluate context recall using LLM.
        
        Args:
            test_item: The test item
            response: The response
            retrieved_contexts: The retrieved contexts
            client_llm_callable: Optional callable to override the stored LLM client
            prompt: Optional prompt to override the stored prompt
            
        Returns:
            Dict: The metric result
        """
        # Use provided callable or stored client
        llm_callable = client_llm_callable or (self._llm_client.generate_text if self._llm_client else None)
        if not llm_callable:
            raise ValueError("No LLM client provided for metric calculation")
        
        # Use provided prompt or default
        used_prompt = prompt or self.prompt or CONTEXT_RECALL_REFERENCE_CLAIMS_PROMPT
        
        # Step 1: Identify claims in the reference answer
        claims, total_claims_count = self._identify_claims_in_reference(test_item, llm_callable, used_prompt)
        
        if not claims:
            logger.warning("No claims identified in the reference answer")
            return {
                "value": 0.0,
                "explanation": "No claims identified in the reference answer",
                "claims": [],
                "supported_claims_count": 0,
                "total_claims_count": 0,
                "metric_name": self.name,
                "timestamp": datetime.now().isoformat()
            }
        
        # Step 2: Verify each claim against the retrieved contexts
        verified_claims, supported_claims_count = self._verify_claims_against_contexts(
            claims, retrieved_contexts, llm_callable
        )
        
        # Step 3: Calculate recall score
        if total_claims_count > 0:
            recall_score = supported_claims_count / total_claims_count
        else:
            recall_score = 0.0
        
        # Create explanation
        explanation = f"Context recall score: {recall_score:.2f} ({supported_claims_count}/{total_claims_count} claims supported by retrieved contexts)"
        
        # Build result
        result = {
            "value": recall_score,
            "explanation": explanation,
            "claims": verified_claims,
            "supported_claims_count": supported_claims_count,
            "total_claims_count": total_claims_count,
            "metric_name": self.name,
            "timestamp": datetime.now().isoformat()
        }
        
        return result
    
    def _evaluate_with_similarity(self, test_item, response, retrieved_contexts):
        """
        Evaluate context recall using similarity measures.
        
        Args:
            test_item: The test item
            response: The response
            retrieved_contexts: The retrieved contexts
            
        Returns:
            Dict: The metric result
        """
        # Get reference contexts
        reference_contexts = []
        if hasattr(test_item, "reference_contexts") and test_item.reference_contexts:
            reference_contexts = test_item.reference_contexts
        else:
            logger.warning("No reference contexts found for non-LLM context recall evaluation")
            return {
                "value": 0.0,
                "explanation": "No reference contexts found",
                "metric_name": self.name,
                "timestamp": datetime.now().isoformat()
            }
        
        # Calculate similarity for each reference context
        relevant_contexts_found = []
        explanations = []
        
        for i, ref_context in enumerate(reference_contexts):
            # Find best matching retrieved context
            best_similarity = 0.0
            best_retrieved = None
            
            for retrieved_context in retrieved_contexts:
                similarity = self._calculate_similarity(ref_context, retrieved_context)
                if similarity > best_similarity:
                    best_similarity = similarity
                    best_retrieved = retrieved_context
            
            # Determine if relevant based on similarity threshold
            is_found = best_similarity >= self.similarity_threshold
            
            explanation = f"Reference context {i+1}: Similarity {best_similarity:.2f} (threshold: {self.similarity_threshold})"
            explanations.append(explanation)
            
            if is_found:
                relevant_contexts_found.append({
                    "reference_context": ref_context,
                    "retrieved_context": best_retrieved,
                    "similarity": best_similarity
                })
        
        # Calculate recall score
        if reference_contexts:
            recall_score = len(relevant_contexts_found) / len(reference_contexts)
        else:
            recall_score = 0.0
        
        # Create result
        result = {
            "value": recall_score,
            "explanation": f"Context recall score: {recall_score:.2f} ({len(relevant_contexts_found)}/{len(reference_contexts)} reference contexts found)\n" + "\n".join(explanations),
            "relevant_contexts_found": relevant_contexts_found,
            "total_reference_contexts": len(reference_contexts),
            "metric_name": self.name,
            "timestamp": datetime.now().isoformat()
        }
        
        return result
    
    def _identify_claims_in_reference(self, test_item, llm_callable, prompt):
        """
        Identify claims in the reference answer using LLM.
        
        Args:
            test_item: The test item
            llm_callable: The LLM callable
            prompt: The prompt to use
            
        Returns:
            Tuple[List[str], int]: List of claims and total claims count
        """
        # Get reference answer text
        if not hasattr(test_item, "reference_answer"):
            logger.warning("No reference answer available for claim identification")
            return [], 0
            
        reference_answer = test_item.reference_answer
        if hasattr(reference_answer, "content"):
            reference_answer = reference_answer.content
        
        # Format the prompt
        try:
            formatted_prompt = prompt.safe_format(
                reference_answer=reference_answer
            )
        except Exception as e:
            logger.warning(f"Error formatting reference claims prompt: {e}")
            return [], 0
        
        # Call LLM to identify claims
        llm_response = llm_callable(formatted_prompt)
        
        # Process response
        try:
            from ..core.utils import parse_json
            json_output = parse_json(llm_response, return_type="object")
            
            # Extract claims
            raw_claims = json_output.get("claims", [])
            
            # Deduplicate claims
            claims = self._deduplicate_claims(raw_claims)
            
            # Use the deduplicated count or the provided count, whichever is smaller
            llm_count = json_output.get("total_claims_count", len(raw_claims))
            total_claims_count = min(llm_count, len(claims))
            
            logger.info(f"Identified {len(raw_claims)} claims in reference, deduplicated to {len(claims)}")
            
            return claims, total_claims_count
            
        except Exception as e:
            logger.warning(f"Failed to parse LLM response for reference claim identification: {e}")
            return [], 0
    
    def _deduplicate_claims(self, claims):
        """
        Deduplicate claims by normalizing and removing duplicates.
        
        Args:
            claims: List of claims
            
        Returns:
            List[str]: Deduplicated list of claims
        """
        if not claims:
            return []
        
        # Normalize claims (lowercase, remove extra whitespace)
        normalized_claims = {}
        
        for claim in claims:
            if not claim or not isinstance(claim, str):
                continue
                
            # Normalize: lowercase, remove extra whitespace
            normalized = " ".join(claim.lower().split())
            
            # Only add if not already present (keep original case)
            if normalized not in normalized_claims:
                normalized_claims[normalized] = claim
        
        # Return deduplicated claims (original case)
        return list(normalized_claims.values())
    
    def _verify_claims_against_contexts(self, claims, retrieved_contexts, llm_callable):
        """
        Verify each claim against the retrieved contexts using separate LLM calls.
        
        Args:
            claims: List of claims to verify
            retrieved_contexts: The retrieved contexts
            llm_callable: The LLM callable
            
        Returns:
            Tuple[List[Dict], int]: List of verified claims with their support status and count of supported claims
        """
        verified_claims = []
        supported_claims_count = 0
        
        # Combine all retrieved contexts into a single document
        combined_contexts = "\n\n".join([str(ctx) for ctx in retrieved_contexts])
        
        for claim in claims:
            # Format the verification prompt
            try:
                formatted_prompt = self.verification_prompt.safe_format(
                    document_content=combined_contexts,
                    claim=claim
                )
            except Exception as e:
                logger.warning(f"Error formatting verification prompt: {e}")
                verified_claims.append({
                    "claim": claim,
                    "supported": False,
                    "explanation": f"Error formatting verification prompt: {e}"
                })
                continue
            
            # Call LLM to verify claim
            llm_response = llm_callable(formatted_prompt)
            
            # Process response
            try:
                from ..core.utils import parse_json
                json_output = parse_json(llm_response, return_type="object")
                
                # Extract verification result
                is_supported = json_output.get("supported", False)
                explanation = json_output.get("explanation", "")
                
                verified_claims.append({
                    "claim": claim,
                    "supported": is_supported,
                    "explanation": explanation
                })
                
                if is_supported:
                    supported_claims_count += 1
                
            except Exception as e:
                logger.warning(f"Failed to parse LLM response for claim verification: {e}")
                verified_claims.append({
                    "claim": claim,
                    "supported": False,
                    "explanation": f"Failed to parse LLM response: {e}"
                })
        
        return verified_claims, supported_claims_count
    
    def _calculate_similarity(self, text1, text2):
        """
        Calculate similarity between two texts.
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            float: Similarity score
        """
        # Extract text content if needed
        if hasattr(text1, "content"):
            text1 = text1.content
        if hasattr(text2, "content"):
            text2 = text2.content
        
        # Convert to string if needed
        text1 = str(text1)
        text2 = str(text2)
        
        # Use appropriate similarity measure
        if self.similarity_measure == "cosine":
            from ..core.utils import cosine_similarity
            
            # If we have embeddings from the client, use them
            if self._llm_client and hasattr(self._llm_client, "get_embeddings"):
                try:
                    emb1 = self._llm_client.get_embeddings(text1)[0]
                    emb2 = self._llm_client.get_embeddings(text2)[0]
                    return cosine_similarity(emb1, emb2)
                except Exception as e:
                    logger.warning(f"Error getting embeddings: {e}")
            
            # Fallback to simple token overlap
            tokens1 = set(text1.lower().split())
            tokens2 = set(text2.lower().split())
            
            if not tokens1 or not tokens2:
                return 0.0
            
            intersection = tokens1.intersection(tokens2)
            union = tokens1.union(tokens2)
            
            return len(intersection) / len(union)
        
        elif self.similarity_measure == "jaccard":
            # Simple Jaccard similarity
            tokens1 = set(text1.lower().split())
            tokens2 = set(text2.lower().split())
            
            if not tokens1 or not tokens2:
                return 0.0
            
            intersection = tokens1.intersection(tokens2)
            union = tokens1.union(tokens2)
            
            return len(intersection) / len(union)
        
        else:
            logger.warning(f"Unknown similarity measure: {self.similarity_measure}")
            return 0.0

class ResponseRelevancyMetric(LLMMeasuredBaseMetric):
    """
    Metric for evaluating the relevancy of a response to the user input.
    
    This metric measures how relevant a response is to the user input by generating
    artificial questions based on the response and calculating the cosine similarity
    between the user input and these questions.
    
    Higher scores indicate better alignment with the user input, while lower scores
    are given if the response is incomplete or includes redundant information.
    """
    name = "ResponseRelevancy"
    description = "Measures how relevant a response is to the user input"
    greater_is_better = True
    context = MetricContext.EVALUATION
    category = MetricCategory.QUALITY
    
    def __init__(self, llm_client=None, num_questions=3, include_raw_response=False):
        """
        Initialize the response relevancy metric.
        
        Args:
            llm_client: The LLM client
            num_questions: Number of questions to generate for evaluation (default: 3)
            include_raw_response: Whether to include the raw LLM response in the output
        """
        self.num_questions = num_questions
        super().__init__(prompt=RESPONSE_RELEVANCY_EVALUATION_PROMPT, llm_client=llm_client, include_raw_response=include_raw_response)
    
    def _format_prompt(self, prompt, test_item, response):
        """
        Format the prompt with test item and response data.
        
        Args:
            prompt: The prompt template
            test_item: The test item
            response: The response
            
        Returns:
            str: The formatted prompt
        """
        # Get user input text
        user_input = ""
        if hasattr(test_item, "input"):
            if hasattr(test_item.input, "content"):
                user_input = test_item.input.content
            else:
                user_input = str(test_item.input)
        
        # Get response text
        response_text = response.content if hasattr(response, "content") else str(response)
        
        # Format the prompt
        try:
            return prompt.safe_format(
                user_input=user_input,
                system_response=response_text,
                num_questions=self.num_questions
            )
        except Exception as e:
            logger.warning(f"Error formatting response relevancy prompt: {e}")
            return str(prompt)
    
    def _process_llm_response(self, llm_response):
        """
        Process the LLM response to extract the generated questions.
        
        Args:
            llm_response: The raw response from the LLM
            
        Returns:
            dict: A dictionary with the extracted questions and value
        """
        try:
            from ..core.utils import parse_json
            result = parse_json(llm_response, return_type="object")
            
            # Extract questions from the response
            questions = result.get("questions", [])
            explanation = result.get("explanation", "")
            
            # Return with a default value - will be updated in _get_custom_measurements
            return {
                "value": 0.0,  # Default value, will be updated
                "explanation": explanation,
                "questions": questions,
                "raw_llm_response": llm_response
            }
        except Exception as e:
            logger.error(f"Error processing LLM response: {str(e)}")
            return {
                "value": 0.0,  # Default value
                "explanation": f"Error processing response: {str(e)}",
                "questions": [],
                "raw_llm_response": llm_response
            }
    
    def _get_custom_measurements(self, llm_response, test_item, response, result, llm_custom_measurements=None):
        """
        Calculate the response relevancy score based on cosine similarity between
        user input and generated questions.
        
        Args:
            llm_response: The raw response from the LLM
            test_item: The test item
            response: The response
            result: The processed result dictionary
            llm_custom_measurements: Custom measurements provided by the LLM, if any
            
        Returns:
            dict: Custom measurements for the result
        """
        # Get user input text
        user_input = ""
        if hasattr(test_item, "input"):
            if hasattr(test_item.input, "content"):
                user_input = test_item.input.content
            else:
                user_input = str(test_item.input)
        
        # Get questions from the result
        questions = result.get("questions", [])
        
        if not questions:
            logger.warning("No questions generated for response relevancy evaluation")
            # Update the result value to 0.0 (already set in _process_llm_response)
            result["explanation"] = "No questions generated for evaluation"
            # Return custom measurements only
            return {
                "generated_questions": [],
                "similarity_scores": [],
                "num_questions": 0
            }
        
        # Calculate cosine similarity between user input and each question
        similarity_scores = []
        
        try:
            from ..core.utils import cosine_similarity
            
            # Generate embeddings for user input and questions
            if self._llm_client and hasattr(self._llm_client, "get_embeddings"):
                # Get embedding for user input
                user_input_embedding = self._llm_client.get_embeddings(user_input)[0]
                
                # Get embeddings for questions and calculate similarity
                for question in questions:
                    question_embedding = self._llm_client.get_embeddings(question)[0]
                    similarity = cosine_similarity(user_input_embedding, question_embedding)
                    similarity_scores.append(similarity)
            else:
                logger.warning("No embedding client available for response relevancy calculation")
                # Fallback to a default score
                similarity_scores = [0.5] * len(questions)
        except Exception as e:
            logger.error(f"Error calculating similarity: {str(e)}")
            # Fallback to a default score
            similarity_scores = [0.5] * len(questions)
        
        # Calculate average similarity score
        avg_similarity = sum(similarity_scores) / len(similarity_scores) if similarity_scores else 0.0
        
        # Create explanation
        explanation = f"Response relevancy score: {avg_similarity:.2f} based on {len(questions)} generated questions."
        if similarity_scores:
            explanation += f" Individual similarity scores: {', '.join([f'{s:.2f}' for s in similarity_scores])}"
        
        # Update the result value and explanation
        result["value"] = avg_similarity
        result["explanation"] = explanation
        
        # Return only the custom measurements
        return {
            "generated_questions": questions,
            "similarity_scores": similarity_scores,
            "num_questions": len(questions)
        }

# Register metrics
register_metric(CorrectnessMetric)
register_metric(FaithfulnessMetric)
register_metric(RelevanceMetric)
register_metric(CoherenceMetric)
register_metric(FluencyMetric)
register_metric(ContextPrecisionMetric)
register_metric(ContextRecallMetric)
register_metric(ResponseRelevancyMetric)
