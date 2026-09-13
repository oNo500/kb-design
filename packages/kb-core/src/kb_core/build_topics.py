"""Compatibility entry point; topic generation is owned by kb-topics."""
try:
    from kb_topics.build import (
        TODAY, VERSION, _assemble_topics, build_topics, main, slug, topic_output_path,
    )
except ModuleNotFoundError as exc:
    if exc.name not in {"kb_topics", "kb_topics.build"}:
        raise
    raise ImportError("Topic generation requires kb-topics; install it or run uv sync in kb-design.") from exc


if __name__ == "__main__":
    raise SystemExit(main())
