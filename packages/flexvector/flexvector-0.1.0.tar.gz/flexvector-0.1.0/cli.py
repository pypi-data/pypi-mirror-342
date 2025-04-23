import argparse
import sys
import time
from typing import List

from loguru import logger

from flexvector.config import VectorDBSettings
from flexvector.core.models import Document, VectorDBClient
from flexvector.factory import VectorDBFactory


def load_data(db_instance: VectorDBClient, input_path: str, collection_name: str):
    logger.info(f"Loading data from {input_path} into collection '{collection_name}'")
    return db_instance.load(collection_name=collection_name, path=input_path)


def query_data(db_instance: VectorDBClient, query: str, collection_name: str, top_k: int = 3):
    results = db_instance.search(
        collection_name=collection_name,
        query=query,
        top_k=top_k
    )
    return results


def delete_collection(db_instance: VectorDBClient, collection_name: str):
    logger.info(f"Deleting collection '{collection_name}'")
    try:
        db_instance.remove_collection(collection_name)
        logger.success(f"Collection '{collection_name}' deleted successfully")
    except Exception as e:
        logger.error(f"Failed to delete collection: {e}")
        sys.exit(1)


def _display_results(results: List[Document]):
    if not results:
        logger.warning("No results found")
        return
    
    logger.info(f"Found {len(results)} results:")
    for i, doc in enumerate(results):
        content = doc.page_content
        # Truncate content if it's too long
        if len(content) > 300:
            content = content[:297] + "..."
            
        logger.info(f"\nResult {i+1}:")
        logger.info(f"Content: {content}")
        logger.info(f"Metadata: {doc.metadata}")
        logger.info("-" * 50)


def main():
    if args.verbose:
        logger.level("DEBUG")
    else:
        logger.level("INFO")

    logger.info(f"Running Operation: {args.operation}")
    
    start = time.perf_counter()

    config = VectorDBSettings()
    db_instance = VectorDBFactory.get(args.db_type, config)

    if args.operation == "load":
        if args.input_file:
            load_data(db_instance, args.input_file, args.collection)
        elif args.input_dir:
            load_data(db_instance, args.input_dir, args.collection)
        else:
            logger.error("Please provide either input file or input directory")
            sys.exit(1)
        logger.info(f"Data loaded successfully into collection '{args.collection}'! Time taken: {time.perf_counter() - start:.2f} seconds")
    
    elif args.operation == "search":
        if not args.query:
            logger.error("Please provide a search query")
            sys.exit(1)
        results = query_data(db_instance, args.query, args.collection, args.top_k)
        _display_results(results)
        logger.info(f"Search completed in {time.perf_counter() - start:.2f} seconds")
    
    elif args.operation == "delete":
        delete_collection(db_instance, args.collection)
        logger.info(f"Operation completed in {time.perf_counter() - start:.2f} seconds")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="flexvector CLI - Tool for interacting with flexvector stores",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    # Required arguments
    parser.add_argument(
        "operation",
        choices=["load", "search", "delete"],
        help="Operation to perform:\n"
             "  load   - Load data into a flexvector collection\n"
             "  search - Search for similar documents in a flexvector collection\n"
             "  delete - Delete a flexvector collection"
    )
    
    # Database configuration
    parser.add_argument(
        "--db-type", "-t",
        choices=["chroma", "qdrant", "weaviate", "pg"],
        default="chroma",
        help="flexvector store type (default: chroma)"
    )
    
    parser.add_argument(
        "--collection", "-c",
        type=str,
        default="default",
        help="Collection name (default: default)"
    )
    
    # Input options for load operation
    parser.add_argument(
        "--input-file", "-i",
        type=str,
        help="Input file path (for load operation)"
    )
    
    parser.add_argument(
        "--input-dir", "-d",
        type=str,
        help="Input directory path (for load operation)"
    )
    
    # Search options
    parser.add_argument(
        "--query", "-q",
        type=str,
        help="Search query (for search operation)"
    )
    
    parser.add_argument(
        "--top-k",
        "-k",
        type=int,
        default=3,
        help="Number of results to return (default: 3)"
    )
    
    # Other options
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    if args.operation == "load" and not (args.input_file or args.input_dir):
        parser.error("The load operation requires either --input-file or --input-dir")
    
    if args.operation == "search" and not args.query:
        parser.error("The search operation requires --query")
    
    main()


# Examples:
# # Load documents from a single file
# python cli.py load --input-file examples/files/data.txt --collection my_documents --verbose

# # Load documents from a directory
# python cli.py load --input-dir examples/files --collection research_papers --verbose

# # Search for documents
# python cli.py search --query "What is vector database?" --collection my_documents --top-k 5 --verbose

# # Delete a collection
# python cli.py delete --collection my_documents --verbose
