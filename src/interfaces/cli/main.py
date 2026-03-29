import typer
from rich.console import Console
from rich.progress import track
from pathlib import Path
from typing import List, Optional
from domain.services.embedding_service import TechnicalDocEmbeddingService
from domain.entities import DocumentType
from application.commands import ProcessDocumentsCommand, SearchDocumentsCommand
from infrastructure.persistence import ChromaDocumentRepository
from infrastructure.file_handlers import (
    MarkdownHandler,
    RSTHandler,
    PDFHandler,
    TextHandler,
)

app = typer.Typer()
console = Console()

HANDLERS = {
    ".md": MarkdownHandler,
    ".rst": RSTHandler,
    ".pdf": PDFHandler,
    ".txt": TextHandler,
}

VALID_DOC_TYPES = [dt.value for dt in DocumentType]


@app.command()
def process(
    directory: str = typer.Argument(..., help="Directory with technical docs"),
    db_path: str = typer.Option("data/tech_docs_db", help="Path to ChromaDB"),
    source: str = typer.Option("local", help="Source identifier"),
    batch_size: int = typer.Option(32, help="Batch size for processing"),
) -> None:
    """Process technical documentation from a directory"""
    try:
        repo = ChromaDocumentRepository(db_path)
        embedding_service = TechnicalDocEmbeddingService()
        command = ProcessDocumentsCommand(repo, embedding_service)
        documents = []
        for file_path in track(
            Path(directory).rglob("*"), description="Processing files"
        ):
            if file_path.suffix.lower() in HANDLERS:
                handler_class = HANDLERS[file_path.suffix.lower()]
                handler_instance = handler_class(source=source)
                if not hasattr(handler_instance, "parse"):
                    console.print(
                        f"[red]Handler {handler_class.__name__} has no 'parse' method[/red]"
                    )
                    continue
                try:
                    doc = handler_instance.parse(str(file_path))
                    if doc:
                        documents.append(doc)
                except Exception as e:
                    console.print(f"[red]Error processing {file_path}: {str(e)}[/red]")

        if not documents:
            console.print("[yellow]No documents found to process[/yellow]")
            return
        console.print(f"Processing {len(documents)} documents...")
        processed_ids = command.execute_batch(documents, batch_size)
        console.print(
            f"[green]Successfully processed {len(processed_ids)} documents[/green]"
        )
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        raise typer.Exit(1)


@app.command()
def search(
    query: str = typer.Argument(..., help="Search query"),
    db_path: str = typer.Option("data/tech_docs_db", help="Path to ChromaDB"),
    top_k: int = typer.Option(5, help="Number of results"),
    source: Optional[str] = typer.Option(None, help="Filter by source"),
    doc_type: Optional[str] = typer.Option(
        None, help=f"Filter by document type ({', '.join(VALID_DOC_TYPES)})"
    ),
) -> None:
    """Search technical documentation"""
    try:
        repo = ChromaDocumentRepository(db_path)
        embedding_service = TechnicalDocEmbeddingService()
        command = SearchDocumentsCommand(repo, embedding_service)

        filters = {}
        if source:
            filters["source"] = source
        if doc_type:
            doc_type = doc_type.lower()
            if doc_type not in VALID_DOC_TYPES:
                console.print(
                    f"[red]Invalid document type: {doc_type}. Valid types are: {VALID_DOC_TYPES}[/red]"
                )
                raise typer.Exit(1)
            filters["type"] = doc_type

        results = command.execute(query, top_k, **filters)

        for i, doc in enumerate(results, 1):
            console.print(f"[bold]{i}. {doc.title}[/bold]")
            console.print(
                f"[dim]|Source: {doc.source} | Type: {doc.document_type.value}[/dim]"
            )
            console.print(f"[blue]|{doc.file_path}[/blue]")
            console.print(doc.content[:200] + "....\n")
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
