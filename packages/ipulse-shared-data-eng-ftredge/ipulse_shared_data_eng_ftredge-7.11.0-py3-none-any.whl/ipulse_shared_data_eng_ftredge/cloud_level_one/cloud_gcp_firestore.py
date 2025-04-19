import inspect
import logging
from typing import Any, Dict, List, Optional, Union
from google.cloud import firestore
from google.api_core.exceptions import GoogleAPICallError
from ipulse_shared_base_ftredge import (
    LogLevel, DataResource, Action, ProgressStatus, StructLog, log_info, log_warning, log_by_lvl
)
from ..pipelines import FunctionResult, Pipelinemon, handle_pipeline_operation_exception
import datetime
import json

def _sanitize_firestore_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sanitize data before sending to Firestore to prevent common errors.
    
    Args:
        data: Dictionary of data to sanitize
        
    Returns:
        Dictionary with sanitized data
    """
    if not isinstance(data, dict):
        raise ValueError(f"Data must be a dictionary, got {type(data)}")
    
    # Create a deep copy to avoid modifying the original
    sanitized = {}
    
    # Handle special values and nested structures
    for key, value in data.items():
        # Ensure keys are strings
        if not isinstance(key, str):
            key = str(key)
            
        # Handle None values
        if value is None:
            sanitized[key] = ""
        # Handle nested dictionaries recursively
        elif isinstance(value, dict):
            sanitized[key] = _sanitize_firestore_data(value)
        # Handle list/array values
        elif isinstance(value, list):
            sanitized_list = []
            for item in value:
                if isinstance(item, dict):
                    sanitized_list.append(_sanitize_firestore_data(item))
                else:
                    sanitized_list.append(item)
            sanitized[key] = sanitized_list
        # Handle datetime objects
        elif isinstance(value, (datetime.datetime, datetime.date)):
            sanitized[key] = value.isoformat()
        # Pass other values as-is
        else:
            sanitized[key] = value
            
    return sanitized

def merge_firestore_document_extended(
    document_id: str,
    collection: str,
    data: Dict[str, Any],
    firestore_client: firestore.Client,
    merge: bool = True,
    pipelinemon: Optional[Pipelinemon] = None,
    logger: Optional[logging.Logger] = None,
    print_out: bool = False,
    raise_e: bool = False
) -> FunctionResult:
    """
    Merges data into a Firestore document.
    
    Args:
        document_id: Document ID
        collection: Collection name
        data: Data to merge
        firestore_client: Firestore client
        merge: Whether to merge or overwrite document
        pipelinemon: Optional Pipelinemon instance
        logger: Optional logger
        print_out: Whether to print output
        raise_e: Whether to raise exceptions
        
    Returns:
        FunctionResult with operation status
    """
    function_name = inspect.currentframe().f_code.co_name
    result = FunctionResult(function_name)
    result.add_metadata(
        document_id=document_id,
        collection=collection,
        merge=merge
    )
    
    try:
        # Input validation
        if not document_id:
            raise ValueError("document_id cannot be empty")
        if not collection:
            raise ValueError("collection cannot be empty")
        if not data:
            raise ValueError("data cannot be empty")
            
        # Sanitize data to prevent common Firestore errors
        try:
            sanitized_data = _sanitize_firestore_data(data)
        except Exception as sanitize_error:
            raise ValueError(f"Failed to sanitize data: {str(sanitize_error)}") from sanitize_error
        
        # Get document reference
        doc_ref = firestore_client.collection(collection).document(document_id)
        
        # Attempt to set/merge document
        doc_ref.set(sanitized_data, merge=merge)
        
        result.add_state("DOCUMENT_UPDATED")
        
        # Log success
        log_by_lvl(
            info_msg=f"Updated Firestore document {document_id} in collection {collection}",
            debug_msg=json.dumps(sanitized_data)[:200] + "..." if len(json.dumps(sanitized_data)) > 200 else json.dumps(sanitized_data),
            logger=logger,
            print_out=print_out
        )
        
        if pipelinemon:
            pipelinemon.add_system_impacted(f"firestore_write: {document_id}")
            pipelinemon.add_log(StructLog(
                level=LogLevel.INFO,
                action=Action.PERSIST_MERGE_DOCUMENT,
                source=DataResource.IN_MEMORY_DATA,
                destination=DataResource.DB_FIRESTORE,
                progress_status=ProgressStatus.DONE,
                description=result.get_final_report()
            ))
            
    except Exception as e:
        handle_pipeline_operation_exception(
            e=e,
            result=result,
            action=Action.PERSIST_MERGE_DOCUMENT,
            source=DataResource.IN_MEMORY_DATA,
            destination=DataResource.DB_FIRESTORE,
            logger=logger,
            pipelinemon=pipelinemon,
            raise_e=raise_e,
            print_out=print_out
        )
    finally:
        result.final()
    return result


def batch_update_firestore_documents_array_union_extended(
    updates: List[Dict[str, Any]],
    collection: str,
    firestore_client: firestore.Client,
    pipelinemon: Optional[Pipelinemon] = None,
    logger: Optional[logging.Logger] = None,
    print_out: bool = False,
    raise_e: bool = False
) -> FunctionResult:
    """
    Updates multiple Firestore documents in a batch using ArrayUnion.

    Args:
        updates: A list of dictionaries, each containing:
            - 'document_id': The ID of the document to update.
            - 'array_field': The name of the array field to update.
            - 'data_to_add': A list containing the single item to add to the array.
        collection: The name of the Firestore collection.
        firestore_client: Initialized Firestore client.
        pipelinemon: Optional pipeline monitoring object.
        logger: Optional logger instance.
        print_out: Whether to print output.
        raise_e: Whether to raise exceptions.

    Returns:
        FunctionResult indicating the status of the batch operation.
    """
    function_name = inspect.currentframe().f_code.co_name
    result = FunctionResult(function_name)
    result.add_metadata(collection=collection, documents_to_update_count=len(updates))
    action = Action.PERSIST_MERGE_DOCUMENT # Using MERGE as we are adding to existing arrays

    batch = firestore_client.batch()
    updated_doc_ids = []

    try:
        result.add_state("BATCH_UPDATE_STARTED")
        if not updates:
            result.add_notice("No updates provided for batch operation.")
            result.progress_status = ProgressStatus.INTENTIONALLY_SKIPPED
            result.final()
            return result

        for update_info in updates:
            doc_id = update_info.get('document_id')
            array_field = update_info.get('array_field')
            data_to_add = update_info.get('data_to_add') # Should be a list with one element

            if not doc_id or not array_field or data_to_add is None:
                result.add_warning(f"Skipping invalid update instruction: {update_info}")
                continue

            doc_ref = firestore_client.collection(collection).document(doc_id)
            # Use ArrayUnion to append elements to the array field
            batch.update(doc_ref, {array_field: firestore.ArrayUnion(data_to_add)})
            updated_doc_ids.append(doc_id)

        if not updated_doc_ids:
             result.add_notice("No valid documents to update after filtering instructions.")
             result.progress_status = ProgressStatus.INTENTIONALLY_SKIPPED
             result.final()
             return result

        batch_results = batch.commit() # This returns a list of WriteResult objects
        result.add_state("BATCH_UPDATE_COMMITTED")
        result.add_metadata(documents_updated_count=len(updated_doc_ids), batch_commit_results=str(batch_results)) # Store commit results as string for simplicity
        result.final()

        msg = f"Successfully updated {len(updated_doc_ids)} documents in collection '{collection}'."
        log_info(msg=msg, logger=logger, print_out=print_out)
        if pipelinemon:
            pipelinemon.add_system_impacted(f"firestore_batch_update: {collection}")
            pipelinemon.add_log(StructLog(
                level=LogLevel.INFO,
                action=action,
                resource=DataResource.DB_FIRESTORE,
                progress_status=result.progress_status,
                q=len(updated_doc_ids),
                q_unit=DataResource.DB_DOCUMENT,
                description=msg
            ))

    except GoogleAPICallError as firestore_e:
        # Handle specific Firestore API errors if needed
        handle_pipeline_operation_exception(
            e=firestore_e, result=result, action=action, resource=DataResource.DB_FIRESTORE,
            pipelinemon=pipelinemon, logger=logger, print_out=print_out, raise_e=raise_e
        )
    except Exception as e:
        handle_pipeline_operation_exception(
            e=e, result=result, action=action, resource=DataResource.DB_FIRESTORE,
            pipelinemon=pipelinemon, logger=logger, print_out=print_out, raise_e=raise_e
        )
    finally:
        # Ensure final state is set even if commit fails partially or fully
        if result.progress_status not in ProgressStatus.get_closed_statuses():
             result.final() # Call final if not already closed by exception handler

    return result
