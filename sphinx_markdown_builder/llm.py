"""Helpers to prune and normalize a docutils doctree for LLM-friendly output."""

from __future__ import annotations

from typing import cast

from docutils import nodes

_NAV_ARTIFACT_TEXTS = frozenset({"genindex", "modindex", "search"})


def _remove_node(node: nodes.Node) -> None:
    if node.parent is not None:
        node.parent.remove(node)


def _is_nav_artifact_list_item(node: nodes.list_item) -> bool:
    text = " ".join(node.astext().split()).strip().lower()
    return text in _NAV_ARTIFACT_TEXTS


def _remove_nav_artifact_lists(doc: nodes.document) -> None:
    for bullet_list in list(doc.findall(nodes.bullet_list)):
        list_items = [child for child in bullet_list.children if isinstance(child, nodes.list_item)]
        if list_items and all(_is_nav_artifact_list_item(item) for item in list_items):
            _remove_node(bullet_list)


def _prune_empty_containers(doc: nodes.document) -> None:
    changed = True
    while changed:
        changed = False

        for bullet_list in list(doc.findall(nodes.bullet_list)):
            if len(bullet_list.children) == 0:
                _remove_node(bullet_list)
                changed = True

        for section in list(doc.findall(nodes.section)):
            children_without_title = [child for child in section.children if not isinstance(child, nodes.title)]
            if len(children_without_title) == 0:
                _remove_node(section)
                changed = True


def prepare_doctree_for_llm(doc: nodes.document) -> nodes.document:
    llm_doc = cast(nodes.document, doc.deepcopy())
    for target in list(llm_doc.findall(nodes.target)):
        _remove_node(target)
    for transition in list(llm_doc.findall(nodes.transition)):
        _remove_node(transition)
    for comment in list(llm_doc.findall(nodes.comment)):
        _remove_node(comment)
    _remove_nav_artifact_lists(llm_doc)
    _prune_empty_containers(llm_doc)
    return llm_doc
