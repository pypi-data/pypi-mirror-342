#! /usr/bin/env bash

function test_bluer_geo_watch_targets_get_catalog() {
    bluer_objects_download - $BLUE_GEO_WATCH_TARGET_LIST

    bluer_ai_assert \
        $(bluer_geo_watch_targets get \
            --what catalog \
            --target_name burning-man-2024 \
            --log 0) \
        EarthSearch
    [[ $? -ne 0 ]] && return 1

    bluer_ai_assert \
        "$(bluer_geo_watch_targets get \
            --what catalog \
            --target_name Deadpool \
            --log 0)" \
        - empty
}

function test_bluer_geo_watch_targets_get_collection() {
    bluer_objects_download - $BLUE_GEO_WATCH_TARGET_LIST

    bluer_ai_assert \
        $(bluer_geo_watch_targets get \
            --what collection \
            --target_name Leonardo \
            --log 0) \
        Venus
    [[ $? -ne 0 ]] && return 1

    bluer_ai_assert \
        "$(bluer_geo_watch_targets get \
            --what collection \
            --target_name Deadpool \
            --log 0)" \
        - empty
}

function test_bluer_geo_watch_targets_get_exists() {
    bluer_objects_download - $BLUE_GEO_WATCH_TARGET_LIST

    bluer_ai_assert \
        $(bluer_geo_watch_targets get \
            --what exists \
            --target_name Leonardo \
            --log 0) \
        1
    [[ $? -ne 0 ]] && return 1

    bluer_ai_assert \
        $(bluer_geo_watch_targets get \
            --what exists \
            --target_name Deadpool \
            --log 0) \
        0
}

function test_bluer_geo_watch_targets_get_query_args() {
    bluer_objects_download - $BLUE_GEO_WATCH_TARGET_LIST

    bluer_ai_assert \
        $(bluer_geo_watch_targets get \
            --what query_args \
            --target_name Leonardo \
            --log 0 \
            --delim +) \
        Venus
    [[ $? -ne 0 ]] && return 1

    bluer_ai_assert \
        "$(bluer_geo_watch_targets get \
            --what query_args \
            --target_name Deadpool \
            --log 0 \
            --delim +)" \
        - empty
}
