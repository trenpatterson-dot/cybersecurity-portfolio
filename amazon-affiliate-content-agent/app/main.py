"""Application entry point for the end-to-end draft workflow."""

from __future__ import annotations

from dataclasses import replace

from app.approval_queue import save_compliance_result, save_draft, update_draft_status
from app.compliance import check_draft_compliance
from app.config import ConfigError, load_settings
from app.db import initialize_database
from app.deal_scoring import score_products, sort_scored_products
from app.drafts import generate_all_draft_types
from app.logger import setup_logger
from app.models import BLOCKED, DRAFTED, READY_FOR_REVIEW, ProductDraft
from app.product_source import resolve_provider


def main() -> int:
    """Run the full product-to-review-queue workflow."""

    try:
        settings = load_settings()
    except ConfigError as error:
        print(error)
        return 1

    logger = setup_logger(settings.log_level)

    logger.info("Starting %s in %s mode", settings.app_name, settings.app_env)
    logger.info("Configuration loaded: %s" % settings.safe_log_values())

    try:
        initialize_database(settings.database_path)
    except Exception as error:  # pragma: no cover - defensive startup guard
        logger.error("Database initialization failed: %s", error)
        return 1

    logger.info("Database ready at %s", settings.database_path)

    try:
        summary = run_workflow(settings, logger)
    except Exception as error:  # pragma: no cover - defensive top-level guard
        logger.error("Workflow failed unexpectedly: %s", error)
        return 1

    _print_summary(summary)
    return 0


def run_workflow(settings, logger) -> dict[str, int]:
    """Run the Phase 9 workflow and return summary counts."""

    provider_selection = resolve_provider(settings)
    if provider_selection.fallback_reason:
        logger.warning(
            "Falling back to mock product source because %s",
            provider_selection.fallback_reason,
        )

    logger.info(
        "Loading products from provider '%s'",
        provider_selection.provider_name,
    )
    products = provider_selection.provider.get_all_products()
    logger.info(
        "Loaded %s products from provider '%s'",
        len(products),
        provider_selection.provider_name,
    )

    logger.info("Scoring loaded products")
    scored_products = sort_scored_products(score_products(products))
    logger.info("Scored %s products", len(scored_products))

    summary = {
        "total_products_loaded": len(products),
        "total_drafts_generated": 0,
        "drafts_ready_for_review": 0,
        "drafts_blocked": 0,
    }

    for scored_product in scored_products:
        product = scored_product.product

        try:
            logger.info(
                "Processing product %s with score %s",
                product.product_id,
                scored_product.score,
            )
            drafts = generate_all_draft_types(product)
        except Exception as error:
            logger.error("Skipping product %s because draft generation failed: %s", product.product_id, error)
            continue

        for draft in drafts:
            _process_draft(draft, summary, logger)

    logger.info("Workflow complete")
    return summary


def _process_draft(draft: ProductDraft, summary: dict[str, int], logger) -> None:
    """Save one draft, save its compliance result, then update its queue status."""

    summary["total_drafts_generated"] += 1

    try:
        drafted_record = save_draft(replace(draft, status=DRAFTED))
        compliance_result = check_draft_compliance(drafted_record)
        save_compliance_result(compliance_result)

        final_status = READY_FOR_REVIEW if compliance_result.passed else BLOCKED
        updated_draft = update_draft_status(drafted_record.draft_id, final_status)

        if final_status == READY_FOR_REVIEW:
            summary["drafts_ready_for_review"] += 1
        else:
            summary["drafts_blocked"] += 1

        logger.info(
            "Draft %s processed with compliance status %s and queue status %s",
            updated_draft.draft_id,
            compliance_result.status,
            updated_draft.status,
        )
    except Exception as error:
        summary["drafts_blocked"] += 1
        logger.error("Draft %s could not be fully processed: %s", draft.draft_id, error)


def _print_summary(summary: dict[str, int]) -> None:
    """Print a readable workflow summary for the terminal."""

    print("Workflow Summary")
    print(f"- total products loaded: {summary['total_products_loaded']}")
    print(f"- total drafts generated: {summary['total_drafts_generated']}")
    print(f"- drafts ready for review: {summary['drafts_ready_for_review']}")
    print(f"- drafts blocked: {summary['drafts_blocked']}")


if __name__ == "__main__":
    raise SystemExit(main())
